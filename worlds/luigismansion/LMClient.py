import asyncio
import os
import time
import traceback

import NetUtils
import Utils
from typing import Any, Optional, Collection

import dolphin_memory_engine as dme

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from worlds import AutoWorldRegister
from settings import get_settings, Settings

from . import CLIENT_VERSION
from .LMGenerator import LuigisMansionRandomizer
from .Items import ALL_ITEMS_TABLE, RECV_ITEMS_IGNORE, RECV_OWN_GAME_ITEMS, BOO_AP_ID_LIST
from .Locations import ALL_LOCATION_TABLE, SELF_LOCATIONS_TO_RECV

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
CURR_MAP_ID_ADDR = 0x804D80A4

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

# This is the flag address we use to determine if Luigi is currently in an Event.
# If this flag is on, do NOT send any items / receive them.
EVENT_FLAG_RECV_ADDRR = 0x803D33B1

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
RANK_REQ_AMTS = [0, 5000000, 20000000, 40000000, 50000000, 60000000, 70000000, 100000000]

# Static time to wait for health and death checks
CHECKS_WAIT = 3
LONGER_MODIFIER = 2

# This address is used to deal with the current display for Captured Boos
BOO_COUNTER_DISPLAY_ADDR = 0x803A3CC4
BOO_COUNTER_DISPLAY_OFFSET = 0x77

# These addresses and bits are used to turn on flags for Boo Count related events.
BOO_WASHROOM_FLAG_ADDR = 0x803D339C
BOO_WASHROOM_FLAG_BIT = 4
BOO_BALCONY_FLAG_ADDR = 0x803D3399
BOO_BALCONY_FLAG_BIT = 2
BOO_FINAL_FLAG_ADDR = 0x803D33A2
BOO_FINAL_FLAG_BIT = 5


def read_short(console_address: int):
    return int.from_bytes(dme.read_bytes(console_address, 2))


def write_short(console_address: int, value: int):
    dme.write_bytes(console_address, value.to_bytes(2))


def read_string(console_address: int, strlen: int):
    return dme.read_bytes(console_address, strlen).decode().strip("\0")


def check_if_addr_is_pointer(addr: int):
    return 2147483648 <= dme.read_word(addr) <= 2172649471


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
        LuigisMansionRandomizer(iso_path, str(os.path.join(directory_to_iso, file_name + ".iso")), output_data)


class LMCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, LMContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, LMContext):
            Utils.async_start(self.ctx.update_death_link(not "DeathLink" in self.ctx.tags), name="Update Deathlink")


class LMContext(CommonContext):
    command_processor = LMCommandProcessor
    game = "Luigi's Mansion"
    items_handling = 0b111
    boo_count: "Label" = None

    def __init__(self, server_address, password):
        """
        Initialize the LM context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)

        # Handle various Dolphin connection related tasks
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False

        # All used when death link is enabled.
        self.is_luigi_dead = False
        self.last_health_checked = time.time()

        # Used for handling received items to the client.
        self.already_mentioned_rank_diff = False
        self.game_clear = False
        self.rank_req = -1
        self.last_not_ingame = time.time()
        self.boosanity = False
        self.boo_washroom_count = None
        self.boo_balcony_count = None
        self.boo_final_count = None

        # Used for handling various weird item checks.
        self.last_map_id = 0

        # Used to let poptracker autotrack Luigi's room
        self.last_room_id = 0

    async def disconnect(self, allow_autoreconnect: bool = False):
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False):
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if password_requested and not self.password:
            await super(LMContext, self).server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Luigi's Mansion ROM loaded in Dolphin. Waiting for player to load into the Foyer. " +
                "For new AP seeds, ensure a new save file is selected (or delete an old game).")
            return
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        super().on_package(cmd, args)
        if cmd == "Connected":  # On Connect
            # Make sure the world version matches
            if not "apworld version" in args["slot_data"] or args["slot_data"]["apworld version"] != CLIENT_VERSION:
                local_version = CLIENT_VERSION if str(args["slot_data"]["apworld version"]) else "N/A"
                raise Utils.VersionException("Error! Server was generated with a different Luigi's Mansion APWorld version. " +
                    f"The client version is {CLIENT_VERSION}! Please verify you are using the same APWorld as the " +
                    f"generator, which is '{local_version}'")

            self.boosanity = bool(args["slot_data"]["boosanity"])
            self.rank_req = int(args["slot_data"]["rank requirement"])
            self.boo_washroom_count = int(args["slot_data"]["washroom boo count"])
            self.boo_balcony_count = int(args["slot_data"]["balcony boo count"])
            self.boo_final_count = int(args["slot_data"]["final boo count"])
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))

    def on_deathlink(self, data: dict[str, Any]):
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        super().on_deathlink(data)
        self.is_luigi_dead = True
        self.set_luigi_dead()
        return

    def run_gui(self):
        from kvui import GameManager

        class LMManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago Luigi's Mansion Client"

        self.ui = LMManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def update_boo_count_label(self):
        from kvui import Label

        if not self.boo_count:
            self.boo_count = Label(text=f"")
            self.ui.connect_layout.add_widget(self.boo_count)

        curr_boo_count = len([item.item for item in self.items_received if item.item in BOO_AP_ID_LIST])

        self.boo_count.text = f"Boo Count: {curr_boo_count}/50"


    def check_alive(self):
        # Our health gets messed up in the Lab, so we can just ignore that location altogether.
        if dme.read_word(CURR_MAP_ID_ADDR) == 1:
            return True

        lm_curr_health = read_short(dme.follow_pointers(CURR_HEALTH_ADDR, [CURR_HEALTH_OFFSET]))
        if "DeathLink" in self.tags:
            # Get the pointer of Luigi's health, as this changes when warping to bosses or climbing into mouse holes.
            if lm_curr_health == 0:
                if time.time() > self.last_health_checked + CHECKS_WAIT:
                    return False
                return True

        if lm_curr_health > 0:
            self.last_health_checked = time.time()
            self.is_luigi_dead = False
            return True

        self.last_health_checked = time.time()
        return False

    def check_ingame(self):
        # The game has an address that lets us know if we are in a playable state or not.
        # This isn't perfect indicator however as although the game says ready, we still map be loading in,
        # warping around, etc.
        int_play_state = dme.read_word(CURR_PLAY_STATE_ADDR)
        if not int_play_state == 2:
            self.last_not_ingame = time.time()
            return False

        curr_map_id = dme.read_word(CURR_MAP_ID_ADDR)

        # This checks for if we warped to another boss arena, which resets our health, so we need a slight delay.
        if curr_map_id != self.last_map_id:
            self.last_map_id = curr_map_id
            self.last_not_ingame = time.time()
            self.already_mentioned_rank_diff = False
            return False

        # These are the only valid maps we want Luigi to have checks with or do health detection with.
        if curr_map_id in [2, 9, 10, 11, 13]:
            if not time.time() > (self.last_not_ingame + (CHECKS_WAIT*LONGER_MODIFIER)):
                return False

            # Even though this is the main mansion map, if the map is unloaded for any reason, there won't be a valid
            # room id, therefore we should not perform any checks yet.
            if curr_map_id == 2:
                bool_loaded_in_map = check_if_addr_is_pointer(ROOM_ID_ADDR)
                return bool_loaded_in_map
            return True

        self.last_not_ingame = time.time()
        return False

    async def check_death(self):
        if self.check_ingame() and not self.check_alive():
            if not self.is_luigi_dead and time.time() >= self.last_death_link + (CHECKS_WAIT*LONGER_MODIFIER*3):
                self.is_luigi_dead = True
                self.set_luigi_dead()
                await self.send_death(self.player_names[self.slot] + " scared themselves to death.")
        return

    def set_luigi_dead(self):
        write_short(dme.follow_pointers(CURR_HEALTH_ADDR, [CURR_HEALTH_OFFSET]), 0)
        return

    async def lm_give_items(self):
        # Only try to give items if we are in game and alive.
        if not (self.check_ingame() and self.check_alive()):
            return

        last_recv_idx = dme.read_word(LAST_RECV_ITEM_ADDR)
        if len(self.items_received) == last_recv_idx:
            return

        # Filter for only items where we have not received yet. If same slot, only receive locations from pre-approved
        # own locations, otherwise accept other slots. Additionally accept only items from a pre-approved list.
        recv_items = self.items_received[last_recv_idx:]

        if len(recv_items) == 0:
            dme.write_word(LAST_RECV_ITEM_ADDR, len(self.items_received))
            return

        # TODO give items from console
        for item in recv_items:
            if item.item in RECV_ITEMS_IGNORE or (item.player == self.slot and not
            (item.location in SELF_LOCATIONS_TO_RECV or item.item in RECV_OWN_GAME_ITEMS)):
                last_recv_idx += 1
                dme.write_word(LAST_RECV_ITEM_ADDR, last_recv_idx)
                continue

            # TODO remove this after an in-game message / dolphin client message is received per item.
            #   Note: Common Client does already have a variation of messages supported though.
            """# Add a received message in the client for the item that is about to be received.
            parts = []
            NetUtils.add_json_text(parts, "Received ")
            NetUtils.add_json_item(parts, item.item, self.slot, item.flags)
            NetUtils.add_json_text(parts, " from ")
            NetUtils.add_json_location(parts, item.location, item.player)
            NetUtils.add_json_text(parts, " by ")
            NetUtils.add_json_text(parts, item.player, type=NetUtils.JSONTypes.player_id)
            self.on_print_json({"data": parts, "cmd": "PrintJSON"})"""

            # Get the current LM Item so we can get the various named tuple fields easier.
            lm_item_name = self.item_names.lookup_in_game(item.item)
            lm_item = ALL_ITEMS_TABLE[lm_item_name]

            # TODO optimize all other cases for reading when a pointer is there vs not.
            for addr_to_update in lm_item.update_ram_addr:
                byte_size = 1 if addr_to_update.ram_byte_size is None else addr_to_update.ram_byte_size

                if not addr_to_update.item_count is None:
                    if not addr_to_update.pointer_offset is None:
                        curr_val = int.from_bytes(dme.read_bytes(dme.follow_pointers(addr_to_update.ram_addr,
            [addr_to_update.pointer_offset]), byte_size))
                        curr_val+= addr_to_update.item_count
                        dme.write_bytes(dme.follow_pointers(addr_to_update.ram_addr,
            [addr_to_update.pointer_offset]), curr_val.to_bytes(byte_size, 'big'))
                    else:
                        curr_val = int.from_bytes(dme.read_bytes(addr_to_update.ram_addr, byte_size))
                        curr_val += addr_to_update.item_count
                        dme.write_bytes(addr_to_update.ram_addr, curr_val.to_bytes(byte_size, 'big'))
                else:
                    if not addr_to_update.pointer_offset is None:
                        curr_val = int.from_bytes(dme.read_bytes(dme.follow_pointers(addr_to_update.ram_addr,
            [addr_to_update.pointer_offset]),byte_size))
                        curr_val = (curr_val | (1 << addr_to_update.bit_position))
                        dme.write_bytes(dme.follow_pointers(addr_to_update.ram_addr,
            [addr_to_update.pointer_offset]), curr_val.to_bytes(byte_size, 'big'))
                    else:
                        curr_val = int.from_bytes(dme.read_bytes(addr_to_update.ram_addr, byte_size))
                        curr_val = (curr_val | (1 << addr_to_update.bit_position))
                        dme.write_bytes(addr_to_update.ram_addr, curr_val.to_bytes(byte_size, 'big'))

            # Update the last received index to ensure we don't receive the same item over and over.
            last_recv_idx += 1
            dme.write_word(LAST_RECV_ITEM_ADDR, last_recv_idx)

            if item.item in BOO_AP_ID_LIST:
                curr_boo_count = len([item.item for item in self.items_received if item.item in BOO_AP_ID_LIST])
                if curr_boo_count >= self.boo_washroom_count:
                    boo_val = dme.read_byte(BOO_WASHROOM_FLAG_ADDR)
                    dme.write_byte(BOO_WASHROOM_FLAG_ADDR, (boo_val | (1 << BOO_WASHROOM_FLAG_BIT)))
                if curr_boo_count >= self.boo_balcony_count:
                    boo_val = dme.read_byte(BOO_BALCONY_FLAG_ADDR)
                    dme.write_byte(BOO_BALCONY_FLAG_ADDR, (boo_val | (1 << BOO_BALCONY_FLAG_BIT)))
                if curr_boo_count >= self.boo_final_count:
                    boo_val = dme.read_byte(BOO_FINAL_FLAG_ADDR)
                    dme.write_byte(BOO_FINAL_FLAG_ADDR, (boo_val | (1 << BOO_FINAL_FLAG_BIT)))

        return

    async def lm_check_locations(self):
        if not (self.check_ingame() and self.check_alive()):
            return

        # There will be different checks on different maps.
        current_map_id = dme.read_word(CURR_MAP_ID_ADDR)

        for mis_loc in self.missing_locations:
            local_loc = self.location_names.lookup_in_game(mis_loc)
            lm_loc_data = ALL_LOCATION_TABLE[local_loc]

            #TODO Maybe helper function can get map id included?
            # If in Boolossus Arena, check Boo ids
            if current_map_id == 11:
                if not mis_loc in BOO_AP_ID_LIST:
                    continue

                #TODO account for ram offsets and other similar things.
                for addr_to_update in lm_loc_data.update_ram_addr:
                    current_boo_state = dme.read_byte(addr_to_update.ram_addr)
                    if (current_boo_state & (1 << addr_to_update.bit_position)) > 0:
                        self.locations_checked.add(mis_loc)

            # If in main mansion map
            elif current_map_id == 2:
                #TODO move this... maybe to check in game?
                current_room_id = dme.read_word(dme.follow_pointers(ROOM_ID_ADDR, [ROOM_ID_OFFSET]))
                if current_room_id != self.last_room_id:
                    await self.send_msgs([{
                        "cmd": "Set",
                        "key": f"lm_room_{self.team}_{self.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": current_room_id}]
                    }])
                    self.last_room_id = current_room_id

                #TODO optimize all other cases for reading when a pointer is there vs not.
                for addr_to_update in lm_loc_data.update_ram_addr:
                    # Only check locations that are currently in the same room as us.
                    if not addr_to_update.in_game_room_id == current_room_id:
                        continue

                    match lm_loc_data.type:
                        case "Furniture" | "Plant":
                            # Check all possible furniture addresses. #TODO Find a way to not check all 600+
                            for current_offset in range(0, FURNITURE_ADDR_COUNT, 4):
                                # Only check if the current address is a pointer
                                current_addr = FURNITURE_MAIN_TABLE_ID + current_offset
                                if not check_if_addr_is_pointer(current_addr):
                                    continue

                                furn_id = dme.read_word(dme.follow_pointers(current_addr, [FURN_ID_OFFSET]))
                                if not furn_id == lm_loc_data.jmpentry:
                                    continue

                                furn_flag = dme.read_word(dme.follow_pointers(current_addr, [FURN_FLAG_OFFSET]))
                                if furn_flag > 0:
                                    self.locations_checked.add(mis_loc)
                        case _:
                            byte_size = 1 if addr_to_update.ram_byte_size is None else addr_to_update.ram_byte_size
                            if not addr_to_update.pointer_offset is None:
                                curr_val = int.from_bytes(dme.read_bytes(dme.follow_pointers(addr_to_update.ram_addr,
                    [addr_to_update.pointer_offset]), byte_size))
                                if (curr_val & (1 << addr_to_update.bit_position)) > 0:
                                    self.locations_checked.add(mis_loc)
                            else:
                                curr_val = int.from_bytes(dme.read_bytes(addr_to_update.ram_addr, byte_size))
                                if (curr_val & (1 << addr_to_update.bit_position)) > 0:
                                    self.locations_checked.add(mis_loc)

        await self.check_locations(self.locations_checked)

        # If on final boss with King Boo
        if current_map_id == 9:
            beat_king_boo = dme.read_byte(KING_BOO_ADDR)
            if (beat_king_boo & (1 << 5)) > 0 and not self.game_clear:
                int_rank_sum = 0
                req_rank_amt = RANK_REQ_AMTS[self.rank_req]
                for key in WALLET_OFFSETS.keys():
                    currency_amt = dme.read_word(dme.follow_pointers(WALLET_START_ADDR, [key]))
                    int_rank_sum += currency_amt * WALLET_OFFSETS[key]
                if int_rank_sum >= req_rank_amt:
                    self.game_clear = True
                else:
                    if not self.already_mentioned_rank_diff:
                        logger.info("Unfortunately, you do NOT have enough money to satisfy the rank" +
                                f"requirements.\nYou are missing: '{(req_rank_amt - int_rank_sum):,}'")
                        self.already_mentioned_rank_diff = True

        if not self.finished_game and self.game_clear:
            self.finished_game = True
            await self.send_msgs([{
                "cmd": "StatusUpdate",
                "status": NetUtils.ClientStatus.CLIENT_GOAL,
            }])
        return

    async def lm_update_non_savable_ram(self):
        if not (self.check_ingame() and self.check_alive()):
            return

        # Always adjust the Vacuum speed as saving and quitting or going to E. Gadds lab could reset it back to normal.
        vac_id = AutoWorldRegister.world_types[self.game].item_name_to_id["Poltergust 4000"]
        if any([netItem.item for netItem in self.items_received if netItem.item == vac_id]):
            vac_speed = "3800000F"
            dme.write_bytes(ALL_ITEMS_TABLE["Poltergust 4000"].update_ram_addr[0].ram_addr, bytes.fromhex(vac_speed))

        #TODO Validate in game display has moved so we don't need this anymore.
        # Always reset the Boo's location captured RAM byte back to 0, only if it's been captured before.
        # Although Boo items share the same address, we are not using it currently.
        #for lm_boo in BOO_LOCATION_TABLE.keys():
        #    lm_boo_item = BOO_LOCATION_TABLE[lm_boo]
        #    if not AutoWorldRegister.world_types[self.game].location_name_to_id[lm_boo] in self.checked_locations:
        #        continue
        #    boo_caught = dme.read_byte(lm_boo_item.room_ram_addr)
        #    dme.write_byte(lm_boo_item.room_ram_addr, boo_caught & ~(1 << lm_boo_item.locationbit))

        return

    # TODO remove this in favor of 0.6.0's implementation.
    async def check_locations(self, locations: Collection[int]) -> set[int]:
        """Send new location checks to the server. Returns the set of actually new locations that were sent."""
        locations = set(locations) & self.missing_locations
        if locations:
            await self.send_msgs([{"cmd": 'LocationChecks', "locations": tuple(locations)}])
        return locations

async def dolphin_sync_task(ctx: LMContext):
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")

    while not ctx.exit_event.is_set():
        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not ctx.check_ingame():
                    await asyncio.sleep(0.1)
                    continue
                if ctx.slot:
                    # Update boo count in LMClient
                    if ctx.ui:
                        await ctx.update_boo_count_label()
                    if "DeathLink" in ctx.tags:
                        await ctx.check_death()
                    await ctx.lm_give_items()
                    await ctx.lm_check_locations()
                    await ctx.lm_update_non_savable_ram()
                else:
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR, SLOT_NAME_STR_LENGTH)
                        if not ctx.auth:
                            ctx.auth = None
                            ctx.awaiting_rom = False
                            logger.info("No slot name was detected. Ensure a randomized ROM is loaded, " +
                                        "retrying in 5 seconds...")
                            ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                            dme.un_hook()
                            await asyncio.sleep(5)
                            continue
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS

                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if not dme.is_hooked():
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue

                if ((read_string(0x80000000, 6) == "GLME01" or
                        read_string(0x80000000, 6) == "GLMJ01") or
                        read_string(0x80000000, 6) == "GLMP01"):
                    logger.info(CONNECTION_REFUSED_GAME_STATUS)
                    ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                    dme.un_hook()
                    await asyncio.sleep(5)
                    continue

                logger.info(CONNECTION_CONNECTED_STATUS)
                ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                ctx.locations_checked = set()
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
        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)
