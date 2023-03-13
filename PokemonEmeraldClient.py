import asyncio
import json
from typing import Optional, Set, Tuple

from CommonClient import CommonContext, get_base_parser, gui_enabled, logger
from Utils import async_start, init_logging


GBA_PORT = 43053

# TODO: Update messages
CONNECTION_STATUS_TIMING_OUT = "Connection timing out. Please restart your emulator, then restart pkmn_rb.lua"
CONNECTION_STATUS_REFUSED = "Connection refused. Please start your emulator and make sure pkmn_rb.lua is running"
CONNECTION_STATUS_RESET = "Connection was reset. Please restart your emulator, then restart pkmn_rb.lua"
CONNECTION_STATUS_TENTATIVE = "Initial connection made"
CONNECTION_STATUS_CONNECTED = "Connected"
CONNECTION_STATUS_INITIAL = "Connection has not been initiated"


class GBAContext(CommonContext):
    game = "Pokemon Emerald"
    items_handling = 0b001
    gba_streams: Optional[Tuple[asyncio.StreamReader, asyncio.StreamWriter]]
    gba_status: Optional[str]
    gba_push_pull_task: Optional[asyncio.Task]
    local_checked_locations: Set[int]

    def __init__(self, server_address: Optional[str], password: Optional[str]):
        super().__init__(server_address, password)
        self.gba_streams = None
        self.gba_status = None
        self.gba_push_pull_task = None
        self.local_checked_locations = set()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(GBAContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
    
    def run_gui(self):
        from kvui import GameManager

        class GBAManager(GameManager):
            base_title = "Archipelago Pokémon Emerald Client"
        
        self.ui = GBAManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def create_payload(ctx: GBAContext):
    payload = json.dumps(
        {
            "items": ctx.items_received
        }
    )
    return payload


async def handle_read_data(data, ctx: GBAContext):
    local_checked_locations = set()

    # If flag is set and corresponds to a location, add to local_checked_locations
    for byte_i, byte in enumerate(data["flag_bytes"]):
        for i in range(8):
            if (byte & (1 << i) != 0):
                flag_id = byte_i * 8 + i
                location_id = flag_id + 3860000
                if (location_id in ctx.server_locations):
                    local_checked_locations.add(location_id)

    if (local_checked_locations != ctx.local_checked_locations):
        ctx.local_checked_locations = local_checked_locations

        if (local_checked_locations != None):
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(local_checked_locations)
            }])


async def gba_send_receive_task(ctx: GBAContext):
    while (not ctx.exit_event.is_set()):
        error_status: Optional[str] = None

        if (ctx.gba_streams == None):
            # Make initial connection
            try:
                logger.debug("Attempting to connect to GBA...")
                ctx.gba_streams = await asyncio.wait_for(asyncio.open_connection("localhost", GBA_PORT), timeout=10)
                logger.debug("Connected to GBA")
                ctx.gba_status = CONNECTION_STATUS_TENTATIVE
            except TimeoutError:
                logger.debug("Connection timed out. Retrying.")
                ctx.gba_status = CONNECTION_STATUS_TIMING_OUT
                continue
            except ConnectionRefusedError:
                logger.debug("Connection timed out. Retrying.")
                ctx.gba_status = CONNECTION_STATUS_REFUSED
                continue
        else:
            (reader, writer) = ctx.gba_streams

            message = create_payload(ctx).encode()
            writer.write(message)
            writer.write(b"\n")

            # Write
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
            except TimeoutError:
                logger.debug("Connection timed out. Reconnecting.")
                error_status = CONNECTION_STATUS_TIMING_OUT
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug("Connection lost. Reconnecting.")
                error_status = CONNECTION_STATUS_RESET
                writer.close()
                ctx.gba_streams = None

            # Read
            try:
                data_bytes = await asyncio.wait_for(reader.readline(), timeout=5)
                data = json.loads(data_bytes.decode())
                async_start(handle_read_data(data, ctx))
            except TimeoutError:
                logger.debug("Connection timed out during read. Reconnecting.")
                error_status = CONNECTION_STATUS_TIMING_OUT
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug("Connection lost during read. Reconnecting.")
                error_status = CONNECTION_STATUS_RESET
                writer.close()
                ctx.gba_streams = None


if __name__ == "__main__":
    init_logging("PokemonEmeraldClient", loglevel="debug")

    async def main(args):
        ctx = GBAContext(args.connect, args.password)
        ctx.server_task

        if (gui_enabled):
            ctx.run_gui()
        ctx.run_cli()

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
