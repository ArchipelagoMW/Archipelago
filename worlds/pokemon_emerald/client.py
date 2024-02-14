from typing import TYPE_CHECKING, Dict, Set

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import BASE_OFFSET, data
from .options import Goal

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


EXPECTED_ROM_NAME = "pokemon emerald version / AP 2"

IS_CHAMPION_FLAG = data.constants["FLAG_IS_CHAMPION"]
DEFEATED_STEVEN_FLAG = data.constants["TRAINER_FLAGS_START"] + data.constants["TRAINER_STEVEN"]
DEFEATED_NORMAN_FLAG = data.constants["TRAINER_FLAGS_START"] + data.constants["TRAINER_NORMAN_1"]

# These flags are communicated to the tracker as a bitfield using this order.
# Modifying the order will cause undetectable autotracking issues.
TRACKER_EVENT_FLAGS = [
    "FLAG_DEFEATED_RUSTBORO_GYM",
    "FLAG_DEFEATED_DEWFORD_GYM",
    "FLAG_DEFEATED_MAUVILLE_GYM",
    "FLAG_DEFEATED_LAVARIDGE_GYM",
    "FLAG_DEFEATED_PETALBURG_GYM",
    "FLAG_DEFEATED_FORTREE_GYM",
    "FLAG_DEFEATED_MOSSDEEP_GYM",
    "FLAG_DEFEATED_SOOTOPOLIS_GYM",
    "FLAG_RECEIVED_POKENAV",                            # Talk to Mr. Stone
    "FLAG_DELIVERED_STEVEN_LETTER",
    "FLAG_DELIVERED_DEVON_GOODS",
    "FLAG_HIDE_ROUTE_119_TEAM_AQUA",                    # Clear Weather Institute
    "FLAG_MET_ARCHIE_METEOR_FALLS",                     # Magma steals meteorite
    "FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT",              # Clear Magma Hideout
    "FLAG_MET_TEAM_AQUA_HARBOR",                        # Aqua steals submarine
    "FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE",              # Clear Aqua Hideout
    "FLAG_HIDE_MOSSDEEP_CITY_SPACE_CENTER_MAGMA_NOTE",  # Clear Space Center
    "FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN",
    "FLAG_HIDE_SKY_PILLAR_TOP_RAYQUAZA",                # Rayquaza departs for Sootopolis
    "FLAG_OMIT_DIVE_FROM_STEVEN_LETTER",                # Steven gives Dive HM (clears seafloor cavern grunt)
    "FLAG_IS_CHAMPION",
    "FLAG_PURCHASED_HARBOR_MAIL"
]
EVENT_FLAG_MAP = {data.constants[flag_name]: flag_name for flag_name in TRACKER_EVENT_FLAGS}

KEY_LOCATION_FLAGS = [
    "NPC_GIFT_RECEIVED_HM01",
    "NPC_GIFT_RECEIVED_HM02",
    "NPC_GIFT_RECEIVED_HM03",
    "NPC_GIFT_RECEIVED_HM04",
    "NPC_GIFT_RECEIVED_HM05",
    "NPC_GIFT_RECEIVED_HM06",
    "NPC_GIFT_RECEIVED_HM07",
    "NPC_GIFT_RECEIVED_HM08",
    "NPC_GIFT_RECEIVED_ACRO_BIKE",
    "NPC_GIFT_RECEIVED_WAILMER_PAIL",
    "NPC_GIFT_RECEIVED_DEVON_GOODS_RUSTURF_TUNNEL",
    "NPC_GIFT_RECEIVED_LETTER",
    "NPC_GIFT_RECEIVED_METEORITE",
    "NPC_GIFT_RECEIVED_GO_GOGGLES",
    "NPC_GIFT_GOT_BASEMENT_KEY_FROM_WATTSON",
    "NPC_GIFT_RECEIVED_ITEMFINDER",
    "NPC_GIFT_RECEIVED_DEVON_SCOPE",
    "NPC_GIFT_RECEIVED_MAGMA_EMBLEM",
    "NPC_GIFT_RECEIVED_POKEBLOCK_CASE",
    "NPC_GIFT_RECEIVED_SS_TICKET",
    "HIDDEN_ITEM_ABANDONED_SHIP_RM_2_KEY",
    "HIDDEN_ITEM_ABANDONED_SHIP_RM_1_KEY",
    "HIDDEN_ITEM_ABANDONED_SHIP_RM_4_KEY",
    "HIDDEN_ITEM_ABANDONED_SHIP_RM_6_KEY",
    "ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_4_SCANNER",
    "ITEM_ABANDONED_SHIP_CAPTAINS_OFFICE_STORAGE_KEY",
    "NPC_GIFT_RECEIVED_OLD_ROD",
    "NPC_GIFT_RECEIVED_GOOD_ROD",
    "NPC_GIFT_RECEIVED_SUPER_ROD",
]
KEY_LOCATION_FLAG_MAP = {data.locations[location_name].flag: location_name for location_name in KEY_LOCATION_FLAGS}


class PokemonEmeraldClient(BizHawkClient):
    game = "Pokemon Emerald"
    system = "GBA"
    patch_suffix = ".apemerald"
    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_found_key_items: Dict[str, bool]
    goal_flag: int

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.goal_flag = IS_CHAMPION_FLAG

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x108, 32, "ROM")]))[0])
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
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
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["gArchipelagoInfo"], 64, "ROM")]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.slot_data is not None:
            if ctx.slot_data["goal"] == Goal.option_champion:
                self.goal_flag = IS_CHAMPION_FLAG
            elif ctx.slot_data["goal"] == Goal.option_steven:
                self.goal_flag = DEFEATED_STEVEN_FLAG
            elif ctx.slot_data["goal"] == Goal.option_norman:
                self.goal_flag = DEFEATED_NORMAN_FLAG

        try:
            # Checks that the player is in the overworld
            overworld_guard = (data.ram_addresses["gMain"] + 4, (data.ram_addresses["CB2_Overworld"] + 1).to_bytes(4, "little"), "System Bus")

            # Read save block address
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["gSaveBlock1Ptr"], 4, "System Bus")],
                [overworld_guard]
            )
            if read_result is None:  # Not in overworld
                return

            # Checks that the save block hasn't moved
            save_block_address_guard = (data.ram_addresses["gSaveBlock1Ptr"], read_result[0], "System Bus")

            save_block_address = int.from_bytes(read_result[0], "little")

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
