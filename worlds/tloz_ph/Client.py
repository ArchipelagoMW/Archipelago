import time
from typing import TYPE_CHECKING, Set, Dict, Any

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from Utils import async_start
from worlds._bizhawk.client import BizHawkClient
from worlds.tloz_ph import LOCATIONS_DATA, ITEMS_DATA
from .data.Constants import STARTING_FLAGS, STAGES
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

    "received_item_index": (0x021BA64C, 2, "ARM7 System Bus"),
    "slot_id": (0x021BA64A, 2, "ARM7 System Bus"),

    "stage": (0x021B2E94, 4, "ARM7 System Bus"),
    "floor": (0x021B2E98, 4, "ARM7 System Bus"),
    "room": (0x021B2EA6, 1, "ARM7 System Bus"),
    "entrance": (0x021B2EA7, 1, "ARM7 System Bus"),
    "flags": (0x021B557C, 52, "ARM7 System Bus"),

    "getting_item": (0x1B6F44, 1, "Main RAM"),
    "show_item": (0x057399, 1, "Main RAM"),
    "in_dialogue": (0x1BA73A, 1, "Main RAM"),
    "getting_ship_part": (0x11F5E4, 1, "Main RAM"),
    "link_x": (0x1CB838, 4, "Main RAM"),
    "link_y": (0x1CB83C, 4, "Main RAM"),
    "link_z": (0x1CB840, 4, "Main RAM"),
    "using_item:": (0x1BA71C, 1, "Main RAM")
}

POINTERS = {
    "ADDR_gItemManager": 0x027e0fb4,
    "ADDR_gPlayerManager": 0x027e0fbc,
    "ADDR_gAdventureFlags": 0x027e0f74,
    "ADDR_gPlayer": 0x027e0fec,
    "ADDR_gOverlayManager_mLoadedOverlays_4": 0x027e0910,
    "ADDR_gMapManager": 0x027e0e60
}


# Read a dict of memory values, like above, returns dict of name to value
async def read_memory_values(ctx, read_list: dict[str, tuple[int, int, str]]) -> dict[str, int]:
    keys = read_list.keys()
    read_data = [r for r in read_list.values()]
    read_result = await bizhawk.read(ctx.bizhawk_ctx, read_data)
    values = [int.from_bytes(i, "little") for i in read_result]
    return {key: value for key, value in zip(keys, values)}


# Read single memory value
async def read_memory_value(ctx, address: int, size=1, domain="Main RAM") -> int:
    print("Reading memory value", address, size, domain)
    read_result = await bizhawk.read(ctx.bizhawk_ctx, [(address, size, domain)])
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
    print(f"Writing Memory: {hex(address)}, {value}, {size}, {domain}, {incr}, {unset}")
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
    print(f"Resulting write value")
    await bizhawk.write(ctx.bizhawk_ctx, [(address, write_value, domain)])
    return write_value





read_keys = ["game_state", "received_item_index", "is_dead", "stage", "room", "floor", "entrance",
             "slot_id", "getting_item", "getting_ship_part"]
READ_LIST = {k: v for k, v in RAM_ADDRS.items() if k in read_keys}
print(READ_LIST)


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
        self.scene_address = None
        self.receiving_location = False
        self.last_vanilla_item = None
        self.removed_boomerang = True

        self.previous_game_state = False
        self.just_entered_game = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
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
        write_list = []
        write_list.append((RAM_ADDRS["slot_id"][0], [ctx.slot], "ARM7 System Bus"))

        for adr, value in STARTING_FLAGS:
            write_list.append((adr, [value], "ARM7 System Bus"))

        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    # Boomerang is set to eneble item menu, called on s+q to remove it again.
    async def boomerwatch(self, ctx) -> bool:
        if not self.removed_boomerang:
            print("Reconnected, boomerwatching")
            # Check if boomerang has been received
            for item in ctx.items_received:
                if self.item_id_to_name[item.item] == "Boomerang":
                    return True
            # Otherwise remove boomerang
            boomerang = ITEMS_DATA["Boomerang"]
            await write_memory_value(ctx, boomerang["address"], boomerang["value"], unset=True)
            print("Boomerwatch Successful!")
            return True
        else:
            return False

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot is None:
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
            # If player is not in-game, don't do anything else

            if not in_game or current_stage not in STAGES:
                print(f"NOT IN GAME, {in_game}, {slot_memory}")
                self.previous_game_state = False
                return

            # On entering game from main menu
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
                print(f"Watching {watch_result.keys()}")
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
            current_scene_id = current_stage * 100 + current_room  # TODO Change to hex for proper bit range?
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
                print(f"New Scene: {current_scene}, slot {slot_memory}")

                # Load locations in room into loop
                self.locations_in_scene = self.location_area_to_watches.get(current_scene_id, None)
                self.watches = {}
                if self.locations_in_scene is not None:
                    # Create memory watches for checks triggerd by flags
                    for loc_name, location in self.locations_in_scene.items():
                        if "address" in location:
                            self.watches[loc_name] = ([location["address"], 1, "ARM7 System Bus"])

                self.scene_address = current_scene_id
                await self.process_scouted_locations(ctx)

                # TODO: Read saveram on room reload for missing locaions

            # Check if link should get item
            if (holding_item or getting_ship_part) and not self.receiving_location and \
                    self.locations_in_scene is not None:
                self.receiving_location = True
                print("Receiving Item")
                await self.process_checked_locations(ctx, None)

            # Remove Vanilla item from invent after exiting get item cs
            if self.receiving_location and not (holding_item or getting_ship_part):
                print("Item Received Successfully, removing vanilla item")
                self.receiving_location = False
                if self.last_vanilla_item is not None:
                    data = ITEMS_DATA[self.last_vanilla_item]
                    await write_memory_value(ctx, data['address'], data['value'],
                                             incr=data.get('incremental', None), unset=True)

            # Process checks, scouts and tracker updates
            # await self.process_tracker_updates(ctx, flag_bytes)

            # Process received items
            await self.process_received_items(ctx, num_received_items)

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

    # Called when checking location!
    async def process_checked_locations(self, ctx: "BizHawkClientContext", pre_process: str = None):
        local_checked_locations = set(ctx.locations_checked)

        # If sent with a pre-proces kwarg
        if pre_process is not None:
            loc_bytes = self.location_name_to_id[pre_process]
            local_checked_locations.add(loc_bytes)
        else:
            # Get link's coords
            coord_addr = {k: v for k, v in RAM_ADDRS.items() if k in ["link_x", "link_y", "link_z"]}
            link_coords = await read_memory_values(ctx, coord_addr)

            # Figure out what check was just gotten
            for loc_name, location in self.locations_in_scene.items():
                loc_bytes = self.location_name_to_id[loc_name]
                if "address" in location:
                    # This gets handled in main loop, move to its own function?
                    pass
                elif len(self.locations_in_scene) == 1:
                    local_checked_locations.add(loc_bytes)
                    self.last_vanilla_item = location.get("true_item", location["vanilla_item"])
                    continue
                else:
                    if (location.get("x_max", 0xFFFFFFFF) > link_coords["link_x"] > location.get("x_min", 0) and
                            location.get("z_max", 0xFFFFFFFF) > link_coords["link_z"] > location.get("z_min", 0) and
                            location.get("y", link_coords["link_y"]) == link_coords["link_y"]):
                        local_checked_locations.add(loc_bytes)
                        self.last_vanilla_item = location.get("true_item", location["vanilla_item"])
                        continue

        # Send locations
        if self.local_checked_locations != local_checked_locations:
            self.local_checked_locations = local_checked_locations
            print(f"Sending Locations: {local_checked_locations}")
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(self.local_checked_locations)
            }])

    async def process_scouted_locations(self, ctx: "BizHawkClientContext"):
        pass

    async def process_received_items(self, ctx: "BizHawkClientContext", num_received_items: int) -> None:
        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        print(f"items received: {num_received_items}, {len(ctx.items_received)}, {self.last_vanilla_item}")
        if num_received_items < len(ctx.items_received):
            next_item = ctx.items_received[num_received_items].item
            item_name = self.item_id_to_name[next_item]
            print(f"About to get {item_name}")
            item_data = ITEMS_DATA[item_name]
            item_address = item_data["address"]

            # Increment in-game items received count
            received_item_address = RAM_ADDRS["received_item_index"]
            write_list = [(received_item_address[0], [num_received_items + 1], received_item_address[2])]
            print(f"Items index address {hex(received_item_address[0])}")
            if item_name == self.last_vanilla_item:
                self.last_vanilla_item = None
            else:
                # Read address item is to be written to
                item_value = await read_memory_value(ctx, item_address, domain="Main RAM",
                                                     size=item_data.get("size", 1))
                print(f"Read address for item {item_name} at {hex(item_address)} for value {hex(item_value)}")

                # Handle different writing operations
                if "incremental" in item_data:
                    item_value += item_data["value"]
                    item_value = 0 if item_value <= 0 else item_value
                    print(f"Giving incremental: {item_name}, {item_value}, ")
                    if "size" in item_data:
                        item_value = split_bits(item_value, item_data["size"])
                        # TODO if incremental goes above size it's a problem!
                else:
                    item_value = [item_value | item_data["value"]]

                item_values = item_value if type(item_value) is list else [item_value]
                print(f"Writing {[hex(i) for i in item_values]}")
                write_list.append((item_address, item_values, "Main RAM"))

                # Handle special item conditions
                if "give_ammo" in item_data:
                    write_list.append((item_data["ammo_address"], [item_data["give_ammo"]], "Main RAM"))
                if "write_bit" in item_data:
                    write_list.append((item_data["write_bit"], [1], "Main RAM"))

            # Write the new item to memory!
            print(f"Writing items {write_list}")
            await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def process_game_completion(self, ctx: "BizHawkClientContext", flag_bytes, current_room: int):
        pass

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead):
        pass
