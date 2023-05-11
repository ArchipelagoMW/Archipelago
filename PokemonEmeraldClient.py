import asyncio
import json
import os
import subprocess
from typing import Optional, Set, Tuple
import zipfile

import bsdiff4

from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, server_loop, gui_enabled, logger
from NetUtils import ClientStatus
from Utils import async_start, init_logging, get_options

from worlds.pokemon_emerald.data import data, config
from worlds.pokemon_emerald.rom import PokemonEmeraldDeltaPatch
from worlds.pokemon_emerald.options import Goal


GBA_SOCKET_PORT = 43053

CONNECTION_STATUS_TIMING_OUT = "Connection timing out. Please restart your emulator, then restart pokemon_emerald_connector.lua"
CONNECTION_STATUS_REFUSED = "Connection refused. Please start your emulator and make sure pokemon_emerald_connector.lua is running"
CONNECTION_STATUS_RESET = "Connection was reset. Please restart your emulator, then restart pokemon_emerald_connector.lua"
CONNECTION_STATUS_TENTATIVE = "Initial connection made"
CONNECTION_STATUS_CONNECTED = "Connected"
CONNECTION_STATUS_INITIAL = "Connection has not been initiated"

IS_CHAMPION_FLAG = data.constants["FLAG_IS_CHAMPION"]
DEFEATED_STEVEN_FLAG = data.constants["TRAINER_FLAGS_START"] + data.constants["TRAINER_STEVEN"]


class GBACommandProcessor(ClientCommandProcessor):
    def _cmd_gba(self):
        """Check GBA Connection State"""
        if isinstance(self.ctx, GBAContext):
            logger.info(f"GBA Status: {self.ctx.gba_status}")


class GBAContext(CommonContext):
    game = "Pokemon Emerald"
    command_processor = GBACommandProcessor
    items_handling = 0b001
    gba_streams: Optional[Tuple[asyncio.StreamReader, asyncio.StreamWriter]]
    gba_status: Optional[str]
    awaiting_rom = False
    gba_push_pull_task: Optional[asyncio.Task]
    local_checked_locations: Set[int]
    goal_flag: int = IS_CHAMPION_FLAG

    def __init__(self, server_address: Optional[str], password: Optional[str]):
        super().__init__(server_address, password)
        self.gba_streams = None
        self.gba_status = CONNECTION_STATUS_INITIAL
        self.gba_push_pull_task = None
        self.local_checked_locations = set()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(GBAContext, self).server_auth(password_requested)
        if self.auth is None:
            self.awaiting_rom = True
            logger.info('Awaiting connection to GBA to get Player information')
            return
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class GBAManager(GameManager):
            base_title = "Archipelago Pokémon Emerald Client"

        self.ui = GBAManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd, args):
        if cmd == 'Connected':
            slot_data = args.get('slot_data', None)
            if slot_data is not None:
                if slot_data.goal == Goal.option_champion:
                    self.goal_flag = IS_CHAMPION_FLAG
                elif slot_data.goal == Goal.option_steven:
                    self.goal_flag = DEFEATED_STEVEN_FLAG


def create_payload(ctx: GBAContext):
    payload = json.dumps({
        "items": [[item.item - config["ap_offset"], item.flags & 1] for item in ctx.items_received]
    })

    return payload


async def handle_read_data(gba_data, ctx: GBAContext):
    local_checked_locations = set()
    game_clear = False

    if "slot_name" in gba_data:
        if ctx.auth is None:
            ctx.auth = bytes([byte for byte in gba_data["slot_name"] if byte != 0]).decode()
            if ctx.awaiting_rom:
                await ctx.server_auth(False)

    if "flag_bytes" in gba_data:
        # If flag is set and corresponds to a location, add to local_checked_locations
        for byte_i, byte in enumerate(gba_data["flag_bytes"]):
            for i in range(8):
                if byte & (1 << i) != 0:
                    flag_id = byte_i * 8 + i
                    location_id = flag_id + config["ap_offset"]
                    if location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)
                    if flag_id == ctx.goal_flag:
                        game_clear = True

        if local_checked_locations != ctx.local_checked_locations:
            ctx.local_checked_locations = local_checked_locations

            if local_checked_locations is not None:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(local_checked_locations)
                }])

        if not ctx.finished_game and game_clear:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])


async def gba_send_receive_task(ctx: GBAContext):
    logger.info("Starting GBA connector. Use /gba for status information")
    while not ctx.exit_event.is_set():
        error_status: Optional[str] = None

        if ctx.gba_streams is None:
            # Make initial connection
            try:
                logger.debug("Attempting to connect to GBA...")
                ctx.gba_streams = await asyncio.wait_for(asyncio.open_connection("localhost", GBA_SOCKET_PORT), timeout=10)
                ctx.gba_status = CONNECTION_STATUS_TENTATIVE
            except TimeoutError:
                logger.debug("Connection to GBA timed out. Retrying.")
                ctx.gba_status = CONNECTION_STATUS_TIMING_OUT
                continue
            except ConnectionRefusedError:
                logger.debug("Connection to GBA refused. Retrying.")
                ctx.gba_status = CONNECTION_STATUS_REFUSED
                continue
        else:
            (reader, writer) = ctx.gba_streams

            message = create_payload(ctx).encode()
            writer.write(message)
            writer.write(b"\n")

            if error_status:
                ctx.gb_status = error_status
                logger.info("Lost connection to GBA and attempting to reconnect. Use /gba for status updates")
            elif ctx.gba_status == CONNECTION_STATUS_TENTATIVE:
                logger.info("Connected to GBA")
                ctx.gba_status = CONNECTION_STATUS_CONNECTED

            # Write
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
            except TimeoutError:
                logger.debug("Connection to GBA timed out. Reconnecting.")
                error_status = CONNECTION_STATUS_TIMING_OUT
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug("Connection to GBA lost. Reconnecting.")
                error_status = CONNECTION_STATUS_RESET
                writer.close()
                ctx.gba_streams = None

            # Read
            try:
                data_bytes = await asyncio.wait_for(reader.readline(), timeout=5)
                data_decoded = json.loads(data_bytes.decode())
                async_start(handle_read_data(data_decoded, ctx))
            except TimeoutError:
                logger.debug("Connection to GBA timed out during read. Reconnecting.")
                error_status = CONNECTION_STATUS_TIMING_OUT
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug("Connection to GBA lost during read. Reconnecting.")
                error_status = CONNECTION_STATUS_RESET
                writer.close()
                ctx.gba_streams = None


async def run_game(rom_file_path):
    auto_start = get_options()["pokemon_emerald_options"].get("rom_start", True)
    if auto_start is True:
        import webbrowser
        webbrowser.open(rom_file_path)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, rom_file_path],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(patch_file_path, ctx):
    base_name = os.path.splitext(patch_file_path)[0]
    output_file_path = base_name + '.gba'

    try:
        base_rom = PokemonEmeraldDeltaPatch.get_source_data()
    except Exception as msg:
        logger.info(msg, extra={'compact_gui': True})
        ctx.gui_error('Error', msg)

    with zipfile.ZipFile(patch_file_path, 'r') as patch_archive:
        with patch_archive.open('delta.bsdiff4', 'r') as stream:
            patch = stream.read()
    patched_rom_data = bsdiff4.patch(base_rom, patch)

    with open(output_file_path, "wb") as patched_rom_file:
        patched_rom_file.write(patched_rom_data)

    async_start(run_game(output_file_path))


if __name__ == "__main__":
    init_logging("PokemonEmeraldClient")

    async def main(args):
        ctx = GBAContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        if args.apemerald_file:
            logger.info("Beginning patching process...")
            async_start(patch_and_run_game(args.apemerald_file, ctx))

        ctx.gba_push_pull_task = asyncio.create_task(gba_send_receive_task(ctx), name="GBA Push/Pull")

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser()
    parser.add_argument("apemerald_file", default="", type=str, nargs="?", help="Path to an APEMERALD file")
    args = parser.parse_args()

    colorama.init()

    asyncio.run(main(args))

    colorama.deinit()
