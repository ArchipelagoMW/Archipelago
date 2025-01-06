import logging
from copy import deepcopy
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from worlds.tloz import Rom, Locations, Items

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


base_id = 7000
nes_logger = logging.getLogger("NES")
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


    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(Rom.ROM_NAME - 0x10, 3, self.rom)]))[0]).decode("ascii")
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
            game_mode = await self.read_ram_value(ctx, Rom.game_mode)
            if game_mode == 0x05:
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
        overworld_data = await self.read_ram_values(ctx, Rom.overworld_status_block, 0x80)
        underworld_early_data = await self.read_ram_values(ctx, Rom.underworld_early_status_block, 0x80)
        underworld_late_data = await self.read_ram_values(ctx, Rom.underworld_late_status_block, 0x80)
        for location, index in self.major_location_offsets.items():
            if (int(overworld_data[index]) & 0x10) > 0:
                locations_checked.append(Locations.location_table[location])
        for location, index in Locations.floor_location_game_offsets_early.items():
            if (int(underworld_early_data[index]) & 0x10 > 0):
                locations_checked.append(Locations.location_table[location])
        for location, index in Locations.floor_location_game_offsets_late.items():
            if (int(underworld_late_data[index]) & 0x10 > 0):
                locations_checked.append(Locations.location_table[location])

        left_shop_slots = await self.read_ram_value(ctx, Rom.left_shop_slots)
        middle_shop_slots = await self.read_ram_value(ctx, Rom.middle_shop_slots)
        right_shop_slots = await self.read_ram_value(ctx, Rom.right_shop_slots)
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
        take_any_caves_checked = await self.read_ram_value(ctx, Rom.take_any_caves_checked)
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
                nes_logger.info(
                    f'New Check: {location_name} ({len(ctx.locations_checked)}/'
                    f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location]}])



    async def received_items_check(self, ctx):
        items_received_count_low = await self.read_ram_value(ctx, Rom.items_obtained)
        items_received_count_high = await self.read_ram_value(ctx, Rom.items_obtained + 1)
        items_received_count = list([items_received_count_low, items_received_count_high])
        items_received_count_value = int.from_bytes(items_received_count, "little")
        if items_received_count_value < len(ctx.items_received):
            current_item = ctx.items_received[items_received_count_value]
            current_item_id = current_item.item
            current_item_name = ctx.item_names.lookup_in_game(current_item_id, ctx.game)
            await self.write_item(ctx, current_item_name)
            await self.write(ctx, Rom.items_obtained, items_received_count_value + 1)

    async def resolve_shop_items(self, ctx):
        pass

    async def resolve_triforce_fragments(self, ctx):
        current_triforce_count = await self.read_ram_value(ctx, Rom.triforce_count)
        current_triforce_byte = 0xFF >> (8 - min(current_triforce_count, 8))
        await self.write(ctx, Rom.triforce_fragments, current_triforce_byte)

    async def write_item(self, ctx, item_name):
        item_game_id = Items.item_game_ids[item_name]
        if item_name == "Bomb":
            item_game_id = 0x29 # Hack to allow bombs to be shown being lifted.
        await self.write(ctx, Rom.item_to_lift, item_game_id)
        await self.write(ctx, Rom.item_lift_timer, 128) # 128 frames of lifting an item
        await self.write(ctx, Rom.sound_effect_queue, 4) # "Found secret" sound
        await self.handle_item(ctx, item_name)

    async def resolve_bonus_items(self, ctx):
        for item in self.bonus_items:
            current_item_name = ctx.item_names.lookup_in_game(item, ctx.game)
            await self.write_item(ctx, current_item_name)
        self.bonus_items.clear()

    async def handle_item(self, ctx, item_name):
        # No nice way to do this, since basically every item needs to be handled a little differently.
        if item_name == "Sword":
            current_sword_value = await self.read_ram_value(ctx, Rom.sword)
            await self.write(ctx, Rom.sword, max(1, current_sword_value))
        elif item_name == "White Sword":
            current_sword_value = await self.read_ram_value(ctx, Rom.sword)
            await self.write(ctx, Rom.sword, max(2, current_sword_value))
        elif item_name == "Magical Sword":
            current_sword_value = await self.read_ram_value(ctx, Rom.sword)
            await self.write(ctx, Rom.sword, max(3, current_sword_value))
        elif item_name == "Bomb":
            current_bombs_value = await self.read_ram_value(ctx, Rom.bombs)
            current_max_bombs_value = await self.read_ram_value(ctx, Rom.max_bombs)
            await self.write(ctx, Rom.bombs, min(current_max_bombs_value, current_bombs_value + 4))
        elif item_name == "Bow":
            await self.write(ctx, Rom.bow, 1)
        elif item_name == "Arrow":
            current_arrow_value = await self.read_ram_value(ctx, Rom.arrow)
            await self.write(ctx, Rom.arrow, max(1, current_arrow_value))
        elif item_name == "Silver Arrow":
            current_arrow_value = await self.read_ram_value(ctx, Rom.arrow)
            await self.write(ctx, Rom.arrow, max(2, current_arrow_value))
        elif item_name == "Candle":
            current_candle_value = await self.read_ram_value(ctx, Rom.candle)
            await self.write(ctx, Rom.candle, max(1, current_candle_value))
        elif item_name == "Red Candle":
            current_candle_value = await self.read_ram_value(ctx, Rom.candle)
            await self.write(ctx, Rom.candle, max(2, current_candle_value))
        elif item_name == "Recorder":
            await self.write(ctx, Rom.recorder, 1)
        elif item_name == "Water of Life (Blue)":
            current_potion_value = await self.read_ram_value(ctx, Rom.potion)
            await self.write(ctx, Rom.potion, max(1, current_potion_value))
        elif item_name == "Water of Life (Red)":
            current_potion_value = await self.read_ram_value(ctx, Rom.potion)
            await self.write(ctx, Rom.potion, max(2, current_potion_value))
        elif item_name == "Magical Rod":
            await self.write(ctx, Rom.magical_rod, 1)
        elif item_name == "Book of Magic":
            await self.write(ctx, Rom.book_of_magic, 1)
        elif item_name == "Raft":
            await self.write(ctx, Rom.raft, 1)
        elif item_name == "Blue Ring":
            current_ring_value = await self.read_ram_value(ctx, Rom.ring)
            if current_ring_value < 2:
                await self.write(ctx, Rom.ring, max(1, current_ring_value))
                await bizhawk.write(ctx.bizhawk_ctx, [(0x0B92, [0x32], self.sram), (0x0804, [0x32], self.sram)])
        elif item_name == "Red Ring":
            current_ring_value = await self.read_ram_value(ctx, Rom.ring)
            await self.write(ctx, Rom.ring, max(2, current_ring_value))
            await bizhawk.write(ctx.bizhawk_ctx, [(0x0B92, [0x16], self.sram), (0x0804, [0x16], self.sram)])
        elif item_name == "Stepladder":
            await self.write(ctx, Rom.stepladder, 1)
        elif item_name == "Magical Key":
            await self.write(ctx, Rom.magical_key, 1)
        elif item_name == "Power Bracelet":
            await self.write(ctx, Rom.power_bracelet, 1)
        elif item_name == "Letter":
            await self.write(ctx, Rom.letter, 1)
        elif item_name == "Heart Container":
            current_heart_byte_value = await self.read_ram_value(ctx, Rom.heart_containers)
            current_container_count = min(((current_heart_byte_value & 0xF0) >> 4) + 1, 15)
            current_hearts_count = min((current_heart_byte_value & 0x0F) + 1, 15)
            await self.write(ctx, Rom.heart_containers, (current_container_count << 4) | current_hearts_count)
        elif item_name == "Triforce Fragment":
            current_triforce_value = await self.read_ram_value(ctx, Rom.triforce_count)
            await self.write(ctx, Rom.triforce_count, min(current_triforce_value + 1, 8))
        elif item_name == "Boomerang":
            await self.write(ctx, Rom.boomerang, 1)
        elif item_name == "Magical Boomerang":
            await self.write(ctx, Rom.magical_boomerang, 1)
        elif item_name == "Magical Shield":
            await self.write(ctx, Rom.magical_shield, 1)
        elif item_name == "Recovery Heart":
            current_heart_byte_value = await self.read_ram_value(ctx, Rom.heart_containers)
            current_container_count = ((current_heart_byte_value & 0xF0) >> 4)
            current_hearts_count = current_heart_byte_value & 0x0F
            if current_hearts_count >= current_container_count:
                await self.write(ctx, Rom.partial_hearts, 0xFF)
                await self.write(ctx, Rom.heart_containers, (current_container_count << 4) | current_container_count)
            else:
                current_hearts_count = min(current_hearts_count + 1, 15)
                await self.write(ctx, Rom.heart_containers, (current_container_count << 4) | current_hearts_count)
        elif item_name == "Fairy":
            current_heart_byte_value = await self.read_ram_value(ctx, Rom.heart_containers)
            current_container_count = ((current_heart_byte_value & 0xF0) >> 4)
            current_hearts_count = current_heart_byte_value & 0x0F
            if (current_hearts_count + 3) >= current_container_count:
                await self.write(ctx, Rom.partial_hearts, 0xFF)
                await self.write(ctx, Rom.heart_containers, (current_container_count << 4) | current_container_count)
            else:
                current_hearts_count = min(current_hearts_count + 3, 15)
                await self.write(ctx, Rom.heart_containers, (current_container_count << 4) | current_hearts_count)
        elif item_name == "Clock":
            await self.write(ctx, Rom.clock, 1)
        elif item_name == "Five Rupees":
            current_rupees_to_add_value = await self.read_ram_value(ctx, Rom.rupees_to_add)
            await self.write(ctx, Rom.rupees_to_add, min(current_rupees_to_add_value + 5, 255))
        elif item_name == "Small Key":
            current_keys = await self.read_ram_value(ctx, Rom.keys)
            await self.write(ctx, Rom.keys, min(current_keys + 1, 255))
        elif item_name == "Food":
            await self.write(ctx, Rom.food, 1)
        else:
            print(item_name)
            raise Exception


    async def read_ram_values(self, ctx, location, size):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.wram)]))[0]

    async def read_ram_value(self, ctx, location):
        value = ((await bizhawk.read(ctx.bizhawk_ctx, [(location, 1, self.wram)]))[0])
        return int.from_bytes(value)

    async def read_rom(self, ctx, location, size):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.rom)]))[0]

    async def write(self, ctx, location, value):
        return await bizhawk.write(ctx.bizhawk_ctx, [(location, [value], self.wram)])