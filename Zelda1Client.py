# Based (read: copied almost wholesale and edited) off the FF1 Client.

import asyncio
import copy
import json
import logging
import time
from asyncio import StreamReader, StreamWriter
from typing import List


import Utils
from worlds import lookup_any_location_id_to_name
from CommonClient import CommonContext, server_loop, gui_enabled, console_loop, ClientCommandProcessor, logger, \
    get_base_parser

from worlds.tloz.Items import item_game_ids
from worlds.tloz.Locations import location_ids
from worlds.tloz import Items, Locations

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart Zelda_connector.lua"
CONNECTION_REFUSED_STATUS = "Connection Refused. Please start your emulator and make sure Zelda_connector.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart Zelda_connector.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

DISPLAY_MSGS = True

item_ids = item_game_ids
location_ids = location_ids
items_by_id = {id: item for item, id in item_ids.items()}
locations_by_id = {id: location for location, id in location_ids.items()}

class ZeldaCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_nes(self):
        """Check NES Connection State"""
        if isinstance(self.ctx, ZeldaContext):
            logger.info(f"NES Status: {self.ctx.nes_status}")

    def _cmd_toggle_msgs(self):
        """Toggle displaying messages in bizhawk"""
        global DISPLAY_MSGS
        DISPLAY_MSGS = not DISPLAY_MSGS
        logger.info(f"Messages are now {'enabled' if DISPLAY_MSGS  else 'disabled'}")


class ZeldaContext(CommonContext):
    command_processor = ZeldaCommandProcessor
    items_handling = 0b101  # get sent remote and starting items
    # Infinite Hyrule compatibility
    overworld_item = 0x5F
    armos_item = 0x24

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.nes_streams: (StreamReader, StreamWriter) = None
        self.nes_sync_task = None
        self.messages = {}
        self.locations_array = None
        self.nes_status = CONNECTION_INITIAL_STATUS
        self.game = 'The Legend of Zelda'
        self.awaiting_rom = False
        self.display_msgs = True

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ZeldaContext, self).server_auth(password_requested)
        if not self.auth:
            self.awaiting_rom = True
            logger.info('Awaiting connection to NES to get Player information')
            return

        await self.send_connect()

    def _set_message(self, msg: str, msg_id: int):
        if DISPLAY_MSGS:
            self.messages[(time.time(), msg_id)] = msg

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            asyncio.create_task(parse_locations(self.locations_array, self, True))
        elif cmd == 'Print':
            msg = args['text']
            if ': !' not in msg:
                self._set_message(msg, SYSTEM_MESSAGE_ID)

    def on_print_json(self, args: dict):
        if self.ui:
            self.ui.print_json(copy.deepcopy(args["data"]))
        else:
            text = self.jsontotextparser(copy.deepcopy(args["data"]))
            logger.info(text)
        relevant = args.get("type", None) in {"Hint", "ItemSend"}
        if relevant:
            item = args["item"]
            # goes to this world
            if self.slot_concerns_self(args["receiving"]):
                relevant = True
            # found in this world
            elif self.slot_concerns_self(item.player):
                relevant = True
            # not related
            else:
                relevant = False
            if relevant:
                item = args["item"]
                msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                self._set_message(msg, item.item)

    def run_gui(self):
        from kvui import GameManager

        class ZeldaManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Zelda 1 Client"

        self.ui = ZeldaManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def get_payload(ctx: ZeldaContext):
    current_time = time.time()
    return json.dumps(
        {
            "items": [item.item for item in ctx.items_received],
            "messages": {f'{key[0]}:{key[1]}': value for key, value in ctx.messages.items()
                         if key[0] > current_time - 10}
        }
    )


async def parse_locations(locations_array, ctx: ZeldaContext, force: bool, zone="None"):
    if locations_array == ctx.locations_array and not force:
        return
    else:
        # print("New values")
        ctx.locations_array = locations_array
        locations_checked = []
        location = None
        for location in ctx.missing_locations:
            location_name = lookup_any_location_id_to_name[location]

            if location_name in Locations.overworld_locations and zone == "overworld":
                status = locations_array[Locations.major_location_offsets[location_name]]
                if location_name == "Ocean Heart Container":
                    status = locations_array[ctx.overworld_item]
                if location_name == "Armos Knights":
                    status = locations_array[ctx.armos_item]
                if status & 0x10:
                    ctx.locations_checked.add(location)
                    locations_checked.append(location)
            elif location_name in Locations.underworld1_locations and zone == "underworld1":
                status = locations_array[Locations.floor_location_game_offsets_early[location_name]]
                if status & 0x10:
                    ctx.locations_checked.add(location)
                    locations_checked.append(location)
            elif location_name in Locations.underworld2_locations and zone == "underworld2":
                status = locations_array[Locations.floor_location_game_offsets_late[location_name]]
                if status & 0x10:
                    ctx.locations_checked.add(location)
                    locations_checked.append(location)
            elif location_name in  Locations.cave_locations and zone == "caves":
                caveType = "None"
                if "caveType" in locations_array.keys():
                    caveType = locations_array["caveType"]
                if caveType != "None":
                    location_data = f"{caveType} Item {locations_array['itemSlot']}"
                    if location_name == location_data:
                        locations_checked.append(location)
        if locations_checked:
            print([ctx.location_names[location] for location in locations_checked])
            await ctx.send_msgs([
                {"cmd": "LocationChecks",
                 "locations": locations_checked}
            ])


async def nes_sync_task(ctx: ZeldaContext):
    logger.info("Starting nes connector. Use /nes for status information")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.nes_streams:
            (reader, writer) = ctx.nes_streams
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
                    if data_decoded["overworldHC"] is not None:
                        ctx.overworld_item = data_decoded["overworldHC"]
                    if data_decoded["overworldPB"] is not None:
                        ctx.armos_item = data_decoded["overworldPB"]
                    if data_decoded['gameMode'] == 19 and ctx.finished_game == False:
                        await ctx.send_msgs([
                            {"cmd": "StatusUpdate",
                             "status": 30}
                        ])
                        ctx.finished_game = True
                    if ctx.game is not None and 'overworld' in data_decoded:
                        # Not just a keep alive ping, parse
                        asyncio.create_task(parse_locations(data_decoded['overworld'], ctx, False, "overworld"))
                    if ctx.game is not None and 'underworld1' in data_decoded:
                        asyncio.create_task(parse_locations(data_decoded['underworld1'], ctx, False, "underworld1"))
                    if ctx.game is not None and 'underworld2' in data_decoded:
                        asyncio.create_task(parse_locations(data_decoded['underworld2'], ctx, False, "underworld2"))
                    if ctx.game is not None and 'caves' in data_decoded:
                        asyncio.create_task(parse_locations(data_decoded['caves'], ctx, False, "caves"))
                    if not ctx.auth:
                        ctx.auth = ''.join([chr(i) for i in data_decoded['playerName'] if i != 0])
                        if ctx.auth == '':
                            logger.info("Invalid ROM detected. No player name built into the ROM. Please regenerate"
                                        "the ROM using the same link but adding your slot name")
                        if ctx.awaiting_rom:
                            await ctx.server_auth(False)
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.nes_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.nes_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.nes_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.nes_streams = None
            if ctx.nes_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to NES")
                    ctx.nes_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.nes_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.nes_status = error_status
                logger.info("Lost connection to nes and attempting to reconnect. Use /nes for status updates")
        else:
            try:
                logger.debug("Attempting to connect to NES")
                ctx.nes_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 52980), timeout=10)
                ctx.nes_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.nes_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.nes_status = CONNECTION_REFUSED_STATUS
                continue


if __name__ == '__main__':
    # Text Mode to use !hint and such with games that have no text entry
    Utils.init_logging("ZeldaClient")

    options = Utils.get_options()
    DISPLAY_MSGS = options["ffr_options"]["display_msgs"]


    async def main(args):
        print(args)
        if args.diff_file:
            import Patch
            logging.info("Patch file was supplied. Creating nes rom..")
            meta, romfile = Patch.create_rom_file(args.diff_file)
            if "server" in meta:
                args.connect = meta["server"]
            logging.info(f"Wrote rom file to {romfile}")
        ctx = ZeldaContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.nes_sync_task = asyncio.create_task(nes_sync_task(ctx), name="NES Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.nes_sync_task:
            await ctx.nes_sync_task


    import colorama

    parser = get_base_parser()
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a Archipelago Binary Patch file')
    args = parser.parse_args()
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()
