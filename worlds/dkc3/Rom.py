import Utils
from Patch import read_rom
from .Locations import lookup_id_to_name, all_locations
from .Levels import level_list, level_dict

USHASH = '120abf304f0c40fe059f6a192ed4f947'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
import math


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
