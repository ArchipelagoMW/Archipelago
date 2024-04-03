import Utils
from worlds.AutoWorld import World
from worlds.Files import APDeltaPatch

import bsdiff4
import hashlib
import os
from pkgutil import get_data

USHASH = 'cfe8c11f0dce19e4fa5f3fd75775e47c'
ROM_PLAYER_LIMIT = 65535

weapon_rom_data = {
    0xBD000B: [0x1FC8, 0xFF],
    0xBD000C: [0x1FBC, 0xFF],
    0xBD000D: [0x1FCA, 0xFF],
    0xBD000E: [0x1FC0, 0xFF],
    0xBD000F: [0x1FC2, 0xFF],
    0xBD0010: [0x1FC4, 0xFF],
    0xBD0011: [0x1FC6, 0xFF],
    0xBD0012: [0x1FBE, 0xFF],
    0xBD001A: [0x1FB2, 0xE0],
}

ride_armor_rom_data = {
    0xBD0015: [0x00],
    0xBD0016: [0x01],
    0xBD0017: [0x02],
    0xBD0018: [0x03],
}

upgrades_rom_data = {
    0xBD001C: [0x00],
    0xBD001D: [0x02],
    0xBD001E: [0x01],
    0xBD001F: [0x03],
}

boss_access_rom_data = {
    0xBD0009: [0x00],
    0xBD0005: [0x01],
    0xBD0008: [0x03],
    0xBD0002: [0x04],
    0xBD0003: [0x05],
    0xBD0006: [0x06],
    0xBD000A: [0x07],
    0xBD0004: [0x08],
    0xBD0007: [0x09],
}

refill_rom_data = {
    0xBD0030: ["small hp refill"],
    0xBD0031: ["large hp refill"],
    0xBD0034: ["1up"],
    #0xBD0032: ["small weapon refill"],
    #0xBD0033: ["large weapon refill"]
}

class MMX3DeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Mega Man X3"
    patch_file_ending = ".apmmx3"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class LocalRom:

    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = Utils.read_snes_rom(stream)
        
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

    def apply_patch(self, patch: bytes):
        self.buffer = bytearray(bsdiff4.patch(bytes(self.buffer), patch))

    def write_crc(self):
        crc = (sum(self.buffer[:0x7FDC] + self.buffer[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])


def patch_rom(world: World, rom, player):
    from Utils import __version__

    # Apply base patch
    rom.apply_patch(get_data(__name__, os.path.join("data", "mmx3_basepatch.bsdiff4")))

    # Edit the ROM header
    rom.name = bytearray(f'MMX3{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)

    # Write options to the ROM
    rom.write_byte(0x17FFE0, world.options.doppler_open.value)
    rom.write_byte(0x17FFE1, world.options.doppler_medal_count.value)
    rom.write_byte(0x17FFE2, world.options.doppler_weapon_count.value)
    rom.write_byte(0x17FFE3, world.options.doppler_upgrade_count.value)
    rom.write_byte(0x17FFE4, world.options.doppler_heart_tank_count.value)
    rom.write_byte(0x17FFE5, world.options.doppler_sub_tank_count.value)
    rom.write_byte(0x17FFE6, world.options.starting_life_count.value)
    if world.options.pickupsanity.value:
        rom.write_byte(0x17FFE7, 0x01)
    else:
        rom.write_byte(0x17FFE7, 0x00)
    rom.write_byte(0x17FFE8, world.options.vile_open.value)
    rom.write_byte(0x17FFE9, world.options.vile_medal_count.value)
    rom.write_byte(0x17FFEA, world.options.vile_weapon_count.value)
    rom.write_byte(0x17FFEB, world.options.vile_upgrade_count.value)
    rom.write_byte(0x17FFEC, world.options.vile_heart_tank_count.value)
    rom.write_byte(0x17FFED, world.options.vile_sub_tank_count.value)

    rom.write_byte(0x17FFEE, world.options.logic_boss_weakness.value)
    rom.write_byte(0x17FFEF, world.options.logic_vile_required.value)
    rom.write_byte(0x17FFF0, world.options.logic_z_saber.value)
    
    #rom.write_byte(0x17FFF1, world.options.doppler_lab_1_boss.value)
    rom.write_byte(0x17FFF1, 0x00)
    rom.write_byte(0x17FFF2, world.options.doppler_lab_2_boss.value)
    rom.write_byte(0x17FFF3, world.options.doppler_lab_3_boss_rematch_count.value)

    bit_medal_count = world.options.bit_medal_count.value
    byte_medal_count = world.options.byte_medal_count.value
    if bit_medal_count == 0 and byte_medal_count == 0:
        byte_medal_count = 1
    elif bit_medal_count >= byte_medal_count:
        if bit_medal_count == 7:
            bit_medal_count = 6
        byte_medal_count = bit_medal_count + 1
    rom.write_byte(0x17FFF4, bit_medal_count)
    rom.write_byte(0x17FFF5, byte_medal_count)

    # QoL
    rom.write_byte(0x17FFF6, world.options.disable_charge_freeze.value)

    # EnergyLink
    rom.write_byte(0x17FFF7, world.options.energy_link.value)
    
    # Setup starting life count
    rom.write_byte(0x0019B1, world.options.starting_life_count.value)
    rom.write_byte(0x0072C3, world.options.starting_life_count.value)
    rom.write_byte(0x0021BE, world.options.starting_life_count.value)

    # Debug option
    rom.write_byte(0x17FFFF, 0x00)

    rom.write_crc()

    
def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["mmx3_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
