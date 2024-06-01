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
    0xBD0030: ["hp refill", 2],
    0xBD0031: ["hp refill", 8],
    0xBD0034: ["1up", 0],
    0xBD0032: ["weapon refill", 2],
    0xBD0033: ["weapon refill", 8]
}

boss_weakness_offsets = {
    "Blast Hornet": 0x03674B,
    "Blizzard Buffalo": 0x036771,
    "Gravity Beetle": 0x036797,
    "Toxic Seahorse": 0x0367BD,
    "Volt Catfish": 0x0367E3,
    "Crush Crawfish": 0x036809,
    "Tunnel Rhino": 0x03682F,
    "Neon Tiger": 0x036855,
    "Bit": 0x03687B,
    "Byte": 0x0368A1,
    "Vile": 0x0368C7,
    "Vile Goliath": 0x0368ED,
    "Doppler": 0x036913,
    "Sigma": 0x036939,
    "Kaiser Sigma": 0x03695F,
    "Godkarmachine": 0x037F00,
    "Press Disposer": 0x037FC8,
    "Worm Seeker-R": 0x03668D,
    "Shurikein": 0x037F28,
    "Hotareeca": 0x037F50,
    "Volt Kurageil": 0x037F78,
    "Hell Crusher": 0x037FA0,
}

boss_hp_caps_offsets = {
    "Maoh": 0x016985,
    "Blast Hornet": 0x1C9DC2,
    "Blizzard Buffalo": 0x01C9CB,
    "Gravity Beetle": 0x09F3C3,
    "Toxic Seahorse": 0x09E612,
    "Volt Catfish": 0x09EBC0,
    "Crush Crawfish": 0x01D1B2,
    "Tunnel Rhino": 0x1FE765,
    "Neon Tiger": 0x09DE11,
    "Bit": 0x0390F2,
    "Byte": 0x1E4614,
    "Vile": 0x02AC3E,
    "Vile Kangaroo": 0x03958F,
    "Vile Goliath": 0x02A4EA,
    "Doppler": 0x09D737,
    "Sigma": 0x0294F2,
    "Kaiser Sigma": 0x029B1F,
    "Godkarmachine": 0x028F60,
    "Press Disposer": 0x09C6B9,
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


def adjust_boss_damage_table(world: World, patch: MMX3ProcedurePatch):
    strictness = world.options.boss_weakness_strictness
    for boss, data in world.boss_weakness_data.items():
        try:
            offset = boss_weakness_offsets[boss]

            # Fixes Worm Seeker-R damage table on strict settings
            if boss == "Worm Seeker-R" and strictness != "not_strict":
                for x in range(len(data)):
                    if x == 0x02 or x == 0x04 or x == 0x05:
                        data[x] = 0x7F
                    else:
                        data[x] = data[x]*3 if data[x] < 0x80 else data[x]
        except:
            continue
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


def adjust_boss_hp(world: World, patch: MMX3ProcedurePatch):
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


def patch_rom(world: World, patch: MMX3ProcedurePatch):
    from Utils import __version__

    # Prepare some ROM locations to receive the basepatch
    patch.write_bytes(0x00638, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0065A, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x00EFD, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x00F36, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x00FF2, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01034, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x03118, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x06A0B, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x06C4C, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x06E76, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x06F28, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x0F242, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x16900, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x19604, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x1B34D, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x24E01, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x24F44, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x24F5C, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x25095, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x29B83, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x2C81D, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x30E4A, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x395EA, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0FF84, bytearray([0xFF for _ in range(0x007C)]))
    patch.write_bytes(0x1FA80, bytearray([0xFF for _ in range(0x0580)]))

    # Adjust Charged Triad Thunder lag (lasts 90 less frames)
    patch.write_byte(0x1FD2D1, 0x14)

    adjust_boss_damage_table(world, patch)
    
    if world.options.boss_randomize_hp != "off":
        adjust_boss_hp(world, patch)

    # Edit the ROM header
    patch.name = bytearray(f'MMX3{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7FC0, patch.name)

    # Setup starting HP
    patch.write_byte(0x007487, world.options.starting_hp.value)
    patch.write_byte(0x0019B6, world.options.starting_hp.value)
    patch.write_byte(0x0021CC, (world.options.starting_hp.value + (world.options.heart_tank_effectiveness.value * 8)) | 0x80)

    # Setup starting life count
    patch.write_byte(0x0019B1, world.options.starting_life_count.value)
    patch.write_byte(0x0072C3, world.options.starting_life_count.value)
    patch.write_byte(0x0021BE, world.options.starting_life_count.value)

    # Write options to the ROM
    patch.write_byte(0x17FFE1, world.options.doppler_medal_count.value)
    patch.write_byte(0x17FFE2, world.options.doppler_weapon_count.value)
    patch.write_byte(0x17FFE3, world.options.doppler_upgrade_count.value)
    patch.write_byte(0x17FFE4, world.options.doppler_heart_tank_count.value)
    patch.write_byte(0x17FFE5, world.options.doppler_sub_tank_count.value)
    patch.write_byte(0x17FFE6, world.options.starting_life_count.value)
    patch.write_byte(0x17FFE7, world.options.pickupsanity.value)
    patch.write_byte(0x17FFE9, world.options.vile_medal_count.value)
    patch.write_byte(0x17FFEA, world.options.vile_weapon_count.value)
    patch.write_byte(0x17FFEB, world.options.vile_upgrade_count.value)
    patch.write_byte(0x17FFEC, world.options.vile_heart_tank_count.value)
    patch.write_byte(0x17FFED, world.options.vile_sub_tank_count.value)

    patch.write_byte(0x17FFEE, world.options.logic_boss_weakness.value)
    patch.write_byte(0x17FFEF, world.options.logic_vile_required.value)
    patch.write_byte(0x17FFF0, world.options.zsaber_in_pool.value)
    
    value = 0
    doppler_open = world.options.doppler_open.value
    if "Medals" in doppler_open:
        value |= 0x01
    if "Weapons" in doppler_open:
        value |= 0x02
    if "Armor Upgrades" in doppler_open:
        value |= 0x04
    if "Heart Tanks" in doppler_open:
        value |= 0x08
    if "Sub Tanks" in doppler_open:
        value |= 0x10
    patch.write_byte(0x17FFE0, value)

    value = 0
    vile_open = world.options.vile_open.value
    if "Medals" in vile_open:
        value |= 0x01
    if "Weapons" in vile_open:
        value |= 0x02
    if "Armor Upgrades" in vile_open:
        value |= 0x04
    if "Heart Tanks" in vile_open:
        value |= 0x08
    if "Sub Tanks" in vile_open:
        value |= 0x10
    patch.write_byte(0x17FFE8, value)

    #patch.write_byte(0x17FFF1, world.options.doppler_lab_1_boss.value)
    patch.write_byte(0x17FFF1, 0x00)
    patch.write_byte(0x17FFF2, world.options.doppler_lab_2_boss.value)
    patch.write_byte(0x17FFF3, world.options.doppler_lab_3_boss_rematch_count.value)
    patch.write_byte(0x17FFF4, world.options.bit_medal_count.value)
    patch.write_byte(0x17FFF5, world.options.byte_medal_count.value)

    # QoL
    patch.write_byte(0x17FFF6, world.options.disable_charge_freeze.value)

    # EnergyLink
    patch.write_byte(0x17FFF7, world.options.energy_link.value)

    # DeathLink
    patch.write_byte(0x17FFF8, world.options.death_link.value)
    
    patch.write_byte(0x17FFF9, world.options.jammed_buster.value)
    patch.write_byte(0x17FFFA, world.options.boss_weakness_rando.value)
    patch.write_byte(0x17FFFB, world.options.boss_weakness_strictness.value)
    patch.write_byte(0x17FFFC, world.options.starting_hp.value)
    patch.write_byte(0x17FFFD, world.options.heart_tank_effectiveness.value)
    patch.write_byte(0x17FFFE, world.options.doppler_all_labs.value)

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
