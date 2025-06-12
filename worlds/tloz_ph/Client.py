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
    "show_item": (0x057399, 1, "Main RAM"),
    "in_dialogue": (0x1BA73A, 1, "Main RAM"),
    "getting_ship_part": (0x11F5E4, 1, "Main RAM"),
    "link_x": (0x1B6FEC, 4, "Main RAM"),
    "link_y": (0x1B6FF0, 4, "Main RAM"),
    "link_z": (0x1B6FF4, 4, "Main RAM"),
    "using_item:": (0x1BA71C, 1, "Main RAM")
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


# Read a dict of memory values, like above, returns dict of name to value
async def read_memory_values(ctx, read_list: dict[str, tuple[int, int, str]]) -> dict[str, int]:
    keys = read_list.keys()
    read_data = [r for r in read_list.values()]
    read_result = await bizhawk.read(ctx.bizhawk_ctx, read_data)
    values = [int.from_bytes(i, "little") for i in read_result]
    return {key: value for key, value in zip(keys, values)}


# Read single memory value
async def read_memory_value(ctx, address: int, size=1, domain="Main RAM") -> int:
    read_result = await bizhawk.read(ctx.bizhawk_ctx, [(address, size, domain)])
    print("Reading memory value", hex(address), size, domain, ", got value", hex(int.from_bytes(read_result[0], "little")))
    return int.from_bytes(read_result[0], "little")


# Split up large values to write into smaller chunks
def split_bits(value, size):
    ret = []
    f = 0xFFFFFF00
    for _ in range(size):
        ret.append(value & 0xFF)
        value = (value & f) >> 8
    return ret


# Write specific value to memory
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


async def write_memory_values(ctx, address: int, values: list, domain="Main RAM"):
    prev = await read_memory_value(ctx, address, len(values), domain)
    new_values = [old | new for old, new in zip(split_bits(prev, 4), values)]
    print(f"values: {new_values}, old: {split_bits(prev, 4)}")
    await bizhawk.write(ctx.bizhawk_ctx, [(address, new_values, domain)])


async def get_small_key_address(ctx):
    return await get_address_from_heap(ctx, offset=SMALL_KEY_OFFSET)


async def get_address_from_heap(ctx, pointer=POINTERS["ADDR_gMapManager"], offset=0):
    m_course = 0
    while m_course == 0:
        m_course = await read_memory_value(ctx, pointer, 4, domain="Data TCM")
    read = await read_memory_value(ctx, m_course - 0x02000000, 4)
    print(f"Got map address @ {hex(read + offset - 0x02000000)}")
    return read + offset - 0x02000000


def get_coord_address():
    return {k: v for k, v in RAM_ADDRS.items() if k in ["link_x", "link_y", "link_z"]}


read_keys = ["game_state", "received_item_index", "is_dead", "stage", "room", "floor", "entrance",
             "slot_id", "getting_item", "getting_ship_part"]
READ_LIST = {k: v for k, v in RAM_ADDRS.items() if k in read_keys}


class PhantomHourglassClient(BizHawkClient):
    game = "The Legend of Zelda - Phantom Hourglass"
    system = "NDS"
    local_checked_locations: Set[int]
    local_scouted_locations: Set[int]
    local_tracker: Dict[str, Any]
    item_id_to_name: Dict[int, str]
    location_name_to_id: Dict[str, int]
    location_area_to_watches: Dict[int, dict[str, dict]]

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
        self.last_scene = "NoScene"
        self.locations_in_scene = {}
        self.watches = {}
        self.last_scene_data = ""
        self.receiving_location = False
        self.last_vanilla_item = None
        self.removed_boomerang = True

        self.previous_game_state = False
        self.just_entered_game = False
        self.current_stage = None
        self.last_stage = None
        self.entering_from = None
        self.entering_dungeon = None
        self.unset_dynamic_watches = []
        self.stage_address = 0

        self.delay_pickup = None
        self.last_key_count = 0

        self.key_address = 0
        self.key_value = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            print(f"Rom Name: {rom_name}")
            if rom_name != "ZELDA_DS:PHAZEP":
                if rom_name == "ZELDA_DS:PHAZEE":
                    raise "Invalid Rom: US version is not supported yet, please use a EU rom"
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

    @staticmethod
    async def set_starting_flags(ctx: "BizHawkClientContext") -> None:
        write_list = [(RAM_ADDRS["slot_id"][0], [ctx.slot], "Main RAM")]
        print("New game, setting starting flags")
        print(ctx.slot_data)
        for adr, value in STARTING_FLAGS:
            write_list.append((adr, [value], "Main RAM"))

        # Set starting time for PH
        ph_time = ctx.slot_data["ph_starting_time"] * 3600
        ph_time_bits = split_bits(ph_time, 4)
        write_list.append((0x1BA528, ph_time_bits, "Main RAM"))

        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    # Boomerang is set to enable item menu, called on s+q to remove it again.
    async def boomerwatch(self, ctx) -> bool:
        # There's a softlock where entering the shop menu counts as not in game,
        # and can remove boomerang before enabling item menu. Same goes for changing scene
        if not (self.removed_boomerang or self.entering_from in SHOPS or self.entering_dungeon is not None):
            print("Reconnected, boomerwatching")
            # Check if boomerang has been received
            for item in ctx.items_received:
                if self.item_id_to_name[item.item] == "Boomerang":
                    return True
            # Otherwise remove boomerang
            boomerang = ITEMS_DATA["Boomerang"]
            await write_memory_value(ctx, boomerang["address"], boomerang["value"], unset=True)

            test = await read_memory_value(ctx, boomerang["address"], 1, "Main RAM")
            print("Boomerwatch ""Successful!"f", value is {test}")
            return True
        else:
            return False

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot is None:
            self.just_entered_game = True
            self.last_scene = None
            return

        # Enable "DeathLink" tag if option was enabled
        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)

        try:
            read_result = await read_memory_values(ctx, READ_LIST)

            in_game = read_result["game_state"]
            slot_memory = read_result["slot_id"]
            current_stage = read_result["stage"]
            self.current_stage = current_stage
            # If player is not in-game, don't do anything else

            if not in_game or current_stage not in STAGES:
                print(f"NOT IN GAME, {in_game}, {slot_memory}")
                self.previous_game_state = False
                return

            # On entering game from main menu / cutscene / shop
            if in_game and not self.previous_game_state:
                self.just_entered_game = True
                print(f"Started Game")

                # Remove boomerang if got item menu
                self.removed_boomerang = await self.boomerwatch(ctx)

                # If new file, set up starting flags
                if slot_memory == 0:
                    await self.set_starting_flags(ctx)
                    self.removed_boomerang = False
                    print(f"Set starting flags for slot {slot_memory}")

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

            # Get current scene
            current_room = read_result["room"]
            current_floor = read_result["floor"]
            current_entrance = read_result["entrance"]

            current_stage_text = STAGES.get(current_stage, current_stage)
            current_scene_id = current_stage * 0x100 + current_room  # TODO Change to hex for proper bit range?
            current_scene = f"{current_stage_text}.{current_room}r{current_floor}e{current_entrance}"

            # This go true when link gets item
            holding_item = read_result["getting_item"] & 0x20
            getting_ship_part = read_result["getting_ship_part"]

            # Other game variables
            num_received_items = read_result["received_item_index"]
            is_dead = read_result["is_dead"]  # TODO find actual deathlink address

            # Process on new room
            if not current_scene == self.last_scene:
                self.last_scene = current_scene
                self.entering_dungeon = None
                self.key_value = await read_memory_value(ctx, self.key_address)
                await self.unset_dynamic_flags(ctx)

                # Set Stage flags if new stage, delay if entering dungeon
                if current_stage != self.last_stage and not STAGES[current_stage] in DUNGEON_NAMES:
                    await self.enter_stage(ctx, current_stage)

                # Load locations in room into loop
                self.locations_in_scene = self.location_area_to_watches.get(current_scene_id, {})
                print(f"Locations in scene {current_scene_id}: {self.locations_in_scene.keys()}")
                self.watches = {}
                sram_read_list = {}
                if self.locations_in_scene is not None:
                    # Create memory watches for checks triggerd by flags, and make list for checking sram
                    for loc_name, location in self.locations_in_scene.items():
                        if "address" in location:
                            self.watches[loc_name] = ([location["address"], 1, "Main RAM"])
                        if "sram_addr" in location and location["sram_addr"] is not None:
                            sram_read_list[loc_name] = (location["sram_addr"], 1, "SRAM")

                    # Read and set locations missed when bizhawk was disconnected
                    if len(sram_read_list) > 0:
                        sram_reads = await read_memory_values(ctx, sram_read_list)
                        for loc_name, value in sram_reads.items():
                            if value & LOCATIONS_DATA[loc_name]["sram_value"]:
                                await self.process_checked_locations(ctx, loc_name)

                # Yellow warp in TotOK saves keys
                if self.entering_from is not None:
                    print(f"Current scene {hex(current_scene_id)}, {hex(self.entering_from)}")
                if current_scene_id == 0x2509 and self.entering_from == 0x2507:
                    await self.write_totok_midway_keys(ctx)

                # Set dynamic flags on scene
                if current_scene_id in self.scene_to_dynamic_flag:
                    await self.set_dynamic_flags_on_scene(ctx, current_scene_id)

                # Check if entering dungeon
                if current_stage in DUNGEON_KEY_DATA and self.last_stage != current_stage:
                    self.entering_dungeon = current_stage
                    if self.entering_from is not None:
                        print(f"Entered dungeon {current_stage} from {hex(self.entering_from)}!")
                else:
                    print(f"Not entering dungeon {hex(current_scene_id)}")
                    self.entering_from = current_scene_id   # stage and room

                self.last_stage = current_stage  # just stage
                await self.read_backup_sram(ctx, current_scene_id)
                await self.process_scouted_locations(ctx, current_scene_id)

            # Check for when entering a dungeon cause key count resets after all the triggers for entering the new room
            if self.entering_dungeon is not None:
                z = await read_memory_value(ctx, *RAM_ADDRS["link_z"])
                if self.entering_from in DUNGEON_KEY_DATA[self.entering_dungeon]["entrances"]:
                    # Make different stuff happen when using midway warp in TotOK
                    if self.entering_from == 0x2600 and current_scene_id == 0x2509:
                        self.entering_dungeon = 372
                    boundaries = DUNGEON_KEY_DATA[self.entering_dungeon]["entrances"][self.entering_from]
                    if boundaries.get("min_z", 0) < z < boundaries.get("max_z", 0xFFF0000):
                        print(f"within limits, about to get keys {hex(boundaries.get("min_z", 0))} < {hex(z)} < "
                              f"{hex(boundaries.get("max_z", 0xFFF0000))}")
                        await self.update_key_count(ctx, self.entering_dungeon)
                        await self.enter_stage(ctx, current_stage)
                        self.entering_dungeon = None
                else:
                    self.entering_dungeon = None
            else:
                self.entering_from = current_scene_id

            # Check if link should get item
            if (holding_item or getting_ship_part) and not self.receiving_location and \
                    self.locations_in_scene is not None:
                self.receiving_location = True
                print("Receiving Item")
                await self.unset_dynamic_flags(ctx)
                await self.process_checked_locations(ctx, None)

            # Process received items
            if num_received_items < len(ctx.items_received):
                await self.process_received_items(ctx, num_received_items)

            # Remove Vanilla item from invent after exiting get item cs
            if self.receiving_location and not (holding_item or getting_ship_part):
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
                    print(f"Removing vanilla item {self.last_vanilla_item}")
                    data = ITEMS_DATA[self.last_vanilla_item]
                    value = data.get('value', 1)
                    if "Small Key" in self.last_vanilla_item:
                        address = self.key_address = await get_small_key_address(ctx)
                    elif "progressive" in data:
                        write_list = []
                        index = sum([1 for i in ctx.items_received[:num_received_items] if i.item == data["id"]])
                        address, value = data["progressive"][index]
                        if "give_ammo" in data:
                            ammo_v = data["give_ammo"][max(index-1, 0)]
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

            # Finished game?

            if not ctx.finished_game:
                await self.process_game_completion(ctx, current_scene_id)

            if "DeathLink" in ctx.tags:
                await self.process_deathlink(ctx, is_dead)

            self.previous_game_state = in_game
            self.just_entered_game = False

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            print("Couldn't read data")

    async def set_dynamic_flags_on_scene(self, ctx, scene):
        flag_list = self.scene_to_dynamic_flag[scene]
        read_list, write_list, data_list = [], [], []
        # Read current flag values
        for flag_data in flag_list:
            if "on_scene" in flag_data:
                read_list.append((flag_data["address"], 1, "Main RAM"))
                data_list.append(flag_data)
        print(f"Reading dynflags: {read_list}")
        ret = await bizhawk.read(ctx.bizhawk_ctx, read_list)
        # Check if have requirements
        for byte, data in zip(ret, data_list):
            prev = int.from_bytes(byte, "little")
            if "requires_item" in data:
                have_item = False
                for i in ctx.items_received:
                    if i.item == ITEMS_DATA[data["requires_item"]]["id"]:
                        have_item = True
                        break

                # Write flags
                if have_item or data.get("if_not_has_item", False):
                    write_list.append((data["address"], [prev | data["bit"]], "Main RAM"))
                elif not have_item and not data.get("unset", False):
                    write_list.append((data["address"], [prev & (~data["bit"])], "Main RAM"))

                if data.get("unset", False) and not have_item:
                    coords = await read_memory_values(ctx, get_coord_address())
                    self.unset_dynamic_watches.append({
                        "scene": scene, "address": data["address"], "value": data["bit"], "coords": coords})
        print(f"Writing dynflags: {write_list}")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    # Called when fully entered a stage
    async def enter_stage(self, ctx, stage):
        self.stage_address = await get_address_from_heap(ctx)
        self.key_address = self.stage_address + SMALL_KEY_OFFSET
        if stage in STAGE_FLAGS:
            print(
                f"Setting Stage flags for {STAGES[stage]}, adr: {hex(self.stage_address + STAGE_FLAGS_OFFSET)}")
            await write_memory_values(ctx, self.stage_address + STAGE_FLAGS_OFFSET,
                                      STAGE_FLAGS[stage])

    async def unset_dynamic_flags(self, ctx):
        print(f"unsetting dynflags {self.unset_dynamic_watches}")
        if self.unset_dynamic_watches:
            for flag in self.unset_dynamic_watches:
                await write_memory_value(ctx, flag["address"], flag["value"], unset=True)
            self.unset_dynamic_watches = []

    # Updates key count based on a tracker counter in memory. Called when entering a dungeon
    async def update_key_count(self, ctx, current_stage: int) -> None:
        key_address = self.key_address = await get_small_key_address(ctx)
        key_data = DUNGEON_KEY_DATA[current_stage]
        print(f"current stage setting keys {current_stage}")
        read_list = {"dungeon": (key_address, 1, "Main RAM"),
                     "tracker": (key_data["address"], 1, "Main RAM")}
        key_values = await read_memory_values(ctx, read_list)
        print(f"Base key value: {key_values["tracker"]}, filtered: {(key_values["tracker"] & key_data["filter"])}, divider: {key_data["value"]}")
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

        # If sent with a pre-proces kwarg
        if pre_process is not None:
            loc_id = self.location_name_to_id[pre_process]
            location = LOCATIONS_DATA[pre_process]
            vanilla_item = location.get("vanilla_item")
            print(f"Pre processing, checked locations: {local_checked_locations}")
            if r or (loc_id not in self.local_checked_locations and vanilla_item != pre_process):
                self.last_vanilla_item = vanilla_item
                self.receiving_location = True
                local_checked_locations.add(loc_id)
            print(f"pre-processed {pre_process}, vanill {self.last_vanilla_item}")
        else:
            # Get link's coords
            link_coords = await read_memory_values(ctx, get_coord_address())
            print(link_coords)

            # Figure out what check was just gotten
            for i, loc in enumerate(self.locations_in_scene.items()):
                loc_name, location = loc
                loc_bytes = self.location_name_to_id[loc_name]

                print(f"Processing locs {loc_name}")
                print(f"{location.get("x_max", 0xFFFFFFFF)} > {link_coords["link_x"]} > {location.get("x_min", 0)}")
                print(f"{location.get("z_max", 0xFFFFFFFF)} > {link_coords["link_z"]} > {location.get("z_min", 0)}")

                if (location.get("x_max", 0xFFFFFFFF) > link_coords["link_x"] > location.get("x_min", 0) and
                        location.get("z_max", 0xFFFFFFFF) > link_coords["link_z"] > location.get("z_min", 0) and
                        location.get("y", link_coords["link_y"]) == link_coords["link_y"]):
                    # For rooms with keys that move, check if you got a key first
                    if "delay_pickup" in location:
                        if len(self.locations_in_scene) > i+1:
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

        if location is not None and "set_bit" in location:
            for addr, bit in location["set_bit"]:
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
            if "unique" in SHOPS[scene]:
                location_id = self.location_name_to_id[SHOPS[scene]["unique"]]
                local_scouted_locations.add(location_id)
            has_bow, has_chus = False, False
            for i in ctx.items_received:
                item = self.item_id_to_name[i.item]
                if item == "Bow (Progressive)":
                    has_bow = True
                if item == "Bombchus (Progressive)":
                    has_chus = True

            if has_bow:
                local_scouted_locations.add(self.location_name_to_id["Island Shop Quiver"])
                if has_chus:
                    local_scouted_locations.add(self.location_name_to_id["Island Shop Bombchu Bag"])
                    local_scouted_locations.add(self.location_name_to_id["Island Shop Heart Container"])

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
            if "Temple of the Ocean King" in item_name:
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
                item_value = prev_value | item_value
            else:
                item_value = prev_value | item_data["value"]

            item_values = item_value if type(item_value) is list else [item_value]
            item_values = [min(255, i) for i in item_values]
            write_list.append((item_address, item_values, "Main RAM"))

            # Handle special item conditions
            if "give_ammo" in item_data:
                write_list.append((item_data["ammo_address"], [item_data["give_ammo"][prog_received]], "Main RAM"))
            if "set_bit" in item_data:
                for adr, bit in item_data["set_bit"]:
                    write_list.append((adr, [bit], "Main RAM"))

        # Write the new item to memory!

        print(f"Write list: {write_list}")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def read_backup_sram(self, ctx: "BizHawkClientContext", stage):
        pass

    async def process_game_completion(self, ctx: "BizHawkClientContext", current_scene: int):
        game_clear = (current_scene == 0x2509)  # Dummy ending, entering totok halfway.

        if game_clear:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])
    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead):
        pass
