import typing
import bsdiff4
import Utils
import hashlib
import os
from pkgutil import get_data

from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

HASH_US = 'a10071fa78554b57538d0b459e00d224'
HASH_US_REV_1 = 'df1cc0c8c8c4b61e3b834cc03366611c'
HASH_LEGACY = 'f1dfbbcdc3d8cdeafa4b4b9aa51a56d6'

STARTING_ID = 0xBE0800

weapon_rom_data = {
    STARTING_ID + 0x000E: [0x1F88, 0xFF],
    STARTING_ID + 0x0010: [0x1F8A, 0xFF],
    STARTING_ID + 0x000D: [0x1F8C, 0xFF],
    STARTING_ID + 0x0012: [0x1F8E, 0xFF],
    STARTING_ID + 0x0011: [0x1F90, 0xFF],
    STARTING_ID + 0x000C: [0x1F92, 0xFF],
    STARTING_ID + 0x000F: [0x1F94, 0xFF],
    STARTING_ID + 0x000B: [0x1F96, 0xFF],
    STARTING_ID + 0x001A: [0x1F7E, 0x80],
}

upgrades_rom_data = {
    STARTING_ID + 0x001C: [0x00],
    STARTING_ID + 0x001D: [0x02],
    STARTING_ID + 0x001E: [0x01],
    STARTING_ID + 0x001F: [0x03],
}

boss_access_rom_data = {
    STARTING_ID + 0x0006: [0x01],
    STARTING_ID + 0x0008: [0x02],
    STARTING_ID + 0x0002: [0x03],
    STARTING_ID + 0x0005: [0x04],
    STARTING_ID + 0x0009: [0x05],
    STARTING_ID + 0x0007: [0x06],
    STARTING_ID + 0x0003: [0x07],
    STARTING_ID + 0x0004: [0x08],
    STARTING_ID + 0x000A: [0x09],
}

refill_rom_data = {
    STARTING_ID + 0x0030: ["hp refill", 2],
    STARTING_ID + 0x0031: ["hp refill", 8],
    STARTING_ID + 0x0034: ["1up", 0],
    STARTING_ID + 0x0032: ["weapon refill", 2],
    STARTING_ID + 0x0033: ["weapon refill", 8],
}

boss_weakness_offsets = {
    "Sting Chameleon": 0x37E20,
    "Storm Eagle": 0x37E60,
    "Flame Mammoth": 0x37E80,
    "Chill Penguin": 0x37EA0,
    "Spark Mandrill": 0x3708B,
    "Armored Armadillo": 0x370A9,
    "Launch Octopus": 0x370C7,
    "Boomer Kuwanger": 0x370E5,
    "Thunder Slimer": 0x37F00,
    "Vile": 0x37E00,
    "Bospider": 0x37EC0,
    "Rangda Bangda": 0x37031,
    "D-Rex": 0x37E40,
    "Velguarder": 0x37EE0,
    "Sigma": 0x3717B,
    "Wolf Sigma": 0x37199,
}

boss_hp_caps_offsets = {
    "Sting Chameleon": 0x406C9,
    "Storm Eagle": 0x3D95F,
    "Flame Mammoth": 0x392BD,
    "Chill Penguin": 0x0B5FB,
    "Spark Mandrill": 0x41D29,
    "Armored Armadillo": 0x1B2B5,
    "Launch Octopus": 0x0C504,
    "Boomer Kuwanger": 0x38BE8,
    "Vile": 0x45C34,
    "Bospider": 0x15C0E,
    #"Rangda Bangda": 0x42A38,
    #"D-Rex": 0x440FD,
    "Velguarder": 0x148DF,
    "Sigma": 0x4467B,
    "Wolf Sigma": 0x44B78,
}

class MMXProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US, HASH_LEGACY]
    game = "Mega Man X"
    patch_file_ending = ".apmmx"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["mmx_basepatch.bsdiff4"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def adjust_boss_damage_table(world: World, patch: MMXProcedurePatch):
    for boss, data in world.boss_weakness_data.items():
        offset = boss_weakness_offsets[boss]
        patch.write_bytes(offset, bytearray(data))

    # Fix second anglerge having different weakness
    patch.write_byte(0x12E62, 0x01)

    # Write weaknesses to a table
    offset = 0x17EC00
    for _, entries in world.boss_weaknesses.items():
        data = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        i = 0
        for entry in entries:
            data[i] = entry[1]
            i += 1
        patch.write_bytes(offset, bytearray(data))
        offset += 8


def adjust_boss_hp(world: World, patch: MMXProcedurePatch):
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


def patch_rom(world: World, patch: MMXProcedurePatch):
    # Prepare some ROM locations to receive the basepatch output
    patch.write_bytes(0x00098C, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0009AE, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x001261, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x001271, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF]))
    patch.write_bytes(0x00131F, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x00132E, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x001352, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0025CA, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0046F3, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x006A61, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x006D67, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x006F97, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x00700F, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x007BF0, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x00EB4A, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x011646, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01B392, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01C67E, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01D84F, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x021D51, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x021E94, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x021F5A, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x02268C, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x03D0B2, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x03D0D9, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x044BEC, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0457CC, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))

    patch.write_bytes(0x0312B0, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF]))

    adjust_boss_damage_table(world, patch)
    
    if world.options.boss_randomize_hp != "off":
        adjust_boss_hp(world, patch)

    patch.write_byte(0x014FF, world.options.starting_hp.value)
    patch.write_byte(0x01DDC, 0x7F)

    # Edit the ROM header
    from Utils import __version__
    patch.name = bytearray(f'MMX1{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7FC0, patch.name)

    # Write options to the ROM
    value = 0
    sigma_open = world.options.sigma_open.value
    if "Medals" in sigma_open:
        value |= 0x01
    if "Weapons" in sigma_open:
        value |= 0x02
    if "Armor Upgrades" in sigma_open:
        value |= 0x04
    if "Heart Tanks" in sigma_open:
        value |= 0x08
    if "Sub Tanks" in sigma_open:
        value |= 0x10
    patch.write_byte(0x17FFE0, value)
    patch.write_byte(0x17FFE1, world.options.sigma_medal_count.value)
    patch.write_byte(0x17FFE2, world.options.sigma_weapon_count.value)
    patch.write_byte(0x17FFE3, world.options.sigma_upgrade_count.value)
    patch.write_byte(0x17FFE4, world.options.sigma_heart_tank_count.value)
    patch.write_byte(0x17FFE5, world.options.sigma_sub_tank_count.value)
    patch.write_byte(0x17FFE6, world.options.starting_life_count.value)
    patch.write_byte(0x17FFE7, world.options.pickupsanity.value)
    patch.write_byte(0x17FFE8, world.options.energy_link.value)
    patch.write_byte(0x17FFE9, world.options.death_link.value)
    patch.write_byte(0x17FFEA, world.options.jammed_buster.value)
    patch.write_byte(0x17FFEB, world.options.logic_boss_weakness.value)
    patch.write_byte(0x17FFEC, world.options.boss_weakness_rando.value)
    patch.write_byte(0x17FFED, world.options.starting_hp.value)
    patch.write_byte(0x17FFEE, world.options.heart_tank_effectiveness.value)
    patch.write_byte(0x17FFEF, world.options.sigma_all_levels.value)
    patch.write_byte(0x17FFF0, world.options.boss_weakness_strictness.value)

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
        file_name = options["mmx_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
