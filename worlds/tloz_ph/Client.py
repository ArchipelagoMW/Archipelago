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
    "game_state": (0x075E0D, 1, "Main RAM"),  # TODO find game state and dead variables
    "is_dead": (0xC2EE, 1, "ARM7 System Bus"),

    "received_item_index": (0x021BA64C, 2, "ARM7 System Bus"),
    "slot_id": (0x021BA64A, 2, "ARM7 System Bus"),

    "stage": (0x021B2E94, 4, "ARM7 System Bus"),
    "floor": (0x021B2E98, 4, "ARM7 System Bus"),
    "room": (0x021B2EA6, 1, "ARM7 System Bus"),
    "entrance": (0x021B2EA7, 1, "ARM7 System Bus"),
    "flags": (0x021B557C, 52, "ARM7 System Bus"),
    "items": (0x021BA644, 6, "ARM7 System Bus"),

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
        self.watches = []
        self.watches_values = []
        self.watches_ids = []
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

    async def set_slot_data(self, ctx: "BizHawkClientContext"):  # TODO Naming Conflict
        write_list = []
        write_list.append((RAM_ADDRS["slot_id"][0], [ctx.slot], "ARM7 System Bus"))

        for adr, value in STARTING_FLAGS:
            write_list.append((adr, [value], "ARM7 System Bus"))

        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot is None:
            return

        # Enable "DeathLink" tag if option was enabled
        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)

        try:
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"],  # Current state of game (is the player actually in-game?)
                RAM_ADDRS["received_item_index"],  # Number of received items
                RAM_ADDRS["is_dead"],  # Is Link Dead? 2

                RAM_ADDRS["stage"],  # Read link's location 3
                RAM_ADDRS["room"],
                RAM_ADDRS["floor"],
                RAM_ADDRS["entrance"],

                RAM_ADDRS["slot_id"],  # Read slot 7

                RAM_ADDRS["getting_item"],  # Turns to 0x2D when link is in holding item cs
                RAM_ADDRS["getting_ship_part"]
            ])

            def result(*args) -> list[int]:
                return [int.from_bytes(read_result[i], "little") for i in args]

            in_game = bool.from_bytes(read_result[0], "little")
            slot_memory = result(7)[0]
            # If player is not in-game, don't do anything else

            if not in_game:
                print(f"NOT IN GAME, {in_game}, {slot_memory}")
                self.previous_game_state = False
                return

            if in_game and not self.previous_game_state:
                self.just_entered_game = True
                print(f"Started Game, Boomerwatch: {self.removed_boomerang}")

                # Remove boomerang if got item menu
                if not self.removed_boomerang:
                    print("Reconnected, boomerwatching")
                    boomer_watch = True
                    for item in ctx.items_received:
                        if self.item_id_to_name[item.item] == "Boomerang":
                            boomer_watch = False
                            self.removed_boomerang = True
                    if boomer_watch:
                        boomerang = ITEMS_DATA["Boomerang"]
                        prev_value_raw = await bizhawk.read(ctx.bizhawk_ctx, [
                            (boomerang["address"], 1, "ARM7 System Bus")])
                        prev_value = int.from_bytes(prev_value_raw[0], "little")
                        prev_value = prev_value - (prev_value & boomerang["value"])
                        write_list = (boomerang["address"], [prev_value], "ARM7 System Bus")
                        await bizhawk.write(ctx.bizhawk_ctx, [write_list])
                        self.removed_boomerang = True
                        print("Boomerwatch Successful!")

                # If new file, set up starting flags
                if slot_memory == 0:
                    await self.set_slot_data(ctx)
                    self.removed_boomerang = False
                    print(f"Set starting flags for slot {slot_memory}")

            # Read for checks on specific global flags
            if len(self.watches) > 0:
                watch_read = await bizhawk.read(ctx.bizhawk_ctx, self.watches)
                watch_result = [int.from_bytes(value, "little") for value in watch_read]
                print(f"Watching {watch_result}")
                for w_result, value, loc_id in zip(watch_result, self.watches_values, self.watches_ids):
                    if w_result & value:
                        print(f"Got read item {loc_id} from address {result} looking at bit {value}")
                        await self.process_checked_locations(ctx, loc_id)
                        self.watches.pop(self.watches_ids.index(loc_id))
                        # TODO This breaks on scenes with multiple watches

            # Get current scene
            current_stage = result(3)[0]
            if current_stage not in STAGES:  # Other scenes include title screen and file select, add slot later
                return
            current_room, current_floor, current_entrance = result(4, 5, 6)

            current_stage_text = STAGES.get(current_stage, current_stage)
            current_scene_id = current_stage * 100 + current_room
            current_scene = f"{current_stage_text}.{current_room}r{current_floor}e{current_entrance}"

            # This go true when link gets item
            holding_item = result(8)[0] & 0x20
            getting_ship_part = result(9)[0] & 0x2

            # Other game variables
            num_received_items = result(1)[0]
            is_dead = (read_result[2][0] != 0)

            # Process on new room
            if not current_scene == self.last_scene:
                self.last_scene = current_scene
                print(f"New Scene: {current_scene}, slot {slot_memory}")

                # Load locations in room into loop
                self.locations_in_scene = self.location_area_to_watches.get(current_scene_id, None)
                self.watches = []
                self.watches_values = []
                self.watches_ids = []
                if self.locations_in_scene is not None:
                    # Create memory watches for checks triggerd by flags
                    for loc_name, location in self.locations_in_scene.items():
                        if "address" in location:
                            self.watches.append([location["address"], 1, "ARM7 System Bus"])
                            self.watches_values.append(location["value"])
                            self.watches_ids.append(loc_name)

                self.scene_address = current_scene_id

                # TODO: Read saveram on room reload for missing locaions

            # Check if link should get item
            if (holding_item or getting_ship_part) and not self.receiving_location and self.locations_in_scene is not None:
                self.receiving_location = True
                print("Receiving Item")
                await self.process_checked_locations(ctx, None)

            # Remove Vanilla item from invent after exiting get item cs
            if self.receiving_location and not (holding_item or getting_ship_part):
                print("Item Received Successfully, removing vanilla item")
                self.receiving_location = False
                if self.last_vanilla_item is not None:
                    data = ITEMS_DATA[self.last_vanilla_item]
                    prev_value_raw = await bizhawk.read(ctx.bizhawk_ctx, [(data["address"], 1, "ARM7 System Bus")])
                    prev_value = int.from_bytes(prev_value_raw[0], "little")
                    if "incremental" in data:
                        prev_value -= data["value"]
                    else:
                        print(f"{prev_value} - {data["value"]} = {prev_value - (prev_value & data["value"])}, just & {prev_value & data["value"]}")
                        prev_value = prev_value - (prev_value & data["value"])
                    print(f"Setting item {self.last_vanilla_item} at address {data["address"]} to {prev_value}")
                    prev_value = 0 if prev_value <= 0 else prev_value
                    await bizhawk.write(ctx.bizhawk_ctx, [(data["address"], [prev_value], "ARM7 System Bus")])




            # Process checks, scouts and tracker updates
            """
            await self.process_checked_locations(ctx, flag_bytes)
            await self.process_scouted_locations(ctx, flag_bytes)
            await self.process_tracker_updates(ctx, flag_bytes)
            """

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

    async def process_checked_locations(self, ctx: "BizHawkClientContext", pre_process: str = None):
        local_checked_locations = set(ctx.locations_checked)

        # If sent with a pre-proces kwarg
        if pre_process is not None:
            loc_bytes = self.location_name_to_id[pre_process]
            local_checked_locations.add(loc_bytes)
        else:

            # Get link's coords
            coords_raw = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["link_x"],  # Link's Coords
                RAM_ADDRS["link_y"],
                RAM_ADDRS["link_z"]
            ])
            link_coords = [int.from_bytes(value, "little") for value in coords_raw]

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
                    if (location.get("x_max", 0xFFFFFFFF) > link_coords[0] > location.get("x_min", 0) and
                            location.get("z_max", 0xFFFFFFFF) > link_coords[2] > location.get("z_min", 0) and
                            location.get("y", link_coords[1]) == link_coords[1]):
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


    async def process_scouted_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        pass

    async def process_received_items(self, ctx: "BizHawkClientContext", num_received_items: int):
        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        if num_received_items < len(ctx.items_received):
            next_item = ctx.items_received[num_received_items].item
            item_data = ITEMS_DATA[self.item_id_to_name[next_item]]
            item_address = item_data["address"]

            # Read address item is to be written to
            prev_value_raw = await bizhawk.read(ctx.bizhawk_ctx, [(item_address, 1, "ARM7 System Bus")])
            prev_value = int.from_bytes(prev_value_raw[0], "little")

            # Increment in-game items received count
            received_item_address = RAM_ADDRS["received_item_index"]
            write_list = [(received_item_address[0], [num_received_items + 1], received_item_address[2])]
            item_value = prev_value

            print(f"Received item {self.item_id_to_name[next_item]}")
            # Handle different writing operations
            if "incremental" in item_data:
                item_value += item_data["value"]
                print(f"Giving incremental: {self.item_id_to_name[next_item]}, {item_value}, ")
                if item_value >= 256:
                    item_value = 255
            else:
                item_value = item_value | item_data["value"]

            if "give_ammo" in item_data:
                write_list.append((item_data["ammo_address"], [item_data["give_ammo"]], "Main RAM"))
            if "write_bit" in item_data:
                write_list.append((item_data["write_bit"], [1], "ARM7 System BUS"))
            write_list.append((item_address, [item_value], "ARM7 System Bus"))
            await bizhawk.write(ctx.bizhawk_ctx, write_list)
            if next_item == self.last_vanilla_item:
                self.last_vanilla_item = None

    async def process_game_completion(self, ctx: "BizHawkClientContext", flag_bytes, current_room: int):
        pass

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead):
        pass


if __name__ == '__main__':
    PhantomHourglassClient()
