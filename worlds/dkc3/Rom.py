import Utils
from Patch import read_rom
from .Locations import lookup_id_to_name, all_locations
from .Levels import level_list, level_dict

USHASH = '120abf304f0c40fe059f6a192ed4f947'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
import math


location_rom_data = {
    0xDC3000: [0x657, 1],
    0xDC3001: [0x657, 2],
    0xDC3002: [0x657, 3],
    0xDC3003: [0x657, 5],

    0xDC3004: [0x65A, 1],
    0xDC3005: [0x65A, 2],
    0xDC3006: [0x65A, 3],
    0xDC3007: [0x65A, 5],

    0xDC3008: [0x659, 1],
    0xDC3009: [0x659, 2],
    0xDC300A: [0x659, 3],
    0xDC300B: [0x659, 5],

    0xDC300C: [0x65D, 1],
    0xDC300D: [0x65D, 2],
    0xDC300E: [0x65D, 3],
    0xDC300F: [0x65D, 5],

    0xDC3010: [0x65C, 1],
    0xDC3011: [0x65C, 2],
    0xDC3012: [0x65C, 3],
    0xDC3013: [0x65C, 5],

    0xDC3014: [0x662, 1],
    0xDC3015: [0x662, 2],
    0xDC3016: [0x662, 3],
    0xDC3017: [0x662, 5],

    0xDC3018: [0x664, 1],
    0xDC3019: [0x664, 2],
    0xDC301A: [0x664, 3],
    0xDC301B: [0x664, 5],

    0xDC301C: [0x65B, 1],
    0xDC301D: [0x65B, 2],
    0xDC301E: [0x65B, 3],
    0xDC301F: [0x65B, 5],

    0xDC3020: [0x661, 1],
    0xDC3021: [0x661, 2],
    0xDC3022: [0x661, 3],
    0xDC3023: [0x661, 5],

    0xDC3024: [0x666, 1],
    0xDC3025: [0x666, 2],
    0xDC3026: [0x666, 3],
    0xDC3027: [0x666, 5],

    0xDC3028: [0x667, 1],
    0xDC3029: [0x667, 2],
    0xDC302A: [0x667, 3],
    0xDC302B: [0x667, 5],

    0xDC302C: [0x66A, 1],
    0xDC302D: [0x66A, 2],
    0xDC302E: [0x66A, 3],
    0xDC302F: [0x66A, 5],

    0xDC3030: [0x658, 1],
    0xDC3031: [0x658, 2],
    0xDC3032: [0x658, 3],
    0xDC3033: [0x658, 5],

    0xDC3034: [0x658, 1],
    0xDC3035: [0x658, 2],
    0xDC3036: [0x658, 3],
    0xDC3037: [0x658, 5],

    0xDC3038: [0x668, 1],
    0xDC3039: [0x668, 2],
    0xDC303A: [0x668, 3],
    0xDC303B: [0x668, 5],

    0xDC303C: [0x66D, 1],
    0xDC303D: [0x66D, 2],
    0xDC303E: [0x66D, 3],
    0xDC303F: [0x66D, 5],

    0xDC3040: [0x672, 1],
    0xDC3041: [0x672, 2],
    0xDC3042: [0x672, 3],
    0xDC3043: [0x672, 5],

    0xDC3044: [0x660, 1],
    0xDC3045: [0x660, 2],
    0xDC3046: [0x660, 3],
    0xDC3047: [0x660, 5],

    0xDC3048: [0x66E, 1],
    0xDC3049: [0x66E, 2],
    0xDC304A: [0x66E, 3],
    0xDC304B: [0x66E, 5],

    0xDC304C: [0x670, 1],
    0xDC304D: [0x670, 2],
    0xDC304E: [0x670, 3],
    0xDC304F: [0x670, 5],

    0xDC3050: [0x673, 1],
    0xDC3051: [0x673, 2],
    0xDC3052: [0x673, 3],
    0xDC3053: [0x673, 5],

    0xDC3054: [0x65F, 1],
    0xDC3055: [0x65F, 2],
    0xDC3056: [0x65F, 3],
    0xDC3057: [0x65F, 5],

    0xDC3058: [0x66C, 1],
    0xDC3059: [0x66C, 2],
    0xDC305A: [0x66C, 3],
    0xDC305B: [0x66C, 5],

    0xDC305C: [0x66F, 1],
    0xDC305D: [0x66F, 2],
    0xDC305E: [0x66F, 3],
    0xDC305F: [0x66F, 5],

    0xDC3060: [0x65E, 1],
    0xDC3061: [0x65E, 2],
    0xDC3062: [0x65E, 3],
    0xDC3063: [0x65E, 5],

    0xDC3064: [0x676, 1],
    0xDC3065: [0x676, 2],
    0xDC3066: [0x676, 3],
    0xDC3067: [0x676, 5],

    0xDC3068: [0x674, 1],
    0xDC3069: [0x674, 2],
    0xDC306A: [0x674, 3],
    0xDC306B: [0x674, 5],

    0xDC306C: [0x669, 1],
    0xDC306D: [0x669, 2],
    0xDC306E: [0x669, 3],
    0xDC306F: [0x669, 5],

    0xDC3070: [0x677, 1],
    0xDC3071: [0x677, 2],
    0xDC3072: [0x677, 3],
    0xDC3073: [0x677, 5],

    0xDC3074: [0x675, 1],
    0xDC3075: [0x675, 2],
    0xDC3076: [0x675, 3],
    0xDC3077: [0x675, 5],

    0xDC3078: [0x657, 1],
    0xDC3079: [0x657, 2],
    0xDC307A: [0x657, 3],
    0xDC307B: [0x657, 5],

    0xDC307C: [0x678, 1],
    0xDC307D: [0x678, 2],
    0xDC307E: [0x678, 3],
    0xDC307F: [0x678, 5],

    0xDC3080: [0x665, 1],
    0xDC3081: [0x665, 2],
    0xDC3082: [0x665, 3],
    0xDC3083: [0x665, 5],

    0xDC3084: [0x679, 1],
    0xDC3085: [0x679, 2],
    0xDC3086: [0x679, 3],
    0xDC3087: [0x679, 5],

    0xDC3088: [0x671, 1],
    0xDC3089: [0x671, 2],
    0xDC308A: [0x671, 3],
    0xDC308B: [0x671, 5],

    0xDC308C: [0x67B, 1],
    0xDC308D: [0x67B, 2],
    0xDC308E: [0x67B, 3],
    0xDC308F: [0x67B, 4],
    0xDC3090: [0x67B, 5],

    0xDC3091: [0x67C, 1],
    0xDC3092: [0x67C, 2],
    0xDC3093: [0x67C, 3],
    0xDC3094: [0x67C, 5],

    0xDC3095: [0x67D, 1],
    0xDC3096: [0x67D, 2],
    0xDC3097: [0x67D, 3],
    0xDC3098: [0x67D, 4],
    0xDC3099: [0x67D, 5],

    0xDC309A: [0x663, 1],
    0xDC309B: [0x663, 2],
    0xDC309C: [0x663, 3],
    0xDC309D: [0x663, 4],
    0xDC309E: [0x663, 5],

    0xDC309F: [0x67E, 1],
    0xDC30A0: [0x67E, 5],

    0xDC30A1: [0x64F, 1],
    0xDC30A2: [0x650, 1],
    0xDC30A3: [0x651, 1],
    0xDC30A4: [0x652, 1],
    0xDC30A5: [0x653, 1],
    0xDC30A6: [0x654, 1],
    0xDC30A7: [0x655, 1],
    0xDC30A8: [0x656, 1],

    0xDC30A9: [0x647, 1],
    0xDC30AA: [0x645, 1],
    0xDC30AB: [0x644, 1],
    0xDC30AC: [0x642, 1],
    0xDC30AD: [0x643, 1],
    0xDC30AE: [0x646, 1],
    0xDC30AF: [0x648, 1],
    0xDC30B0: [0x649, 1],
    0xDC30B1: [0x64A, 1],
    0xDC30B2: [0x64B, 1],
    0xDC30B3: [0x64C, 1],
    0xDC30B4: [0x64D, 1],
    0xDC30B5: [0x64E, 1],

    0xDC30B6: [0x615, 7], # DKC3_TODO: 

    0xDC30B7: [0x615, 2, True],
    0xDC30B8: [0x615, 3, True],
    0xDC30B9: [0x619, 2],
    #0xDC30BA:
    0xDC30BB: [0x61B, 3],
    0xDC30BC: [0x61D, 2],
    0xDC30BD: [0x621, 4],
    0xDC30BE: [0x625, 4, True],
}


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
    rom.write_byte(0x3498B9, bonus_coin_cost)
    rom.write_byte(0x3498BA, bonus_coin_cost)
    rom.write_byte(0x3498BB, bonus_coin_cost)
    rom.write_byte(0x3498BC, bonus_coin_cost)
    rom.write_byte(0x3498BD, bonus_coin_cost)

    # Gyrocopter Costs
    dk_coin_cost = world.dk_coins_for_gyrocopter[player]
    rom.write_byte(0x3484A6, dk_coin_cost)
    rom.write_byte(0x3484D5, dk_coin_cost)

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

    # Handle Level Shuffle Here
    if world.level_shuffle[player]:
        for i in range(len(active_level_list)):
            rom.write_byte(level_dict[level_list[i]].nameIDAddress, level_dict[active_level_list[i]].nameID)
            rom.write_byte(level_dict[level_list[i]].levelIDAddress, level_dict[active_level_list[i]].levelID)

        rom.write_byte(0x34BC3E, (0x32 + level_dict[active_level_list[0]].levelID))
        rom.write_byte(0x34BC47, (0x32 + level_dict[active_level_list[5]].levelID))
        rom.write_byte(0x34BC4A, (0x32 + level_dict[active_level_list[10]].levelID))
        rom.write_byte(0x34BC53, (0x32 + level_dict[active_level_list[15]].levelID))
        rom.write_byte(0x34BC59, (0x32 + level_dict[active_level_list[20]].levelID))
        rom.write_byte(0x34BC5C, (0x32 + level_dict[active_level_list[25]].levelID))
        rom.write_byte(0x34BC65, (0x32 + level_dict[active_level_list[30]].levelID))
        rom.write_byte(0x34BC6E, (0x32 + level_dict[active_level_list[35]].levelID))


    from Main import __version__
    rom.name = bytearray(f'BM{__version__.replace(".", "")[0:3]}_{player}_{world.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)




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
