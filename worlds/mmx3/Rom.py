
import Utils
import hashlib
import struct
import os
import io
from pathlib import Path
from pkgutil import get_data

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from . import MMX3World

from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

from .Graphics import graphics_slots
from .Aesthetics import get_palette_bytes, player_palettes

action_names = ("SHOT", "JUMP", "DASH", "SELECT_L", "SELECT_R", "MENU")
action_buttons = ("Y", "B", "A", "L", "R", "X", "START", "SELECT")

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

chip_rom_data = {
    0xBD0040: [0x18A],       # Quick Charge
    0xBD0041: [0x180],       # Speedster
    0xBD0042: [0x187],       # Super Recover
    0xBD0043: [0x183],       # Rapid Five
    0xBD0044: [0x185],       # Speed Shot
    0xBD0045: [0x184],       # Buster Plus
    0xBD0046: [0x18D],       # Weapon Plus
    0xBD0047: [0x186],       # Item Plus
}

refill_rom_data = {
    0xBD0030: ["hp refill", 2],
    0xBD0031: ["hp refill", 8],
    0xBD0034: ["1up", 0],
    0xBD0032: ["weapon refill", 2],
    0xBD0033: ["weapon refill", 8]
}

x_palette_set_offsets = {
    "Default": 0x62400,
    "Charge Blue": 0x62F60,
    "Charge Pink": 0x62F80,
    "Charge Red": 0x625A0,
    "Charge Green": 0x625E0,
    "Gold Armor": 0x62580,
    "Acid Burst": 0x62480,
    "Parasitic Bomb": 0x624A0,
    "Triad Thunder": 0x624C0,
    "Spinning Blade": 0x624E0,
    "Ray Splasher": 0x62500,
    "Gravity Well": 0x62520,
    "Frost Shield": 0x62540,
    "Tornado Fang": 0x62560,
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

boss_hp_threshold_offsets = {
    "Volt Catfish": 0x9ECC3,
    "Toxic Seahorse": 0x9E76B,
    "Gravity Beetle": 0x9F57F,
}

class MMX3PatchExtension(APPatchExtension):
    game = "Mega Man X3"

    @staticmethod
    def relocate_graphics(caller: APProcedurePatch, rom: bytes):
        stream = io.BytesIO(rom)
        rom = bytearray(rom)
        rom += bytearray([0xFF for _ in range(0x100000)])

        for _, data in graphics_slots.items():
            pc_ptr = data[1]
            compressed_size = data[2]
            new_pc_ptr = pc_ptr + 0x130000
            stream.seek(pc_ptr)
            rom[new_pc_ptr:new_pc_ptr + compressed_size] = stream.read(compressed_size)
            rom[pc_ptr:pc_ptr + compressed_size] = bytearray([0x00 for _ in range(compressed_size)])

        return bytes(rom)
    
    @staticmethod
    def output_xml(caller: APProcedurePatch, rom: bytes):
        manifest = caller.get_file("mmx3_manifest_for_bsnes.xml")
        with open(f"{Path(caller.path).stem}.xml", "wb") as f:
            f.write(manifest)
        return rom

class MMX3ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US, HASH_LEGACY]
    game = "Mega Man X3"
    patch_file_ending = ".apmmx3"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("relocate_graphics", []),
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["mmx3_basepatch.bsdiff4"]),
        ("output_xml", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def adjust_palettes(world: "MMX3World", patch: MMX3ProcedurePatch):
    player_palette_options = {
        "Default": world.options.palette_default.current_key,
        "Gold Armor": world.options.palette_gold_armor.current_key,
        "Charge Blue": world.options.palette_charge_blue.current_key,
        "Charge Pink": world.options.palette_charge_pink.current_key,
        "Charge Red": world.options.palette_charge_red.current_key,
        "Charge Green": world.options.palette_charge_green.current_key,
        "Acid Burst": world.options.palette_acid_burst.current_key,
        "Parasitic Bomb": world.options.palette_parasitic_bomb.current_key,
        "Triad Thunder": world.options.palette_triad_thunder.current_key,
        "Spinning Blade": world.options.palette_spinning_blade.current_key,
        "Ray Splasher": world.options.palette_ray_splasher.current_key,
        "Gravity Well": world.options.palette_gravity_well.current_key,
        "Frost Shield": world.options.palette_frost_shield.current_key,
        "Tornado Fang": world.options.palette_tornado_fang.current_key,
    }
    player_custom_palettes = world.options.player_palettes
    for palette_set, offset in x_palette_set_offsets.items():
        palette_option = player_palette_options[palette_set]
        palette = player_palettes[palette_option]

        if palette_set in player_custom_palettes.keys():
            if len(player_custom_palettes[palette_set]) == 0x10:
                palette = player_custom_palettes[palette_set]
            else:
                print (f"[{world.multiworld.player_name[world.player]}] Custom palette set for {palette_set} doesn't have exactly 16 colors. Falling back to the selected preset ({palette_option})")
        data = get_palette_bytes(palette)
        patch.write_bytes(offset, data)
        

def adjust_boss_damage_table(world: "MMX3World", patch: MMX3ProcedurePatch):
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
    excluded_bosses = [
        "Dr. Doppler's Lab 1 Boss",
        "Dr. Doppler's Lab 2 Boss", 
    ]
    for boss, entries in world.boss_weaknesses.items():
        if boss in excluded_bosses:
            continue
        data = [0xFF for _ in range(16)]
        i = 0
        for entry in entries:
            data[i] = entry[1]
            i += 1
        patch.write_bytes(offset, bytearray(data))
        offset += 16


def adjust_boss_hp(world: "MMX3World", patch: MMX3ProcedurePatch):
    option = world.options.boss_randomize_hp
    if option == "weak":
        ranges = [1,32]
    elif option == "regular":
        ranges = [16,48]
    elif option == "strong":
        ranges = [32,64]
    elif option == "chaotic":
        ranges = [1,64]
    
    for boss, offset in boss_hp_caps_offsets.items():
        if boss in boss_hp_threshold_offsets.keys():
            value = world.random.randint(ranges[0] + 1, ranges[1])
            value_threshold = world.random.randint(1, value - 1)
            offset_threshold = boss_hp_threshold_offsets[boss]
            patch.write_byte(offset_threshold, value_threshold)
        else:
            value = world.random.randint(ranges[0], ranges[1])
        patch.write_byte(offset, value)



def patch_rom(world: "MMX3World", patch: MMX3ProcedurePatch):
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
    adjust_palettes(world, patch)
    
    if world.options.boss_randomize_hp != "off":
        adjust_boss_hp(world, patch)

    # Edit the ROM header
    patch.name = bytearray(f'MMX3{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7FC0, patch.name)

    # Remap buttons
    button_values = {
        "A": 0x20,
        "B": 0x80,
        "X": 0x10,
        "Y": 0x40,
        "L": 0x08,
        "R": 0x04,
        "START": 0x01,
        "SELECT": 0x02,
    }
    action_offsets = {
        "SHOT": 0x360E3,
        "JUMP": 0x360E4,
        "DASH": 0x360E5,
        "SELECT_L": 0x360E6,
        "SELECT_R": 0x360E7,
        "MENU": 0x360E8,
    }
    button_config = world.options.button_configuration.value
    for action, button in button_config.items():
        patch.write_byte(action_offsets[action], button_values[button])

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

    value = 0
    if world.options.long_jumps.value:
        value |= 0x01
    patch.write_byte(0x17FFF1, value)

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
