import time
from collections import defaultdict
from typing import TYPE_CHECKING, Set, Dict, Any

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from Utils import async_start
from .data.Locations import LOCATIONS_DATA
from .Options import OracleOfSeasonsGoal
from .Util import build_item_id_to_name_dict, build_location_name_to_id_dict

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

ROOM_AFTER_DRAGONOX = 0x0790
ROOM_BLAINOS_GYM = 0x03B4
ROOM_ZELDA_ENDING = 0x059A

ROM_ADDRS = {
    "game_identifier": (0x0134, 9, "ROM"),
    "slot_name": (0xFFFC0, 64, "ROM"),
}

RAM_ADDRS = {
    "game_state": (0xC2EE, 1, "System Bus"),
    "received_item_index": (0xC6A0, 2, "System Bus"),
    "received_item": (0xCBFB, 1, "System Bus"),
    "location_flags": (0xC600, 0x500, "System Bus"),

    "current_map_group": (0xCC49, 1, "System Bus"),
    "current_map_id": (0xCC4C, 1, "System Bus"),
    "is_dead": (0xCC34, 1, "System Bus"),
}

GASHA_ADDRS = {
    "Mount Cucco Gasha Spot": (0xc71f, 0x00),
    "Tarm Ruins Gasha Spot": (0xc722, 0x01),
    "Goron Mountain West Gasha Spot": (0xc738, 0x02),
    "Goron Mountain East Gasha Spot": (0xc73b, 0x03),
    "Onox Gasha Spot": (0xc744, 0x04),
    "Sunken City Gasha Spot": (0xc73f, 0x05),
    "Holodrum Plain Island Gasha Spot": (0xc775, 0x06),
    "Spool Swamp North Gasha Spot": (0xc780, 0x07),
    "Eyeglass Lake Gasha Spot": (0xc789, 0x08),
    "Lower Holodrum Plain Gasha Spot": (0xc795, 0x09),
    "North Horon Gasha Spot": (0xc7a6, 0x0a),
    "Eastern Suburbs Gasha Spot": (0xc7ac, 0x0b),
    "Spool Swamp South Gasha Spot": (0xc7c0, 0x0c),
    "Samasa Desert Gasha Spot": (0xc7ef, 0x0d),
    "Western Coast Gasha Spot": (0xc7f0, 0x0e),
    "Horon Village Gasha Spot": (0xc7c8, 0x0f),
}


class OracleOfSeasonsClient(BizHawkClient):
    game = "The Legend of Zelda - Oracle of Seasons"
    system = "GBC"
    patch_suffix = ".apoos"
    local_checked_locations: Set[int]
    local_scouted_locations: Dict[int, set[int]]
    local_tracker: Dict[str, Any]
    item_id_to_name: Dict[int, str]
    location_name_to_id: Dict[str, int]

    def __init__(self) -> None:
        super().__init__()
        self.item_id_to_name = build_item_id_to_name_dict()
        self.location_name_to_id = build_location_name_to_id_dict()
        self.local_scouted_locations = defaultdict(lambda: set())
        self.local_tracker = {}

        self.set_deathlink = False
        self.last_deathlink = None
        self.was_alive_last_frame = False
        self.is_expecting_received_death = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name != "ZELDA DIN":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001  # Only remote items
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["slot_name"]]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
        pass

    def on_package(self, ctx, cmd, args):
        if cmd == "Connected":
            if args["slot_data"]["options"]["death_link"]:
                self.set_deathlink = True
                self.last_deathlink = time.time()
            if args["slot_data"]["options"]["move_link"]:
                ctx.tags.add("MoveLink")
                self.move_link = []
                async_start(ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}]))
        if cmd == "Bounced":
            if ctx.slot_data["options"]["move_link"] and "tags" in args and args["tags"][0] == "MoveLink":
                data = args["data"]
                if data["slot"] != ctx.slot:
                    data["last_process"] = time.time()
                    data["spoilage"] = data["last_process"] + data["timespan"]
                    self.move_link.append(data)
        super().on_package(ctx, cmd, args)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot_data is None:
            return

        # Enable "DeathLink" tag if option was enabled
        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)

        try:
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"],  # Current state of game (is the player actually in-game?)
                RAM_ADDRS["received_item_index"],  # Number of received items
                RAM_ADDRS["received_item"],  # Received item still pending?
                RAM_ADDRS["location_flags"],  # Location flags
                RAM_ADDRS["current_map_group"],  # Current map group & id where the player is currently located
                RAM_ADDRS["current_map_id"],  # ^^^
                RAM_ADDRS["is_dead"]
            ])

            # If player is not in-game, don't do anything else
            if read_result is None or read_result[0][0] != 2:
                return

            num_received_items = int.from_bytes(read_result[1], "little")
            received_item_is_empty = (read_result[2][0] == 0)
            flag_bytes = read_result[3]
            current_room = (read_result[4][0] << 8) | read_result[5][0]
            is_dead = (read_result[6][0] != 0)

            if "MoveLink" in ctx.tags:
                # We need to move the player first to not teleport the player away from an item
                await self.process_movelink_for_april_fools(ctx, current_room)

            await self.process_checked_locations(ctx, flag_bytes)
            await self.process_scouted_locations(ctx, flag_bytes)
            await self.process_tracker_updates(ctx, flag_bytes, current_room)

            # Process received items (only if we aren't in Blaino's Gym to prevent him from calling us cheaters)
            if received_item_is_empty and current_room != ROOM_BLAINOS_GYM:
                await self.process_received_items(ctx, num_received_items)

            if not ctx.finished_game:
                await self.process_game_completion(ctx, flag_bytes, current_room)

            if "DeathLink" in ctx.tags:
                await self.process_deathlink(ctx, is_dead)

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def process_checked_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        checked_locations = set()
        for name, location in LOCATIONS_DATA.items():
            if "flag_byte" not in location:
                continue

            byte_addr = location["flag_byte"]
            byte_offset = byte_addr - RAM_ADDRS["location_flags"][0]
            bit_mask = location["bit_mask"] if "bit_mask" in location else 0x20
            if flag_bytes[byte_offset] & bit_mask == bit_mask:
                location_id = self.location_name_to_id[name]
                checked_locations.add(location_id)

        # Check how many deterministic Gasha Nuts have been opened, and mark their matching locations as checked
        byte_offset = 0xC649 - RAM_ADDRS["location_flags"][0]
        gasha_counter = flag_bytes[byte_offset] >> 2
        for i in range(gasha_counter):
            name = f"Gasha Nut #{i + 1}"
            location_id = self.location_name_to_id[name]
            checked_locations.add(location_id)

        # Send locations
        await ctx.check_locations(checked_locations)

    async def process_scouted_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        self.local_scouted_locations[ctx.slot].update(ctx.locations_info)
        new_scouted_locations = defaultdict(lambda: [])
        for name, location in LOCATIONS_DATA.items():
            if "scouting_byte" not in location:
                continue
            # Do not hint forced shop slot if it is enabled, since it would cause an error on MultiServer's side
            if name == "Horon Village: Shop #3":
                if ctx.slot_data["options"]["enforce_potion_in_shop"]:
                    continue

            # Do not hint buisiness scrubs if disabled, since it would cause an error on MultiServer's side
            if name.endswith("Business Scrub"):
                if not ctx.slot_data["options"]["shuffle_business_scrubs"]:
                    continue

            # Check "scouting_byte" to see if map has been visited for scoutable locations
            byte_to_test = location["scouting_byte"]
            byte_offset = byte_to_test - RAM_ADDRS["location_flags"][0]
            bit_mask = location["scouting_mask"] if "scouting_mask" in location else 0x10
            if flag_bytes[byte_offset] & bit_mask == bit_mask:
                if "owl_id" in location:
                    if len(ctx.slot_data["item_hints"]) == 0:
                        continue
                    hint = ctx.slot_data["item_hints"][location["owl_id"]]
                    if hint is None:
                        continue
                    location_id, player = hint
                else:
                    # Map has been visited, scout the location if it hasn't been already
                    player = ctx.slot
                    location_id = self.location_name_to_id[name]
                if location_id not in self.local_scouted_locations[player]:
                    new_scouted_locations[player].append(location_id)
                    self.local_scouted_locations[player].add(location_id)

        for player in new_scouted_locations:
            await ctx.send_msgs([{
                "cmd": "CreateHints",
                "locations": new_scouted_locations[player],
                "player": player
            }])
            # We could use _read_hints_{self.ctx.team}_{player} to check if the hint was created

    async def process_received_items(self, ctx: "BizHawkClientContext", num_received_items: int):
        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        if num_received_items < len(ctx.items_received):
            next_item = ctx.items_received[num_received_items].item
            item_id = next_item // 0x100
            item_subid = next_item % 0x100
            if item_id == 0x30:  # Small or master key
                item_subid = item_subid & 0x7F  # TODO: Remove this if/when both master and small can be obtained in the same world
            await bizhawk.write(ctx.bizhawk_ctx, [(0xCBFB, [item_id, item_subid], "System Bus")])

    async def process_game_completion(self, ctx: "BizHawkClientContext", flag_bytes, current_room: int):
        game_clear = False
        if ctx.slot_data["options"]["goal"] == OracleOfSeasonsGoal.option_beat_onox:
            # Room with Din's descending crystal was reached, it's a win
            game_clear = (current_room == ROOM_AFTER_DRAGONOX)
        elif ctx.slot_data["options"]["goal"] == OracleOfSeasonsGoal.option_beat_ganon:
            # Room with Zelda lying down was reached, and Ganon was beaten
            ganon_flag_offset = 0xCA9A - RAM_ADDRS["location_flags"][0]
            ganon_was_beaten = (flag_bytes[ganon_flag_offset] & 0x80 == 0x80)
            game_clear = (current_room == ROOM_ZELDA_ENDING) and ganon_was_beaten

        if game_clear:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead):
        if ctx.last_death_link > self.last_deathlink and not is_dead:
            # A death was received from another player, make our player die as well
            await bizhawk.write(ctx.bizhawk_ctx, [(RAM_ADDRS["received_item"][0], [0xFF], "System Bus")])
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
                await ctx.send_death(ctx.player_names[ctx.slot] + " might not be the Hero of Time after all.")
                self.last_deathlink = ctx.last_death_link

    async def process_tracker_updates(self, ctx: "BizHawkClientContext", flag_bytes: bytes, current_room: int):
        # Processes the gasha tracking
        local_tracker = dict(self.local_tracker)

        # Gasha handling
        byte_offset = 0xC64a - RAM_ADDRS["location_flags"][0]
        gasha_seed_bytes = flag_bytes[byte_offset] + flag_bytes[byte_offset + 1] * 0x100
        for gasha_name in GASHA_ADDRS:
            (byte_addr, flag) = GASHA_ADDRS[gasha_name]

            # Check if the seed has been harvested
            byte_offset = byte_addr - RAM_ADDRS["location_flags"][0]
            if flag_bytes[byte_offset] & 0x20:
                local_tracker[f"Harvested {gasha_name}"] = True
            else:
                # Check if the seed is currently planted
                flag_mask = 0x01 << flag
                if not gasha_seed_bytes & flag_mask:
                    continue

            local_tracker[f"Planted {gasha_name}"] = True

        # Position tracking
        local_tracker["Current Room"] = current_room

        # Beast tracking
        byte_offset = 0xc6c9 - RAM_ADDRS["location_flags"][0]
        golden_beast_data = [
            (0x01, "Octorock"),
            (0x02, "Moblin"),
            (0x04, "Darknut"),
            (0x08, "Lynel")
        ]
        golden_beast_flags = flag_bytes[byte_offset]
        for mask, name in golden_beast_data:
            if golden_beast_flags & mask:
                local_tracker[f"Golden {name} Beaten"] = True

        # Wild seed/bomb tracking
        wild_item_data = [
            (0x03, "Bombs"),
            (0x20, "Ember"),
            (0x21, "Scent"),
            (0x22, "Pegasus"),
            (0x23, "Gale"),
            (0x24, "Mystery"),
        ]
        base_offset = 0xc692 - RAM_ADDRS["location_flags"][0]
        for item_id, item_name in wild_item_data:
            byte_offset = base_offset + item_id // 8
            mask = 0x01 << item_id % 8
            if flag_bytes[byte_offset] & mask:
                local_tracker[f"Obtained {item_name}"] = True

        # Lost woods deku
        byte_offset = 0xc8b7 - RAM_ADDRS["location_flags"][0]
        if flag_bytes[byte_offset] & 0x20:
            local_tracker["Learned Lost Woods Sequence"] = True
        # Pedestal deku
        byte_offset = 0xc9f8 - RAM_ADDRS["location_flags"][0]
        if flag_bytes[byte_offset] & 0x20:
            local_tracker["Learned Pedestal Sequence"] = True

        # Blown up remains
        base_offset = 0xc6ca - RAM_ADDRS["location_flags"][0]
        blown_up_flag = 0x15
        byte_offset = base_offset + blown_up_flag // 8
        mask = 0x01 << blown_up_flag % 8
        if flag_bytes[byte_offset] & mask:
            local_tracker["Blew Up Volcano"] = True

        updates = {}
        for key, value in local_tracker.items():
            if key not in self.local_tracker or self.local_tracker[key] != value:
                updates[key] = value

        if "Current Room" in updates:
            await ctx.send_msgs([{
                "cmd": "Bounce",
                "slots": [ctx.slot],
                "data": {
                    "Current Room": current_room
                }
            }])
            del updates["Current Room"]

        if len(updates) > 0:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"OoS_{ctx.team}_{ctx.slot}",
                "default": {},
                "operations": [{
                    "operation": "update",
                    "value": updates
                }],
            }])

        self.local_tracker = local_tracker

    async def process_movelink_for_april_fools(self, ctx: "BizHawkClientContext", current_room: int):
        values = await bizhawk.read(ctx.bizhawk_ctx, [(0xD00A, 4, "System Bus"), (0xCD00, 1, "System Bus")])
        positions = values[0]
        x = positions[3] / 0x10 + positions[2] / 0x1000
        y = positions[1] / 0x10 + positions[0] / 0x1000
        now = time.time()

        if hasattr(self, "movelink_data"):
            accumulator = self.movelink_data["accumulator"]
            can_move = values[1][0] == 1 and current_room == self.movelink_data["room"]
            if self.movelink_data["position"]:
                last_x, last_y = self.movelink_data["position"]
                if can_move:  # can link move and didn't warp
                    accumulator["x"] += x - last_x
                    accumulator["y"] += y - last_y
            if now - accumulator["time"] >= 1:
                if abs(accumulator["x"]) > 0.2 or abs(accumulator["y"]) > 0.2:
                    await ctx.send_msgs([{
                        "cmd": "Bounce",
                        "tags": ["MoveLink"],
                        "data": {
                            "slot": ctx.slot,
                            "timespan": 1,
                            "x": accumulator["x"],
                            "y": accumulator["y"]
                        }
                    }])
                    self.movelink_data["accumulator"] = {"x": 0, "y": 0, "time": now}
            self.movelink_data["room"] = current_room
        else:
            self.movelink_data = {
                "position": (0, 0),
                "accumulator": {
                    "x": 0,
                    "y": 0,
                    "time": now,
                },
                "room": current_room
            }
            can_move = False

        i = 0
        has_moved = False
        while i < len(self.move_link):
            move = self.move_link[i]
            if can_move:
                proportion = (min(now, move["spoilage"]) - move["last_process"]) / move["timespan"]
                x += move["x"] * proportion
                y += move["y"] * proportion
                has_moved = True
            if now >= move["spoilage"]:
                del self.move_link[i]
            else:
                move["last_process"] = now
                i += 1

        x = int(x * 0x1000)
        y = int(y * 0x1000)

        x = max(x, 0x600)
        y = max(y, 0x600)
        if current_room < 0x400:
            x = min(x, 0x9AFF)
            y = min(y, 0x79FF)
        else:
            x = min(x, 0xEAFF)
            y = min(y, 0xA9FF)
        if can_move:
            self.movelink_data["position"] = (x / 0x1000, y / 0x1000)
        else:
            self.movelink_data["position"] = None

        if has_moved:
            await bizhawk.write(ctx.bizhawk_ctx, [(0xD00A, [y % 0x100, y // 0x100, x % 0x100, x // 0x100], "System Bus")])
