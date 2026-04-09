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
first_quest_dungeon_items_early = 0x18910
first_quest_dungeon_items_late = 0x18C10
game_mode = 0x12
sword = 0x0657
bombs = 0x0658
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
heart_containers = 0x066F
triforce_fragments = 0x0671
boomerang = 0x0674
magical_boomerang = 0x0675
magical_shield = 0x0676
rupees_to_add = 0x067D




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
        file_name = get_base_rom_path()
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if NA10CHECKSUM != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for NA (1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path() -> str:
    from . import TLoZWorld
    return TLoZWorld.settings.rom_file
