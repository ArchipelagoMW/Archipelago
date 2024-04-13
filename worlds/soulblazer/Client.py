import logging
import asyncio
from typing import Dict, List, Optional, NamedTuple, TYPE_CHECKING

from .Names import Addresses, ItemID
from .Names.ArchipelagoID import base_id, lair_id_offset, npc_reward_offset
from .Locations import (
    SoulBlazerLocationData,
    all_locations_table,
    LocationType,
    chest_table,
    npc_reward_table,
    lair_table,
)
from .Items import SoulBlazerItemData, all_items_table
from NetUtils import ClientStatus, color, NetworkItem
from worlds.AutoSNIClient import SNIClient

if TYPE_CHECKING:
    from .Context import ItemSend, SoulBlazerContext

snes_logger = logging.getLogger("SNES")


def address_for_location(type: LocationType, id: int) -> int:
    if type == LocationType.LAIR:
        return base_id + lair_id_offset + id
    if type == LocationType.NPC_REWARD:
        return base_id + npc_reward_offset + id
    return base_id + id


def is_bit_set(data: bytes, offset: int, index: int) -> bool:
    return data[offset + (index // 8)] & 1 << (index % 8)


def encode_string(string: str, buffer_length: int) -> bytes:
    # TODO: Also replace ascii chars missing from Soul Blazer's charmap
    return string[:buffer_length].encode("ascii", "replace") + bytes([0x00])


class SoulBlazerSNIClient(SNIClient):
    game = "Soul Blazer"
    patch_suffix = ".apsb"

    location_data_for_address = {data.address: data for data in all_locations_table.values()}
    item_data_for_code = {data.code: data for data in all_items_table.values()}

    # async def is_location_checked(self, ctx, location: int) -> bool:
    #    """Returns True if the location is a local location which has been checked already indicating that the item has already been handled locally."""
    #    # TODO: Should we also mark the location as checked if it was in our world and we were getting it again from the server?
    #    from SNIClient import snes_read
    #
    #    location_data = self.location_data_for_address.get(location)
    #    if location_data is None:
    #        return False
    #
    #    if location_data.type == LocationType.CHEST:
    #        flag_index = Addresses.CHEST_FLAG_INDEXES[location_data.id]
    #        chest_data = await snes_read(ctx, Addresses.CHEST_OPENED_TABLE, (flag_index // 8) + 1)
    #        return is_bit_set(chest_data, 0, flag_index)
    #    if location_data.type == LocationType.NPC_REWARD:
    #        npc_data = await snes_read(ctx, Addresses.NPC_REWARD_TABLE, (location_data.id // 8) + 1)
    #        return is_bit_set(npc_data, 0, location_data.id)
    #    if location_data.type == LocationType.LAIR:
    #        lair_byte = await snes_read(ctx, Addresses.LAIR_SPAWN_TABLE + location_data.id, 1)
    #        return lair_byte[0] & 0x80

    async def was_obtained_locally(self, ctx, item: NetworkItem) -> bool:
        """Returns True if the item was a local item that has already been obtained."""

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
            return is_bit_set(chest_data, 0, flag_index)
        if location_data.type == LocationType.NPC_REWARD:
            npc_data = await snes_read(ctx, Addresses.NPC_REWARD_TABLE, (location_data.id // 8) + 1)
            return is_bit_set(npc_data, 0, location_data.id)
        if location_data.type == LocationType.LAIR:
            lair_byte = await snes_read(ctx, Addresses.LAIR_SPAWN_TABLE + location_data.id, 1)
            return lair_byte[0] & 0x80

    async def deathlink_kill_player(self, ctx):
        pass
        # TODO: Handle Receiving Deathlink

    async def validate_rom(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        from .Context import SoulBlazerContext

        rom_name = await snes_read(ctx, Addresses.SNES_ROMNAME_START, Addresses.ROMNAME_SIZE)
        if rom_name is None or rom_name == bytes([0] * Addresses.ROMNAME_SIZE) or rom_name[:3] != b"SB_":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items

        ctx.rom = rom_name

        ctx.want_slot_data = True
        # This feels hacky, but I cant figure out any other way to get the context to expose slot data.
        if ctx.__class__ != SoulBlazerContext:
            ctx.__class__ = SoulBlazerContext
            ctx.gem_data = {}
            ctx.exp_data = {}
            ctx.item_send_queue = []
            await ctx.send_msgs([{"cmd": "GetDataPackage", "games": ["Soul Blazer"]}])

        # death_link = await snes_read(ctx, DEATH_LINK_ACTIVE_ADDR, 1)
        ## TODO: Handle Deathlink
        # if death_link:
        #    ctx.allow_collect = bool(death_link[0] & 0b100)
        #    await ctx.update_death_link(bool(death_link[0] & 0b1))
        return True

    async def game_watcher(self, ctx: "SoulBlazerContext"):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # TODO: Handle Deathlink

        save_file_name = await snes_read(ctx, Addresses.PLAYER_NAME, Addresses.PLAYER_NAME_SIZE)
        if save_file_name is None or save_file_name[0] == 0x00:
            # We haven't loaded a save file
            return

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return

        ram_misc_start = Addresses.EVENT_FLAGS_WIN
        ram_misc_end = Addresses.NPC_REWARD_TABLE + Addresses.NPC_REWARD_TABLE_SIZE
        # Misc values in LowRAM
        ram_misc = await snes_read(ctx, ram_misc_start, ram_misc_end - ram_misc_start + 1)
        ram_lair_spawn = await snes_read(ctx, Addresses.LAIR_SPAWN_TABLE, Addresses.LAIR_SPAWN_TABLE_SIZE)

        if ram_misc is None or ram_lair_spawn is None:
            return

        # Any new checks?

        # Chests
        new_checks: List[int] = [
            loc.address
            for loc in chest_table.values()
            if is_bit_set(ram_misc, Addresses.CHEST_OPENED_TABLE - ram_misc_start, Addresses.CHEST_FLAG_INDEXES[loc.id])
            and loc.address not in ctx.locations_checked
        ]

        # NPC Rewards
        new_checks += [
            loc.address
            for loc in npc_reward_table.values()
            if is_bit_set(ram_misc, Addresses.NPC_REWARD_TABLE - ram_misc_start, loc.id)
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
        has_victory = is_bit_set(ram_misc, Addresses.EVENT_FLAGS_WIN - ram_misc_start, Addresses.EVENT_FLAGS_WIN_BIT)

        verify_save_file_name = await snes_read(ctx, Addresses.PLAYER_NAME, Addresses.PLAYER_NAME_SIZE)
        if verify_save_file_name is None or verify_save_file_name[0] == 0x00 or verify_save_file_name != save_file_name:
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

        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])

        if has_victory and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        # Check if there are any queued item sends that we are ready to display.
        if bool(ctx.item_send_queue):
            tx_status = await snes_read(ctx, Addresses.TX_STATUS, 1)
            if tx_status is not None and tx_status[0] == 0x01:
                send = ctx.item_send_queue.pop(0)
                player_name = encode_string(ctx.player_names[send.receiving], Addresses.TX_ADDRESSEE_SIZE)
                item_name = encode_string(ctx.item_names[send.item.item], Addresses.TX_NAME_SIZE)
                snes_buffered_write(ctx, Addresses.TX_ADDRESSEE, player_name)
                snes_buffered_write(ctx, Addresses.TX_ITEM_NAME, item_name)
                # Write to Status last to ensure all the data is placed before signaling ready.
                snes_buffered_write(ctx, Addresses.TX_STATUS, bytes([0x02]))
                await snes_flush_writes(ctx)

        # TODO: also prevent receiving NPC unlocks when in a boss room to prevent the boss from regenerating to full health. Can happen either in the ROM or client, whichever is easiest to implement.
        recv_bytes = await snes_read(ctx, Addresses.RECEIVE_COUNT, 2)
        if recv_bytes is None:
            return

        recv_index = int.from_bytes(recv_bytes, "little")
        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            rx_status = await snes_read(ctx, Addresses.RX_STATUS, 1)
            if rx_status is not None and rx_status[0] == 0x01 and not await self.was_obtained_locally(ctx, item):
                # TODO: Should we also mark the location as checked if it was in our world and we were getting it again from the server?
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
                # Write to Status last to ensure all the data is placed before signaling ready.
                snes_buffered_write(ctx, Addresses.RX_STATUS, bytes([0x02]))
                await snes_flush_writes(ctx)

                if item.player == ctx.slot:
                    ctx.locations_checked.add(item.location)

        # TODO: Anything else?
