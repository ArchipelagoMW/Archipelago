import logging
import asyncio
import types
from typing import Dict, List, Optional, NamedTuple, TYPE_CHECKING, Set

from .Names import Addresses, ItemID, MapID
from .Names.ArchipelagoID import BASE_ID, LAIR_ID_OFFSET, NPC_REWARD_OFFSET
from .Locations import (
    SoulBlazerLocationData,
    address_for_location,
    all_locations_table,
    LocationType,
    chest_table,
    npc_reward_table,
    lair_table,
)
from .Items import SoulBlazerItemData, all_items_table
from .Util import encode_string, is_bit_set, Rectangle
from .Lair import LairData, unpack_lair_data
from .Entity import EntityData, unpack_entity_data
from NetUtils import ClientStatus, color, NetworkItem
from worlds.AutoSNIClient import SNIClient
from Utils import async_start

if TYPE_CHECKING:
    # from .Context import ItemSend, SoulBlazerContext
    from SNIClient import SNIContext


snes_logger = logging.getLogger("SNES")

STATUS_DELAY_FRAMES = 0x03


class ItemSend(NamedTuple):
    receiving: int
    item: NetworkItem


class LocationData(NamedTuple):
    map_number: int
    map_sub_number: int
    x: int
    y: int

    @property
    def map_id(self) -> int:
        return MapID.map_id_for_number[(self.map_number, self.map_sub_number)]


class SoulBlazerSNIClient(SNIClient):
    game = "Soul Blazer"
    patch_suffix = ".apsb"

    location_data_for_address = {data.address: data for data in all_locations_table.values()}
    item_data_for_code = {data.code: data for data in all_items_table.values()}

    def __init__(self) -> None:
        super().__init__()
        self.lair_data: List[LairData] = []
        self.entity_list: List[EntityData] = []
        self.lairs_for_map: Dict[int, Set[int]] = {}
        self.lairs_rom_name: bytes = bytes(0)

    async def was_obtained_locally(self, ctx, item: NetworkItem) -> bool:
        """True if the item was a local item that has already been obtained."""

        from SNIClient import snes_read

        # If it came from someone else, then we couldn't have got it locally.
        if item.player != ctx.slot:
            return False

        location_data = self.location_data_for_address.get(item.location)
        # I dont think this should ever happen.
        if location_data is None:
            return False

        if location_data.type == LocationType.CHEST:
            flag_index = Addresses.CHEST_FLAG_INDEXES[location_data.id]
            chest_data = await snes_read(ctx, Addresses.CHEST_OPENED_TABLE, (flag_index // 8) + 1)
            return is_bit_set(chest_data, flag_index)
        if location_data.type == LocationType.NPC_REWARD:
            npc_data = await snes_read(ctx, Addresses.NPC_REWARD_TABLE, (location_data.id // 8) + 1)
            return is_bit_set(npc_data, location_data.id)
        if location_data.type == LocationType.LAIR:
            lair_byte = await snes_read(ctx, Addresses.LAIR_SPAWN_TABLE + location_data.id, 1)
            return lair_byte[0] & 0x80

    def is_in_excluded_zone(self, location: LocationData, lair_state_table: bytes) -> bool:
        """True if player is in a location that should not allow items to be received."""

        return any(rect.contains(location.x, location.y) for rect in exclusion_zones.get(location.map_id, [])) or any(
            self.is_lair_in_progress(lair_id, lair_state_table) for lair_id in self.lairs_for_map[location.map_id]
        )

    def is_lair_in_progress(self, lair_id: int, lair_state_table: bytes) -> bool:
        """Returns true if a lair is in the progress of being sealed"""

        lair_state = lair_state_table[lair_id]

        # First check if lair sealed or cleared.
        if bool(lair_state & 0x80) or lair_state & 0x3F == 0:
            return False

        # Boss Lairs are always in progress while the lair is active.
        if lair_id in boss_lair_ids:
            return True

        max_enemies = lair_state & 0x3F

        lair_entity = next(
            (x for x in self.entity_list if x.parent_entity == 0 and x.lair_assotiated_with == lair_id), None
        )

        # I dont think should be able to happen.
        if lair_entity is None:
            return False

        # Regular lairs are in progress if at least one enemy in the lair has been killed.
        return lair_entity.loop_counter < max_enemies

    async def deathlink_kill_player(self, ctx):
        pass
        # TODO: Handle Receiving Deathlink

    async def validate_rom(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read, SNIContext

        rom_name = await snes_read(ctx, Addresses.SNES_ROMNAME_START, Addresses.ROMNAME_SIZE)
        if rom_name is None or rom_name == bytes([0] * Addresses.ROMNAME_SIZE) or rom_name[:3] != b"SB_":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items

        ctx.rom = rom_name

        ctx.want_slot_data = True

        # This is pretty hacky, but I cant figure out a way to get this data otherwise.
        def new_on_package(self: SNIContext, cmd: str, args: dict):
            """Custom package handling for Soul Blazer."""
            # Run the original on_package
            SNIContext.on_package(self, cmd, args)

            if cmd in {"Connected", "RoomUpdate"}:
                slot_data = args.get("slot_data", None)
                if slot_data:
                    self.gem_data = slot_data.get("gem_data", {})
                    self.exp_data = slot_data.get("exp_data", {})
            elif cmd == "Retrieved":
                slot_data = args["keys"].get(f"_read_slot_data_{self.slot}", None)
                if slot_data:
                    self.gem_data = slot_data.get("gem_data", {})
                    self.exp_data = slot_data.get("exp_data", {})
            elif cmd == "PrintJSON":
                # We want ItemSends from us to another player so we can print them in game
                if (
                    args.get("type", "") == "ItemSend"
                    and args["receiving"] != self.slot
                    and args["item"].player == self.slot
                ):
                    if not hasattr(self, "item_send_queue"):
                        self.item_send_queue = []
                    self.item_send_queue.append(ItemSend(args["receiving"], args["item"]))

        # Replace the on_package function on our context's instance only.
        ctx.on_package = types.MethodType(new_on_package, ctx)

        # death_link = await snes_read(ctx, DEATH_LINK_ACTIVE_ADDR, 1)
        ## TODO: Handle Deathlink
        # if death_link:
        #    ctx.allow_collect = bool(death_link[0] & 0b100)
        #    await ctx.update_death_link(bool(death_link[0] & 0b1))

        return True

    async def game_watcher(self, ctx: "SNIContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # TODO: Handle Deathlink

        rom = await snes_read(ctx, Addresses.SNES_ROMNAME_START, Addresses.ROMNAME_SIZE)
        if rom != ctx.rom:
            # Rom is no longer loaded.
            ctx.rom = None
            return

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return

        # Only read lair data once per rom.
        if self.lairs_rom_name != rom:
            lair_bytes = await snes_read(ctx, Addresses.LAIR_DATA, Addresses.LAIR_DATA_SIZE * Addresses.LAIRS_COUNT)
            if lair_bytes is None:
                return False
            self.lair_data = unpack_lair_data(lair_bytes)
            self.lairs_for_map = {
                map: {id for id, lair in enumerate(self.lair_data) if lair.lair_map == map}
                for map in MapID.map_number_for_id.keys()
            }
            self.lairs_rom_name = rom

        save_file_name = await snes_read(ctx, Addresses.PLAYER_NAME, Addresses.PLAYER_NAME_SIZE)
        if save_file_name is None or save_file_name[0] == 0x00 or save_file_name[-1] != 0x00:
            # We haven't loaded a save file
            return

        ram_misc_start = Addresses.EVENT_FLAGS_WIN
        ram_misc_end = Addresses.NPC_REWARD_TABLE + Addresses.NPC_REWARD_TABLE_SIZE
        # Misc values in LowRAM
        ram_misc = await snes_read(ctx, ram_misc_start, ram_misc_end - ram_misc_start + 1)
        ram_lair_spawn = await snes_read(ctx, Addresses.LAIR_SPAWN_TABLE, Addresses.LAIR_SPAWN_TABLE_SIZE)

        location_data_start = Addresses.MAP_NUMBER
        location_data_end = Addresses.POSITION_INT_Y
        # We need to know which map the player is on, and what their X/Y coords are.
        location_data = await snes_read(ctx, location_data_start, location_data_end - location_data_start + 1)

        # 4k bytes. Hopefully not too much to read.
        entity_bytes = await snes_read(ctx, Addresses.ENTITIES_TABLE, Addresses.ENTITY_SIZE * Addresses.ENTITY_COUNT)

        if (
            ram_misc is None
            or ram_lair_spawn is None
            or ram_lair_spawn is None
            or location_data is None
            or entity_bytes is None
        ):
            return

        self.entity_list = unpack_entity_data(entity_bytes)

        player_location = LocationData(
            location_data[Addresses.MAP_NUMBER - location_data_start],
            location_data[Addresses.MAP_SUB_NUMBER - location_data_start],
            location_data[Addresses.POSITION_INT_X - location_data_start],
            location_data[Addresses.POSITION_INT_Y - location_data_start],
        )

        # Any new checks?

        # Chests
        new_checks: List[int] = [
            loc.address
            for loc in chest_table.values()
            if is_bit_set(ram_misc, Addresses.CHEST_FLAG_INDEXES[loc.id], Addresses.CHEST_OPENED_TABLE - ram_misc_start)
            and loc.address not in ctx.locations_checked
        ]

        # NPC Rewards
        new_checks += [
            loc.address
            for loc in npc_reward_table.values()
            if is_bit_set(ram_misc, loc.id, Addresses.NPC_REWARD_TABLE - ram_misc_start)
            and loc.address not in ctx.locations_checked
        ]

        # Lairs
        new_checks += [
            loc.address
            for loc in lair_table.values()
            # Last bit set means the location has been checked.
            if ram_lair_spawn[loc.id] & 0x80 and loc.address not in ctx.locations_checked
        ]

        # Did we win?
        has_victory = is_bit_set(ram_misc, Addresses.EVENT_FLAGS_WIN_BIT, Addresses.EVENT_FLAGS_WIN - ram_misc_start)

        verify_save_file_name = await snes_read(ctx, Addresses.PLAYER_NAME, Addresses.PLAYER_NAME_SIZE)
        if (
            verify_save_file_name is None
            or verify_save_file_name[0] == 0x00
            or verify_save_file_name[-1] != 0x00
            or verify_save_file_name != save_file_name
        ):
            # We have somehow exited the save file (or worse)
            ctx.rom = None
            return

        rom = await snes_read(ctx, Addresses.SNES_ROMNAME_START, Addresses.ROMNAME_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            # We have somehow loaded a different ROM
            return

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            snes_logger.info(
                f"New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})"
            )

        async_start(ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}]))

        if has_victory and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        # Check if there are any queued item sends that we are ready to display.
        if not hasattr(ctx, "item_send_queue"):
            ctx.item_send_queue = []

        if bool(ctx.item_send_queue):
            tx_status = await snes_read(ctx, Addresses.TX_STATUS, 1)
            if tx_status is not None and tx_status[0] == STATUS_DELAY_FRAMES:
                send = ctx.item_send_queue.pop(0)
                player_name = encode_string(ctx.player_names[send.receiving], Addresses.TX_ADDRESSEE_SIZE)
                item_name = encode_string(ctx.item_names[send.item.item], Addresses.TX_NAME_SIZE)
                snes_buffered_write(ctx, Addresses.TX_ADDRESSEE, player_name)
                snes_buffered_write(ctx, Addresses.TX_ITEM_NAME, item_name)
                await snes_flush_writes(ctx)
                # Write to Status last to ensure all the data is placed before signaling ready.
                snes_buffered_write(ctx, Addresses.TX_STATUS, bytes([STATUS_DELAY_FRAMES + 1]))
                await snes_flush_writes(ctx)

        # Receive items if possible
        if not hasattr(ctx, "gem_data") or not hasattr(ctx, "exp_data"):
            # We dont have slot data yet, try requesting it and return.
            async_start(ctx.send_msgs([{"cmd": "Get", "locations": [f"_read_slot_data_{ctx.slot}"]}]))
            return

        # Only ever prepare to send things when the game is ready to receive first since otherwise the index might be out of sync.
        rx_status = await snes_read(ctx, Addresses.RX_STATUS, 1)
        if rx_status is None or rx_status[0] != STATUS_DELAY_FRAMES:
            return

        # Game is ready to receive and receive index is in a stable state.
        recv_bytes = await snes_read(ctx, Addresses.RECEIVE_COUNT, 2)
        if recv_bytes is None:
            return

        recv_index = int.from_bytes(recv_bytes, "little")
        # Check if there are items that the Client knows about that the game does not have yet.
        if recv_index < len(ctx.items_received) and not self.is_in_excluded_zone(player_location, ram_lair_spawn):
            item = ctx.items_received[recv_index]

            if await self.was_obtained_locally(ctx, item):
                # Item was already obtained locally, but receive count was not incremented.
                # snes_logger.info(
                #    f"Item was obtained locally. Incrementing receive count from {recv_index} to {recv_index+1}"
                # )
                recv_index += 1
                snes_buffered_write(ctx, Addresses.RECEIVE_COUNT, recv_index.to_bytes(2, "little"))
                await snes_flush_writes(ctx)
                return

            # TODO: Should we also mark the location as checked in game if it was in our world and we were getting it again from the server?
            # This would remove the need to recheck things in case of resetting without saving, but you would lose out on lair monster exp.
            player_name = encode_string(ctx.player_names[item.player], Addresses.RX_SENDER_SIZE)
            item_data = self.item_data_for_code[item.item]
            operand = item_data.operand_for_id
            if item_data.id == ItemID.GEMS:
                operand = ctx.gem_data.get(f"{item.item}:{item.location}:{item.player}", operand)
            if item_data.id == ItemID.EXP:
                operand = ctx.exp_data.get(f"{item.item}:{item.location}:{item.player}", operand)

            snes_buffered_write(ctx, Addresses.RX_INCREMENT, bytes([0x01]))
            snes_buffered_write(ctx, Addresses.RX_ID, item_data.id.to_bytes(1, "little"))
            snes_buffered_write(ctx, Addresses.RX_OPERAND, operand.to_bytes(2, "little"))
            snes_buffered_write(ctx, Addresses.RX_SENDER, player_name)
            await snes_flush_writes(ctx)
            # Write to Status last to ensure all the data is placed before signaling ready.
            snes_buffered_write(ctx, Addresses.RX_STATUS, bytes([STATUS_DELAY_FRAMES + 1]))
            await snes_flush_writes(ctx)

            if item.player == ctx.slot:
                ctx.locations_checked.add(item.location)


exclusion_zones = {
    # Lost side marsh rafts
    # If this goes well we could do this for other tricky locations too like the dolphin ride.
    # Or if we can find a cleaner way that doesnt involve defining all these excluded regions then we dont have to do this.
    # TODO: Give names to MapIDs somewhere.
    # TODO: Rafts no longer required I think since the game no longer processes things while directional movement is disabled.
    # TODO: Might still want to exclude the Lost side marsh island so you dont have to take the gem fairy back to town.
    # TODO: Exclude the ice patches if you dont have the mushroom shoes equipped?
    0x19: [
        Rectangle(0x0F, 0x11, 0x01, 0x09),
        Rectangle(0x05, 0x0E, 0x07, 0x01),
        Rectangle(0x09, 0x17, 0x0F, 0x01),
        Rectangle(0x1C, 0x0A, 0x01, 0x09),
        Rectangle(0x05, 0x06, 0x13, 0x01),
        # We could also do the island, but the crystal is there to let you go home.
    ],
    # Boss arena of Deathtoll's Shrine.
    0x7C: [Rectangle(0x00, 0x00, 0x0F, 0x0F)],
    # Final Battle, the entire possible area.
    0x7C: [Rectangle(0x00, 0x00, 0xFF, 0xFF)],
}

boss_lair_maps = {0x0C, 0x22, 0x32, 0x44, 0x59, 0x72}
boss_lair_ids = {0x0009, 0x0050, 0x00B6, 0x0103, 0x012F, 0x0195}
