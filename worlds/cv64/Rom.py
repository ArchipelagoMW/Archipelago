import Utils
from Utils import read_snes_rom
from worlds.Files import APDeltaPatch

import hashlib
import os
import math

from .Names import PatchName, LocationName
from .Levels import level_list, level_dict

USHASH = '1cc5cf3b4d29d8c3ade957648b529dc1'
BSUSHASH = '0bbaa6de2b9cbb822f8b4d85c1d5497b'
ROM_PLAYER_LIMIT = 65535


rom_loc_offsets = {
    0xC64001: 0x10C67B,  # Forest of Silence
    0xC64002: 0x10C71B,
    0xC64003: 0x10C6BB,
    0xC64004: 0x10C68B,
    0xC64005: 0x10C693,
    0xC64006: 0x10C6C3,
    0xC64007: 0x10C6E3,
    0xC64008: 0x10C6CB,
    0xC64009: 0x10C683,
    0xC6400A: 0x10C743,
    0xC6400B: 0x10C6A3,
    0xC6400C: 0x10C69B,
    0xC6400D: 0x10C6D3,
    0xC6400E: 0x10C6AB,
    0xC6400F: 0x10C76B,
    0xC64010: 0x10C75B,
    0xC64011: 0x10C713,
    0xC64012: 0x10C733,
    0xC64013: 0x10C6B3,
    0xC64014: 0x10C72B,
    0xC640A6: 0x7C7F9D,
    0xC640A7: 0xBFC937,  # Werewolf plaque

    0xC64015: 0x10C7F7,  # Castle Wall
    0xC64016: 0x10C7FF,
    0xC64017: 0x10C807,
    0xC64018: 0x10C817,
    0xC64019: 0x10C80F,
    0xC6401A: 0x10C7E7,
    0xC6401B: 0x10C7DF,
    0xC6401C: 0x10C7EF,
    0xC640A8: 0x7F99A9,
    0xC640A9: 0x7F9A3E,

    0xC6401D: 0x10C87F,  # Villa
    0xC6401E: 0x10C887,
    0xC6401F: 0x10C89F,
    0xC64020: 0x10C8A7,
    0xC64021: 0x10C897,
    0xC64022: 0x10C8AF,
    0xC64023: 0x10C8B7,
    0xC64024: 0x10C8C7,
    # 0xC64025: 0x10C8CF,
    0xC64026: 0x10C8D7,
    0xC64027: 0x10C8DF,
    0xC64028: 0x10C8E7,
    0xC64029: 0x10C8EF,
    0xC6402A: 0x10C927,
    0xC6402B: 0x10C90F,
    0xC6402C: 0x10C917,
    0xC6402D: 0x10C91F,
    0xC6402E: 0xBFC203,  # Vincent
    0xC6402F: 0x10C967,
    0xC64030: 0x10C947,
    0xC64031: 0x10C9A7,
    0xC64032: 0x10C96F,
    0xC64033: 0x10C977,
    0xC64034: 0x10C95F,
    0xC64035: 0x10C97F,
    0xC64036: 0x10C94F,
    0xC64037: 0x10C957,
    0xC64038: 0x10C92F,
    0xC64039: 0x10C93F,
    0xC6403A: 0x10C937,
    0xC6403B: 0x10CF4B,
    0xC6403C: 0x10CF63,
    0xC6403D: 0x10CF6B,
    0xC6403E: 0x10CF5B,
    0xC6403F: 0x10C8BF,
    0xC64040: 0x10CF53,
    0xC640AA: 0xBFC95F,  # Dog food gate
    0xC640AB: 0x8099CC,
    0xC640AC: 0xBFC957,  # Fountain FL
    0xC640AD: 0x80997D,
    0xC640AE: 0x809956,
    0xC640AF: 0x80992D,
    0xC640B0: 0xBFC95B,  # Fountain RL
    0xC640B1: 0x80993C,
    0xC640B2: 0x81F07C,
    0xC640B3: 0x83A5CA,
    0xC640B4: 0xBFC97F,  # Storeroom R
    0xC640B5: 0x83A604,
    0xC640B6: 0x83A588,
    0xC640B7: 0x83A593,
    0xC640B8: 0x83A635,
    0xC640B9: 0xBFC98B,  # Dining Room vase
    0xC640BA: 0xBFC98F,  # Archives table
    0xC640BB: 0x83A5B1,
    0xC640BC: 0x83A610,
    0xC640BD: 0xBFC987,  # Living room painting
    0xC640BE: 0x83A61B,
    0xC640BF: 0x850FEC,


    0xC64041: 0x10C9AF,  # Tunnel
    0xC64042: 0x10C9B7,
    0xC64043: 0x10CA9F,
    0xC64044: 0x10C9DF,
    0xC64045: 0x10C9E7,
    0xC64046: 0x10C9D7,
    0xC64047: 0x10C9CF,
    0xC64048: 0x10CA27,
    0xC64049: 0x10CAA7,
    0xC6404A: 0x10CAB7,
    0xC6404B: 0x10C9C7,
    0xC6404C: 0x10CA2F,
    0xC6404D: 0x10C9F7,
    0xC6404E: 0x10CA37,
    0xC6404F: 0x10C9FF,
    0xC64050: 0x10CA07,
    0xC64051: 0x10CA0F,
    0xC64052: 0x10CA3F,
    0xC64053: 0x10CA17,
    0xC64054: 0x10CA47,
    0xC64055: 0x10CA4F,
    0xC64056: 0x10CAAF,
    0xC640C0: 0xBFC9B7,  # Bucket
    0xC640C1: 0x86D8E1,
    0xC640C2: 0x86D8FC,

    0xC64057: 0x10CB03,  # Underground Waterway
    0xC64058: 0x10CAF3,
    0xC64059: 0x10CAFB,
    0xC6405A: 0x10CB23,
    0xC6405B: 0x10CB0B,
    0xC6405C: 0x10CB13,
    0xC6405D: 0x10CB33,
    0xC6405E: 0x10CB2B,

    0xC6405F: 0x10CB67,  # Castle Center
    0xC64060: 0x10CBD7,
    0xC64061: 0x10CB6F,
    0xC64062: 0x10CB77,
    0xC64063: 0x10CBA7,
    0xC64064: 0x10CB7F,
    0xC64065: 0x10CBAF,
    0xC64066: 0x10CBB7,
    0xC64067: 0x10CB87,
    0xC64068: 0x10CBBF,
    0xC64069: 0x10CB8F,
    0xC6406A: 0xBFC1E3,  # Mandragora shelf
    0xC6406B: 0x10CBF7,
    0xC6406C: 0x10CC17,
    0xC6406D: 0x10CC07,
    0xC6406E: 0x10CBFF,
    0xC6406F: 0x10CC33,
    0xC64070: 0x10CC3B,
    0xC64071: 0x10CC43,
    0xC64072: 0x10CC4B,
    0xC64073: 0x10CC53,
    0xC64074: 0x10CC8F,
    0xC64075: 0x10CC87,
    0xC64076: 0x10CC97,
    0xC64077: 0x10CC77,
    0xC64078: 0x10CC7F,
    0xC64079: 0x10CC9F,
    0xC6407A: 0x10CCA7,
    0xC6407B: 0x10CCAF,
    0xC6407C: 0x10CCB7,
    0xC6407D: 0xBFC20F,  # Blue lizard man
    0xC6407E: 0xBFC1C3,  # Nitro shelf
    0xC6407F: 0x10CCD7,
    0xC64080: 0x10CCDF,
    0xC64081: 0x10CCE7,
    0xC64082: 0x10CCFF,
    0xC64083: 0x10CD07,
    0xC640C3: 0x8985E5,
    0xC640C4: 0x8985D6,
    0xC640C5: 0x8C44D9,
    0xC640C6: 0x8C44E7,
    0xC640C7: 0x8C450A,
    0xC640C8: 0xBFC9D7,  # Lizard coffin nearside mid-right
    0xC640C9: 0xBFC9DB,  # Lizard coffin nearside mid-left
    0xC640CA: 0x8C451C,
    0xC640CB: 0x8C44fD,
    0xC640CC: 0x8C44F5,
    0xC640CD: 0x8DF782,
    0xC640CE: 0x8DF580,
    0xC640CF: 0x8F1197,
    0xC640D0: 0x90FCE9,
    0xC640D1: 0x90FCDA,
    0xC640D2: 0x90FBA7,
    0xC640D3: 0x90FBB3,
    0xC640D4: 0x90FBC0,
    0xC640D5: 0x90FF1D,
    0xC640D6: 0x90FE5C,

    0xC64084: 0x10CE73,  # Duel Tower
    0xC64085: 0x10CE7B,
    0xC64086: 0x10CE8B,
    0xC64087: 0x10CE93,

    0xC64088: 0x10CD1F,  # Tower of Execution
    0xC64089: 0x10CD27,
    0xC6408A: 0x10CD17,
    0xC6408B: 0x10CD47,
    0xC6408C: 0x10CD4F,
    0xC6408D: 0x10CD37,

    0xC6408E: 0x10CE0B,  # Tower of Science
    0xC6408F: 0x10CDF3,
    0xC64090: 0x10CE13,
    0xC64091: 0x10CDFB,
    0xC64092: 0x10CE3B,
    0xC64093: 0x10CE33,
    0xC64094: 0x10CE03,
    0xC64095: 0x10CE1B,
    0xC64096: 0x10CE23,

    0xC64097: 0x10CDB3,  # Tower of Sorcery
    0xC64098: 0x10CDBB,
    0xC64099: 0x10CDD3,
    0xC6409A: 0x10CDDB,
    0xC6409B: 0x10CDC3,
    0xC6409C: 0x10CDCB,
    0xC6409D: 0x10CDE3,

    0xC6409E: 0x10CF7B,  # Room of Clocks
    0xC6409F: 0x10CFB3,
    0xC640A0: 0x10CFBB,

    0xC640A1: 0x10CEB3,  # Clock Tower
    0xC640A2: 0x10CEC3,
    0xC640A3: 0x10CEBB,
    0xC640D7: 0x99BC4D,
    0xC640D8: 0x99BC3E,
    0xC640D9: 0x99BC30,

    0xC640A4: 0x10CE9B,  # Castle Keep
    0xC640A5: 0x10CEA3,
    0xC640DA: 0x9778C8,
    0xC640DB: 0xBFCA6B,  # Right flame
}

npc_items = {0xC6402E, 0xC6407D, 0xC6407E, 0xC6406A}
invis_items = {}

rom_item_bytes = {
    "White jewel": 0x01,
    "Red jewel(S)": 0x02,
    "Red jewel(L)": 0x03,
    "Special1": 0x04,
    "Special2": 0x05,
    "Roast chicken": 0x06,
    "Roast beef": 0x07,
    "Healing kit": 0x08,
    "Purifying": 0x09,
    "Cure ampoule": 0x0A,
    "pot-pourri": 0x0B,
    "PowerUp": 0x0C,
    "Holy water": 0x0D,
    "Cross": 0x0E,
    "Axe": 0x0F,
    "Knife": 0x10,
    "Wooden stake": 0x11,
    "Rose": 0x12,
    "The contract": 0x13,
    "engagement ring": 0x14,
    "Magical Nitro": 0x15,
    "Mandragora": 0x16,
    "Sun card": 0x17,
    "Moon card": 0x18,
    "Incandescent gaze": 0x19,
    "500 GOLD": 0x1A,
    "300 GOLD": 0x1B,
    "100 GOLD": 0x1C,
    "Archives key": 0x1D,
    "Left Tower Key": 0x1E,
    "Storeroom Key": 0x1F,
    "Garden Key": 0x20,
    "Copper Key": 0x21,
    "Chamber Key": 0x22,
    "Execution Key": 0x23,
    "Science Key1": 0x24,
    "Science Key2": 0x25,
    "Science Key3": 0x26,
    "Clocktower Key1": 0x27,
    "Clocktower Key2": 0x28,
    "Clocktower Key3": 0x29,
}

rom_invis_item_bytes = {
    "White jewel": 0x7E,
    "Red jewel(S)": 0x38,
    "Red jewel(L)": 0x39,
    "Special1": 0x7F,
    "Special2": 0x80,
    "Roast chicken": 0x3A,
    "Roast beef": 0x3B,
    "Healing kit": 0x3C,
    "Purifying": 0x3D,
    "Cure ampoule": 0x3E,
    "pot-pourri": 0x81,
    "PowerUp": 0x82,
    "Holy water": 0x83,
    "Cross": 0x84,
    "Axe": 0x85,
    "Knife": 0x86,
    "Wooden stake": 0x87,
    "Rose": 0x88,
    "The contract": 0x89,
    "engagement ring": 0x8A,
    "Magical Nitro": 0x8B,
    "Mandragora": 0x8C,
    "Sun card": 0x3F,
    "Moon card": 0x40,
    "Incandescent gaze": 0x8D,
    "500 GOLD": 0x41,
    "300 GOLD": 0x42,
    "100 GOLD": 0x43,
    "Archives key": 0x8E,
    "Left Tower Key": 0x8F,
    "Storeroom Key": 0x90,
    "Garden Key": 0x91,
    "Copper Key": 0x92,
    "Chamber Key": 0x93,
    "Execution Key": 0x94,
    "Science Key1": 0x95,
    "Science Key2": 0x96,
    "Science Key3": 0x97,
    "Clocktower Key1": 0x98,
    "Clocktower Key2": 0x99,
    "Clocktower Key3": 0x9A,
}

warp_scene_offsets = [0xADF77, 0xADF87, 0xADF97, 0xADFA7, 0xADFBB, 0xADFCB, 0xADFDF]


class LocalRom(object):

    def __init__(self, file, patch=True, vanilla_rom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_snes_rom(stream)
        # if patch:
        #    self.patch_rom()
        #    self.orig_buffer = self.buffer.copy()
        # if vanilla_rom:
        #    with open(vanillaRom, 'rb') as vanillaStream:
        #        self.orig_buffer = read_rom(vanillaStream)
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return (self.buffer[address] & bitflag) != 0

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


def patch_rom(world, rom, player, offsets_to_ids, active_level_list, warp_list):
    # local_random = world.slot_seeds[player]

    w1 = str(world.special1s_per_warp[player]).zfill(2)
    w2 = str(world.special1s_per_warp[player] * 2).zfill(2)
    w3 = str(world.special1s_per_warp[player] * 3).zfill(2)
    w4 = str(world.special1s_per_warp[player] * 4).zfill(2)
    w5 = str(world.special1s_per_warp[player] * 5).zfill(2)
    w6 = str(world.special1s_per_warp[player] * 6).zfill(2)
    w7 = str(world.special1s_per_warp[player] * 7).zfill(2)

    # NOP out the CRC BNEs
    rom.write_bytes(0x66C, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x678, [0x00, 0x00, 0x00, 0x00])

    # Always offer Hard Mode on file creation
    rom.write_bytes(0xC8810, [0x24, 0x0A, 0x01, 0x00])  # ADDIU	T2, R0, 0x0100

    # Disable Easy Mode cutoff point at Castle Center elevator
    rom.write_bytes(0xD9E18, [0x24, 0x0D, 0x00, 0x00])

    # Disable the Forest, Castle Wall, and Villa intro cutscenes and make it possible to change the starting level
    rom.write_byte(0xB73308, 0x00)
    rom.write_byte(0xB7331A, 0x40)
    rom.write_byte(0xB7332B, 0x4C)
    rom.write_byte(0xB6302B, 0x00)
    rom.write_byte(0x109F8F, 0x00)

    # Prevent Forest end cutscene flag from setting so it can be triggered infinitely
    rom.write_byte(0xEEA51, 0x01)

    # Make the CW drawbridge always closed (since rando doesn't play the CW intro cutscene that closes it)
    rom.write_bytes(0x6C00EC, [0x24, 0x0A, 0x00, 0x01])  # ADDIU T2, R0, 0x0001
    rom.write_bytes(0x6C0ADC, [0x24, 0x0A, 0x00, 0x01])  # ADDIU T2, R0, 0x0001

    # Villa coffin time-of-day hack
    rom.write_byte(0xD9D83, 0x74)
    rom.write_bytes(0xD9D84, [0x08, 0x0F, 0xF1, 0x4D])  # J 0x803FC534
    rom.write_bytes(0xBFC534, PatchName.coffin_time_checker)

    # Fix both Castle Center elevator bridges for both characters
    rom.write_bytes(0x6CEAA0, [0x24, 0x0B, 0x00, 0x01])
    rom.write_bytes(0x6CEAA4, [0x24, 0x0D, 0x00, 0x01])

    # Were-bull arena flag hack
    rom.write_bytes(0x6E38F0, [0x0C, 0x0F, 0xF1, 0x57])
    rom.write_bytes(0xBFC55C, PatchName.werebull_flag_unsetter)

    # Enable being able to carry multiple Special jewels, Nitros, and Mandragoras simultaneously
    rom.write_bytes(0xBF1F4, [0x3C, 0x03, 0x80, 0x39])  # LUI V1, 0x8039
    # Special1
    rom.write_bytes(0xBF210, [0x80, 0x65, 0x9C, 0x4B])  # LB A1, 0x9C4B (V1)
    rom.write_bytes(0xBF214, [0x24, 0xA5, 0x00, 0x01])  # ADDIU A1, A1, 0x0001
    rom.write_bytes(0xBF21C, [0xA0, 0x65, 0x9C, 0x4B])  # SB A1, 0x9C4B (V1)
    # Special2
    rom.write_bytes(0xBF230, [0x80, 0x65, 0x9C, 0x4C])  # LB A1, 0x9C4C (V1)
    rom.write_bytes(0xBF234, [0x24, 0xA5, 0x00, 0x01])  # ADDIU A1, A1, 0x0001
    rom.write_bytes(0xbf23C, [0xA0, 0x65, 0x9C, 0x4C])  # SB A1, 0x9C4C (V1)
    # Magical Nitro
    rom.write_bytes(0xBF360, [0x10, 0x00, 0x00, 0x04])  # B 0x8013C184
    rom.write_bytes(0xBF378, [0x25, 0xE5, 0x00, 0x01])  # ADDIU A1, T7, 0x0001
    rom.write_bytes(0xBF37C, [0x10, 0x00, 0x00, 0x03])  # B 0x8013C19C
    # Mandragora
    rom.write_bytes(0xBF3A8, [0x10, 0x00, 0x00, 0x04])  # B 0x8013C1CC
    rom.write_bytes(0xBF3C0, [0x25, 0x05, 0x00, 0x01])  # ADDIU A1, T0, 0x0001
    rom.write_bytes(0xBF3C4, [0x10, 0x00, 0x00, 0x03])  # B 0x8013C1E4

    # Give PowerUps their Legacy of Darkness behavior when attempting to pick up more than two
    rom.write_bytes(0xA9730, [0x24, 0x09, 0x00, 0x00])  # ADDIU	T1, R0, 0x0000
    rom.write_bytes(0xBF2FC, [0x08, 0x0F, 0xF1, 0x6D])  # J	0x803FC5B4
    rom.write_bytes(0xBF300, [0x00, 0x00, 0x00, 0x00])  # NOP
    rom.write_bytes(0xBFC5B4, PatchName.give_powerup_stopper)

    # Rename "Wooden stake" and "Rose" to "Sent major" and "Sent" respectively
    rom.write_bytes(0xEFE34, cv64_text_converter("Sent major  ", False))
    rom.write_bytes(0xEFE4E, cv64_text_converter("Sent", False))

    # Change the Stage Select menu options
    rom.write_bytes(0xADF64, PatchName.warp_menu_rewrite)
    rom.write_bytes(0x10E0C8, PatchName.warp_pointer_table)
    rom.write_byte(0xADF67, level_dict[active_level_list[0]].startSceneID)
    for i in range(len(warp_list)):
        rom.write_byte(warp_scene_offsets[i], level_dict[warp_list[i]].midSceneID)
        rom.write_byte(warp_scene_offsets[i] + 4, level_dict[warp_list[i]].midSpawnID)

    # Play the "teleportation" sound effect when teleporting
    rom.write_bytes(0xAE088, [0x08, 0x00, 0x4F, 0xAB,   # J 0x80013EAC
                              0x24, 0x04, 0x01, 0x9E])  # ADDIU A0, R0, 0x019E

    # Change the Stage Select menu's text to reflect its new purpose
    rom.write_bytes(0xEFAD0, cv64_text_converter(f"Where to...?\t{active_level_list[0]}\t"
                                                 f"`{w1} {warp_list[0]}\t"
                                                 f"`{w2} {warp_list[1]}\t"
                                                 f"`{w3} {warp_list[2]}\t"
                                                 f"`{w4} {warp_list[3]}\t"
                                                 f"`{w5} {warp_list[4]}\t"
                                                 f"`{w6} {warp_list[5]}\t"
                                                 f"`{w7} {warp_list[6]}", False))

    # Lizard-man save proofing
    rom.write_bytes(0xA99AC, [0x08, 0x0F, 0xF0, 0xB8])  # J 0x803FC2E0
    rom.write_bytes(0xBFC2E0, PatchName.boss_save_stopper)

    # Disable or guarantee vampire Vincent's fight
    if world.fight_vincent[player] == "never":
        rom.write_bytes(0xAACC0, [0x24, 0x01, 0x00, 0x01])  # ADDIU AT, R0, 0x0001
    elif world.fight_vincent[player] == "always":
        rom.write_bytes(0xAACE0, [0x24, 0x18, 0x00, 0x10])  # ADDIU	T8, R0, 0x0010
    else:
        rom.write_bytes(0xAACE0, [0x24, 0x18, 0x00, 0x00])  # ADDIU	T8, R0, 0x0000

    # Disable or guarantee Renon's fight
    rom.write_bytes(0xAACB4, [0x08, 0x0F, 0xF1, 0xA4])  # J 0x803FC690
    if world.fight_renon[player] == "never":
        rom.write_byte(0xB804F0, 0x00)
        rom.write_byte(0xB80632, 0x00)
        rom.write_byte(0xB80988, 0xB8)
        rom.write_byte(0xB816BD, 0xB8)
        rom.write_bytes(0xBFC690, PatchName.renon_cutscene_checker_jr)
    elif world.fight_renon[player] == "always":
        rom.write_byte(0xB804F0, 0x0C)
        rom.write_byte(0xB80632, 0x0C)
        rom.write_byte(0xB80988, 0xC4)
        rom.write_byte(0xB816BD, 0xC4)
        rom.write_bytes(0xBFC690, PatchName.renon_cutscene_checker_jr)
    else:
        rom.write_bytes(0xBFC690, PatchName.renon_cutscene_checker)

    # Disable or guarantee the Bad Ending
    if world.bad_ending_condition[player] == "never":
        rom.write_bytes(0xAEE5C6, [0x3C, 0x0A, 0x00, 0x00])  # LUI  T2, 0x0000
    elif world.bad_ending_condition[player] == "always":
        rom.write_bytes(0xAEE5C6, [0x3C, 0x0A, 0x00, 0x40])  # LUI  T2, 0x0040

    # Play Castle Keep's song if teleporting in front of Dracula's door outside the escape sequence
    rom.write_bytes(0x6E937C, [0x08, 0x0F, 0xF1, 0x2E])
    rom.write_bytes(0xBFC4B8, PatchName.ck_door_music_player)

    # Increase item capacity to 100
    if world.increase_item_limit[player]:
        rom.write_byte(0xBF30B, 0x64)

    # Prevent the vanilla Magical Nitro transport's "can explode" flag from setting
    rom.write_bytes(0xB5D7AA, [0x00, 0x00, 0x00, 0x00])

    # Enable the Game Over's "Continue" menu starting the cursor on whichever checkpoint is most recent
    rom.write_bytes(0xB4DDC, [0x0C, 0x06, 0x0D, 0x58])  # JAL 0x80183560
    rom.write_bytes(0x106750, PatchName.continue_cursor_start_checker)
    rom.write_bytes(0x1C444, [0x08, 0x0F, 0xF0, 0x90])  # J   0x803FC240
    rom.write_bytes(0xBFC240, PatchName.savepoint_cursor_updater)
    rom.write_bytes(0x1C2D0, [0x08, 0x0F, 0xF0, 0x94])  # J   0x803FC250
    rom.write_bytes(0xBFC250, PatchName.stage_start_cursor_updater)
    rom.write_byte(0xB585C8, 0xFF)

    # Add data for White Jewel #22 (the new Duel Tower savepoint) at the end of the White Jewel ID data list
    rom.write_bytes(0x104AC8, [0x00, 0x00, 0x00, 0x06,
                               0x00, 0x13, 0x00, 0x15])

    # Spawn coordinates list extension
    rom.write_bytes(0xD5BF4, [0x08, 0x0F, 0xF1, 0x03])  # J	0x803FC40C
    rom.write_bytes(0xBFC40C, PatchName.spawn_coordinates_extension)
    rom.write_bytes(0x108A5E, PatchName.waterway_end_coordinates)

    # Change the File Select stage numbers to match the new stage order. Also fix a vanilla issue wherein saving in a
    # character-exclusive stage as the other character would incorrectly display the name of that character's equivalent
    # stage on the save file instead of the one they're actually in.
    rom.write_byte(0xC9FE3, 0xD4)
    rom.write_byte(0xCA055, 0x08)
    rom.write_byte(0xCA066, 0x40)
    rom.write_bytes(0xCA068, [0x86, 0x0C, 0x17, 0xD0])  # LH T4, 0x17D0 (S0)
    rom.write_byte(0xCA06D, 0x08)
    rom.write_byte(0x104A31, 0x01)
    rom.write_byte(0x104A39, 0x01)
    rom.write_byte(0x104A89, 0x01)
    rom.write_byte(0x104A91, 0x01)
    rom.write_byte(0x104A99, 0x01)
    rom.write_byte(0x104AA1, 0x01)

    stage_number = 0x01
    for i in range(len(active_level_list) - 1):
        for offset in level_dict[active_level_list[i]].stageNumberOffsetList:
            rom.write_byte(offset, stage_number)
        if active_level_list[i - 2] == LocationName.castle_center:
            stage_number -= 1
        elif active_level_list[i - 1] != LocationName.villa:
            stage_number += 1

    # Top elevator switch check
    rom.write_bytes(0x6CF0A0, [0x0C, 0x0F, 0xF0, 0xAF])  # JAL 0x803FC2BC
    rom.write_bytes(0xBFC2BC, PatchName.elevator_flag_checker)

    # Waterway brick platforms skip
    if world.skip_waterway_platforms[player]:
        rom.write_bytes(0x6C7E2C, [0x00, 0x00, 0x00, 0x00])  # NOP

    # Disable time restrictions
    if world.disable_time_restrictions[player]:
        # Fountain
        rom.write_bytes(0x6C2340, [0x00, 0x00, 0x00, 0x00])  # NOP
        rom.write_bytes(0x6C257C, [0x10, 0x00, 0x00, 0x23])  # B [forward 0x23]
        # Rosa
        rom.write_byte(0xEEAAB, 0x00)
        rom.write_byte(0xEEAAD, 0x18)
        # Moon doors
        rom.write_bytes(0xDC3E0, [0x00, 0x00, 0x00, 0x00])  # NOP
        rom.write_bytes(0xDC3E8, [0x00, 0x00, 0x00, 0x00])  # NOP
        # Sun doors
        rom.write_bytes(0xDC410, [0x00, 0x00, 0x00, 0x00])  # NOP
        rom.write_bytes(0xDC418, [0x00, 0x00, 0x00, 0x00])  # NOP

    # Custom data-loading code
    rom.write_bytes(0x6B5028, [0x08, 0x06, 0x0D, 0x70])  # J 0x801835D0
    rom.write_bytes(0x1067B0, PatchName.custom_code_loader)

    # Custom remote item rewarding and DeathLink receiving code
    rom.write_bytes(0x19B98, [0x08, 0x0F, 0xF0, 0x00])  # J 0x803FC000
    rom.write_bytes(0xBFC000, PatchName.remote_item_giver)

    # DeathLink counter decrementer code
    rom.write_bytes(0x1C2A0, [0x08, 0x0F, 0xF0, 0x52])  # J 0x803FC148
    rom.write_bytes(0x1C340, [0x08, 0x0F, 0xF0, 0x52])  # J 0x803FC148
    rom.write_bytes(0xBFC148, PatchName.deathlink_counter_decrementer)

    # Death flag un-setter on "Beginning of stage" state overwrite code
    rom.write_bytes(0x1C2B0, [0x08, 0x0F, 0xF0, 0x47])  # J 0x803FC11C
    rom.write_bytes(0xBFC11C, PatchName.death_flag_unsetter)

    # Warp menu-opening code
    rom.write_bytes(0xB9BA8, [0x08, 0x0F, 0xF0, 0x9B])  # J	0x803FC26C
    rom.write_bytes(0xBFC26C, PatchName.warp_menu_opener)

    # NPC item textbox hack
    rom.write_bytes(0xBF1DC, [0x08, 0x0F, 0xF0, 0x67])  # J 0x803FC19C
    rom.write_bytes(0xBF1E0, [0x27, 0xBD, 0xFF, 0xE0])  # ADDIU SP, SP, -0x20
    rom.write_bytes(0xBFC19C, PatchName.npc_item_hack)

    # Sub-weapon check function hook
    rom.write_bytes(0xBF32C, [0x00, 0x00, 0x00, 0x00])  # NOP
    rom.write_bytes(0xBF330, [0x08, 0x0F, 0xF0, 0x5D])  # J	0x803FC174
    rom.write_bytes(0xBFC174, PatchName.give_subweapon_stopper)

    # Warp menu Special1 restriction
    rom.write_bytes(0xADD68, [0x0C, 0x04, 0xAB, 0x12])  # JAL 0x8012AC48
    rom.write_bytes(0xADE28, PatchName.stage_select_overwrite)
    rom.write_byte(0xADE47, world.special1s_per_warp[player])

    # Dracula's door text pointer hijack
    rom.write_bytes(0xD69F0, [0x08, 0x0F, 0xF1, 0x41])  # J 0x803FC504
    rom.write_bytes(0xBFC504, PatchName.dracula_door_text_redirector)

    # Dracula's chamber condition
    rom.write_bytes(0xE2FDC, [0x08, 0x04, 0xAB, 0x25])  # J 0x8012AC78
    rom.write_bytes(0xADE84, PatchName.special_goal_checker)
    rom.write_bytes(0xBFCC3C, [0xA0, 0x00, 0xFF, 0xFF, 0xA0, 0x01, 0xFF, 0xFF, 0xA0, 0x02, 0xFF, 0xFF, 0xA0, 0x03, 0xFF,
                               0xFF, 0xA0, 0x04, 0xFF, 0xFF, 0xA0, 0x05, 0xFF, 0xFF, 0xA0, 0x06, 0xFF, 0xFF, 0xA0, 0x07,
                               0xFF, 0xFF, 0xA0, 0x08, 0xFF, 0xFF, 0xA0, 0x09])
    if world.draculas_condition[player] == 1:
        rom.write_bytes(0x6C8A54, [0x0C, 0x0F, 0xF0, 0x89])  # JAL 0x803FC224
        rom.write_bytes(0xBFC224, PatchName.crystal_special2_giver)
        rom.write_byte(0xADE8F, 0x01)
        rom.write_bytes(0xBFCC62, cv64_text_converter(f"It won't budge!\n"
                                                      f"You'll need the power\n"
                                                      f"of the basement crystal\n"
                                                      f"to undo the seal.", True))
    elif world.draculas_condition[player] == 2:
        rom.write_bytes(0xBBD50, [0x08, 0x0F, 0xF1, 0x8D])  # J	0x803FC634
        rom.write_bytes(0xBFC634, PatchName.boss_speical2_giver)
        rom.write_bytes(0xBFC55C, PatchName.werebull_flag_unsetter_special2_electric_boogaloo)
        rom.write_byte(0xADE8F, world.bosses_required[player].value)
        rom.write_bytes(0xBFCC62, cv64_text_converter(f"It won't budge!\n"
                                                      f"You'll need to defeat\n"
                                                      f"{world.bosses_required[player].value} powerful monsters\n"
                                                      f"to undo the seal.", True))
    elif world.draculas_condition[player] == 3:
        rom.write_byte(0xADE8F, world.special2s_required[player].value)
        rom.write_bytes(0xBFCC62, cv64_text_converter(f"It won't budge!\n"
                                                      f"You'll need to find\n"
                                                      f"{world.special2s_required[player].value} Special2 jewels\n"
                                                      f"to undo the seal.", True))
    else:
        rom.write_byte(0xADE8F, 0x00)

    # On-the-fly TLB script modifier
    rom.write_bytes(0xBFC338, PatchName.double_component_checker)
    rom.write_bytes(0xBFC3D4, PatchName.downstairs_seal_checker)
    rom.write_bytes(0xBFC700, PatchName.tlb_modifiers)

    # On-the-fly scene object data modifier hook
    rom.write_bytes(0xEAB04, [0x08, 0x0F, 0xF2, 0x40])  # J 0x803FC900
    rom.write_bytes(0xBFC8F8, PatchName.scene_data_modifiers)

    # Fix locked doors to check the key counters instead of their vanilla key locations' flags
    # Pickup flag check modifications:
    rom.write_bytes(0x10B2D8, [0x00, 0x00, 0x00, 0x02])  # Left Tower Door
    rom.write_bytes(0x10B2F0, [0x00, 0x00, 0x00, 0x03])  # Storeroom Door
    rom.write_bytes(0x10B2FC, [0x00, 0x00, 0x00, 0x01])  # Archives Door
    rom.write_bytes(0x10B314, [0x00, 0x00, 0x00, 0x04])  # Maze Gate
    rom.write_bytes(0x10B350, [0x00, 0x00, 0x00, 0x05])  # Copper Door
    rom.write_bytes(0x10B3A4, [0x00, 0x00, 0x00, 0x06])  # Torture Chamber Door
    rom.write_bytes(0x10B3B0, [0x00, 0x00, 0x00, 0x07])  # ToE Gate
    rom.write_bytes(0x10B3BC, [0x00, 0x00, 0x00, 0x08])  # Science Door1
    rom.write_bytes(0x10B3C8, [0x00, 0x00, 0x00, 0x09])  # Science Door2
    rom.write_bytes(0x10B3D4, [0x00, 0x00, 0x00, 0x0A])  # Science Door3
    rom.write_bytes(0x6F0094, [0x00, 0x00, 0x00, 0x0B])  # CT Door 1
    rom.write_bytes(0x6F00A4, [0x00, 0x00, 0x00, 0x0C])  # CT Door 2
    rom.write_bytes(0x6F00B4, [0x00, 0x00, 0x00, 0x0D])  # CT Door 3
    # Item counter decrement check modifications:
    rom.write_bytes(0xEDA84, [0x00, 0x00, 0x00, 0x01])   # Archives Door
    rom.write_bytes(0xEDA8C, [0x00, 0x00, 0x00, 0x02])   # Left Tower Door
    rom.write_bytes(0xEDA94, [0x00, 0x00, 0x00, 0x03])   # Storeroom Door
    rom.write_bytes(0xEDA9C, [0x00, 0x00, 0x00, 0x04])   # Maze Gate
    rom.write_bytes(0xEDAA4, [0x00, 0x00, 0x00, 0x05])   # Copper Door
    rom.write_bytes(0xEDAAC, [0x00, 0x00, 0x00, 0x06])   # Torture Chamber Door
    rom.write_bytes(0xEDAB4, [0x00, 0x00, 0x00, 0x07])   # ToE Gate
    rom.write_bytes(0xEDABC, [0x00, 0x00, 0x00, 0x08])   # Science Door1
    rom.write_bytes(0xEDAC4, [0x00, 0x00, 0x00, 0x09])   # Science Door2
    rom.write_bytes(0xEDACC, [0x00, 0x00, 0x00, 0x0A])   # Science Door3
    rom.write_bytes(0xEDAD4, [0x00, 0x00, 0x00, 0x0B])   # CT Door 1
    rom.write_bytes(0xEDADC, [0x00, 0x00, 0x00, 0x0C])   # CT Door 2
    rom.write_bytes(0xEDAE4, [0x00, 0x00, 0x00, 0x0D])   # CT Door 3

    rom.write_bytes(0x10AB2C, [0x80, 0x15, 0xFB, 0xD4])  # Maze Gates' check code pointer adjustments
    rom.write_bytes(0x10AB40, [0x80, 0x15, 0xFB, 0xD4])
    rom.write_bytes(0xE2E14, PatchName.normal_door_hook)
    rom.write_bytes(0xBFC5D0, PatchName.normal_door_code)
    rom.write_bytes(0x6EF298, PatchName.ct_door_hook)
    rom.write_bytes(0xBFC608, PatchName.ct_door_code)

    # Make the Easy-only candle drops in Room of Clocks appear on any difficulty
    rom.write_byte(0x9B518F, 0x01)

    # Slightly move some once-invisible freestanding items to be more visible
    if world.reveal_invisible_items[player]:
        rom.write_byte(0x7C7F95, 0xEF)  # Forest dirge maiden statue
        rom.write_byte(0x7C7FA8, 0xAB)  # Forest werewolf statue
        rom.write_byte(0x8099C4, 0x8C)  # Villa courtyard tombstone
        rom.write_byte(0x83A626, 0xC2)  # Villa living room painting
        rom.write_byte(0x83A62F, 0x64)  # Villa living room painting
        rom.write_byte(0x8985DD, 0xF5)  # CC torture instrument rack
        rom.write_byte(0x8C44D0, 0x22)  # CC red carpet hallway knight
        rom.write_byte(0x8DF57C, 0xF1)  # CC cracked wall hallway flamethrower
        rom.write_byte(0x90FCD6, 0xA5)  # CC nitro hallway flamethrower
        rom.write_byte(0x90FB9F, 0x9A)  # CC invention room round machine
        rom.write_byte(0x90FBAF, 0x03)  # CC invention room giant famicart
        rom.write_byte(0x90FE54, 0x97)  # CC staircase knight (x)
        rom.write_byte(0x90FE58, 0xFB)  # CC staircase knight (z)

    # Write the new scene/spawn IDs for Stage Shuffle
    if world.stage_shuffle[player]:
        rom.write_byte(0xB73308, level_dict[active_level_list[0]].startSceneID)
        rom.write_byte(0xD9DAB, level_dict[active_level_list[active_level_list.index(LocationName.villa) + 2]].startSceneID)
        rom.write_byte(0x109CCF, level_dict[active_level_list[active_level_list.index(LocationName.castle_center) + 3]].startSceneID)
        for i in range(len(active_level_list) - 1):
            if active_level_list[i - 1] == LocationName.villa:
                rom.write_byte(level_dict[active_level_list[i]].endzoneSceneOffset,
                               level_dict[active_level_list[i + 2]].startSceneID)
                rom.write_byte(level_dict[active_level_list[i]].endzoneSpawnOffset,
                               level_dict[active_level_list[i + 2]].startSpawnID)
            elif active_level_list[i - 2] == LocationName.castle_center:
                rom.write_byte(level_dict[active_level_list[i]].endzoneSceneOffset,
                               level_dict[active_level_list[i + 3]].startSceneID)
                rom.write_byte(level_dict[active_level_list[i]].endzoneSpawnOffset,
                               level_dict[active_level_list[i + 3]].startSpawnID)
            else:
                rom.write_byte(level_dict[active_level_list[i]].endzoneSceneOffset, level_dict[active_level_list[i + 1]].startSceneID)
                rom.write_byte(level_dict[active_level_list[i]].endzoneSpawnOffset, level_dict[active_level_list[i + 1]].startSpawnID)

            if level_dict[active_level_list[i]].startzoneSceneOffset != 0xFFFFFF:
                if i - 1 < 0:
                    rom.write_byte(level_dict[active_level_list[i]].startzoneSceneOffset,
                                   level_dict[active_level_list[i]].startSceneID)
                elif active_level_list[i - 2] == LocationName.villa:
                    rom.write_byte(level_dict[active_level_list[i]].startzoneSceneOffset, 0x1A)
                    rom.write_byte(level_dict[active_level_list[i]].startzoneSpawnOffset, 0x03)
                elif active_level_list[i - 3] == LocationName.castle_center:
                    rom.write_byte(level_dict[active_level_list[i]].startzoneSceneOffset, 0x0F)
                    rom.write_byte(level_dict[active_level_list[i]].startzoneSpawnOffset, 0x03)
                else:
                    rom.write_byte(level_dict[active_level_list[i]].startzoneSceneOffset,
                                   level_dict[active_level_list[i - 1]].endSceneID)
                    rom.write_byte(level_dict[active_level_list[i]].startzoneSpawnOffset,
                                   level_dict[active_level_list[i - 1]].endSpawnID)

    # Write the new item bytes
    for offset, item_id in offsets_to_ids.items():
        rom.write_byte(offset, item_id)


class CV64DeltaPatch(APDeltaPatch):
    hash = USHASH
    bshash = BSUSHASH
    game = "Castlevania 64"
    patch_file_ending = ".apcv64"

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
        if USHASH != basemd5.hexdigest() and BSUSHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it.')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["cv64_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


def cv64_text_converter(cv64text, a_advance) -> list:
    char_dict = {
        "\n": 0x01,
        " ": 0x02,
        "!": 0x03,
        '"': 0x04,
        "#": 0x05,
        "$": 0x06,
        "%": 0x07,
        "&": 0x08,
        "'": 0x09,
        "(": 0x0A,
        ")": 0x0B,
        "*": 0x0C,
        "+": 0x0D,
        ",": 0x0E,
        "-": 0x0F,
        ".": 0x10,
        "/": 0x11,
        "0": 0x12,
        "1": 0x13,
        "2": 0x14,
        "3": 0x15,
        "4": 0x16,
        "5": 0x17,
        "6": 0x18,
        "7": 0x19,
        "8": 0x1A,
        "9": 0x1B,
        ":": 0x1C,
        ";": 0x1D,
        "<": 0x1E,
        "=": 0x1F,
        ">": 0x20,
        "?": 0x21,
        "@": 0x22,
        "A": 0x23,
        "B": 0x24,
        "C": 0x25,
        "D": 0x26,
        "E": 0x27,
        "F": 0x28,
        "G": 0x29,
        "H": 0x2A,
        "I": 0x2B,
        "J": 0x2C,
        "K": 0x2D,
        "L": 0x2E,
        "M": 0x2F,
        "N": 0x30,
        "O": 0x31,
        "P": 0x32,
        "Q": 0x33,
        "R": 0x34,
        "S": 0x35,
        "T": 0x36,
        "U": 0x37,
        "V": 0x38,
        "W": 0x39,
        "X": 0x3A,
        "Y": 0x3B,
        "Z": 0x3C,
        "[": 0x3D,
        "\\": 0x3E,
        "]": 0x3F,
        "^": 0x40,
        "_": 0x41,

        "a": 0x43,
        "b": 0x44,
        "c": 0x45,
        "d": 0x46,
        "e": 0x47,
        "f": 0x48,
        "g": 0x49,
        "h": 0x4A,
        "i": 0x4B,
        "j": 0x4C,
        "k": 0x4D,
        "l": 0x4E,
        "m": 0x4F,
        "n": 0x50,
        "o": 0x51,
        "p": 0x52,
        "q": 0x53,
        "r": 0x54,
        "s": 0x55,
        "t": 0x56,
        "u": 0x57,
        "v": 0x58,
        "w": 0x59,
        "x": 0x5A,
        "y": 0x5B,
        "z": 0x5C,
        "{": 0x5D,
        "|": 0x5E,
        "}": 0x5F,

        "`": 0x61,
        "「": 0x62,
        "」": 0x63,

        "~": 0x65,






        "″": 0x72,
        "°": 0x73,
        "∞": 0x74
    }

    textbytes = []
    for i in cv64text:
        if i == "\t":
            textbytes.append(0xFF)
            textbytes.append(0xFF)
        else:
            textbytes.append(0x00)
            textbytes.append(char_dict[i])
    if a_advance:
        textbytes.append(0xA3)
        textbytes.append(0x00)
    textbytes.append(0xFF)
    textbytes.append(0xFF)
    return textbytes

