import asyncio
import hashlib
import json
import time
import os
import bsdiff4
import subprocess
import zipfile
from asyncio import StreamReader, StreamWriter, CancelledError
from typing import List


import Utils
from NetUtils import ClientStatus
from Utils import async_start
from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, \
    get_base_parser
from worlds.adventure import AdventureDeltaPatch

from worlds.adventure.Locations import base_location_id
from worlds.adventure.Rom import AdventureForeignItemInfo, AdventureAutoCollectLocation, BatNoTouchLocation
from worlds.adventure.Items import base_adventure_item_id, standard_item_max, item_table
from worlds.adventure.Offsets import static_item_element_size, connector_port_offset

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = \
    "Connection timing out. Please restart your emulator, then restart connector_adventure.lua"
CONNECTION_REFUSED_STATUS = \
    "Connection Refused. Please start your emulator and make sure connector_adventure.lua is running"
CONNECTION_RESET_STATUS = \
    "Connection was reset. Please restart your emulator, then restart connector_adventure.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

SCRIPT_VERSION = 1


class AdventureCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_2600(self):
        """Check 2600 Connection State"""
        if isinstance(self.ctx, AdventureContext):
            logger.info(f"2600 Status: {self.ctx.atari_status}")

    def _cmd_aconnect(self):
        """Discard current atari 2600 connection state"""
        if isinstance(self.ctx, AdventureContext):
            self.ctx.atari_sync_task.cancel()


class AdventureContext(CommonContext):
    command_processor = AdventureCommandProcessor
    game = 'Adventure'
    lua_connector_port: int = 17242

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.freeincarnates_used: int = -1
        self.freeincarnate_pending: int = 0
        self.foreign_items: [AdventureForeignItemInfo] = []
        self.autocollect_items: [AdventureAutoCollectLocation] = []
        self.atari_streams: (StreamReader, StreamWriter) = None
        self.atari_sync_task = None
        self.messages = {}
        self.locations_array = None
        self.atari_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.display_msgs = True
        self.deathlink_pending = False
        self.set_deathlink = False
        self.client_compatibility_mode = 0
        self.items_handling = 0b111
        self.checked_locations_sent: bool = False
        self.port_offset = 0
        self.bat_no_touch_locations: [BatNoTouchLocation] = []
        self.local_item_locations = {}
        self.dragon_speed_info = {}

        options = Utils.get_settings()
        self.display_msgs = options["adventure_options"]["display_msgs"]

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(AdventureContext, self).server_auth(password_requested)
        if not self.auth:
            self.auth = self.player_name
        if not self.auth:
            self.awaiting_rom = True
            logger.info('Awaiting connection to adventure_connector to get Player information')
            return

        await self.send_connect()

    def _set_message(self, msg: str, msg_id: int):
        if self.display_msgs:
            self.messages[(time.time(), msg_id)] = msg

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.locations_array = None
            if Utils.get_settings()["adventure_options"].get("death_link", False):
                self.set_deathlink = True
            async_start(self.get_freeincarnates_used())
        elif cmd == "RoomInfo":
            self.seed_name = args['seed_name']
        elif cmd == 'Print':
            msg = args['text']
            if ': !' not in msg:
                self._set_message(msg, SYSTEM_MESSAGE_ID)
        elif cmd == "ReceivedItems":
            msg = f"Received {', '.join([self.item_names.lookup_in_game(item.item) for item in args['items']])}"
            self._set_message(msg, SYSTEM_MESSAGE_ID)
        elif cmd == "Retrieved":
            if f"adventure_{self.auth}_freeincarnates_used" in args["keys"]:
                self.freeincarnates_used = args["keys"][f"adventure_{self.auth}_freeincarnates_used"]
                if self.freeincarnates_used is None:
                    self.freeincarnates_used = 0
                self.freeincarnates_used += self.freeincarnate_pending
                self.send_pending_freeincarnates()
        elif cmd == "SetReply":
            if args["key"] == f"adventure_{self.auth}_freeincarnates_used":
                self.freeincarnates_used = args["value"]
                if self.freeincarnates_used is None:
                    self.freeincarnates_used = 0
                self.freeincarnates_used += self.freeincarnate_pending
                self.send_pending_freeincarnates()

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    def run_gui(self):
        from kvui import GameManager

        class AdventureManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Adventure Client"

        self.ui = AdventureManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def get_freeincarnates_used(self):
        if self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "SetNotify", "keys": [f"adventure_{self.auth}_freeincarnates_used"]}])
            await self.send_msgs([{"cmd": "Get", "keys": [f"adventure_{self.auth}_freeincarnates_used"]}])

    def send_pending_freeincarnates(self):
        if self.freeincarnate_pending > 0:
            async_start(self.send_pending_freeincarnates_impl(self.freeincarnate_pending))
            self.freeincarnate_pending = 0

    async def send_pending_freeincarnates_impl(self, send_val: int) -> None:
        await self.send_msgs([{"cmd": "Set", "key": f"adventure_{self.auth}_freeincarnates_used",
                               "default": 0, "want_reply": False,
                               "operations": [{"operation": "add", "value": send_val}]}])

    async def used_freeincarnate(self) -> None:
        if self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "Set", "key": f"adventure_{self.auth}_freeincarnates_used",
                                   "default": 0, "want_reply": True,
                                   "operations": [{"operation": "add", "value": 1}]}])
        else:
            self.freeincarnate_pending = self.freeincarnate_pending + 1


def convert_item_id(ap_item_id: int):
    static_item_index = ap_item_id - base_adventure_item_id
    return static_item_index * static_item_element_size


def get_payload(ctx: AdventureContext):
    current_time = time.time()
    items = []
    dragon_speed_update = {}
    diff_a_locked = ctx.diff_a_mode > 0
    diff_b_locked = ctx.diff_b_mode > 0
    freeincarnate_count = 0
    for item in ctx.items_received:
        item_id_str = str(item.item)
        if base_adventure_item_id < item.item <= standard_item_max:
            items.append(convert_item_id(item.item))
        elif item_id_str in ctx.dragon_speed_info:
            if item.item in dragon_speed_update:
                last_index = len(ctx.dragon_speed_info[item_id_str]) - 1
                dragon_speed_update[item.item] = ctx.dragon_speed_info[item_id_str][last_index]
            else:
                dragon_speed_update[item.item] = ctx.dragon_speed_info[item_id_str][0]
        elif item.item == item_table["Left Difficulty Switch"].id:
            diff_a_locked = False
        elif item.item == item_table["Right Difficulty Switch"].id:
            diff_b_locked = False
        elif item.item == item_table["Freeincarnate"].id:
            freeincarnate_count = freeincarnate_count + 1
    freeincarnates_available = 0

    if ctx.freeincarnates_used >= 0:
        freeincarnates_available = freeincarnate_count - (ctx.freeincarnates_used + ctx.freeincarnate_pending)
    ret = json.dumps(
        {
            "items": items,
            "messages": {f'{key[0]}:{key[1]}': value for key, value in ctx.messages.items()
                         if key[0] > current_time - 10},
            "deathlink": ctx.deathlink_pending,
            "dragon_speeds": dragon_speed_update,
            "difficulty_a_locked": diff_a_locked,
            "difficulty_b_locked": diff_b_locked,
            "freeincarnates_available": freeincarnates_available,
            "bat_logic": ctx.bat_logic
        }
    )
    ctx.deathlink_pending = False
    return ret


async def parse_locations(data: List, ctx: AdventureContext):
    locations = data

    # for loc_name, loc_data in location_table.items():

    # if flags["EventFlag"][280] & 1 and not ctx.finished_game:
    #    await ctx.send_msgs([
    #                {"cmd": "StatusUpdate",
    #                 "status": 30}
    #            ])
    #    ctx.finished_game = True
    if locations == ctx.locations_array:
        return
    ctx.locations_array = locations
    if locations is not None:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations}])


def send_ap_foreign_items(adventure_context):
    foreign_item_json_list = []
    autocollect_item_json_list = []
    bat_no_touch_locations_json_list = []
    for fi in adventure_context.foreign_items:
        foreign_item_json_list.append(fi.get_dict())
    for fi in adventure_context.autocollect_items:
        autocollect_item_json_list.append(fi.get_dict())
    for ntl in adventure_context.bat_no_touch_locations:
        bat_no_touch_locations_json_list.append(ntl.get_dict())
    payload = json.dumps(
        {
            "foreign_items": foreign_item_json_list,
            "autocollect_items": autocollect_item_json_list,
            "local_item_locations": adventure_context.local_item_locations,
            "bat_no_touch_locations": bat_no_touch_locations_json_list
        }
    )
    print("sending foreign items")
    msg = payload.encode()
    (reader, writer) = adventure_context.atari_streams
    writer.write(msg)
    writer.write(b'\n')


def send_checked_locations_if_needed(adventure_context):
    if not adventure_context.checked_locations_sent and adventure_context.checked_locations is not None:
        if len(adventure_context.checked_locations) == 0:
            return
        checked_short_ids = []
        for location in adventure_context.checked_locations:
            checked_short_ids.append(location - base_location_id)
        print("Sending checked locations")
        payload = json.dumps(
            {
                "checked_locations": checked_short_ids,
            }
        )
        msg = payload.encode()
        (reader, writer) = adventure_context.atari_streams
        writer.write(msg)
        writer.write(b'\n')
        adventure_context.checked_locations_sent = True


async def atari_sync_task(ctx: AdventureContext):
    logger.info("Starting Atari 2600 connector. Use /2600 for status information")
    while not ctx.exit_event.is_set():
        try:
            error_status = None
            if ctx.atari_streams:
                (reader, writer) = ctx.atari_streams
                msg = get_payload(ctx).encode()
                writer.write(msg)
                writer.write(b'\n')
                try:
                    await asyncio.wait_for(writer.drain(), timeout=1.5)
                    try:
                        # Data will return a dict with 1+ fields
                        # 1. A keepalive response of the Players Name (always)
                        # 2. romhash field with sha256 hash of the ROM memory region
                        # 3. locations, messages, and deathLink
                        # 4. freeincarnate, to indicate a freeincarnate was used
                        data = await asyncio.wait_for(reader.readline(), timeout=5)
                        data_decoded = json.loads(data.decode())
                        if 'scriptVersion' not in data_decoded or data_decoded['scriptVersion'] != SCRIPT_VERSION:
                            msg = "You are connecting with an incompatible Lua script version. Ensure your connector " \
                                  "Lua and AdventureClient are from the same Archipelago installation."
                            logger.info(msg, extra={'compact_gui': True})
                            ctx.gui_error('Error', msg)
                            error_status = CONNECTION_RESET_STATUS
                        if ctx.seed_name and bytes(ctx.seed_name, encoding='ASCII') != ctx.seed_name_from_data:
                            msg = "The server is running a different multiworld than your client is. " \
                                  "(invalid seed_name)"
                            logger.info(msg, extra={'compact_gui': True})
                            ctx.gui_error('Error', msg)
                            error_status = CONNECTION_RESET_STATUS
                        if 'romhash' in data_decoded:
                            if ctx.rom_hash.upper() != data_decoded['romhash'].upper():
                                msg = "The rom hash does not match the client rom hash data"
                                print("got " + data_decoded['romhash'])
                                print("expected " + str(ctx.rom_hash))
                                logger.info(msg, extra={'compact_gui': True})
                                ctx.gui_error('Error', msg)
                                error_status = CONNECTION_RESET_STATUS
                                if ctx.auth is None:
                                    ctx.auth = ctx.player_name
                            if ctx.awaiting_rom:
                                await ctx.server_auth(False)
                        if 'locations' in data_decoded and ctx.game and ctx.atari_status == CONNECTION_CONNECTED_STATUS \
                                and not error_status and ctx.auth:
                            # Not just a keep alive ping, parse
                            async_start(parse_locations(data_decoded['locations'], ctx))
                        if 'deathLink' in data_decoded and data_decoded['deathLink'] > 0 and 'DeathLink' in ctx.tags:
                            dragon_name = "a dragon"
                            if data_decoded['deathLink'] == 1:
                                dragon_name = "Rhindle"
                            elif data_decoded['deathLink'] == 2:
                                dragon_name = "Yorgle"
                            elif data_decoded['deathLink'] == 3:
                                dragon_name = "Grundle"
                            print (ctx.auth + " has been eaten by " + dragon_name )
                            await ctx.send_death(ctx.auth + " has been eaten by " + dragon_name)
                            # TODO - also if player reincarnates with a dragon onscreen ' dies to avoid being eaten by '
                        if 'victory' in data_decoded and not ctx.finished_game:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                        if 'freeincarnate' in data_decoded:
                            await ctx.used_freeincarnate()
                        if ctx.set_deathlink:
                            await ctx.update_death_link(True)
                        send_checked_locations_if_needed(ctx)
                    except asyncio.TimeoutError:
                        logger.debug("Read Timed Out, Reconnecting")
                        error_status = CONNECTION_TIMING_OUT_STATUS
                        writer.close()
                        ctx.atari_streams = None
                    except ConnectionResetError as e:
                        logger.debug("Read failed due to Connection Lost, Reconnecting")
                        error_status = CONNECTION_RESET_STATUS
                        writer.close()
                        ctx.atari_streams = None
                except TimeoutError:
                    logger.debug("Connection Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.atari_streams = None
                except ConnectionResetError:
                    logger.debug("Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.atari_streams = None
                except CancelledError:
                    logger.debug("Connection Cancelled, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.atari_streams = None
                    pass
                except Exception as e:
                    print("unknown exception " + e)
                    raise
                if ctx.atari_status == CONNECTION_TENTATIVE_STATUS:
                    if not error_status:
                        logger.info("Successfully Connected to 2600")
                        ctx.atari_status = CONNECTION_CONNECTED_STATUS
                        ctx.checked_locations_sent = False
                        send_ap_foreign_items(ctx)
                        send_checked_locations_if_needed(ctx)
                    else:
                        ctx.atari_status = f"Was tentatively connected but error occurred: {error_status}"
                elif error_status:
                    ctx.atari_status = error_status
                    logger.info("Lost connection to 2600 and attempting to reconnect. Use /2600 for status updates")
            else:
                try:
                    port = ctx.lua_connector_port + ctx.port_offset
                    logger.debug(f"Attempting to connect to 2600 on port {port}")
                    print(f"Attempting to connect to 2600 on port {port}")
                    ctx.atari_streams = await asyncio.wait_for(
                        asyncio.open_connection("localhost",
                                                port),
                        timeout=10)
                    ctx.atari_status = CONNECTION_TENTATIVE_STATUS
                except TimeoutError:
                    logger.debug("Connection Timed Out, Trying Again")
                    ctx.atari_status = CONNECTION_TIMING_OUT_STATUS
                    continue
                except ConnectionRefusedError:
                    logger.debug("Connection Refused, Trying Again")
                    ctx.atari_status = CONNECTION_REFUSED_STATUS
                    continue
                except CancelledError:
                    pass
        except CancelledError:
            pass
    print("exiting atari sync task")


async def run_game(romfile):
    auto_start = Utils.get_settings()["adventure_options"].get("rom_start", True)
    rom_args = Utils.get_settings()["adventure_options"].get("rom_args")
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        open_args = [auto_start, romfile]
        if rom_args is not None:
            open_args.insert(1, rom_args)
        subprocess.Popen(open_args,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(patch_file, ctx):
    base_name = os.path.splitext(patch_file)[0]
    comp_path = base_name + '.a26'
    try:
        base_rom = AdventureDeltaPatch.get_source_data()
    except Exception as msg:
        logger.info(msg, extra={'compact_gui': True})
        ctx.gui_error('Error', msg)

    with open(Utils.local_path("data", "adventure_basepatch.bsdiff4"), "rb") as file:
        basepatch = bytes(file.read())

    base_patched_rom_data = bsdiff4.patch(base_rom, basepatch)

    with zipfile.ZipFile(patch_file, 'r') as patch_archive:
        if not AdventureDeltaPatch.check_version(patch_archive):
            logger.error("apadvn version doesn't match this client.  Make sure your generator and client are the same")
            raise Exception("apadvn version doesn't match this client.")

        ctx.foreign_items = AdventureDeltaPatch.read_foreign_items(patch_archive)
        ctx.autocollect_items = AdventureDeltaPatch.read_autocollect_items(patch_archive)
        ctx.local_item_locations = AdventureDeltaPatch.read_local_item_locations(patch_archive)
        ctx.dragon_speed_info = AdventureDeltaPatch.read_dragon_speed_info(patch_archive)
        ctx.seed_name_from_data, ctx.player_name = AdventureDeltaPatch.read_rom_info(patch_archive)
        ctx.diff_a_mode, ctx.diff_b_mode = AdventureDeltaPatch.read_difficulty_switch_info(patch_archive)
        ctx.bat_logic = AdventureDeltaPatch.read_bat_logic(patch_archive)
        ctx.bat_no_touch_locations = AdventureDeltaPatch.read_bat_no_touch(patch_archive)
        ctx.rom_deltas = AdventureDeltaPatch.read_rom_deltas(patch_archive)
        ctx.auth = ctx.player_name

    patched_rom_data = AdventureDeltaPatch.apply_rom_deltas(base_patched_rom_data, ctx.rom_deltas)
    rom_hash = hashlib.sha256()
    rom_hash.update(patched_rom_data)
    ctx.rom_hash = rom_hash.hexdigest()
    ctx.port_offset = patched_rom_data[connector_port_offset]

    with open(comp_path, "wb") as patched_rom_file:
        patched_rom_file.write(patched_rom_data)

    async_start(run_game(comp_path))


if __name__ == '__main__':

    Utils.init_logging("AdventureClient")

    async def main():
        parser = get_base_parser()
        parser.add_argument('patch_file', default="", type=str, nargs="?",
                            help='Path to an ADVNTURE.BIN rom file')
        parser.add_argument('port', default=17242, type=int, nargs="?",
                            help='port for adventure_connector connection')
        args = parser.parse_args()

        ctx = AdventureContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.atari_sync_task = asyncio.create_task(atari_sync_task(ctx), name="Adventure Sync")

        if args.patch_file:
            ext = args.patch_file.split(".")[len(args.patch_file.split(".")) - 1].lower()
            if ext == "apadvn":
                logger.info("apadvn file supplied, beginning patching process...")
                async_start(patch_and_run_game(args.patch_file, ctx))
            else:
                logger.warning(f"Unknown patch file extension {ext}")
        if args.port is int:
            ctx.lua_connector_port = args.port

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.atari_sync_task:
            await ctx.atari_sync_task
            print("finished atari_sync_task (main)")


    import colorama

    colorama.just_fix_windows_console()

    asyncio.run(main())
    colorama.deinit()
