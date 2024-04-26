import typing
import bsdiff4
import Utils
import hashlib
import os
from typing import Optional, TYPE_CHECKING
from pkgutil import get_data

from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

HASH_US = 'cfe8c11f0dce19e4fa5f3fd75775e47c'
HASH_LEGACY = 'ff683b75e75e9b59f0c713c7512a016b'

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

class MMX3ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US, HASH_LEGACY]
    game = "Mega Man X3"
    patch_file_ending = ".apmmx3"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["mmx3_basepatch.bsdiff4"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

def patch_rom(world: World, patch: MMX3ProcedurePatch):
    from Utils import __version__

    # Prepare some ROM locations to receive the basepatch output
    patch.write_bytes(0x00638, bytearray([0x85,0xB4,0x8A]))
    patch.write_bytes(0x0065A, bytearray([0x85,0xB4,0x8A]))
    patch.write_bytes(0x00EFD, bytearray([0xA9,0x10,0x20,0x91,0x86]))
    patch.write_bytes(0x00F36, bytearray([0xA5,0xAD,0x89,0x08,0xF0,0x09,0xA5,0x3C,
                                          0x3A,0x10,0x11,0xA9,0x02,0x80,0x0D,0x89,
                                          0x24,0xF0,0x24,0xA5,0x3C,0x1A,0xC9,0x03,
                                          0xD0,0x02,0xA9,0x00,0x85,0x3C,0xAA,0xBD,
                                          0xF8,0x87,0x8D,0xE0,0x09,0xA5,0x3C,0x18,
                                          0x69,0x10,0x20,0x91,0x86,0xA9,0xF0,0x85,
                                          0x3B,0xA9,0x1C,0x22,0x2B,0x80,0x01]))
    patch.write_bytes(0x00FF2, bytearray([0x9C,0xD9,0x09,0x9C,0xDA,0x09]))
    patch.write_bytes(0x01034, bytearray([0x64,0x38,0x64,0x39]))
    patch.write_bytes(0x03118, bytearray([0xA9,0x08,0x85,0xD5]))
    patch.write_bytes(0x06A0B, bytearray([0x62,0x81]))
    patch.write_bytes(0x06C4C, bytearray([0x85,0x00,0x0A]))
    patch.write_bytes(0x06E76, bytearray([0x9F,0xCB,0xFF,0x7E]))
    patch.write_bytes(0x06F28, bytearray([0x41,0x88]))
    patch.write_bytes(0x0F242, bytearray([0xA9,0x02,0x85]))
    patch.write_bytes(0x16900, bytearray([0xA9,0x04,0x85,0x01]))
    patch.write_bytes(0x19604, bytearray([0xA9,0x01,0x0C,0xD7,0x1F]))
    patch.write_bytes(0x1B34D, bytearray([0xA9,0xC0,0x0C,0xB2,0x1F]))
    patch.write_bytes(0x24E01, bytearray([0xED,0x00,0x00,0x8D,0xFF,0x09]))
    patch.write_bytes(0x24F44, bytearray([0x85,0x27,0xA9,0x20]))
    patch.write_bytes(0x24F5C, bytearray([0x64,0x27,0xA9,0x06]))
    patch.write_bytes(0x25095, bytearray([0xED,0x00,0x00,0x8D,0xFF,0x09]))
    patch.write_bytes(0x29B83, bytearray([0xA9,0x04,0x85,0x01]))
    patch.write_bytes(0x2C81D, bytearray([0xBD,0xFD,0xBB,0x0C,0xD1,0x1F,0x60,0xA9,
                                          0xFF,0x0C,0xCC,0x1F]))
    patch.write_bytes(0x30E4A, bytearray([0xAD,0x97,0xAD,0x97]))
    patch.write_bytes(0x395EA, bytearray([0xA9,0x04,0x85,0x01]))
    patch.write_bytes(0x0FF84, bytearray([0xFF for _ in range(0x007C)]))
    patch.write_bytes(0x1FA80, bytearray([0xFF for _ in range(0x0580)]))

    # Edit the ROM header
    patch.name = bytearray(f'MMX3{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7FC0, patch.name)

    # Write options to the ROM
    patch.write_byte(0x17FFE0, world.options.doppler_open.value)
    patch.write_byte(0x17FFE1, world.options.doppler_medal_count.value)
    patch.write_byte(0x17FFE2, world.options.doppler_weapon_count.value)
    patch.write_byte(0x17FFE3, world.options.doppler_upgrade_count.value)
    patch.write_byte(0x17FFE4, world.options.doppler_heart_tank_count.value)
    patch.write_byte(0x17FFE5, world.options.doppler_sub_tank_count.value)
    patch.write_byte(0x17FFE6, world.options.starting_life_count.value)
    if world.options.pickupsanity.value:
        patch.write_byte(0x17FFE7, 0x01)
    else:
        patch.write_byte(0x17FFE7, 0x00)
    patch.write_byte(0x17FFE8, world.options.vile_open.value)
    patch.write_byte(0x17FFE9, world.options.vile_medal_count.value)
    patch.write_byte(0x17FFEA, world.options.vile_weapon_count.value)
    patch.write_byte(0x17FFEB, world.options.vile_upgrade_count.value)
    patch.write_byte(0x17FFEC, world.options.vile_heart_tank_count.value)
    patch.write_byte(0x17FFED, world.options.vile_sub_tank_count.value)

    patch.write_byte(0x17FFEE, world.options.logic_boss_weakness.value)
    patch.write_byte(0x17FFEF, world.options.logic_vile_required.value)
    patch.write_byte(0x17FFF0, world.options.logic_z_saber.value)
    
    #patch.write_byte(0x17FFF1, world.options.doppler_lab_1_boss.value)
    patch.write_byte(0x17FFF1, 0x00)
    patch.write_byte(0x17FFF2, world.options.doppler_lab_2_boss.value)
    patch.write_byte(0x17FFF3, world.options.doppler_lab_3_boss_rematch_count.value)

    bit_medal_count = world.options.bit_medal_count.value
    byte_medal_count = world.options.byte_medal_count.value
    if bit_medal_count == 0 and byte_medal_count == 0:
        byte_medal_count = 1
    elif bit_medal_count >= byte_medal_count:
        if bit_medal_count == 7:
            bit_medal_count = 6
        byte_medal_count = bit_medal_count + 1
    patch.write_byte(0x17FFF4, bit_medal_count)
    patch.write_byte(0x17FFF5, byte_medal_count)

    # QoL
    patch.write_byte(0x17FFF6, world.options.disable_charge_freeze.value)

    # EnergyLink
    patch.write_byte(0x17FFF7, world.options.energy_link.value)

    # DeathLink
    patch.write_byte(0x17FFF8, world.options.death_link.value)
    
    patch.write_byte(0x17FFF9, world.options.jammed_buster.value)

    # Setup starting life count
    patch.write_byte(0x0019B1, world.options.starting_life_count.value)
    patch.write_byte(0x0072C3, world.options.starting_life_count.value)
    patch.write_byte(0x0021BE, world.options.starting_life_count.value)

    patch.write_file("token_patch.bin", patch.get_token_binary())

    
def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US, HASH_LEGACY}:
            raise Exception('Supplied Base Rom does not match known MD5 for US or LC release. '
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
