# Based (read: copied almost wholesale and edited) off the TLoZ Client.

import asyncio
import copy
import json
import logging
import random
import time
from typing import cast, Dict, Optional
from asyncio import StreamReader, StreamWriter

import Utils
from Utils import async_start
from NetUtils import ClientStatus
from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, \
    get_base_parser

from worlds.khcom.Items import item_table
from worlds.khcom.Locations import location_table

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart KHDaysRandomizer.lua"
CONNECTION_REFUSED_STATUS = "Connection Refused. Please start your emulator and make sure KHDaysRandomizer.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart KHDaysRandomizer.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

item_ids = {item: id.code for item, id in item_table.items()}
location_ids = location_table
items_by_id = {id: item for item, id in item_ids.items()}
locations_by_id = {id: location for location, id in location_ids.items()}


class KHCOMCommandProcessor(ClientCommandProcessor):

    def _cmd_gba(self):
        """Check GBA Connection State"""
        if isinstance(self.ctx, KHCOMContext):
            logger.info(f"GBA Status: {self.ctx.gba_status}")

class KHCOMContext(CommonContext):
    command_processor = KHCOMCommandProcessor
    items_handling = 0b111  # full remote
    connected = "false"
    locations_array = []

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.bonus_items = []
        self.gba_streams: (StreamReader, StreamWriter) = None
        self.gba_sync_task = None
        self.messages = {}
        self.locations_array = []
        self.gba_status = CONNECTION_INITIAL_STATUS
        self.game = 'Kingdom Hearts Chain of Memories'
        self.awaiting_rom = False
        self.check_locs_count = {}

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(KHCOMContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            slot_data = args["slot_data"]
            self.connected = "true"
            async_start(self.send_msgs([
                {"cmd": "Get",
                "keys": ["received_items"]}
            ]))
        elif cmd == 'Retrieved':
            if "keys" not in args:
                logger.warning(f"invalid Retrieved packet to KHCOMClient: {args}")
                return
            keys = cast(Dict[str, Optional[str]], args["keys"])

    async def connection_closed(self):
        self.connected = "false"
        await super(KHCOMContext, self).connection_closed()

    def on_print_json(self, args: dict):
        if self.ui:
            self.ui.print_json(copy.deepcopy(args["data"]))
        else:
            text = self.jsontotextparser(copy.deepcopy(args["data"]))
            logger.info(text)

    def run_gui(self):
        from kvui import GameManager

        class KHCOMManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago KHCOM Client"

        self.ui = KHCOMManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def get_payload(ctx: KHCOMContext):
    current_time = time.time()
    ctx.check_locs_count = {}
    for item in item_table:
        ctx.check_locs_count[item] = 0
    for item in ctx.checked_locations:
        ctx.check_locs_count["".join([i+" " for i in temp_view[:-1]]).removesuffix(" ")] += 1
    return json.dumps(
        {
            "items": [items_by_id[item.item] for item in ctx.items_received if item.item >= 25000],
            "checked_locs": ctx.check_locs_count,
            "locs_sent": {key: value for key, value in ctx.locations_checked},
            "messages": {f'{key[0]}:{key[1]}': value for key, value in ctx.messages.items()
                         if key[0] > current_time - 10},
            "connection": ctx.connected
        }
    )


async def gba_sync_task(ctx: KHCOMContext):
    logger.info("Starting gba connector. Use /gba for status information")
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
                    ctx.valid_characters = {items_by_id[item.item] for item in ctx.items_received if item.item < 25000}
                    if ctx.game is not None and 'checked_locs' in data_decoded:
                        for i in data_decoded["checked_locs"]:
                            if data_decoded["checked_locs"][i] not in ctx.locations_array:
                                ctx.locations_array.append(data_decoded["checked_locs"][i])
                                if data_decoded["checked_locs"][i] not in ctx.server_locations:
                                    print("Unknown location: "+str(data_decoded["checked_locs"][i]))
                        await ctx.send_msgs([
                            {"cmd": "LocationChecks",
                            "locations": ctx.locations_array}
                        ])
                    if ctx.game is not None and 'day' in data_decoded:
                        if not ctx.finished_game and int(data_decoded["day"]) >= ctx.day_requirement:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
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
                    ctx.locations_array = []
                    logger.info("Successfully Connected to GBA")
                    ctx.gba_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.gba_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.gba_status = error_status
                logger.info("Lost connection to gba and attempting to reconnect. Use /gba for status updates")
        else:
            try:
                logger.debug("Attempting to connect to GBA")
                ctx.gba_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 52987), timeout=10)
                ctx.gba_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.gba_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.gba_status = CONNECTION_REFUSED_STATUS
                continue


if __name__ == '__main__':
    # Text Mode to use !hint and such with games that have no text entry
    Utils.init_logging("KHCOMClient")


    async def main(args):
        if args.diff_file:
            import Patch
            logging.info("Patch file was supplied. Creating gba rom..")
            meta, romfile = Patch.create_rom_file(args.diff_file)
            if "server" in meta:
                args.connect = meta["server"]
            logging.info(f"Wrote rom file to {romfile}")
        ctx = KHCOMContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.gba_sync_task = asyncio.create_task(gba_sync_task(ctx), name="GBA Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.gba_sync_task:
            await ctx.gba_sync_task


    import colorama

    parser = get_base_parser()
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a Archipelago Binary Patch file')
    args = parser.parse_args()
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()