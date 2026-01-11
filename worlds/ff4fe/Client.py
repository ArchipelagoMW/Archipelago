import typing
import logging
from logging import Logger

from NetUtils import ClientStatus
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
        self.location_name_to_id = None
        self.key_item_names = None
        self.key_items_with_flags = None
        self.json_doc = None
        self.flags = None
        self.no_free_characters = False
        self.no_earned_characters = False
        self.junked_items = None
        self.kept_items = None
        self.logged_version = False

    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        rom_name: bytes = await snes_read(ctx, Rom.ROM_NAME, 20)
        if rom_name is None or rom_name[:3] != b"4FE":
            return False

        ctx.game = self.game
        if self.logged_version is False:
            from . import FF4FEWorld
            generation_data = await snes_read(ctx, Rom.generation_version_byte, 1)
            patching_data = await snes_read(ctx, Rom.patch_version_byte, 1)
            if generation_data is None or patching_data is None:
                return False
            generation_version = int.from_bytes(generation_data)
            patching_version = int.from_bytes(patching_data)
            snes_logger.info(f"FF4FE APWorld version v{generation_version} used for generation.")
            snes_logger.info(f"FF4FE APWorld version v{patching_version} used for patching.")
            snes_logger.info(f"FF4FE APWorld version v{FF4FEWorld.version} used for playing.")
            self.logged_version = True

        # We're not actually full remote items, but some are so we let the server know to send us all items;
        # we'll handle the ones that are actually local separately.
        ctx.items_handling = 0b111

        ctx.rom = rom_name



        return True

    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_flush_writes
        # We check victory before the connection check because victory is set in a cutscene.
        # Thus, we would no longer be in a "valid" state to send or receive items.
        if await self.connection_check(ctx) == False:
            return
        await self.location_check(ctx)
        await self.reward_check(ctx)
        await self.objective_check(ctx)
        await self.received_items_check(ctx)
        await self.resolve_key_items(ctx)
        await snes_flush_writes(ctx)

    async def connection_check(self, ctx: SNIContext):
        from SNIClient import snes_read
        rom: bytes = await snes_read(ctx, Rom.ROM_NAME, 20)
        if rom != ctx.rom:
            ctx.rom = None
            return False

        if ctx.server is None or ctx.slot is None:
            # not successfully connected to a multiworld server, cannot process the game sending items
            return False

        # Caching of useful information.
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

        if self.junked_items is None:
            junked_items_length_data = await snes_read(ctx, Rom.junked_items_length_byte, 1)
            if junked_items_length_data is None:
                return
            junked_items_array_length = junked_items_length_data[0]
            junked_items_array_data = await snes_read(ctx, Rom.junked_items_array_start, junked_items_array_length)
            if junked_items_array_data is None:
                return
            self.junked_items = []
            for item_byte in junked_items_array_data:
                item_data = [item for item in items.all_items if item.fe_id == item_byte].pop()
                self.junked_items.append(item_data.name)

        if self.kept_items is None:
            kept_items_length_data = await snes_read(ctx, Rom.kept_items_length_byte, 1)
            if kept_items_length_data is None:
                return
            kept_items_array_length = kept_items_length_data[0]
            kept_items_array_data = await snes_read(ctx, Rom.kept_items_array_start, kept_items_array_length)
            if kept_items_array_data is None:
                return
            self.kept_items = []
            for item_byte in kept_items_array_data:
                item_data = [item for item in items.all_items if item.fe_id == item_byte].pop()
                self.kept_items.append(item_data.name)


        await self.check_victory(ctx)

        # If we're not in a safe state, _don't do anything_.
        for sentinel in Rom.sentinel_addresses:
            sentinel_data = await snes_read(ctx, sentinel, 1)
            if sentinel_data is None:
                return False
            sentinel_value = sentinel_data[0]
            if sentinel_value != 0:
                return False
        # Cache the game's internal settings document.
        # This is used to track any special flags in lieu of slot data.
        if self.json_doc is None:
            await self.load_json_data(ctx)

        return True

    async def load_json_data(self, ctx: SNIContext):
        from SNIClient import snes_read
        import json
        json_length_data = await snes_read(ctx, Rom.json_doc_length_location, 4)
        if json_length_data is None:
            return
        json_length = int.from_bytes(json_length_data, "little")
        json_data = await snes_read(ctx, Rom.json_doc_location, json_length)
        if json_data is None:
            return
        self.json_doc = json.loads(json_data)
        self.flags = self.json_doc["flags"]
        flag_list = self.flags.split(" ")
        character_flags = [flags for flags in flag_list if flags[0] == "C"].pop()
        if "nofree" in character_flags:
            self.no_free_characters = True
        if "noearned" in character_flags:
            self.no_earned_characters = True


    async def location_check(self, ctx: SNIContext):
        from SNIClient import snes_read
        treasure_data = await snes_read(ctx, Rom.treasure_found_locations_start, Rom.treasure_found_size)
        if treasure_data is None:
            return False
        # Go through every treasure, and if it's been opened, find the location and send it if need be.
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
        from SNIClient import snes_read
        reward_data = await snes_read(ctx, Rom.checked_reward_locations_start, Rom.checked_reward_size)
        if reward_data is None:
            return False
        # Same as the treasure location check.
        for i in range(Rom.checked_reward_size * 8):
            byte = i // 8
            bit = i % 8
            checked = reward_data[byte] & (2 ** bit)
            if i == 1:
                checked = 1  # FE never actually flags your starting character as obtained, amazingly
            if checked > 0:
                reward_found = [reward for reward in locations.all_locations if reward.fe_id == i + 0x200]
                if len(reward_found) > 0:
                    reward_found = reward_found.pop()
                    location_id = self.location_name_to_id[reward_found.name]
                    if location_id not in ctx.locations_checked:
                        ctx.locations_checked.add(location_id)
                        snes_logger.info(
                            f'New Check: {reward_found.name} '
                            f'({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])
        if self.no_free_characters:
            for location in locations.free_character_locations:
                location_id = self.location_name_to_id[location]
                if location_id not in ctx.locations_checked:
                    ctx.locations_checked.add(location_id)
                    snes_logger.info(
                        f'New Check: {location} '
                        f'({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])
        if self.no_earned_characters:
            for location in locations.earned_character_locations:
                location_id = self.location_name_to_id[location]
                if location_id not in ctx.locations_checked:
                    ctx.locations_checked.add(location_id)
                    snes_logger.info(
                        f'New Check: {location} '
                        f'({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])


    async def objective_check(self, ctx):
        from SNIClient import snes_read
        objective_progress_data = await snes_read(ctx, Rom.objective_progress_start_location, Rom.objective_progress_size)
        if objective_progress_data is None:
            return False
        objective_count_data = await snes_read(ctx, Rom.objective_count_location, 1)
        if objective_count_data is None:
            return False
        objective_count = objective_count_data[0]
        if objective_count == 0:
            return
        objectives_needed_count_data = await snes_read(ctx, Rom.objectives_needed_count_location, 1)
        if objectives_needed_count_data is None:
            return False
        objectives_needed = objectives_needed_count_data[0]
        # Go through every FE objective, and flag it if we've done it.
        for i in range(objective_count):
            objective_progress = objective_progress_data[i]
            if objective_progress > 0:
                location_id = self.location_name_to_id[f"Objective {i + 1} Status"]
                if location_id not in ctx.locations_checked:
                    ctx.locations_checked.add(location_id)
                    snes_logger.info(
                        f'New Check: Objective {i + 1} Cleared! '
                        f'({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                    await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])
        # Check if we've cleared the required number of objectives, and send the appropriate location if so.
        # If this results in victory, that check is handled elsewhere.
        objectives_cleared = 0
        for i in range(objective_count):
            location_id = self.location_name_to_id[f"Objective {i + 1} Status"]
            if location_id in ctx.locations_checked:
                objectives_cleared += 1
        if objectives_cleared >= objectives_needed:
            location_id = self.location_name_to_id["Objectives Status"]
            if location_id not in ctx.locations_checked:
                ctx.locations_checked.add(location_id)
                reward_location_id = self.location_name_to_id["Objective Reward"]
                ctx.locations_checked.add(reward_location_id)
                snes_logger.info(
                        f'All Objectives Cleared! '
                        f'({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id, reward_location_id]}])


    async def received_items_check(self, ctx: SNIContext):
        from SNIClient import snes_buffered_write, snes_read
        items_received_data = await snes_read(ctx, Rom.items_received_location_start, Rom.items_received_size)
        if items_received_data is None:
            return
        items_received_amount = int.from_bytes(items_received_data, "big")
        if items_received_amount >= len(ctx.items_received):
            return
        inventory_data = await snes_read(ctx, Rom.inventory_start_location, Rom.inventory_size)
        if inventory_data is None:
            return
        junk_tier_data = await snes_read(ctx, Rom.junk_tier_byte, 1)
        if junk_tier_data is None:
            return
        time_is_money_data = await snes_read(ctx, Rom.sell_value_byte, 1)
        if time_is_money_data is None:
            return

        # Get all the useful data about the latest unhandled item.
        item_received = ctx.items_received[items_received_amount]
        item_received_id = item_received.item
        item_received_name = ctx.item_names.lookup_in_game(item_received_id, ctx.game)
        item_received_location_name = ctx.location_names.lookup_in_slot(item_received.location, item_received.player)
        item_received_game_data = [item for item in items.all_items if item.name == item_received_name].pop()
        item_received_game_id = item_received_game_data.fe_id
        # Characters are handled entirely ingame, for now
        if item_received_name in items.characters:
            self.increment_items_received(ctx, items_received_amount)
            return
        # Five key items require specific flags to be set in addition to existing in the inventory.
        if item_received_name in Rom.special_flag_key_items.keys():
            flag_byte = Rom.special_flag_key_items[item_received_name][0]
            flag_bit = Rom.special_flag_key_items[item_received_name][1]
            key_item_received_data = await snes_read(ctx, flag_byte, 1)
            if key_item_received_data is None:
                return
            key_item_received_value = key_item_received_data[0]
            key_item_received_value = key_item_received_value | flag_bit
            snes_buffered_write(ctx, flag_byte, bytes([key_item_received_value]))
            # The Hook doesn't actually go in the inventory, though, so it gets its own special case.
            if item_received_name == "Hook":
                self.increment_items_received(ctx, items_received_amount)
                snes_logger.info('Received %s from %s (%s)' % (
                    item_received_name,
                    ctx.player_names[item_received.player],
                    item_received_location_name))
                return
        # Any non MIAB items that come from ourself are actually local items in a trenchcoat and so we just move on,
        # since we got them ingame.
        if item_received.player == ctx.slot and item_received.location >= 0:
            if "Monster in a Box" not in item_received_location_name:
                self.increment_items_received(ctx, items_received_amount)
                return
        # Any item that hits our junk tier settings is automatically sold.
        if item_received_name in items.sellable_item_names and item_received.location >= 0:
            if self.check_junk_item(item_received_game_data, junk_tier_data[0]):
                # The Time is Money wacky prevents us from getting cash through any means other than time.
                time_is_money = False if time_is_money_data[0] != 0 else True
                # Item sale prices are capped at 127000 GP.
                item_price = min(item_received_game_data.price // 2, 127000 if not time_is_money else 0)
                current_gp_data = await snes_read(ctx, Rom.gp_byte_location, Rom.gp_byte_size)
                if current_gp_data is None:
                    return
                current_gp_amount = int.from_bytes(current_gp_data, "little")
                current_gp_amount += item_price

                lower_byte = current_gp_amount % (2**8)
                middle_byte = (current_gp_amount // (2**8)) % (2**8)
                upper_byte = current_gp_amount // (2**16)
                snes_buffered_write(ctx, Rom.gp_byte_location, bytes([lower_byte]))
                snes_buffered_write(ctx, Rom.gp_byte_location + 1, bytes([middle_byte]))
                snes_buffered_write(ctx, Rom.gp_byte_location + 2, bytes([upper_byte]))
                self.increment_items_received(ctx, items_received_amount)
                snes_logger.info('Received %s from %s (%s)' % (
                    item_received_name,
                    ctx.player_names[item_received.player],
                    item_received_location_name))
                snes_logger.info(f"Automatically sold {item_received_name} for {item_price} GP.")
                return
        # If we've made it this far, this is an item that actually goes in the inventory.
        for i, byte in enumerate(inventory_data):
            # Every other slot in the inventory data is the quantity.
            if i % 2 == 1:
                continue
            # We need a free slot or a slot that already has our item (if Unstackable wacky isn't in play)
            if inventory_data[i] == 0 or (inventory_data[i] == item_received_game_id and "unstackable" not in self.flags):
                snes_buffered_write(ctx, Rom.inventory_start_location + i, bytes([item_received_game_id]))
                if inventory_data[i] == 0:
                    snes_buffered_write(ctx,
                                        Rom.inventory_start_location + i + 1,
                                        bytes([10 if ("Arrows" in item_received_name and "unstackable" not in self.flags) else 1]))
                else:
                    item_count = inventory_data[i + 1]
                    item_count = min((item_count + 10) if "Arrows" in item_received_name else (item_count + 1), 99)
                    snes_buffered_write(ctx, Rom.inventory_start_location + i + 1, bytes([item_count]))
                self.increment_items_received(ctx, items_received_amount)

                snes_logger.info('Received %s from %s (%s)' % (
                    item_received_name,
                    ctx.player_names[item_received.player],
                    item_received_location_name))
                break

    async def check_victory(self, ctx):
        from SNIClient import snes_read
        for sentinel in Rom.sentinel_addresses: # Defend against RAM initialized to static values everywhere.
            sentinel_data = await snes_read(ctx, sentinel, 1)
            if sentinel_data is None:
                return
            sentinel_value = sentinel_data[0]
            if sentinel_value >= 0x02:
                return
        victory_data = await snes_read(ctx, Rom.victory_byte_location, 1)
        if victory_data is None:
            return
        if victory_data[0] > 0:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

    async def resolve_key_items(self, ctx):
        # We need to write key items into the ingame tracker.
        from SNIClient import snes_buffered_write, snes_read
        tracker_data = await snes_read(ctx, Rom.key_items_tracker_start_location, Rom.key_items_tracker_size)
        if tracker_data is None:
            return
        new_tracker_bytes = bytearray(tracker_data[:Rom.key_items_tracker_size])
        key_items_collected = [item.item for item in ctx.items_received
                               if item.item in self.key_item_names.values()
                               and item.item != "Pass"]
        key_items_flag_byte = None
        buffered_flag_byte = None
        for key_item in self.key_items_with_flags.keys():
            if self.key_items_with_flags[key_item] in key_items_collected:
                flag_byte = Rom.special_flag_key_items[key_item][0]
                if key_item == "Hook":
                    flag_bit = Rom.special_flag_key_items[key_item][1]
                    key_item_received_data = await snes_read(ctx, flag_byte, 1)
                    if key_item_received_data is None:
                        return
                    hook_received_value = key_item_received_data[0]
                    hook_received_value = hook_received_value | flag_bit
                    # The bitwise AND isn't an error: there's a flag that can erroneously get set that stops us from
                    # flying the airship.
                    # Which is bad.
                    hook_received_value = hook_received_value & Rom.airship_flyable_flag[1]
                    snes_buffered_write(ctx, flag_byte, bytes([hook_received_value]))
                    drill_attached_data = await snes_read(ctx, Rom.drill_attached_flag[0], 1)
                    if drill_attached_data is None:
                        return
                    drill_attached_value = drill_attached_data[0]
                    snes_buffered_write(ctx, Rom.drill_attached_flag[0], bytes([drill_attached_value | Rom.drill_attached_flag[1]]))
                elif key_items_flag_byte is None:
                    flag_bit = Rom.special_flag_key_items[key_item][1]
                    key_item_received_data = await snes_read(ctx, flag_byte, 1)
                    if key_item_received_data is None:
                        return
                    key_items_flag_byte = key_item_received_data[0]
                    key_items_flag_byte = key_items_flag_byte | flag_bit
                    buffered_flag_byte = flag_byte
                else:
                    flag_bit = Rom.special_flag_key_items[key_item][1]
                    key_items_flag_byte = key_items_flag_byte | flag_bit
        if key_items_flag_byte is not None and buffered_flag_byte is not None:
            snes_buffered_write(ctx, buffered_flag_byte, bytes([key_items_flag_byte]))
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

    def check_junk_item(self, item_received_game_data, junk_tier):
        if item_received_game_data.name in self.kept_items:
            return False
        if item_received_game_data.name in self.junked_items:
            return True
        return item_received_game_data.tier <= junk_tier


    def increment_items_received(self, ctx, items_received_amount):
        from SNIClient import snes_buffered_write
        new_count = items_received_amount + 1
        lower_byte = new_count % 256
        upper_byte = new_count // 256
        snes_buffered_write(ctx, Rom.items_received_location_start, bytes([upper_byte]))
        snes_buffered_write(ctx, Rom.items_received_location_start + 1, bytes([lower_byte]))
