import typing
import logging
from logging import Logger

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient
from . import rom as Rom
from . import items
from . import locations
from .rom import key_items_tracker_size

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
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

        ctx.items_handling = 0b101  # get sent remote and starting items

        ctx.rom = rom_name

        self.location_name_to_id = None

        return True

    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        if await self.connection_check(ctx) == False:
            return
        await self.location_check(ctx)
        await self.reward_check(ctx)
        await self.check_victory(ctx)
        await self.received_items_check(ctx)
        #await self.write_items(ctx)
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
        items_received_amount = int.from_bytes(items_received_data, "little")
        if items_received_amount >= len(ctx.items_received):
            return
        inventory_data = await snes_read(ctx, Rom.inventory_start_location, Rom.inventory_size)
        if inventory_data is None:
            return
        tracker_data = await snes_read(ctx, Rom.key_items_tracker_start_location, key_items_tracker_size)
        if tracker_data is None:
            return
        item_received = ctx.items_received[items_received_amount]
        item_received_id = item_received.item
        item_received_name = ctx.item_names.lookup_in_game(item_received_id, ctx.game)
        item_received_game_id = [item.fe_id for item in items.all_items if item.name == item_received_name].pop()
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
                snes_buffered_write(ctx, Rom.items_received_location_start, bytes([items_received_amount + 1]))
                snes_logger.info('Received %s from %s (%s)' % (
                    item_received_name,
                    ctx.player_names[item_received.player],
                    ctx.location_names[item_received.location]))
                return
        for i, byte in enumerate(inventory_data):
            if i % 2 == 1:
                continue
            if inventory_data[i] == 0 or inventory_data[i] == item_received_game_id:
                snes_buffered_write(ctx, Rom.inventory_start_location + i, bytes([item_received_game_id]))
                if inventory_data[i] == 0:
                    snes_buffered_write(ctx, Rom.inventory_start_location + i + 1, bytes([1]))
                else:
                    snes_buffered_write(ctx, Rom.inventory_start_location + i + 1, bytes([inventory_data[i + 1] + 1]))
                snes_buffered_write(ctx, Rom.items_received_location_start, bytes([items_received_amount + 1]))
                if item_received_name in items.key_item_names and item_received_name != "Pass":
                    key_item_index = items.key_items_tracker_ids[item_received_name]
                    byte = key_item_index // 8
                    bit = key_item_index % 8
                    new_tracker_byte = tracker_data[byte] | (2**bit)
                    snes_buffered_write(ctx, Rom.key_items_tracker_start_location + byte, bytes([new_tracker_byte]))
                snes_logger.info('Received %s from %s (%s)' % (
                    item_received_name,
                    ctx.player_names[item_received.player],
                    ctx.location_names[item_received.location]))
                break

        # place item
        # increment items received

    async def check_victory(self, ctx):
        pass

    async def treasure_check(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        treasure_data = await snes_read(ctx, Rom.treasure_chest_base_address, 40)

        if treasure_data is not None:
            for chest in Rom.treasure_chest_data.keys():
                treasure_byte, treasure_bit = Rom.get_treasure_chest_bit(chest)
                treasure_found = treasure_data[treasure_byte] & treasure_bit
                treasure_id = self.location_ids[chest]
                if treasure_found and treasure_id not in ctx.locations_checked:
                    ctx.locations_checked.add(treasure_id)
                    snes_logger.info(
                        f'New Check: {chest} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [treasure_id]}])

    async def received_items_check2(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        items_received_data = await snes_read(ctx, Rom.items_received_address, 2)
        if items_received_data is None:
            return
        items_received_amount = int.from_bytes(items_received_data, "little")
        if items_received_amount >= len(ctx.items_received):
            return
        event_ready_data = await snes_read(ctx, Rom.event_trigger_byte, 1)
        if event_ready_data is None:
            return
        if event_ready_data[0] != 0:
            return
        else:
            item = ctx.items_received[items_received_amount]
            item_name = ctx.item_names[item.item]
            item_id = item.item
            allow_local_network_item = False
            if item.player == ctx.slot:
                if item.location == self.location_ids["Veldt"]:
                    allow_local_network_item = True
                elif item_name not in Rom.item_name_id.keys():
                    allow_local_network_item = True
                elif item.location == -1:
                    allow_local_network_item = True
                else:
                    self.increment_items_received(ctx, items_received_amount)
                    return
            if item.player == ctx.slot and not allow_local_network_item:
                return
            if item_name in Rom.characters:
                character_index = Rom.characters.index(item_name)
                character_init_byte, character_init_bit = Rom.get_character_initialized_bit(character_index)
                character_init_data = await snes_read(ctx, character_init_byte, 1)
                if character_init_data is None:
                    return

                character_recruit_byte, character_recruit_bit = Rom.get_character_recruited_bit(character_index)
                character_recruit_data = await snes_read(ctx, character_recruit_byte, 1)
                if character_recruit_data is None:
                    return


                character_initialized = character_init_data[0] & character_init_bit
                character_recruited = character_recruit_data[0] & character_recruit_bit
                character_name = Rom.characters[character_index]
                character_ap_id = item_id
                character_item = next((item for item in ctx.items_received if item.item == character_ap_id),
                                         None)
                if character_item is not None:
                    new_init_data = character_init_data[0] | character_init_bit
                    if new_init_data == character_init_data[0]:
                        self.increment_items_received(ctx, items_received_amount)
                        return
                    self.set_dialogue_byte(ctx, item_name)
                    snes_buffered_write(ctx, Rom.event_argument_byte, bytes([character_index]))
                    snes_buffered_write(ctx, Rom.event_trigger_byte, bytes([1]))
                    snes_logger.info('Received %s from %s (%s)' % (
                        ctx.item_names[character_item.item],
                        ctx.player_names[character_item.player],
                        ctx.location_names[character_item.location]))
            elif item_name in Rom.espers:
                esper_index = Rom.espers.index(item_name)
                esper_byte, esper_bit = Rom.get_obtained_esper_bit(esper_index)
                esper_data = await snes_read(ctx, esper_byte, 1)
                if esper_data is None:
                    return
                esper_count = await snes_read(ctx, Rom.espers_obtained_address, 1)
                if esper_count is None:
                    return
                esper_count = esper_count[0]
                esper_obtained = esper_data[0] & esper_bit
                new_data = esper_data[0] | esper_bit
                self.increment_items_received(ctx, items_received_amount)
                if esper_obtained == 0:
                    self.set_dialogue_byte(ctx, item_name)
                    snes_buffered_write(ctx, Rom.event_argument_byte, bytes([esper_index]))
                    snes_buffered_write(ctx, Rom.event_trigger_byte, bytes([2]))
                snes_logger.info('Received %s from %s (%s)' % (
                    ctx.item_names[item.item],
                    ctx.player_names[item.player],
                    ctx.location_names[item.location]))

            else:
                self.set_dialogue_byte(ctx, item_name)
                snes_buffered_write(ctx, Rom.event_argument_byte, bytes([Rom.item_name_id[item_name]]))
                snes_buffered_write(ctx, Rom.event_trigger_byte, bytes([3]))
                self.increment_items_received(ctx, items_received_amount)
                snes_logger.info('Received %s from %s (%s)' % (
                    ctx.item_names[item.item],
                    ctx.player_names[item.player],
                    ctx.location_names[item.location]))

    async def check_victory1(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        formation_data = await snes_read(ctx, Rom.formation_id, 2)
        if formation_data is None:
            return
        animation_data = await snes_read(ctx, Rom.animation_byte, 1)
        if animation_data is None:
            return
        formation_value = int.from_bytes(formation_data, "little")
        animation_value = animation_data[0]
        #for now
        if formation_value == 0x0202 and animation_value == 0x01:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    async def check_victory2(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        victory_data = await snes_read(ctx, Rom.victory_address, 1)
        if victory_data is None:
            return

        victory_value = victory_data[0]
        #for now
        if victory_value & 0x02:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    def increment_items_received(self, ctx, items_received_amount):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        items_received_amount += 1
        snes_buffered_write(ctx, Rom.items_received_address, items_received_amount.to_bytes(2, 'little'))

    def set_dialogue_byte(self, ctx: SNIContext, item):
        from SNIClient import snes_buffered_write
        dialog_id = ctx.slot_data["dialogs"][item]
        snes_buffered_write(ctx, Rom.event_dialog_byte, dialog_id.to_bytes(2, 'little'))
