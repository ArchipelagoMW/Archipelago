import asyncio
import os
import re
import time
import traceback

import Utils
from typing import Any, Optional

import dolphin_memory_engine as dme

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem, color
from settings import get_settings, Settings
from worlds.luigismansion import BOO_LOCATION_TABLE

from .LMGenerator import LuigisMansionRandomizer
from .Items import ALL_ITEMS_TABLE, LMItem
from .Locations import ALL_LOCATION_TABLE, LMLocation

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for LM. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure LM is running."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

# This is the address that holds the player's slot name.
# This way, the player does not have to manually authenticate their slot name.
SLOT_NAME_ADDR = 0x80314660
SLOT_NAME_STR_LENGTH = 0x10

# This Play State address lets us know if the game is playable and ready. This should have a value of 2
# Map ID is used to confirm Luigi is loading into the Mansion or one of the boss maps.
CURR_PLAY_STATE_ADDR = 0x803A3AE4
CURR_MAP_ID_ADDR = 0x804D7834

# This address is used to check/set the player's health for DeathLink. (2 bytes / Half word)
CURR_HEALTH_ADDR = 0x803D8B40
CURR_HEALTH_OFFSET = 0xB8

# This address is used to track which room Luigi is in within the main mansion map (Map2)
ROOM_ID_ADDR = 0x803D8B7C
ROOM_ID_OFFSET = 0x35C

# This Furniture address table contains the start of the addresses used for currently loaded in Furniture.
# Since multiple rooms can be loaded into the background, several hundred addresses must be checked.
# Each furniture flag and ID are 4 Bytes / Word.
# Flag Offset will contain whether the current piece of furniture has been interacted with or not.
# This flag follows the 2 rooms away rule and resets between reloading the game / save file.
# A Flag with value 0x00 indicates no interaction, 0x01 indicates it has been interacted with and has either
# dropped something or had dust, and 0x02 indicates an important item, such as a Mario Item or Elemental Medal.
FURNITURE_MAIN_TABLE_ID = 0x803CD768
FURNITURE_ADDR_COUNT = 760
FURN_FLAG_OFFSET = 0x8C
FURN_ID_OFFSET = 0xBC

# This is a short of length 0x02 which contains the last received index of the item that was given to Luigi
# This index is updated every time a new item is received.
LAST_RECV_ITEM_ADDR = 0x803CDEBA

# This address will monitor when you capture the final boss, King Boo
KING_BOO_ADDR = 0x803D5DBF

# This address will start the point to Luigi's inventory to get his wallet to calculate rank.
WALLET_START_ADDR = 0x803D8B7C

WALLET_OFFSETS: dict[int, int] = {
    0x324: 5000,
    0x328: 20000,
    0x32C: 100000,
    0x330: 500000,
    0x334: 800000,
    0x338: 1000000,
    0x33C: 2000000,
    0x344: 20000000,
    0x348: 50000,
    0x34C: 100000,
    0x350: 1000000
}

# Rank Requirements for each rank. H, G, F, E, D, C, B, A
RANK_REQ_AMTS = [0, 5000000, 20000000, 40000000,50000000, 60000000, 70000000, 100000000]

# List of received items to ignore because they are handled elsewhere
# TODO Remove hearts from here when fixed.
RECV_ITEMS_IGNORE = [8063, 8064, 8128, 8129]
RECV_OWN_GAME_LOCATIONS = [BOO_LOCATION_TABLE,]


def read_short(console_address: int):
    return int.from_bytes(dme.read_bytes(console_address, 2))


def write_short(console_address: int, value: int):
    dme.write_bytes(console_address, value.to_bytes(2))


def read_string(console_address: int, strlen: int):
    return dme.read_bytes(console_address, strlen).decode().strip("\0")


def get_base_rom_path(file_name: str = "") -> str:
    options: Settings = get_settings()
    if not file_name:
        file_name = options["luigismansion_options"]["iso_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def save_patched_iso(output_data):
    iso_path = get_base_rom_path()
    directory_to_iso, file = os.path.split(output_data)
    file_name = os.path.splitext(file)[0]

    if iso_path:
        LuigisMansionRandomizer(iso_path, os.path.join(directory_to_iso, file_name + ".iso"), output_data)


class LMCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, LMContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class LMContext(CommonContext):
    command_processor = LMCommandProcessor
    game = "Luigi's Mansion"
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        self.dolphin_sync_task = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.has_send_death = False

        # Used for handling received items to the client.
        self.goal_type = None
        self.game_clear = False
        self.rank_req = -1

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":  # On Connect
            self.goal_type = int(args["slot_data"]["goal"])
            self.rank_req = int(args["slot_data"]["rank requirement"])
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))

        if cmd == "ReceivedItems": # On Receive Item from Server
            self.items_received = args["items"]
            give_items(self)



    def on_deathlink(self, data: dict[str, Any]):
        super().on_deathlink(data)
        _give_death(self)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(LMContext, self).server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information")
            return
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class LMManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago Luigi's Mansion Client"

        self.ui = LMManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def _give_death(ctx: LMContext):
    if ctx.slot and dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS and check_ingame():
        ctx.has_send_death = True
        write_short(dme.follow_pointers(CURR_HEALTH_ADDR, [CURR_HEALTH_OFFSET]), 0)
    return


def get_map_id():
    return dme.read_word(CURR_MAP_ID_ADDR)


def check_if_addr_is_pointer(addr: int):
    return 2147483648 <= dme.read_word(addr) <= 2172649471


# TODO Validate this works
async def give_items(ctx: LMContext):
    # Only try to give items if we are in game and alive.
    if not await check_ingame() and await check_alive():
        return

    last_recv_idx = read_short(LAST_RECV_ITEM_ADDR)
    if len(ctx.items_received) <= last_recv_idx:
        return

    # Filter for only items where we have not received yet. If same slot, only receive the locations from the
    # pre-approved own locations (as everything is currently a NetworkItem), otherwise accept other slots.
    list_recv_items = [netItem for netItem in ctx.items_received if ctx.items_received.index(netItem)> last_recv_idx
        and ((netItem.player == ctx.slot and LMLocation.get_apid(netItem.location) in RECV_OWN_GAME_LOCATIONS) or
             not netItem.player == ctx.slot) and netItem.item in RECV_ITEMS_IGNORE]

    if len(list_recv_items) == 0:
        write_short(LAST_RECV_ITEM_ADDR, (len(ctx.items_received) - 1))
        return

    for item in list_recv_items:
        # If boo radar or super vacuum, ignore these as they are handled in patching.
        if item.item is None or item.item in RECV_ITEMS_IGNORE:
            write_short(LAST_RECV_ITEM_ADDR, ctx.items_received.index(item))
            continue

        # Get the current LM Item so we can get the various named tuple fields easier.
        lm_item = ALL_ITEMS_TABLE[next(key for key in ALL_ITEMS_TABLE.keys() if
                          LMItem.get_apid(ALL_ITEMS_TABLE[key].code) == item.item)]
        if not lm_item.ram_addr is None and (not lm_item.itembit is None or not lm_item.pointer_offset is None):
            lm_item_name = ctx.item_names.lookup_in_game(item.item)
            logger.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(lm_item_name, 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player),
                (ctx.items_received.index(item)+1), len(ctx.items_received)))
            if not lm_item.pointer_offset is None:
                # Assume we need to update an existing value of size X with Y value at the pointer's address
                curr_val = int.from_bytes(dme.read_bytes(dme.follow_pointers(lm_item.ram_addr,
                                                    [lm_item.pointer_offset]), lm_item.ram_byte_size))
                # TODO fix for hearts, will break receival otherwise
                curr_val += int(re.search(r"^\d+", lm_item_name).group())
                dme.write_bytes(dme.follow_pointers(lm_item.ram_addr,
                    [lm_item.pointer_offset]), curr_val.to_bytes(lm_item.ram_byte_size, 'big'))
            else:
                # Assume it is a single address with a bit to update, rather than adding to an existing value
                item_val = dme.read_byte(lm_item.ram_addr)
                dme.write_byte(lm_item.ram_addr, (item_val | (1 << lm_item.itembit)))

            # Update the last received index to ensure we dont receive the same item over and over.
            write_short(LAST_RECV_ITEM_ADDR, ctx.items_received.index(item))
        else:
            # TODO Debug remove before release
            logger.warn("Missing information for AP ID: " + str(item.item))
    return


async def check_locations(ctx: LMContext):
    list_types_to_skip_currently = ["BSpeedy", "Portrait", "Event", "Toad"]

    current_map_id = get_map_id()
    for location, data in ALL_LOCATION_TABLE.items():
        if data.type in list_types_to_skip_currently:
            continue

        if data.code is None or not LMLocation.get_apid(data.code) in ctx.missing_locations:
            continue

        # If in main mansion map
        if current_map_id == 2:
            # TODO Debug remove before release
            if data.in_game_room_id is None:
                logger.warn("Missing in game room id: " + location)

            # Only check locations that are currently in the same room as us.
            current_room_id = dme.read_word(dme.follow_pointers(ROOM_ID_ADDR, [ROOM_ID_OFFSET]))
            if not data.in_game_room_id == current_room_id:
                continue

            match data.type:
                case "Furniture":
                    # Check all possible furniture addresses. #TODO Find a way to not check all 600+
                    for current_offset in range(0, FURNITURE_ADDR_COUNT, 4):
                        # Only check if the current address is a pointer
                        current_addr = FURNITURE_MAIN_TABLE_ID + current_offset
                        if not check_if_addr_is_pointer(current_addr):
                            continue

                        furn_id = dme.read_word(dme.follow_pointers(current_addr, [FURN_ID_OFFSET]))
                        if not furn_id == data.jmpentry:
                            continue

                        furn_flag = dme.read_word(dme.follow_pointers(current_addr, [FURN_FLAG_OFFSET]))
                        if furn_flag > 0:
                            ctx.locations_checked.add(LMLocation.get_apid(data.code))
                case "Plant":
                    # Check all possible furniture addresses. #TODO Find a way to not check all 600+
                    for current_offset in range(0, FURNITURE_ADDR_COUNT, 4):
                        # Only check if the current address is a pointer
                        current_addr = FURNITURE_MAIN_TABLE_ID + current_offset
                        if not check_if_addr_is_pointer(current_addr):
                            continue

                        furn_id = dme.read_word(dme.follow_pointers(current_addr, [FURN_ID_OFFSET]))
                        if not furn_id == data.jmpentry:
                            continue

                        furn_flag = dme.read_word(dme.follow_pointers(current_addr, [FURN_FLAG_OFFSET]))
                        if furn_flag > 0:
                            ctx.locations_checked.add(LMLocation.get_apid(data.code))
                case "Chest":
                    # Bit 2 of the current room address indicates if a chest in that room has been opened.
                    current_room_state_int = read_short(data.room_ram_addr)
                    if (current_room_state_int & (1 << 2)) > 0:
                        ctx.locations_checked.add(LMLocation.get_apid(data.code))
                case "Boo":
                    current_boo_state_int = dme.read_byte(data.room_ram_addr)
                    if (current_boo_state_int & (1 << data.locationbit)) > 0:
                        ctx.locations_checked.add(LMLocation.get_apid(data.code))
                        dme.write_byte(current_boo_state_int, 0)

    await ctx.check_locations(ctx.locations_checked)

    if current_map_id == 9:
        beat_king_boo = dme.read_byte(KING_BOO_ADDR)
        if (beat_king_boo & (1 << 5)) > 0 and not ctx.game_clear:
            if ctx.goal_type == 0:
                ctx.game_clear = True
            elif ctx.goal_type == 1:
                int_rank_sum = 0
                req_rank_amt = RANK_REQ_AMTS[ctx.rank_req]
                for key in WALLET_OFFSETS.keys():
                    currency_amt = dme.read_word(dme.follow_pointers(WALLET_START_ADDR, [key]))
                    int_rank_sum += currency_amt * WALLET_OFFSETS[key]

                if int_rank_sum >= req_rank_amt:
                    ctx.game_clear = True
                else:
                    logger.info("Unfortunately, you do NOT have enough money to satisfy the rank requirements.\n" +
                                f"You are missing: '{(req_rank_amt - int_rank_sum):,}'")

    if not ctx.finished_game and ctx.game_clear:
        ctx.finished_game = True
        await ctx.send_msgs([{
            "cmd": "StatusUpdate",
            "status": ClientStatus.CLIENT_GOAL,
        }])
    return


async def check_alive():
    lm_curr_health = read_short(dme.follow_pointers(CURR_HEALTH_ADDR, [CURR_HEALTH_OFFSET]))
    return lm_curr_health > 0


async def check_death(ctx: LMContext):
    if await check_ingame():
        if not await check_alive() and not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
            ctx.has_send_death = True
            await ctx.send_death(ctx.player_names[ctx.slot] + " scared themselves to death.")
        else:
            ctx.has_send_death = False


async def check_ingame():
    current_map_id = get_map_id()
    if current_map_id == 2:
        # If this is NOT a pointer, then either we are on another map (aka boss fight) or game is not fully loaded.
        bool_loaded_in_map = check_if_addr_is_pointer(ROOM_ID_ADDR)
    else:
        bool_loaded_in_map = 0 < current_map_id < 14

    int_play_state = dme.read_word(CURR_PLAY_STATE_ADDR)
    return int_play_state == 2 and bool_loaded_in_map


async def dolphin_sync_task(ctx: LMContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            # TODO Handle if Dolphin was closed pre-maturely. Something around here causes the error.
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not await check_ingame():
                    await asyncio.sleep(0.1)
                    continue
                if ctx.slot:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR, SLOT_NAME_STR_LENGTH)
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if dme.is_hooked():
                    if read_string(0x80000000, 6) != "GLME01":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dme.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dme.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def main(output_data: Optional[str] = None, connect=None, password=None):
    Utils.init_logging("Luigi's Mansion Client")

    if output_data:
        save_patched_iso(output_data)

    async def _main(connect, password):
        ctx = LMContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
