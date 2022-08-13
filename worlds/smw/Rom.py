import Utils
from Patch import read_rom, APDeltaPatch
from .Locations import lookup_id_to_name, all_locations
from .Levels import level_info_dict, full_level_list, submap_level_list, location_id_to_level_id

USHASH = 'cdd3c8c37322978ca8669b34bc89c804'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
import math


location_rom_data = {

}


item_rom_data = {
    0xBC3001: [0x18E4], # 1-Up Mushroom
    0xBC3002: [0xF48], # Yoshi Egg

    0xBC000E: [0x1F27], # Green Switch Palace
    0xBC000F: [0x1F28], # Yellow Switch Palace
    0xBC0010: [0x1F29], # Blue Switch Palace
    0xBC0011: [0x1F2A], # Red Switch Palace

    0xBC0013: [0x0086], # Ice Trap
    0xBC0014: [0x18BD], # Stun Trap
}

music_rom_data = [

]

level_music_ids = [

]

class LocalRom(object):

    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

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



def patch_rom(world, rom, player, active_level_dict):
    local_random = world.slot_seeds[player]

    # Force all 8 Bowser's Castle Rooms
    rom.write_byte(0x3A680, 0xD4)
    rom.write_byte(0x3A684, 0xD4)
    rom.write_byte(0x3A688, 0xD4)
    rom.write_byte(0x3A68C, 0xD4)
    rom.write_byte(0x3A705, 0xD3)
    rom.write_byte(0x3A763, 0xD2)
    rom.write_byte(0x3A800, 0xD1)
    rom.write_byte(0x3A83D, 0xCF)
    rom.write_byte(0x3A932, 0xCE)
    rom.write_byte(0x3A9E1, 0xCD)
    rom.write_byte(0x3AA75, 0xCC)

    # Prevent Title Screen Deaths
    rom.write_byte(0x1C6A, 0x80)

    # Always allow Start+Select
    rom.write_bytes(0x2267, bytearray([0xEA, 0xEA]))


    # Repurpose Bonus Stars counter for Yoshi Eggs
    if world.goal[player] == "yoshi_egg_hunt":
        rom.write_bytes(0x3F1AA, bytearray([0x00] * 0x20))

    # Lock Abilities
    rom.write_bytes(0x597C, bytearray([0xEA] * 0x03)) # Run
    rom.write_byte(0xAA5C, 0x80) # Shell/Key/P-Switch Carry
    rom.write_byte(0xE6D8, 0x80) # Springboard Carry
    rom.write_byte(0x7275, 0x80) # Purple Block Carry
    rom.write_byte(0xF1EC, 0x80) # Yoshi Carry
    rom.write_byte(0x4D62, 0x80) # Climb
    rom.write_byte(0xAB1B, 0x01) # P-Switch
    rom.write_byte(0x563E, 0x80) # Spin Jump
    rom.write_bytes(0x5984, bytearray([0xFF] * 0x03)) # Swim
    rom.write_byte(0x59D8, 0xFF) # Item Swim
    rom.write_byte(0x59DB, 0x00) # Item Swim
    rom.write_byte(0x108A1, 0x78) # Yoshi
    rom.write_byte(0xA2BC, 0x70) # Baby Yoshi

    # Lock Upgrades
    rom.write_byte(0xC599, 0x00) # No Capes
    rom.write_byte(0xC5F8, 0x00) # No Fire Flowers
    rom.write_byte(0x5156, 0xEA) # No Mushrooms
    rom.write_byte(0x5157, 0xEA) # No Mushrooms
    rom.write_byte(0x72E6, 0xEA) # No Midway Gate
    rom.write_byte(0x72E7, 0xEA) # No Midway Gate
    rom.write_byte(0xC581, 0x01) # No Stars
    rom.write_byte(0x62E6, 0x01) # No Star Music
    rom.write_byte(0xC300, 0x01) # No P-Balloons
    rom.write_byte(0xC305, 0x01) # No P-Balloons

    # Handle Level Shuffle Here
    if world.level_shuffle[player]:
        rom.write_bytes(0x37600, bytearray([0x00] * 0x800)) # Duplicate Level Table
        
        rom.write_bytes(0x2D89C, bytearray([0x00, 0xF6, 0x06])) # Level Load Pointer
        rom.write_bytes(0x20F46, bytearray([0x00, 0xF6, 0x06])) # Mid Gate Pointer
        rom.write_bytes(0x20E7B, bytearray([0x00, 0xF6, 0x06])) # Level Name Pointer
        rom.write_bytes(0x21543, bytearray([0x00, 0xF6, 0x06])) # Also Level Name Pointer?
        rom.write_bytes(0x20F64, bytearray([0x00, 0xF6, 0x06])) # Level Beaten Pointer

        ### Fix Translevel Check
        rom.write_bytes(0x2D8AE, bytearray([0x20, 0x00, 0xDD]))       # JSR $DD00
        rom.write_bytes(0x2D8B1, bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA])) # NOP NOP NOP NOP NOP
        
        rom.write_bytes(0x2D7CB, bytearray([0x20, 0x00, 0xDD]))       # JSR $DD00
        rom.write_bytes(0x2D7CE, bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA])) # NOP NOP NOP NOP NOP

        rom.write_bytes(0x2DD00, bytearray([0xDA]))             # PHX
        rom.write_bytes(0x2DD01, bytearray([0x08]))             # PHP
        rom.write_bytes(0x2DD02, bytearray([0xE2, 0x30]))       # SEP #30
        rom.write_bytes(0x2DD04, bytearray([0xAE, 0xBF, 0x13])) # LDX $13BF
        rom.write_bytes(0x2DD07, bytearray([0xE0, 0x25]))       # CPX #25
        rom.write_bytes(0x2DD09, bytearray([0x90, 0x04]))       # BCC $DD0F
        rom.write_bytes(0x2DD0B, bytearray([0xA2, 0x01]))       # LDX #01
        rom.write_bytes(0x2DD0D, bytearray([0x80, 0x02]))       # BRA $DD11
        rom.write_bytes(0x2DD0F, bytearray([0xA2, 0x00]))       # LDX #00
        rom.write_bytes(0x2DD11, bytearray([0x86, 0x0F]))       # STX $0F
        rom.write_bytes(0x2DD13, bytearray([0x28]))             # PLP
        rom.write_bytes(0x2DD14, bytearray([0xFA]))             # PLX
        rom.write_bytes(0x2DD15, bytearray([0x60]))             # RTS
        ### End Fix Translevel Check

        for level_id, level_data in level_info_dict.items():
            tile_id = active_level_dict[level_id]
            tile_data = level_info_dict[tile_id]

            print("Writing: ", hex(tile_data.levelIDAddress), " | ", hex(level_id))
            rom.write_byte(tile_data.levelIDAddress, level_id)
            print("Writing: ", hex(0x2D608 + level_id), " | ", hex(tile_data.eventIDValue))
            rom.write_byte(0x2D608 + level_id, tile_data.eventIDValue)


    from Main import __version__
    rom.name = bytearray(f'SMW{__version__.replace(".", "")[0:3]}_{player}_{world.seed:11}\0', 'utf8')[:20]
    rom.name.extend([0] * (20 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)


class SMWDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Super Mario World"
    patch_file_ending = ".apsmw"

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
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["smw_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name
