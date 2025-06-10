import time
from typing import TYPE_CHECKING, Set, Dict, Any

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from Utils import async_start
from worlds._bizhawk.client import BizHawkClient
from worlds.tloz_ph import LOCATIONS_DATA, ITEMS_DATA
from .data.Constants import STARTING_FLAGS, STAGES, DUNGEON_KEY_DATA, SHOPS
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


async def get_small_key_address(ctx):
    m_course = 0
    while m_course == 0:
        m_course = await read_memory_value(ctx, POINTERS["ADDR_gMapManager"], 4, domain="Data TCM")
    read = await read_memory_value(ctx, m_course - 0x02000000, 4)
    print(f"Got map address @ {hex(read + SMALL_KEY_OFFSET - 0x02000000)}")
    return read + SMALL_KEY_OFFSET - 0x02000000

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

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            print(f"Rom Name: {rom_name}")
            if rom_name != "ZELDA_DS:PHAZEP":
                return False
        except bizhawk.RequestFailedError:
            print("Invalid rom????")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b011
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
        for adr, value in STARTING_FLAGS:
            write_list.append((adr, [value], "Main RAM"))

        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    # Boomerang is set to eneble item menu, called on s+q to remove it again.
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

            # On entering game from main menu / cutscene
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
                print(f"New room {self.last_scene} -> {current_scene}")
                print(f"New Scene: {current_scene}, slot {slot_memory}")

                # Load locations in room into loop
                self.locations_in_scene = self.location_area_to_watches.get(current_scene_id, None)
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
                boundaries = DUNGEON_KEY_DATA[self.entering_dungeon]["entrances"][self.entering_from]
                print(f"In dungeon {self.entering_dungeon} from {self.entering_from}")
                if boundaries.get("min_z", 0) < z < boundaries.get("max_z", 0xFFF0000):
                    print(f"within limits, about to get keys {hex(boundaries.get("min_z", 0))} < {hex(z)} < "
                          f"{hex(boundaries.get("max_z", 0xFFF0000))}")
                    await self.update_key_count(ctx, self.current_stage)
                    self.entering_dungeon = None
            else:
                self.entering_from = current_scene_id

            # Check if link should get item
            if (holding_item or getting_ship_part) and not self.receiving_location and \
                    self.locations_in_scene is not None:
                self.receiving_location = True
                print("Receiving Item")
                await self.process_checked_locations(ctx, None)

            # Process received items
            if num_received_items < len(ctx.items_received):
                await self.process_received_items(ctx, num_received_items)

            # Remove Vanilla item from invent after exiting get item cs
            if self.receiving_location and not (holding_item or getting_ship_part):
                print("Item Received Successfully")
                self.receiving_location = False
                if self.last_vanilla_item is not None:
                    print(f"Removing vanilla item {self.last_vanilla_item}")
                    data = ITEMS_DATA[self.last_vanilla_item]
                    value = data.get('value', 1)
                    if "Small Key" in self.last_vanilla_item:
                        address = await get_small_key_address(ctx)
                    elif "progressive" in data:
                        index = sum([1 for i in ctx.items_received[:num_received_items] if i.item == data["id"]])
                        address, value = data["progressive"][index]
                        ammo_v = data["give_ammo"][max(index-1, 0)]
                        write_list = [(data["ammo_address"], [ammo_v], "Main RAM")]
                        if index == 2:
                            write_list.append((address, [1], "Main RAM"))
                        await bizhawk.write(ctx.bizhawk_ctx, write_list)
                    else:
                        address = data["address"]

                    await write_memory_value(ctx, address, value,
                                             incr=data.get('incremental', None), unset=True)

            # Process checks, scouts and tracker updates
            # await self.process_tracker_updates(ctx, flag_bytes)



            # Finished game?
            """
            if not ctx.finished_game:
                await self.process_game_completion(ctx, flag_bytes, current_room)
            """
            if "DeathLink" in ctx.tags:
                await self.process_deathlink(ctx, is_dead)

            self.previous_game_state = in_game
            self.just_entered_game = False

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            print("Couldn't read data")

    # Updates key count based on a tracker counter in memory. Called when entering a dungeon
    @staticmethod
    async def update_key_count(ctx, current_stage: int) -> None:
        key_address = await get_small_key_address(ctx)
        key_data = DUNGEON_KEY_DATA[current_stage]
        read_list = {"dungeon": (key_address, 1, "Main RAM"),
                     "tracker": (key_data["address"], 1, "Main RAM")}
        key_values = await read_memory_values(ctx, read_list)
        print(f"Base key value: {key_values["tracker"]}, filtered: {(key_values["tracker"] & key_data["filter"])}, divider: {key_data["value"]}")
        new_keys = (((key_values["tracker"] & key_data["filter"]) // key_data["value"])
                    + key_values["dungeon"])
        if new_keys != 0:
            new_keys = 7 if new_keys >= 7 else new_keys
            reset_tracker = (~key_data["filter"]) & key_values["tracker"]
            print(f"Finally writing keys to memory {hex(key_address)} with value {hex(new_keys)}")
            await bizhawk.write(ctx.bizhawk_ctx, [(key_address, [new_keys], "Main RAM"),
                                                  (key_data["address"], [reset_tracker], "Main RAM")])

    # Called when checking location!
    async def process_checked_locations(self, ctx: "BizHawkClientContext", pre_process: str = None):
        local_checked_locations = set(ctx.locations_checked)

        # If sent with a pre-proces kwarg
        if pre_process is not None:
            loc_bytes = self.location_name_to_id[pre_process]
            local_checked_locations.add(loc_bytes)
            location = LOCATIONS_DATA[pre_process]
            self.last_vanilla_item = location.get("true_item", location["vanilla_item"])
            self.receiving_location = True
        else:
            # Get link's coords
            coord_addr = {k: v for k, v in RAM_ADDRS.items() if k in ["link_x", "link_y", "link_z"]}
            link_coords = await read_memory_values(ctx, coord_addr)
            print(link_coords)

            # Figure out what check was just gotten
            for loc_name, location in self.locations_in_scene.items():
                loc_bytes = self.location_name_to_id[loc_name]
                if len(self.locations_in_scene) == 1:
                    local_checked_locations.add(loc_bytes)
                    self.last_vanilla_item = location.get("true_item", location["vanilla_item"])
                    break
                else:
                    if (location.get("x_max", 0xFFFFFFFF) > link_coords["link_x"] > location.get("x_min", 0) and
                            location.get("z_max", 0xFFFFFFFF) > link_coords["link_z"] > location.get("z_min", 0) and
                            location.get("y", link_coords["link_y"]) == link_coords["link_y"]):
                        local_checked_locations.add(loc_bytes)
                        self.last_vanilla_item = location.get("true_item", location["vanilla_item"])
                        break

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

        # If same as vanilla item don't remove
        if item_name == self.last_vanilla_item:
            self.last_vanilla_item = None
            print(f"oops it's vanilla! {self.last_vanilla_item}")
        # Handle Small Keys
        elif "Small Key" in item_name:
            data = DUNGEON_KEY_DATA[item_data["dungeon"]]
            prev_value = await read_memory_value(ctx, data["address"])
            if self.current_stage == item_data["dungeon"]:
                print("In dungeon! Getting Key")
                key_address = await get_small_key_address(ctx)
                prev_value = await read_memory_value(ctx, key_address)
                write_list.append((key_address, [prev_value+1], "Main RAM"))

            elif (prev_value & data["filter"]) != data["filter"]:
                new_value = prev_value + data["value"]
                print(f"Writing keys to storage: {hex(prev_value)} -> {hex(new_value)}")
                write_list.append((data["address"], [new_value], "Main RAM"))
            else:
                print(f"Too many keys for dungeon {item_data['dungeon']}")
        else:
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
                item_value = prev_value + item_data["value"]
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
            if "write_bit" in item_data:
                write_list.append((item_data["write_bit"], [1], "Main RAM"))

        # Write the new item to memory!

        print(f"Write list: {write_list}")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def read_backup_sram(self, ctx: "BizHawkClientContext", stage):
        pass

    async def process_game_completion(self, ctx: "BizHawkClientContext", flag_bytes, current_room: int):
        pass

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead):
        pass
