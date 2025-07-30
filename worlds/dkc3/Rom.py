import Utils
from Utils import read_snes_rom
from worlds.AutoWorld import World
from worlds.Files import APDeltaPatch
from .Levels import level_list, level_dict

USHASH = '120abf304f0c40fe059f6a192ed4f947'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
import math


level_unlock_map = {
    0x657: [0x65A],
    0x65A: [0x680, 0x639, 0x659],
    0x659: [0x65D],
    0x65D: [0x65C],
    0x65C: [0x688, 0x64F],

    0x662: [0x681, 0x664],
    0x664: [0x65B],
    0x65B: [0x689, 0x661],
    0x661: [0x63A, 0x666],
    0x666: [0x650, 0x649],

    0x667: [0x66A],
    0x66A: [0x682, 0x658],
    0x658: [0x68A, 0x66B],
    0x66B: [0x668],
    0x668: [0x651],

    0x66D: [0x63C, 0x672],
    0x672: [0x68B, 0x660],
    0x660: [0x683, 0x66E],
    0x66E: [0x670],
    0x670: [0x652],

    0x673: [0x684, 0x65F],
    0x65F: [0x66C],
    0x66C: [0x66F],
    0x66F: [0x65E],
    0x65E: [0x63D, 0x653, 0x68C, 0x64C],

    0x676: [0x63E, 0x674, 0x685],
    0x674: [0x63F, 0x669],
    0x669: [0x677],
    0x677: [0x68D, 0x675],
    0x675: [0x654],

    0x67A: [0x640, 0x678],
    0x678: [0x665],
    0x665: [0x686, 0x679],
    0x679: [0x68E, 0x671],

    0x67B: [0x67C],
    0x67C: [0x67D],
    0x67D: [0x663],
    0x663: [0x67E],
}

location_rom_data = {
    0xDC3000: [0x657, 1], # Lakeside Limbo
    0xDC3001: [0x657, 2],
    0xDC3002: [0x657, 3],
    0xDC3003: [0x657, 5],
    0xDC3100: [0x657, 7],

    0xDC3004: [0x65A, 1], # Doorstop Dash
    0xDC3005: [0x65A, 2],
    0xDC3006: [0x65A, 3],
    0xDC3007: [0x65A, 5],
    0xDC3104: [0x65A, 7],

    0xDC3008: [0x659, 1], # Tidal Trouble
    0xDC3009: [0x659, 2],
    0xDC300A: [0x659, 3],
    0xDC300B: [0x659, 5],
    0xDC3108: [0x659, 7],

    0xDC300C: [0x65D, 1], # Skidda's Row
    0xDC300D: [0x65D, 2],
    0xDC300E: [0x65D, 3],
    0xDC300F: [0x65D, 5],
    0xDC310C: [0x65D, 7],

    0xDC3010: [0x65C, 1], # Murky Mill
    0xDC3011: [0x65C, 2],
    0xDC3012: [0x65C, 3],
    0xDC3013: [0x65C, 5],
    0xDC3110: [0x65C, 7],


    0xDC3014: [0x662, 1], # Barrel Shield Bust-Up
    0xDC3015: [0x662, 2],
    0xDC3016: [0x662, 3],
    0xDC3017: [0x662, 5],
    0xDC3114: [0x662, 7],

    0xDC3018: [0x664, 1], # Riverside Race
    0xDC3019: [0x664, 2],
    0xDC301A: [0x664, 3],
    0xDC301B: [0x664, 5],
    0xDC3118: [0x664, 7],

    0xDC301C: [0x65B, 1], # Squeals on Wheels
    0xDC301D: [0x65B, 2],
    0xDC301E: [0x65B, 3],
    0xDC301F: [0x65B, 5],
    0xDC311C: [0x65B, 7],

    0xDC3020: [0x661, 1], # Springin' Spiders
    0xDC3021: [0x661, 2],
    0xDC3022: [0x661, 3],
    0xDC3023: [0x661, 5],
    0xDC3120: [0x661, 7],

    0xDC3024: [0x666, 1], # Bobbing Barrel Brawl
    0xDC3025: [0x666, 2],
    0xDC3026: [0x666, 3],
    0xDC3027: [0x666, 5],
    0xDC3124: [0x666, 7],


    0xDC3028: [0x667, 1], # Bazza's Blockade
    0xDC3029: [0x667, 2],
    0xDC302A: [0x667, 3],
    0xDC302B: [0x667, 5],
    0xDC3128: [0x667, 7],

    0xDC302C: [0x66A, 1], # Rocket Barrel Ride
    0xDC302D: [0x66A, 2],
    0xDC302E: [0x66A, 3],
    0xDC302F: [0x66A, 5],
    0xDC312C: [0x66A, 7],

    0xDC3030: [0x658, 1], # Kreeping Klasps
    0xDC3031: [0x658, 2],
    0xDC3032: [0x658, 3],
    0xDC3033: [0x658, 5],
    0xDC3130: [0x658, 7],

    0xDC3034: [0x66B, 1], # Tracker Barrel Trek
    0xDC3035: [0x66B, 2],
    0xDC3036: [0x66B, 3],
    0xDC3037: [0x66B, 5],
    0xDC3134: [0x66B, 7],

    0xDC3038: [0x668, 1], # Fish Food Frenzy
    0xDC3039: [0x668, 2],
    0xDC303A: [0x668, 3],
    0xDC303B: [0x668, 5],
    0xDC3138: [0x668, 7],


    0xDC303C: [0x66D, 1], # Fire-ball Frenzy
    0xDC303D: [0x66D, 2],
    0xDC303E: [0x66D, 3],
    0xDC303F: [0x66D, 5],
    0xDC313C: [0x66D, 7],

    0xDC3040: [0x672, 1], # Demolition Drainpipe
    0xDC3041: [0x672, 2],
    0xDC3042: [0x672, 3],
    0xDC3043: [0x672, 5],
    0xDC3140: [0x672, 7],

    0xDC3044: [0x660, 1], # Ripsaw Rage
    0xDC3045: [0x660, 2],
    0xDC3046: [0x660, 3],
    0xDC3047: [0x660, 5],
    0xDC3144: [0x660, 7],

    0xDC3048: [0x66E, 1], # Blazing Bazukas
    0xDC3049: [0x66E, 2],
    0xDC304A: [0x66E, 3],
    0xDC304B: [0x66E, 5],
    0xDC3148: [0x66E, 7],

    0xDC304C: [0x670, 1], # Low-G Labyrinth
    0xDC304D: [0x670, 2],
    0xDC304E: [0x670, 3],
    0xDC304F: [0x670, 5],
    0xDC314C: [0x670, 7],


    0xDC3050: [0x673, 1], # Krevice Kreepers
    0xDC3051: [0x673, 2],
    0xDC3052: [0x673, 3],
    0xDC3053: [0x673, 5],
    0xDC3150: [0x673, 7],

    0xDC3054: [0x65F, 1], # Tearaway Toboggan
    0xDC3055: [0x65F, 2],
    0xDC3056: [0x65F, 3],
    0xDC3057: [0x65F, 5],
    0xDC3154: [0x65F, 7],

    0xDC3058: [0x66C, 1], # Barrel Drop Bounce
    0xDC3059: [0x66C, 2],
    0xDC305A: [0x66C, 3],
    0xDC305B: [0x66C, 5],
    0xDC3158: [0x66C, 7],

    0xDC305C: [0x66F, 1], # Krack-Shot Kroc
    0xDC305D: [0x66F, 2],
    0xDC305E: [0x66F, 3],
    0xDC305F: [0x66F, 5],
    0xDC315C: [0x66F, 7],

    0xDC3060: [0x65E, 1], # Lemguin Lunge
    0xDC3061: [0x65E, 2],
    0xDC3062: [0x65E, 3],
    0xDC3063: [0x65E, 5],
    0xDC3160: [0x65E, 7],


    0xDC3064: [0x676, 1], # Buzzer Barrage
    0xDC3065: [0x676, 2],
    0xDC3066: [0x676, 3],
    0xDC3067: [0x676, 5],
    0xDC3164: [0x676, 7],

    0xDC3068: [0x674, 1], # Kong-Fused Cliffs
    0xDC3069: [0x674, 2],
    0xDC306A: [0x674, 3],
    0xDC306B: [0x674, 5],
    0xDC3168: [0x674, 7],

    0xDC306C: [0x669, 1], # Floodlit Fish
    0xDC306D: [0x669, 2],
    0xDC306E: [0x669, 3],
    0xDC306F: [0x669, 5],
    0xDC316C: [0x669, 7],

    0xDC3070: [0x677, 1], # Pothole Panic
    0xDC3071: [0x677, 2],
    0xDC3072: [0x677, 3],
    0xDC3073: [0x677, 5],
    0xDC3170: [0x677, 7],

    0xDC3074: [0x675, 1], # Ropey Rumpus
    0xDC3075: [0x675, 2],
    0xDC3076: [0x675, 3],
    0xDC3077: [0x675, 5],
    0xDC3174: [0x675, 7],


    0xDC3078: [0x67A, 1], # Konveyor Rope Klash
    0xDC3079: [0x67A, 2],
    0xDC307A: [0x67A, 3],
    0xDC307B: [0x67A, 5],
    0xDC3178: [0x67A, 7],

    0xDC307C: [0x678, 1], # Creepy Caverns
    0xDC307D: [0x678, 2],
    0xDC307E: [0x678, 3],
    0xDC307F: [0x678, 5],
    0xDC317C: [0x678, 7],

    0xDC3080: [0x665, 1], # Lightning Lookout
    0xDC3081: [0x665, 2],
    0xDC3082: [0x665, 3],
    0xDC3083: [0x665, 5],
    0xDC3180: [0x665, 7],

    0xDC3084: [0x679, 1], # Koindozer Klamber
    0xDC3085: [0x679, 2],
    0xDC3086: [0x679, 3],
    0xDC3087: [0x679, 5],
    0xDC3184: [0x679, 7],

    0xDC3088: [0x671, 1], # Poisonous Pipeline
    0xDC3089: [0x671, 2],
    0xDC308A: [0x671, 3],
    0xDC308B: [0x671, 5],
    0xDC3188: [0x671, 7],


    0xDC308C: [0x67B, 1], # Stampede Sprint
    0xDC308D: [0x67B, 2],
    0xDC308E: [0x67B, 3],
    0xDC308F: [0x67B, 4],
    0xDC3090: [0x67B, 5],
    0xDC318C: [0x67B, 7],

    0xDC3091: [0x67C, 1], # Criss Kross Cliffs
    0xDC3092: [0x67C, 2],
    0xDC3093: [0x67C, 3],
    0xDC3094: [0x67C, 5],
    0xDC3191: [0x67C, 7],

    0xDC3095: [0x67D, 1], # Tyrant Twin Tussle
    0xDC3096: [0x67D, 2],
    0xDC3097: [0x67D, 3],
    0xDC3098: [0x67D, 4],
    0xDC3099: [0x67D, 5],
    0xDC3195: [0x67D, 7],

    0xDC309A: [0x663, 1], # Swoopy Salvo
    0xDC309B: [0x663, 2],
    0xDC309C: [0x663, 3],
    0xDC309D: [0x663, 4],
    0xDC309E: [0x663, 5],
    0xDC319A: [0x663, 7],

    0xDC309F: [0x67E, 1], # Rocket Rush
    0xDC30A0: [0x67E, 5],

    0xDC30A1: [0x64F, 1], # Bosses
    0xDC30A2: [0x650, 1],
    0xDC30A3: [0x651, 1],
    0xDC30A4: [0x652, 1],
    0xDC30A5: [0x653, 1],
    0xDC30A6: [0x654, 1],
    0xDC30A7: [0x655, 1],
    0xDC30A8: [0x656, 1],

    0xDC30A9: [0x647, 1], # Banana Bird Caves
    0xDC30AA: [0x645, 1],
    0xDC30AB: [0x644, 1],
    0xDC30AC: [0x642, 1],
    0xDC30AD: [0x643, 1],
    0xDC30AE: [0x646, 1],
    0xDC30AF: [0x648, 1],
    0xDC30B0: [0x649, 1],
    0xDC30B1: [0x64A, 1],
    #0xDC30B2: [0x64B, 1], # Disabled until Trade Sequence
    0xDC30B3: [0x64C, 1],
    #0xDC30B4: [0x64D, 1], # Disabled until Trade Sequence
    0xDC30B5: [0x64E, 1],

    0xDC30B6: [0x5FE, 4], # Banana Bird Mother

    # DKC3_TODO: Disabled until Trade Sequence
    #0xDC30B7: [0x615, 2, True],
    #0xDC30B8: [0x615, 3, True],
    #0xDC30B9: [0x619, 2],
    ##0xDC30BA:
    #0xDC30BB: [0x61B, 3],
    #0xDC30BC: [0x61D, 2],
    #0xDC30BD: [0x621, 4],
    #0xDC30BE: [0x625, 4, True],
}

boss_location_ids = [
    0xDC30A1,
    0xDC30A2,
    0xDC30A3,
    0xDC30A4,
    0xDC30A5,
    0xDC30A6,
    0xDC30A7,
    0xDC30A8,
    0xDC30B6,
]


item_rom_data = {
    0xDC3001: [0x5D5], # 1-Up Balloon
    0xDC3002: [0x5C9], # Bear Coin
    0xDC3003: [0x5CB], # Bonus Coin
    0xDC3004: [0x5CF], # DK Coin
    0xDC3005: [0x5CD], # Banana Bird
    0xDC3006: [0x5D1, 0x603], # Cog
}

music_rom_data = [
    0x3D06B1,
    0x3D0753,
    0x3D071D,
    0x3D07FA,
    0x3D07C4,

    0x3D08FE,
    0x3D096C,
    0x3D078E,
    0x3D08CD,
    0x3D09DD,

    0x3D0A0E,
    0x3D0AB3,
    0x3D06E7,
    0x3D0AE4,
    0x3D0A45,

    0x3D0B46,
    0x3D0C40,
    0x3D0897,
    0x3D0B77,
    0x3D0BD9,

    0x3D0C71,
    0x3D0866,
    0x3D0B15,
    0x3D0BA8,
    0x3D0830,

    0x3D0D04,
    0x3D0CA2,
    0x3D0A7C,
    0x3D0D35,
    0x3D0CD3,

    0x3D0DC8,
    0x3D0D66,
    0x3D09AC,
    0x3D0D97,
    0x3D0C0F,

    0x3D0DF9,
    0x3D0E31,
    0x3D0E62,
    0x3D0934,
    0x3D0E9A,
]

level_music_ids = [
    0x06,
    0x07,
    0x08,
    0x0A,
    0x0B,
    0x0E,
    0x0F,
    0x10,
    0x17,
    0x19,
    0x1C,
    0x1D,
    0x1E,
    0x21,
]

class LocalRom:

    def __init__(self, file, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_snes_rom(stream)
        #if patch:
        #    self.patch_rom()
        #    self.orig_buffer = self.buffer.copy()
        #if vanillaRom:
        #    with open(vanillaRom, 'rb') as vanillaStream:
        #        self.orig_buffer = read_snes_rom(vanillaStream)
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytearray:
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



def patch_rom(world: World, rom: LocalRom, active_level_list):

    # Boomer Costs
    bonus_coin_cost = world.options.krematoa_bonus_coin_cost
    inverted_bonus_coin_cost = 0x100 - bonus_coin_cost
    rom.write_byte(0x3498B9, inverted_bonus_coin_cost)
    rom.write_byte(0x3498BA, inverted_bonus_coin_cost)
    rom.write_byte(0x3498BB, inverted_bonus_coin_cost)
    rom.write_byte(0x3498BC, inverted_bonus_coin_cost)
    rom.write_byte(0x3498BD, inverted_bonus_coin_cost)

    rom.write_byte(0x349857, bonus_coin_cost)
    rom.write_byte(0x349862, bonus_coin_cost)

    # Gyrocopter Costs
    dk_coin_cost = world.options.dk_coins_for_gyrocopter
    rom.write_byte(0x3484A6, dk_coin_cost)
    rom.write_byte(0x3484D5, dk_coin_cost)
    rom.write_byte(0x3484D7, 0x90)
    rom.write_byte(0x3484DC, 0xEA)
    rom.write_byte(0x3484DD, 0xEA)
    rom.write_byte(0x3484DE, 0xEA)
    rom.write_byte(0x348528, 0x80) # Prevent Single-Ski Lock

    # Make Swanky free
    rom.write_byte(0x348C48, 0x00)

    rom.write_bytes(0x34AB70, bytearray([0xEA, 0xEA]))
    rom.write_bytes(0x34ABF7, bytearray([0xEA, 0xEA]))
    rom.write_bytes(0x34ACD0, bytearray([0xEA, 0xEA]))

    # Banana Bird Costs
    if world.options.goal == "banana_bird_hunt":
        banana_bird_cost = math.floor(world.options.number_of_banana_birds * world.options.percentage_of_banana_birds / 100.0)
        rom.write_byte(0x34AB85, banana_bird_cost)
        rom.write_byte(0x329FD8, banana_bird_cost)
        rom.write_byte(0x32A025, banana_bird_cost)
        rom.write_byte(0x329FDA, 0xB0)
    else:
    #    rom.write_byte(0x34AB84, 0x20)  # These cause hangs at Wrinkly's
    #    rom.write_byte(0x329FD8, 0x20)
    #    rom.write_byte(0x32A025, 0x20)
        rom.write_byte(0x329FDA, 0xB0)

    # Baffle Mirror Fix
    rom.write_byte(0x9133, 0x08)
    rom.write_byte(0x9135, 0x0C)
    rom.write_byte(0x9136, 0x2B)
    rom.write_byte(0x9137, 0x06)

    # Palette Swap
    rom.write_byte(0x3B96A5, 0xD0)
    if world.options.kong_palette_swap == "default":
        rom.write_byte(0x3B96A9, 0x00)
        rom.write_byte(0x3B96A8, 0x00)
    elif world.options.kong_palette_swap == "purple":
        rom.write_byte(0x3B96A9, 0x00)
        rom.write_byte(0x3B96A8, 0x3C)
    elif world.options.kong_palette_swap == "spooky":
        rom.write_byte(0x3B96A9, 0x00)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.options.kong_palette_swap == "dark":
        rom.write_byte(0x3B96A9, 0x05)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.options.kong_palette_swap == "chocolate":
        rom.write_byte(0x3B96A9, 0x1D)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.options.kong_palette_swap == "shadow":
        rom.write_byte(0x3B96A9, 0x45)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.options.kong_palette_swap == "red_gold":
        rom.write_byte(0x3B96A9, 0x5D)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.options.kong_palette_swap == "gbc":
        rom.write_byte(0x3B96A9, 0x20)
        rom.write_byte(0x3B96A8, 0x3C)
    elif world.options.kong_palette_swap == "halloween":
        rom.write_byte(0x3B96A9, 0x70)
        rom.write_byte(0x3B96A8, 0x3C)

    if world.options.music_shuffle:
        for address in music_rom_data:
            rand_song = world.random.choice(level_music_ids)
            rom.write_byte(address, rand_song)

    # Starting Lives
    rom.write_byte(0x9130, world.options.starting_life_count.value)
    rom.write_byte(0x913B, world.options.starting_life_count.value)

    # Cheat options
    cheat_bytes = [0x00, 0x00]

    if world.options.merry:
        cheat_bytes[0] |= 0x01

    if world.options.autosave:
        cheat_bytes[0] |= 0x02

    if world.options.difficulty == "tufst":
        cheat_bytes[0] |= 0x80
        cheat_bytes[1] |= 0x80
    elif world.options.difficulty == "hardr":
        cheat_bytes[0] |= 0x00
        cheat_bytes[1] |= 0x00
    elif world.options.difficulty == "norml":
        cheat_bytes[1] |= 0x40

    rom.write_bytes(0x8303, bytearray(cheat_bytes))

    # Handle Level Shuffle Here
    if world.options.level_shuffle:
        for i in range(len(active_level_list)):
            rom.write_byte(level_dict[level_list[i]].nameIDAddress, level_dict[active_level_list[i]].nameID)
            rom.write_byte(level_dict[level_list[i]].levelIDAddress, level_dict[active_level_list[i]].levelID)

            rom.write_byte(0x3FF800 + level_dict[active_level_list[i]].levelID, level_dict[level_list[i]].levelID)
            rom.write_byte(0x3FF860 + level_dict[level_list[i]].levelID, level_dict[active_level_list[i]].levelID)

        # First levels of each world
        rom.write_byte(0x34BC3E, (0x32 + level_dict[active_level_list[0]].levelID))
        rom.write_byte(0x34BC47, (0x32 + level_dict[active_level_list[5]].levelID))
        rom.write_byte(0x34BC4A, (0x32 + level_dict[active_level_list[10]].levelID))
        rom.write_byte(0x34BC53, (0x32 + level_dict[active_level_list[15]].levelID))
        rom.write_byte(0x34BC59, (0x32 + level_dict[active_level_list[20]].levelID))
        rom.write_byte(0x34BC5C, (0x32 + level_dict[active_level_list[25]].levelID))
        rom.write_byte(0x34BC65, (0x32 + level_dict[active_level_list[30]].levelID))
        rom.write_byte(0x34BC6E, (0x32 + level_dict[active_level_list[35]].levelID))

        # Cotton-Top Cove Boss Unlock
        rom.write_byte(0x34C02A, (0x32 + level_dict[active_level_list[14]].levelID))

        # Kong-Fused Cliffs Unlock
        rom.write_byte(0x34C213, (0x32 + level_dict[active_level_list[25]].levelID))
        rom.write_byte(0x34C21B, (0x32 + level_dict[active_level_list[26]].levelID))

    if world.options.goal == "knautilus":
        # Swap Kastle KAOS and Knautilus
        rom.write_byte(0x34D4E1, 0xC2)
        rom.write_byte(0x34D4E2, 0x24)
        rom.write_byte(0x34D551, 0xBA)
        rom.write_byte(0x34D552, 0x23)

        rom.write_byte(0x32F339, 0x55)

    # Handle KONGsanity Here
    if world.options.kongsanity:
        # Arich's Hoard KONGsanity fix
        rom.write_bytes(0x34BA8C, bytearray([0xEA, 0xEA]))

        # Don't hide the level flag if the 0x80 bit is set
        rom.write_bytes(0x34CE92, bytearray([0x80]))

        # Use the `!` next to level name for indicating KONG letters
        rom.write_bytes(0x34B8F0, bytearray([0x80]))
        rom.write_bytes(0x34B8F3, bytearray([0x80]))

        # Hijack to code to set the 0x80 flag for the level when you complete KONG
        rom.write_bytes(0x3BCD4B, bytearray([0x22, 0x80, 0xFA, 0XB8])) # JSL $B8FA80

        rom.write_bytes(0x38FA80, bytearray([0xDA]))             # PHX
        rom.write_bytes(0x38FA81, bytearray([0x48]))             # PHA
        rom.write_bytes(0x38FA82, bytearray([0x08]))             # PHP
        rom.write_bytes(0x38FA83, bytearray([0xE2, 0x20]))       # SEP #20
        rom.write_bytes(0x38FA85, bytearray([0x48]))             # PHA
        rom.write_bytes(0x38FA86, bytearray([0x18]))             # CLC
        rom.write_bytes(0x38FA87, bytearray([0x6D, 0xD3, 0x18])) # ADC $18D3
        rom.write_bytes(0x38FA8A, bytearray([0x8D, 0xD3, 0x18])) # STA $18D3
        rom.write_bytes(0x38FA8D, bytearray([0x68]))             # PLA
        rom.write_bytes(0x38FA8E, bytearray([0xC2, 0x20]))       # REP 20
        rom.write_bytes(0x38FA90, bytearray([0X18]))             # CLC
        rom.write_bytes(0x38FA91, bytearray([0x6D, 0xD5, 0x05])) # ADC $05D5
        rom.write_bytes(0x38FA94, bytearray([0x8D, 0xD5, 0x05])) # STA $05D5
        rom.write_bytes(0x38FA97, bytearray([0xAE, 0xB9, 0x05])) # LDX $05B9
        rom.write_bytes(0x38FA9A, bytearray([0xBD, 0x32, 0x06])) # LDA $0632, X
        rom.write_bytes(0x38FA9D, bytearray([0x09, 0x80, 0x00])) # ORA #8000
        rom.write_bytes(0x38FAA0, bytearray([0x9D, 0x32, 0x06])) # STA $0632, X
        rom.write_bytes(0x38FAA3, bytearray([0xAD, 0xD5, 0x18])) # LDA $18D5
        rom.write_bytes(0x38FAA6, bytearray([0xD0, 0x03]))       # BNE $80EA
        rom.write_bytes(0x38FAA8, bytearray([0x9C, 0xD9, 0x18])) # STZ $18D9
        rom.write_bytes(0x38FAAB, bytearray([0xA9, 0x78, 0x00])) # LDA #0078
        rom.write_bytes(0x38FAAE, bytearray([0x8D, 0xD5, 0x18])) # STA $18D5
        rom.write_bytes(0x38FAB1, bytearray([0x28]))             # PLP
        rom.write_bytes(0x38FAB2, bytearray([0x68]))             # PLA
        rom.write_bytes(0x38FAB3, bytearray([0xFA]))             # PLX
        rom.write_bytes(0x38FAB4, bytearray([0x6B]))             # RTL
    # End Handle KONGsanity

    # Handle Credits
    rom.write_bytes(0x32A5DF, bytearray([0x41, 0x52, 0x43, 0x48, 0x49, 0x50, 0x45, 0x4C, 0x41, 0x47, 0x4F, 0x20, 0x4D, 0x4F, 0xC4])) # "ARCHIPELAGO MOD"
    rom.write_bytes(0x32A5EE, bytearray([0x00, 0x03, 0x50, 0x4F, 0x52, 0x59, 0x47, 0x4F, 0x4E, 0xC5])) # "PORYGONE"

    from Utils import __version__
    rom.name = bytearray(f'D3{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)

    # DKC3_TODO: This is a hack, reconsider
    # Don't grant (DK, Bonus, Bear) Coins
    rom.write_byte(0x3BD454, 0xEA)
    rom.write_byte(0x3BD455, 0xEA)

    # Don't grant Cogs
    rom.write_byte(0x3BD574, 0xEA)
    rom.write_byte(0x3BD575, 0xEA)
    rom.write_byte(0x3BD576, 0xEA)

    # Don't grant Banana Birds at their caves
    rom.write_byte(0x32DD62, 0xEA)
    rom.write_byte(0x32DD63, 0xEA)
    rom.write_byte(0x32DD64, 0xEA)

    # Don't grant Banana Birds at Bears
    rom.write_byte(0x3492DB, 0xEA)
    rom.write_byte(0x3492DC, 0xEA)
    rom.write_byte(0x3492DD, 0xEA)
    rom.write_byte(0x3493F4, 0xEA)
    rom.write_byte(0x3493F5, 0xEA)
    rom.write_byte(0x3493F6, 0xEA)

    # Don't grant present at Blizzard
    rom.write_byte(0x8454, 0x00)

    # Don't grant Patch and Skis from their bosses
    rom.write_byte(0x3F3762, 0x00)
    rom.write_byte(0x3F377B, 0x00)
    rom.write_byte(0x3F3797, 0x00)

    # Always allow Start+Select
    rom.write_byte(0x8BAB, 0x01)

    # Handle Alt Palettes in Krematoa
    rom.write_byte(0x3B97E9, 0x80)
    rom.write_byte(0x3B97EA, 0xEA)


class DKC3DeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Donkey Kong Country 3"
    patch_file_ending = ".apdkc3"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["dkc3_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
