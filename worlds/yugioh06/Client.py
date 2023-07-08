import asyncio
import json
import math
import time
import os
import bsdiff4
import subprocess
import zipfile
from asyncio import StreamReader, StreamWriter
from typing import List


import Utils
from NetUtils import NetworkItem
from Utils import async_start
from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, \
    get_base_parser

from worlds.yugioh06.Rom import YGO06DeltaPatch
SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart pkmn_rb.lua"
CONNECTION_REFUSED_STATUS = "Connection Refused. Please start your emulator and make sure pkmn_rb.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart pkmn_rb.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

DISPLAY_MSGS = True

SCRIPT_VERSION = 1


class GBACommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_gba(self):
        """Check Gameboy Connection State"""
        if isinstance(self.ctx, GBAContext):
            logger.info(f"Gameboy Status: {self.ctx.gba_status}")


class GBAContext(CommonContext):
    command_processor = GBACommandProcessor
    game = 'Yu-Gi-Oh! 2006'

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gba_streams: (StreamReader, StreamWriter) = None
        self.gba_sync_task = None
        self.messages = {}
        self.locations_array = None
        self.gba_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.display_msgs = True
        self.deathlink_pending = False
        self.set_deathlink = False
        self.client_compatibility_mode = 0
        self.items_handling = 0b001
        self.sent_release = False
        self.sent_collect = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(GBAContext, self).server_auth(password_requested)
        if not self.auth:
            self.awaiting_rom = True
            logger.info('Awaiting connection to Bizhawk to get Player information')
            return

        await self.send_connect()

    def _set_message(self, msg: str, msg_id: int):
        if DISPLAY_MSGS:
            self.messages[(time.time(), msg_id)] = msg

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.locations_array = None
            if 'death_link' in args['slot_data'] and args['slot_data']['death_link']:
                self.set_deathlink = True
        elif cmd == "RoomInfo":
            self.seed_name = args['seed_name']
        elif cmd == 'Print':
            msg = args['text']
            if ': !' not in msg:
                self._set_message(msg, SYSTEM_MESSAGE_ID)
        elif cmd == "ReceivedItems":
            msg = f"Received {', '.join([self.item_names[item.item] for item in args['items']])}"
            self._set_message(msg, SYSTEM_MESSAGE_ID)

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    def run_gui(self):
        from kvui import GameManager

        class GBAManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Yu-Gi-Oh! 2006 Client"

        self.ui = GBAManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def get_payload(ctx: GBAContext):
    current_time = time.time()
    ret = json.dumps(
        {
            "items": parse_items(ctx.items_received),
            "messages": {f'{key[0]}:{key[1]}': value for key, value in ctx.messages.items()
                         if key[0] > current_time - 10},
            "deathlink": ctx.deathlink_pending,
            "options": ((ctx.permissions['release'] in ('goal', 'enabled')) * 2) + (ctx.permissions['collect'] in ('goal', 'enabled'))
        }
    )
    ctx.deathlink_pending = False
    return ret


def parse_items(items: List[NetworkItem]):
    array = [0] * 32
    for item in items:
        index = item.item - 5730001
        if index == 253:
            array[31] += 1
        else:
            byte = math.floor(index / 8)
            bit = index % 8
            array[byte] = array[byte] | (1 << bit)
    return array


async def parse_locations(locations_array: List[int], ctx: GBAContext):
    if locations_array == ctx.locations_array:
        return
    else:
        ctx.locations_array = locations_array
        locations_checked = []
        for location in ctx.missing_locations:
            lId = (location % 5730000) - 1
            index = math.floor(lId / 8)
            bit = lId % 8
            if locations_array[index] & (1 << bit) != 0:
                locations_checked.append(location)
        if locations_checked:
            # print([ctx.location_names[location] for location in locations_checked])
            await ctx.send_msgs([
                {"cmd": "LocationChecks",
                 "locations": locations_checked}
            ])
        if locations_array[18] & (1 << 5) != 0:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": 30
            }])
            ctx.finished_game = True


async def gba_sync_task(ctx: GBAContext):
    logger.info("Starting GBA connector. Use /gba for status information")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.gba_streams:
            (reader, writer) = ctx.gba_streams
            msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    # Data will return a dict with up to two fields:
                    # 1. A keepalive response of the Players Name (always)
                    # 2. An array representing the memory values of the locations area (if in game)
                    data = await asyncio.wait_for(reader.readline(), timeout=5)
                    data_decoded = json.loads(data.decode())
                    if 'scriptVersion' not in data_decoded or data_decoded['scriptVersion'] != SCRIPT_VERSION:
                        msg = "You are connecting with an incompatible Lua script version. Ensure your connector Lua " \
                            "and YuGiOh06Client are from the same Archipelago installation."
                        logger.info(msg, extra={'compact_gui': True})
                        ctx.gui_error('Error', msg)
                        error_status = CONNECTION_RESET_STATUS
                    if not ctx.auth:
                        ctx.auth = ''.join([chr(i) for i in data_decoded['playerName'] if i != 0])
                        logger.info(ctx.auth)
                        if ctx.auth == '':
                            logger.info("Invalid ROM detected. No player name built into the ROM. Please regenerate"
                                        "the ROM using the same link but adding your slot name")
                        if ctx.awaiting_rom:
                            await ctx.server_auth(False)
                    if 'locations' in data_decoded and ctx.game and ctx.gba_status == CONNECTION_CONNECTED_STATUS \
                            and not error_status and ctx.auth:
                        # Not just a keep alive ping, parse
                        async_start(parse_locations(data_decoded['locations'], ctx))
                    if 'deathLink' in data_decoded and data_decoded['deathLink'] and 'DeathLink' in ctx.tags:
                        await ctx.send_death(ctx.auth + " lost all of his life points")
                    if 'options' in data_decoded:
                        msgs = []
                        if data_decoded['options'] & 4 and not ctx.sent_release:
                            ctx.sent_release = True
                            msgs.append({"cmd": "Say", "text": "!release"})
                        if data_decoded['options'] & 8 and not ctx.sent_collect:
                            ctx.sent_collect = True
                            msgs.append({"cmd": "Say", "text": "!collect"})
                        if msgs:
                            await ctx.send_msgs(msgs)
                    if ctx.set_deathlink:
                        await ctx.update_death_link(True)
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.gba_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.gba_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.gba_streams = None
            if ctx.gba_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to Gameboy")
                    ctx.gba_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.gba_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.gba_status = error_status
                logger.info("Lost connection to Gameboy and attempting to reconnect. Use /gb for status updates")
        else:
            try:
                logger.debug("Attempting to connect to Gameboy")
                ctx.gba_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 17242), timeout=10)
                ctx.gba_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.gba_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.gba_status = CONNECTION_REFUSED_STATUS
                continue


async def run_game(romfile):
    auto_start = True# Utils.get_options()["ygo06_options"].get("rom_start", True)
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(patch_file, ctx):
    base_name = os.path.splitext(patch_file)[0]
    comp_path = base_name + '.gba'
    delta_patch = YGO06DeltaPatch

    try:
        base_rom = delta_patch.get_source_data()
    except Exception as msg:
        logger.info(msg, extra={'compact_gui': True})
        ctx.gui_error('Error', msg)

    with zipfile.ZipFile(patch_file, 'r') as patch_archive:
        with patch_archive.open('delta.bsdiff4', 'r') as stream:
            patch = stream.read()
    patched_rom_data = bsdiff4.patch(base_rom, patch)

    with open(comp_path, "wb") as patched_rom_file:
        patched_rom_file.write(patched_rom_data)

    async_start(run_game(comp_path))


async def main(args):

    ctx = GBAContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    ctx.gba_sync_task = asyncio.create_task(gba_sync_task(ctx), name="GBA Sync")

    if args.patch_file:
        ext = args.patch_file.split(".")[len(args.patch_file.split(".")) - 1].lower()
        if ext == "apygo06":
            logger.info("APYGO06 file supplied, beginning patching process...")
            async_start(patch_and_run_game(args.patch_file, ctx))
        else:
            logger.warning(f"Unknown patch file extension {ext}")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await ctx.shutdown()

    if ctx.gba_sync_task:
        await ctx.gba_sync_task

parser = get_base_parser()
parser.add_argument('patch_file', default="", type=str, nargs="?",
                            help='Path to an APYGO06 patch file')
args = parser.parse_args()

Utils.init_logging("YuGiOh06Client")

options = Utils.get_options()


def launch():
    import colorama

    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()
