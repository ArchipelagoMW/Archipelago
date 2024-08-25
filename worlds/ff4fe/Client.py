import typing
import logging
from logging import Logger

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient
from . import rom as Rom
from . import items
from . import locations

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext, snes_buffered_write
else:
    SNIContext = typing.Any

snes_logger: Logger = logging.getLogger("SNES")


class FF4FEClient(SNIClient):
    game: str = "Final Fantasy IV Free Enterprise"
    patch_suffix = ".apff4fe"
    def __init__(self):
        super()

    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        rom_name: bytes = await snes_read(ctx, Rom.ROM_NAME, 20)
        if rom_name is None or rom_name[:3] != b"4FE":
            return False

        ctx.game = self.game

        ctx.items_handling = 0b111

        ctx.rom = rom_name

        self.location_name_to_id = None
        self.key_item_names = None
        self.key_items_with_flags = None

        return True

    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        if await self.connection_check(ctx) == False:
            return
        await self.location_check(ctx)
        await self.reward_check(ctx)
        await self.check_victory(ctx)
        await self.received_items_check(ctx)
        await self.resolve_key_items(ctx)
        await snes_flush_writes(ctx)

    async def connection_check(self, ctx: SNIContext):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        rom: bytes = await snes_read(ctx, Rom.ROM_NAME, 20)
        if rom != ctx.rom:
            ctx.rom = None
            return False

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return False

        if self.location_name_to_id is None:
            from . import FF4FEWorld
            self.location_name_to_id = FF4FEWorld.location_name_to_id


        if self.key_item_names is None:
            from . import FF4FEWorld
            self.key_item_names = {item: id for item, id in FF4FEWorld.item_name_to_id.items()
                if item in items.key_item_names}

        if self.key_items_with_flags is None:
            from . import FF4FEWorld
            self.key_items_with_flags = {item: id for item, id in FF4FEWorld.item_name_to_id.items()
                if item in Rom.special_flag_key_items.keys()}

        for sentinel in Rom.sentinel_addresses:
            sentinel_data = await snes_read(ctx, sentinel, 1)
            if sentinel_data is None:
                return False
            sentinel_value = sentinel_data[0]
            if sentinel_value != 0:
                return False
        return True

    async def location_check(self, ctx: SNIContext):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        treasure_data = await snes_read(ctx, Rom.treasure_found_locations_start, Rom.treasure_found_size)
        if treasure_data is None:
            return False
        for i in range(Rom.treasure_found_size * 8):
            byte = i // 8
            bit = i % 8
            checked = treasure_data[byte] & (2**bit)
            if checked > 0:
                treasure_found = [treasure for treasure in locations.all_locations if treasure.fe_id == i]
                if len(treasure_found) > 0:
                    treasure_found = treasure_found.pop()
                    location_id = self.location_name_to_id[treasure_found.name]
                    if location_id not in ctx.locations_checked:
                        ctx.locations_checked.add(location_id)
                        snes_logger.info(
                            f'New Check: {treasure_found.name} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])


    async def reward_check(self, ctx: SNIContext):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        reward_data = await snes_read(ctx, Rom.checked_reward_locations_start, Rom.checked_reward_size)
        if reward_data is None:
            return False
        for i in range(Rom.checked_reward_size * 8):
            byte = i // 8
            bit = i % 8
            checked = reward_data[byte] & (2 ** bit)
            if checked > 0:
                reward_found = [reward for reward in locations.all_locations if reward.fe_id == i + 0x200]
                if len(reward_found) > 0:
                    reward_found = reward_found.pop()
                    location_id = self.location_name_to_id[reward_found.name]
                    if location_id not in ctx.locations_checked:
                        ctx.locations_checked.add(location_id)
                        snes_logger.info(
                            f'New Check: {reward_found.name} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])


    async def flag_check(self, ctx):
        pass

    async def received_items_check(self, ctx: SNIContext):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        items_received_data = await snes_read(ctx, Rom.items_received_location_start, Rom.items_received_size)
        if items_received_data is None:
            return
        items_received_amount = int.from_bytes(items_received_data, "big")
        if items_received_amount >= len(ctx.items_received):
            return
        inventory_data = await snes_read(ctx, Rom.inventory_start_location, Rom.inventory_size)
        if inventory_data is None:
            return

        item_received = ctx.items_received[items_received_amount]
        item_received_id = item_received.item
        item_received_name = ctx.item_names.lookup_in_game(item_received_id, ctx.game)
        item_received_game_id = [item.fe_id for item in items.all_items if item.name == item_received_name].pop()
        if item_received_name in items.characters:
            self.increment_items_received(ctx, items_received_amount)
            return
        if item_received_name in Rom.special_flag_key_items.keys():
            flag_byte = Rom.special_flag_key_items[item_received_name][0]
            flag_bit = Rom.special_flag_key_items[item_received_name][1]
            key_item_received_data = await snes_read(ctx, flag_byte, 1)
            if key_item_received_data is None:
                return
            key_item_received_value = key_item_received_data[0]
            key_item_received_value = key_item_received_value | flag_bit
            snes_buffered_write(ctx, flag_byte, bytes([key_item_received_value]))
            if item_received_name == "Hook":
                self.increment_items_received(ctx, items_received_amount)
                snes_logger.info('Received %s from %s (%s)' % (
                    item_received_name,
                    ctx.player_names[item_received.player],
                    ctx.location_names[item_received.location]))
                return
        if item_received.player == ctx.slot and item_received.location != -1:
            self.increment_items_received(ctx, items_received_amount)
            return
        for i, byte in enumerate(inventory_data):
            if i % 2 == 1:
                continue
            if inventory_data[i] == 0 or inventory_data[i] == item_received_game_id:

                snes_buffered_write(ctx, Rom.inventory_start_location + i, bytes([item_received_game_id]))
                if inventory_data[i] == 0:
                    snes_buffered_write(ctx, Rom.inventory_start_location + i + 1, bytes([1]))
                else:
                    item_count = inventory_data[i + 1]
                    item_count = min(item_count + 1, 99)
                    snes_buffered_write(ctx, Rom.inventory_start_location + i + 1, bytes([item_count]))
                self.increment_items_received(ctx, items_received_amount)

                snes_logger.info('Received %s from %s (%s)' % (
                    item_received_name,
                    ctx.player_names[item_received.player],
                    ctx.location_names[item_received.location]))
                break

        # place item
        # increment items received

    async def check_victory(self, ctx):
        from SNIClient import snes_buffered_write, snes_read
        victory_data = await snes_read(ctx, Rom.victory_byte_location, 1)
        if victory_data is None:
            return
        if victory_data[0] > 0:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
        pass

    async def resolve_key_items(self, ctx):
        from SNIClient import snes_buffered_write, snes_read
        tracker_data = await snes_read(ctx, Rom.key_items_tracker_start_location, Rom.key_items_tracker_size)
        if tracker_data is None:
            return
        new_tracker_bytes = bytearray(tracker_data[:Rom.key_items_tracker_size])
        key_items_collected = [item.item for item in ctx.items_received
                               if item.item in self.key_item_names.values()
                               and item.item != "Pass"]
        for key_item in self.key_items_with_flags.keys():
            if self.key_items_with_flags[key_item] in key_items_collected:
                flag_byte = Rom.special_flag_key_items[key_item][0]
                flag_bit = Rom.special_flag_key_items[key_item][1]
                key_item_received_data = await snes_read(ctx, flag_byte, 1)
                if key_item_received_data is None:
                    return
                key_item_received_value = key_item_received_data[0]
                key_item_received_value = key_item_received_value | flag_bit
                snes_buffered_write(ctx, flag_byte, bytes([key_item_received_value]))
        for key_item in key_items_collected:
            item_received_name = ctx.item_names.lookup_in_game(key_item, ctx.game)
            if item_received_name != "Pass":
                key_item_index = items.key_items_tracker_ids[item_received_name]
                byte = key_item_index // 8
                bit = key_item_index % 8
                new_tracker_bytes[byte] = new_tracker_bytes[byte] | (2 ** bit)
        for i in range(Rom.key_items_tracker_size):
            snes_buffered_write(ctx, Rom.key_items_tracker_start_location + i, bytes([new_tracker_bytes[i]]))
        snes_buffered_write(ctx, Rom.key_items_found_location, bytes([len(key_items_collected)]))



    def increment_items_received(self, ctx, items_received_amount):
        from SNIClient import snes_buffered_write
        new_count = items_received_amount + 1
        lower_byte = new_count % 256
        upper_byte = new_count // 256
        snes_buffered_write(ctx, Rom.items_received_location_start, bytes([upper_byte]))
        snes_buffered_write(ctx, Rom.items_received_location_start + 1, bytes([lower_byte]))