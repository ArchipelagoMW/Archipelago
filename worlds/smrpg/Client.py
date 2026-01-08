import typing
import logging
from logging import Logger

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any
from . import Rom, Locations

snes_logger: Logger = logging.getLogger("SNES")

base_id = 850000

class SMRPGClient(SNIClient):
    game = "Super Mario RPG Legend of the Seven Stars"
    locations = Rom.location_data
    location_names = locations.keys()
    location_ids = None

    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        rom_name: bytes = await snes_read(ctx, Rom.rom_name_location, 20)
        if rom_name is None or rom_name[:4] != b"MRPG":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.rom = rom_name
        return True

    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        if await self.connection_check(ctx) == False:
            return
        await self.location_check(ctx)
        await self.received_items_check(ctx)
        await self.check_victory(ctx)
        await snes_flush_writes(ctx)

    async def connection_check(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        rom: bytes = await snes_read(ctx, Rom.rom_name_location, 20)
        if rom != ctx.rom:
            ctx.rom = None
            return False

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return False

        if self.location_ids is None:
            self.location_ids = ctx.location_names.lookup_in_game(self.location_ids)

        return await self.check_if_items_sendable(ctx)

    async def location_check(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        if not await self.check_if_items_sendable(ctx):
            return
        location_chunk_data = await snes_read(ctx, Rom.min, Rom.max - Rom.min + 32)
        if location_chunk_data is None:
            return
        for key, value in Rom.location_data.items():
            location_name = key
            location_address = value.address - Rom.min
            location_id = Locations.location_table[location_name].id + base_id
            location_data = location_chunk_data[location_address]
            if location_id not in ctx.locations_checked:
                location_data = location_data & value.bit
                if ((location_data > 0) and value.set_when_checked) \
                        or ((location_data == 0) and not value.set_when_checked):
                    ctx.locations_checked.add(location_id)
                    snes_logger.info(
                        f'New Check: {location_name} '
                        f'({len(ctx.locations_checked)}/'
                        f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])


    async def received_items_check(self, ctx):
        from SNIClient import snes_read, snes_buffered_write
        items_received_data = await snes_read(ctx, Rom.items_received_address, 2)
        if items_received_data is None:
            return
        items_received_amount = int.from_bytes(items_received_data, "little")
        if items_received_amount >= len(ctx.items_received):
            return
        if not await self.check_if_items_sendable(ctx):
            return
        item = ctx.items_received[items_received_amount]
        item_id = item.item
        item_name = ctx.item_names.lookup_in_game(item_id)
        item_data = Rom.item_data[item_name]
        item_inventory_address = 0
        max_index = 0
        write_item = False
        write_reward = False
        write_recovery = False
        item_written = False
        amount = 0
        max_value = 0
        if item_data.category == Rom.ItemCategory.item:
            item_inventory_address = Rom.items_inventory_address
            max_index = 29
            write_item = True
        elif item_data.category == Rom.ItemCategory.gear:
            item_inventory_address = Rom.gear_inventory_address
            max_index = 30
            write_item = True
        elif item_data.category == Rom.ItemCategory.key:
            item_inventory_address = Rom.keys_inventory_address
            max_index = 16
            write_item = True
        elif item_data.category == Rom.ItemCategory.coin:
            amount = item_data.id
            max_value = Rom.max_coins
            item_inventory_address = Rom.coins_address
            write_reward = True
        elif item_data.category == Rom.ItemCategory.frog_coin:
            amount = item_data.id
            max_value = Rom.max_frog_coins
            item_inventory_address = Rom.frog_coins_address
            write_reward = True
        elif item_data.category == Rom.ItemCategory.flower:
            amount = item_data.id
            max_value = Rom.max_flowers
            item_inventory_address = Rom.max_flowers_address
            write_reward = True
        elif item_data.category == Rom.ItemCategory.recovery:
            write_recovery = True
        if write_item:
            item_written = await self.write_item_to_inventory(ctx, item_data.id, item_inventory_address, max_index)
        if write_reward:
            item_written = await self.add_reward_to_count(
                ctx, amount, item_inventory_address, max_value, item_data.category != Rom.ItemCategory.flower)
        if write_recovery:
            item_written = await self.recover_characters(ctx)
        if item_written:
            snes_logger.info(f"Received {item_name}")
            self.increment_items_received(ctx, items_received_amount)

    async def check_victory(self, ctx):
        from SNIClient import snes_read
        current_music = await snes_read(ctx, Rom.items_sendable_address_2, 1)
        if current_music is None:
            return
        if current_music[0] in Rom.victory_music_values:
            ctx.locations_checked.add(Locations.location_table["Boss - Smithy Spot"].id)
        if Locations.location_table["Boss - Smithy Spot"].id in ctx.locations_checked:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    def increment_items_received(self, ctx, items_received_amount):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        items_received_amount += 1
        snes_buffered_write(ctx, Rom.items_received_address, items_received_amount.to_bytes(2, 'little'))

    async def write_item_to_inventory(self, ctx, item_id, inventory_address, max_index):
        from SNIClient import snes_buffered_write, snes_read
        current_inventory_data = await snes_read(ctx, inventory_address, max_index)
        if current_inventory_data is None:
            return
        if item_id == Rom.item_data["Alto Card"].id:
            has_alto = False
            has_tenor = False
            for index, item_byte in enumerate(current_inventory_data):
                if item_byte == Rom.item_data["Alto Card"].id:
                    has_alto = True
                if item_byte == Rom.item_data["Tenor Card"].id:
                    has_tenor = True
            if has_alto:
                item_id = Rom.item_data["Tenor Card"].id
            if has_tenor:
                item_id = Rom.item_data["Soprano Card"].id
        for index, item_byte in enumerate(current_inventory_data):
            if item_byte == 255:
                snes_buffered_write(ctx, inventory_address + index, item_id.to_bytes(1, 'little'))
                return True
        return False

    async def add_reward_to_count(self, ctx, amount, destination, max_value, coins = False):
        from SNIClient import snes_buffered_write, snes_read
        byte_count = 2 if coins else 1
        current_value_data = await snes_read(ctx, destination, byte_count)
        if current_value_data is None:
            return
        current_value = int.from_bytes(current_value_data[0:byte_count], "little")
        current_value += amount
        current_value = min(current_value, max_value)
        snes_buffered_write(ctx, destination, current_value.to_bytes(byte_count, 'little'))
        return True

    async def recover_characters(self, ctx):
        from SNIClient import snes_read, snes_buffered_write
        for character in Rom.characters:
            max_hp_data = await snes_read(ctx, Rom.hit_points[character][1], 2)
            if max_hp_data is None:
                return
            max_hp = int.from_bytes(max_hp_data, "little")
            snes_buffered_write(ctx, Rom.hit_points[character][0], max_hp.to_bytes(2, "little"))
        max_flowers_data = await snes_read(ctx, Rom.max_flowers_address, 1)
        if max_flowers_data is None:
            return
        max_flowers = int.from_bytes(max_flowers_data, "little")
        snes_buffered_write(ctx, Rom.current_flowers_address, max_flowers.to_bytes(1, "little"))
        return True

    async def check_if_items_sendable(self, ctx):
        from SNIClient import snes_read
        items_sendable_data_1 = await snes_read(ctx, Rom.items_sendable_address_1, 1)
        items_sendable_data_2 = await snes_read(ctx, Rom.items_sendable_address_2, 1)
        items_sendable_data_3 = await snes_read(ctx, Rom.items_sendable_address_3, 1)
        items_sendable_data_4 = await snes_read(ctx, Rom.items_sendable_address_4, 1)
        if items_sendable_data_1 is None \
                or items_sendable_data_2 is None \
                or items_sendable_data_3 is None \
                or items_sendable_data_4 is None:
            return False
        if items_sendable_data_1[0] == 0 \
                or items_sendable_data_2[0] in Rom.nonsendable_music_values \
                or items_sendable_data_3[0] != 0 \
                or items_sendable_data_4[0] != 0:
            return False
        return True
