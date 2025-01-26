import asyncio
import os
import time
import traceback
import Utils
from typing import Any, Optional

import dolphin_memory_engine as dme

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem
from settings import get_settings, Settings
from .LMGenerator import LuigisMansionRandomizer

from .Items import LOOKUP_ID_TO_NAME, ALL_ITEMS_TABLE
from .Locations import ALL_LOCATION_TABLE, LMLocation, LMLocationData


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

# This is an array of length 0x10 where each element is a byte and contains item IDs for items to give the player.
# 0xFF represents no item. The array is read and cleared every frame.
# GIVE_ITEM_ARRAY_ADDR = 0x803FE868

luigi_recv_text = "Luigi was able to find: "

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
    iso_path = get_base_rom_path()  #TODO fix??
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
        self.items_received_2: list[tuple[NetworkItem, int]] = []
        self.dolphin_sync_task = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.last_rcvd_index = -1
        self.has_send_death = False

        self.len_give_item_array = 0x10

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected": # On Connect
            self.items_received_2 = []
            self.last_rcvd_index = -1
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
        if cmd == "ReceivedItems": # On Receive Item from Server
            if args["index"] >= self.last_rcvd_index:
                self.last_rcvd_index = args["index"]
                for item in args["items"]:
                    self.items_received_2.append((item, self.last_rcvd_index))
                    self.last_rcvd_index += 1
            self.items_received_2.sort(key=lambda v: v[1])

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


# TODO CORRECT FOR LM
def _give_item(ctx: LMContext, item_name: str) -> bool:
    if not check_ingame():  # or dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) == 0xFF:
        return False
    return False

    #item_id = ALL_ITEMS_TABLE[item_name].item_id

    # Loop through the give item array, placing the item in an empty slot
    #for idx in range(ctx.len_give_item_array):
    #    slot = dme.read_byte(GIVE_ITEM_ARRAY_ADDR + idx)
    #    if slot == 0xFF:
    #        dme.write_byte(GIVE_ITEM_ARRAY_ADDR + idx, item_id)
    #        return True

    # Unable to place the item in the array, so return `False`
    #return False


# TODO CORRECT FOR LM
async def give_items(ctx: LMContext):
    return
    #if check_ingame() and dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) != 0xFF:
        # Read the expected index of the player, which is the index of the latest item they've received
        # expected_idx = read_short(EXPECTED_INDEX_ADDR)
        #
        # # Loop through items to give
        # for item, idx in ctx.items_received_2:
        #     # If the index of the item is greater than the expected index of the player, give the player the item
        #     if expected_idx <= idx:
        #         # Attempt to give the item and increment the expected index
        #         while not _give_item(ctx, LOOKUP_ID_TO_NAME[item.item]):
        #             await asyncio.sleep(0.01)
        #
        #         # Increment the expected index
        #         write_short(EXPECTED_INDEX_ADDR, idx + 1)


# TODO CORRECT FOR LM
async def check_locations(ctx: LMContext):
    list_types_to_skip_currently = ["BSpeedy", "Portrait", "Event", "Toad", "Boo"]

    current_map_id = get_map_id()
    for location, data in ALL_LOCATION_TABLE.items():
        if data.type in list_types_to_skip_currently:
            continue

        if not LMLocation.get_apid(data.code) in ctx.missing_locations:
            continue

        # If in main mansion map
        if current_map_id == 2:
            #TODO Debug remove before release
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
                    if (current_room_state_int & (1<<2)) > 0:
                        ctx.locations_checked.add(LMLocation.get_apid(data.code))


    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])
    return


async def check_alive():
    lm_curr_health = read_short(dme.follow_pointers(CURR_HEALTH_ADDR, [CURR_HEALTH_OFFSET]))
    return lm_curr_health > 0

async def check_death(ctx: LMContext):
    if check_ingame():
        if not check_alive() and not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " scared themselves to death.")
        else:
            ctx.has_send_death = False

def check_ingame():
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
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame():
                    # Reset give item array while not in game
                    # dolphin_memory_engine.write_bytes(GIVE_ITEM_ARRAY_ADDR, bytes([0xFF] * ctx.len_give_item_array))
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

    if output_data :
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
