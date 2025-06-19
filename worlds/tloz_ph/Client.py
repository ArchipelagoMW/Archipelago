import time
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

ROM_ADDRS = {
    "game_identifier": (0x00000000, 16, "ROM"),
    "slot_name": (0xFFFC0, 64, "ROM"),
}

RAM_ADDRS = {
    "game_state": (0x075E0D, 1, "Main RAM"),  # TODO find death variables
    "is_dead": (0xC2EE, 1, "ARM7 System Bus"),

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

    "link_x": (0x1B6FEC, 4, "Main RAM"),
    "link_y": (0x1B6FF0, 4, "Main RAM"),
    "link_z": (0x1B6FF4, 4, "Main RAM"),
    "using_item:": (0x1BA71C, 1, "Main RAM"),
    "boat_x": (0x1B8518, 4, "Main RAM"),
    "boat_z": (0x1B8520, 4, "Main RAM"),
    "save_slot": (0x1B8124, 1, "Main RAM"),
    "equipped_item": (0x1BA520, 4, "Main RAM"),
    "got_item_menu": (0x19A5B0, 1, "Main RAM")
}

POINTERS = {
    "ADDR_gItemManager": 0x0fb4,
    "ADDR_gPlayerManager": 0x0fbc,
    "ADDR_gAdventureFlags": 0x0f74,
    "ADDR_gPlayer": 0x0fec,
    "ADDR_gOverlayManager_mLoadedOverlays_4": 0x0910,
    "ADDR_gMapManager": 0x0e60
}

# gMapManager -> mCourse -> mSmallKeys
SMALL_KEY_OFFSET = 0x260
STAGE_FLAGS_OFFSET = 0x268

# Addresses to read each cycle
read_keys_always = ["game_state", "received_item_index", "is_dead", "stage", "room", "slot_id"]
read_keys_land = ["getting_item", "getting_ship_part"]
read_keys_sea = ["shot_frog"]


# Split up large values to write into smaller chunks
def split_bits(value, size):
    ret = []
    f = 0xFFFFFF00
    for _ in range(size):
        ret.append(value & 0xFF)
        value = (value & f) >> 8
    return ret


# Read list of address data
async def read_memory_values(ctx, read_list: dict[str, tuple[int, int, str]], signed=False) -> dict[str, int]:
    keys = read_list.keys()
    read_data = [(a, s, d) for a, s, d in read_list.values()]
    read_result = await bizhawk.read(ctx.bizhawk_ctx, read_data)
    values = [int.from_bytes(i, "little", signed=signed) for i in read_result]
    return {key: value for key, value in zip(keys, values)}


# Read single address
async def read_memory_value(ctx, address: int, size=1, domain="Main RAM", signed=False) -> int:
    read_result = await bizhawk.read(ctx.bizhawk_ctx, [(address, size, domain)])
    print("Reading memory value", hex(address), size, domain, ", got value",
          hex(int.from_bytes(read_result[0], "little")))
    return int.from_bytes(read_result[0], "little", signed=signed)


# Write single address
async def write_memory_value(ctx, address: int, value: int, domain="Main RAM", incr=None, size=1, unset=False):
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
            print(f"Unseting bit with filter {hex(~value)}")
            write_value = prev & (~value)
        else:
            write_value = prev | value
    if size > 1:
        write_value = split_bits(write_value, size)
    else:
        write_value = [write_value]
    print(f"Writing Memory: {hex(address)}, {write_value}, {size}, {domain}, {incr}, {unset}")
    await bizhawk.write(ctx.bizhawk_ctx, [(address, write_value, domain)])
    return write_value


# Write list of values starting from address
async def write_memory_values(ctx, address: int, values: list, domain="Main RAM"):
    prev = await read_memory_value(ctx, address, len(values), domain)
    new_values = [old | new for old, new in zip(split_bits(prev, 4), values)]
    print(f"values: {new_values}, old: {split_bits(prev, 4)}")
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
        self.last_vanilla_item = None

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

        self.delay_pickup = None
        self.last_key_count = 0
        self.key_address = 0
        self.key_value = 0
        self.goal_room = 0x3600

        self.get_main_read_list(self.current_stage)

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
        ctx.watcher_timeout = 0.5

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

        # Set starting time for PH
        ph_time = ctx.slot_data["ph_starting_time"] * 3600
        ph_time_bits = split_bits(ph_time, 4)
        write_list.append((0x1BA528, ph_time_bits, "Main RAM"))

        # Set Frog flags if not randomizing frogs
        if ctx.slot_data["randomize_frogs"] == 1:
            write_list += [(a, [v], "Main RAM") for a, v in STARTING_FROG_FLAGS]
        await bizhawk.write(ctx.bizhawk_ctx, write_list)
        self.removed_boomerang = False

    # Boomerang is set to enable item menu, called on s+q to remove it again.
    async def boomerwatch(self, ctx) -> bool:
        print(f"got item menu {await read_memory_value(ctx, *RAM_ADDRS["got_item_menu"])}")
        if await read_memory_value(ctx, *RAM_ADDRS["got_item_menu"]) > 0:
            print("Reconnected, boomerwatching")
            # Check if boomerang has been received
            for item in ctx.items_received:
                if item.item == ITEMS_DATA["Boomerang"]["id"]:
                    return True
            # Otherwise remove boomerang
            boomerang = ITEMS_DATA["Boomerang"]
            await write_memory_value(ctx, boomerang["address"], boomerang["value"], unset=True)

            test = await read_memory_value(ctx, boomerang["address"], 1, "Main RAM")
            print("Boomerwatch ""Successful!"f", value is {test}")
            return True
        else:
            return False

    def get_coord_address(self, at_sea=None) -> dict[str, tuple[int, int, str]]:
        at_sea = self.at_sea if at_sea is None else at_sea
        if at_sea:
            return {k: v for k, v in RAM_ADDRS.items() if k in ["boat_x", "boat_z"]}
        else:
            return {k: v for k, v in RAM_ADDRS.items() if k in ["link_x", "link_y", "link_z"]}

    async def get_coords(self, ctx):
        coords = await read_memory_values(ctx, self.get_coord_address(), signed=True)
        return {
            "x": coords.get("link_x", coords.get("boat_x", 0)),
            "y": coords.get("link_y", 0),
            "z": coords.get("link_z", coords.get("boat_z", 0))
        }

    def get_main_read_list(self, stage):
        read_keys = read_keys_always
        if stage is not None:
            if stage == 0:
                read_keys += read_keys_sea
                self.at_sea = True
            else:
                read_keys += read_keys_land
                self.at_sea = False
        self.main_read_list = {k: v for k, v in RAM_ADDRS.items() if k in read_keys}

    def get_ending_room(self, ctx):
        if ctx.slot_data["goal"] == "beat_bellumbeck":
            self.goal_room = 0x3600
        elif ctx.slot_data["goal"] == "triforce_door":
            self.goal_room = 0x2509

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot is None:
            self.just_entered_game = True
            self.last_scene = None
            self.get_main_read_list(self.current_stage)
            return

        # Enable "DeathLink" tag if option was enabled
        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)

        try:
            read_result = await read_memory_values(ctx, self.main_read_list)

            in_game = read_result["game_state"]
            slot_memory = read_result["slot_id"]
            current_stage = read_result["stage"]
            self.current_stage = current_stage

            # If player is not in-game, don't do anything else
            if not in_game or current_stage not in STAGES:
                print(f"NOT IN GAME, {in_game}, {slot_memory}")
                self.previous_game_state = False

                current_stage = await read_memory_value(ctx, *RAM_ADDRS["stage"])
                if not ctx.finished_game:
                    await self.process_game_completion(ctx, current_stage)
                return

            # On entering game from main menu / cutscene / shop / stage transition
            if in_game and not self.previous_game_state:
                self.just_entered_game = True
                self.last_stage = None
                self.last_scene = None
                self.removed_boomerang = False  # Catches stray item menu errors, only 1 read
                self.save_slot = await read_memory_value(ctx, RAM_ADDRS["save_slot"][0])
                self.get_ending_room(ctx)
                print(f"Started Game")

                # If new file, set up starting flags
                if slot_memory == 0:
                    await self.set_starting_flags(ctx)
                    print(f"Set starting flags for slot {slot_memory}")

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
            is_dead = read_result["is_dead"]  # TODO find actual deathlink address

            # Process on new room
            if current_scene != self.last_scene:
                print(f"Entered new scene {hex(current_scene)}")
                self.last_scene = current_scene
                self.entering_dungeon = None
                await self.load_local_locations(ctx, current_scene)

                # Start watch for stage fully loading
                if current_stage != self.last_stage:
                    self.new_stage_loading = await read_memory_values(ctx, self.get_coord_address(False))
                    self.get_main_read_list(None)  # Sometimes stage loading causes false item reads

                # Set dynamic flags on scene
                await self.set_dynamic_flags(ctx, current_scene)

                # Check if entering dungeon
                if current_stage in DUNGEON_KEY_DATA and self.last_stage != current_stage:
                    self.entering_dungeon = current_stage
                else:
                    self.entering_from = current_scene  # stage and room

                # Hard coded room stuff

                # Yellow warp in TotOK saves keys
                if self.entering_from is not None:
                    if current_scene == 0x2509 and self.entering_from == 0x2507:  # TODO: set constants for these rooms
                        await self.write_totok_midway_keys(ctx)

                self.last_stage = current_stage
                await self.process_scouted_locations(ctx, current_scene)

            # Set stage flags when scene fully loaded
            if self.new_stage_loading is not None:
                await self.enter_stage(ctx, current_stage, current_scene)

            # Read for checks on specific global flags
            if len(self.watches) > 0:
                watch_result = await read_memory_values(ctx, self.watches)
                for loc_name, prev_value in watch_result.items():
                    loc_data = LOCATIONS_DATA[loc_name]
                    if prev_value & loc_data["value"]:
                        print(f"Got read item {loc_name} from address {loc_data['address']} "
                              f"looking at bit {loc_data['value']}")
                        await self.process_checked_locations(ctx, loc_name)
                        self.watches.pop(loc_name)

            # Check if link is getting location
            if getting_location and not self.receiving_location and self.locations_in_scene is not None:
                self.receiving_location = True
                print("Receiving Item")
                await self.process_checked_locations(ctx, None)

            # Process received items
            if num_received_items < len(ctx.items_received):
                await self.process_received_items(ctx, num_received_items)

            # Exit location received cs
            if self.receiving_location and not getting_location:
                print("Item Received Successfully")
                self.receiving_location = False

                # Check for delayed pickup first!
                if self.delay_pickup is not None:
                    print(f"Delayed pickup: old {self.last_key_count} new {self.key_value} loc {self.delay_pickup[0]}")
                    self.key_value = await read_memory_value(ctx, self.key_address)
                    if self.key_value > self.last_key_count:
                        await self.process_checked_locations(ctx, self.delay_pickup[1], True)
                    else:
                        await self.process_checked_locations(ctx, self.delay_pickup[0])
                    self.delay_pickup = None
                    self.last_key_count = 0

                # Remove vanilla item
                elif self.last_vanilla_item is not None and "dummy" not in ITEMS_DATA[self.last_vanilla_item]:
                    await self.remove_vanilla_item(ctx, num_received_items)

            # Finished game?
            if not ctx.finished_game:
                await self.process_game_completion(ctx, current_scene)

            # Process Deathlink
            if "DeathLink" in ctx.tags:
                await self.process_deathlink(ctx, is_dead)

            self.previous_game_state = in_game
            self.just_entered_game = False

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            print("Couldn't read data")

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
                    item, count_want = item
                    if (count_want == 0 and count_have != 0) or (count_want > 0 and count_have < count_want):
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
            return True

        def check_slot_data(d):
            if "has_slot_data" in d:
                for slot, value in d["has_slot_data"]:
                    if ctx.slot_data.get(slot, None) != value:
                        return False
            return True

        # Loop dynamic flags in scene
        if scene in self.scene_to_dynamic_flag:
            read_addr = set()
            set_bits, unset_bits = {}, {}
            print(f"Flags on Scene: {[i["name"] for i in self.scene_to_dynamic_flag[scene]]}")
            for data in self.scene_to_dynamic_flag[scene]:
                # Special case for having goal requirements
                if "goal_requirement" in data:
                    if data["goal_requirement"]:
                        data["has_items"] = data.get("has_items", []) + [(i, 1) for i in ctx.slot_data["boss_rewards"]]
                    else:
                        data["has_items"] = data.get("has_items", []) + [(i, 0) for i in ctx.slot_data["boss_rewards"]]
                if not check_items(data):
                    print(f"{data["name"]} does not have item reqs")
                    continue
                if not check_locations(data):
                    print(f"{data["name"]} does not have location reqs")
                    continue
                if not check_slot_data(data):
                    print(f"{data["name"]} does not have slot data reqs")
                    continue


                # Create read/write lists
                for a, v in data.get("set_if_true", []):
                    read_addr.add(a)
                    set_bits[a] = set_bits.get(a, 0) | v
                    print(f"setting bit for {data["name"]}")
                for a, v in data.get("unset_if_true", []):
                    read_addr.add(a)
                    unset_bits[a] = unset_bits.get(a, 0) | v
                    print(f"unsetting bit for {data["name"]}")

            # Read all values for all dynamic flags in scene
            read_list = {a: (a, 1, "Main RAM") for a in read_addr}
            prev = await read_memory_values(ctx, read_list)
            print(f"{[[hex(int(a)), hex(v)] for a, v in prev.items()]}")

            # Calculate values to write
            for a, v in set_bits.items():
                prev[a] = prev[a] | v
            for a, v in unset_bits.items():
                prev[a] = prev[a] & (~v)

            # Write
            write_list = [(int(a), [v], "Main RAM") for a, v in prev.items()]
            print(f"Dynaflags writes: {prev}")
            await bizhawk.write(ctx.bizhawk_ctx, write_list)

    # Called when a stage has fully loaded
    async def enter_stage(self, ctx, stage, scene_id):
        # Delay until fully loaded
        if self.new_stage_loading != await read_memory_values(ctx, self.get_coord_address(False)):
            self.stage_address = await get_address_from_heap(ctx)
            self.key_address = self.stage_address + SMALL_KEY_OFFSET
            if stage in STAGE_FLAGS:
                print(
                    f"Setting Stage flags for {STAGES[stage]}, adr: {hex(self.stage_address + STAGE_FLAGS_OFFSET)}")
                await write_memory_values(ctx, self.stage_address + STAGE_FLAGS_OFFSET,
                                          STAGE_FLAGS[stage])
            # Give dungeon keys
            if stage in DUNGEON_KEY_DATA:
                # Change key read location if using TotOK midway
                if self.entering_from == 0x2600 and scene_id == 0x2509:
                    self.entering_dungeon = 372
                elif stage != 0x25 or self.entering_from == 0x2600:  # Prevent regiving keys in TotoK
                    await self.update_key_count(ctx, self.entering_dungeon)
            self.new_stage_loading = None
            self.get_main_read_list(stage)

            if not self.removed_boomerang:
                await self.boomerwatch(ctx)

    async def load_local_locations(self, ctx, scene):
        # Load locations in room into loop
        self.locations_in_scene = self.location_area_to_watches.get(scene, {})
        print(f"Locations in scene {scene}: {self.locations_in_scene.keys()}")
        self.watches = {}
        sram_read_list = {}
        if self.locations_in_scene is not None:
            # Create memory watches for checks triggerd by flags, and make list for checking sram
            for loc_name, location in self.locations_in_scene.items():
                if "address" in location:
                    self.watches[loc_name] = (location["address"], 1, "Main RAM")
                if "sram_addr" in location and location["sram_addr"] is not None:
                    sram_read_list[loc_name] = (location["sram_addr"], 1, "SRAM")

            # Read and set locations missed when bizhawk was disconnected
            if self.save_slot == 0 and len(sram_read_list) > 0:
                sram_reads = await read_memory_values(ctx, sram_read_list)
                # TODO: Figure out is offset effects sram too
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
        print(f"Base key value: {key_values["tracker"]}, filtered: {(key_values["tracker"] & key_data["filter"])}, "
              f"divider: {key_data["value"]}")
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
    async def process_checked_locations(self, ctx: "BizHawkClientContext", pre_process: str = None, r=False):
        local_checked_locations = set(ctx.checked_locations)
        location = None

        # If sent with a pre-proces kwarg
        if pre_process is not None:
            loc_id = self.location_name_to_id[pre_process]
            location = LOCATIONS_DATA[pre_process]
            vanilla_item = location.get("vanilla_item")
            if r or (loc_id not in self.local_checked_locations and vanilla_item != pre_process):
                self.last_vanilla_item = vanilla_item
                self.receiving_location = True
                local_checked_locations.add(loc_id)
            print(f"pre-processed {pre_process}, vanill {self.last_vanilla_item}")
        else:
            # Get link's coords

            link_coords = await self.get_coords(ctx)
            print(link_coords)

            # Figure out what check was just gotten
            for i, loc in enumerate(self.locations_in_scene.items()):
                loc_name, location = loc
                loc_bytes = self.location_name_to_id[loc_name]

                if "address" in location:
                    continue

                print(f"Processing locs {loc_name}")
                print(
                    f"{location.get("x_max", 0x8FFFFFFF)} > {link_coords["x"]} > {location.get("x_min", -0x8FFFFFFF)}")
                print(
                    f"{location.get("z_max", 0x8FFFFFFF)} > {link_coords["z"]} > {location.get("z_min", -0x8FFFFFFF)}")

                if (location.get("x_max", 0x8FFFFFFF) > link_coords["x"] > location.get("x_min", -0x8FFFFFFF) and
                        location.get("z_max", 0x8FFFFFFF) > link_coords["z"] > location.get("z_min", -0x8FFFFFFF) and
                        location.get("y", link_coords["y"]) == link_coords["y"]):
                    # For rooms with keys that move, check if you got a key first
                    if "delay_pickup" in location:
                        if len(self.locations_in_scene) > i + 1:
                            self.last_key_count = await read_memory_value(ctx, self.key_address)
                            self.delay_pickup = [loc_name, location["delay_pickup"]]
                            break
                    local_checked_locations.add(loc_bytes)
                    vanilla_item = ITEMS_DATA[location["vanilla_item"]]
                    if vanilla_item["id"] not in [i.item for i in ctx.items_received] or "incremental" in vanilla_item:
                        self.last_vanilla_item = location.get("vanilla_item")
                    print(f"Got location {loc_name}! with vanilla {self.last_vanilla_item} id {loc_bytes}")
                    break
                location = None

        print(f"location: {location}")
        if location is not None and "set_bit" in location:
            for addr, bit in location["set_bit"]:
                print(f"Setting bit {bit} for location vanil {location['vanilla_item']}")
                await write_memory_value(ctx, addr, bit)

        # Send locations
        if self.local_checked_locations != local_checked_locations:
            self.local_checked_locations = local_checked_locations
            print(f"Sending Locations: {local_checked_locations}")
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(self.local_checked_locations)
            }])

    async def process_scouted_locations(self, ctx: "BizHawkClientContext", scene):
        local_scouted_locations = set(ctx.locations_scouted)
        if scene in SHOPS:
            # Items unique to that shop
            if "unique" in SHOPS[scene]:
                locations = SHOPS[scene]["unique"]
                [local_scouted_locations.add(self.location_name_to_id[loc]) for loc in locations]

            if "beedle" in SHOPS[scene]:
                read = await read_memory_value(ctx, 0x1BA644)
                if read & 0x10:  # TODO: Hard coding this is stupid
                    local_scouted_locations.add(self.location_name_to_id["Beedle Shop Bomb Bag"])

            # Items in all island shops
            if SHOPS[scene].get("island_shop", False):
                has_bow, has_chus = False, False
                for i in ctx.items_received:
                    item = self.item_id_to_name[i.item]
                    if item == "Bow (Progressive)":
                        has_bow = True
                    if item == "Bombchus (Progressive)":
                        has_chus = True

                local_scouted_locations.add(self.location_name_to_id["Island Shop Power Gem"])
                if has_bow:
                    local_scouted_locations.add(self.location_name_to_id["Island Shop Quiver"])
                    if has_chus:
                        local_scouted_locations.add(self.location_name_to_id["Island Shop Bombchu Bag"])
                        local_scouted_locations.add(self.location_name_to_id["Island Shop Heart Container"])

        # Send hints
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
        write_list = [(received_item_address[0], [num_received_items + 1], received_item_address[2])]
        print(f"Vanilla item: {self.last_vanilla_item}, item name: {item_name}")

        # If same as vanilla item don't remove
        if item_name == self.last_vanilla_item or "dummy" in item_data:
            self.last_vanilla_item = None
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
                write_list.append((self.key_address, [self.key_value + 1], "Main RAM"))
                # TotOK - adds to key increment if you get it in the dungeon, otherwise do as usual
                if "Temple of the Ocean King" in item_name:
                    new_value = prev_value + data["value"]
                    print(f"Writing TotOK key to storage: {hex(prev_value)} -> {hex(new_value)}")
                    write_list.append((data["address"], [new_value], "Main RAM"))

            # Get key elsewhere
            elif (prev_value & data["filter"]) != data["filter"]:
                new_value = prev_value + data["value"]
                print(f"Writing keys to storage: {hex(prev_value)} -> {hex(new_value)}")
                write_list.append((data["address"], [new_value], "Main RAM"))
            else:
                print(f"Too many keys for dungeon {item_data['dungeon']}")
        elif "address" in item_data or "progressive" in item_data:
            # Handle progressive items (not to be confused with progression items)
            prog_received = 0
            if "progressive" in item_data:
                prog_received = sum([1 for i in ctx.items_received[:num_received_items] if i.item == next_item])
                prog_received = len(item_data["progressive"])-1 if prog_received > len(
                    item_data["progressive"])-1 else prog_received
                item_address, item_value = item_data["progressive"][prog_received]
            else:
                item_address = item_data["address"]

            # Read address item is to be written to
            prev_value = await read_memory_value(ctx, item_address, domain="Main RAM",
                                                 size=item_data.get("size", 1))

            # Handle different writing operations
            if "incremental" in item_data:
                # Sand of hours check
                if item_data["value"] == "Sand":
                    value = ctx.slot_data["ph_time_increment"] * 3600
                else:
                    value = item_data["value"]

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

        # Write the new item to memory!

        print(f"Write list: {write_list}")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def remove_vanilla_item(self, ctx, num_received_items):
        print(f"Removing vanilla item {self.last_vanilla_item}")
        data = ITEMS_DATA[self.last_vanilla_item]
        value = data.get('value', 1)
        if "Small Key" in self.last_vanilla_item:
            address = self.key_address = await get_small_key_address(ctx)
        elif "progressive" in data:
            write_list = []
            index = sum([1 for i in ctx.items_received[:num_received_items] if i.item == data["id"]])
            if index >= len(data["progressive"]):
                return
            address, value = data["progressive"][index]
            if "give_ammo" in data:
                ammo_v = data["give_ammo"][max(index - 1, 0)]
                write_list.append((data["ammo_address"], [ammo_v], "Main RAM"))
            if index == 2:
                write_list.append((address, [1], "Main RAM"))
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
        else:
            address = data["address"]

        if value == "Sand":
            value = 3600

        await write_memory_value(ctx, address, value,
                                 incr=data.get('incremental', None), unset=True)
        self.last_vanilla_item = None

    async def process_game_completion(self, ctx: "BizHawkClientContext", current_scene: int):
        game_clear = False
        current_scene = current_scene * 0x100 if current_scene < 0x100 else current_scene
        game_clear = (current_scene == self.goal_room)  # Enter End Credits

        if game_clear:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead):
        pass
