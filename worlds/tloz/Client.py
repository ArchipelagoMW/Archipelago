import logging
from copy import deepcopy
from typing import TYPE_CHECKING, List

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from worlds.tloz import Rom, Locations, Items

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


base_id = 7000
logger = logging.getLogger("Client")

class TLOZClient(BizHawkClient):
    game = "The Legend of Zelda"
    system = "NES"
    patch_suffix = ".aptloz"

    def __init__(self):
        self.wram = "RAM"
        self.sram = "WRAM"
        self.rom = "PRG ROM"
        self.bonus_items = []
        self.major_location_offsets = None
        self.guard_list = [(Rom.game_mode, [0x05], self.wram)] # 0x05 is normal gameplay in overworld or dungeon


    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(Rom.ROM_NAME - 0x10, 3, self.rom)]))[0]).decode("ascii")
            logger.info(rom_name)
            if rom_name != "LOZ":
                return False  # Not a MYGAME ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        # This is a MYGAME ROM
        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        if ctx.slot is None:
            return
        try:
            if self.major_location_offsets is None:
                location_offsets = await self.read_rom(ctx, 0x40, 4)
                location_offsets = bytearray(location_offsets)
                starting_sword_cave_location = location_offsets[0]
                white_sword_pond_location = location_offsets[1]
                magical_sword_grave_location = location_offsets[2]
                letter_cave_location = location_offsets[3]
                self.major_location_offsets = deepcopy(Locations.major_location_offsets)
                self.major_location_offsets["Starting Sword Cave"] = starting_sword_cave_location
                self.major_location_offsets["White Sword Pond"] = white_sword_pond_location
                self.major_location_offsets["Magical Sword Grave"] = magical_sword_grave_location
                self.major_location_offsets["Letter Cave"] = letter_cave_location
            await self.check_victory(ctx)
            await self.location_check(ctx)
            await self.received_items_check(ctx)
            await self.resolve_shop_items(ctx)
            await self.resolve_triforce_fragments(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def check_victory(self, ctx):
        game_mode = await self.read_ram_value(ctx, Rom.game_mode)
        if game_mode == 19 and ctx.finished_game == False:
            await ctx.send_msgs([
                {"cmd": "StatusUpdate",
                 "status": ClientStatus.CLIENT_GOAL}
            ])

    async def location_check(self, ctx):
        locations_checked = []
        overworld_data = await self.read_ram_values_guarded(ctx, Rom.overworld_status_block, 0x80)
        underworld_early_data = await self.read_ram_values_guarded(ctx, Rom.underworld_early_status_block, 0x80)
        underworld_late_data = await self.read_ram_values_guarded(ctx, Rom.underworld_late_status_block, 0x80)
        if overworld_data is None or underworld_early_data is None or underworld_late_data is None:
            return
        for location, index in self.major_location_offsets.items():
            if (int(overworld_data[index]) & 0x10) > 0:
                locations_checked.append(Locations.location_table[location])
        for location, index in Locations.floor_location_game_offsets_early.items():
            if (int(underworld_early_data[index]) & 0x10 > 0):
                locations_checked.append(Locations.location_table[location])
        for location, index in Locations.floor_location_game_offsets_late.items():
            if (int(underworld_late_data[index]) & 0x10 > 0):
                locations_checked.append(Locations.location_table[location])

        left_shop_slots = await self.read_ram_value_guarded(ctx, Rom.left_shop_slots)
        middle_shop_slots = await self.read_ram_value_guarded(ctx, Rom.middle_shop_slots)
        right_shop_slots = await self.read_ram_value_guarded(ctx, Rom.right_shop_slots)
        if left_shop_slots is None or middle_shop_slots is None or right_shop_slots is None:
            return
        shop_slots = {"Left": left_shop_slots, "Middle": middle_shop_slots, "Right": right_shop_slots}
        for name, shop in shop_slots.items():
            if shop & Rom.arrow_shop > 0:
                locations_checked.append(Locations.location_table[f"Arrow Shop Item {name}"])
            if shop & Rom.candle_shop > 0:
                locations_checked.append(Locations.location_table[f"Candle Shop Item {name}"])
            if shop & Rom.shield_shop > 0:
                locations_checked.append(Locations.location_table[f"Shield Shop Item {name}"])
            if shop & Rom.ring_shop > 0:
                locations_checked.append(Locations.location_table[f"Blue Ring Shop Item {name}"])
            if shop & Rom.potion_shop > 0:
                locations_checked.append(Locations.location_table[f"Potion Shop Item {name}"])
            if shop & Rom.take_any > 0:
                locations_checked.append(Locations.location_table[f"Take Any Item {name}"])
        take_any_caves_checked = await self.read_ram_value_guarded(ctx, Rom.take_any_caves_checked)
        if take_any_caves_checked is None:
            return
        if take_any_caves_checked >= 4:
            if "Take Any Item Left" not in ctx.checked_locations:
                locations_checked.append(Locations.location_table[f"Take Any Item Left"])
                self.bonus_items.append(ctx.slot_data["TakeAnyLeft"])
            if "Take Any Item Middle" not in ctx.checked_locations:
                locations_checked.append(Locations.location_table[f"Take Any Item Left"])
                self.bonus_items.append(ctx.slot_data["TakeAnyMiddle"])
            if "Take Any Item Right" not in ctx.checked_locations:
                locations_checked.append(Locations.location_table[f"Take Any Item Left"])
                self.bonus_items.append(ctx.slot_data["TakeAnyRight"])
        for location in locations_checked:
            if location not in ctx.locations_checked:
                ctx.locations_checked.add(location)
                location_name = ctx.location_names.lookup_in_game(location)
                logger.info(
                    f'New Check: {location_name} ({len(ctx.locations_checked)}/'
                    f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location]}])



    async def received_items_check(self, ctx):
        items_received_count_low = await self.read_ram_value_guarded(ctx, Rom.items_obtained_low)
        items_received_count_high = await self.read_ram_value_guarded(ctx, Rom.items_obtained_high)
        if items_received_count_low is None or items_received_count_high is None:
            return
        items_received_count = list([items_received_count_low, items_received_count_high])
        items_received_count_value = int.from_bytes(items_received_count, "little")
        if items_received_count_value < len(ctx.items_received):
            current_item = ctx.items_received[items_received_count_value]
            current_item_id = current_item.item
            current_item_name = ctx.item_names.lookup_in_game(current_item_id, ctx.game)
            items_received_count_value += 1
            new_items_received_count_low = items_received_count_value % 256
            new_items_received_count_high = items_received_count_value // 256
            new_items_received_count_low_write = (Rom.items_obtained_low, [new_items_received_count_low], self.wram)
            new_items_received_count_high_write = (Rom.items_obtained_high, [new_items_received_count_high], self.wram)
            write_list: List[tuple[int, List[int], str]] = [new_items_received_count_low_write, new_items_received_count_high_write]
            await self.write_item(ctx, current_item_name, write_list)

    async def resolve_shop_items(self, ctx):
        pass

    async def resolve_triforce_fragments(self, ctx):
        current_triforce_count = await self.read_ram_value_guarded(ctx, Rom.triforce_count)
        if current_triforce_count is None:
            return
        current_triforce_byte = 0xFF >> (8 - min(current_triforce_count, 8))
        write_list = [(Rom.triforce_fragments, [current_triforce_byte], self.wram)]
        await self.write(ctx, write_list)

    async def write_item(self, ctx, item_name, write_list: List[tuple[int, List[int], str]]):
        item_game_id = Items.item_game_ids[item_name]
        if item_name == "Bomb":
            item_game_id = 0x29 # Hack to allow bombs to be shown being lifted.
        lift_write = (Rom.item_to_lift, [item_game_id], self.wram)
        timer_write = (Rom.item_lift_timer, [128], self.wram) # 128 frames of lifting an item
        sound_write = (Rom.sound_effect_queue, [4], self.wram) # "Found secret" sound
        write_list.extend([lift_write, timer_write, sound_write])
        await self.handle_item(ctx, item_name, write_list)

    async def resolve_bonus_items(self, ctx):
        for item in self.bonus_items:
            current_item_name = ctx.item_names.lookup_in_game(item, ctx.game)
            await self.write_item(ctx, current_item_name, [])
        self.bonus_items.clear()

    async def handle_item(self, ctx, item_name, write_list: List[tuple[int, List[int], str]]):
        # No nice way to do this, since basically every item needs to be handled a little differently.
        if item_name == "Sword":
            current_sword_value = await self.read_ram_value_guarded(ctx, Rom.sword)
            if current_sword_value is None:
                return
            write_list.append((Rom.sword, [max(1, current_sword_value)], self.wram))
        elif item_name == "White Sword":
            current_sword_value = await self.read_ram_value_guarded(ctx, Rom.sword)
            if current_sword_value is None:
                return
            write_list.append((Rom.sword, [max(2, current_sword_value)], self.wram))
        elif item_name == "Magical Sword":
            write_list.append((Rom.sword, [3], self.wram))
        elif item_name == "Bomb":
            current_bombs_value = await self.read_ram_value_guarded(ctx, Rom.bombs)
            current_max_bombs_value = await self.read_ram_value_guarded(ctx, Rom.max_bombs)
            if current_bombs_value is None or current_max_bombs_value is None:
                return
            write_list.append((Rom.bombs, [min(current_max_bombs_value, current_bombs_value + 4)], self.wram))
        elif item_name == "Bow":
            write_list.append((Rom.bow, [1], self.wram))
        elif item_name == "Arrow":
            current_arrow_value = await self.read_ram_value_guarded(ctx, Rom.arrow)
            if current_arrow_value is None:
                return
            write_list.append((Rom.arrow, [max(1, current_arrow_value)], self.wram))
        elif item_name == "Silver Arrow":
            write_list.append((Rom.arrow, [2], self.wram))
        elif item_name == "Candle":
            current_candle_value = await self.read_ram_value_guarded(ctx, Rom.candle)
            if current_candle_value is None:
                return
            write_list.append((Rom.candle, [max(1, current_candle_value)], self.wram))
        elif item_name == "Red Candle":
            write_list.append(((Rom.candle, [2], self.wram)))
        elif item_name == "Recorder":
            write_list.append((Rom.recorder, [1], self.wram))
        elif item_name == "Water of Life (Blue)":
            current_potion_value = await self.read_ram_value_guarded(ctx, Rom.potion)
            if current_potion_value is None:
                return
            write_list.append((Rom.potion, [max(1, current_potion_value)], self.wram))
        elif item_name == "Water of Life (Red)":
            write_list.append((Rom.potion, [2], self.wram))
        elif item_name == "Magical Rod":
            write_list.append((Rom.magical_rod, [1], self.wram))
        elif item_name == "Book of Magic":
            write_list.append((Rom.book_of_magic, [1], self.wram))
        elif item_name == "Raft":
            write_list.append((Rom.raft, [1], self.wram))
        elif item_name == "Blue Ring":
            current_ring_value = await self.read_ram_value_guarded(ctx, Rom.ring)
            if current_ring_value is None:
                return
            if current_ring_value < 2:
                write_list.append((Rom.ring, [max(1, current_ring_value)], self.wram))
                write_list.extend([(0x0B92, [0x32], self.sram), (0x0804, [0x32], self.sram)]) # Palette data
        elif item_name == "Red Ring":
            write_list.append((Rom.ring, [2], self.wram))
            write_list.extend([(0x0B92, [0x16], self.sram), (0x0804, [0x16], self.sram)])
        elif item_name == "Stepladder":
            write_list.append((Rom.stepladder, [1], self.wram))
        elif item_name == "Magical Key":
            write_list.append((Rom.magical_key, [1], self.wram))
        elif item_name == "Power Bracelet":
            write_list.append((Rom.power_bracelet, [1], self.wram))
        elif item_name == "Letter":
            write_list.append((Rom.letter, [1], self.wram))
        elif item_name == "Heart Container":
            current_heart_byte_value = await self.read_ram_value_guarded(ctx, Rom.heart_containers)
            if current_heart_byte_value is None:
                return
            current_container_count = min(((current_heart_byte_value & 0xF0) >> 4) + 1, 15)
            current_hearts_count = min((current_heart_byte_value & 0x0F) + 1, 15)
            write_list.append((Rom.heart_containers, [(current_container_count << 4) | current_hearts_count], self.wram))
        elif item_name == "Triforce Fragment":
            current_triforce_value = await self.read_ram_value_guarded(ctx, Rom.triforce_count)
            if current_triforce_value is None:
                return
            write_list.append((Rom.triforce_count, [min(current_triforce_value + 1, 8)], self.wram))
        elif item_name == "Boomerang":
            write_list.append((Rom.boomerang, [1], self.wram))
        elif item_name == "Magical Boomerang":
            write_list.append((Rom.magical_boomerang, [1], self.wram))
        elif item_name == "Magical Shield":
            write_list.append((Rom.magical_shield, [1], self.wram))
        elif item_name == "Recovery Heart":
            current_heart_byte_value = await self.read_ram_value_guarded(ctx, Rom.heart_containers)
            if current_heart_byte_value is None:
                return
            current_container_count = ((current_heart_byte_value & 0xF0) >> 4)
            current_hearts_count = current_heart_byte_value & 0x0F
            if current_hearts_count >= current_container_count:
                write_list.append((Rom.partial_hearts, [0xFF], self.wram))
                write_list.append((Rom.heart_containers, [(current_container_count << 4) | current_container_count], self.wram))
            else:
                current_hearts_count = min(current_hearts_count + 1, 15)
                write_list.append((Rom.heart_containers, [(current_container_count << 4) | current_hearts_count], self.wram))
        elif item_name == "Fairy":
            current_heart_byte_value = await self.read_ram_value_guarded(ctx, Rom.heart_containers)
            if current_heart_byte_value is None:
                return
            current_container_count = ((current_heart_byte_value & 0xF0) >> 4)
            current_hearts_count = current_heart_byte_value & 0x0F
            if (current_hearts_count + 3) >= current_container_count:
                write_list.append((Rom.partial_hearts, [0xFF], self.wram))
                write_list.append((Rom.heart_containers, [(current_container_count << 4) | current_container_count], self.wram))
            else:
                write_list.append((Rom.heart_containers, [(current_container_count << 4) | current_hearts_count], self.wram))
        elif item_name == "Clock":
            write_list.append((Rom.clock, [1], self.wram))
        elif item_name == "Five Rupees":
            current_rupees_to_add_value = await self.read_ram_value_guarded(ctx, Rom.rupees_to_add)
            if current_rupees_to_add_value is None:
                return
            write_list.append((Rom.rupees_to_add, [min(current_rupees_to_add_value + 5, 255)], self.wram))
        elif item_name == "Small Key":
            current_keys = await self.read_ram_value_guarded(ctx, Rom.keys)
            if current_keys is None:
                return
            write_list.append((Rom.keys, [min(current_keys + 1, 255)], self.wram))
        elif item_name == "Food":
            write_list.append((Rom.keys, [1], self.wram))
        await self.write(ctx, write_list)


    async def read_ram_value(self, ctx, location):
        value = ((await bizhawk.read(ctx.bizhawk_ctx, [(location, 1, self.wram)]))[0])
        return int.from_bytes(value, "little")

    async def read_ram_value_guarded(self, ctx, location):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                           [(location, 1, self.wram)],
                                           self.guard_list)
        if value is None:
            return None
        return int.from_bytes(value[0], "little")

    async def read_ram_values_guarded(self, ctx, location, size):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                          [(location, size, self.wram)],
                                          self.guard_list)
        if value is None:
            return None
        return value[0]

    async def read_rom(self, ctx, location, size):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.rom)]))[0]

    async def write(self, ctx, write_list: List[tuple[int, List[int], str]]):
        return await bizhawk.guarded_write(ctx.bizhawk_ctx, write_list, self.guard_list)