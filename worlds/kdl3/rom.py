import typing
from pkgutil import get_data

import Utils
from typing import Optional, TYPE_CHECKING, Tuple, Dict, List
import hashlib
import os
import struct

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from .aesthetics import get_palette_bytes, kirby_target_palettes, get_kirby_palette, gooey_target_palettes, \
    get_gooey_palette
from .compression import hal_decompress
import bsdiff4

if TYPE_CHECKING:
    from . import KDL3World

KDL3UHASH = "201e7658f6194458a3869dde36bf8ec2"
KDL3JHASH = "b2f2d004ea640c3db66df958fce122b2"

level_pointers = {
    0x770000: 0x0084,
    0x770001: 0x009C,
    0x770002: 0x00B8,
    0x770003: 0x00D8,
    0x770004: 0x0104,
    0x770005: 0x0124,
    0x770006: 0x014C,
    0x770007: 0x0170,
    0x770008: 0x0190,
    0x770009: 0x01B0,
    0x77000A: 0x01E8,
    0x77000B: 0x0218,
    0x77000C: 0x024C,
    0x77000D: 0x0270,
    0x77000E: 0x02A0,
    0x77000F: 0x02C4,
    0x770010: 0x02EC,
    0x770011: 0x0314,
    0x770012: 0x03CC,
    0x770013: 0x0404,
    0x770014: 0x042C,
    0x770015: 0x044C,
    0x770016: 0x0478,
    0x770017: 0x049C,
    0x770018: 0x04E4,
    0x770019: 0x0504,
    0x77001A: 0x0530,
    0x77001B: 0x0554,
    0x77001C: 0x05A8,
    0x77001D: 0x0640,
    0x770200: 0x0148,
    0x770201: 0x0248,
    0x770202: 0x03C8,
    0x770203: 0x04E0,
    0x770204: 0x06A4,
    0x770205: 0x06A8,
}

bb_bosses = {
    0x770200: 0xED85F1,
    0x770201: 0xF01360,
    0x770202: 0xEDA3DF,
    0x770203: 0xEDC2B9,
    0x770204: 0xED7C3F,
    0x770205: 0xEC29D2,
}

level_sprites = {
    0x19B2C6: 1827,
    0x1A195C: 1584,
    0x19F6F3: 1679,
    0x19DC8B: 1717,
    0x197900: 1872
}

stage_tiles = {
    0: [
        0, 1, 2,
        16, 17, 18,
        32, 33, 34,
        48, 49, 50
    ],
    1: [
        3, 4, 5,
        19, 20, 21,
        35, 36, 37,
        51, 52, 53
    ],
    2: [
        6, 7, 8,
        22, 23, 24,
        38, 39, 40,
        54, 55, 56
    ],
    3: [
        9, 10, 11,
        25, 26, 27,
        41, 42, 43,
        57, 58, 59,
    ],
    4: [
        12, 13, 64,
        28, 29, 65,
        44, 45, 66,
        60, 61, 67
    ],
    5: [
        14, 15, 68,
        30, 31, 69,
        46, 47, 70,
        62, 63, 71
    ]
}

heart_star_address = 0x2D0000
heart_star_size = 456
consumable_address = 0x2F91DD
consumable_size = 698

stage_palettes = [0x60964, 0x60B64, 0x60D64, 0x60F64, 0x61164]

music_choices = [
    2,  # Boss 1
    3,  # Boss 2 (Unused)
    4,  # Boss 3 (Miniboss)
    7,  # Dedede
    9,  # Event 2 (used once)
    10,  # Field 1
    11,  # Field 2
    12,  # Field 3
    13,  # Field 4
    14,  # Field 5
    15,  # Field 6
    16,  # Field 7
    17,  # Field 8
    18,  # Field 9
    19,  # Field 10
    20,  # Field 11
    21,  # Field 12 (Gourmet Race)
    23,  # Dark Matter in the Hyper Zone
    24,  # Zero
    25,  # Level 1
    26,  # Level 2
    27,  # Level 4
    28,  # Level 3
    29,  # Heart Star Failed
    30,  # Level 5
    31,  # Minigame
    38,  # Animal Friend 1
    39,  # Animal Friend 2
    40,  # Animal Friend 3
]
# extra room pointers we don't want to track other than for music
room_music = {
    3079990: 23,  # Zero
    2983409: 2,  # BB Whispy
    3150688: 2,  # BB Acro
    2991071: 2,  # BB PonCon
    2998969: 2,  # BB Ado
    2980927: 7,  # BB Dedede
    2894290: 23  # BB Zero
}

enemy_remap = {
    "Waddle Dee": 0,
    "Bronto Burt": 2,
    "Rocky": 3,
    "Bobo": 5,
    "Chilly": 6,
    "Poppy Bros Jr.": 7,
    "Sparky": 8,
    "Polof": 9,
    "Broom Hatter": 11,
    "Cappy": 12,
    "Bouncy": 13,
    "Nruff": 15,
    "Glunk": 16,
    "Togezo": 18,
    "Kabu": 19,
    "Mony": 20,
    "Blipper": 21,
    "Squishy": 22,
    "Gabon": 24,
    "Oro": 25,
    "Galbo": 26,
    "Sir Kibble": 27,
    "Nidoo": 28,
    "Kany": 29,
    "Sasuke": 30,
    "Yaban": 32,
    "Boten": 33,
    "Coconut": 34,
    "Doka": 35,
    "Icicle": 36,
    "Pteran": 39,
    "Loud": 40,
    "Como": 41,
    "Klinko": 42,
    "Babut": 43,
    "Wappa": 44,
    "Mariel": 45,
    "Tick": 48,
    "Apolo": 49,
    "Popon Ball": 50,
    "KeKe": 51,
    "Magoo": 53,
    "Raft Waddle Dee": 57,
    "Madoo": 58,
    "Corori": 60,
    "Kapar": 67,
    "Batamon": 68,
    "Peran": 72,
    "Bobin": 73,
    "Mopoo": 74,
    "Gansan": 75,
    "Bukiset (Burning)": 76,
    "Bukiset (Stone)": 77,
    "Bukiset (Ice)": 78,
    "Bukiset (Needle)": 79,
    "Bukiset (Clean)": 80,
    "Bukiset (Parasol)": 81,
    "Bukiset (Spark)": 82,
    "Bukiset (Cutter)": 83,
    "Waddle Dee Drawing": 84,
    "Bronto Burt Drawing": 85,
    "Bouncy Drawing": 86,
    "Kabu (Dekabu)": 87,
    "Wapod": 88,
    "Propeller": 89,
    "Dogon": 90,
    "Joe": 91
}

miniboss_remap = {
    "Captain Stitch": 0,
    "Yuki": 1,
    "Blocky": 2,
    "Jumper Shoot": 3,
    "Boboo": 4,
    "Haboki": 5
}

ability_remap = {
    "No Ability": 0,
    "Burning Ability": 1,
    "Stone Ability": 2,
    "Ice Ability": 3,
    "Needle Ability": 4,
    "Clean Ability": 5,
    "Parasol Ability": 6,
    "Spark Ability": 7,
    "Cutter Ability": 8,
}


class RomData:
    def __init__(self, file: bytes, name: typing.Optional[str] = None):
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytearray:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values: typing.Sequence[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)


def handle_level_sprites(stages: List[Tuple[int, ...]], sprites: List[bytearray], palettes: List[List[bytearray]]) \
        -> Tuple[List[bytearray], List[bytearray]]:
    palette_by_level = list()
    for palette in palettes:
        palette_by_level.extend(palette[10:16])
    out_palettes = list()
    for i in range(5):
        for j in range(6):
            palettes[i][10 + j] = palette_by_level[stages[i][j]]
        out_palettes.append(bytearray([x for palette in palettes[i] for x in palette]))
    tiles_by_level = list()
    for spritesheet in sprites:
        decompressed = hal_decompress(spritesheet)
        tiles = [decompressed[i:i + 32] for i in range(0, 2304, 32)]
        tiles_by_level.extend([[tiles[x] for x in stage_tiles[stage]] for stage in stage_tiles])
    out_sprites = list()
    for world in range(5):
        levels = [stages[world][x] for x in range(6)]
        world_tiles: typing.List[bytes] = [bytes() for _ in range(72)]
        for i in range(6):
            for x in range(12):
                world_tiles[stage_tiles[i][x]] = tiles_by_level[levels[i]][x]
        out_sprites.append(bytearray())
        for tile in world_tiles:
            out_sprites[world].extend(tile)
        # insert our fake compression
        out_sprites[world][0:0] = [0xe3, 0xff]
        out_sprites[world][1026:1026] = [0xe3, 0xff]
        out_sprites[world][2052:2052] = [0xe0, 0xff]
        out_sprites[world].append(0xff)
    return out_sprites, out_palettes


def write_heart_star_sprites(rom: RomData) -> None:
    compressed = rom.read_bytes(heart_star_address, heart_star_size)
    decompressed = hal_decompress(compressed)
    patch = get_data(__name__, "data/APHeartStar.bsdiff4")
    patched = bytearray(bsdiff4.patch(decompressed, patch))
    rom.write_bytes(0x1AF7DF, patched)
    patched[0:0] = [0xE3, 0xFF]
    patched.append(0xFF)
    rom.write_bytes(0x1CD000, patched)
    rom.write_bytes(0x3F0EBF, [0x00, 0xD0, 0x39])


def write_consumable_sprites(rom: RomData, consumables: bool, stars: bool) -> None:
    compressed = rom.read_bytes(consumable_address, consumable_size)
    decompressed = hal_decompress(compressed)
    patched = bytearray(decompressed)
    if consumables:
        patch = get_data(__name__, "data/APConsumable.bsdiff4")
        patched = bytearray(bsdiff4.patch(bytes(patched), patch))
    if stars:
        patch = get_data(__name__, "data/APStars.bsdiff4")
        patched = bytearray(bsdiff4.patch(bytes(patched), patch))
    patched[0:0] = [0xE3, 0xFF]
    patched.append(0xFF)
    rom.write_bytes(0x1CD500, patched)
    rom.write_bytes(0x3F0DAE, [0x00, 0xD5, 0x39])


class KDL3PatchExtensions(APPatchExtension):
    game = "Kirby's Dream Land 3"

    @staticmethod
    def apply_post_patch(_: APProcedurePatch, rom: bytes) -> bytes:
        rom_data = RomData(rom)
        write_heart_star_sprites(rom_data)
        if rom_data.read_bytes(0x3D014, 1)[0] > 0:
            stages = [struct.unpack("HHHHHHH", rom_data.read_bytes(0x3D020 + x * 14, 14)) for x in range(5)]
            palettes = [rom_data.read_bytes(full_pal, 512) for full_pal in stage_palettes]
            read_palettes = [[palette[i:i + 32] for i in range(0, 512, 32)] for palette in palettes]
            sprites = [rom_data.read_bytes(offset, level_sprites[offset]) for offset in level_sprites]
            sprites, palettes = handle_level_sprites(stages, sprites, read_palettes)
            for addr, palette in zip(stage_palettes, palettes):
                rom_data.write_bytes(addr, palette)
            for addr, level_sprite in zip([0x1CA000, 0x1CA920, 0x1CB230, 0x1CBB40, 0x1CC450], sprites):
                rom_data.write_bytes(addr, level_sprite)
            rom_data.write_bytes(0x460A, [0x00, 0xA0, 0x39, 0x20, 0xA9, 0x39, 0x30, 0xB2, 0x39, 0x40, 0xBB, 0x39,
                                          0x50, 0xC4, 0x39])
        write_consumable_sprites(rom_data, rom_data.read_byte(0x3D018) > 0, rom_data.read_byte(0x3D01A) > 0)
        return rom_data.get_bytes()


class KDL3ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [KDL3UHASH, KDL3JHASH]
    game = "Kirby's Dream Land 3"
    patch_file_ending = ".apkdl3"
    procedure = [
        ("apply_bsdiff4", ["kdl3_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_post_patch", []),
        ("calc_snes_crc", [])
    ]
    name: bytes  # used to pass to __init__

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def patch_rom(world: "KDL3World", patch: KDL3ProcedurePatch) -> None:
    patch.write_file("kdl3_basepatch.bsdiff4",
                     get_data(__name__, "data/kdl3_basepatch.bsdiff4"))

    # Write open world patch
    if world.options.open_world:
        patch.write_token(APTokenTypes.WRITE, 0x143C7, bytes([0xAD, 0xC1, 0x5A, 0xCD, 0xC1, 0x5A, ]))
        # changes the stage flag function to compare $5AC1 to $5AC1,
        # always running the "new stage" function
        # This has further checks present for bosses already, so we just
        # need to handle regular stages
        # write check for boss to be unlocked

    if world.options.consumables:
        # reroute maxim tomatoes to use the 1-UP function, then null out the function
        patch.write_token(APTokenTypes.WRITE, 0x3002F, bytes([0x37, 0x00]))
        patch.write_token(APTokenTypes.WRITE, 0x30037, bytes([0xA9, 0x26, 0x00,  # LDA #$0026
                                                              0x22, 0x27, 0xD9, 0x00,  # JSL $00D927
                                                              0xA4, 0xD2,  # LDY $D2
                                                              0x6B,  # RTL
                                                              0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA,
                                                              0xEA,  # NOP #10
                                                              ]))

    # stars handling is built into the rom, so no changes there

    rooms = world.rooms
    if world.options.music_shuffle > 0:
        if world.options.music_shuffle == 1:
            shuffled_music = music_choices.copy()
            world.random.shuffle(shuffled_music)
            music_map = dict(zip(music_choices, shuffled_music))
            # Avoid putting star twinkle in the pool
            music_map[5] = world.random.choice(music_choices)
            # Heart Star music doesn't work on regular stages
            music_map[8] = world.random.choice(music_choices)
            for room in rooms:
                room.music = music_map[room.music]
            for room_ptr in room_music:
                patch.write_token(APTokenTypes.WRITE, room_ptr + 2, bytes([music_map[room_music[room_ptr]]]))
            for i, old_music in zip(range(5), [25, 26, 28, 27, 30]):
                # level themes
                patch.write_token(APTokenTypes.WRITE, 0x133F2 + i, bytes([music_map[old_music]]))
            # Zero
            patch.write_token(APTokenTypes.WRITE, 0x9AE79, music_map[0x18].to_bytes(1, "little"))
            # Heart Star success and fail
            patch.write_token(APTokenTypes.WRITE, 0x4A388, music_map[0x08].to_bytes(1, "little"))
            patch.write_token(APTokenTypes.WRITE, 0x4A38D, music_map[0x1D].to_bytes(1, "little"))
        elif world.options.music_shuffle == 2:
            for room in rooms:
                room.music = world.random.choice(music_choices)
            for room_ptr in room_music:
                patch.write_token(APTokenTypes.WRITE, room_ptr + 2,
                                  world.random.choice(music_choices).to_bytes(1, "little"))
            for i in range(5):
                # level themes
                patch.write_token(APTokenTypes.WRITE, 0x133F2 + i,
                                  world.random.choice(music_choices).to_bytes(1, "little"))
            # Zero
            patch.write_token(APTokenTypes.WRITE, 0x9AE79, world.random.choice(music_choices).to_bytes(1, "little"))
            # Heart Star success and fail
            patch.write_token(APTokenTypes.WRITE, 0x4A388, world.random.choice(music_choices).to_bytes(1, "little"))
            patch.write_token(APTokenTypes.WRITE, 0x4A38D, world.random.choice(music_choices).to_bytes(1, "little"))

    for room in rooms:
        room.patch(patch, bool(world.options.consumables.value), not bool(world.options.remote_items.value))

    if world.options.virtual_console in [1, 3]:
        # Flash Reduction
        patch.write_token(APTokenTypes.WRITE, 0x9AE68, b"\x10")
        patch.write_token(APTokenTypes.WRITE, 0x9AE8E, bytes([0x08, 0x00, 0x22, 0x5D, 0xF7, 0x00, 0xA2, 0x08, ]))
        patch.write_token(APTokenTypes.WRITE, 0x9AEA1, b"\x08")
        patch.write_token(APTokenTypes.WRITE, 0x9AEC9, b"\x01")
        patch.write_token(APTokenTypes.WRITE, 0x9AED2, bytes([0xA9, 0x1F]))
        patch.write_token(APTokenTypes.WRITE, 0x9AEE1, b"\x08")

    if world.options.virtual_console in [2, 3]:
        # Hyper Zone BB colors
        patch.write_token(APTokenTypes.WRITE, 0x2C5E16, bytes([0xEE, 0x1B, 0x18, 0x5B, 0xD3, 0x4A, 0xF4, 0x3B, ]))
        patch.write_token(APTokenTypes.WRITE, 0x2C8217, bytes([0xFF, 0x1E, ]))

    # boss requirements
    patch.write_token(APTokenTypes.WRITE, 0x3D000,
                      struct.pack("HHHHH", world.boss_requirements[0], world.boss_requirements[1],
                                  world.boss_requirements[2], world.boss_requirements[3],
                                  world.boss_requirements[4]))
    patch.write_token(APTokenTypes.WRITE, 0x3D00A,
                      struct.pack("H", world.required_heart_stars if world.options.goal_speed == 1 else 0xFFFF))
    patch.write_token(APTokenTypes.WRITE, 0x3D00C, world.options.goal_speed.value.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D00E, world.options.open_world.value.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D010, ((world.options.remote_items.value << 1) +
                                                    world.options.death_link.value).to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D012, world.options.goal.value.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D014, world.options.stage_shuffle.value.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D016, world.options.ow_boss_requirement.value.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D018, world.options.consumables.value.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D01A, world.options.starsanity.value.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D01C, world.options.gifting.value.to_bytes(2, "little"))
    patch.write_token(APTokenTypes.WRITE, 0x3D01E, world.options.strict_bosses.value.to_bytes(2, "little"))
    # don't write gifting for solo game, since there's no one to send anything to

    for level in world.player_levels:
        for i in range(len(world.player_levels[level])):
            patch.write_token(APTokenTypes.WRITE, 0x3F002E + ((level - 1) * 14) + (i * 2),
                              struct.pack("H", level_pointers[world.player_levels[level][i]]))
            patch.write_token(APTokenTypes.WRITE, 0x3D020 + (level - 1) * 14 + (i * 2),
                              struct.pack("H", world.player_levels[level][i] & 0x00FFFF))
            if (i == 0) or (i > 0 and i % 6 != 0):
                patch.write_token(APTokenTypes.WRITE, 0x3D080 + (level - 1) * 12 + (i * 2),
                                  struct.pack("H", (world.player_levels[level][i] & 0x00FFFF) % 6))

    for i in range(6):
        if world.boss_butch_bosses[i]:
            patch.write_token(APTokenTypes.WRITE, 0x3F0000 + (level_pointers[0x770200 + i]),
                              struct.pack("I", bb_bosses[0x770200 + i]))

    # copy ability shuffle
    if world.options.copy_ability_randomization.value > 0:
        for enemy in world.copy_abilities:
            if enemy in miniboss_remap:
                patch.write_token(APTokenTypes.WRITE, 0xB417E + (miniboss_remap[enemy] << 1),
                                  struct.pack("H", ability_remap[world.copy_abilities[enemy]]))
            else:
                patch.write_token(APTokenTypes.WRITE, 0xB3CAC + (enemy_remap[enemy] << 1),
                                  struct.pack("H", ability_remap[world.copy_abilities[enemy]]))
        # following only needs done on non-door rando
        # incredibly lucky this follows the same order (including 5E == star block)
        patch.write_token(APTokenTypes.WRITE, 0x2F77EA,
                          (0x5E + (ability_remap[world.copy_abilities["Sparky"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2F7811,
                          (0x5E + (ability_remap[world.copy_abilities["Sparky"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2F9BC4,
                          (0x5E + (ability_remap[world.copy_abilities["Blocky"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2F9BEB,
                          (0x5E + (ability_remap[world.copy_abilities["Blocky"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2FAC06,
                          (0x5E + (ability_remap[world.copy_abilities["Jumper Shoot"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2FAC2D,
                          (0x5E + (ability_remap[world.copy_abilities["Jumper Shoot"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2F9E7B,
                          (0x5E + (ability_remap[world.copy_abilities["Yuki"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2F9EA2,
                          (0x5E + (ability_remap[world.copy_abilities["Yuki"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2FA951,
                          (0x5E + (ability_remap[world.copy_abilities["Sir Kibble"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2FA978,
                          (0x5E + (ability_remap[world.copy_abilities["Sir Kibble"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2FA132,
                          (0x5E + (ability_remap[world.copy_abilities["Haboki"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2FA159,
                          (0x5E + (ability_remap[world.copy_abilities["Haboki"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2FA3E8,
                          (0x5E + (ability_remap[world.copy_abilities["Boboo"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2FA40F,
                          (0x5E + (ability_remap[world.copy_abilities["Boboo"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2F90E2,
                          (0x5E + (ability_remap[world.copy_abilities["Captain Stitch"]] << 1)).to_bytes(1, "little"))
        patch.write_token(APTokenTypes.WRITE, 0x2F9109,
                          (0x5E + (ability_remap[world.copy_abilities["Captain Stitch"]] << 1)).to_bytes(1, "little"))

        if world.options.copy_ability_randomization == 2:
            for enemy in enemy_remap:
                # we just won't include it for minibosses
                patch.write_token(APTokenTypes.WRITE, 0xB3E40 + (enemy_remap[enemy] << 1),
                                  struct.pack("h", world.random.randint(-1, 2)))

    # write jumping goal
    patch.write_token(APTokenTypes.WRITE, 0x94F8, struct.pack("H", world.options.jumping_target))
    patch.write_token(APTokenTypes.WRITE, 0x944E, struct.pack("H", world.options.jumping_target))

    from Utils import __version__
    patch_name = bytearray(
        f'KDL3{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch_name.extend([0] * (21 - len(patch_name)))
    patch.name = bytes(patch_name)
    patch.write_token(APTokenTypes.WRITE, 0x3C000, patch.name)
    patch.write_token(APTokenTypes.WRITE, 0x3C020, world.options.game_language.value.to_bytes(1, "little"))

    patch.write_token(APTokenTypes.COPY, 0x7FC0, (21, 0x3C000))
    patch.write_token(APTokenTypes.COPY, 0x7FD9, (1, 0x3C020))

    # handle palette
    if world.options.kirby_flavor_preset.value != 0:
        for addr in kirby_target_palettes:
            target = kirby_target_palettes[addr]
            palette = get_kirby_palette(world)
            if palette is not None:
                patch.write_token(APTokenTypes.WRITE, addr, get_palette_bytes(palette, target[0], target[1], target[2]))

    if world.options.gooey_flavor_preset.value != 0:
        for addr in gooey_target_palettes:
            target = gooey_target_palettes[addr]
            palette = get_gooey_palette(world)
            if palette is not None:
                patch.write_token(APTokenTypes.WRITE, addr, get_palette_bytes(palette, target[0], target[1], target[2]))

    patch.write_file("token_patch.bin", patch.get_token_binary())


def get_base_rom_bytes() -> bytes:
    rom_file: str = get_base_rom_path()
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        base_rom_bytes = bytes(Utils.read_snes_rom(open(rom_file, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {KDL3UHASH, KDL3JHASH}:
            raise Exception("Supplied Base Rom does not match known MD5 for US or JP release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from . import KDL3World
    if not file_name:
        file_name = KDL3World.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
