import logging
from copy import deepcopy, copy
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from worlds.tloz import Rom, Locations, Items

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


base_id = 7000
logger = logging.getLogger("Client")

WRAM_NAMES = {
    "NesHawk": "Battery RAM",
    "SubNESHawk": "Battery RAM",
    "QuickNes": "WRAM",
    "quickerNES": "WRAM",
}

class TLOZClient(BizHawkClient):
    game = "The Legend of Zelda"
    system = "NES"
    patch_suffix = ".aptloz"

    def __init__(self):
        self.wram = "RAM"
        self.sram = "WRAM" # Placeholder
        self.rom = "PRG ROM"
        self.bonus_items = []
        self.major_location_offsets = None
        self.base_guard_list = [(Rom.game_mode, [0x05], self.wram)] # 0x05 is normal gameplay in overworld or dungeon
        self.guard_list = [(Rom.game_mode, [0x05], self.wram)]
        self.take_any_item_ids = None


    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(Rom.rom_name_location, 3, self.rom)]))[0]).decode("ascii")
            if rom_name != "LOZ":
                return False
            #nes_core = (await bizhawk.get_cores(ctx.bizhawk_ctx))["NES"]
        except (bizhawk.RequestFailedError, UnicodeDecodeError):
            return False  # Not able to get a response, say no for now

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True

        #self.sram_name = WRAM_NAMES[nes_core]

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(Rom.player_name_location, Rom.player_name_length, "PRG ROM")]))[0]
        ctx.auth = auth_raw.decode().replace('\x00', ' ').strip()

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return
        try:
            if self.major_location_offsets is None:
                location_offsets = await self.read_rom(ctx, Rom.major_offsets_location, 4)
                self.major_location_offsets = deepcopy(Locations.major_location_offsets)
                self.major_location_offsets["Starting Sword Cave"] = location_offsets[0]
                self.major_location_offsets["White Sword Pond"] = location_offsets[1]
                self.major_location_offsets["Magical Sword Grave"] = location_offsets[2]
                self.major_location_offsets["Letter Cave"] = location_offsets[3]
            if self.take_any_item_ids is None:
                from . import TLoZWorld
                self.take_any_item_ids = {}
                self.take_any_item_ids["Left"] = TLoZWorld.location_name_to_id["Take Any Item Left"]
                self.take_any_item_ids["Middle"] = TLoZWorld.location_name_to_id["Take Any Item Middle"]
                self.take_any_item_ids["Right"] = TLoZWorld.location_name_to_id["Take Any Item Right"]
            self.guard_list = [*self.base_guard_list]
            await self.check_victory(ctx)
            await self.location_check(ctx)
            await self.received_items_check(ctx)
            await self.resolve_shop_items(ctx)
            await self.resolve_triforce_fragments(ctx)
            await self.resolve_bonus_items(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def check_victory(self, ctx: "BizHawkClientContext"):
        game_mode = await self.read_ram_value(ctx, Rom.game_mode)
        if game_mode == 19 and ctx.finished_game == False:
            ctx.finished_game = True
            await ctx.send_msgs([
                {"cmd": "StatusUpdate",
                 "status": ClientStatus.CLIENT_GOAL}
            ])

    async def location_check(self, ctx: "BizHawkClientContext"):
        locations_checked = []
        overworld_data = await self.read_ram_values_guarded(ctx, Rom.overworld_status_block, 0x80)
        underworld_early_data = await self.read_ram_values_guarded(ctx, Rom.underworld_early_status_block, 0x80)
        underworld_late_data = await self.read_ram_values_guarded(ctx, Rom.underworld_late_status_block, 0x80)
        if overworld_data is None or underworld_early_data is None or underworld_late_data is None:
            return
        for location, index in self.major_location_offsets.items():
            if (overworld_data[index] & 0x10) > 0:
                locations_checked.append(Locations.location_table[location])
        for location, index in Locations.floor_location_game_offsets_early.items():
            if (underworld_early_data[index] & 0x10) > 0:
                locations_checked.append(Locations.location_table[location])
        for location, index in Locations.floor_location_game_offsets_late.items():
            if (underworld_late_data[index] & 0x10) > 0:
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
            if self.take_any_item_ids["Left"] not in ctx.checked_locations:
                locations_checked.append(Locations.location_table[f"Take Any Item Left"])
                self.bonus_items.append(ctx.slot_data["TakeAnyLeft"])
            if self.take_any_item_ids["Middle"] not in ctx.checked_locations:
                locations_checked.append(Locations.location_table[f"Take Any Item Middle"])
                self.bonus_items.append(ctx.slot_data["TakeAnyMiddle"])
            if self.take_any_item_ids["Right"] not in ctx.checked_locations:
                locations_checked.append(Locations.location_table[f"Take Any Item Right"])
                self.bonus_items.append(ctx.slot_data["TakeAnyRight"])

        found_locations = await ctx.check_locations(locations_checked)
        for location in found_locations:
            ctx.locations_checked.add(location)
            location_name = ctx.location_names.lookup_in_game(location)
            logger.info(
                f'New Check: {location_name} ({len(ctx.locations_checked)}/'
                f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')



    async def received_items_check(self, ctx: "BizHawkClientContext"):
        items_received_count_low = await self.read_ram_value_guarded(ctx, Rom.items_obtained_low)
        items_received_count_high = await self.read_ram_value_guarded(ctx, Rom.items_obtained_high)
        if items_received_count_low is None or items_received_count_high is None:
            return
        items_received_count_value = (items_received_count_high << 8) | items_received_count_low
        if items_received_count_value < len(ctx.items_received):
            current_item = ctx.items_received[items_received_count_value]
            current_item_id = current_item.item
            current_item_name = ctx.item_names.lookup_in_game(current_item_id, ctx.game)
            items_received_count_value += 1
            new_items_received_count_low = items_received_count_value % 256
            new_items_received_count_high = items_received_count_value // 256
            new_items_received_count_low_write = (Rom.items_obtained_low, [new_items_received_count_low], self.wram)
            new_items_received_count_high_write = (Rom.items_obtained_high, [new_items_received_count_high], self.wram)
            write_list: list[tuple[int, list[int], str]] = [new_items_received_count_low_write, new_items_received_count_high_write]
            await self.write_item(ctx, current_item_name, write_list)

    async def resolve_shop_items(self, ctx: "BizHawkClientContext"):
        left_shop_slots = await self.read_ram_value_guarded(ctx, Rom.left_shop_slots)
        middle_shop_slots = await self.read_ram_value_guarded(ctx, Rom.middle_shop_slots)
        right_shop_slots = await self.read_ram_value_guarded(ctx, Rom.right_shop_slots)
        if left_shop_slots is None or middle_shop_slots is None or right_shop_slots is None:
            return
        for shop_category, shops in Locations.shop_categories.items():
            bit = Rom.shop_correspondance[shop_category]
            for shop in shops:
                shop_id = Locations.location_table[shop] + base_id
                if shop_id in ctx.checked_locations:
                    if "Left" in shop:
                        left_shop_slots = left_shop_slots | bit
                    if "Middle" in shop:
                        middle_shop_slots = middle_shop_slots | bit
                    if "Right" in shop:
                        right_shop_slots = right_shop_slots | bit
        bit = Rom.take_any
        for slot in Locations.take_any_locations:
            slot_id = Locations.location_table[slot] + base_id
            if slot_id in ctx.checked_locations:
                if "Left" in slot:
                    left_shop_slots = left_shop_slots | bit
                if "Middle" in slot:
                    middle_shop_slots = middle_shop_slots | bit
                if "Right" in slot:
                    right_shop_slots = right_shop_slots | bit
        left_shop_write = (Rom.left_shop_slots, [left_shop_slots], self.wram)
        middle_shop_write = (Rom.middle_shop_slots, [middle_shop_slots], self.wram)
        right_shop_write = (Rom.right_shop_slots, [right_shop_slots], self.wram)
        await self.write(ctx, [left_shop_write, middle_shop_write, right_shop_write])

    async def resolve_triforce_fragments(self, ctx: "BizHawkClientContext"):
        current_triforce_count = await self.read_ram_value_guarded(ctx, Rom.triforce_count)
        if current_triforce_count is None:
            return
        current_triforce_byte = 0xFF >> (8 - min(current_triforce_count, 8))
        write_list = [(Rom.triforce_fragments, [current_triforce_byte], self.wram)]
        await self.write(ctx, write_list)

    async def write_item(self, ctx, item_name, write_list: list[tuple[int, list[int], str]]):
        item_game_id = Items.item_game_ids[item_name]
        if item_name == "Bomb":
            item_game_id = 0x29 # Hack to allow bombs to be shown being lifted.
        lift_write = (Rom.item_to_lift, [item_game_id], self.wram)
        timer_write = (Rom.item_lift_timer, [128], self.wram) # 128 frames of lifting an item
        sound_write = (Rom.sound_effect_queue, [4], self.wram) # "Found secret" sound
        write_list.extend([lift_write, timer_write, sound_write])
        return await self.handle_item(ctx, item_name, write_list)

    async def resolve_bonus_items(self, ctx: "BizHawkClientContext"):
        new_bonus_items = copy(self.bonus_items)
        for item in self.bonus_items:
            current_item_name = ctx.item_names.lookup_in_game(item, ctx.game)
            success = await self.write_item(ctx, current_item_name, [])
            if success:
                new_bonus_items.remove(item)
        self.bonus_items = new_bonus_items

    async def handle_item(self, ctx: "BizHawkClientContext", item_name, write_list: list[tuple[int, list[int], str]]):
        # No nice way to do this, since basically every item needs to be handled a little differently.
        if item_name == "Sword":
            current_sword_value = await self.read_ram_value_guarded(ctx, Rom.sword)
            if current_sword_value is None:
                return
            self.guard_list.append((Rom.sword, [current_sword_value], self.wram))
            write_list.append((Rom.sword, [max(1, current_sword_value)], self.wram))
        elif item_name == "White Sword":
            current_sword_value = await self.read_ram_value_guarded(ctx, Rom.sword)
            if current_sword_value is None:
                return
            self.guard_list.append((Rom.sword, [current_sword_value], self.wram))
            write_list.append((Rom.sword, [max(2, current_sword_value)], self.wram))
        elif item_name == "Magical Sword":
            write_list.append((Rom.sword, [3], self.wram))
        elif item_name == "Bomb":
            current_bombs_value = await self.read_ram_value_guarded(ctx, Rom.bombs)
            current_max_bombs_value = await self.read_ram_value_guarded(ctx, Rom.max_bombs)
            if current_bombs_value is None or current_max_bombs_value is None:
                return
            self.guard_list.append((Rom.bombs, [current_bombs_value], self.wram))
            write_list.append((Rom.bombs, [min(current_max_bombs_value, current_bombs_value + 4)], self.wram))
        elif item_name == "Bow":
            write_list.append((Rom.bow, [1], self.wram))
        elif item_name == "Arrow":
            current_arrow_value = await self.read_ram_value_guarded(ctx, Rom.arrow)
            if current_arrow_value is None:
                return
            self.guard_list.append((Rom.arrow, [current_arrow_value], self.wram))
            write_list.append((Rom.arrow, [max(1, current_arrow_value)], self.wram))
        elif item_name == "Silver Arrow":
            write_list.append((Rom.arrow, [2], self.wram))
        elif item_name == "Candle":
            current_candle_value = await self.read_ram_value_guarded(ctx, Rom.candle)
            if current_candle_value is None:
                return
            self.guard_list.append((Rom.candle, [current_candle_value], self.wram))
            write_list.append((Rom.candle, [max(1, current_candle_value)], self.wram))
        elif item_name == "Red Candle":
            write_list.append(((Rom.candle, [2], self.wram)))
        elif item_name == "Recorder":
            write_list.append((Rom.recorder, [1], self.wram))
        elif item_name == "Water of Life (Blue)":
            current_potion_value = await self.read_ram_value_guarded(ctx, Rom.potion)
            if current_potion_value is None:
                return
            self.guard_list.append((Rom.potion, [current_potion_value], self.wram))
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
            self.guard_list.append((Rom.ring, [current_ring_value], self.wram))
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
            self.guard_list.append((Rom.heart_containers, [current_heart_byte_value], self.wram))
            write_list.append((Rom.heart_containers, [(current_container_count << 4) | current_hearts_count], self.wram))
        elif item_name == "Triforce Fragment":
            current_triforce_value = await self.read_ram_value_guarded(ctx, Rom.triforce_count)
            if current_triforce_value is None:
                return
            self.guard_list.append((Rom.triforce_count, [current_triforce_value], self.wram))
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
            self.guard_list.append((Rom.heart_containers, [current_heart_byte_value], self.wram))
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
            self.guard_list.append((Rom.heart_containers, [current_heart_byte_value], self.wram))
            current_container_count = ((current_heart_byte_value & 0xF0) >> 4)
            current_hearts_count = current_heart_byte_value & 0x0F
            if (current_hearts_count + 3) >= current_container_count:
                write_list.append((Rom.partial_hearts, [0xFF], self.wram))
                write_list.append((Rom.heart_containers, [(current_container_count << 4) | current_container_count], self.wram))
            else:
                current_hearts_count = min(current_hearts_count + 3, 15)
                write_list.append((Rom.heart_containers, [(current_container_count << 4) | current_hearts_count], self.wram))
        elif item_name == "Clock":
            write_list.append((Rom.clock, [1], self.wram))
        elif item_name == "Five Rupees":
            current_rupees_to_add_value = await self.read_ram_value_guarded(ctx, Rom.rupees_to_add)
            if current_rupees_to_add_value is None:
                return
            self.guard_list.append((Rom.rupees_to_add, [current_rupees_to_add_value], self.wram))
            write_list.append((Rom.rupees_to_add, [min(current_rupees_to_add_value + 5, 255)], self.wram))
        elif item_name == "Small Key":
            current_keys = await self.read_ram_value_guarded(ctx, Rom.keys)
            if current_keys is None:
                return
            self.guard_list.append((Rom.keys, [current_keys], self.wram))
            write_list.append((Rom.keys, [min(current_keys + 1, 255)], self.wram))
        elif item_name == "Food":
            write_list.append((Rom.food, [1], self.wram))
        return await self.write(ctx, write_list)


    async def read_ram_value(self, ctx, location):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, 1, self.wram)]))[0][0]

    async def read_ram_value_guarded(self, ctx: "BizHawkClientContext", location):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                           [(location, 1, self.wram)],
                                           self.guard_list)
        if value is None:
            return None
        return value[0][0]

    async def read_ram_values_guarded(self, ctx: "BizHawkClientContext", location, size):
        value = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                          [(location, size, self.wram)],
                                          self.guard_list)
        if value is None:
            return None
        return value[0]

    async def read_rom(self, ctx: "BizHawkClientContext", location, size):
        return (await bizhawk.read(ctx.bizhawk_ctx, [(location, size, self.rom)]))[0]

    async def write(self, ctx: "BizHawkClientContext", write_list: list[tuple[int, list[int], str]]):
        return await bizhawk.guarded_write(ctx.bizhawk_ctx, write_list, self.guard_list)