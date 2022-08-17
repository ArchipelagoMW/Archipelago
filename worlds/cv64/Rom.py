import Utils
import hashlib
import os
import math

from BaseClasses import Location
from Patch import read_rom, APDeltaPatch

USHASH = '1cc5cf3b4d29d8c3ade957648b529dc1'
ROM_PLAYER_LIMIT = 65535


locations_rom_data = {
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


item_rom_data = {
    0xC64002: 0x02,  # Red jewel(S)
    0xC64003: 0x03,  # Red jewel(L)
    0xC64004: 0x04,  # Special1
    0xC64007: 0x07,  # Roast beef
    0xC6400C: 0x0C,  # PowerUp
    0xC64017: 0x17,  # Sun card
    0xC64018: 0x18,  # Moon card
    0xC6401A: 0x1A,  # 500 GOLD
    0xC6401B: 0x1B,  # 300 GOLD
    0xC6401C: 0x1C,  # 100 GOLD
    0xC6401E: 0x1E,  # Left Tower Key
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


def patch_rom(world, rom, player):
    local_random = world.slot_seeds[player]

    # Disable vampire Vincent cutscene
    rom.write_byte(0xAACC0, 0x24)
    rom.write_byte(0xAACC1, 0x01)
    rom.write_byte(0xAACC2, 0x00)
    rom.write_byte(0xAACC3, 0x01)

    # Increase item capacity to 99
    rom.write_byte(0xBF30B, 0x63)

    # Disable Easy Mode cutoff point
    rom.write_byte(0xD9E18, 0x24)
    rom.write_byte(0xD9E19, 0x0D)
    rom.write_byte(0xD9E1A, 0x00)
    rom.write_byte(0xD9E1B, 0x00)

    # Fix both elevator bridges for both characters
    rom.write_byte(0x6CEAA0, 0x24)
    rom.write_byte(0x6CEAA1, 0x0B)
    rom.write_byte(0x6CEAA2, 0x00)
    rom.write_byte(0x6CEAA3, 0x01)
    rom.write_byte(0x6CEAA4, 0x24)
    rom.write_byte(0x6CEAA5, 0x0D)
    rom.write_byte(0x6CEAA6, 0x00)
    rom.write_byte(0x6CEAA7, 0x01)

    # Write the new item bytes
    # for locationid, address in locations_rom_data.items():
    #    rom.write_byte(address, get_item_byte(locationid))

    from Main import __version__
    rom.name = bytearray(f'CV64{__version__.replace(".", "")[0:3]}_{player}_{world.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)


class CV64DeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Castlevania"
    patch_file_ending = ".apcv64"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


# def get_item_byte(locationid):
#    pass


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
