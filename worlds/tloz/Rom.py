import hashlib
import zlib
import os

import Utils
from worlds.Files import APDeltaPatch

NA10CHECKSUM = '337bd6f1a1163df31bf2633665589ab0'
ROM_PLAYER_LIMIT = 65535
ROM_NAME = 0x10
bit_positions = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
candle_shop = bit_positions[5]
arrow_shop = bit_positions[4]
potion_shop = bit_positions[1]
shield_shop = bit_positions[6]
ring_shop = bit_positions[7]
take_any = bit_positions[2]
left_shop_slots = 0x0628
middle_shop_slots = 0x0629
right_shop_slots = 0x062A
take_any_caves_checked = 0x0678
first_quest_dungeon_items_early = 0x18910
first_quest_dungeon_items_late = 0x18C10
game_mode = 0x12
items_obtained = 0x0677
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
starting_sword_cave_location_byte = 0x40
white_sword_pond_location_byte = 0x41
magical_sword_grave_location_byte = 0x42
letter_cave_location_byte = 0x43


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
