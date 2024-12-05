import asyncio
import os
import time
import traceback
from typing import Any, Optional

import dolphin_memory_engine
from dolphin_memory_engine import read_bytes

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem
from settings import get_settings, Settings
from .LMGenerator import LuigisMansionRandomizer

from .Items import LOOKUP_ID_TO_NAME, ALL_ITEMS_TABLE
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

# This address is used to check/set the player's health for DeathLink. TODO CORRECT FOR LM
CURR_HEALTH_ADDR = 0x803C4C0A
BOOLOSSUS_HEALTH_ADDR = 0x8113442D
BOWSER_HEALTH_ADDR = 0x811BBEC5
BASE_HEALTH_ADDR = 0x81349A0D

# This address (and its 7 other offsets) are used to check if the player captured any boos
BOOS_BITFLD_ADDR = 0x803D5E04

# This address (and its 9 other offsets) are used to check if the player has received keys to any doors in the mansion.
KEYS_BITFLD_ADDR = 0x803D5E14

# Address used to check if the elemental medals are received.
MEDALS_RECV_ADDR = 0x803D5DB2 # Bits Fire 5, Ice 6, Water 7

# Addresses used to check if the mario items are received
MARIO_ITEMS_RECV_ONE_ADDR = 0x803D5DBB # Bits Hat 4, Star 5, Glove 6, Shoe 7
MARIO_ITEMS_RECV_TWO_ADDR = 0x803D5DBC # Bit Letter 0

# # This address contains the current stage ID.
CURR_MANSION_MAP_ID_ADDR = 0x804D80A4

# This address lets us know if the game is playable and ready. This should have a value of 2
CURR_PLAY_STATE_ADDR = 0x803A3AE4

# This address is used to check the stage name to verify the player is in-game before sending items.
# CURR_STAGE_NAME_ADDR = 0x803C9D3C

# This is an array of length 0x10 where each element is a byte and contains item IDs for items to give the player.
# 0xFF represents no item. The array is read and cleared every frame.
GIVE_ITEM_ARRAY_ADDR = 0x803FE868

# This is the address that holds the player's slot name.
# This way, the player does not have to manually authenticate their slot name.
# SLOT_NAME_ADDR = 0x803FE88C


key_name_collection = [["", "Butler's Room", "", "Heart", "Fortune Teller", "Mirror Room", "", "Laundry Room"],
                       ["", "Stairs 1F - BF", "Boneyard", "Kitchen", "", "", "Dinning Room", "Ball Room"],
                       ["Storage Room", "Billiards Room", "Projection Room", "", "1F Washroom", "Conservatory", "",
                            "1F Bathroom"],
                       ["Stairs 1F - 2F", "Rec Room", "", "Nursery", "Twin's Room", "Sitting Room", "Guest Room",
                            "Master Bedroom"],
                       ["Study", "Family Hallway (2F)", "Parlor", "", "", "", "Anteroom", ""],
                       ["Observatory", "2F Balcony", "Spade", "Wardrobe Room", "Astral Hall", "2F Washroom", "",
                            "Tea Room"],
                       ["2F Bathroom", "Nana's Room", "Ceramics Room", "Armory", "Telephone Room", "Clockwork Room",
                            "", "3F Hallway"],
                       ["Safari Room", "", "", "Diamond", "", "", "Big Balcony", "Artist's Studio"],
                       ["", "Cold Storage", "", "BF Hallway", "Cellar", "Pipe Room", "King Boo Hallway",
                            "Breaker Room"],
                       ["Secret Altar", "", "1F Shortcut", "2F Hallway", "", "", "", ""]]


boo_name_collection = [["Butler's Room Boo (PeekaBoo)", "Hidden Room Boo (GumBoo)", "Fortune Teller Boo (Booigi)",
                        "Mirror Room Boo (Kung Boo)", "Laundry Room Boo (Boogie)", "Kitchen Boo (Booligan)",
                        "Dining Room Boo (Boodacious)", "Ball Room Boo (Boo La La)"],
                       ["Billiards Boo (Boohoo)", "Projection Room Boo (ShamBoo)", "Storage Room Boo (Game Boo)",
                        "Conservatory Boo (Boomeo)", "Rec Room Boo (Booregard)", "Nursery Boo (TurBoo)",
                        "Twin's Room Boo (Booris)", "Sitting Room Boo (Boolivia)"],
                       ["Guest Room (Boonita)", "Master Bedroom Boo (Boolicious)", "Study Boo (TaBoo)",
                        "Parlor Boo (BamBoo)", "Wardrobe Boo (GameBoo Advance)", "Anteroom  Boo (Bootha)",
                        "Astral Boo (Boonswoggle)", "Nana's Room (LamBooger)"],
                       ["Tea Room (Mr. Boojangles)", "Armory Boo (Underboo)", "Telephone Room Boo (Boomerang)",
                        "Safari Room Boo (Little Boo Peep)", "Ceramics Studio (TamBoorine)",
                        "Clockwork Room Boo (Booscaster)", "Artist's Studio Boo (Bootique)",
                        "Cold Storage Boo (Boolderdash)"],
                       ["Cellar Boo (Booripedes)", "Pipe Room  Boo (Booffant)", "Breaker Room Boo (Boo B. Hatch)",
                        "Boolossus Boo 1", "Boolossus Boo 2", "Boolossus Boo 3", "Boolossus Boo 4", "Boolossus Boo 5"],
                       ["Boolossus Boo 6", "Boolossus Boo 7", "Boolossus Boo 8", "Boolossus Boo 9", "Boolossus Boo 10",
                        "Boolossus Boo 11", "Boolossus Boo 12", "Boolossus Boo 13"],
                       ["Boolossus Boo 14", "Boolossus Boo 15", "", "", "", "", "", ""]]


def get_base_rom_path(file_name: str = "") -> str:
    options: Settings = get_settings()
    if not file_name:
        file_name = options["luigismansion_options"]["iso_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def save_patched_iso(output_data):
    iso_path = get_base_rom_path()  # fix
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

        # Jake temp custom variables
        self.keys_tracked = [-1] * 10
        self.medals_tracked = [-1] * 3
        self.mario_items_tracked = [-1] * 5
        self.boos_captured = [-1] * 7

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.items_received_2 = []
            self.last_rcvd_index = -1
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
        if cmd == "ReceivedItems":
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

def read_short(console_address: int):
    return int.from_bytes(dolphin_memory_engine.read_bytes(console_address, 2))


def write_short(console_address: int, value: int):
    dolphin_memory_engine.write_bytes(console_address, value.to_bytes(2))


def read_string(console_address: int, strlen: int):
    return dolphin_memory_engine.read_bytes(console_address, strlen).decode().strip("\0")


# TODO CORRECT FOR LM
def _give_death(ctx: LMContext):
    if (
            ctx.slot
            and dolphin_memory_engine.is_hooked()
            and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
            and check_ingame()
    ):
        ctx.has_send_death = True
        write_short(CURR_HEALTH_ADDR, 0)


# TODO CORRECT FOR LM
def _give_item(ctx: LMContext, item_name: str) -> bool:
    if not check_ingame():  # or dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR) == 0xFF:
        return False

    item_id = ALL_ITEMS_TABLE[item_name].item_id

    # Loop through the give item array, placing the item in an empty slot
    for idx in range(ctx.len_give_item_array):
        slot = dolphin_memory_engine.read_byte(GIVE_ITEM_ARRAY_ADDR + idx)
        if slot == 0xFF:
            dolphin_memory_engine.write_byte(GIVE_ITEM_ARRAY_ADDR + idx, item_id)
            return True

    # Unable to place the item in the array, so return `False`
    return False


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
    # We check which locations are currently checked on the current stage
    # curr_stage_id = dolphin_memory_engine.read_byte(CURR_STAGE_ID_ADDR)

    # Read in various bitfields for the locations in the current stage
    # charts_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(CHARTS_BITFLD_ADDR, 8))
    # sea_alt_bitfield = dolphin_memory_engine.read_word(SEA_ALT_BITFLD_ADDR)
    # chests_bitfield = dolphin_memory_engine.read_word(CHESTS_BITFLD_ADDR)
    # switches_bitfield = int.from_bytes(dolphin_memory_engine.read_bytes(SWITCHES_BITFLD_ADDR, 10))
    # pickups_bitfield = dolphin_memory_engine.read_word(PICKUPS_BITFLD_ADDR)

    temp_medals_watch = int.from_bytes(dolphin_memory_engine.read_bytes(MEDALS_RECV_ADDR, 1), 'big')
    medals_recv_arr = [(temp_medals_watch & (1 << 5)), (temp_medals_watch & (1 << 6)), (temp_medals_watch & (1 << 7))]
    if medals_recv_arr != ctx.medals_tracked:
        ctx.medals_tracked = medals_recv_arr
        bool_fire = True if medals_recv_arr[0] else False
        bool_ice = True if medals_recv_arr[1] else False
        bool_water = True if medals_recv_arr[2] else False
        medals_str = f"Fire Medal: {bool_fire}; Ice Medal: {bool_ice}; Water Medal: {bool_water}"
        print("Currently Luigi has the following medals: " + medals_str)

    for mem_addr_pos in range(10):
        current_keys_int = int.from_bytes(dolphin_memory_engine.read_bytes(KEYS_BITFLD_ADDR + mem_addr_pos, 1), 'big')
        if current_keys_int != ctx.keys_tracked[mem_addr_pos]:
            if ctx.keys_tracked[mem_addr_pos] > 0:
                bit_int = current_keys_int ^ ctx.keys_tracked[mem_addr_pos]
            else:
                bit_int = current_keys_int
            ctx.keys_tracked[mem_addr_pos] = current_keys_int
            for i in range(8):
                if (bit_int & (1<<i)) > 0 and not key_name_collection[mem_addr_pos][i] == "":
                    print("Key Received: '" + key_name_collection[mem_addr_pos][i] + " Key'")

    mario_items_arr_one = int.from_bytes(dolphin_memory_engine.read_bytes(MARIO_ITEMS_RECV_ONE_ADDR, 1), 'big')
    mario_items_arr_two = int.from_bytes(dolphin_memory_engine.read_bytes(MARIO_ITEMS_RECV_TWO_ADDR, 1), 'big')
    mario_items_recv_arr = [(mario_items_arr_one & (1 << 4)), (mario_items_arr_one & (1 << 5)),
                            (mario_items_arr_one & (1 << 6)), (mario_items_arr_one & (1 << 7)),
                            (mario_items_arr_two & (1 << 0))]
    if mario_items_recv_arr != ctx.mario_items_tracked:
        ctx.mario_items_tracked = mario_items_recv_arr
        bool_hat = True if mario_items_recv_arr[0] else False
        bool_star = True if mario_items_recv_arr[1] else False
        bool_glove = True if mario_items_recv_arr[2] else False
        bool_shoe = True if mario_items_recv_arr[3] else False
        bool_letter = True if mario_items_recv_arr[4] else False
        mario_items_str = f"Hat: {bool_hat}; Star: {bool_star}; Glove: {bool_glove}; Shoe: {bool_shoe}; Letter: {bool_letter}"
        print("Currently Luigi has the following mario items: " + mario_items_str)

    for mem_addr_pos in range(7):
        current_boos_int = int.from_bytes(dolphin_memory_engine.read_bytes(BOOS_BITFLD_ADDR + mem_addr_pos, 1), 'big')
        if current_boos_int != ctx.boos_captured[mem_addr_pos]:
            if ctx.boos_captured[mem_addr_pos] > 0:
                bit_int = current_boos_int ^ ctx.boos_captured[mem_addr_pos]
            else:
                bit_int = current_boos_int
            ctx.boos_captured[mem_addr_pos] = current_boos_int
            for i in range(8):
                if (bit_int & (1<<i)) > 0 and not boo_name_collection[mem_addr_pos][i] == "":
                    print("Boo Captured: '" + boo_name_collection[mem_addr_pos][i] + "'")

    # for location, data in ALL_LOCATION_TABLE.items():
    #     checked = False
    #
    #     # Special-case checks TODO CORRECT FOR LM
    #     if data.type == "Special":
    #         # The flag for "Windfall Island - Maggie - Delivery Reward" is still unknown.
    #         # However, as a temporary workaround, we can just check if the player had Moblin's letter at some point,
    #         # but it's no longer in their Delivery Bag
    #         if location == "Windfall Island - Maggie - Delivery Reward":
    #             was_moblins_owned = (dolphin_memory_engine.read_word(LETTER_OWND_ADDR) >> 15) & 1
    #             dbag_contents = [dolphin_memory_engine.read_byte(LETTER_BASE_ADDR + offset) for offset in range(8)]
    #             checked = was_moblins_owned and 0x9B not in dbag_contents
    #
    #         # For Letter from Baito's Mother, we need to check two bytes
    #         # 0x1 = Note to Mom sent, 0x2 = Mail sent by Baito's Mother, 0x3 = Mail read by Link
    #         if location == "Mailbox - Letter from Baito's Mother":
    #             checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3
    #
    #         # For Letter from Grandma, we need to check two bytes
    #         # 0x1 = Grandma saved, 0x2 = Mail sent by Grandma, 0x3 = Mail read by Link
    #         if location == "Mailbox - Letter from Grandma":
    #             checked = dolphin_memory_engine.read_byte(data.address) & 0x3 == 0x3
    #
    #         # For the Ankle's reward, we check if the bits for turning all five statues are set
    #         # For some reason, the bit for the Dragon Tingle Statue is located in a separate location than the rest
    #         if location == "Tingle Island - Ankle - Reward for All Tingle Statues":
    #             dragon_tingle_statue_rewarded = dolphin_memory_engine.read_byte(TINGLE_STATUE_1_ADDR) & 0x40 == 0x40
    #             other_tingle_statues_rewarded = dolphin_memory_engine.read_byte(TINGLE_STATUE_2_ADDR) & 0x0F == 0x0F
    #             checked = dragon_tingle_statue_rewarded and other_tingle_statues_rewarded
    #
    #         # For the Bird-Man Contest, we check if the high score is greater than 250 yards
    #         if location == "Flight Control Platform - Bird-Man Contest - First Prize":
    #             high_score = dolphin_memory_engine.read_byte(FCP_SCORE_LO_ADDR) + (
    #                     dolphin_memory_engine.read_byte(FCP_SCORE_HI_ADDR) << 8
    #             )
    #             checked = high_score > 250
    #
    #     # TODO Change from WW flag system
    #     elif data.stage_id == curr_stage_id:
    #         match data.type:
    #             case LMLocationType.CHART:
    #                 checked = (charts_bitfield >> data.bit) & 1
    #             case LMLocationType.BOCTO:
    #                 checked = (read_short(data.address) >> data.bit) & 1
    #             case LMLocationType.CHEST:
    #                 checked = (chests_bitfield >> data.bit) & 1
    #             case LMLocationType.SWTCH:
    #                 checked = (switches_bitfield >> data.bit) & 1
    #             case LMLocationType.PCKUP:
    #                 checked = (pickups_bitfield >> data.bit) & 1
    #             case LMLocationType.EVENT:
    #                 checked = (dolphin_memory_engine.read_byte(data.address) >> data.bit) & 1
    #
    #     # Sea (Alt) chests
    #     elif curr_stage_id == 0x0 and data.stage_id == 0x1:
    #         assert data.type == LMLocationType.CHEST
    #         checked = (sea_alt_bitfield >> data.bit) & 1
    #
    #     if checked:
    #         location_id = LMLocation.get_apid(data.code)
    #         if location_id:
    #             ctx.locations_checked.add(location_id)
    #         else:
    #             if not ctx.finished_game:
    #                 await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
    #                 ctx.finished_game = True
    #
    # # Send the list of newly-checked locations to the server
    # locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    # if locations_checked:
    #     await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


# TODO CORRECT FOR LM
async def check_alive():
    cur_health = read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


# TODO CORRECT FOR LM
async def check_death(ctx: LMContext):
    if check_ingame():
        cur_health = read_short(CURR_HEALTH_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " scared themselves to death.")
        else:
            ctx.has_send_death = False


def check_ingame():
    return int.from_bytes(dolphin_memory_engine.read_bytes(CURR_PLAY_STATE_ADDR, 4)) == 2
    # return True # read_string(CURR_STAGE_NAME_ADDR, 8) not in ["", "sea_T", "Name"] #TODO PLEASE GOD FIX ME

async def dolphin_sync_task(ctx: LMContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
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
                        logger.info('Enter slot name:')
                        ctx.auth = await ctx.console_input()
                        # ctx.auth = read_string(SLOT_NAME_ADDR, 0x40)
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    if dolphin_memory_engine.read_bytes(0x80000000, 6) != b"GLME01":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
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
            dolphin_memory_engine.un_hook()
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
