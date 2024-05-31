import typing
import bsdiff4
import Utils
import hashlib
import os
from typing import Optional
from pkgutil import get_data

from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .Weaknesses import boss_weakness_data

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
    0xBD0030: ["hp refill", 2],
    0xBD0031: ["hp refill", 8],
    0xBD0034: ["1up", 0],
    0xBD0032: ["weapon refill", 2],
    0xBD0033: ["weapon refill", 8],
}

boss_weakness_offsets = {
    "Wheel Gator": 0x0,
    "Bubble Crab": 0x0,
    "Flame Stag": 0x0,
    "Morph Moth": 0x0,
    "Magna Centipede": 0x0,
    "Crystal Snail": 0x0,
    "Overdrive Ostrich": 0x0,
    "Wire Sponge": 0x0,
    "Agile": 0x0,
    "Serges": 0x0,
    "Violen": 0x0,
    "Neo Violen": 0x0,
    "Serges Tank": 0x0,
    "Agile Flyer": 0x0,
    "Zero": 0x0,
    "Sigma": 0x0,
}

boss_hp_caps_offsets = {
    "Wheel Gator": 0x0,
    "Bubble Crab": 0x0,
    "Flame Stag": 0x0,
    "Morph Moth": 0x0,
    "Magna Centipede": 0x0,
    "Crystal Snail": 0x0,
    "Overdrive Ostrich": 0x0,
    "Wire Sponge": 0x0,
    "Agile": 0x0,
    "Serges": 0x0,
    "Violen": 0x0,
    "Gigantic Mechaniloid CF-0": 0x0,
    "Sea Canthller": 0x0,
    "Pararoid S-38": 0x0,
    "Chop Register": 0x0,
    "Raider Killer": 0x0,
    "Magna Quartz": 0x0,
    "Neo Violen": 0x0,
    "Serges Tank": 0x0,
    "Agile Flyer": 0x0,
    "Zero": 0x0,
    "Sigma": 0x0,
}


class MMX2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US, HASH_LEGACY]
    game = "Mega Man X2"
    patch_file_ending = ".apmmx2"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["mmx2_basepatch.bsdiff4"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def adjust_boss_damage_table(world: World, patch: MMX2ProcedurePatch):
    strictness = world.options.boss_weakness_strictness
    for boss, data in world.boss_weakness_data.items():
        offset = boss_weakness_offsets[boss]
        patch.write_bytes(offset, bytearray(data))

    # Write weaknesses to a table
    offset = 0x98000
    for _, entries in world.boss_weaknesses.items():
        data = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        i = 0
        for entry in entries:
            data[i] = entry[1]
            i += 1
        patch.write_bytes(offset, bytearray(data))
        offset += 8


def adjust_boss_hp(world: World, patch: MMX2ProcedurePatch):
    option = world.options.boss_randomize_hp
    if option == "weak":
        ranges = [1,32]
    elif option == "regular":
        ranges = [16,48]
    elif option == "strong":
        ranges = [32,64]
    elif option == "chaotic":
        ranges = [1,64]
    
    for _, offset in boss_hp_caps_offsets.items():
        patch.write_byte(offset, world.random.randint(ranges[0], ranges[1]))


def patch_rom(world: World, patch: MMX2ProcedurePatch):
    from Utils import __version__

    # Prepare some ROM locations to receive the basepatch

    adjust_boss_damage_table(world, patch)
    
    if world.options.boss_randomize_hp != "off":
        adjust_boss_hp(world, patch)

    # Edit the ROM header
    patch.name = bytearray(f'MMX2{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7FC0, patch.name)

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
        file_name = options["mmx2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
