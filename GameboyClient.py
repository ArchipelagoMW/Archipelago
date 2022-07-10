import asyncio
import json
import time
from asyncio import StreamReader, StreamWriter
from typing import List


import Utils
from CommonClient import CommonContext, server_loop, gui_enabled, console_loop, ClientCommandProcessor, logger, \
    get_base_parser

from worlds.pokemon_rb.locations import get_locations, Rod, EventFlag, Missable, Hidden
location_data = get_locations()
location_map = {"Rod": {}, "EventFlag": {}, "Missable": {}, "Hidden": {}}
location_bytes_bits = {}
for location in location_data:
    if location.ram_address is not None:
        location_map[type(location.ram_address).__name__][location.ram_address.flag] = location.address
        location_bytes_bits[location.address] = {'byte': location.ram_address.byte, 'bit': location.ram_address.bit}

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart pkmn_rb.lua"
CONNECTION_REFUSED_STATUS = "Connection Refused. Please start your emulator and make sure pkmn_rb.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart pkmn_rb.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

DISPLAY_MSGS = True


class GBCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_gb(self):
        """Check Gameboy Connection State"""
        if isinstance(self.ctx, GBContext):
            logger.info(f"Gameboy Status: {self.ctx.gb_status}")

    def _cmd_toggle_msgs(self):
        """Toggle displaying messages in bizhawk"""
        global DISPLAY_MSGS
        DISPLAY_MSGS = not DISPLAY_MSGS
        logger.info(f"Messages are now {'enabled' if DISPLAY_MSGS  else 'disabled'}")


class GBContext(CommonContext):
    command_processor = GBCommandProcessor
    game = 'Pokemon Red and Blue'
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gb_streams: (StreamReader, StreamWriter) = None
        self.gb_sync_task = None
        self.messages = {}
        self.locations_array = None
        self.gb_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.display_msgs = True

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(GBContext, self).server_auth(password_requested)
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
            asyncio.create_task(parse_locations(self.locations_array, self, True))
        elif cmd == 'Print':
            msg = args['text']
            if ': !' not in msg:
                self._set_message(msg, SYSTEM_MESSAGE_ID)
        elif cmd == "ReceivedItems":
            msg = f"Received {', '.join([self.item_names[item.item] for item in args['items']])}"
            self._set_message(msg, SYSTEM_MESSAGE_ID)
        elif cmd == 'PrintJSON':
            print_type = args['type']
            item = args['item']
            receiving_player_id = args['receiving']
            receiving_player_name = self.player_names[receiving_player_id]
            sending_player_id = item.player
            sending_player_name = self.player_names[item.player]
            if print_type == 'Hint':
                msg = f"Hint: Your {self.item_names[item.item]} is at" \
                      f" {self.player_names[item.player]}'s {self.location_names[item.location]}"
                self._set_message(msg, item.item)
            elif print_type == 'ItemSend' and receiving_player_id != self.slot:
                if sending_player_id == self.slot:
                    if receiving_player_id == self.slot:
                        msg = f"You found your own {self.item_names[item.item]}"
                    else:
                        msg = f"You sent {self.item_names[item.item]} to {receiving_player_name}"
                else:
                    if receiving_player_id == sending_player_id:
                        msg = f"{sending_player_name} found their {self.item_names[item.item]}"
                    else:
                        msg = f"{sending_player_name} sent {self.item_names[item.item]} to " \
                              f"{receiving_player_name}"
                self._set_message(msg, item.item)

    def run_gui(self):
        from kvui import GameManager

        class GBManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Gameboy Client"

        self.ui = GBManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def get_payload(ctx: GBContext):
    current_time = time.time()
    return json.dumps(
        {
            "items": [item.item for item in ctx.items_received],
            "messages": {f'{key[0]}:{key[1]}': value for key, value in ctx.messages.items()
                         if key[0] > current_time - 10}
        }
    )


async def parse_locations(data: List, ctx: GBContext, force=False):
    if force:
        locations = data
    else:
        #locations = {"EventFlag": {}, "Missable": {}, "Hidden": {}, "Rod": {}}
        locations = []
        flags = {"EventFlag": data[:0x140], "Missable": data[0x140:0x140 + 0x20],
                 "Hidden": data[0x140 + 0x20: 0x140 + 0x20 + 0x0E], "Rod": data[0x140 + 0x20 + 0x0E:]}
        for flag_type, loc_map in location_map.items():
            #locations[flag_type] = {}
            for flag, loc_id in loc_map.items():
                try:
                    if flags[flag_type][location_bytes_bits[loc_id]['byte']] & 1 << location_bytes_bits[loc_id]['bit']:
                        locations.append(loc_id)
                except:
                    breakpoint()
        if locations == ctx.locations_array:
            return
        ctx.locations_array = locations
    print(locations)
    if locations is not None:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations}])

    #print(locations_array)

    # else:
    #     # print("New values")
    #     ctx.locations_array = locations_array
    #     locations_checked = []
    #     if len(locations_array) > 0xFE and locations_array[0xFE] & 0x02 != 0 and not ctx.finished_game:
    #         await ctx.send_msgs([
    #             {"cmd": "StatusUpdate",
    #              "status": 30}
    #         ])
    #         ctx.finished_game = True
    #     for location in ctx.missing_locations:
    #         # index will be - 0x100 or 0x200
    #         index = location
    #         if location < 0x200:
    #             # Location is a chest
    #             index -= 0x100
    #             flag = 0x04
    #         else:
    #             # Location is an NPC
    #             index -= 0x200
    #             flag = 0x02
    #
    #         # print(f"Location: {ctx.location_names[location]}")
    #         # print(f"Index: {str(hex(index))}")
    #         # print(f"value: {locations_array[index] & flag != 0}")
    #         if locations_array[index] & flag != 0:
    #             locations_checked.append(location)
    #     if locations_checked:
    #         # print([ctx.location_names[location] for location in locations_checked])
    #         await ctx.send_msgs([
    #             {"cmd": "LocationChecks",
    #              "locations": locations_checked}
    #         ])


async def gb_sync_task(ctx: GBContext):
    logger.info("Starting GB connector. Use /gb for status information")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.gb_streams:
            (reader, writer) = ctx.gb_streams
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
                    #print(data_decoded)
                    if ctx.game is not None and 'locations' in data_decoded:
                        # Not just a keep alive ping, parse
                        asyncio.create_task(parse_locations(data_decoded['locations'], ctx, False))
                    if not ctx.auth:
                        ctx.auth = ''.join([chr(i) for i in data_decoded['playerName'] if i != 0])
                        if ctx.auth == '':
                            logger.info("Invalid ROM detected. No player name built into the ROM.")
                        print("NAME: " + ctx.auth)
                        if ctx.awaiting_rom:
                            await ctx.server_auth(False)
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.gb_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.gb_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.gb_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.gb_streams = None
            if ctx.gb_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to Gameboy")
                    ctx.gb_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.gb_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.gb_status = error_status
                logger.info("Lost connection to Gameboy and attempting to reconnect. Use /gb for status updates")
        else:
            try:
                logger.debug("Attempting to connect to Gameboy")
                ctx.gb_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 17242), timeout=10)
                ctx.gb_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.gb_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.gb_status = CONNECTION_REFUSED_STATUS
                continue


if __name__ == '__main__':
    # Text Mode to use !hint and such with games that have no text entry
    Utils.init_logging("GameboyClient")

    options = Utils.get_options()
    DISPLAY_MSGS = options["ffr_options"]["display_msgs"]

    async def main(args):
        ctx = GBContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.gb_sync_task = asyncio.create_task(gb_sync_task(ctx), name="GB Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.gb_sync_task:
            await ctx.gb_sync_task


    import colorama

    parser = get_base_parser()
    args = parser.parse_args()
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()
