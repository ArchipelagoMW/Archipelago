import hashlib
import json
import zlib
import os
from pkgutil import get_data

import bsdiff4

import Utils
from BaseClasses import ItemClassification
from worlds.Files import APDeltaPatch, APProcedurePatch, APTokenMixin, APPatchExtension


NA10CHECKSUM = '337bd6f1a1163df31bf2633665589ab0'
ROM_PLAYER_LIMIT = 65535
ROM_NAME = 0x10
bit_positions = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
candle_shop = bit_positions[4]
arrow_shop = bit_positions[3]
potion_shop = bit_positions[2]
shield_shop = bit_positions[5]
ring_shop = bit_positions[6]
take_any = bit_positions[1]
left_shop_slots = 0x0628
middle_shop_slots = 0x0629
right_shop_slots = 0x062A
take_any_caves_checked = 0x0678
first_quest_dungeon_items_early = 0x18910
first_quest_dungeon_items_late = 0x18C10
game_mode = 0x12
items_obtained_low = 0x0677
items_obtained_high = 0x067B
sword = 0x0657
bombs = 0x0658
max_bombs = 0x067C
arrow = 0x0659
bow = 0x065A
candle = 0x065B
recorder = 0x065C
food = 0x065D
potion = 0x065E
magical_rod = 0x065F
raft = 0x0660
book_of_magic = 0x0661
ring = 0x0662
stepladder = 0x0663
magical_key = 0x0664
power_bracelet = 0x0665
letter = 0x0666
clock = 0x066C
keys = 0x066E
heart_containers = 0x066F
partial_hearts = 0x0670
triforce_fragments = 0x0671
triforce_count = 0x0679
boomerang = 0x0674
magical_boomerang = 0x0675
magical_shield = 0x0676
rupees_to_add = 0x067D

item_to_lift = 0x0505
item_lift_timer = 0x0506
sound_effect_queue = 0x0602


overworld_status_block = 0x067F
underworld_early_status_block = 0x06FF
underworld_late_status_block = 0x077F

cave_type_flags = {
    "Starting Sword Cave": 0b01000000,
    "Take Any Item": 0b01000100,
    "Door Repair": 0b01011100,
    "Potion Shop": 0b01101000,
    "Level 9": 0b00100100,
    "White Sword Pond": 0b01001000,
    "Level 5": 0b00010100,
    "Candle Shop": 0b01111000,
    "Letter Cave": 0b01100000,
    "Secret Money Large": 0b10001000,
    "Money Making Game": 0b01011000,
    "Shield Shop": 0b01111100,
    "Secret Money Medium": 0b10000100,
    "Go Up The Mountain Hint": 0b01101100,
    "Secret Is In Tree Hint": 0b01010100,
    "Warp Cave": 0b01010000,
    "Magical Sword Grave": 0b01001100,
    "Level 6": 0b00011000,
    "Arrow Shop": 0b01110100,
    "Blue Ring Shop": 0b10000000,
    "Level 2": 0b00001000,
    "Level 7": 0b00011100,
    "Level 4": 0b00010000,
    "Secret Money Small": 0b10001100,
    "Level 8": 0b00100000,
    "Lost Woods Hint": 0b01110000,
    "Level 3": 0b00001100,
    "Old Man Grave Hint": 0b01100100,
    "Level 1": 0b00000100
}

warp_cave_offset = 0x19344
starting_sword_cave_location_byte = 0x50
white_sword_pond_location_byte = 0x51
magical_sword_grave_location_byte = 0x52
letter_cave_location_byte = 0x53


class TLoZDeltaPatch(APDeltaPatch):
    hash = NA10CHECKSUM
    game = "The Legend of Zelda"
    patch_file_ending = ".aptloz"
    result_file_ending = ".nes"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if NA10CHECKSUM != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for NA (1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["tloz_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

class TLOZPatchExtension(APPatchExtension):
    game = "The Legend of Zelda"

    @staticmethod
    def apply_base_patch(rom):
        # The base patch source is on a different repo, so here's the summary of changes:
        # Remove Triforce check for recorder, so you can always warp.
        # Remove level check for Triforce Fragments (and maps and compasses, but this won't matter)
        # Replace some code with a jump to free space
        # Check if we're picking up a Triforce Fragment. If so, increment the local count
        # In either case, we do the instructions we overwrote with the jump and then return to normal flow
        # Remove map/compass check so they're always on
        # Removing a bit from the boss roars flags, so we can have more dungeon items. This allows us to
        # go past 0x1F items for dungeon items.
        base_patch = get_data(__name__, "z1_base_patch.bsdiff4")
        rom_data = bsdiff4.patch(rom.read(), base_patch)
        rom_data = bytearray(rom_data)
        # Set every item to the new nothing value, but keep room flags. Type 2 boss roars should
        # become type 1 boss roars, so we at least keep the sound of roaring where it should be.
        for i in range(0, 0x7F):
            item = rom_data[first_quest_dungeon_items_early + i]
            if item & 0b00100000:
                item = item & 0b11011111
                item = item | 0b01000000
                rom_data[first_quest_dungeon_items_early + i] = item
            if item & 0b00011111 == 0b00000011:  # Change all Item 03s to Item 3F, the proper "nothing"
                rom_data[first_quest_dungeon_items_early + i] = item | 0b00111111

            item = rom_data[first_quest_dungeon_items_late + i]
            if item & 0b00100000:
                item = item & 0b11011111
                item = item | 0b01000000
                rom_data[first_quest_dungeon_items_late + i] = item
            if item & 0b00011111 == 0b00000011:
                rom_data[first_quest_dungeon_items_late + i] = item | 0b00111111
        return rom_data

    @staticmethod
    def write_entrances(rom_data, entrance_randomizer_set):
        from worlds.tloz import cave_data_location_start
        warp_caves = []
        for entrance, data in entrance_randomizer_set.items():
            entrance_offset = int(entrance[7:], 16)
            entrance_name = data
            entrance_flag = cave_type_flags[entrance_name]
            original_data = rom_data[cave_data_location_start + entrance_offset]
            original_data = original_data & 0b00000011
            new_data = entrance_flag | original_data
            rom_data[cave_data_location_start + entrance_offset] = new_data
            if entrance_name == "Warp Cave":
                warp_caves.append(entrance_offset)
            if entrance_name == "Starting Sword Cave":
                rom_data[starting_sword_cave_location_byte] = entrance_offset
            if entrance_name == "White Sword Pond":
                rom_data[white_sword_pond_location_byte] = entrance_offset
            if entrance_name == "Magical Sword Grave":
                rom_data[magical_sword_grave_location_byte] = entrance_offset
            if entrance_name == "Letter Cave":
                rom_data[letter_cave_location_byte] = entrance_offset
        for i, cave in enumerate(warp_caves):
            rom_data[warp_cave_offset + i] = cave
            print(hex(cave))
        return rom_data

    @staticmethod
    def apply_randomizer(caller, rom, placement_file):
        from worlds.tloz import (shop_price_location_ids, shop_locations, item_game_ids, location_ids,
                                 item_prices, secret_money_ids)
        placements: dict[str, any] = json.loads(caller.get_file(placement_file))
        with open(get_base_rom_path(), 'rb') as rom:
            rom_data = TLOZPatchExtension.apply_base_patch(rom)
            rom_data = TLOZPatchExtension.write_entrances(rom_data, placements["entrance_randomizer_set"])
        rom_name = bytearray(placements["meta"]["rom_name"][:0x20], "utf8")[:0x20]
        rom_name.extend([0] * (0x20 - len(rom_name)))
        rom_data[0x10:0x30] = rom_name
        player_name = bytearray(placements["meta"]["player_name"], 'utf8')[:0x20]
        player_name.extend([0] * (0x20 - len(player_name)))
        rom_data[0x30:0x50] = player_name

        # Write each location's new data in
        for location, item in placements.items():
            # Zelda and Ganon aren't real locations. Neither is the metadata.
            if location == "Ganon" or location == "Zelda" or location == "entrance_randomizer_set" or location == "meta":
                continue

            if "Secret Money" in location:
                rom_data[secret_money_ids[location]] = item
                continue

            if "Classification" in location:
                continue

            # Neither are boss defeat events
            if "Status" in location:
                continue
            item_id = item_game_ids[item]
            location_id = location_ids[location]

            # Shop prices need to be set
            if location in shop_locations:
                if location[-5:] == "Right":
                    # Final item in stores has bit 6 and 7 set. It's what marks the cave a shop.
                    item_id = item_id | 0b11000000
                price_location = shop_price_location_ids[location]
                item_price = item_prices[item]
                if item == "Rupee":
                    item_class = placements.get(location + " Classification", ItemClassification.filler)
                    if item_class == ItemClassification.progression:
                        item_price = item_price * 2
                    elif item_class == ItemClassification.useful:
                        item_price = item_price // 2
                    elif item_class == ItemClassification.filler:
                        item_price = item_price // 2
                    elif item_class == ItemClassification.trap:
                        item_price = item_price * 2
                rom_data[price_location] = item_price
            if location == "Take Any Item Right":
                # Same story as above: bit 6 is what makes this a Take Any cave
                item_id = item_id | 0b01000000
            rom_data[location_id] = item_id
        return rom_data


class TLOZProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "The Legend of Zelda"
    hash = NA10CHECKSUM
    patch_file_ending = ".aptloz"
    result_file_ending = ".nes"

    procedure = [
        ("apply_randomizer", ["placement_file.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()