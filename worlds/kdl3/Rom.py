import typing
from pkgutil import get_data
from random import Random

import Utils
from typing import Optional, Dict, List
import hashlib
import os
import struct

from BaseClasses import MultiWorld
from worlds.Files import APDeltaPatch
from .Aesthetics import get_palette_bytes, kirby_target_palettes, get_kirby_palette, gooey_target_palettes, \
    get_gooey_palette
from .Compression import hal_decompress
import bsdiff4

from .Room import Room

KDL3UHASH = "201e7658f6194458a3869dde36bf8ec2"
KDL3JHASH = "b2f2d004ea640c3db66df958fce122b2"

level_pointers = {
    0x770001: 0x0084,
    0x770002: 0x009C,
    0x770003: 0x00B8,
    0x770004: 0x00D8,
    0x770005: 0x0104,
    0x770006: 0x0124,
    0x770007: 0x014C,
    0x770008: 0x0170,
    0x770009: 0x0190,
    0x77000A: 0x01B0,
    0x77000B: 0x01E8,
    0x77000C: 0x0218,
    0x77000D: 0x024C,
    0x77000E: 0x0270,
    0x77000F: 0x02A0,
    0x770010: 0x02C4,
    0x770011: 0x02EC,
    0x770012: 0x0314,
    0x770013: 0x03CC,
    0x770014: 0x0404,
    0x770015: 0x042C,
    0x770016: 0x044C,
    0x770017: 0x0478,
    0x770018: 0x049C,
    0x770019: 0x04E4,
    0x77001A: 0x0504,
    0x77001B: 0x0530,
    0x77001C: 0x0554,
    0x77001D: 0x05A8,
    0x77001E: 0x0640,
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
room_pointers = [
    3079990,  # Zero
    2983409,  # BB Whispy
    3150688,  # BB Acro
    2991071,  # BB PonCon
    2998969,  # BB Ado
    2980927,  # BB Dedede
    2894290  # BB Zero
]

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
    def __init__(self, file: str, name: typing.Optional[str] = None):
        self.file = bytearray()
        self.read_from_file(file)
        self.name = name

    def read_byte(self, offset: int):
        return self.file[offset]

    def read_bytes(self, offset: int, length: int):
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int):
        self.file[offset] = value

    def write_bytes(self, offset: int, values: typing.Sequence) -> None:
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file: str):
        with open(file, 'wb') as outfile:
            outfile.write(self.file)

    def read_from_file(self, file: str):
        with open(file, 'rb') as stream:
            self.file = bytearray(stream.read())

    def write_crc(self):
        crc = (sum(self.file[:0x7FDC] + self.file[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])


def handle_level_sprites(stages, sprites, palettes):
    palette_by_level = list()
    for palette in palettes:
        palette_by_level.extend(palette[10:16])
    for i in range(5):
        for j in range(6):
            palettes[i][10 + j] = palette_by_level[stages[i][j] - 1]
        palettes[i] = [x for palette in palettes[i] for x in palette]
    tiles_by_level = list()
    for spritesheet in sprites:
        decompressed = hal_decompress(spritesheet)
        tiles = [decompressed[i:i + 32] for i in range(0, 2304, 32)]
        tiles_by_level.extend([[tiles[x] for x in stage_tiles[stage]] for stage in stage_tiles])
    for world in range(5):
        levels = [stages[world][x] - 1 for x in range(6)]
        world_tiles: typing.List[typing.Optional[bytes]] = [None for _ in range(72)]
        for i in range(6):
            for x in range(12):
                world_tiles[stage_tiles[i][x]] = tiles_by_level[levels[i]][x]
        sprites[world] = list()
        for tile in world_tiles:
            sprites[world].extend(tile)
        # insert our fake compression
        sprites[world][0:0] = [0xe3, 0xff]
        sprites[world][1026:1026] = [0xe3, 0xff]
        sprites[world][2052:2052] = [0xe0, 0xff]
        sprites[world].append(0xff)
    return sprites, palettes


def write_heart_star_sprites(rom: RomData):
    compressed = rom.read_bytes(heart_star_address, heart_star_size)
    decompressed = hal_decompress(compressed)
    patch = get_data(__name__, os.path.join("data", "APHeartStar.bsdiff4"))
    patched = bytearray(bsdiff4.patch(decompressed, patch))
    rom.write_bytes(0x1AF7DF, patched)
    patched[0:0] = [0xE3, 0xFF]
    patched.append(0xFF)
    rom.write_bytes(0x1CD000, patched)
    rom.write_bytes(0x3F0EBF, [0x00, 0xD0, 0x39])


def write_consumable_sprites(rom: RomData):
    compressed = rom.read_bytes(consumable_address, consumable_size)
    decompressed = hal_decompress(compressed)
    patch = get_data(__name__, os.path.join("data", "APConsumable.bsdiff4"))
    patched = bytearray(bsdiff4.patch(decompressed, patch))
    patched[0:0] = [0xE3, 0xFF]
    patched.append(0xFF)
    rom.write_bytes(0x1CD500, patched)
    rom.write_bytes(0x3F0DAE, [0x00, 0xD5, 0x39])


class KDL3DeltaPatch(APDeltaPatch):
    hash = [KDL3UHASH, KDL3JHASH]
    game = "Kirby's Dream Land 3"
    patch_file_ending = ".apkdl3"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def patch(self, target: str):
        super().patch(target)
        rom = RomData(target)
        target_language = rom.read_byte(0x3C020)
        rom.write_byte(0x7FD9, target_language)
        write_heart_star_sprites(rom)
        if rom.read_bytes(0x3D014, 1)[0] > 0:
            stages = [struct.unpack("HHHHHHH", rom.read_bytes(0x3D020 + x * 14, 14)) for x in range(5)]
            palettes = [rom.read_bytes(full_pal, 512) for full_pal in stage_palettes]
            palettes = [[palette[i:i + 32] for i in range(0, 512, 32)] for palette in palettes]
            sprites = [rom.read_bytes(offset, level_sprites[offset]) for offset in level_sprites]
            sprites, palettes = handle_level_sprites(stages, sprites, palettes)
            for addr, palette in zip(stage_palettes, palettes):
                rom.write_bytes(addr, palette)
            for addr, level_sprite in zip([0x1CA000, 0x1CA920, 0x1CB230, 0x1CBB40, 0x1CC450], sprites):
                rom.write_bytes(addr, level_sprite)
            rom.write_bytes(0x460A, [0x00, 0xA0, 0x39, 0x20, 0xA9, 0x39, 0x30, 0xB2, 0x39, 0x40, 0xBB, 0x39,
                                     0x50, 0xC4, 0x39])
        if rom.read_bytes(0x3D018, 1)[0] > 0:
            write_consumable_sprites(rom)
        rom_name = rom.read_bytes(0x3C000, 21)
        rom.write_bytes(0x7FC0, rom_name)
        rom.write_crc()
        rom.write_to_file(target)


def patch_rom(multiworld: MultiWorld, player: int, rom: RomData, heart_stars_required: int,
              boss_requirements: Dict[int, int], shuffled_levels: Dict[int, List[int]], bb_boss_enabled: List[bool],
              copy_abilities: Dict[str, str], slot_random: Random):
    # increase BWRAM by 0x8000
    rom.write_byte(0x7FD8, 0x06)

    # hook BWRAM initialization for initializing our new BWRAM
    rom.write_bytes(0x33, [0x22, 0x00, 0x9E, 0x07, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, ])  # JSL $079E00, NOP the rest

    # Initialize BWRAM with ROM parameters
    rom.write_bytes(0x39E00, [0xA0, 0x01, 0x60,  # LDA #$6001 starting addr
                              0xA9, 0xFE, 0x1F,  # LDY #$1FFE bytes to write
                              0x54, 0x40, 0x40,  # MVN $40, $40 copy $406000 from 406001 to 407FFE
                              0xA2, 0x00, 0x00,  # LDX #$0000
                              0xA0, 0x14, 0x00,  # LDY #$0014
                              0xBD, 0x00, 0x81,  # LDA $8100, X - rom header
                              0xDF, 0x00, 0xC0, 0x07,  # CMP $07C000, X - compare to real rom name
                              0xD0, 0x06,  # BNE $079E1E - area is uninitialized or corrupt, reset
                              0xE8,  # INX
                              0x88,  # DEY
                              0x30, 0x2C,  # BMI $079E48 - if Y is negative, rom header matches, valid bwram
                              0x80, 0xF1,  # BRA $079E0F - else continue loop
                              0xA9, 0x00, 0x00,  # LDA #$0000
                              0x8D, 0x00, 0x80,  # STA $8000 - initialize first byte that gets copied
                              0xA2, 0x00, 0x80,  # LDX #$8000
                              0xA0, 0x01, 0x80,  # LDY #$8001
                              0xA9, 0xFD, 0x7F,  # LDA #$7FFD
                              0x54, 0x40, 0x40,  # MVN $40, $40 - initialize 0x8000 onward
                              0xA2, 0x00, 0xD0,  # LDX #$D000 - seed info 0x3D000
                              0xA0, 0x00, 0x90,  # LDY #$9000 - target location
                              0xA9, 0x00, 0x10,  # LDA #$1000
                              0x54, 0x40, 0x07,  # MVN $07, $40
                              0xA2, 0x00, 0xC0,  # LDX #$C000 - ROM name
                              0xA0, 0x00, 0x81,  # LDY #$8100 - target
                              0xA9, 0x15, 0x00,  # LDA #$0015
                              0x54, 0x40, 0x07,  # MVN $07, $40
                              0x6B,  # RTL
                              ])

    # Copy Ability
    rom.write_bytes(0x399A0, [0xB9, 0xF3, 0x54,  # LDA $54F3
                              0x48,  # PHA
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0x68,  # PLA
                              0xDD, 0x20, 0x80,  # CMP $7F50, X
                              0xEA, 0xEA,  # NOP NOP
                              0xF0, 0x03,  # BEQ $0799B1
                              0xA9, 0x00, 0x00,  # LDA #$0000
                              0x99, 0xA9, 0x54,  # STA $54A9, Y
                              0x6B,  # RET
                              0xEA, 0xEA, 0xEA, 0xEA,  # NOPs to fill gap
                              0x48,  # PHA
                              0x0A,  # ASL
                              0xA8,  # TAX
                              0x68,  # PLA
                              0xD9, 0x20, 0x80,  # CMP $7F50, Y
                              0xEA,  # NOP
                              0xF0, 0x03,  # BEQ $0799C6
                              0xA9, 0x00, 0x00,  # LDA #$0000
                              0x9D, 0xA9, 0x54,  # STA $54A9, X
                              0x9D, 0xDF, 0x39,  # STA $39DF, X
                              0x6B,  # RET
                              ])

    # Kirby/Gooey Copy Ability
    rom.write_bytes(0x30518, [0x22, 0xA0, 0x99, 0x07, 0xEA, 0xEA, ])  # JSL $0799A0

    # Animal Copy Ability
    rom.write_bytes(0x507E8, [0x22, 0xB9, 0x99, 0x07, 0xEA, 0xEA, ])  # JSL $0799B0

    # Entity Spawn
    rom.write_bytes(0x21CD7, [0x22, 0x00, 0x9D, 0x07, ])  # JSL $079D00

    # Check Spawn Animal
    rom.write_bytes(0x39D00, [0x48,  # PHA
                              0xE0, 0x02, 0x00,  # CPX #$0002  - is this an animal friend?
                              0xD0, 0x0C,  # BNE $079D12
                              0xEB,  # XBA
                              0x48,  # PHA
                              0x0A,  # ASL
                              0xA8,  # TAY
                              0x68,  # PLA
                              0x1A,  # INC
                              0xD9, 0x00, 0x80,  # CMP $8000, Y - do we have this animal friend
                              0xF0, 0x01,  # BEQ $079D12 - we have this animal friend
                              0xE8,  # INX
                              0x7A,  # PLY
                              0xA9, 0x99, 0x99,  # LDA #$9999
                              0x6B,  # RTL
                              ])

    # Allow Purification
    rom.write_bytes(0xAFC8, [0x22, 0x00, 0x9A, 0x07,  # JSL $079A00
                             0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, ])

    # Check Purification and Enable Sub-games
    rom.write_bytes(0x39A00, [0x8A,  # TXA
                              0xC9, 0x00, 0x00,  # CMP #$0000 - is this level 1
                              0xF0, 0x03,  # BEQ $079A09
                              0x4A,  # LSR
                              0x4A,  # LSR
                              0x1A,  # INC
                              0xAA,  # TAX
                              0xAD, 0x70, 0x80,  # LDA $8070 - heart stars
                              0x18,  # CLC
                              0xCF, 0x0A, 0xD0, 0x07,  # Compare to goal heart stars
                              0x90, 0x28,  # BCC $079A3C - we don't have enough
                              0xDA,  # PHX
                              0xA9, 0x14, 0x00,  # LDA #$0014
                              0x8D, 0x62, 0x7F,  # STA #$7F62 - play sound fx 0x14
                              0xAF, 0x12, 0xD0, 0x07,  # LDA $07D012 - goal
                              0xC9, 0x00, 0x00,  # CMP #$0000 - are we on zero goal?
                              0xF0, 0x11,  # BEQ $079A35 - we are
                              0xA9, 0x01, 0x00,  # LDA #$0001
                              0xAE, 0x17, 0x36,  # LDX $3617 - current save
                              0x9D, 0xDD, 0x53,  # STA $53DD - boss butch
                              0x9D, 0xDF, 0x53,  # STA $53DF - MG5
                              0x9D, 0xE1, 0x53,  # STA $53E1 - Jumping
                              0x80, 0x06,  # BRA $079A3B
                              0xA9, 0x01, 0x00,  # LDA #$0001
                              0x8D, 0xA0, 0x80,  # STA $80A0 - zero unlock address
                              0xFA,  # PLX
                              0xAD, 0x70, 0x80,  # LDA $8070 - current heart stars
                              0xDF, 0x00, 0xD0, 0x07,  # CMP $07D000, X - compare to world heart stars
                              0xB0, 0x02,  # BCS $079A47
                              0x18,  # CLC
                              0x6B,  # RTL
                              0x38,  # SEC
                              0x6B,  # RTL
                              ])

    # Check for Sound on Main Loop
    rom.write_bytes(0x6AE4, [0x22, 0x00, 0x9B, 0x07, 0xEA])  # JSL $079B00

    # Play Sound Effect at given address and check/update traps
    rom.write_bytes(0x39B00, [0x85, 0xD4,  # STA $D4
                              0xEE, 0x24, 0x35,  # INC $3524
                              0xEA,  # NOP
                              0xAD, 0x62, 0x7F,  # LDA $7F62 - sfx to be played
                              0xF0, 0x07,  # BEQ $079B12 - skip if 0
                              0x22, 0x27, 0xD9, 0x00,  # JSL $00D927 - play sfx
                              0x9C, 0x62, 0x7F,  # STZ $7F62
                              0xAD, 0xD0, 0x36,  # LDA $36D0
                              0xC9, 0xFF, 0xFF,  # CMP #$FFFF - are we in menus?
                              0xF0, 0x34,  # BEQ $079B4E - return if we are
                              0xAD, 0x41, 0x55,  # LDA $5541 - gooey status
                              0x10, 0x0F,  # BPL $079B2E - gooey is already spawned
                              0xAD, 0x80, 0x80,  # LDA $8080
                              0xC9, 0x00, 0x00,  # CMP #$0000 - did we get a gooey trap
                              0xF0, 0x07,  # BEQ $079B2E - branch if we did not
                              0x22, 0x80, 0xA1, 0x07,  # JSL $07A180 - spawn gooey
                              0x9C, 0x80, 0x80,  # STZ $8080
                              0xAD, 0x82, 0x80,  # LDA $8082 - slowness
                              0xF0, 0x04,  # BEQ $079B37 - are we under the effects of a slowness trap
                              0x3A,  # DEC
                              0x8D, 0x82, 0x80,  # STA $8082 - dec by 1 each frame
                              0xDA,  # PHX
                              0x5A,  # PHY
                              0xAD, 0xA9, 0x54,  # LDA $54A9 - copy ability
                              0xF0, 0x0E,  # BEQ $079B4C - branch if we do not have a copy ability
                              0xAD, 0x84, 0x80,  # LDA $8084 - eject ability
                              0xF0, 0x09,  # BEQ $079B4C - branch if we haven't received eject
                              0xA9, 0x00, 0x20,  # LDA #$2000 - select button press
                              0x8D, 0xC1, 0x60,  # STA $60C1 - write to controller mirror
                              0x9C, 0x84, 0x80,  # STZ $8084
                              0x7A,  # PLY
                              0xFA,  # PLX
                              0x6B,  # RTL
                              ])

    # Dedede - Remove bad ending
    rom.write_byte(0xB013, 0x38)  # Change CLC to SEC

    # Heart Star Graphics Fix
    rom.write_bytes(0x39B50, [0xA9, 0x00, 0x00,  # LDA #$0000
                              0xDA,  # PHX
                              0x5A,  # PHY
                              0xAE, 0x3F, 0x36,  # LDX $363F - current level
                              0xAC, 0x41, 0x36,  # LDY $3641 - current stage
                              0xE0, 0x00, 0x00,  # CPX #$0000
                              0xF0, 0x09,  # BEQ $079B69
                              0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A,  # INC x6
                              0xCA,  # DEX
                              0x80, 0xF2,  # BRA $079B5B - return to loop head
                              0xC0, 0x00, 0x00,  # CPY #$0000
                              0xF0, 0x04,  # BEQ $079B72
                              0x1A,  # INC
                              0x88,  # DEY
                              0x80, 0xF7,  # BRA $079B69 - return to loop head
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBF, 0x80, 0xD0, 0x07,  # LDA $079D080, X - table of original stage number
                              0xC9, 0x03, 0x00,  # CMP #$0003 - is the current stage a minigame stage?
                              0xF0, 0x03,  # BEQ $079B80 - branch if so
                              0x18,  # CLC
                              0x80, 0x01,  # BRA $079B81
                              0x38,  # SEC
                              0x7A,  # PLY
                              0xFA,  # PLX
                              0x6B,  # RTL
                              ])

    # Reroute Heart Star Graphic Check
    rom.write_bytes(0x4A01F, [0x22, 0x50, 0x9B, 0x07, 0xEA, 0xEA, 0xB0, ])  # 1-Ups
    rom.write_bytes(0x4A0AE, [0x22, 0x50, 0x9B, 0x07, 0xEA, 0xEA, 0x90, ])  # Heart Stars

    # reroute 5-6 miniboss music override
    rom.write_bytes(0x93238, [0x22, 0x80, 0x9F, 0x07, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xB0,
                              ])
    rom.write_bytes(0x39F80, [0xEA,
                              0xDA,  # PHX
                              0x5A,  # PHY
                              0xA9, 0x00, 0x00,  # LDA #0000
                              0xAE, 0x3F, 0x36,  # LDX $363F
                              0xAC, 0x41, 0x36,  # LDY $3641
                              0xE0, 0x00, 0x00,  # CPX #$0000
                              0xF0, 0x0A,  # BEQ $079F9B
                              0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A,  # INC x6
                              0xCA,  # DEX
                              0x80, 0xF1,  # BRA $079F8C - return to loop head
                              0xC0, 0x00, 0x00,  # CPY #$0000
                              0xF0, 0x04,  # BEQ $079FA4
                              0x1A,  # INC
                              0x88,  # DEY
                              0x80, 0xF7,  # BRA $079F9B - return to loop head
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBF, 0x20, 0xD0, 0x07,  # LDA $07D020, X
                              0xC9, 0x1E, 0x00,  # CMP #$001E
                              0xF0, 0x03,  # BEQ $079FB2
                              0x18,  # CLC
                              0x80, 0x01,  # BRA $079FB3
                              0x38,  # SEC
                              0x7A,  # PLY
                              0xFA,  # PLX
                              0x6B,  # RTL
                              ])
    # reroute zero eligibility
    rom.write_bytes(0x137B1, [0xA0, 0x80, 0xC9, 0x01, ])  # compare $80A0 to #$0001 for validating zero access

    # set goal on non-fast goal
    rom.write_bytes(0x14463, [0x22, 0x00, 0x9F, 0x07, 0xEA, 0xEA, ])
    rom.write_bytes(0x39F00, [0xDA,  # PHX
                              0xAF, 0x12, 0xD0, 0x07,  # LDA $07D012
                              0xC9, 0x00, 0x00,  # CMP #$0000
                              0xF0, 0x11,  # BEQ $079F1B
                              0xA9, 0x01, 0x00,  # LDA #$0001
                              0xAE, 0x17, 0x36,  # LDX $3617 - current save
                              0x9D, 0xDD, 0x53,  # STA $53DD, X - Boss butch
                              0x9D, 0xDF, 0x53,  # STA $53DF, X - MG5
                              0x9D, 0xD1, 0x53,  # STA $53D1, X - Jumping
                              0x80, 0x06,  # BRA $079F21
                              0xA9, 0x01, 0x00,  # LDA #$0001
                              0x8D, 0xA0, 0x80,  # STA $80A0
                              0xFA,  # PLX
                              0xA9, 0x06, 0x00,  # LDA #$0006
                              0x8D, 0xC1, 0x5A,  # STA $5AC1 - cutscene
                              0x6B,  # RTL
                              ])

    # set flag for completing a stage
    rom.write_bytes(0x1439D, [0x22, 0x80, 0xA0, 0x07, 0xEA, 0xEA, ])
    rom.write_bytes(0x3A080, [0xDA,  # PHX
                              0xAD, 0xC1, 0x5A,  # LDA $5AC1 - completed stage cutscene
                              0xF0, 0x38,  # BEQ $07A0BE - we have not completed a stage
                              0xA9, 0x00, 0x00,  # LDA #$0000
                              0xAE, 0xCF, 0x53,  # LDX $53CF - current level
                              0xE0, 0x00, 0x00,  # CPX #$0000
                              0xF0, 0x0A,  # BEQ $07A09B
                              0xCA,  # DEX
                              0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A, 0x1A,  # INC x6
                              0x80, 0xF1,  # BRA $07A08C - return to loop head
                              0xAE, 0xD3, 0x53,  # LDX $53D3 - current stage
                              0xE0, 0x07, 0x00,  # CPX #$0007 - is this a boss stage
                              0xF0, 0x1B,  # BEQ $07A0BE - return if so
                              0xCA,  # DEX
                              0xE0, 0x00, 0x00,  # CPX #$0000
                              0xF0, 0x04,  # BEQ $07A0AD
                              0x1A,  # INC
                              0xCA,  # DEX
                              0x80, 0xF7,  # BRA $07A0A4 - return to loop head
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBD, 0x20, 0x90,  # LDA $9020, X - load the stage we completed
                              0x3A,  # DEC
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xA9, 0x01, 0x00,  # LDA #$0001
                              0x1D, 0x00, 0x82,  # ORA $8200, X
                              0x9D, 0x00, 0x82,  # STA $8200, X
                              0xFA,  # PLX
                              0xAD, 0xCF, 0x53,  # LDA $53CF
                              0xCD, 0xCB, 0x53,  # CMP $53CB
                              0x6B,  # RTL
                              ])

    # spawn Gooey for Gooey trap
    rom.write_bytes(0x3A180, [0x5A, 0xDA, 0xA2, 0x00, 0x00, 0xA0, 0x00, 0x00, 0x8D, 0x43, 0x55, 0xB9, 0x22, 0x19, 0x85,
                              0xC0, 0xB9, 0xA2, 0x19, 0x85, 0xC2, 0xA9, 0x08, 0x00, 0x85, 0xC4, 0xA9, 0x02, 0x00, 0x8D,
                              0x2A, 0x35, 0xA9, 0x03, 0x00, 0x22, 0x4F, 0xF5, 0x00, 0x8E, 0x41, 0x55, 0xA9, 0xFF, 0xFF,
                              0x9D, 0x22, 0x06, 0x22, 0xEF, 0xBA, 0x00, 0x22, 0x3C, 0x88, 0xC4, 0xAE, 0xD1, 0x39, 0xE0,
                              0x01, 0x00, 0xF0, 0x0D, 0xA9, 0xFF, 0xFF, 0xE0, 0x02, 0x00, 0xF0, 0x01, 0x3A, 0x22, 0x22,
                              0x3C, 0xC4, 0xFA, 0x7A, 0x6B, ])
    # this is mostly just a copy of the function to spawn gooey when you press the A button, could probably be simpler

    # limit player speed when speed trap enabled
    rom.write_bytes(0x3A200, [0xDA,  # PHX
                              0xAE, 0x82, 0x80,  # LDX $8082 - do we have slowness
                              0xF0, 0x01,  # BEQ $07A207 - branch if we do not
                              0x4A,  # LSR
                              0xFA,  # PLX
                              0x99, 0x22, 0x1F,  # STA $1F22, Y - player max speed
                              0x49, 0xFF, 0xFF,  # EOR #$FFFF
                              0x6B,  # RTL
                              ])
    rom.write_bytes(0x785E, [0x22, 0x00, 0xA2, 0x07, 0xEA, 0xEA, ])

    # write heart star count
    rom.write_bytes(0x2246, [0x0D, 0xDA, 0xBD, 0xA0, 0x6C, 0xAA, 0xBD, 0x22, 0x6E, 0x20, 0x5B, 0xA2, 0xFA, 0xE8, 0x22,
                             0x80, 0xA2, 0x07, ])  # change upper branch to hit our JSL, then JSL
    rom.write_bytes(0x14317, [0x22, 0x00, 0xA3, 0x07, ])
    rom.write_bytes(0x3A280, [0xE0, 0x00, 0x00,  # CPX #$0000
                              0xF0, 0x01,  # BEQ $07A286
                              0xE8,  # INX
                              0xEC, 0x1E, 0x65,  # CPX $651E
                              0x90, 0x66,  # BCC 07A2F1
                              0xE0, 0x00, 0x00,  # CPX #$0000
                              0xF0, 0x61,  # BEQ $07A2F1
                              0xAF, 0xD0, 0x36, 0x40,  # LDA $4036D0
                              0x29, 0xFF, 0x00,  # AND #$00FF
                              0xF0, 0x57,  # BEQ $07A2F0
                              0xAD, 0x00, 0x30,  # LDA $3000
                              0x29, 0x00, 0x02,  # AND #$0200
                              0xC9, 0x00, 0x00,  # CMP #$0000
                              0xD0, 0x4C,  # BNE $07A2F0
                              0x5A,  # PHY
                              0xAD, 0x00, 0x30,  # LDA $3000
                              0xA8,  # TAY
                              0x18,  # CLC
                              0x69, 0x20, 0x00,  # ADC #$0020
                              0x8D, 0x00, 0x30,  # STA $3000
                              0xAF, 0x70, 0x80, 0x40,  # LDA $408070
                              0xA2, 0x00, 0x00,  # LDX #$0000
                              0xC9, 0x0A, 0x00,  # CMP $000A
                              0x90, 0x07,  # BCC $07A2C3
                              0x38,  # SEC
                              0xE9, 0x0A, 0x00,  # SBC #$000A
                              0xE8,  # INX
                              0x80, 0xF4,  # BRA $07A2B7
                              0xDA,  # PHX
                              0xAA,  # TAX
                              0x68,  # PLA
                              0x09, 0x00, 0x25,  # ORA #$2500
                              0x48,  # PHA
                              0xA9, 0x70, 0x2C,  # LDA #$2C70
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0x68,  # PLA
                              0xC8,  # INY
                              0xC8,  # INY
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0x8A,  # TXA
                              0x09, 0x00, 0x25,  # ORA #$2500
                              0x48,  # PHA
                              0xA9, 0x78, 0x2C,  # LDA #$2C78
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0x68,  # PLA
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0x22, 0x80, 0xA3, 0x07,  # JSL $07A380 - we ran out of room
                              0x7A,  # PLY
                              0x38,  # SEC
                              0x6B,  # RTL
                              ])
    rom.write_bytes(0x3A300, [0x22, 0x9F, 0xD2, 0x00,  # JSL $00D29F - play sfx
                              0xDA,  # PHX
                              0x8B,  # PHB
                              0xA9, 0x00, 0x00,
                              0x48,  # PHA
                              0xAB,  # PLB
                              0xAB,  # PLB
                              0xA9, 0x00, 0x70,  # LDA #$7000
                              0x8D, 0x16, 0x21,  # STA $2116
                              0xA2, 0x00, 0x00,  # LDX #$0000
                              0xE0, 0x40, 0x01,  # CPX #$0140
                              0xF0, 0x0B,  # BEQ $07A325
                              0xBF, 0x50, 0x2F, 0xD9,  # LDA $D92F50, X
                              0x8D, 0x18, 0x21,  # STA $2118
                              0xE8,  # INX
                              0xE8,  # INX
                              0x80, 0xF0,  # BRA $07A315
                              0xA2, 0x00, 0x00,  # LDX #$0000
                              0xE0, 0x20, 0x00,  # CPX #$0020
                              0xF0, 0x0B,  # BEQ $07A338
                              0xBF, 0x10, 0x2E, 0xD9,  # LDA $D92E10, X
                              0x8D, 0x18, 0x21,  # STA $2118
                              0xE8,  # INX
                              0xE8,  # INX
                              0x80, 0xF0,  # BRA $07A328
                              0x5A,  # PHY
                              0xAF, 0x12, 0xD0, 0x07,  # LDA $07D012
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBF, 0x00, 0xE0, 0x07,  # LDA $07E000, X
                              0xAA,  # TAX
                              0xA0, 0x00, 0x00,  # LDY #$0000
                              0xC0, 0x20, 0x00,  # CPY #$0020
                              0xF0, 0x0D,  # BEQ $07A359
                              0xBF, 0x70, 0x31, 0xD9,  # LDA $D93170, X
                              0x8D, 0x18, 0x21,  # STA $2118
                              0xE8,  # INX
                              0xE8,  # INX
                              0xC8,  # INY
                              0xC8,  # INY
                              0x80, 0xEE,  # BRA $07A347
                              0xAF, 0x0C, 0xD0, 0x07,  # LDA $07D00C
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBF, 0x10, 0xE0, 0x07,  # LDA $07E010, X
                              0xAA,  # TAX
                              0xA0, 0x00, 0x00,  # LDY #$0000
                              0xC0, 0x20, 0x00,  # CPY #$0020
                              0xF0, 0x0D,  # BEQ $07A379
                              0xBF, 0x70, 0x31, 0xD9,  # LDA $D93170, X
                              0x8D, 0x18, 0x21,  # STA $2118
                              0xE8,  # INX
                              0xE8,  # INX
                              0xC8,  # INY
                              0xC8,  # INY
                              0x80, 0xEE,  # BRA $07A367
                              0x7A,  # PLY
                              0xAB,  # PLB
                              0xFA,  # PLX
                              0x6B,  # RTL
                              ])
    rom.write_bytes(0x3A380, [0xA9, 0x80, 0x2C,  # LDA #$2C80
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xA9, 0x0A, 0x25,  # LDA #$250A
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xAF, 0xCF, 0x53, 0x40,  # LDA $4053CF
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBF, 0x00, 0x90, 0x40,  # LDA $409000, X
                              0xC9, 0xFF, 0xFF,  # CMP #$FFFF
                              0xD0, 0x04,  # BNE $07A3A3
                              0xCA,  # DEX
                              0xCA,  # DEX
                              0x80, 0xF3,  # BRA $07A396
                              0xA2, 0x00, 0x00,  # LDX #$0000
                              0xC9, 0x0A, 0x00,  # CMP #$000A
                              0x90, 0x07,  # BCC $07A3A9
                              0x38,  # SEC
                              0xE9, 0x0A, 0x00,  # SBC #$000A
                              0xE8,  # INX
                              0x80, 0xF4,  # BRA $07A39D - return to loop head
                              0xDA,  # PHX
                              0xAA,  # TAX
                              0x68,  # PLA
                              0x09, 0x00, 0x25,  # ORA #$2500
                              0x48,  # PHA
                              0xA9, 0x88, 0x2C,  # LDA #$2C88
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0x68,  # PLA
                              0xC8,  # INY
                              0xC8,  # INY
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0x8A,  # TXA
                              0x09, 0x00, 0x25,  # ORA #$2500
                              0x48,  # PHA
                              0xA9, 0x90, 0x2C,  # LDA #$2C90
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0x68,  # PLA
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xA9, 0xD8, 0x14,  # LDA #$14D8
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xA9, 0x0B, 0x25,  # LDA #$250B
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xA9, 0xE0, 0x14,  # LDA #$14E0
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xA9, 0x0A, 0x25,  # LDA #$250A
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xA9, 0xE8, 0x14,  # LDA #$14E8
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xA9, 0x0C, 0x25,  # LDA #$250C
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0xAD, 0x00, 0x30,  # LDA $3000
                              0x38,  # SEC
                              0xE9, 0x40, 0x30,  # SBC #$3040
                              0x4A,  # LSR
                              0x4A,  # LSR
                              0xC9, 0x04, 0x00,  # CMP #$0004
                              0x90, 0x06,  # BCC $07A415
                              0x3A, 0x3A, 0x3A, 0x3A,  # DEC x4
                              0x80, 0xF5,  # BRA $07A40A - return to loop head
                              0x8D, 0x40, 0x32,  # STA $3240
                              0xA9, 0x04, 0x00,  # LDA #$0004
                              0x38,  # SEC
                              0xED, 0x40, 0x32,  # SBC $3240
                              0xAA,  # TAX
                              0xA9, 0xFF, 0x00,  # LDA #$00FF
                              0xE0, 0x00, 0x00,  # CPX #$0000
                              0xF0, 0x05,  # BEQ $07A42D
                              0x4A,  # LSR
                              0x4A,  # LSR
                              0xCA,  # DEX
                              0x80, 0xF6,  # BRA $07A423
                              0xAC, 0x02, 0x30,  # LDY $3002
                              0x39, 0x00, 0x00,  # AND $0000, Y
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xA9, 0x00, 0x00,  # LDA #$0000
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0xC8,  # INY
                              0xC8,  # INY
                              0x99, 0x00, 0x00,  # STA $0000, Y
                              0x6B,  # RTL
                              ])
    # Goal/Goal Speed letter offsets
    rom.write_bytes(0x3E000, [0x20, 0x03, 0x20, 0x00, 0x80, 0x01, 0x20, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                              0x00, 0xA0, 0x01, 0xA0, 0x00, ])

    # Heart Star Visual redirect
    rom.write_bytes(0x1427C, [0x22, 0x80, 0xA4, 0x07, 0xEA, 0xEA, ])
    rom.write_bytes(0x3A480, [0xDA,  # PHX
                              0x8A,  # TXA
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBD, 0x20, 0x90,  # LDA $9020, X
                              0x3A,  # DEC
                              0xAA,  # TAX
                              0xC9, 0x07, 0x00,  # CMP #$0007
                              0x30, 0x07,  # BMI $07A495
                              0xE8,  # INX
                              0x18,  # CLC
                              0xE9, 0x06, 0x00,  # SBC #$0006
                              0x80, 0xF4,  # BRA $07A489
                              0xBD, 0xA7, 0x53,  # LDA $53A7, X
                              0xFA,  # PLX
                              0x29, 0xFF, 0x00,  # AND #$00FF
                              0x6B,  # RTL
                              ])

    # Heart Star Cutscene redirect
    rom.write_bytes(0x49F35, [0x22, 0x00, 0xA5, 0x07, ])
    rom.write_bytes(0x3A500, [0xAA,  # TAX
                              0xAD, 0xD3, 0x53,  # LDA $53D3
                              0x3A,  # DEC
                              0x8D, 0xC3, 0x5A,  # STA $5AC3
                              0x6B,  # RTL
                              ])

    # display received items in pause menu
    rom.write_bytes(0x8406, [0x50, 0xA5, 0x07])
    rom.write_bytes(0x3A550, [0x22, 0x9F, 0xD2, 0x00,  # JSL $00D29F
                              0xDA,  # PHX
                              0x5A,  # PHY
                              0xA9, 0x00, 0x33,  # LDA #$3300
                              0x8F, 0x16, 0x21, 0x00,  # STA VMADDL
                              0xA9, 0x07, 0x00,  # LDA #$0007
                              0x8F, 0x04, 0x43, 0x00,  # STA A1B0
                              0xA9, 0x00, 0xF0,  # LDA #$F000
                              0x8F, 0x02, 0x43, 0x00,  # STA A1T0L
                              0xA9, 0xC0, 0x01,  # LDA #$01C0
                              0x8F, 0x05, 0x43, 0x00,  # STA DAS0L
                              0xE2, 0x20,  # SEP #$20
                              0xA9, 0x01,  # LDA #$01
                              0x8F, 0x00, 0x43, 0x00,  # STA DMAP0
                              0xA9, 0x18,  # LDA #$18
                              0x8F, 0x01, 0x43, 0x00,  # STA BBAD0
                              0xA9, 0x01,  # LDA #$01
                              0x8F, 0x0B, 0x42, 0x00,  # MDMAEN
                              0xC2, 0x20,  # REP #$20
                              0xA0, 0x00, 0x00,  # LDY #$0000
                              0xC8,  # INY - loop head
                              0xC0, 0x09, 0x00,  # CPY #$0009
                              0x10, 0x1B,  # BPL $07A5AC
                              0x98,  # TYA
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBD, 0x20, 0x80,  # LDA $8020, X
                              0xF0, 0xF2,  # BEQ $07A58B - return to loop head
                              0x98,  # TYA
                              0x18,  # CLC
                              0x69, 0xE2, 0x31,  # ADC #$31E2
                              0x8F, 0x16, 0x21, 0x00,  # STA VMADDL
                              0xBF, 0x20, 0xE0, 0x07,  # LDA $07E020, X
                              0x8F, 0x18, 0x21, 0x00,  # STA VMDATAL
                              0x80, 0xDF,  # BRA $07A58B - return to loop head
                              0xA0, 0xFF, 0xFF,  # LDY #$FFFF
                              0xC8,  # INY - loop head
                              0xC0, 0x07, 0x00,  # CPY #$0007
                              0x10, 0x1B,  # BPL $07A5D0
                              0x98,  # TYA
                              0x0A,  # ASL
                              0xAA,  # TAX
                              0xBD, 0x00, 0x80,  # LDA $8000, X
                              0xF0, 0xF2,  # BEQ $07A5AF - return to loop head
                              0x98,  # TYA
                              0x18,  # CLC
                              0x69, 0x03, 0x32,  # ADC #$3203
                              0x8F, 0x16, 0x21, 0x00,  # STA VMADDL
                              0xBF, 0x40, 0xE0, 0x07,  # LDA $07E040, X
                              0x8F, 0x18, 0x21, 0x00,  # STA VMDATAL
                              0x80, 0xDF,  # BRA $07A5AF - retun to loop head
                              0x7A,  # PLY
                              0xFA,  # PLX
                              0x6B,  # RTL
                              ])

    # data writing for prior
    rom.write_bytes(0x3E020,
                    [0x00, 0x0C, 0x30, 0x09, 0x31, 0x09, 0x32, 0x09, 0x33, 0x09, 0x34, 0x09, 0x35, 0x09, 0x36, 0x09,
                     0x37, 0x09,
                     ])
    rom.write_bytes(0x3E040, [0x38, 0x05, 0x39, 0x05, 0x3A, 0x01, 0x3B, 0x05, 0x3C, 0x05, 0x3D, 0x05, ])
    tiles = get_data(__name__, os.path.join("data", "APPauseIcons.dat"))
    rom.write_bytes(0x3F000, tiles)

    # base patch done, write relevant slot info

    # Write strict bosses patch
    if multiworld.strict_bosses[player]:
        rom.write_bytes(0x3A000, [0xDA,  # PHX
                                  0xAD, 0xCB, 0x53,  # LDA $53CB - unlocked level
                                  0xC9, 0x05, 0x00,  # CMP #$0005 - have we unlocked level 5?
                                  0xB0, 0x15,  # BCS $07A01E - we don't need to do anything if so
                                  0xEA, 0xEA, 0xEA, 0xEA, 0xEA,  # NOP x5, unsure when these got here
                                  0xAE, 0xCB, 0x53,  # LDX $53CB
                                  0xCA,  # DEX
                                  0x8A,  # TXA
                                  0x0A,  # ASL
                                  0xAA,  # TAX
                                  0xAD, 0x70, 0x80,  # LDA $8070 - current heart stars
                                  0xDF, 0x00, 0xD0, 0x07,  # CMP $07D000, X - do we have enough HS to purify?
                                  0xB0, 0x03,  # BCS $07A021 - branch if we do not
                                  0x38,  # SEC
                                  0x80, 0x01,  # BRA $07A022
                                  0x18,  # CLC
                                  0xFA,  # PLX
                                  0xAD, 0xCD, 0x53,  # LDA $53CD
                                  0x6B,  # RTL
                                  ])
        rom.write_bytes(0x143D9, [0x22, 0x00, 0xA0, 0x07, 0xEA, 0xEA, ])

    # Write open world patch
    if multiworld.open_world[player]:
        rom.write_bytes(0x14238, [0xA9, 0x06, 0x00,  # LDA #$0006
                                  0x22, 0x80, 0x9A, 0x07,  # JSL $079A80
                                  0xEA, 0xEA, 0xEA, 0xEA, 0xEA, ])  # set starting stages to 6
        rom.write_bytes(0x39A80, [0x8D, 0xC1, 0x5A,  # STA $5AC1 (cutscene)
                                  0x8D, 0xCD, 0x53,  # STA $53CD (unlocked stages)
                                  0x1A,  # INC
                                  0x8D, 0xB9, 0x5A,  # STA $5AB9 (currently selectable stages)
                                  0xA9, 0x01, 0x00,  # LDA #$0001
                                  0x8D, 0x9D, 0x5A,  # STA $5A9D
                                  0x8D, 0x9F, 0x5A,  # STA $5A9F
                                  0x8D, 0xA1, 0x5A,  # STA $5AA1
                                  0x8D, 0xA3, 0x5A,  # STA $5AA3
                                  0x8D, 0xA5, 0x5A,  # STA $5AA5
                                  0x6B,  # RTL
                                  ])
        rom.write_bytes(0x143C7, [0xAD, 0xC1, 0x5A, 0xCD, 0xC1, 0x5A, ])
        # changes the stage flag function to compare $5AC1 to $5AC1,
        # always running the "new stage" function
        # This has further checks present for bosses already, so we just
        # need to handle regular stages
        # write check for boss to be unlocked
        rom.write_bytes(0x3A100, [0xDA,  # PHX
                                  0x5A,  # PHY
                                  0xAD, 0xCD, 0x53,  # LDA $53CD
                                  0xC9, 0x06, 0x00,  # CMP #$0006
                                  0xD0, 0x50,  # BNE $07A15A - return if we aren't on stage 6
                                  0xAD, 0xCF, 0x53,  # LDA $53CF
                                  0x1A,  # INC
                                  0xCD, 0xCB, 0x53,  # CMP $53CB - are we on the most unlocked level?
                                  0xD0, 0x47,  # BNE $07A15A - return if we aren't
                                  0xA9, 0x00, 0x00,  # LDA #$0000
                                  0xAE, 0xCF, 0x53,  # LDX $53CF
                                  0xE0, 0x00, 0x00,  # CPX #$0000
                                  0xF0, 0x06,  # BEQ $07A124
                                  0x69, 0x06, 0x00,  # ADC #$0006
                                  0xCA,  # DEX
                                  0x80, 0xF5,  # BRA $07A119 - return to loop head
                                  0x0A,  # ASL
                                  0xAA,  # TAX
                                  0xA9, 0x00, 0x00,  # LDA #$0000
                                  0xA0, 0x06, 0x00,  # LDX #$0006
                                  0x5A,  # PHY
                                  0xDA,  # PHX
                                  0xFA,  # PLX
                                  0xBC, 0x20, 0x90,  # LDY $9020, X - get stage id
                                  0x88,  # DEY
                                  0xE8,  # INX
                                  0xE8,  # INX
                                  0x48,  # PHA
                                  0x98,  # TYA
                                  0x0A,  # ASL
                                  0xA8,  # TAY
                                  0x68,  # PLA
                                  0x79, 0x00, 0x82,  # ADC $8200, Y - add current stage value to total
                                  0x7A,  # PLY
                                  0x88,  # DEY
                                  0x5A,  # PHY
                                  0xDA,  # PHX
                                  0xC0, 0x00, 0x00,  # CPY #$0000
                                  0xD0, 0xE8,  # BNE $07A12E - return to loop head
                                  0xFA,  # PLX
                                  0x7A,  # PLY
                                  0x38,  # SEC
                                  0xED, 0x16, 0x90,  # SBC $9016
                                  0x90, 0x0C,  # BCC $07A12E
                                  0xAD, 0xCD, 0x53,  # LDA $53CD
                                  0x1A,  # INC
                                  0x8D, 0xCD, 0x53,  # STA $53CD
                                  0x8D, 0xC1, 0x5A,  # STA $5AC1
                                  0x80, 0x03,  # BRA 07A15D
                                  0x9C, 0xC1, 0x5A,  # STZ $5AC1
                                  0x7A,  # PLY
                                  0xFA,  # PLX
                                  0x6B,  # RTL
                                  ])
        # write hook to boss check
        rom.write_bytes(0x143F0, [0x22, 0x00, 0xA1, 0x07, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, ])

    # Write checks for consumable-sanity
    if multiworld.consumables[player]:
        # Redirect Consumable Effect and write index
        rom.write_bytes(0x3001E, [0x22, 0x80, 0x9E, 0x07, 0x4A, 0xC9, 0x05, 0x00, 0xB0, 0xFE, 0x0A, 0xAA, 0x7C, 0x2D,
                                  0x00, 0x37, 0x00, 0x37, 0x00, 0x7E, 0x00, 0x94, 0x00, 0x37, 0x00, 0xA9, 0x26, 0x00,
                                  0x22, 0x27, 0xD9, 0x00, 0xA4, 0xD2, 0x6B, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA,
                                  0xEA, 0xEA, 0xEA, ])
        # JSL first, then edit the following sections to point 1-ups and heart stars to the same function, function just
        # calls sound effect playing and prepares for the next function

        # Write Consumable Index to index array
        rom.write_bytes(0x39E80, [0x48,  # PHA
                                  0xDA,  # PHX
                                  0x5A,  # PHY
                                  0x29, 0xFF, 0x00,  # AND #$00FF
                                  0x48,  # PHA
                                  0xAE, 0xCF, 0x53,  # LDX $53CF
                                  0xAC, 0xD3, 0x53,  # LDY $53D3
                                  0xA9, 0x00, 0x00,  # LDA #$0000
                                  0x88,  # DEY
                                  0xE0, 0x00, 0x00,  # CPX #$0000
                                  0xF0, 0x07,  # BEQ $079E9D
                                  0x18,  # CLC
                                  0x69, 0x07, 0x00,  # ADC #$0007
                                  0xCA,  # DEX
                                  0x80, 0xF4,  # BRA $079E91 - return to loop head
                                  0xC0, 0x00, 0x00,  # CPY #$0000
                                  0xF0, 0x04,  # BEQ $079EA6
                                  0x1A,  # INC
                                  0x88,  # DEY
                                  0x80, 0xF7,  # BRA $079E9D - return to loop head
                                  0x0A,  # ASL
                                  0xAA,  # TAX
                                  0xBF, 0x20, 0xD0, 0x07,  # LDA $07D020, X - current stage
                                  0x3A,  # DEC
                                  0x0A, 0x0A, 0x0A, 0x0A, 0x0A, 0x0A,  # ASL x6
                                  0xAA,  # TAX
                                  0x68,  # PLA
                                  0xC9, 0x00, 0x00,  # CMP #$0000
                                  0xF0, 0x04,  # BEQ $079EBE
                                  0xE8,  # INX
                                  0x3A,  # DEC
                                  0x80, 0xF7,  # BRA $079EB5 - return to loop head
                                  0xBD, 0x00, 0xA0,  # LDA $A000, X - consumables index
                                  0x09, 0x01, 0x00,  # ORA #$0001
                                  0x9D, 0x00, 0xA0,  # STA $A000, X
                                  0x7A,  # PLY
                                  0xFA,  # PLX
                                  0x68,  # PLA
                                  0xEB,  # XBA
                                  0x29, 0xFF, 0x00,  # AND #$00FF
                                  0x6B,  # RTL
                                  ])

    rooms = [region for region in multiworld.regions if region.player == player and isinstance(region, Room)]
    if multiworld.music_shuffle[player] > 0:
        if multiworld.music_shuffle[player] == 1:
            shuffled_music = music_choices.copy()
            slot_random.shuffle(shuffled_music)
            music_map = dict(zip(music_choices, shuffled_music))
            # Avoid putting star twinkle in the pool
            music_map[5] = slot_random.choice(music_choices)
            # Heart Star music doesn't work on regular stages
            music_map[8] = slot_random.choice(music_choices)
            for room in rooms:
                room.music = music_map[room.music]
            for room in room_pointers:
                old_music = rom.read_byte(room + 2)
                rom.write_byte(room + 2, music_map[old_music])
            for i in range(5):
                # level themes
                old_music = rom.read_byte(0x133F2 + i)
                rom.write_byte(0x133F2 + i, music_map[old_music])
            # Zero
            rom.write_byte(0x9AE79, music_map[0x18])
            # Heart Star success and fail
            rom.write_byte(0x4A388, music_map[0x08])
            rom.write_byte(0x4A38D, music_map[0x1D])
        elif multiworld.music_shuffle[player] == 2:
            for room in rooms:
                room.music = slot_random.choice(music_choices)
            for room in room_pointers:
                rom.write_byte(room + 2, slot_random.choice(music_choices))
            for i in range(5):
                # level themes
                rom.write_byte(0x133F2 + i, slot_random.choice(music_choices))
            # Zero
            rom.write_byte(0x9AE79, slot_random.choice(music_choices))
            # Heart Star success and fail
            rom.write_byte(0x4A388, slot_random.choice(music_choices))
            rom.write_byte(0x4A38D, slot_random.choice(music_choices))

    for room in rooms:
        room.patch(rom)

    if multiworld.virtual_console[player] in [1, 3]:
        # Flash Reduction
        rom.write_byte(0x9AE68, 0x10)
        rom.write_bytes(0x9AE8E, [0x08, 0x00, 0x22, 0x5D, 0xF7, 0x00, 0xA2, 0x08, ])
        rom.write_byte(0x9AEA1, 0x08)
        rom.write_byte(0x9AEC9, 0x01)
        rom.write_bytes(0x9AED2, [0xA9, 0x1F])
        rom.write_byte(0x9AEE1, 0x08)

    if multiworld.virtual_console[player] in [2, 3]:
        # Hyper Zone BB colors
        rom.write_bytes(0x2C5E16, [0xEE, 0x1B, 0x18, 0x5B, 0xD3, 0x4A, 0xF4, 0x3B, ])
        rom.write_bytes(0x2C8217, [0xFF, 0x1E, ])

    # boss requirements
    rom.write_bytes(0x3D000, struct.pack("HHHHH", boss_requirements[0], boss_requirements[1], boss_requirements[2],
                                         boss_requirements[3], boss_requirements[4]))
    rom.write_bytes(0x3D00A, struct.pack("H", heart_stars_required if multiworld.goal_speed[player] == 1 else 0xFFFF))
    rom.write_byte(0x3D00C, multiworld.goal_speed[player])
    rom.write_byte(0x3D010, multiworld.death_link[player])
    rom.write_byte(0x3D012, multiworld.goal[player])
    rom.write_byte(0x3D014, multiworld.stage_shuffle[player])
    rom.write_byte(0x3D016, multiworld.ow_boss_requirement[player])
    rom.write_byte(0x3D018, multiworld.consumables[player])

    for level in shuffled_levels:
        for i in range(len(shuffled_levels[level])):
            rom.write_bytes(0x3F002E + ((level - 1) * 14) + (i * 2),
                            struct.pack("H", level_pointers[shuffled_levels[level][i]]))
            rom.write_bytes(0x3D020 + (level - 1) * 14 + (i * 2),
                            struct.pack("H", shuffled_levels[level][i] & 0x00FFFF))
            if (i == 0) or (i > 0 and i % 6 != 0):
                rom.write_bytes(0x3D080 + (level - 1) * 12 + (i * 2),
                                struct.pack("H", (shuffled_levels[level][i] & 0x00FFFF) % 6))

    for i in range(6):
        if bb_boss_enabled[i]:
            rom.write_bytes(0x3F0000 + (level_pointers[0x770200 + i]), struct.pack("I", bb_bosses[0x770200 + i]))

    # copy ability shuffle
    if multiworld.copy_ability_randomization[player] > 0:
        for enemy in copy_abilities:
            if enemy in miniboss_remap:
                rom.write_bytes(0xB417E + (miniboss_remap[enemy] << 1),
                                struct.pack("H", ability_remap[copy_abilities[enemy]]))
            else:
                rom.write_bytes(0xB3CAC + (enemy_remap[enemy] << 1),
                                struct.pack("H", ability_remap[copy_abilities[enemy]]))
        # following only needs done on non-door rando
        # incredibly lucky this follows the same order (including 5E == star block)
        rom.write_byte(0x2F77EA, 0x5E + (ability_remap[copy_abilities["Sparky"]] << 1))
        rom.write_byte(0x2F7811, 0x5E + (ability_remap[copy_abilities["Sparky"]] << 1))
        rom.write_byte(0x2F9BC4, 0x5E + (ability_remap[copy_abilities["Blocky"]] << 1))
        rom.write_byte(0x2F9BEB, 0x5E + (ability_remap[copy_abilities["Blocky"]] << 1))
        rom.write_byte(0x2FAC06, 0x5E + (ability_remap[copy_abilities["Jumper Shoot"]] << 1))
        rom.write_byte(0x2FAC2D, 0x5E + (ability_remap[copy_abilities["Jumper Shoot"]] << 1))
        rom.write_byte(0x2F9E7B, 0x5E + (ability_remap[copy_abilities["Yuki"]] << 1))
        rom.write_byte(0x2F9EA2, 0x5E + (ability_remap[copy_abilities["Yuki"]] << 1))
        rom.write_byte(0x2FA951, 0x5E + (ability_remap[copy_abilities["Sir Kibble"]] << 1))
        rom.write_byte(0x2FA978, 0x5E + (ability_remap[copy_abilities["Sir Kibble"]] << 1))
        rom.write_byte(0x2FA132, 0x5E + (ability_remap[copy_abilities["Haboki"]] << 1))
        rom.write_byte(0x2FA159, 0x5E + (ability_remap[copy_abilities["Haboki"]] << 1))
        rom.write_byte(0x2FA3E8, 0x5E + (ability_remap[copy_abilities["Boboo"]] << 1))
        rom.write_byte(0x2FA40F, 0x5E + (ability_remap[copy_abilities["Boboo"]] << 1))
        rom.write_byte(0x2F90E2, 0x5E + (ability_remap[copy_abilities["Captain Stitch"]] << 1))
        rom.write_byte(0x2F9109, 0x5E + (ability_remap[copy_abilities["Captain Stitch"]] << 1))

        if multiworld.copy_ability_randomization[player] == 2:
            for enemy in enemy_remap:
                # we just won't include it for minibosses
                rom.write_bytes(0xB3E40 + (enemy_remap[enemy] << 1), struct.pack("h", slot_random.randint(-1, 2)))

    # write jumping goal
    rom.write_bytes(0x94F8, struct.pack("H", multiworld.jumping_target[player]))
    rom.write_bytes(0x944E, struct.pack("H", multiworld.jumping_target[player]))

    from Utils import __version__
    rom.name = bytearray(f'KDL3{__version__.replace(".", "")[0:3]}_{player}_{multiworld.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x3C000, rom.name)
    rom.write_byte(0x3C020, multiworld.game_language[player].value)

    # handle palette
    if multiworld.kirby_flavor_preset[player] != 0:
        for addr in kirby_target_palettes:
            target = kirby_target_palettes[addr]
            palette = get_kirby_palette(multiworld, player)
            rom.write_bytes(addr, get_palette_bytes(palette, target[0], target[1], target[2]))

    if multiworld.gooey_flavor_preset[player] != 0:
        for addr in gooey_target_palettes:
            target = gooey_target_palettes[addr]
            palette = get_gooey_palette(multiworld, player)
            rom.write_bytes(addr, get_palette_bytes(palette, target[0], target[1], target[2]))


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
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["kdl3_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
