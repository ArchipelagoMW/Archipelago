import Utils
from Patch import read_rom, APDeltaPatch
from .Locations import lookup_id_to_name, all_locations
from .Levels import level_list, level_dict

USHASH = '120abf304f0c40fe059f6a192ed4f947'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
import math


location_rom_data = {
    0xDC3000: [0x657, 1], # Lakeside Limbo
    0xDC3001: [0x657, 2],
    0xDC3002: [0x657, 3],
    0xDC3003: [0x657, 5],

    0xDC3004: [0x65A, 1], # Doorstop Dash
    0xDC3005: [0x65A, 2],
    0xDC3006: [0x65A, 3],
    0xDC3007: [0x65A, 5],

    0xDC3008: [0x659, 1], # Tidal Trouble
    0xDC3009: [0x659, 2],
    0xDC300A: [0x659, 3],
    0xDC300B: [0x659, 5],

    0xDC300C: [0x65D, 1], # Skidda's Row
    0xDC300D: [0x65D, 2],
    0xDC300E: [0x65D, 3],
    0xDC300F: [0x65D, 5],

    0xDC3010: [0x65C, 1], # Murky Mill
    0xDC3011: [0x65C, 2],
    0xDC3012: [0x65C, 3],
    0xDC3013: [0x65C, 5],


    0xDC3014: [0x662, 1], # Barrel Shield Bust-Up
    0xDC3015: [0x662, 2],
    0xDC3016: [0x662, 3],
    0xDC3017: [0x662, 5],

    0xDC3018: [0x664, 1], # Riverside Race
    0xDC3019: [0x664, 2],
    0xDC301A: [0x664, 3],
    0xDC301B: [0x664, 5],

    0xDC301C: [0x65B, 1], # Squeals on Wheels
    0xDC301D: [0x65B, 2],
    0xDC301E: [0x65B, 3],
    0xDC301F: [0x65B, 5],

    0xDC3020: [0x661, 1], # Springin' Spiders
    0xDC3021: [0x661, 2],
    0xDC3022: [0x661, 3],
    0xDC3023: [0x661, 5],

    0xDC3024: [0x666, 1], # Bobbing Barrel Brawl
    0xDC3025: [0x666, 2],
    0xDC3026: [0x666, 3],
    0xDC3027: [0x666, 5],


    0xDC3028: [0x667, 1], # Bazza's Blockade
    0xDC3029: [0x667, 2],
    0xDC302A: [0x667, 3],
    0xDC302B: [0x667, 5],

    0xDC302C: [0x66A, 1], # Rocket Barrel Ride
    0xDC302D: [0x66A, 2],
    0xDC302E: [0x66A, 3],
    0xDC302F: [0x66A, 5],

    0xDC3030: [0x658, 1], # Kreeping Klasps
    0xDC3031: [0x658, 2],
    0xDC3032: [0x658, 3],
    0xDC3033: [0x658, 5],

    0xDC3034: [0x66B, 1], # Tracker Barrel Trek
    0xDC3035: [0x66B, 2],
    0xDC3036: [0x66B, 3],
    0xDC3037: [0x66B, 5],

    0xDC3038: [0x668, 1], # Fish Food Frenzy
    0xDC3039: [0x668, 2],
    0xDC303A: [0x668, 3],
    0xDC303B: [0x668, 5],


    0xDC303C: [0x66D, 1], # Fire-ball Frenzy
    0xDC303D: [0x66D, 2],
    0xDC303E: [0x66D, 3],
    0xDC303F: [0x66D, 5],

    0xDC3040: [0x672, 1], # Demolition Drainpipe
    0xDC3041: [0x672, 2],
    0xDC3042: [0x672, 3],
    0xDC3043: [0x672, 5],

    0xDC3044: [0x660, 1], # Ripsaw Rage
    0xDC3045: [0x660, 2],
    0xDC3046: [0x660, 3],
    0xDC3047: [0x660, 5],

    0xDC3048: [0x66E, 1], # Blazing Bazukas
    0xDC3049: [0x66E, 2],
    0xDC304A: [0x66E, 3],
    0xDC304B: [0x66E, 5],

    0xDC304C: [0x670, 1], # Low-G Labyrinth
    0xDC304D: [0x670, 2],
    0xDC304E: [0x670, 3],
    0xDC304F: [0x670, 5],


    0xDC3050: [0x673, 1], # Krevice Kreepers
    0xDC3051: [0x673, 2],
    0xDC3052: [0x673, 3],
    0xDC3053: [0x673, 5],

    0xDC3054: [0x65F, 1], # Tearaway Toboggan
    0xDC3055: [0x65F, 2],
    0xDC3056: [0x65F, 3],
    0xDC3057: [0x65F, 5],

    0xDC3058: [0x66C, 1], # Barrel Drop Bounce
    0xDC3059: [0x66C, 2],
    0xDC305A: [0x66C, 3],
    0xDC305B: [0x66C, 5],

    0xDC305C: [0x66F, 1], # Krack-Shot Kroc
    0xDC305D: [0x66F, 2],
    0xDC305E: [0x66F, 3],
    0xDC305F: [0x66F, 5],

    0xDC3060: [0x65E, 1], # Lemguin Lunge
    0xDC3061: [0x65E, 2],
    0xDC3062: [0x65E, 3],
    0xDC3063: [0x65E, 5],


    0xDC3064: [0x676, 1], # Buzzer Barrage
    0xDC3065: [0x676, 2],
    0xDC3066: [0x676, 3],
    0xDC3067: [0x676, 5],

    0xDC3068: [0x674, 1], # Kong-Fused Cliffs
    0xDC3069: [0x674, 2],
    0xDC306A: [0x674, 3],
    0xDC306B: [0x674, 5],

    0xDC306C: [0x669, 1], # Floodlit Fish
    0xDC306D: [0x669, 2],
    0xDC306E: [0x669, 3],
    0xDC306F: [0x669, 5],

    0xDC3070: [0x677, 1], # Pothole Panic
    0xDC3071: [0x677, 2],
    0xDC3072: [0x677, 3],
    0xDC3073: [0x677, 5],

    0xDC3074: [0x675, 1], # Ropey Rumpus
    0xDC3075: [0x675, 2],
    0xDC3076: [0x675, 3],
    0xDC3077: [0x675, 5],


    0xDC3078: [0x67A, 1], # Konveyor Rope Klash
    0xDC3079: [0x67A, 2],
    0xDC307A: [0x67A, 3],
    0xDC307B: [0x67A, 5],

    0xDC307C: [0x678, 1], # Creepy Caverns
    0xDC307D: [0x678, 2],
    0xDC307E: [0x678, 3],
    0xDC307F: [0x678, 5],

    0xDC3080: [0x665, 1], # Lightning Lookout
    0xDC3081: [0x665, 2],
    0xDC3082: [0x665, 3],
    0xDC3083: [0x665, 5],

    0xDC3084: [0x679, 1], # Koindozer Klamber
    0xDC3085: [0x679, 2],
    0xDC3086: [0x679, 3],
    0xDC3087: [0x679, 5],

    0xDC3088: [0x671, 1], # Poisonous Pipeline
    0xDC3089: [0x671, 2],
    0xDC308A: [0x671, 3],
    0xDC308B: [0x671, 5],


    0xDC308C: [0x67B, 1], # Stampede Sprint
    0xDC308D: [0x67B, 2],
    0xDC308E: [0x67B, 3],
    0xDC308F: [0x67B, 4],
    0xDC3090: [0x67B, 5],

    0xDC3091: [0x67C, 1], # Criss Kross Cliffs
    0xDC3092: [0x67C, 2],
    0xDC3093: [0x67C, 3],
    0xDC3094: [0x67C, 5],

    0xDC3095: [0x67D, 1], # Tyrant Twin Tussle
    0xDC3096: [0x67D, 2],
    0xDC3097: [0x67D, 3],
    0xDC3098: [0x67D, 4],
    0xDC3099: [0x67D, 5],

    0xDC309A: [0x663, 1], # Swoopy Salvo
    0xDC309B: [0x663, 2],
    0xDC309C: [0x663, 3],
    0xDC309D: [0x663, 4],
    0xDC309E: [0x663, 5],

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

    0xDC30B6: [0x5FD, 4], # Banana Bird Mother

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

class LocalRom(object):

    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        #if patch:
        #    self.patch_rom()
        #    self.orig_buffer = self.buffer.copy()
        #if vanillaRom:
        #    with open(vanillaRom, 'rb') as vanillaStream:
        #        self.orig_buffer = read_rom(vanillaStream)
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
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



def patch_rom(world, rom, player, active_level_list):
    local_random = world.slot_seeds[player]

    # Boomer Costs
    bonus_coin_cost = world.krematoa_bonus_coin_cost[player]
    inverted_bonus_coin_cost = 0x100 - bonus_coin_cost
    rom.write_byte(0x3498B9, inverted_bonus_coin_cost)
    rom.write_byte(0x3498BA, inverted_bonus_coin_cost)
    rom.write_byte(0x3498BB, inverted_bonus_coin_cost)
    rom.write_byte(0x3498BC, inverted_bonus_coin_cost)
    rom.write_byte(0x3498BD, inverted_bonus_coin_cost)

    rom.write_byte(0x349857, bonus_coin_cost)
    rom.write_byte(0x349862, bonus_coin_cost)

    # Gyrocopter Costs
    dk_coin_cost = world.dk_coins_for_gyrocopter[player]
    rom.write_byte(0x3484A6, dk_coin_cost)
    rom.write_byte(0x3484D5, dk_coin_cost)
    rom.write_byte(0x3484D7, 0x90)
    rom.write_byte(0x3484DC, 0xEA)
    rom.write_byte(0x3484DD, 0xEA)
    rom.write_byte(0x3484DE, 0xEA)
    rom.write_byte(0x348528, 0x80) # Prevent Single-Ski Lock


    # Make Swanky free
    rom.write_byte(0x348C48, 0x00)

    # Banana Bird Costs
    if world.goal[player] == "banana_bird_hunt":
        banana_bird_cost = math.floor(world.number_of_banana_birds[player] * world.percentage_of_banana_birds[player] / 100.0)
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
    if world.kong_palette_swap[player] == "default":
        rom.write_byte(0x3B96A9, 0x00)
        rom.write_byte(0x3B96A8, 0x00)
    elif world.kong_palette_swap[player] == "purple":
        rom.write_byte(0x3B96A9, 0x00)
        rom.write_byte(0x3B96A8, 0x3C)
    elif world.kong_palette_swap[player] == "spooky":
        rom.write_byte(0x3B96A9, 0x00)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.kong_palette_swap[player] == "dark":
        rom.write_byte(0x3B96A9, 0x05)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.kong_palette_swap[player] == "chocolate":
        rom.write_byte(0x3B96A9, 0x1D)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.kong_palette_swap[player] == "shadow":
        rom.write_byte(0x3B96A9, 0x45)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.kong_palette_swap[player] == "red_gold":
        rom.write_byte(0x3B96A9, 0x5D)
        rom.write_byte(0x3B96A8, 0xA0)
    elif world.kong_palette_swap[player] == "gbc":
        rom.write_byte(0x3B96A9, 0x20)
        rom.write_byte(0x3B96A8, 0x3C)
    elif world.kong_palette_swap[player] == "halloween":
        rom.write_byte(0x3B96A9, 0x70)
        rom.write_byte(0x3B96A8, 0x3C)

    if world.music_shuffle[player]:
        for address in music_rom_data:
            rand_song = local_random.choice(level_music_ids)
            rom.write_byte(address, rand_song)

    # Starting Lives
    rom.write_byte(0x9130, world.starting_life_count[player].value)
    rom.write_byte(0x913B, world.starting_life_count[player].value)


    # Handle Level Shuffle Here
    if world.level_shuffle[player]:
        for i in range(len(active_level_list)):
            rom.write_byte(level_dict[level_list[i]].nameIDAddress, level_dict[active_level_list[i]].nameID)
            rom.write_byte(level_dict[level_list[i]].levelIDAddress, level_dict[active_level_list[i]].levelID)

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

    if world.goal[player] == "knautilus":
        # Swap Kastle KAOS and Knautilus
        rom.write_byte(0x34D4E1, 0xC2)
        rom.write_byte(0x34D4E2, 0x24)
        rom.write_byte(0x34D551, 0xBA)
        rom.write_byte(0x34D552, 0x23)

        rom.write_byte(0x32F339, 0x55)


    from Main import __version__
    rom.name = bytearray(f'D3{__version__.replace(".", "")[0:3]}_{player}_{world.seed:11}\0', 'utf8')[:21]
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
        base_rom_bytes = bytes(read_rom(open(file_name, "rb")))

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
        file_name = Utils.local_path(file_name)
    return file_name
