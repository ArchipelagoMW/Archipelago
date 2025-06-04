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
    "game_state": (0xC2EE, 1, "ARM7 System Bus"),  # TODO find game state and dead variables
    "is_dead": (0xC2EE, 1, "ARM7 System Bus"),

    "received_item_index": (0x021BA64C, 2, "ARM7 System Bus"),
    "slot_id": (0x021BA64A, 2, "ARM7 System Bus"),

    "stage": (0x021B2E94, 4, "ARM7 System Bus"),
    "floor": (0x021B2E98, 4, "ARM7 System Bus"),
    "room": (0x021B2EA6, 1, "ARM7 System Bus"),
    "entrance": (0x021B2EA7, 1, "ARM7 System Bus"),
    "flags": (0x021B557C, 52, "ARM7 System Bus"),
    "items": (0x021BA644, 6, "ARM7 System Bus"),

    "link_stalled": (0x1BA728, 1, "Main RAM"),
    "show_item": (0x057399, 1, "Main RAM"),
    "in_dialogue": (0x1BA73A, 1, "Main RAM"),
    "link_x": (0x1CB838, 4, "Main RAM"),
    "link_y": (0x1CB83C, 4, "Main RAM"),
    "link_z": (0x1CB840, 4, "Main RAM")

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
    location_area_to_watches: Dict[int, list[dict[int, str]]]

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
        self.watches = {}
        self.last_scene_data = ""
        self.scene_address = None
        self.receiving_location = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name != "ZELDA_DS:PHAZEP":
                return False
        except bizhawk.RequestFailedError:
            print("Request Failed Error")
            return False

        ctx.game = self.game
        ctx.items_handling = 0b10
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5

        return True


    def on_package(self, ctx, cmd, args):
        if cmd == 'Connected':
            if 'death_link' in args['slot_data'] and args['slot_data']['death_link']:
                self.set_deathlink = True
                self.last_deathlink = time.time()
        super().on_package(ctx, cmd, args)

    async def set_slot_data(self, ctx: "BizHawkClientContext"):
        write_list = []
        write_list.append(
            (RAM_ADDRS["slot_id"][0], [1], "ARM7 System Bus"))  # Replace slot with ctx.slot once server connected
        write_list.append((RAM_ADDRS["items"][0], [0x4], "ARM7 System Bus"))

        for adr, value in STARTING_FLAGS:
            write_list.append((adr, [value], "ARM7 System Bus"))

        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        """
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return
        """
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

                RAM_ADDRS["link_stalled"],  # These 3 together say when in item get cs
                RAM_ADDRS["show_item"],  # 9
                RAM_ADDRS["in_dialogue"],
                RAM_ADDRS["link_x"],  # Link's Coords 11
                RAM_ADDRS["link_y"],
                RAM_ADDRS["link_z"]
            ])
            """
            # If player is not in-game, don't do anything else
            if read_result is None or read_result[0][0] != 2:
                return
            """

            def result(*args) -> list[int]:
                return [int.from_bytes(read_result[i], "little") for i in args]

            # Get current scene
            current_stage = result(3)[0]
            if current_stage not in STAGES:  # Other scenes include title screen and file select, add slot later
                return
            current_room, current_floor, current_entrance = result(4, 5, 6)

            current_stage_text = STAGES.get(current_stage, current_stage)
            current_scene_id = current_stage * 100 + current_room
            current_scene = f"{current_stage_text}.{current_room}r{current_floor}e{current_entrance}"

            # These go true when link gets item
            link_stalled = result(8)[0] == 8
            show_item = result(9)[0] == 0x10
            in_dialogue = result(10)[0] == 8

            # Link's coordinates
            link_x, link_y, link_z = result(11, 12, 13)
            link_coords = (link_x, link_y, link_z)

            # Other game variables
            slot_memory = result(7)
            num_received_items = result(1)[0]
            is_dead = (read_result[2][0] != 0)



            # Process on new room
            if not current_scene == self.last_scene:
                self.last_scene = current_scene
                print(f"New Scene: {current_scene}")

                # If new file, set up starting flags
                if slot_memory == 0:
                    await self.set_slot_data(ctx)

                self.watches = self.location_area_to_watches.get(current_scene_id, None)
                # TODO: complete location watches
                self.scene_address = current_scene_id

            if link_stalled and show_item and not in_dialogue:
                print("Room Transition/opening door~")

            if not link_stalled and show_item and in_dialogue:
                print("Talking to NPC~")

            # Triggers when link holds item above head
            if link_stalled and show_item and in_dialogue and not self.receiving_location and self.watches is not None:
                self.receiving_location = True
                print("Receiving Item")
                await self.process_checked_locations(ctx, link_coords)

            if self.receiving_location and not (link_stalled or show_item or in_dialogue):
                print("Item Received Successfully")
                self.receiving_location = False



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

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            print("Couldn't read data")

    async def process_checked_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        local_checked_locations = set(ctx.locations_checked)
        for loc_name, location in self.watches.items():
            loc_bytes = self.location_name_to_id[loc_name]
            if "address" in location:
                # Read address and check if set
                pass
            elif len(self.watches) == 1:
                local_checked_locations.add(loc_bytes)
            else:
                if (location.get("max_x", 0xFFFFFFFF) > flag_bytes[0] > location.get("min_x", 0) and
                        location.get("max_z", 0xFFFFFFFF) > flag_bytes[2] > location.get("min_z", 0)):
                    local_checked_locations.add(loc_bytes)

        # Send locations
        if self.local_checked_locations != local_checked_locations:
            self.local_checked_locations = local_checked_locations
            print("Sending Locations")
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(self.local_checked_locations)
            }])

    async def process_scouted_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        pass

    async def process_received_items(self, ctx: "BizHawkClientContext", num_received_items: int):
        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        print(f"Items Received: {num_received_items} / {ctx.items_received}")
        if num_received_items < len(ctx.items_received):
            next_item = ctx.items_received[num_received_items].item
            print("Sent item", next_item)
            item_address = ITEMS_DATA[next_item].address
            item_value = ITEMS_DATA[next_item].address
            await bizhawk.write(ctx.bizhawk_ctx, [
                (item_address, [item_value], "ARM7 System Bus"),
                (RAM_ADDRS["received_item_index"][0], [num_received_items+1], RAM_ADDRS["received_item_index"][2])
            ])

    async def process_game_completion(self, ctx: "BizHawkClientContext", flag_bytes, current_room: int):
        pass

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead):
        pass

if __name__ == '__main__':
    PhantomHourglassClient()
