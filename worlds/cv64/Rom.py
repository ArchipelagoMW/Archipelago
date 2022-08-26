import Utils
import hashlib
import os
# import math

# from BaseClasses import Location
from Patch import read_rom, APDeltaPatch
from .Names import PatchName

USHASH = '1cc5cf3b4d29d8c3ade957648b529dc1'
ROM_PLAYER_LIMIT = 65535


rom_loc_offsets = {
    0xC64001: 0x10C67B,  # Forest of Silence
    0xC64002: 0x10C71B,
    0xC64003: 0x10C6BB,
    0xC64004: 0x10C68B,
    0xC64005: 0x10C693,
    0xC64006: 0x10C6C3,
    0xC64007: 0x10C6E3,
    0xC64008: 0x10C6CB,
    0xC64009: 0x10C683,
    0xC6400A: 0x10C743,
    0xC6400B: 0x10C6A3,
    0xC6400C: 0x10C69B,
    0xC6400D: 0x10C6D3,
    0xC6400E: 0x10C6AB,
    0xC6400F: 0x10C76B,
    0xC64010: 0x10C75B,
    0xC64011: 0x10C713,
    0xC64012: 0x10C733,
    0xC64013: 0x10C6B3,
    0xC64014: 0x10C72B,

    0xC64015: 0x10C7E7,  # Castle Wall
    0xC64016: 0x10C7DF,
    0xC64017: 0x10C7EF,
    0xC64018: 0x10C7F7,
    0xC64019: 0x10C7FF,
    0xC6401A: 0x10C807,
    0xC6401B: 0x10C80B,
    0xC6401C: 0x10C810,
}

rom_item_bytes = {
    "Red jewel(S)": 0x02,
    "Red jewel(L)": 0x03,
    "Special1": 0x04,
    "Roast beef": 0x07,
    "PowerUp": 0x0C,
    "Sun card": 0x17,
    "Moon card": 0x18,
    "500 GOLD": 0x1A,
    "300 GOLD": 0x1B,
    "100 GOLD": 0x1C,
    "Left Tower Key": 0x1E,
}


class LocalRom(object):

    def __init__(self, file, patch=True, vanilla_rom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        # if patch:
        #    self.patch_rom()
        #    self.orig_buffer = self.buffer.copy()
        # if vanilla_rom:
        #    with open(vanillaRom, 'rb') as vanillaStream:
        #        self.orig_buffer = read_rom(vanillaStream)
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())


def patch_rom(world, rom, player, offsets_to_ids):
    # local_random = world.slot_seeds[player]

    # NOP out the CRC BNEs
    rom.write_bytes(0x66C, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x678, [0x00, 0x00, 0x00, 0x00])

    # Disable Easy Mode cutoff point
    rom.write_bytes(0xD9E18, [0x24, 0x0D, 0x00, 0x00])

    # Fix both elevator bridges for both characters
    rom.write_bytes(0x6CEAA0, [0x24, 0x0B, 0x00, 0x01])
    rom.write_bytes(0x6CEAA4, [0x24, 0x0D, 0x00, 0x01])

    # Disable vampire Vincent cutscene
    if world.fight_vincent[player] == "never":
        rom.write_bytes(0xAACC0, [0x24, 0x01, 0x00, 0x01])

    # Increase item capacity to 100
    if world.increase_item_limit[player] == "true":
        rom.write_byte(0xBF30B, 0x64)

    # Custom warp menu and remote item-rewarding check code injection
    rom.write_bytes(0x19B98, [0x08, 0x06, 0x0D, 0x8B])  # J 0x8018362C
    rom.write_bytes(0x10681C, PatchName.remote_item_and_warp)

    # Custom warp menu code
    rom.write_bytes(0xADD68, [0x0C, 0x04, 0xAB, 0x12])  # JAL 0x8012AC48
    rom.write_bytes(0xADE28, PatchName.stage_select_overwrite)
    rom.write_byte(0xADD6F, world.special2s_per_warp[player])

    # Write the new item bytes
    for offset, item_id in offsets_to_ids.items():
        rom.write_byte(offset, item_id)


class CV64DeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Castlevania 64"
    patch_file_ending = ".apcv64"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it.')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["cv64_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name
