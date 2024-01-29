from typing import TYPE_CHECKING, Dict, Set

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient


if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

# The Canary Byte is a flag byte that is intentionally left unused. If this byte is FF, then we know the flag
# data cannot be trusted, so we don't send checks.
canary_byte = 0x20001A9

key_item_start_address = 0x20019C0

menu_byte = 0x0200027A
menu_bit_mask = 0x10

screen_transition_byte = 0x02001880
screen_transition_bit_mask = 0x10

dialog_byte = 0x02009480
dialog_bit_mask = 0x01

battle_byte = 0x020097F8
battle_bit_mask = 0x08

title_byte = 0x020097F8
title_bit_mask = 0x04

alpha_defeated_byte = 0x2000433
alpha_defeated_bit_mask = 0x01

item_index_byte = 0x20000AE

player_name_offset = 0x7FFFC0
player_name_length = 63

location_flag_offset = 0x02000000
location_flag_length = 0x434

undernet_item_bytes = {0x020019DB, 0x020019DC, 0x020019DD, 0x020019DE, 0x020019DF, 0x020019E0, 0x020019FA, 0x020019E2}
undernet_item_ids = {27, 28, 29, 30, 31, 32, 58, 34}

chip_code_start_offset = 0x8011510 # + 0x20 * chip_id
chip_start_offset = 0x02001F60 # + 0x12 * chip_id
program_start_address = 0x02001A80 # + 0x04 * program_id
sub_chip_start_address = 0x02001A30

zenny_byte = 0x20018F4
frags_byte = 0x20018F8
reg_mem_byte = 0x02001897
max_health_byte = 0x20018A2

net_shortcut_bytes = 0x2000032 #92: 0x10 93: 0x08 94: 0x20 95: 0x40


class MMBN3Client(BizHawkClient):
    game = "MegaMan Battle Network 3"
    system = "GBA"
    patch_suffix = ".apbn3"
    local_checked_locations: Set[int]
    goal_flag: int

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        ##!
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x108, 32, "ROM")]))[0])
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            """
            if not rom_name.startswith("pokemon emerald version"):
                return False
            if rom_name == "pokemon emerald version":
                logger.info("ERROR: You appear to be running an unpatched version of Pokemon Emerald. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != EXPECTED_ROM_NAME:
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your client version against the version being "
                            "used by the generator.")
                return False
            """
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(player_name_offset, player_name_length, "ROM")]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        ##!
        """
        try:
            # Read save block address
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["gSaveBlock1Ptr"], 4, "System Bus")],
                [overworld_guard]
            )
            if read_result is None:  # Not in overworld
                return

            # Handle giving the player items
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [
                    (save_block_address + 0x3778, 2, "System Bus"),                        # Number of received items
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 4, 1, "System Bus")  # Received item struct full?
                ],
                [overworld_guard, save_block_address_guard]
            )
            if read_result is None:  # Not in overworld, or save block moved
                return

            num_received_items = int.from_bytes(read_result[0], "little")
            received_item_is_empty = read_result[1][0] == 0

            # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
            # fill it with the next item
            if num_received_items < len(ctx.items_received) and received_item_is_empty:
                next_item = ctx.items_received[num_received_items]
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 0, (next_item.item - BASE_OFFSET).to_bytes(2, "little"), "System Bus"),
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 2, (num_received_items + 1).to_bytes(2, "little"), "System Bus"),
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 4, [1], "System Bus"),  # Mark struct full
                    (data.ram_addresses["gArchipelagoReceivedItem"] + 5, [next_item.flags & 1], "System Bus"),
                ])

            # Read flags in 2 chunks
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(save_block_address + 0x1450, 0x96, "System Bus")],  # Flags
                [overworld_guard, save_block_address_guard]
            )
            if read_result is None:  # Not in overworld, or save block moved
                return

            flag_bytes = read_result[0]

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(save_block_address + 0x14E6, 0x96, "System Bus")],  # Flags
                [overworld_guard, save_block_address_guard]
            )
            if read_result is not None:
                flag_bytes += read_result[0]

            game_clear = False
            local_checked_locations = set()
            local_set_events = {flag_name: False for flag_name in TRACKER_EVENT_FLAGS}
            local_found_key_items = {location_name: False for location_name in KEY_LOCATION_FLAGS}

            # Check set flags
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    if byte & (1 << i) != 0:
                        flag_id = byte_i * 8 + i

                        location_id = flag_id + BASE_OFFSET
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if flag_id == self.goal_flag:
                            game_clear = True

                        if flag_id in EVENT_FLAG_MAP:
                            local_set_events[EVENT_FLAG_MAP[flag_id]] = True

                        if flag_id in KEY_LOCATION_FLAG_MAP:
                            local_found_key_items[KEY_LOCATION_FLAG_MAP[flag_id]] = True

            # Send locations
            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations

                if local_checked_locations is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(local_checked_locations)
                    }])

            # Send game clear
            if not ctx.finished_game and game_clear:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

            # Send tracker event flags
            if local_set_events != self.local_set_events and ctx.slot is not None:
                event_bitfield = 0
                for i, flag_name in enumerate(TRACKER_EVENT_FLAGS):
                    if local_set_events[flag_name]:
                        event_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_emerald_events_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": event_bitfield}]
                }])
                self.local_set_events = local_set_events

            if local_found_key_items != self.local_found_key_items:
                key_bitfield = 0
                for i, location_name in enumerate(KEY_LOCATION_FLAGS):
                    if local_found_key_items[location_name]:
                        key_bitfield |= 1 << i

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_emerald_keys_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": key_bitfield}]
                }])
                self.local_found_key_items = local_found_key_items
        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass
        """

    async def is_in_menu(self, ctx) -> bool:
        return (await bizhawk.read(ctx.bizhawk_ctx, [(0x0200027A, 1, "System Bus")]))[0][0] & 0x10 == 0
