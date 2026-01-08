import time
from typing import TYPE_CHECKING, Set, Dict

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from . import LOCATIONS_DATA, ITEMS_DATA, OracleOfAgesGoal
from .Data import build_item_id_to_name_dict, build_location_name_to_id_dict

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

ROOM_ZELDA_ENDING = 0x05F1

ROM_ADDRS = {
    "game_identifier": (0x0134, 11, "ROM"),
    "slot_name": (0xFFFC0, 64, "ROM"),
}

RAM_ADDRS = {
    "game_state": (0xC2EE, 1, "System Bus"),
    "received_item_index": (0xC6A8, 2, "System Bus"),
    "received_item": (0xCBFB, 1, "System Bus"),
    "location_flags": (0xC600, 0x500, "System Bus"),

    "current_map_group": (0xCC2d, 1, "System Bus"),
    "current_map_id": (0xCC30, 1, "System Bus"),
    "is_dead": (0xCDD5, 1, "System Bus"),
}


class OracleOfAgesClient(BizHawkClient):
    game = "The Legend of Zelda - Oracle of Ages"
    system = "GBC"
    patch_suffix = ".apooa"
    local_checked_locations: Set[int]
    local_scouted_locations: Set[int]
    item_id_to_name: Dict[int, str]
    location_name_to_id: Dict[str, int]

    def __init__(self) -> None:
        super().__init__()
        self.item_id_to_name = build_item_id_to_name_dict()
        self.location_name_to_id = build_location_name_to_id_dict()
        self.local_checked_locations = set()
        self.local_scouted_locations = set()

        self.set_deathlink = False
        self.last_deathlink = None
        self.was_alive_last_frame = False
        self.is_expecting_received_death = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name != "ZELDA NAYRU":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101  # Remote items + starting inventory
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["slot_name"]]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
        pass

    def on_package(self, ctx, cmd, args):
        if cmd == 'Connected':
            if 'death_link' in args['slot_data'] and args['slot_data']['death_link']:
                self.set_deathlink = True
                self.last_deathlink = time.time()
        super().on_package(ctx, cmd, args)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        # Enable "DeathLink" tag if option was enabled
        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)

        try:
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"],            # Current state of game (is the player actually in-game?)
                RAM_ADDRS["received_item_index"],   # Number of received items
                RAM_ADDRS["received_item"],         # Received item still pending?
                RAM_ADDRS["location_flags"],        # Location flags
                RAM_ADDRS["current_map_group"],     # Current map group & id where the player is currently located
                RAM_ADDRS["current_map_id"],        # ^^^
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

            await self.process_checked_locations(ctx, flag_bytes)
            await self.process_scouted_locations(ctx, flag_bytes)

            # Process received items (only if we aren't in Blaino's Gym to prevent him from calling us cheaters)
            if received_item_is_empty:
                await self.process_received_items(ctx, num_received_items)

            if not ctx.finished_game:
                await self.process_game_completion(ctx, flag_bytes, current_room)

            if "DeathLink" in ctx.tags:
                await self.process_deathlink(ctx, is_dead)

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def process_checked_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        
        local_checked_locations = set(ctx.locations_checked)
        for name, location in LOCATIONS_DATA.items():
            if "flag_byte" not in location:
                continue

            bytes_to_test = location["flag_byte"]

            if bytes_to_test == 0xFFFF:
                continue

            if not hasattr(bytes_to_test, "__len__"):
                bytes_to_test = [bytes_to_test]

            # Check all "flag_byte" to see if location has been checked
            for byte_addr in bytes_to_test:
                byte_offset = byte_addr - RAM_ADDRS["location_flags"][0]
                bit_mask = location["bit_mask"] if "bit_mask" in location else 0x20
                if flag_bytes[byte_offset] & bit_mask == bit_mask:
                    location_id = self.location_name_to_id[name]
                    local_checked_locations.add(location_id)
                    break

        # Send locations
        if self.local_checked_locations != local_checked_locations:
            self.local_checked_locations = local_checked_locations
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(self.local_checked_locations)
            }])

    async def process_scouted_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        
        
        local_scouted_locations = set(ctx.locations_scouted)
        for name, location in LOCATIONS_DATA.items():
            if "scouting_byte" not in location or location["scouting_byte"] == 0xFFFF :
                continue

            # Check "scouting_byte" to see if map has been visited for scoutable locations
            byte_to_test = location["scouting_byte"]
            byte_offset = byte_to_test - RAM_ADDRS["location_flags"][0]
            bit_mask = location["scouting_mask"] if "scouting_mask" in location else 0x10
            if flag_bytes[byte_offset] & bit_mask == bit_mask:
                # Map has been visited, scout the location if it hasn't been already
                location_id = self.location_name_to_id[name]
                local_scouted_locations.add(location_id)

        if self.local_scouted_locations != local_scouted_locations:
            self.local_scouted_locations = local_scouted_locations
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.local_scouted_locations),
                "create_as_hint": int(2)
            }])

    async def process_received_items(self, ctx: "BizHawkClientContext", num_received_items: int):
        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        if num_received_items < len(ctx.items_received):
            next_item_name = self.item_id_to_name[ctx.items_received[num_received_items].item]
            await bizhawk.write(ctx.bizhawk_ctx, [(0xCBFB, [
                ITEMS_DATA[next_item_name]["id"],
                ITEMS_DATA[next_item_name]["subid"] if "subid" in ITEMS_DATA[next_item_name] else 0
            ], "System Bus")])

    async def process_game_completion(self, ctx: "BizHawkClientContext", flag_bytes, current_room: int):
        game_clear = False
        if ctx.slot_data is not None:
            if ctx.slot_data["goal"] == OracleOfAgesGoal.option_beat_veran:
                veran_flag_offset = 0xC6D8 - RAM_ADDRS["location_flags"][0]
                veran_was_beaten = (flag_bytes[veran_flag_offset] & 0x80 == 0x80)
                game_clear = veran_was_beaten
            elif ctx.slot_data["goal"] == OracleOfAgesGoal.option_beat_ganon:
                # Room with Zelda lying down was reached, and Ganon was beaten
                ganon_flag_offset = 0xCAF1 - RAM_ADDRS["location_flags"][0]
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
