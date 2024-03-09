import asyncio
import json
import time
import os
from asyncio import StreamReader, StreamWriter, CancelledError
from typing import NamedTuple

import Utils
from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, \
    get_base_parser
from NetUtils import ClientStatus
from Utils import async_start, user_path
from worlds import network_data_package, AutoWorldRegister
from worlds.sotn.Items import base_item_id, ItemData, get_item_data, IType
from worlds.sotn.Locations import location_table, LocationData, base_location_id, zones_dict, ZoneData, \
    get_location_data
from worlds.sotn.Rom import pos_patch

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = \
    "Connection timing out. Please restart your emulator, then restart connector_sotn.lua"
CONNECTION_REFUSED_STATUS = \
    "Connection Refused. Please start your emulator and make sure connector_sotn.lua is running"
CONNECTION_RESET_STATUS = \
    "Connection was reset. Please restart your emulator, then restart connector_sotn.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

SCRIPT_VERSION = 1


sotn_loc_name_to_id = network_data_package["games"]["Symphony of the Night"]["location_name_to_id"]


class SotnCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_psx(self):
        """Check PSX Connection State"""
        if isinstance(self.ctx, SotnContext):
            logger.info(f"PSX Status: {self.ctx.psx_status}")

    def _cmd_aconnect(self):
        """Discard current PSX connection state"""
        if isinstance(self.ctx, SotnContext):
            self.ctx.psx_sync_task.cancel()

    def _cmd_missing(self, filter_text = "") -> bool:
        """List all missing location checks, from your local game state.
        Can be given text, which will be used as filter."""
        if not self.ctx.game:
            self.output("No game set, cannot determine missing checks.")
            return False
        count = 0
        checked_count = 0
        for location, location_id in AutoWorldRegister.world_types[self.ctx.game].location_name_to_id.items():
            if filter_text and filter_text not in location:
                continue
            if location_id < 0:
                continue
            if location_id not in self.ctx.locations_checked:
                if location_id in self.ctx.missing_locations:
                    self.output('Missing: ' + location)
                    count += 1
                # Having missing and checked together is weird
                """elif location_id in self.ctx.checked_locations:
                    self.output('Checked: ' + location)
                    count += 1
                    checked_count += 1"""

        if count:
            self.output(
                f"Found {count} missing location checks.")
        else:
            self.output("No missing location checks found.")
        return True

    def _cmd_zones(self):
        """List zones names"""
        if not self.ctx.game:
            self.output("No game set, cannot determine missing checks.")
            return False

        for key, value in zones_dict.items():
            zd: ZoneData = value
            if zd.abrev == "WRP" or zd.abrev == "RWRP" or zd.abrev == "ST0" or zd.abrev == "DRE" or "BO" in zd.abrev:
                continue
            self.output(f'{zd.abrev} - {zd.name}')

    def _cmd_patch(self, patch_dir: str):
        """Patch the ROM with the provided .apsotn(ONLY NAME)"""
        if not os.path.exists(patch_dir + ".apsotn"):
            logger.info(".apsotn not found!")
            return
        if os.path.exists(patch_dir + ".bin"):
            logger.info("Patched ROM found!")
            return
        logger.info("Start patching. Please wait!")
        diff_handler(patch_dir)


class SotnContext(CommonContext):
    command_processor = SotnCommandProcessor
    game = "Symphony of the Night"
    lua_connector_port: int = 17242  # No idea why this number?

    def __init__(self, server_address, password):
        super(SotnContext, self).__init__(server_address, password)
        self.psx_streams: (StreamReader, StreamWriter) = None
        self.psx_sync_task = None
        self.messages = {}
        self.locations_array = None
        self.psx_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.display_msgs = True
        self.client_compatibility_mode = 0
        self.items_handling = 0b101
        self.checked_locations_sent: bool = False
        self.misplaced_items = []
        self.finished_game = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(SotnContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def _set_message(self, msg: str, msg_id: int):
        if self.display_msgs:
            self.messages[(time.time(), msg_id)] = msg

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.locations_array = None
            self.misplaced_items = []
        elif cmd == 'Print':
            msg = args['text']
            if ': !' not in msg:
                self._set_message(msg, SYSTEM_MESSAGE_ID)
        elif cmd == "ReceivedItems":
            msg = f"{', '.join([self.item_names[item.item] for item in args['items']])}"
            self._set_message(msg, SYSTEM_MESSAGE_ID)
        elif cmd == "PrintJSON":
            if 'item' in args:
                message_type: NamedTuple = args['type']
                player: NamedTuple = args['receiving']
                received: NamedTuple = args['item']

                if message_type != "Hint" and (received.location == 127083080 or received.location == 127020003):
                    # Holy glasses and CAT - Mormegil, send a library card, so player won't get stuck
                    # If there are 2 SOTN players at the same time, both might receive a free library card
                    self.misplaced_items.append(166)
                    print("Sending Library Card")

                if message_type != "Hint" and received.player == player:
                    # Check if it's our item first
                    if base_item_id <= received.item <= base_item_id + 423:
                        # Check if the item came from offworld
                        if base_location_id <= received.location <= base_location_id + 310024:
                            loc_data: LocationData = get_location_data(received.location)
                        else:
                            loc_data = None

                        item_data: ItemData = get_item_data(received.item)
                        # Is a exploration token?
                        if 127110031 <= received.location <= 127110050:
                            self.misplaced_items.append(received.item - base_item_id)
                            print("Exploration token")

                        if loc_data is not None:
                            if loc_data.can_be_relic:
                                # There is a item on a relic spot, send it to the player
                                if item_data.type != IType.RELIC:
                                    self.misplaced_items.append(received.item - base_item_id)
                            else:
                                # Normal location containing a relic
                                if item_data.type == IType.RELIC:
                                    self.misplaced_items.append(received.item - base_item_id)
        elif cmd == "RoomInfo":
            self.seed_name = args['seed_name']

    def run_gui(self):
        import webbrowser
        from kvui import GameManager, Button

        class SotnManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Sotn Client"

            def build(self):
                b = super().build()

                button1 = Button(text="1", size=(30, 30), size_hint_x=None,
                                on_press=lambda _:
                                webbrowser.open('https://shrines.rpgclassics.com/psx/castlevsn/map.shtml'))
                self.connect_layout.add_widget(button1)

                button2 = Button(text="2", size=(30, 30), size_hint_x=None,
                                 on_press=lambda _:
                                 webbrowser.open('https://www.deviantart.com/kamenriderninja/art/'
                                                 'Castlevania-Symphony-of-the-Night-Map-340872423'))
                self.connect_layout.add_widget(button2)

                return b

        self.ui = SotnManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def convert_item_id(ap_item_id: int):
    static_item_index = ap_item_id - base_item_id
    return static_item_index


def get_payload(ctx: SotnContext):
    current_time = time.time()
    items = []

    for item in ctx.items_received:
        items.append(convert_item_id(item.item))

    ret = json.dumps(
        {
            "items": items,
            "messages": {f'{key[0]}:{key[1]}': value for key, value in ctx.messages.items()
                         if key[0] > current_time - 10},
            "player": ctx.username,
            "seed_name": ctx.seed_name,
            "misplaced": [i for i in ctx.misplaced_items]
        }
    )

    return ret


async def parse_locations(data: dict, ctx: SotnContext):
    locations = data
    checked = []
    ld: LocationData

    if not locations or locations == ctx.locations_array:
        return
    ctx.locations_array = locations
    if locations is not None:
        for key, value in locations.items():
            if value:
                ld = location_table[key]
                checked.append(ld.location_id)
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checked}])
        if not ctx.checked_locations_sent and len(checked) > 0:
            payload = json.dumps(
                {
                    "checked_locations": checked,
                }
            )
            msg = payload.encode()
            (reader, writer) = ctx.psx_streams
            writer.write(msg)
            writer.write(b'\n')
            ctx.checked_locations_sent = True


async def parse_bosses(data: dict, ctx: SotnContext):
    bosses = data

    if not bosses:
        return

    if "Dracula" in bosses:
        if bosses["Dracula"] and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True


async def psx_sync_task(ctx: SotnContext):
    logger.info("Starting PSX connector. Use /psx for status information")
    while not ctx.exit_event.is_set():
        try:
            error_status = None
            if ctx.psx_streams:
                (reader, writer) = ctx.psx_streams
                msg = get_payload(ctx).encode()
                writer.write(msg)
                writer.write(b'\n')
                try:
                    await asyncio.wait_for(writer.drain(), timeout=1.5)
                    try:
                        data = await asyncio.wait_for(reader.readline(), timeout=5)
                        data_decoded = json.loads(data.decode())
                        if 'scriptVersion' not in data_decoded or data_decoded['scriptVersion'] != SCRIPT_VERSION:
                            msg = "You are connecting with an incompatible Lua script version. Ensure your connector " \
                                  "Lua and SotnClient are from the same Archipelago installation."
                            logger.info(msg, extra={'compact_gui': True})
                            ctx.gui_error('Error', msg)
                            error_status = CONNECTION_RESET_STATUS
                        if 'locations' in data_decoded and ctx.game and ctx.psx_status == CONNECTION_CONNECTED_STATUS \
                                and not error_status and ctx.auth:
                            # Not just a keep alive ping, parse
                            async_start(parse_locations(data_decoded['locations'], ctx))
                        if 'bosses' in data_decoded and ctx.game and ctx.psx_status == CONNECTION_CONNECTED_STATUS \
                                and not error_status and ctx.auth:
                            async_start(parse_bosses(data_decoded['bosses'], ctx))
                        if 'victory' in data_decoded and not ctx.finished_game:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                    except asyncio.TimeoutError:
                        logger.debug("Read Timed Out, Reconnecting")
                        error_status = CONNECTION_TIMING_OUT_STATUS
                        writer.close()
                        ctx.psx_streams = None
                    except ConnectionResetError as e:
                        logger.debug("Read failed due to Connection Lost, Reconnecting")
                        error_status = CONNECTION_RESET_STATUS
                        writer.close()
                        ctx.psx_streams = None
                except TimeoutError:
                    logger.debug("Connection Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.psx_streams = None
                except ConnectionResetError:
                    logger.debug("Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.psx_streams = None
                except CancelledError:
                    logger.debug("Connection Cancelled, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.psx_streams = None
                    pass
                except Exception as e:
                    print("unknown exception " + e)
                    raise
                if ctx.psx_status == CONNECTION_TENTATIVE_STATUS:
                    if not error_status:
                        logger.info("Successfully Connected to PSX")
                        ctx.psx_status = CONNECTION_CONNECTED_STATUS
                        ctx.checked_locations_sent = False
                    else:
                        ctx.psx_status = f"Was tentatively connected but error occurred: {error_status}"
                elif error_status:
                    ctx.psx_status = error_status
                    logger.info("Lost connection to PSX and attempting to reconnect. Use /psx for status updates")
            else:
                try:
                    port = ctx.lua_connector_port
                    logger.debug(f"Attempting to connect to PSX on port {port}")
                    print(f"Attempting to connect to PSX on port {port}")
                    ctx.psx_streams = await asyncio.wait_for(
                        asyncio.open_connection("localhost",
                                                port),
                        timeout=10)
                    ctx.psx_status = CONNECTION_TENTATIVE_STATUS
                except TimeoutError:
                    logger.debug("Connection Timed Out, Trying Again")
                    ctx.psx_status = CONNECTION_TIMING_OUT_STATUS
                    continue
                except ConnectionRefusedError:
                    logger.debug("Connection Refused, Trying Again")
                    ctx.psx_status = CONNECTION_REFUSED_STATUS
                    continue
                except CancelledError:
                    pass
        except CancelledError:
            pass
    print("exiting PSX sync task")


def diff_handler(diff_file: str):
    logger.info("Handling patch")
    if diff_file:
        try:
            logger.info("Patching game")
            source1 = os.path.splitext(diff_file)[0]
            try:
                name_start = source1.index("AP_")
            except ValueError:
                logger.info("File not an AP format ")
                return
            source1 = source1[name_start:] + ".bin"
            source2 = "Castlevania - Symphony of the Night (USA) (Track 2).bin"
            destination = os.path.splitext(diff_file)[0] + ".cue"

            logger.info(pos_patch(os.path.splitext(diff_file)[0]))

            cue_file = f'FILE "{source1}" BINARY\n  TRACK 01 MODE2/2352\n\tINDEX 01 00:00:00\n'
            cue_file += f'FILE "{source2}" BINARY\n  TRACK 02 AUDIO\n'
            cue_file += f'\tINDEX 00 00:00:00\n\tINDEX 01 00:02:00'
            with open(destination, 'wb') as outfile:
                outfile.write(bytes(cue_file, 'utf-8'))
        except Exception as e:
            Utils.messagebox('Error', str(e), True)
            raise
        logger.info("All done!")

def main():

    Utils.init_logging("SotnClient")

    async def main():
        parser = get_base_parser()
        parser.add_argument('diff_file', default="", type=str, nargs="?",
                            help='Path to a Archipelago Binary Patch file')
        parser.add_argument('port', default=17242, type=int, nargs="?",
                            help='port for sotn_connector connection')
        args = parser.parse_args()

        if args.diff_file:
            try:
                diff_handler(args.diff_file)
            except Exception as e:
                Utils.messagebox('Error', str(e), True)
                raise

        ctx = SotnContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.psx_sync_task = asyncio.create_task(psx_sync_task(ctx), name="Sotn Sync")

        if args.port is int:
            ctx.lua_connector_port = args.port

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.psx_sync_task:
            await ctx.psx_sync_task
            print("finished PSX_sync_task (main)")


    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()


if __name__ == '__main__':
    main()
