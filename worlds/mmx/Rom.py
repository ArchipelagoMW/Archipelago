import Utils
import hashlib
import os
import settings

from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .Aesthetics import get_palette_bytes, player_palettes

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from . import MMXWorld

HASH_US = 'a10071fa78554b57538d0b459e00d224'
HASH_US_REV_1 = 'df1cc0c8c8c4b61e3b834cc03366611c'
HASH_LEGACY = 'f1dfbbcdc3d8cdeafa4b4b9aa51a56d6'

STARTING_ID = 0xBE0800

action_names = ("SHOT", "JUMP", "DASH", "SELECT_L", "SELECT_R", "MENU")
action_buttons = ("Y", "B", "A", "L", "R", "X", "START", "SELECT")

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

x_palette_set_offsets = {
    "Default": 0x02B700,
    "Homing Torpedo": 0x02CC40,
    "Chameleon Sting": 0x02CC60,
    "Rolling Shield": 0x02CD20,
    "Fire Wave": 0x02CD00,
    "Storm Tornado": 0x02CCC0,
    "Electric Spark": 0x02CCE0,
    "Boomerang Cutter": 0x02CCA0,
    "Shotgun Ice": 0x02CC80,
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

enemy_tweaks_offsets = {
    "Chill Penguin": 0x158000,
    "Armored Armadillo": 0x158002,
    "Spark Mandrill": 0x158004,
}

enemy_tweaks_indexes = {
    "Chill Penguin": {
        "Random horizontal slide speed": 0x0001,
        "Jumps when starting slide": 0x0002,
        "Random ice block horizontal speed": 0x0004,
        "Random ice block vertical speed": 0x0008,
        "Shoot random amount of ice blocks": 0x0010,
        "Ice block shooting rate enhancer #1": 0x0020,
        "Ice block shooting rate enhancer #2": 0x0040,
        "Ice block shooting rate enhancer #3": 0x0080,
        "Random blizzard strength": 0x0100,
        "Fast falls after jumping": 0x0200,
        "Random mist range": 0x0400,
        "Can't be stunned/set on fire with incoming damage": 0x4000,
        "Can't be set on fire with weakness": 0x8000,
    },
    "Armored Armadillo": {
        "Random bouncing speed": 0x0001,
        "Random bouncing angle": 0x0002,
        "Random energy horizontal speed": 0x0004,
        "Random energy vertical speed": 0x0008,
        "Energy shooting rate enhancer #1": 0x0010,
        "Energy shooting rate enhancer #2": 0x0020,
        "Don't absorb any projectile": 0x1000,
        "Absorbs any projectile except weakness": 0x2000,
        "Don't flinch from incoming damage without armor": 0x4000,
        "Can't block incoming projectiles": 0x8000,
    },
    "Spark Mandrill": {
        "Random Electric Spark speed": 0x0001,
        "Additional Electric Spark #1": 0x0002,
        "Additional Electric Spark #2": 0x0004,
        "Landing creates Electric Spark": 0x0008,
        "Hitting a wall creates Electric Spark": 0x0010,
        "Can't be stunned during Dash Punch with weakness": 0x4000,
        "Can't be frozen with weakness": 0x8000,
    }
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

    def write_byte(self, offset, value) -> None:
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def adjust_palettes(world: "MMXWorld", patch: MMXProcedurePatch) -> None:
    player_palette_options = {
        "Default": world.options.palette_default.current_key,
        "Homing Torpedo": world.options.palette_homing_torpedo.current_key,
        "Chameleon Sting": world.options.palette_chameleon_sting.current_key,
        "Rolling Shield": world.options.palette_rolling_shield.current_key,
        "Fire Wave": world.options.palette_fire_wave.current_key,
        "Storm Tornado": world.options.palette_storm_tornado.current_key,
        "Electric Spark": world.options.palette_electric_spark.current_key,
        "Boomerang Cutter": world.options.palette_boomerang_cutter.current_key,
        "Shotgun Ice": world.options.palette_shotgun_ice.current_key,
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


def adjust_boss_damage_table(world: "MMXWorld", patch: MMXProcedurePatch) -> None:
    for boss, data in world.boss_weakness_data.items():
        offset = boss_weakness_offsets[boss]
        patch.write_bytes(offset, bytearray(data))

    # Fix second anglerge having different weakness
    patch.write_byte(0x12E62, 0x01)

    # Write weaknesses to a table
    offset = 0x17E9A2
    for _, entries in world.boss_weaknesses.items():
        data = [0xFF for _ in range(16)]
        i = 0
        for entry in entries:
            data[i] = entry[1]
            i += 1
        patch.write_bytes(offset, bytearray(data))
        offset += 16


def adjust_boss_hp(world: "MMXWorld", patch: MMXProcedurePatch) -> None:
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


def patch_rom(world: "MMXWorld", patch: MMXProcedurePatch) -> None:
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
    adjust_palettes(world, patch)

    if world.options.boss_randomize_hp != "off":
        adjust_boss_hp(world, patch)

    patch.write_byte(0x014FF, world.options.starting_hp.value)
    patch.write_byte(0x01DDC, 0x7F)

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
        "SHOT": 0x36E20,
        "JUMP": 0x36E21,
        "DASH": 0x36E22,
        "SELECT_L": 0x36E23,
        "SELECT_R": 0x36E24,
        "MENU": 0x36E25,
    }
    button_config = world.options.button_configuration.value
    for action, button in button_config.items():
        patch.write_byte(action_offsets[action], button_values[button])

    # Write tweaks
    enemy_tweaks_available = {
        "Chill Penguin": world.options.chill_penguin_tweaks.value,
        "Armored Armadillo": world.options.armored_armadillo_tweaks.value,
        "Spark Mandrill": world.options.spark_mandrill_tweaks.value,
    }
    for boss, offset in enemy_tweaks_offsets.items():
        selected_tweaks = enemy_tweaks_available[boss]
        final_value = 0
        for tweak in selected_tweaks:
            final_value |= enemy_tweaks_indexes[boss][tweak]
        patch.write_bytes(offset, bytearray([final_value & 0xFF, (final_value >> 8) & 0xFF]))

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
    patch.write_byte(0x167C20, value)
    patch.write_byte(0x167C21, world.options.sigma_medal_count.value)
    patch.write_byte(0x167C22, world.options.sigma_weapon_count.value)
    patch.write_byte(0x167C23, world.options.sigma_upgrade_count.value)
    patch.write_byte(0x167C24, world.options.sigma_heart_tank_count.value)
    patch.write_byte(0x167C25, world.options.sigma_sub_tank_count.value)
    patch.write_byte(0x167C26, world.options.starting_life_count.value)
    patch.write_byte(0x167C27, world.options.pickupsanity.value)
    patch.write_byte(0x167C28, world.options.energy_link.value)
    patch.write_byte(0x167C29, world.options.death_link.value)
    patch.write_byte(0x167C2A, world.options.jammed_buster.value)
    patch.write_byte(0x167C2B, world.options.logic_boss_weakness.value)
    patch.write_byte(0x167C2C, world.options.boss_weakness_rando.value)
    patch.write_byte(0x167C2D, world.options.starting_hp.value)
    patch.write_byte(0x167C2E, world.options.heart_tank_effectiveness.value)
    patch.write_byte(0x167C2F, world.options.sigma_all_levels.value)
    patch.write_byte(0x167C30, world.options.boss_weakness_strictness.value)

    value = 0
    if world.options.better_walljump.value:
        value |= 0x01
    if world.options.air_dash.value:
        value |= 0x02
    if world.options.long_jumps.value:
        value |= 0x04
    patch.write_byte(0x167C31, value)

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
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["mmx_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
