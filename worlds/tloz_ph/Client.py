import random
import time
import logging
from typing import TYPE_CHECKING, Set, Dict, Any

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from Utils import async_start
from worlds._bizhawk.client import BizHawkClient
from worlds.tloz_ph import LOCATIONS_DATA, ITEMS_DATA
from .data.Constants import *
from .Util import *

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

ROM_ADDRS = {
    "game_identifier": (0x00000000, 16, "ROM"),
    "slot_name": (0xFFFC0, 64, "ROM"),
}

RAM_ADDRS = {
    "game_state": (0x060C48, 1, "Main RAM"),
    "in_cutscene": (0x060F78, 1, "Main RAM"),

    "link_health": (0x1CB08E, 2, "Main RAM"),
    "boat_health": (0x1FA036, 1, "Main RAM"),
    "salvage_health": (0x1F5720, 1, "Main RAM"),

    "received_item_index": (0x1BA64C, 2, "Main RAM"),
    "slot_id": (0x1BA64A, 2, "Main RAM"),

    "stage": (0x1B2E94, 4, "Main RAM"),
    "floor": (0x1B2E98, 4, "Main RAM"),
    "room": (0x1B2EA6, 1, "Main RAM"),
    "entrance": (0x1B2EA7, 1, "Main RAM"),
    "flags": (0x1B557C, 52, "Main RAM"),

    "getting_item": (0x1B6F44, 1, "Main RAM"),
    "shot_frog": (0x1B7038, 1, "Main RAM"),
    "getting_ship_part": (0x11F5E4, 1, "Main RAM"),
    "getting_salvage": (0x1BA654, 1, "Main RAM"),

    "link_x": (0x1B6FEC, 4, "Main RAM"),
    "link_y": (0x1B6FF0, 4, "Main RAM"),
    "link_z": (0x1B6FF4, 4, "Main RAM"),
    "using_item:": (0x1BA71C, 1, "Main RAM"),
    "drawing_sea_route": (0x241570, 1, "Main RAM"),
    "boat_x": (0x1B8518, 4, "Main RAM"),
    "boat_z": (0x1B8520, 4, "Main RAM"),
    "save_slot": (0x1B8124, 1, "Main RAM"),
    "equipped_item": (0x1BA520, 4, "Main RAM"),
    "got_item_menu": (0x19A5B0, 1, "Main RAM"),

    "loading_stage": (0x1B2E78, 1, "Main RAM"),  # 0 when loading stage, some sorta pointer
    "loading_room": (0x10BD6F, 1, "Main RAM"),  # 0 when not loading room

    "opened_clog": (0x0FC5BC, 1, "Main RAM"),
    "flipped_clog": (0x0FA37B, 1, "Main RAM"),

}

POINTERS = {
    "ADDR_gItemManager": 0x0fb4,
    "ADDR_gPlayerManager": 0x0fbc,
    "ADDR_gAdventureFlags": 0x0f74,
    "ADDR_gPlayer": 0x0f90,
    "ADDR_gOverlayManager_mLoadedOverlays_4": 0x0910,
    "ADDR_gMapManager": 0x0e60
}

# gMapManager -> mCourse -> mSmallKeys
SMALL_KEY_OFFSET = 0x260
STAGE_FLAGS_OFFSET = 0x268

# Addresses to read each cycle
read_keys_always = ["game_state", "in_cutscene", "received_item_index", "stage", "room", "slot_id",
                    "loading_room",
                    "opened_clog"]
read_keys_deathlink = ["link_health"]
read_keys_land = ["getting_item", "getting_ship_part"]
read_keys_sea = ["shot_frog", "getting_salvage"]
read_keys_deathlink_sea = ["boat_health", "drawing_sea_route"]
read_keys_deathlink_salvage = ["salvage_health"]


# Split up large values to write into smaller chunks
def split_bits(value, size):
    ret = []
    f = 0xFFFFFFFFFFFFFF00
    for _ in range(size):
        ret.append(value & 0xFF)
        value = (value & f) >> 8
    return ret


def item_count(ctx, item_name):
    return sum([1 for i in ctx.items_received if i.item == ITEMS_DATA[item_name]["id"]])


# Read list of address data
async def read_memory_values(ctx, read_list: dict[str, tuple[int, int, str]], signed=False) -> dict[str, int]:
    keys = read_list.keys()
    read_data = [(a, s, d) for a, s, d in read_list.values()]
    read_result = await bizhawk.read(ctx.bizhawk_ctx, read_data)
    values = [int.from_bytes(i, "little", signed=signed) for i in read_result]
    return {key: value for key, value in zip(keys, values)}


# Read single address
async def read_memory_value(ctx, address: int, size=1, domain="Main RAM", signed=False, silent=False) -> int:
    read_result = await bizhawk.read(ctx.bizhawk_ctx, [(address, size, domain)])
    if not silent:
        print("Reading memory value", hex(address), size, domain, ", got value",
              hex(int.from_bytes(read_result[0], "little")))
    return int.from_bytes(read_result[0], "little", signed=signed)


# Write single address
async def write_memory_value(ctx, address: int, value: int, domain="Main RAM", incr=None, size=1, unset=False,
                             overwrite=False):
    prev = await read_memory_value(ctx, address, size, domain)
    if incr is not None:
        value = -value if unset else value
        if incr:
            write_value = prev + value
        else:
            write_value = prev - value
        write_value = 0 if write_value <= 0 else write_value
    else:
        if unset:
            print(f"Unseting bit {hex(address)} {hex(value)} with filter {hex(~value)} from prev {hex(prev)} "
                  f"for result {hex(prev & (~value))}")
            write_value = prev & (~value)
        elif not overwrite:
            write_value = prev | value
        else:
            write_value = value
    if size > 1:
        write_value = split_bits(write_value, size)
    else:
        write_value = [write_value]
    print(f"Writing Memory: {hex(address)}, {write_value}, {size}, {domain}, {incr}, {unset}")
    await bizhawk.write(ctx.bizhawk_ctx, [(address, write_value, domain)])
    return write_value


# Write list of values starting from address
async def write_memory_values(ctx, address: int, values: list, domain="Main RAM", overwrite=False):
    if not overwrite:
        prev = await read_memory_value(ctx, address, len(values), domain)
        new_values = [old | new for old, new in zip(split_bits(prev, 4), values)]
        print(f"values: {new_values}, old: {split_bits(prev, 4)}")
    else:
        new_values = values
    await bizhawk.write(ctx.bizhawk_ctx, [(address, new_values, domain)])


# Get address from pointer
async def get_address_from_heap(ctx, pointer=POINTERS["ADDR_gMapManager"], offset=0) -> int:
    m_course = 0
    while m_course == 0:
        m_course = await read_memory_value(ctx, pointer, 4, domain="Data TCM")
    read = await read_memory_value(ctx, m_course - 0x02000000, 4)
    print(f"Got map address @ {hex(read + offset - 0x02000000)}")
    return read + offset - 0x02000000


# Get address for small key count in current stage
async def get_small_key_address(ctx):
    return await get_address_from_heap(ctx, offset=SMALL_KEY_OFFSET)


class PhantomHourglassClient(BizHawkClient):
    game = "The Legend of Zelda - Phantom Hourglass"
    system = "NDS"
    local_checked_locations: Set[int]
    local_scouted_locations: Set[int]
    local_tracker: Dict[str, Any]
    item_id_to_name: Dict[int, str]
    location_name_to_id: Dict[str, int]
    location_area_to_watches: Dict[int, dict[str, dict]]
    watches: Dict[str, tuple[int, int, str]]

    def __init__(self) -> None:
        super().__init__()
        self.item_id_to_name = build_item_id_to_name_dict()
        self.location_name_to_id = build_location_name_to_id_dict()
        self.location_area_to_watches = build_location_room_to_watches()
        self.scene_to_dynamic_flag = build_scene_to_dynamic_flag()
        self.hint_scene_to_watches = build_hint_scene_to_watches()

        self.local_checked_locations = set()
        self.local_scouted_locations = set()
        self.local_tracker = {}

        self.set_deathlink = False
        self.last_deathlink = None
        self.was_alive_last_frame = False
        self.is_expecting_received_death = False

        self.save_slot = 0
        self.version_offset = 0

        self.last_scene = None
        self.locations_in_scene = {}
        self.watches = {}
        self.receiving_location = False
        self.last_vanilla_item: list[str] = []
        self.delay_reset = False
        self.last_treasures = 0
        self.last_ship_parts = []
        self.last_potions = [0, 0]

        self.removed_boomerang = False

        self.previous_game_state = False
        self.just_entered_game = False
        self.current_stage = 0xB
        self.main_read_list = {}
        self.last_stage = None
        self.entering_from = None
        self.entering_dungeon = None
        self.unset_dynamic_watches = []
        self.stage_address = 0
        self.new_stage_loading = None
        self.at_sea = False
        self.getting_location_type = None

        self.entered_entrance = False
        self.loading_scene = False
        self.backup_coord_read = None

        self.warp_to_start_flag = False

        self.delay_pickup: list[str, list[list[str, str, int]]] or None = None
        self.last_key_count = 0
        self.key_address = 0
        self.key_value = 0
        self.metal_count = 0
        self.goal_room = 0x3600

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            print(f"Rom Name: {rom_name}")
            if rom_name != "ZELDA_DS:PHAZEP":  # EU
                if rom_name == "ZELDA_DS:PHAZEE":  # US
                    self.version_offset = -64
                    return False
                else:
                    return False
        except bizhawk.RequestFailedError:
            print("Invalid rom")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.15

        return True

    def on_package(self, ctx, cmd, args):
        if cmd == 'Connected':
            if 'death_link' in args['slot_data'] and args['slot_data']['death_link']:
                self.set_deathlink = True
                self.last_deathlink = time.time()
        super().on_package(ctx, cmd, args)

    async def set_starting_flags(self, ctx: "BizHawkClientContext") -> None:
        write_list = [(RAM_ADDRS["slot_id"][0], [ctx.slot], "Main RAM")]
        print("New game, setting starting flags")
        print(ctx.slot_data)
        for adr, value in STARTING_FLAGS:
            write_list.append((adr, [value], "Main RAM"))

        # Set starting time for PH, removed since ph became an item
        # ph_time = ctx.slot_data["ph_starting_time"] * 60
        ph_time_bits = split_bits(0, 4)
        print(ph_time_bits)
        write_list.append((0x1BA528, ph_time_bits, "Main RAM"))

        # Set Frog flags if not randomizing frogs
        if ctx.slot_data["randomize_frogs"] == 1:
            write_list += [(a, [v], "Main RAM") for a, v in STARTING_FROG_FLAGS]
        # Set Fog Flags
        fog_bits = FOG_SETTINGS_FLAGS[ctx.slot_data["fog_settings"]]
        if len(fog_bits) > 0:
            write_list += [(a, [v], "Main RAM") for a, v in fog_bits]
        if ctx.slot_data["skip_ocean_fights"] == 1:
            write_list += [(0x1B5592, [0x84], "Main RAM")]
        # Ban player from harrow if not randomized
        if ctx.slot_data["randomize_harrow"] == 0:
            write_list += [(0x1B559A, [0x18], "Main RAM")]

        await bizhawk.write(ctx.bizhawk_ctx, write_list)
        self.removed_boomerang = False

    # Boomerang is set to enable item menu, called on s+q to remove it again.
    async def boomerwatch(self, ctx) -> bool:
        if await read_memory_value(ctx, *RAM_ADDRS["got_item_menu"]) > 0:
            # Check if boomerang has been received
            for item in ctx.items_received:
                if item.item == ITEMS_DATA["Boomerang"]["id"]:
                    return True
            # Otherwise remove boomerang
            boomerang = ITEMS_DATA["Boomerang"]
            await write_memory_value(ctx, boomerang["address"], boomerang["value"], unset=True)

            test = await read_memory_value(ctx, boomerang["address"], 1, "Main RAM", silent=True)
            return True
        else:
            return False

    def update_metal_count(self, ctx):
        metal_ids = [ITEMS_DATA[i]["id"] for i in ITEM_GROUPS["Metals"]]
        self.metal_count = sum(1 for i in ctx.items_received if i.item in metal_ids)

    async def update_treasure_tracker(self, ctx):
        self.last_treasures = await read_memory_value(ctx, 0x1BA5AC, 8)
        # print(f"Treasure Tracker! {split_bits(self.last_treasures, 8)}")

    async def give_random_treasure(self, ctx):
        address = 0x1BA5AC + random.randint(0, 7)
        await write_memory_value(ctx, address, 1, incr=True)
        await self.update_treasure_tracker(ctx)

    async def update_potion_tracker(self, ctx):
        read_list = {"left": (0x1BA5D8, 1, "Main RAM"),
                     "right": (0x1BA5D9, 1, "Main RAM")}
        reads = await read_memory_values(ctx, read_list)
        self.last_potions = list(reads.values())

    def get_coord_address(self, at_sea=None, multi=False) -> dict[str, tuple[int, int, str]]:
        if not multi:
            at_sea = self.at_sea if at_sea is None else at_sea
            if at_sea:
                return {k: v for k, v in RAM_ADDRS.items() if k in ["boat_x", "boat_z"]}
            elif not at_sea:
                return {k: v for k, v in RAM_ADDRS.items() if k in ["link_x", "link_y", "link_z"]}
        return {k: v for k, v in RAM_ADDRS.items() if k in ["link_x", "link_y", "link_z"] + ["boat_x", "boat_z"]}

    async def get_coords(self, ctx, multi=False):
        coords = await read_memory_values(ctx, self.get_coord_address(multi=multi), signed=True)
        if not multi:
            return {
                "x": coords.get("link_x", coords.get("boat_x", 0)),
                "y": coords.get("link_y", 0),
                "z": coords.get("link_z", coords.get("boat_z", 0))
            }
        return coords

    async def get_main_read_list(self, ctx, stage, in_game=True):
        read_keys = read_keys_always.copy()
        death_link_keys = []
        death_link_reads = {}
        death_link_pointers = {}
        if stage is not None:
            if stage == 0:
                read_keys += read_keys_sea
                death_link_keys = read_keys_deathlink_sea
                self.at_sea = True
            elif stage == 3:
                death_link_keys = read_keys_deathlink_salvage
                # Add separate reads for instant-repairs
                read_keys += read_keys_deathlink_salvage
            else:
                read_keys += read_keys_land + read_keys_deathlink
                if in_game:
                    death_link_pointers["link_health"] = ("ADDR_gPlayer", 0xa)
                self.at_sea = False

            # Read health for deathlink and cancelling warp to start on death
            for key in death_link_keys:
                value = RAM_ADDRS[key]
                if key in ["boat_health", "salvage_health"]:
                    key = "link_health"
                death_link_reads[key] = value

            death_link_reads |= {key: value for key, value in RAM_ADDRS.items() if key in death_link_keys}

            for name, pointer in death_link_pointers.items():
                addr, offset = pointer
                pointer_1 = await read_memory_value(ctx, POINTERS[addr], 4, "Data TCM")
                death_link_reads[name] = (pointer_1 + offset - 0x2000000, 2, "Main RAM")

            self.main_read_list = {k: v for k, v in RAM_ADDRS.items() if k in read_keys} | death_link_reads
        else:
            self.at_sea = None
        # print(f"Read kwys {read_keys}, {death_link_reads}, {stage}")

    async def full_heal(self, ctx, bonus=0):
        if not self.at_sea:
            hearts = item_count(ctx, "Heart Container") + 3 + bonus
            health_address = await read_memory_value(ctx, POINTERS["ADDR_gPlayer"], 4, "Data TCM") + 0xA - 0x2000000
            print(f"Sent full heal hearts {hearts} addr {hex(health_address)}")
            await write_memory_values(ctx, health_address, split_bits(hearts * 4, 2), overwrite=True)

    async def refill_ammo(self, ctx):
        items = [i + " (Progressive)" for i in ["Bombs", "Bombchus", "Bow"]]

        # Count upgrades
        counts = {ITEMS_DATA[i]["id"]: 0 for i in items}
        for i in ctx.items_received:
            for k in counts:
                if k == i.item:
                    counts[k] += 1

        # Write Upgrades
        write_list = []
        for i, count in enumerate(counts.values()):
            data = ITEMS_DATA[items[i]]
            write_list += [(data["ammo_address"], [data["give_ammo"][count - 1]], "Main RAM")]
        await bizhawk.write(ctx.bizhawk_ctx, write_list)
        await self.full_heal(ctx)
        logger.info(f"You drink a glass of milk. You feel refreshed.")

    def get_progress(self, ctx, scene=0):
        # Count current metals
        progress = 0
        metals = [ITEMS_DATA[i]["id"] for i in ITEM_GROUPS["Metals"]]
        for i in ctx.items_received:
            if i.item in metals:
                progress += 1

        # Figure out totals
        if ctx.slot_data["goal_requirements"] < 2:
            total = ctx.slot_data["dungeons_required"]
            required = total
        elif ctx.slot_data["goal_requirements"] == 2:
            total = ctx.slot_data["metal_hunt_total"]
            required = ctx.slot_data["metal_hunt_required"]
        else:
            return True

        if scene == 0xB0A:
            # Oshus Text
            bellum_texts = ["spawns the phantoms in TotOK B13.",
                            "opens the staircase to Bellum at the bottom of TotOK.",
                            "opens the blue warp to Bellum in TotOK.",
                            "spawns the ruins of the Ghost Ship in the SW Quadrant.",
                            "wins the game."]
            logger.info(f"You have {progress} out of {required} rare metals. There are {total} metals in total.\n"
                        f"Finding the metals {bellum_texts[ctx.slot_data['bellum_access']]}")
        elif scene == 0x160A:
            zauz_required = ctx.slot_data["zauz_required_metals"]
            logger.info(f"Zauz needs {zauz_required} rare metals to give an item. You have {progress}/{total} metals.")

    def get_ending_room(self, ctx):
        if ctx.slot_data["goal_requirements"] == "beat_bellumbeck":
            self.goal_room = 0x3600
        elif ctx.slot_data["goal_requirements"] == "triforce_door":
            self.goal_room = 0x2509

    # Main Loop
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot is None:
            self.just_entered_game = True
            self.last_scene = None
            # print(f"NOT CONNECTED {ctx.server} {ctx.server.socket.open} {ctx.server.socket.closed} {ctx.slot}")
            return

        # Enable "DeathLink" tag if option was enabled
        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)

        # Get main read list before entering loop
        if self.just_entered_game:
            await self.get_main_read_list(ctx, self.current_stage, in_game=False)

        try:
            # await bizhawk.lock(ctx.bizhawk_ctx)
            read_result = await read_memory_values(ctx, self.main_read_list)

            in_game = read_result["game_state"]
            in_cutscene = not read_result["in_cutscene"]
            slot_memory = read_result["slot_id"]
            current_stage = read_result["stage"]
            self.current_stage = current_stage

            # loading_stage = not read_result["loading_stage"]
            loading_room = read_result["loading_room"]
            loading_scene = loading_room # or loading_stage
            loading = loading_scene or self.entered_entrance

            # If player is on title screen, don't do anything else
            if not in_game or current_stage not in STAGES:
                self.previous_game_state = False
                print("NOT IN GAME")
                # Finished game?
                if not ctx.finished_game:
                    await self.process_game_completion(ctx, current_stage)
                return

            # On entering game from main menu
            if in_game and not self.previous_game_state:
                self.just_entered_game = True
                self.last_stage = None
                self.last_scene = None
                self.removed_boomerang = False  # Catches stray item menu errors, only 1 read
                self.save_slot = await read_memory_value(ctx, RAM_ADDRS["save_slot"][0], silent=True)
                self.get_ending_room(ctx)
                self.update_metal_count(ctx)
                # await bizhawk.set_message_interval(ctx.bizhawk_ctx, 10)
                print(f"Started Game")

            # If new file, set up starting flags
            if slot_memory == 0:
                if await read_memory_value(ctx, 0x1b55a8, silent=True) & 2:  # Check if watched intro cs
                    await self.set_starting_flags(ctx)
                    print(f"Set starting flags for slot {slot_memory}")
                else:
                    return

            # Get current scene
            current_room = read_result["room"]
            current_room = 0 if current_room == 0xFF else current_room  # Resetting in a dungeon sets a special value
            current_scene = current_stage * 0x100 + current_room

            # This go true when link gets item
            if self.at_sea:
                getting_location = read_result.get("shot_frog", False)
            else:
                getting_location = read_result.get("getting_item", 0) & 0x20 or read_result.get("getting_ship_part",
                                                                                                False)
            # Other game variables
            num_received_items = read_result["received_item_index"]
            is_dead = not read_result.get("link_health", True)
            salvage_health = read_result.get("salvage_health", 5)
            drawing_on_sea_chart = read_result.get("drawing_sea_route", False)
            opened_clog = read_result.get("opened_clog", False)

            # Process on new room. As soon as it's triggered, changing the scene variable causes entrance destination
            # await bizhawk.lock(ctx.bizhawk_ctx)  # Lock to try and catch entrance warp
            if current_scene != self.last_scene and not self.entered_entrance and not self.loading_scene:
                if self.last_scene is not None:
                    print(f"New Room: {hex(current_scene)} last room {hex(self.last_scene)}")
                else:
                    print(f"New Room: {hex(current_scene)} last room {self.last_scene}")

                # Backup in case of missing loading
                self.backup_coord_read = await self.get_coords(ctx, multi=True)
                print("Backup: ", self.backup_coord_read)

                # Trigger a different entrance to vanilla
                current_scene = await self.entrance_warp(ctx, current_scene)

                # Set dynamic flags on scene
                await self.set_dynamic_flags(ctx, current_scene)

                print(f"Entered new scene {hex(current_scene)}")
                self.entered_entrance = time.time()  # Triggered first part of loading - setting new room
                self.entering_dungeon = None
                self.delay_reset = False

            # await bizhawk.unlock(ctx.bizhawk_ctx)

            # Nothing happens while loading
            if not loading and not self.loading_scene and not self.entered_entrance:

                # TODO Debug send message on sword send
                if not await read_memory_value(ctx, 0x1ba644, silent=True) & 1:
                    if ctx.items_received and ctx.items_received[-1].item != 1 and 1 in [i.item for i in
                                                                                         ctx.items_received]:
                        for _ in range(20):
                            logger.warning("CRITICAL(ish) ERROR DETECTED!!!")
                        logger.warning("CRITICAL ERROR DETECTED!!!\n"
                                       f"Sword disappear on scene {hex(current_scene)}\n"
                                       f"Dynaflags {await self.set_dynamic_flags(ctx, current_scene)}\n"
                                       f"reads in scene {self.watches}\n"
                                       f"last 5 item {ctx.items_received[-5:]}"
                                       f"Last vanilla items {self.last_vanilla_item}\n"
                                       f"Delay pickup {self.delay_pickup} delay reset {self.delay_reset}\n"
                                       f"Getting location {getting_location} receiving location {self.receiving_location}")
                        await write_memory_value(ctx, 0x1ba644, 1)
                        logger.info(
                            "Your sword has been returned. The day is saved, but please contact the dev anyway.")

                # Read for checks on specific global flags
                if len(self.watches) > 0:
                    watch_result = await read_memory_values(ctx, self.watches)
                    for loc_name, prev_value in watch_result.items():
                        loc_data = LOCATIONS_DATA[loc_name]
                        if prev_value & loc_data["value"]:
                            print(f"Got read item {loc_name} from address {loc_data['address']} "
                                  f"looking at bit {loc_data['value']}")

                            # force_remove = ITEMS_DATA[loc_data["vanilla_item"]].get("incremental", False)
                            force_remove = False
                            await self.process_checked_locations(ctx, loc_name, force_remove)
                            self.receiving_location = True
                            self.watches.pop(loc_name)

                # Check if link is getting location
                if getting_location and not self.receiving_location and self.locations_in_scene is not None:
                    self.receiving_location = True
                    print("Receiving Item")
                    await self.process_checked_locations(ctx, None, detection_type=self.getting_location_type)

                # Process received items
                if num_received_items < len(ctx.items_received):
                    await self.process_received_items(ctx, num_received_items)

                # Exit location received cs
                if self.receiving_location and not getting_location and not self.delay_reset:
                    print("Item Received Successfully")
                    self.receiving_location = False

                    # Check for delayed pickup first!
                    if self.delay_pickup is not None:
                        print(f"Delay pickup {self.delay_pickup}")
                        fallback, pickups = self.delay_pickup
                        need_fallback = True
                        for location, item, value in pickups:
                            if "Small Key" in item:
                                self.key_value = await read_memory_value(ctx, self.key_address)
                                new_item_read = self.key_value
                            else:
                                check_item = ITEMS_DATA[item]
                                new_item_read = await read_memory_value(ctx, check_item["address"],
                                                                        check_item.get("size", 1))
                            if "Rupee" in item:
                                if new_item_read - value == ITEMS_DATA[item]["value"]:
                                    await self.process_checked_locations(ctx, location, True)
                                    need_fallback = False
                            elif new_item_read != value:
                                await self.process_checked_locations(ctx, location, True)
                                need_fallback = False

                        if need_fallback:
                            await self.process_checked_locations(ctx, fallback, True)

                        self.delay_pickup = None
                        self.last_key_count = 0

                    # Remove vanilla item
                    elif self.last_vanilla_item:
                        await self.remove_vanilla_item(ctx, num_received_items)

                # Address reads often give items before animation
                if self.delay_reset and getting_location:
                    self.delay_reset = False
                    self.receiving_location = False
                    print(f"Delay reset over for {self.last_vanilla_item}")

                # Opened clog warp to start check
                if opened_clog:
                    if await read_memory_value(ctx, *RAM_ADDRS["flipped_clog"], silent=True) & 1:
                        if not self.warp_to_start_flag:
                            logger.info(f"Primed a warp to start. Enter a transition to warp to {STAGES[0xB]}.")
                        self.warp_to_start_flag = True
                    else:
                        if self.warp_to_start_flag and await read_memory_value(ctx, *RAM_ADDRS["opened_clog"]):
                            logger.info("Canceled warp to start.")
                            self.warp_to_start_flag = False

                # Cancel warp to start if in a dangerous situation
                if self.warp_to_start_flag:
                    # Cyclone slate warp to start crashes, prevent that from working
                    if self.at_sea:
                        if await read_memory_value(ctx, 0x1B636C):
                            self.warp_to_start_flag = False
                            logger.info("Canceled warp to start, Cyclone Slate is not a valid warp method")
                    if is_dead:
                        self.warp_to_start_flag = False
                        logger.info("Canceled warp to start, death is not a valid warp method")

                # Auto-repair salvage arm if you have a kit
                if salvage_health <= 1:
                    await self.instant_repair_salvage_arm(ctx)

                # Finished game?
                if not ctx.finished_game:
                    await self.process_game_completion(ctx, current_scene)

                # Process Deathlink
                if "DeathLink" in ctx.tags and not drawing_on_sea_chart and not in_cutscene:
                    # print(f"Deathlink {read_result['link_health']}, {is_dead}")
                    await self.process_deathlink(ctx, is_dead, self.current_stage)

            # Started actual scene loading
            if self.entered_entrance and loading_scene:
                self.loading_scene = True  # Second phase of loading room
                self.entered_entrance = False
                print("Loading Scene", current_scene)

            # Fully loaded room
            if self.loading_scene and not loading:
                print("Fully Loaded Room", current_scene)
                self.loading_scene = False
                self.backup_coord_read = None
                await self.load_local_locations(ctx, current_scene)
                await self.update_potion_tracker(ctx)
                await self.update_treasure_tracker(ctx)
                await self.process_scouted_locations(ctx, current_scene)

                # Check if entering dungeon
                if current_stage in DUNGEON_KEY_DATA and self.last_stage != current_stage:
                    self.entering_dungeon = current_stage
                    self.entering_from = self.last_scene
                else:
                    self.entering_from = current_scene  # stage and room

                # Run entering stage code
                if self.last_stage != current_stage:
                    print("Fully Loaded Stage")
                    await self.enter_stage(ctx, current_stage, current_scene)
                    await self.get_main_read_list(ctx, current_stage)

                # Hard coded room stuff
                # Yellow warp in TotOK saves keys
                if self.last_scene is not None:
                    if current_scene == 0x2509 and self.last_scene == 0x2507:  # TODO: set constants for these rooms
                        await self.write_totok_midway_keys(ctx)

                # Repair salvage arm in certain rooms
                if current_scene in [0x130A, 0x500]:
                    await self.repair_salvage_arm(ctx, current_scene)

                # Milk bar refills all ammo
                if current_scene in [0xb0C]:
                    await self.refill_ammo(ctx)

                # Oshus gives metal info
                if current_scene in [0xB0A, 0x160A]:
                    self.get_progress(ctx, current_scene)

                self.last_stage = current_stage
                self.last_scene = current_scene

            self.previous_game_state = in_game
            self.just_entered_game = False

            # In case of a short load being missed, have a backup check on coords (they stay the same during transitions)
            if self.entered_entrance and self.backup_coord_read:
                if time.time() - self.entered_entrance > 2:
                    if self.backup_coord_read != await self.get_coords(ctx, multi=True):
                        self.loading_scene = True  # Second phase of loading room
                        self.entered_entrance = False
                        print("Missed loading read, using backup")

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            print("Couldn't read data")

    async def entrance_warp(self, ctx, going_to):
        write_list = []
        res = going_to

        # Warp to start
        if self.warp_to_start_flag:
            self.warp_to_start_flag = False
            home = 0xB03
            if home != self.last_scene:
                write_list += [(RAM_ADDRS["stage"][0], split_bits(11, 4), "Main RAM"),
                               (RAM_ADDRS["room"][0], split_bits(3, 1), "Main RAM"),
                               (RAM_ADDRS["floor"][0], split_bits(0, 4), "Main RAM"),
                               (RAM_ADDRS["entrance"][0], split_bits(5, 1), "Main RAM"), ]
                res = home
                self.current_stage = 0xB
                logger.info("Warping to Start")
            else:
                logger.info("Warp to start failed, warping from home scene")

        if write_list:
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
        return res

    # Processes events defined in data\dynamic_flags.py
    async def set_dynamic_flags(self, ctx, scene):
        # Check item conditions
        def check_items(d):
            if "has_items" in d:
                counter = [0] * len(d["has_items"])
                for has_item in ctx.items_received:
                    for i, want_item in enumerate(d["has_items"]):
                        if has_item.item == ITEMS_DATA[want_item[0]]["id"]:
                            counter[i] += 1
                for item, count_have in zip(d["has_items"], counter):
                    item, count_want, *operation = item
                    if not operation:
                        if (count_want == 0 and count_have != 0) or (count_want > 0 and count_have < count_want):
                            return False
                    elif operation[0] == "has_exact":
                        if count_want != count_have:
                            return False
                    elif operation[0] == "not_has":
                        if count_have >= count_want:
                            return False
            return True

        # Check location conditions
        def check_locations(d):
            for loc in d.get("has_locations", []):
                if self.location_name_to_id[loc] not in ctx.checked_locations:
                    return False
            for loc in d.get("not_has_locations", []):
                if self.location_name_to_id[loc] in ctx.checked_locations:
                    return False
            if "any_not_has_locations" in d:
                for loc in d.get("any_not_has_locations", []):
                    if self.location_name_to_id[loc] not in ctx.checked_locations:
                        return True
                return False
            return True

        def check_slot_data(d):
            if "has_slot_data" in d:
                for slot, value in d["has_slot_data"]:
                    if ctx.slot_data.get(slot, None) != value:
                        return False
            return True

        # Came from particular location
        def check_last_room(d):
            for i in d.get("not_last_scenes", []):
                if self.last_scene == i:
                    return False
            for i in d.get("last_scenes", []):
                if self.last_scene != i:
                    return False
            return True

        # Read a dict of addresses to see if they match value
        async def check_bits(d):
            if "check_bits" in d:
                r_list = {addr: (addr, 1, "Main RAM") for addr, _ in d["check_bits"].items()}
                values = await read_memory_values(ctx, r_list)
                for addr, p in values.items():
                    if not (p & d["check_bits"][addr]):
                        return False
            return True

        # Special case of metals
        def check_metals(d):
            if "zauz_metals" in d or "goal_requirement" in d:
                metals_ids = [ITEMS_DATA[metal]["id"] for metal in ITEM_GROUPS["Metals"]]
                current_metals = sum([1 for i in ctx.items_received if i.item in metals_ids])
                print(f"Metal check: {current_metals} metals out of {ctx.slot_data['zauz_required_metals']}")

                # Zauz Check
                if "zauz_metals" in d:
                    if current_metals < ctx.slot_data["zauz_required_metals"]:
                        if d["zauz_metals"]:
                            return False
                    else:
                        if not d["zauz_metals"]:
                            return False

                # Goal Check
                if "goal_requirement" in d:
                    return current_metals >= ctx.slot_data["required_metals"]
            return True

        def check_beedle_points(d):
            if not d.get("beedle_points", False):
                return True
            reference = {"Beedle Points (10)": 10,
                         "Beedle Points (20)": 20,
                         "Beedle Points (50)": 50}
            # Count points
            reference = {ITEMS_DATA[k]["id"]: c for k, c in reference.items()}
            points = 0
            for i in ctx.items_received:
                if i.item in reference:
                    points += reference[i.item]
            print(f"Beedle points {d.get('beedle_points')} >= {points}")
            return points >= d.get('beedle_points', 300)

        # Loop dynamic flags in scene
        if scene in self.scene_to_dynamic_flag:
            read_addr = set()
            set_bits, unset_bits = {}, {}
            print(f"Flags on Scene: {[i['name'] for i in self.scene_to_dynamic_flag[scene]]}")
            for data in self.scene_to_dynamic_flag[scene]:

                # Items, locations, slot data
                if not check_items(data):
                    print(f"{data['name']} does not have item reqs")
                    continue
                if not check_locations(data):
                    print(f"{data['name']} does not have location reqs")
                    continue
                if not check_slot_data(data):
                    print(f"{data['name']} does not have slot data reqs")
                    continue
                if not check_last_room(data):
                    print(f"{data['name']} came from wrong room {hex(self.last_scene)}")
                    continue
                if not await check_bits(data):
                    print(f"{data['name']} is missing bits")
                    continue
                if not check_metals(data):
                    print(f"{data['name']} does not have enough metals")
                    continue
                if not check_beedle_points(data):
                    continue

                # Create read/write lists
                for a, v in data.get("set_if_true", []):
                    read_addr.add(a)
                    # You can add an item name as a value, and it will set the value to it's count
                    if type(v) is str:
                        print(f"value is item {v}")
                        v = item_count(ctx, v)
                        print(f"value is count {v}")
                    set_bits[a] = set_bits.get(a, 0) | v
                    print(f"setting bit for {data['name']}")
                for a, v in data.get("unset_if_true", []):
                    read_addr.add(a)
                    unset_bits[a] = unset_bits.get(a, 0) | v
                    print(f"unsetting bit for {data['name']}")

                if "full_heal" in data:
                    await self.full_heal(ctx)

            # Read all values for all dynamic flags in scene
            read_list = {a: (a, 1, "Main RAM") for a in read_addr}
            prev = await read_memory_values(ctx, read_list)
            # print(f"{[[hex(int(a)), hex(v)] for a, v in prev.items()]}")

            # Calculate values to write
            for a, v in set_bits.items():
                prev[a] = prev[a] | v
            for a, v in unset_bits.items():
                prev[a] = prev[a] & (~v)

            # Write
            write_list = [(int(a), [v], "Main RAM") for a, v in prev.items()]
            print(f"Dynaflags writes: {prev}")
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
            return write_list

    # Called when a stage has fully loaded
    async def enter_stage(self, ctx, stage, scene_id):
        self.stage_address = await get_address_from_heap(ctx)
        self.key_address = self.stage_address + SMALL_KEY_OFFSET
        if stage in STAGE_FLAGS:
            flags = STAGE_FLAGS[stage]

            # Change certain stage flags based on options
            if stage == 0 and ctx.slot_data["skip_ocean_fights"] == 1:
                flags = SKIP_OCEAN_FIGHTS_FLAGS

            print(f"Setting Stage flags for {STAGES[stage]}, "
                  f"adr: {hex(self.stage_address + STAGE_FLAGS_OFFSET)}")
            await write_memory_values(ctx, self.stage_address + STAGE_FLAGS_OFFSET, flags)
        # Give dungeon keys
        if stage in DUNGEON_KEY_DATA:
            # Change key read location if using TotOK midway
            if self.entering_from == 0x2600 and scene_id == 0x2509:
                await self.update_key_count(ctx, 372)
            elif stage != 0x25 or self.entering_from == 0x2600:  # Prevent regiving keys in TotoK
                await self.update_key_count(ctx, self.entering_dungeon)
        self.entering_from = scene_id

        # Salvage Arm Auto-Repairs in certain rooms, delay until fully loaded for coming from sea
        # if scene_id in [0x130A, 0x500]:
        #    await self.repair_salvage_arm(ctx, scene_id)

        if not self.removed_boomerang:
            await self.boomerwatch(ctx)

    @staticmethod
    async def repair_salvage_arm(ctx, scene=0x500):
        read_list = {"salvage_health": (0x1BA390, 1, "Main RAM"),
                     "rupees": (0x1BA53E, 2, "Main RAM"),
                     "repair_kits": (0x1BA661, 1, "Main RAM"), }
        prev = await read_memory_values(ctx, read_list)
        if prev["salvage_health"] <= 2:
            write_list = []
            text = f"Repaired Salvage Arm for "
            if prev["repair_kits"] > 0:
                write_list.append((0x1BA661, [prev["repair_kits"] - 1], "Main RAM"))
                text += f"1 Salvage Repair Kit. You have {prev['repair_kits']} remaining."
            else:
                # Repair cost, doesn't care if you're out of rupees out of qol
                cost = 100 if prev["salvage_health"] == 0 else (6 - prev["salvage_health"]) * 10
                rupees = 0 if prev["rupees"] - cost <= 0 else prev["rupees"] - cost
                write_list.append((0x1BA53E, split_bits(rupees, 2), "Main RAM"))
                text += f"{cost} rupees."
                print(rupees)
            write_list.append((0x1BA390, [5], "Main RAM"))

            print(write_list)
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
        else:
            text = f"This room automatically repairs your Salvage Arm, for a cost, when at 2 health or below."
        # Send a client message about the repair
        logger.info(text)

    @staticmethod
    async def instant_repair_salvage_arm(ctx):
        salvage_kits = await read_memory_value(ctx, 0x1BA661)
        if salvage_kits > 0:
            write_list = [(0x1BA661, [salvage_kits - 1], "Main RAM"),
                          (RAM_ADDRS["salvage_health"][0], [5], "Main RAM"),
                          (0x1BA390, [5], "Main RAM")]  # Global salvage health
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
            logger.info(f"Salvage Arm instant-repaired. You have {salvage_kits - 1} Salvage Repair Kits remaining.")

    async def load_local_locations(self, ctx, scene):
        # Load locations in room into loop
        self.locations_in_scene = self.location_area_to_watches.get(scene, {})
        print(f"Locations in scene {scene}: {self.locations_in_scene.keys()}")
        self.watches = {}
        sram_read_list = {}
        locations_found = ctx.checked_locations
        if self.locations_in_scene is not None:
            # Create memory watches for checks triggerd by flags, and make list for checking sram
            for loc_name, location in self.locations_in_scene.items():
                loc_id = self.location_name_to_id[loc_name]
                if loc_id in locations_found:
                    if "address" in location:
                        read = await read_memory_value(ctx, location["address"])
                        if read & location["value"]:
                            print(f"Location {loc_name} has already been found and triggered")
                            continue
                else:
                    if "sram_addr" in location and location["sram_addr"] is not None:
                        sram_read_list[loc_name] = (location["sram_addr"], 1, "SRAM")
                        print(f"Created sram read for loacation {loc_name}")

                if "address" in location:
                    self.watches[loc_name] = (location["address"], 1, "Main RAM")

            # Read and set locations missed when bizhawk was disconnected
            if self.save_slot == 0 and len(sram_read_list) > 0:
                sram_reads = await read_memory_values(ctx, sram_read_list)
                for loc_name, value in sram_reads.items():
                    if value & LOCATIONS_DATA[loc_name]["sram_value"]:
                        await self.process_checked_locations(ctx, loc_name)

    # Updates key count based on a tracker counter in memory. Called when entering a dungeon
    async def update_key_count(self, ctx, current_stage: int) -> None:
        key_address = self.key_address = await get_small_key_address(ctx)
        key_data = DUNGEON_KEY_DATA[current_stage]
        print(f"current stage setting keys {current_stage}")
        read_list = {"dungeon": (key_address, 1, "Main RAM"),
                     "tracker": (key_data["address"], 1, "Main RAM")}
        key_values = await read_memory_values(ctx, read_list)
        print(f"Base key value: {key_values['tracker']}, filtered: {(key_values['tracker'] & key_data['filter'])}, "
              f"divider: {key_data['value']}")
        new_keys = (((key_values["tracker"] & key_data["filter"]) // key_data["value"])
                    + key_values["dungeon"])

        # Create write list, reset key tracker
        if new_keys != 0:
            new_keys = 7 if new_keys >= 7 else new_keys
            if current_stage == 37:
                if self.location_name_to_id["TotOK 1F SW Sea Chart Chest"] in ctx.checked_locations:
                    new_keys -= 1  # Opening the SW sea chart door uses a key permanently! No savescums!
            write_list = [(key_address, [new_keys], "Main RAM")]
            if key_data["name"] != "Temple of the Ocean King":
                reset_tracker = (~key_data["filter"]) & key_values["tracker"]
                write_list.append((key_data["address"], [reset_tracker], "Main RAM"))

            print(f"Finally writing keys to memory {hex(key_address)} with value {hex(new_keys)}")
            await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def write_totok_midway_keys(self, ctx):
        data = DUNGEON_KEY_DATA[372]
        keys = await read_memory_value(ctx, self.key_address)
        keys = keys * data["value"]
        keys = data["filter"] if keys > data["filter"] else keys
        await write_memory_value(ctx, 0x1BA64F, keys)

    # Called when checking location!
    async def process_checked_locations(self, ctx: "BizHawkClientContext", pre_process: str = None, r=False,
                                        detection_type=None):
        local_checked_locations = set()
        all_checked_locations = ctx.checked_locations
        location = None

        # If sent with a pre-proces kwarg
        if pre_process is not None:
            self.receiving_location = True
            loc_id = self.location_name_to_id[pre_process]
            location = LOCATIONS_DATA[pre_process]
            if r or (loc_id not in all_checked_locations):
                await self.set_vanilla_item(ctx, location, loc_id)
                local_checked_locations.add(loc_id)
            print(f"pre-processed {pre_process}, vanill {self.last_vanilla_item}")
        else:
            # Get link's coords
            link_coords = await self.get_coords(ctx)
            print(link_coords)

            # Certain checks use their detection method to differentiate them, like frogs and salvage
            locations_in_scene = self.locations_in_scene.copy()

            print(locations_in_scene)
            # Figure out what check was just gotten
            for i, loc in enumerate(locations_in_scene.items()):
                loc_name, location = loc
                loc_bytes = self.location_name_to_id[loc_name]

                if "address" in location:
                    continue

                print(f"Processing locs {loc_name}")
                print(
                    f"{location.get('x_max', 0x8FFFFFFF)} > {link_coords['x']} > {location.get('x_min', -0x8FFFFFFF)}")
                print(
                    f"{location.get('z_max', 0x8FFFFFFF)} > {link_coords['z']} > {location.get('z_min', -0x8FFFFFFF)}")

                if (location.get("x_max", 0x8FFFFFFF) > link_coords["x"] > location.get("x_min", -0x8FFFFFFF) and
                        location.get("z_max", 0x8FFFFFFF) > link_coords["z"] > location.get("z_min", -0x8FFFFFFF) and
                        location.get("y", link_coords["y"]) == link_coords["y"]):
                    # For rooms with checks that move or are close, check what you got first
                    if "delay_pickup" in location:
                        if len(self.locations_in_scene) > i + 1:
                            await self.set_delay_pickup(ctx, loc_name, location)
                            break
                    local_checked_locations.add(loc_bytes)
                    await self.set_vanilla_item(ctx, location, loc_bytes)
                    print(f"Got location {loc_name}! with vanilla {self.last_vanilla_item} id {loc_bytes}")
                    break
                location = None

        if location is not None and "set_bit" in location:
            for addr, bit in location["set_bit"]:
                print(f"Setting bit {bit} for location vanil {location['vanilla_item']}")
                await write_memory_value(ctx, addr, bit)

        # Delay reset of vanilla item from certain address reads
        if location is not None and "delay_reset" in location:
            self.delay_reset = True
            print(f"Started Delay Reset for {self.last_vanilla_item}")

        # Send locations
        # print(f"Local locations: {local_checked_locations} in \n{all_checked_locations}")
        if any([i not in all_checked_locations for i in local_checked_locations]):
            print(f"Sending Locations: {local_checked_locations}")
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(local_checked_locations)
            }])

    # Set checks to look for inventory changes
    async def set_delay_pickup(self, ctx, loc_name, location):
        delay_locations = []
        delay_pickup = location["delay_pickup"]
        if type(delay_pickup) is str:
            delay_locations.append(delay_pickup)
        elif type(delay_pickup) is list:
            delay_locations += delay_pickup

        self.delay_pickup = [loc_name, []]
        for loc in delay_locations:
            delay_item_check = LOCATIONS_DATA[loc].get("vanilla_item", None)
            if "Small Key" in delay_item_check:
                self.last_key_count = await read_memory_value(ctx, self.key_address)
                last_item_read = self.last_key_count
            else:
                last_item = ITEMS_DATA[delay_item_check]
                last_item_read = await read_memory_value(ctx, last_item["address"], last_item.get("size", 1))
            self.delay_pickup[1].append([loc, delay_item_check, last_item_read])
        print(f"Delay pickup {self.delay_pickup}")

    # Called during location processing to determine what vanilla item to remove
    async def set_vanilla_item(self, ctx, location, loc_id):
        item = location.get("vanilla_item", None)
        item_data = ITEMS_DATA[item]
        print(f"Setting vanilla for {item_data}")
        if item is not None and not item_data.get("dummy", False):
            if ("incremental" in item_data or "progressive" in item_data or
                    item_data["id"] not in [i.item for i in ctx.items_received]):
                self.last_vanilla_item.append(item)

                # Don't remove heart containers if already at max
                if item == "Heart Container" and item_count(ctx, item) >= 13:
                    self.last_vanilla_item.pop()

                # Farmable locations don't remove vanilla
                if "farmable" in location and loc_id in ctx.checked_locations:
                    if item == "Ship Part":
                        await self.give_random_treasure(ctx)
                    else:
                        self.last_vanilla_item.pop()

    async def process_scouted_locations(self, ctx: "BizHawkClientContext", scene):
        def check_items(d):
            for item in d.get("has_items", []):
                if ITEMS_DATA[item]["id"] not in [i.item for i in ctx.items_received]:
                    return False
            return True

        def check_slot_data(d):
            for args in d.get("slot_data", []):
                if type(args) is str:
                    option, value = args, [True]
                else:
                    option, value = args
                    value = [value] if type(value) is int else value
                if ctx.slot_data[option] not in value:
                    return False
            return True

        local_scouted_locations = set(ctx.locations_scouted)
        if self.hint_scene_to_watches.get(scene, []):
            print(f"hints {self.hint_scene_to_watches.get(scene, [])}")
        for hint_name in self.hint_scene_to_watches.get(scene, []):
            hint_data = HINT_DATA[hint_name]
            # Check requirements
            if not check_items(hint_data):
                continue
            if not check_slot_data(hint_data):
                continue

            # Figure out locations to hint
            if "locations" in hint_data:
                # Hint required dungeons
                if "Dungeon Hints" in hint_data["locations"]:
                    for loc in ctx.slot_data["required_dungeon_locations"]:
                        local_scouted_locations.add(self.location_name_to_id[loc])
                else:
                    locations_checked = ctx.locations_scouted
                    for loc in hint_data["locations"]:
                        loc_id = self.location_name_to_id[loc]
                        if loc_id in locations_checked:
                            continue
                        local_scouted_locations.add(loc_id)
            else:
                local_scouted_locations.add(self.location_name_to_id[hint_name])

        # Send hints
        if self.local_scouted_locations != local_scouted_locations:
            self.local_scouted_locations = local_scouted_locations
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.local_scouted_locations),
                "create_as_hint": int(2)
            }])

    async def scout_location(self, ctx: "BizHawkClientContext", locations):
        local_scouted_locations = set(ctx.locations_scouted)
        for loc in locations:
            local_scouted_locations.add(LOCATIONS_DATA[loc]["id"])

        if self.local_scouted_locations != local_scouted_locations:
            self.local_scouted_locations = local_scouted_locations
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.local_scouted_locations),
                "create_as_hint": int(2)
            }])

    async def process_received_items(self, ctx: "BizHawkClientContext", num_received_items: int) -> None:
        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        next_item = ctx.items_received[num_received_items].item
        item_name = self.item_id_to_name[next_item]
        item_data = ITEMS_DATA[item_name]
        item_value = 0

        # Increment in-game items received count
        received_item_address = RAM_ADDRS["received_item_index"]
        write_list = [(received_item_address[0], split_bits(num_received_items + 1, 2), received_item_address[2])]
        print(f"Vanilla item: {self.last_vanilla_item} for {item_name}")

        # If same as vanilla item don't remove
        if self.last_vanilla_item and item_name == self.last_vanilla_item[-1]:
            if self.last_vanilla_item:
                self.last_vanilla_item.pop()
            print(f"oops it's vanilla or dummy! {self.last_vanilla_item}")
            # If got totok key at vanilla location, add to memory anyway
            if item_name == "Small Key (Temple of the Ocean King)":
                data = DUNGEON_KEY_DATA[item_data["dungeon"]]
                prev_value = await read_memory_value(ctx, data["address"])
                new_value = prev_value + data["value"]
                write_list.append((data["address"], [new_value], "Main RAM"))

        # Handle Small Keys
        elif "Small Key" in item_name:
            data = DUNGEON_KEY_DATA[item_data["dungeon"]]
            prev_value = await read_memory_value(ctx, data["address"])

            # Get key in own dungeon
            if self.current_stage == item_data["dungeon"]:
                print("In dungeon! Getting Key")
                self.key_value = await read_memory_value(ctx, self.key_address)
                self.key_value = 7 if self.key_value > 7 else self.key_value
                write_list.append((self.key_address, [self.key_value + 1], "Main RAM"))
                # TotOK - adds to key increment if you get it in the dungeon, otherwise do as usual
                if "Temple of the Ocean King" in item_name:
                    bit_filter = data["filter"]
                    new_value = prev_value | bit_filter if (prev_value & bit_filter) + data[
                        "value"] > bit_filter else prev_value + data["value"]
                    print(f"Writing TotOK key to storage: {hex(prev_value)} -> {hex(new_value)}")
                    write_list.append((data["address"], [new_value], "Main RAM"))

            # Get key elsewhere
            elif (prev_value & data["filter"]) != data["filter"]:
                new_value = prev_value + data["value"]
                print(f"Writing keys to storage: {hex(prev_value)} -> {hex(new_value)}")
                write_list.append((data["address"], [new_value], "Main RAM"))
            else:
                print(f"Too many keys for dungeon {item_data['dungeon']}")

        # Handle ammo refills
        elif "refill" in item_data:
            refill_id = ITEMS_DATA[item_data["refill"]]["id"]
            prog_received = sum([1 for i in ctx.items_received[:num_received_items] if i.item == refill_id]) - 1
            if prog_received >= 0:
                write_list.append((item_data["address"], [item_data["give_ammo"][prog_received]], "Main RAM"))

        elif "address" in item_data or "progressive" in item_data:
            # Handle progressive items (not to be confused with progression items)
            prog_received = 0
            if "progressive" in item_data:
                prog_received = sum([1 for i in ctx.items_received[:num_received_items] if i.item == next_item])
                prog_received = len(item_data["progressive"]) - 1 if prog_received > len(
                    item_data["progressive"]) - 1 else prog_received
                item_address, item_value = item_data["progressive"][prog_received]
            else:
                item_address = item_data["address"]

            # Read address item is to be written to
            prev_value = await read_memory_value(ctx, item_address, domain="Main RAM",
                                                 size=item_data.get("size", 1))

            # Handle different writing operations
            if "incremental" in item_data:
                if type(item_data.get("value", 1)) is str:

                    # Sand of hours check
                    if "Sand" in item_data['value']:
                        if item_data.get("value") == "Sand":
                            if not ctx.slot_data["ph_required"] or item_count(ctx, "Phantom Hourglass"):
                                value = ctx.slot_data["ph_time_increment"] * 60
                            else:
                                value = 0
                        elif item_data.get("value") == "Sand PH":
                            value = ctx.slot_data["ph_starting_time"] * 60

                            # If ph is required, add all time so far on finding
                            if ctx.slot_data["ph_required"] and item_count(ctx, "Phantom Hourglass") < 2:
                                value += (ctx.slot_data["ph_time_increment"] * 60 * item_count(ctx, "Sand of Hours")
                                          + item_count(ctx, "Sand of Hours (Small)") * 3600
                                          + item_count(ctx, "Sand of Hours (Boss)") * 7200)
                        else:
                            value = item_data.get("value")
                        last_time = await read_memory_value(ctx, item_address, size=4)
                        if last_time + value > 359940:
                            value = 359940 - last_time
                    elif item_data.get("value") == "pack_size":
                        value = ctx.slot_data["spirit_gem_packs"]
                    else:
                        value = "Error!"
                else:
                    value = item_data.get("value", 1)

                    # Heal on heart container
                    if item_name == "Heart Container":
                        await self.full_heal(ctx)

                item_value = prev_value + value
                item_value = 0 if item_value <= 0 else item_value
                if "size" in item_data:
                    item_value = split_bits(item_value, item_data["size"])
                    # TODO if incremental goes above size it's a problem!
            elif "progressive" in item_data:
                if "progressive_overwrite" in item_data and prog_received >= 1:
                    item_value = item_value  # Bomb upgrades need to overwrite of everything breaks
                else:
                    item_value = prev_value | item_value
            else:
                item_value = prev_value | item_data["value"]

            item_values = item_value if type(item_value) is list else [item_value]
            item_values = [min(254, i) for i in item_values]
            write_list.append((item_address, item_values, "Main RAM"))

            # Handle special item conditions
            if "give_ammo" in item_data:
                write_list.append((item_data["ammo_address"], [item_data["give_ammo"][prog_received]], "Main RAM"))
            if "set_bit" in item_data:
                for adr, bit in item_data["set_bit"]:
                    bit_prev = await read_memory_value(ctx, adr)
                    write_list.append((adr, [bit | bit_prev], "Main RAM"))

        # Set ship
        elif "ship" in item_data:
            for addr in EQUIPPED_SHIP_PARTS_ADDR:
                write_list.append((addr, [item_data["ship"]], "Main RAM"))

        elif item_name == "Refill: Health":
            await self.full_heal(ctx)

        # Write the new item to memory!
        print(f"Write list: {write_list}")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

        # If treasure, update treasure tracker
        if "treasure" in item_data:
            await self.update_treasure_tracker(ctx)
        if "Potion" in item_name:
            await self.update_potion_tracker(ctx)
        # If hint on receive, send hint (currently only treasure maps)
        if "hint_on_receive" in item_data:
            if ctx.slot_data["randomize_salvage"] == 1:
                await self.scout_location(ctx, item_data["hint_on_receive"])
        # Increment metal count
        if item_name in ITEM_GROUPS["Metals"]:
            self.metal_count += 1
            await self.process_game_completion(ctx, 0)

    async def remove_vanilla_item(self, ctx, num_received_items):
        print(f"Removing vanilla items {self.last_vanilla_item}")
        # Handle items from random pools
        for item in self.last_vanilla_item:
            if "dummy" in ITEMS_DATA[item]:
                continue
            if item == "Treasure":
                treasure_write_list = split_bits(self.last_treasures, 8)
                print(f"Treasure Write List: {treasure_write_list}")
                await write_memory_values(ctx, 0x1BA5AC, treasure_write_list, overwrite=True)
            elif item == "Ship Part":
                ship_write_list = ([1] + [0] * 8) * 8
                await write_memory_values(ctx, 0x1BA564, ship_write_list, overwrite=True)
            elif "Potion" in item:
                print(f"Pots {self.last_potions}")
                if not all(self.last_potions):
                    await write_memory_values(ctx, 0x1BA5D8, self.last_potions, overwrite=True)
                else:
                    # If you already have 2 potions, it gives rupees instead
                    await write_memory_value(ctx, 0x1BA53E, ITEMS_DATA[item]["value"],
                                             incr=False, size=2)
            # Handle all other items
            else:
                data = ITEMS_DATA[item]
                value = data.get('value', 1)
                if "Small Key" in item:
                    address = self.key_address = await get_small_key_address(ctx)
                elif "progressive" in data:
                    write_list = []
                    index = sum([1 for i in ctx.items_received[:num_received_items] if i.item == data["id"]])
                    if index >= len(data["progressive"]):
                        continue
                    address, value = data["progressive"][index]
                    if "give_ammo" in data:
                        ammo_v = data["give_ammo"][max(index - 1, 0)]
                        write_list.append((data["ammo_address"], [ammo_v], "Main RAM"))
                    await bizhawk.write(ctx.bizhawk_ctx, write_list)
                else:
                    address, value = data["address"], data.get("value", 1)

                await write_memory_value(ctx, address, value,
                                         incr=data.get('incremental', None), unset=True, size=data.get("size", 1))
        self.last_vanilla_item = []

    async def process_game_completion(self, ctx: "BizHawkClientContext", current_scene: int):
        game_clear = False
        current_scene = current_scene * 0x100 if current_scene < 0x100 else current_scene
        if ctx.slot_data["bellum_access"] == 4:
            game_clear = self.metal_count >= ctx.slot_data["required_metals"]
        else:
            game_clear = (current_scene == self.goal_room)  # Enter End Credits

        if game_clear:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead, stage):
        if ctx.last_death_link > self.last_deathlink and not is_dead:
            # A death was received from another player, make our player die as well
            if stage == 0:
                await write_memory_value(ctx, RAM_ADDRS["boat_health"][0], 0, overwrite=True)
            elif stage == 3:
                await write_memory_value(ctx, RAM_ADDRS["salvage_health"][0], 0, overwrite=True)
            else:
                await write_memory_value(ctx, RAM_ADDRS["link_health"][0], 0, size=2, overwrite=True)

            self.is_expecting_received_death = True
            self.last_deathlink = ctx.last_death_link

        if not self.was_alive_last_frame and not is_dead:
            # We revived from any kind of death
            self.was_alive_last_frame = True
        elif self.was_alive_last_frame and is_dead:
            # Our player just died...
            self.was_alive_last_frame = False
            if self.is_expecting_received_death:
                # ...because of a received deathlink, so let's not make a circular chain of deaths please
                self.is_expecting_received_death = False
            else:
                # ...because of their own incompetence, so let's make their mates pay for that
                await ctx.send_death(ctx.player_names[ctx.slot] + " may have disappointed the Ocean King.")
                self.last_deathlink = ctx.last_death_link
