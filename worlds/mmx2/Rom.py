import Utils
import hashlib
import os

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from . import MMX2World

from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .Aesthetics import get_palette_bytes, player_palettes

STARTING_ID = 0xBE0C00

action_names = ("SHOT", "JUMP", "DASH", "SELECT_L", "SELECT_R", "MENU")
action_buttons = ("Y", "B", "A", "L", "R", "X", "START", "SELECT")

HASH_US = '67905b989b00046db06df3434ed79f04'
HASH_LEGACY = 'a8aa24df75686a5bb1a08a27d1876f5f'

weapon_rom_data = {
    STARTING_ID + 0x000B: [0x1FC1, 0xFF],
    STARTING_ID + 0x000C: [0x1FBD, 0xFF],
    STARTING_ID + 0x000D: [0x1FC9, 0xFF],
    STARTING_ID + 0x000E: [0x1FBF, 0xFF],
    STARTING_ID + 0x000F: [0x1FC7, 0xFF],
    STARTING_ID + 0x0010: [0x1FBB, 0xFF],
    STARTING_ID + 0x0011: [0x1FC3, 0xFF],
    STARTING_ID + 0x0012: [0x1FC5, 0xFF],
    STARTING_ID + 0x001A: [0x1FB1, 0x80],
}

upgrades_rom_data = {
    STARTING_ID + 0x001C: [0x00],
    STARTING_ID + 0x001D: [0x02],
    STARTING_ID + 0x001E: [0x01],
    STARTING_ID + 0x001F: [0x03],
}

boss_access_rom_data = {
    STARTING_ID + 0x0009: [0x00],
    STARTING_ID + 0x0005: [0x01],
    STARTING_ID + 0x0004: [0x03],
    STARTING_ID + 0x0006: [0x04],
    STARTING_ID + 0x0008: [0x05],
    STARTING_ID + 0x0003: [0x06],
    STARTING_ID + 0x0002: [0x08],
    STARTING_ID + 0x0007: [0x09],
    STARTING_ID + 0x000A: [0x07],
}

refill_rom_data = {
    STARTING_ID + 0x0030: ["hp refill", 2],
    STARTING_ID + 0x0031: ["hp refill", 8],
    STARTING_ID + 0x0034: ["1up", 0],
    STARTING_ID + 0x0032: ["weapon refill", 2],
    STARTING_ID + 0x0033: ["weapon refill", 8],
}

x_palette_set_offsets = {
    "Default": 0x02B100,
    "Crystal Hunter": 0x02CCA0,
    "Bubble Splash": 0x02CC60,
    "Silk Shot": 0x02CCC0,
    "Spin Wheel": 0x02CD00,
    "Sonic Slicer": 0x02CC40,
    "Strike Chain": 0x02CCE0,
    "Magnet Mine": 0x02CC20,
    "Speed Burner": 0x02CC80,
}

boss_weakness_offsets = {
    "Wheel Gator": 0x37643,
    "Bubble Crab": 0x3753A,
    "Flame Stag": 0x3761D,
    "Morph Moth": 0x376DB,
    "Magna Centipede": 0x374EE,
    "Crystal Snail": 0x37514,
    "Overdrive Ostrich": 0x375F7,
    "Wire Sponge": 0x37560,
    "Magna Quartz": 0x37DF8,
    "Chop Register": 0x37E20,
    "Raider Killer": 0x37E48,
    "Pararoid S-38": 0x37E70,
    "Agile": 0x37D80,
    "Serges": 0x37DA8,
    "Violen": 0x37DD0,
    "Neo Violen": 0x3780B,
    "Serges Tank": 0x377BF,
    "Agile Flyer": 0x377E5,
    "Zero": 0x3774D,
    "Sigma": 0x37773,
    "Sigma Virus": 0x37799,
}

boss_hp_caps_offsets = {
    "Wheel Gator": 0x1B7B0,
    "Bubble Crab": 0x3C267,
    "Flame Stag": 0x24056,
    "Morph Moth": 0x1AB86,
    "Magna Centipede": 0x22C75,
    "Crystal Snail": 0x3B521,
    "Overdrive Ostrich": 0x4690B,
    "Wire Sponge": 0x21C54,
    "Agile": 0x23E49,  # they all share the same hp
    #"Serges": 0x0,
    #"Violen": 0x0,
    "Gigantic Mechaniloid CF-0": 0x3949F,
    "Serges Tank": 0x14D4F,
    "Agile Flyer": 0xAF148,
    "Zero": 0x14BCBF,
    "Sigma": 0x15618F,
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

    def write_bytes(self, offset, value: Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

def adjust_palettes(world: "MMX2World", patch: MMX2ProcedurePatch):
    player_palette_options = {
        "Default": world.options.palette_default.current_key,
        "Crystal Hunter": world.options.palette_crystal_hunter.current_key,
        "Bubble Splash": world.options.palette_bubble_splash.current_key,
        "Silk Shot": world.options.palette_silk_shot.current_key,
        "Spin Wheel": world.options.palette_spin_wheel.current_key,
        "Sonic Slicer": world.options.palette_sonic_slicer.current_key,
        "Strike Chain": world.options.palette_strike_chain.current_key,
        "Magnet Mine": world.options.palette_magnet_mine.current_key,
        "Speed Burner": world.options.palette_speed_burner.current_key,
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


def adjust_boss_damage_table(world: "MMX2World", patch: MMX2ProcedurePatch):
    for boss, data in world.boss_weakness_data.items():
        offset = boss_weakness_offsets[boss]

        if boss == "Serges Tank":
            for x in range(len(data)):
                data[x] = data[x]*3 if data[x] < 0x80 else data[x]
        elif boss == "Wheel Gator":
            patch.write_bytes(0x37669, bytearray(data))
                
        patch.write_bytes(offset, bytearray(data))

    # Write weaknesses to a table
    offset = 0x140000
    for _, entries in world.boss_weaknesses.items():
        data = [0xFF for _ in range(16)]
        i = 0
        for entry in entries:
            data[i] = entry[1]
            i += 1
        patch.write_bytes(offset, bytearray(data))
        offset += 16


def adjust_boss_hp(world: "MMX2World", patch: MMX2ProcedurePatch):
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
        if boss == "Morph Moth":
            value = world.random.randint(ranges[0] + 1, ranges[1])
            value_2 = world.random.randint(1, value - 1)
            patch.write_byte(0x1ABB7, value_2)
            patch.write_byte(0x1B05E, value_2)
        elif boss == "Gigantic Mechaniloid CF-0":
            patch.write_byte(0x39F74, value)
        else:
            value = world.random.randint(ranges[0], ranges[1])
        patch.write_byte(offset, value)
        

def patch_rom(world: "MMX2World", patch: MMX2ProcedurePatch):
    from Utils import __version__

    # Prepare some ROM locations to receive the basepatch
    patch.write_bytes(0x00610, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x00632, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01113, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01154, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF]))
    patch.write_bytes(0x0120A, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01219, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x0123D, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x026A5, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x06A79, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x06CD5, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x06EF8, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x06EFB, bytearray([0xFF]))
    patch.write_bytes(0x06F7B, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x0919E, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0CDE2, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0CE11, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x21D47, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x22CCE, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x3944B, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x398C8, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x3A187, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x459E6, bytearray([0xFF]))
    patch.write_bytes(0x459E8, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x45C11, bytearray([0xFF]))
    patch.write_bytes(0x45C13, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x1488EF, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x149A02, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x154082, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x155CA5, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x1569BB, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x17FB5A, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x17FB62, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF]))
    patch.write_bytes(0x07E80, bytearray([0xFF for _ in range(0x120)]))
    patch.write_bytes(0x0FE80, bytearray([0xFF for _ in range(0x180)]))
    patch.write_bytes(0x17FA0, bytearray([0xFF for _ in range(0x60)]))
    patch.write_bytes(0x1FF00, bytearray([0xFF for _ in range(0x100)]))
    patch.write_bytes(0x3FF78, bytearray([0xFF for _ in range(0x88)]))
    patch.write_bytes(0x30DEC, bytearray([0xFF for _ in range(0x55)]))

    adjust_boss_damage_table(world, patch)
    adjust_palettes(world, patch)
    
    if world.options.boss_randomize_hp != "off":
        adjust_boss_hp(world, patch)

    # Edit the ROM header
    patch.name = bytearray(f'MMX2{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
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
        "SHOT": 0x371F9,
        "JUMP": 0x371FA,
        "DASH": 0x371FB,
        "SELECT_L": 0x371FC,
        "SELECT_R": 0x371FD,
        "MENU": 0x371FE,
    }
    button_config = world.options.button_configuration.value
    for action, button in button_config.items():
        patch.write_byte(action_offsets[action], button_values[button])

    # Starting HP
    patch.write_byte(0x01D6A, 0x7F)
    
    # Write options to the ROM
    value = 0
    base_open = world.options.base_open.value
    if "Medals" in base_open:
        value |= 0x01
    if "Weapons" in base_open:
        value |= 0x02
    if "Armor Upgrades" in base_open:
        value |= 0x04
    if "Heart Tanks" in base_open:
        value |= 0x08
    if "Sub Tanks" in base_open:
        value |= 0x10
    patch.write_byte(0x17FFE0, value)
    patch.write_byte(0x17FFE1, world.options.base_medal_count.value)
    patch.write_byte(0x17FFE2, world.options.base_weapon_count.value)
    patch.write_byte(0x17FFE3, world.options.base_upgrade_count.value)
    patch.write_byte(0x17FFE4, world.options.base_heart_tank_count.value)
    patch.write_byte(0x17FFE5, world.options.base_sub_tank_count.value)
    patch.write_byte(0x17FFE6, world.options.starting_life_count.value)
    patch.write_byte(0x17FFE7, world.options.pickupsanity.value)
    patch.write_byte(0x17FFE8, world.options.energy_link.value)
    patch.write_byte(0x17FFE9, world.options.death_link.value)
    patch.write_byte(0x17FFEA, world.options.jammed_buster.value)
    patch.write_byte(0x17FFED, world.options.starting_hp.value)
    patch.write_byte(0x17FFEE, world.options.heart_tank_effectiveness.value)
    patch.write_byte(0x17FFEF, world.options.base_all_levels.value)
    patch.write_byte(0x17FFEC, world.options.boss_weakness_rando.value)
    patch.write_byte(0x17FFF0, world.options.boss_weakness_strictness.value)
    patch.write_byte(0x17FFF2, world.options.x_hunters_medal_count.value)
    value = 0
    if world.options.long_jumps.value:
        value |= 0x01
    if world.options.shoryuken_use_hadouken_input.value:
        value |= 0x80
    patch.write_byte(0x17FFF1, value)
    patch.write_byte(0x17FFF3, world.options.base_boss_rematch_count.value)

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
