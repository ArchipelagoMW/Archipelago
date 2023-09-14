import Utils

from worlds.Files import APDeltaPatch
from BaseClasses import ItemClassification

import hashlib
import os

from . import Patches
from .Names import RName
from .Locations import base_id
from .Stages import stage_info
from .Text import cv64_string_to_bytes, cv64_text_truncate, cv64_text_wrap
from .LZKN64 import compress_buffer

USHASH = '1cc5cf3b4d29d8c3ade957648b529dc1'
BSUSHASH = '0bbaa6de2b9cbb822f8b4d85c1d5497b'
ROM_PLAYER_LIMIT = 65535


rom_sub_weapon_offsets = {
    0x10C6EB: 0x10,  # Forest
    0x10C6F3: 0x0F,
    0x10C6FB: 0x0E,
    0x10C703: 0x0D,

    0x10C81F: 0x0F,  # Castle Wall
    0x10C827: 0x10,
    0x10C82F: 0x0E,
    0x7F9A0F: 0x0D,

    0x83A5D9: 0x0E,  # Villa
    0x83A5E5: 0x0D,
    0x83A5F1: 0x0F,
    0xBFC903: 0x10,
    0x10C987: 0x10,
    0x10C98F: 0x0D,
    0x10C997: 0x0F,
    0x10CF73: 0x10,

    0x10CA57: 0x0D,  # Tunnel
    0x10CA5F: 0x0E,
    0x10CA67: 0x10,
    0x10CA6F: 0x0D,
    0x10CA77: 0x0F,
    0x10CA7F: 0x0E,

    0x10CBC7: 0x0E,  # Castle Center
    0x10CC0F: 0x0D,
    0x10CC5B: 0x0F,

    0x10CD3F: 0x0E,  # Character towers
    0x10CE2B: 0x0E,
    0x10CE83: 0x10,

    0x10CF8B: 0x0F,  # Room of Clocks
    0x10CF93: 0x0D,

    0x99BC5A: 0x0D,  # Clock Tower
    0x10CECB: 0x10,
    0x10CED3: 0x0F,
    0x10CEDB: 0x0E,
    0x10CEE3: 0x0D,
}

rom_sub_weapon_flags = {
    0x10C6EC: 0x0200FF04,  # Forest of Silence
    0x10C6FC: 0x0400FF04,
    0x10C6F4: 0x0800FF04,
    0x10C704: 0x4000FF04,

    0x10C831: 0x08,  # Castle Wall
    0x10C829: 0x10,
    0x10C821: 0x20,

    # Villa
    0xBFC926: 0xFF04,
    0xBFC93A: 0x80,
    0xBFC93F: 0x01,
    0xBFC943: 0x40,
    0xBFC947: 0x80,
    0x10C989: 0x10,
    0x10C991: 0x20,
    0x10C999: 0x40,
    0x10CF77: 0x80,

    0x10CA58: 0x4000FF0E,  # Tunnel
    0x10CA6B: 0x80,
    0x10CA60: 0x1000FF05,
    0x10CA70: 0x2000FF05,
    0x10CA78: 0x4000FF05,
    0x10CA80: 0x8000FF05,

    0x10CBCA: 0x02,  # Castle Center
    0x10CC10: 0x80,
    0x10CC5C: 0x40,

    0x10CE86: 0x01,  # Duel Tower
    0x10CD43: 0x02,  # Tower of Execution
    0x10CE2E: 0x20,  # Tower of Science

    0x10CF8E: 0x04,  # Room of Clocks
    0x10CF96: 0x08,

    0x10CECE: 0x08,  # Clock Tower
    0x10CED6: 0x10,
    0x10CEE6: 0x20,
    0x10CEDE: 0x80,
}

rom_empty_breakables_flags = {
    0x10C74D: 0x40FF05,  # Forest of Silence
    0x10C765: 0x20FF0E,
    0x10C774: 0x0800FF0E,
    0x10C755: 0x80FF05,
    0x10C784: 0x0100FF0E,
    0x10C73C: 0x0200FF0E,

    0x10C8D0: 0x0400FF0E,  # Villa foyer

    0x10CF9F: 0x08,  # Room of Clocks flags
    0x10CFA7: 0x01,
    0xBFCB6F: 0x04,  # Room of Clocks candle property IDs
    0xBFCB73: 0x05,
}

rom_axe_cross_lower_values = {
    0x6: [0x7C7F97, 0x07],  # Forest
    0x8: [0x7C7FA6, 0xF9],

    0x30: [0x83A60A, 0x71],  # Villa hallway
    0x27: [0x83A617, 0x26],
    0x2C: [0x83A624, 0x6E],

    0x16C: [0x850FE6, 0x07],  # Villa maze

    0x10A: [0x8C44D3, 0x08],  # CC factory floor
    0x109: [0x8C44E1, 0x08],

    0x74: [0x8DF77C, 0x07],  # CC invention area
    0x60: [0x90FD37, 0x43],
    0x55: [0xBFCC2B, 0x43],
    0x65: [0x90FBA1, 0x51],
    0x64: [0x90FBAD, 0x50],
    0x61: [0x90FE56, 0x43]
}

rom_looping_music_fade_ins = {
    0x10: None,
    0x11: None,
    0x12: None,
    0x13: None,
    0x14: None,
    0x15: None,
    0x16: 0x17,
    0x18: 0x19,
    0x1A: 0x1B,
    0x21: 0x75,
    0x27: None,
    0x2E: 0x23,
    0x39: None,
    0x45: 0x63,
    0x56: None,
    0x57: 0x58,
    0x59: None,
    0x5A: None,
    0x5B: 0x5C,
    0x5D: None,
    0x5E: None,
    0x5F: None,
    0x60: 0x61,
    0x62: None,
    0x64: None,
    0x65: None,
    0x66: None,
    0x68: None,
    0x69: None,
    0x6D: 0x78,
    0x6E: None,
    0x6F: None,
    0x73: None,
    0x74: None,
    0x77: None,
    0x79: None
}

warp_map_offsets = [0xADF67, 0xADF77, 0xADF87, 0xADF97, 0xADFA7, 0xADFBB, 0xADFCB, 0xADFDF]

renon_item_dialogue = {
    0x02: "More Sub-weapon uses!\n"
          "Just what you need!",
    0x03: "Galamoth told me it's\n"
          "a heart in other times.",
    0x04: "Who needs Warp Rooms\n"
          "when you have these?",
    0x05: "I was told to safeguard\n"
          "this, but I dunno why.",
    0x06: "Fresh off a Behemoth!\n"
          "Those cows are weird.",
    0x07: "Preserved with special\n"
          " wall-based methods.",
    0x08: "Don't tell Geneva\n"
          "about this...",
    0x09: "If this existed in 1094,\n"
          "that whip wouldn't...",
    0x0A: "For when some lizard\n"
          "brain spits on your ego.",
    0x0C: "It'd be a shame if you\n"
          "lost it immediately...",
    0x0D: "Arthur was far better\n"
          "with it than you!",
    0x0E: "Night Creatures handle\n"
          "with care!",
    0x0F: "Some may call it a\n"
          "\"Banshee Boomerang.\"",
    0x10: "No weapon triangle\n"
          "advantages with this.",
    0x15: "This non-volatile kind\n"
          "is safe to handle.",
    0x16: "If you can soul-wield,\n"
          "they have a good one!",
    0x17: "Calls the morning sun\n"
          "to vanquish the night.",
    0x18: "1 on-demand horrible\n"
          "night. Devils love it!",
    0x1A: "Want to study here?\n"
          "It will cost you.",
    0x1B: "\"Let them eat cake!\"\n"
          "Said no princess ever.",
    0x1C: "Why do I suspect this\n"
          "was a toilet room?",
    0x1D: "When you see Coller,\n"
          "tell him I said hi!",
    0x1E: "Atomic number is 29\n"
          "and weight is 63.546.",
    0x1F: "One torture per pay!\n"
          "Who will it be?",
    0x20: "Being here feels like\n"
          "time is slowing down.",
    0x21: "Only one thing beind\n"
          "this. Do you dare?",
    0x22: "The key 2 Science!\n"
          "Both halves of it!",
    0x23: "This warehouse can\n"
          "be yours for a fee.",
    0x24: "Long road ahead if you\n"
          "don't have the others.",
    0x25: "Will you get the curse\n"
          "of eternal burning?",
    0x26: "What's beyond time?\n"
          "Find out yourself!",
    0x27: "Want to take out a\n"
          "loan? By all means!",
    0x28: "The bag is green,\n"
          "so it must be lucky!",
    0x29: "(Does this fool realize?)\n"
          "Oh, sorry.",
    "prog":   "They will absolutely\n"
              "need it in time!",
    "useful": "Now, this would be\n"
              "useful to send...",
    "common": "Every last little bit\n"
              "helps, right?",
    "trap":   "I'll teach this fool\n"
              "a lesson for a price!"
}


class LocalRom(object):

    def __init__(self, file):
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values: list):
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_int16(self, address, value: int):
        value = value & 0xFFFF
        self.write_bytes(address, [(value >> 8) & 0xFF, value & 0xFF])

    def write_int16s(self, startaddress, values: list):
        for i, value in enumerate(values):
            self.write_int16(startaddress + (i * 2), value)

    def write_int24(self, address, value: int):
        value = value & 0xFFFFFF
        self.write_bytes(address, [(value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF])

    def write_int24s(self, startaddress, values: list):
        for i, value in enumerate(values):
            self.write_int24(startaddress + (i * 3), value)

    def write_int32(self, address, value: int):
        value = value & 0xFFFFFFFF
        self.write_bytes(address, [(value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF])

    def write_int32s(self, startaddress, values: list):
        for i, value in enumerate(values):
            self.write_int32(startaddress + (i * 4), value)

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())


def patch_rom(multiworld, rom, player, offsets_to_ids, total_available_bosses, active_stage_list, active_stage_exits,
              active_warp_list, required_s2s, music_list, countdown_list, shop_name_list, shop_desc_list,
              shop_price_list, shop_colors_list, slot_name, active_locations):
    w1 = str(multiworld.special1s_per_warp[player]).zfill(2)
    w2 = str(multiworld.special1s_per_warp[player] * 2).zfill(2)
    w3 = str(multiworld.special1s_per_warp[player] * 3).zfill(2)
    w4 = str(multiworld.special1s_per_warp[player] * 4).zfill(2)
    w5 = str(multiworld.special1s_per_warp[player] * 5).zfill(2)
    w6 = str(multiworld.special1s_per_warp[player] * 6).zfill(2)
    w7 = str(multiworld.special1s_per_warp[player] * 7).zfill(2)

    # NOP out the CRC BNEs
    rom.write_int32(0x66C, 0x00000000)
    rom.write_int32(0x678, 0x00000000)

    # Always offer Hard Mode on file creation
    rom.write_int32(0xC8810, 0x240A0100)  # ADDIU	T2, R0, 0x0100

    # Disable Easy Mode cutoff point at Castle Center elevator
    rom.write_int32(0xD9E18, 0x240D0000)  # ADDIU	T5, R0, 0x0000

    # Disable the Forest, Castle Wall, and Villa intro cutscenes and make it possible to change the starting level
    rom.write_byte(0xB73308, 0x00)
    rom.write_byte(0xB7331A, 0x40)
    rom.write_byte(0xB7332B, 0x4C)
    rom.write_byte(0xB6302B, 0x00)
    rom.write_byte(0x109F8F, 0x00)

    # Prevent Forest end cutscene flag from setting so it can be triggered infinitely
    rom.write_byte(0xEEA51, 0x01)

    # Hack to make the Forest, CW and Villa intro cutscenes play at the start of their levels no matter what map came
    # before them
    rom.write_int32(0x97244, 0x803FDD60)
    rom.write_int32s(0xBFDD60, Patches.forest_cw_villa_intro_cs_player)

    # Make changing the map ID to 0xFF reset the map. Helpful to work around a bug wherein the camera gets stuck when
    # entering a loading zone that doesn't change the map.
    rom.write_int32s(0x197B0, [0x0C0FF7E6,   # JAL   0x803FDF98
                               0x24840008])  # ADDIU A0, A0, 0x0008
    rom.write_int32s(0xBFDF98, Patches.map_id_refresher)

    # Enable swapping characters when loading into a map by holding L.
    rom.write_int32(0x97294, 0x803FDFC4)
    rom.write_int32(0x19710, 0x080FF80E)  # J 0x803FE038
    rom.write_int32s(0xBFDFC4, Patches.character_changer)

    # Villa coffin time-of-day hack
    rom.write_byte(0xD9D83, 0x74)
    rom.write_int32(0xD9D84, 0x080FF14D)  # J 0x803FC534
    rom.write_int32s(0xBFC534, Patches.coffin_time_checker)

    # Fix both Castle Center elevator bridges for both characters unless enabling only one character's stages. At which
    # point one bridge will be always broken and one always repaired instead.
    if multiworld.character_stages[player].value == 2:
        rom.write_int32(0x6CEAA0, 0x240B0000)  # ADDIU T3, R0, 0x0000
    elif multiworld.character_stages[player].value == 3:
        rom.write_int32(0x6CEAA0, 0x240B0001)  # ADDIU T3, R0, 0x0001
    else:
        rom.write_int32(0x6CEAA0, 0x240B0001)  # ADDIU T3, R0, 0x0001
        rom.write_int32(0x6CEAA4, 0x240D0001)  # ADDIU T5, R0, 0x0001

    # Were-bull arena flag hack
    rom.write_int32(0x6E38F0, 0x0C0FF157)  # JAL   0x803FC55C
    rom.write_int32s(0xBFC55C, Patches.werebull_flag_unsetter)
    rom.write_int32(0xA949C,  0x0C0FF380)  # JAL   0x803FCE00
    rom.write_int32s(0xBFCE00, Patches.werebull_flag_pickup_setter)

    # Enable being able to carry multiple Special jewels, Nitros, and Mandragoras simultaneously
    rom.write_int32(0xBF1F4, 0x3C038039)  # LUI V1, 0x8039
    # Special1
    rom.write_int32(0xBF210, 0x80659C4B)  # LB A1, 0x9C4B (V1)
    rom.write_int32(0xBF214, 0x24A50001)  # ADDIU A1, A1, 0x0001
    rom.write_int32(0xBF21C, 0xA0659C4B)  # SB A1, 0x9C4B (V1)
    # Special2
    rom.write_int32(0xBF230, 0x80659C4C)  # LB A1, 0x9C4C (V1)
    rom.write_int32(0xBF234, 0x24A50001)  # ADDIU A1, A1, 0x0001
    rom.write_int32(0xbf23C, 0xA0659C4C)  # SB A1, 0x9C4C (V1)
    # Magical Nitro
    rom.write_int32(0xBF360, 0x10000004)  # B 0x8013C184
    rom.write_int32(0xBF378, 0x25E50001)  # ADDIU A1, T7, 0x0001
    rom.write_int32(0xBF37C, 0x10000003)  # B 0x8013C19C
    # Mandragora
    rom.write_int32(0xBF3A8, 0x10000004)  # B 0x8013C1CC
    rom.write_int32(0xBF3C0, 0x25050001)  # ADDIU A1, T0, 0x0001
    rom.write_int32(0xBF3C4, 0x10000003)  # B 0x8013C1E4

    # Give PowerUps their Legacy of Darkness behavior when attempting to pick up more than two
    rom.write_int32(0xA9730, 0x24090000)  # ADDIU	T1, R0, 0x0000
    rom.write_int32(0xBF2FC, 0x080FF16D)  # J	0x803FC5B4
    rom.write_int32(0xBF300, 0x00000000)  # NOP
    rom.write_int32s(0xBFC5B4, Patches.give_powerup_stopper)

    # Rename "Wooden stake" and "Rose" to "Sent major" and "Sent" respectively
    rom.write_bytes(0xEFE34, cv64_string_to_bytes("Sent major  ", False))
    rom.write_bytes(0xEFE4E, cv64_string_to_bytes("Sent", False))
    # Capitalize the "k" in "Archives key" to be consistent with...literally every other key name!
    rom.write_byte(0xEFF21, 0x2D)

    # Skip the "There is a white jewel" text so checking one saves the game instantly.
    rom.write_int32s(0xEFC72, [0x00020002 for i in range(37)])
    rom.write_int32(0xA8FC0, 0x24020001)  # ADDIU V0, R0, 0x0001
    # Skip the yes/no prompts when activating things.
    rom.write_int32s(0xBFDACC, Patches.map_text_redirector)
    rom.write_int32(0xA9084, 0x24020001)  # ADDIU V0, R0, 0x0001
    rom.write_int32(0xBEBE8, 0x0C0FF6B4)  # JAL   0x803FDAD0
    # Skip Vincent and Heinrich's mandatory-for-a-check dialogue
    rom.write_int32(0xBED9C, 0x0C0FF6DA)  # JAL   0x803FDB68
    # Skip the long yes/no prompt in the CC planetarium to set the pieces.
    rom.write_int32(0xB5C5DF, 0x24030001)  # ADDIU  V1, R0, 0x0001
    # Skip the yes/no prompt to activate the CC elevator.
    rom.write_int32(0xB5E3FB, 0x24020001)  # ADDIU  V0, R0, 0x0001
    # Skip the yes/no prompts to set Nitro/Mandragora at both walls.
    rom.write_int32(0xB5DF3E, 0x24030001)  # ADDIU  V1, R0, 0x0001

    # Custom message if you try checking the downstairs CC crack before removing the seal.
    rom.write_bytes(0xBFDBAC, cv64_string_to_bytes("The Furious Nerd Curse\n"
                                                   "prevents you from setting\n"
                                                   "anything until the seal\n"
                                                   "is removed!", True))

    # Change the Special1 and 2 menu descriptions to tell you how many you need to unlock a warp and fight Dracula
    # respectively.
    if multiworld.draculas_condition[player].value == 0:
        total_s2s = 0
    elif multiworld.draculas_condition[player].value == 1:
        total_s2s = 1
    elif multiworld.draculas_condition[player].value == 2:
        total_s2s = total_available_bosses
    else:
        total_s2s = multiworld.total_special2s[player]
    special_text = cv64_string_to_bytes(f"{multiworld.special1s_per_warp[player]} per warp unlock.\n"
                                        f"{multiworld.total_special1s[player]} exist in total.", False) + \
        cv64_string_to_bytes(f"Need {required_s2s} to battle Dracula\n"
                             f"out of {total_s2s} in total.", False)
    rom.write_bytes(0xBFDC5C, special_text)
    rom.write_int32s(0xBFDD20, Patches.special_descriptions_redirector)

    # Change the Stage Select menu options
    rom.write_int32s(0xADF64, Patches.warp_menu_rewrite)
    rom.write_int32s(0x10E0C8, Patches.warp_pointer_table)
    for i in range(len(active_warp_list)):
        if i == 0:
            rom.write_byte(warp_map_offsets[i], stage_info[active_warp_list[i]].start_map_id)
            rom.write_byte(warp_map_offsets[i] + 4, stage_info[active_warp_list[i]].start_spawn_id)
        else:
            rom.write_byte(warp_map_offsets[i], stage_info[active_warp_list[i]].mid_map_id)
            rom.write_byte(warp_map_offsets[i] + 4, stage_info[active_warp_list[i]].mid_spawn_id)

    # Play the "teleportation" sound effect when teleporting
    rom.write_int32s(0xAE088, [0x08004FAB,   # J 0x80013EAC
                               0x2404019E])  # ADDIU A0, R0, 0x019E

    # Change the Stage Select menu's text to reflect its new purpose
    rom.write_bytes(0xEFAD0, cv64_string_to_bytes(f"Where to...?\t{active_warp_list[0]}\t"
                                                  f"`{w1} {active_warp_list[1]}\t"
                                                  f"`{w2} {active_warp_list[2]}\t"
                                                  f"`{w3} {active_warp_list[3]}\t"
                                                  f"`{w4} {active_warp_list[4]}\t"
                                                  f"`{w5} {active_warp_list[5]}\t"
                                                  f"`{w6} {active_warp_list[6]}\t"
                                                  f"`{w7} {active_warp_list[7]}", False))

    # Lizard-man save proofing
    rom.write_int32(0xA99AC, 0x080FF0B8)  # J 0x803FC2E0
    rom.write_int32s(0xBFC2E0, Patches.boss_save_stopper)

    # Disable or guarantee vampire Vincent's fight
    if multiworld.vincent_fight_condition[player] == "never":
        rom.write_int32(0xAACC0, 0x24010001)  # ADDIU AT, R0, 0x0001
        rom.write_int32(0xAACE0, 0x24180000)  # ADDIU T8, R0, 0x0000
    elif multiworld.vincent_fight_condition[player] == "always":
        rom.write_int32(0xAACE0, 0x24180010)  # ADDIU T8, R0, 0x0010
    else:
        rom.write_int32(0xAACE0, 0x24180000)  # ADDIU T8, R0, 0x0000

    # Disable or guarantee Renon's fight
    rom.write_int32(0xAACB4, 0x080FF1A4)  # J 0x803FC690
    if multiworld.renon_fight_condition[player] == "never":
        rom.write_byte(0xB804F0, 0x00)
        rom.write_byte(0xB80632, 0x00)
        rom.write_byte(0xB807E3, 0x00)
        rom.write_byte(0xB80988, 0xB8)
        rom.write_byte(0xB816BD, 0xB8)
        rom.write_byte(0xB817CF, 0x00)
        rom.write_int32s(0xBFC690, Patches.renon_cutscene_checker_jr)
    elif multiworld.renon_fight_condition[player] == "always":
        rom.write_byte(0xB804F0, 0x0C)
        rom.write_byte(0xB80632, 0x0C)
        rom.write_byte(0xB807E3, 0x0C)
        rom.write_byte(0xB80988, 0xC4)
        rom.write_byte(0xB816BD, 0xC4)
        rom.write_byte(0xB817CF, 0x0C)
        rom.write_int32s(0xBFC690, Patches.renon_cutscene_checker_jr)
    else:
        rom.write_int32s(0xBFC690, Patches.renon_cutscene_checker)

    # NOP the Easy Mode check when buying a thing from Renon, so he can be triggered even on this mode.
    rom.write_int32(0xBD8B4, 0x00000000)

    # Disable or guarantee the Bad Ending
    if multiworld.bad_ending_condition[player] == "never":
        rom.write_int32(0xAEE5C6, 0x3C0A0000)  # LUI  T2, 0x0000
    elif multiworld.bad_ending_condition[player] == "always":
        rom.write_int32(0xAEE5C6, 0x3C0A0040)  # LUI  T2, 0x0040

    # Play Castle Keep's song if teleporting in front of Dracula's door outside the escape sequence
    rom.write_int32(0x6E937C, 0x080FF12E)  # J 0x803FC4B8
    rom.write_int32s(0xBFC4B8, Patches.ck_door_music_player)

    # Increase item capacity to 100 if "Increase Item Limit" is turned on
    if multiworld.increase_item_limit[player]:
        rom.write_byte(0xBF30B, 0x64)  # Most items
        rom.write_byte(0xBF3F7, 0x64)  # Sun/Moon cards
    rom.write_byte(0xBF353, 0x64)  # Keys (increase regardless)

    # Change the item healing values if "Nerf Healing" is turned on
    if multiworld.nerf_healing_items[player]:
        rom.write_byte(0xB56371, 0x50)  # Healing kit   (100 -> 80)
        rom.write_byte(0xB56374, 0x32)  # Roast beef    ( 80 -> 50)
        rom.write_byte(0xB56377, 0x19)  # Roast chicken ( 50 -> 25)

    # Disable loading zone healing if turned off
    if not multiworld.loading_zone_heals[player]:
        rom.write_byte(0xD99A5, 0x00)  # Skip all loading zone checks
        rom.write_byte(0xA9DFFB, 0x40)  # Disable free heal from King Skeleton by reading the unused magic meter value

    # Disable spinning on the Special1 and 2 pickup models so colorblind people can more easily identify them
    rom.write_byte(0xEE4F5, 0x00)  # Special1
    rom.write_byte(0xEE505, 0x00)  # Special2
    # Make the Special2 the same size as a Red jewel(L) to further distinguish them
    rom.write_int32(0xEE4FC, 0x3FA66666)

    # Prevent the vanilla Magical Nitro transport's "can explode" flag from setting
    rom.write_int32(0xB5D7AA, 0x00000000)  # NOP

    # Ensure the vampire Nitro check will always pass, so they'll never not spawn and crash the Villa cutscenes
    rom.write_byte(0xA6253D, 0x03)

    # Enable the Game Over's "Continue" menu starting the cursor on whichever checkpoint is most recent
    rom.write_int32(0xB4DDC, 0x0C060D58)  # JAL 0x80183560
    rom.write_int32s(0x106750, Patches.continue_cursor_start_checker)
    rom.write_int32(0x1C444, 0x080FF08A)  # J   0x803FC228
    rom.write_int32(0x1C2A0, 0x080FF08A)  # J   0x803FC228
    rom.write_int32s(0xBFC228, Patches.savepoint_cursor_updater)
    rom.write_int32(0x1C2D0, 0x080FF094)  # J   0x803FC250
    rom.write_int32s(0xBFC250, Patches.stage_start_cursor_updater)
    rom.write_byte(0xB585C8, 0xFF)

    # Make the Special1 and 2 play sounds when you reach milestones with them.
    rom.write_int32s(0xBFDA50, Patches.special_sound_notifs)
    rom.write_int32(0xBF240, 0x080FF694)  # J 0x803FDA50
    rom.write_int32(0xBF220, 0x080FF69E)  # J 0x803FDA78

    # Add data for White Jewel #22 (the new Duel Tower savepoint) at the end of the White Jewel ID data list
    rom.write_int16s(0x104AC8, [0x0000, 0x0006,
                                0x0013, 0x0015])

    # Take the contract in Waterway off of its 00400000 bitflag.
    rom.write_byte(0x87E3DA, 0x00)

    # Spawn coordinates list extension
    rom.write_int32(0xD5BF4, 0x080FF103)  # J	0x803FC40C
    rom.write_int32s(0xBFC40C, Patches.spawn_coordinates_extension)
    rom.write_int32s(0x108A5E, Patches.waterway_end_coordinates)

    # Change the File Select stage numbers to match the new stage order. Also fix a vanilla issue wherein saving in a
    # character-exclusive stage as the other character would incorrectly display the name of that character's equivalent
    # stage on the save file instead of the one they're actually in.
    rom.write_byte(0xC9FE3, 0xD4)
    rom.write_byte(0xCA055, 0x08)
    rom.write_byte(0xCA066, 0x40)
    rom.write_int32(0xCA068, 0x860C17D0)  # LH T4, 0x17D0 (S0)
    rom.write_byte(0xCA06D, 0x08)
    rom.write_byte(0x104A31, 0x01)
    rom.write_byte(0x104A39, 0x01)
    rom.write_byte(0x104A89, 0x01)
    rom.write_byte(0x104A91, 0x01)
    rom.write_byte(0x104A99, 0x01)
    rom.write_byte(0x104AA1, 0x01)

    for stage in active_stage_list:
        for offset in stage_info[stage].stage_number_offset_list:
            rom.write_byte(offset, active_stage_exits[stage]["position"])

    # CC top elevator switch check
    rom.write_int32(0x6CF0A0, 0x0C0FF0B0)  # JAL 0x803FC2C0
    rom.write_int32s(0xBFC2C0, Patches.elevator_flag_checker)

    # Disable time restrictions
    if multiworld.disable_time_restrictions[player]:
        # Fountain
        rom.write_int32(0x6C2340, 0x00000000)  # NOP
        rom.write_int32(0x6C257C, 0x10000023)  # B [forward 0x23]
        # Rosa
        rom.write_byte(0xEEAAB, 0x00)
        rom.write_byte(0xEEAAD, 0x18)
        # Moon doors
        rom.write_int32(0xDC3E0, 0x00000000)  # NOP
        rom.write_int32(0xDC3E8, 0x00000000)  # NOP
        # Sun doors
        rom.write_int32(0xDC410, 0x00000000)  # NOP
        rom.write_int32(0xDC418, 0x00000000)  # NOP

    # Custom data-loading code
    rom.write_int32(0x6B5028, 0x08060D70)  # J 0x801835D0
    rom.write_int32s(0x1067B0, Patches.custom_code_loader)

    # Custom remote item rewarding and DeathLink receiving code
    rom.write_int32(0x19B98, 0x080FF000)  # J 0x803FC000
    rom.write_int32s(0xBFC000, Patches.remote_item_giver)
    rom.write_int32s(0xBFE190, Patches.subweapon_surface_checker)

    # Make received DeathLinks blow you to smithereens instead of kill you normally.
    if multiworld.death_link[player].value == 2:
        rom.write_int32(0x27A70, 0x10000008)  # B [forward 0x08]
        rom.write_int32s(0xBFC0D0, Patches.deathlink_nitro_edition)

    # DeathLink counter decrementer code
    rom.write_int32(0x1C340, 0x080FF8F0)  # J 0x803FE3C0
    rom.write_int32s(0xBFE3C0, Patches.deathlink_counter_decrementer)
    rom.write_int32(0x25B6C, 0x0080FF052)  # J 0x803FC148
    rom.write_int32s(0xBFC148, Patches.nitro_fall_killer)

    # Death flag un-setter on "Beginning of stage" state overwrite code
    rom.write_int32(0x1C2B0, 0x080FF047)  # J 0x803FC11C
    rom.write_int32s(0xBFC11C, Patches.death_flag_unsetter)

    # Warp menu-opening code
    rom.write_int32(0xB9BA8, 0x080FF099)  # J	0x803FC264
    rom.write_int32s(0xBFC264, Patches.warp_menu_opener)

    # NPC item textbox hack
    rom.write_int32(0xBF1DC, 0x080FF067)  # J 0x803FC19C
    rom.write_int32(0xBF1E0, 0x27BDFFE0)  # ADDIU SP, SP, -0x20
    rom.write_int32s(0xBFC19C, Patches.npc_item_hack)

    # Sub-weapon check function hook
    rom.write_int32(0xBF32C, 0x00000000)  # NOP
    rom.write_int32(0xBF330, 0x080FF05D)  # J	0x803FC174
    rom.write_int32s(0xBFC174, Patches.give_subweapon_stopper)

    # Warp menu Special1 restriction
    rom.write_int32(0xADD68, 0x0C04AB12)  # JAL 0x8012AC48
    rom.write_int32s(0xADE28, Patches.stage_select_overwrite)
    rom.write_byte(0xADE47, multiworld.special1s_per_warp[player])

    # Dracula's door text pointer hijack
    rom.write_int32(0xD69F0, 0x080FF141)  # J 0x803FC504
    rom.write_int32s(0xBFC504, Patches.dracula_door_text_redirector)

    # Dracula's chamber condition
    rom.write_int32(0xE2FDC, 0x0804AB25)  # J 0x8012AC78
    rom.write_int32s(0xADE84, Patches.special_goal_checker)
    rom.write_bytes(0xBFCC48, [0xA0, 0x00, 0xFF, 0xFF, 0xA0, 0x01, 0xFF, 0xFF, 0xA0, 0x02, 0xFF, 0xFF, 0xA0, 0x03, 0xFF,
                               0xFF, 0xA0, 0x04, 0xFF, 0xFF, 0xA0, 0x05, 0xFF, 0xFF, 0xA0, 0x06, 0xFF, 0xFF, 0xA0, 0x07,
                               0xFF, 0xFF, 0xA0, 0x08, 0xFF, 0xFF, 0xA0, 0x09])
    if multiworld.draculas_condition[player] == 1:
        rom.write_int32(0x6C8A54, 0x0C0FF0C1)  # JAL 0x803FC304
        rom.write_int32s(0xBFC304, Patches.crystal_special2_giver)
        rom.write_byte(0xADE8F, 0x01)
        rom.write_bytes(0xBFCC6E, cv64_string_to_bytes(f"It won't budge!\n"
                                                       f"You'll need the power\n"
                                                       f"of the basement crystal\n"
                                                       f"to undo the seal.", True))
    elif multiworld.draculas_condition[player] == 2:
        rom.write_int32(0xBBD50, 0x080FF18C)  # J	0x803FC630
        rom.write_int32s(0xBFC630, Patches.boss_special2_giver)
        rom.write_int32s(0xBFC55C, Patches.werebull_flag_unsetter_special2_electric_boogaloo)
        rom.write_byte(0xADE8F, multiworld.bosses_required[player].value)
        rom.write_bytes(0xBFCC6E, cv64_string_to_bytes(f"It won't budge!\n"
                                                       f"You'll need to defeat\n"
                                                       f"{required_s2s} powerful monsters\n"
                                                       f"to undo the seal.", True))
    elif multiworld.draculas_condition[player] == 3:
        rom.write_byte(0xADE8F, multiworld.special2s_required[player].value)
        rom.write_bytes(0xBFCC6E, cv64_string_to_bytes(f"It won't budge!\n"
                                                       f"You'll need to find\n"
                                                       f"{required_s2s} Special2 jewels\n"
                                                       f"to undo the seal.", True))
    else:
        rom.write_byte(0xADE8F, 0x00)

    # On-the-fly TLB script modifier
    rom.write_int32s(0xBFC338, Patches.double_component_checker)
    rom.write_int32s(0xBFC3D4, Patches.downstairs_seal_checker)
    rom.write_int32s(0xBFE074, Patches.mandragora_with_nitro_setter)
    rom.write_int32s(0xBFC700, Patches.overlay_modifiers)

    # On-the-fly actor data modifier hook
    rom.write_int32(0xEAB04, 0x080FF220)  # J 0x803FC880
    rom.write_int32s(0xBFC878, Patches.map_data_modifiers)

    # Fix to make flags apply to freestanding invisible items properly
    rom.write_int32(0xA84F8, 0x90CC0039)  # LBU T4, 0x0039 (A2)

    # Fix locked doors to check the key counters instead of their vanilla key locations' bitflags
    # Pickup flag check modifications:
    rom.write_int32(0x10B2D8, 0x00000002)  # Left Tower Door
    rom.write_int32(0x10B2F0, 0x00000003)  # Storeroom Door
    rom.write_int32(0x10B2FC, 0x00000001)  # Archives Door
    rom.write_int32(0x10B314, 0x00000004)  # Maze Gate
    rom.write_int32(0x10B350, 0x00000005)  # Copper Door
    rom.write_int32(0x10B3A4, 0x00000006)  # Torture Chamber Door
    rom.write_int32(0x10B3B0, 0x00000007)  # ToE Gate
    rom.write_int32(0x10B3BC, 0x00000008)  # Science Door1
    rom.write_int32(0x10B3C8, 0x00000009)  # Science Door2
    rom.write_int32(0x10B3D4, 0x0000000A)  # Science Door3
    rom.write_int32(0x6F0094, 0x0000000B)  # CT Door 1
    rom.write_int32(0x6F00A4, 0x0000000C)  # CT Door 2
    rom.write_int32(0x6F00B4, 0x0000000D)  # CT Door 3
    # Item counter decrement check modifications:
    rom.write_int32(0xEDA84, 0x00000001)   # Archives Door
    rom.write_int32(0xEDA8C, 0x00000002)   # Left Tower Door
    rom.write_int32(0xEDA94, 0x00000003)   # Storeroom Door
    rom.write_int32(0xEDA9C, 0x00000004)   # Maze Gate
    rom.write_int32(0xEDAA4, 0x00000005)   # Copper Door
    rom.write_int32(0xEDAAC, 0x00000006)   # Torture Chamber Door
    rom.write_int32(0xEDAB4, 0x00000007)   # ToE Gate
    rom.write_int32(0xEDABC, 0x00000008)   # Science Door1
    rom.write_int32(0xEDAC4, 0x00000009)   # Science Door2
    rom.write_int32(0xEDACC, 0x0000000A)   # Science Door3
    rom.write_int32(0xEDAD4, 0x0000000B)   # CT Door 1
    rom.write_int32(0xEDADC, 0x0000000C)   # CT Door 2
    rom.write_int32(0xEDAE4, 0x0000000D)   # CT Door 3

    rom.write_int32(0x10AB2C, 0x8015FBD4)  # Maze Gates' check code pointer adjustments
    rom.write_int32(0x10AB40, 0x8015FBD4)
    rom.write_int32s(0x10AB50, [0x0D0C0000,
                                0x8015FBD4])
    rom.write_int32s(0x10AB64, [0x0D0C0000,
                                0x8015FBD4])
    rom.write_int32s(0xE2E14, Patches.normal_door_hook)
    rom.write_int32s(0xBFC5D0, Patches.normal_door_code)
    rom.write_int32s(0x6EF298, Patches.ct_door_hook)
    rom.write_int32s(0xBFC608, Patches.ct_door_code)
    # Fix key counter not decrementing if 2 or above
    rom.write_int32(0xAA0E0, 0x24020000)  # ADDIU	V0, R0, 0x0000

    # Make the Easy-only candle drops in Room of Clocks appear on any difficulty
    rom.write_byte(0x9B518F, 0x01)

    # Slightly move some once-invisible freestanding items to be more visible
    if multiworld.invisible_items[player].value == 1:
        rom.write_byte(0x7C7F95, 0xEF)  # Forest dirge maiden statue
        rom.write_byte(0x7C7FA8, 0xAB)  # Forest werewolf statue
        rom.write_byte(0x8099C4, 0x8C)  # Villa courtyard tombstone
        rom.write_byte(0x83A626, 0xC2)  # Villa living room painting
        # rom.write_byte(0x83A62F, 0x64)  # Villa Mary's room table
        rom.write_byte(0xBFCB97, 0xF5)  # CC torture instrument rack
        rom.write_byte(0x8C44D5, 0x22)  # CC red carpet hallway knight
        rom.write_byte(0x8DF57C, 0xF1)  # CC cracked wall hallway flamethrower
        rom.write_byte(0x90FCD6, 0xA5)  # CC nitro hallway flamethrower
        rom.write_byte(0x90FB9F, 0x9A)  # CC invention room round machine
        rom.write_byte(0x90FBAF, 0x03)  # CC invention room giant famicart
        rom.write_byte(0x90FE54, 0x97)  # CC staircase knight (x)
        rom.write_byte(0x90FE58, 0xFB)  # CC staircase knight (z)

    # Change bitflag on item in upper coffin in Forest final switch gate tomb to one that's not used by something else
    rom.write_int32(0x10C77C, 0x00000002)

    # Make the torch directly behind Dracula's chamber that normally doesn't set a flag set bitflag 0x08 in 0x80389BFA
    rom.write_byte(0x10CE9F, 0x01)

    # Change the CC post-Behemoth boss depending on the option for Post-Behemoth Boss
    if multiworld.post_behemoth_boss[player].value == 1:
        rom.write_byte(0xEEDAD, 0x02)
        rom.write_byte(0xEEDD9, 0x01)
    elif multiworld.post_behemoth_boss[player].value == 2:
        rom.write_byte(0xEEDAD, 0x00)
        rom.write_byte(0xEEDD9, 0x03)
        # Put both on the same flag so changing character won't trigger a rematch with the same boss.
        rom.write_byte(0xEED8B, 0x40)
    elif multiworld.post_behemoth_boss[player].value == 3:
        rom.write_byte(0xEEDAD, 0x03)
        rom.write_byte(0xEEDD9, 0x00)
        rom.write_byte(0xEED8B, 0x40)

    # Change the RoC boss depending on the option for Room of Clocks Boss
    if multiworld.room_of_clocks_boss[player].value == 1:
        rom.write_byte(0x109FB3, 0x56)
        rom.write_byte(0x109FBF, 0x44)
        rom.write_byte(0xD9D44, 0x14)
        rom.write_byte(0xD9D4C, 0x14)
    elif multiworld.room_of_clocks_boss[player].value == 2:
        rom.write_byte(0x109FBF, 0x44)
        rom.write_byte(0xD9D45, 0x00)
        # Put both on the same flag so changing character won't trigger a rematch with the same boss.
        rom.write_byte(0x109FB7, 0x90)
        rom.write_byte(0x109FC3, 0x90)
    elif multiworld.room_of_clocks_boss[player].value == 3:
        rom.write_byte(0x109FB3, 0x56)
        rom.write_int32(0xD9D44, 0x00000000)
        rom.write_byte(0xD9D4D, 0x00)
        rom.write_byte(0x109FB7, 0x90)
        rom.write_byte(0x109FC3, 0x90)

    # Tunnel gondola skip
    if multiworld.skip_gondolas[player]:
        rom.write_int32(0x6C5F58, 0x080FF7D0)  # J 0x803FDF40
        rom.write_int32s(0xBFDF40, Patches.gondola_skipper)
        # New gondola transfer point candle coordinates
        rom.write_byte(0xBFC9A3, 0x04)
        rom.write_bytes(0x86D824, [0x27, 0x01, 0x10, 0xF7, 0xA0])

    # Waterway brick platforms skip
    if multiworld.skip_brick_platforms[player]:
        rom.write_int32(0x6C7E2C, 0x00000000)  # NOP

    # Ambience silencing fix
    rom.write_int32(0xD9270, 0x080FF840)  # J 0x803FE100
    rom.write_int32s(0xBFE100, Patches.ambience_silencer)
    # Fix for the door sliding sound playing infinitely if leaving the fan meeting room before the door closes entirely.
    # Hooking this in the ambience silencer code does nothing for some reason.
    rom.write_int32s(0xAE10C, [0x08004FAB,   # J   0x80013EAC
                               0x3404829B])  # ORI A0, R0, 0x829B
    rom.write_int32s(0xD9E8C, [0x08004FAB,   # J   0x80013EAC
                               0x3404829B])  # ORI A0, R0, 0x829B
    # Fan meeting room ambience fix
    rom.write_int32(0x109964, 0x803FE13C)

    # Make the Villa coffin cutscene skippable
    rom.write_int32(0xAA530, 0x080FF880)  # J 0x803FE200
    rom.write_int32s(0xBFE200, Patches.coffin_cutscene_skipper)

    # Increase shimmy speed
    if multiworld.increase_shimmy_speed[player]:
        rom.write_byte(0xA4241, 0x5A)

    # Disable landing fall damage
    if multiworld.fall_guard[player]:
        rom.write_byte(0x27B23, 0x00)

    # Enable the unused film reel effect on all cutscenes
    if multiworld.cinematic_experience[player]:
        rom.write_int32(0xAA33C, 0x240A0001)  # ADDIU T2, R0, 0x0001
        rom.write_byte(0xAA34B, 0x0C)
        rom.write_int32(0xAA4C4, 0x24090001)  # ADDIU T1, R0, 0x0001

    # Permanent PowerUp stuff
    if multiworld.permanent_powerups[player]:
        # Make receiving PowerUps increase the unused menu PowerUp counter instead of the one outside the save struct
        rom.write_int32(0xBF2EE, 0x806B619B)   # LB	T3, 0x619B (V1)
        rom.write_int32(0xBFC5BE, 0xA06C619B)  # SB	T4, 0x619B (V1)
        # Make Reinhardt's whip check the menu PowerUp counter
        rom.write_int32(0x69FA08, 0x80CC619B)  # LB	T4, 0x619B (A2)
        rom.write_int32(0x69FBFC, 0x80C3619B)  # LB	V1, 0x619B (A2)
        rom.write_int32(0x69FFE0, 0x818C9C53)  # LB	T4, 0x9C53 (T4)
        # Make Carrie's orb check the menu PowerUp counter
        rom.write_int32(0x6AC86C, 0x8105619B)  # LB	A1, 0x619B (T0)
        rom.write_int32(0x6AC950, 0x8105619B)  # LB	A1, 0x619B (T0)
        rom.write_int32(0x6AC99C, 0x810E619B)  # LB	T6, 0x619B (T0)
        rom.write_int32(0x5AFA0, 0x80639C53)   # LB	V1, 0x9C53 (V1)
        rom.write_int32(0x5B0A0, 0x81089C53)   # LB	T0, 0x9C53 (T0)
        rom.write_byte(0x391C7, 0x00)  # Prevent PowerUps from dropping from enemies
        rom.write_byte(0xAEC451, 0x2E)  # Make Fake Dracula's fireballs drop l jewels instead of PowerUps
        rom.write_byte(0xAAC531, 0x2E)  # Make Real Dracula's fireballs drop l jewels instead of PowerUps

    # Write the randomized (or disabled) music ID list and its associated code
    if multiworld.background_music[player] != 0:
        rom.write_int32(0x14588, 0x08060D60)  # J 0x80183580
        rom.write_int32(0x14590, 0x00000000)  # NOP
        rom.write_int32s(0x106770, Patches.music_modifier)
        rom.write_bytes(0xBFCD30, music_list)
        rom.write_int32(0x15780, 0x0C0FF36E)  # JAL 0x803FCDB8
        rom.write_int32s(0xBFCDB8, Patches.music_comparer_modifier)

    # Enable storing item flags anywhere and changing the item model/visibility on any item instance.
    rom.write_int32s(0xA857C, [0x080FF38F,   # J	    0x803FCE3C
                               0x94D90038])  # LHU   T9, 0x0038 (A2)
    rom.write_int32s(0xBFCE3C, Patches.item_customizer)
    rom.write_int32s(0xA86A0, [0x0C0FF3AF,   # JAL   0x803FCEBC
                               0x95C40002])  # LHU   A0, 0x0002 (T6)
    rom.write_int32s(0xBFCEBC, Patches.item_appearance_switcher)
    rom.write_int32s(0xA8728, [0x0C0FF3B8,   # JAL   0x803FCEE4
                               0x01396021])  # ADDU  T4, T1, T9
    rom.write_int32s(0xBFCEE4, Patches.item_model_visibility_switcher)
    rom.write_int32s(0xA8A04, [0x0C0FF3C2,   # JAL   0x803FCF08
                               0x018B6021])  # ADDU  T4, T4, T3
    rom.write_int32s(0xBFCF08, Patches.item_shine_visibility_switcher)

    # If playing with universal sub-weapons or included empty breakables, write these values to have them store flags
    # and, in the case of the RoC candles, change them to two unused candle settings.
    if multiworld.empty_breakables[player]:
        offsets_to_ids.update({**rom_empty_breakables_flags})
    if multiworld.sub_weapon_shuffle[player].value > 1:
        offsets_to_ids.update({**rom_sub_weapon_flags})

    # Disable the 3HBs checking and setting flags when breaking them and enable their individual items checking and
    # setting flags instead.
    if multiworld.multi_hit_breakables[player]:
        rom.write_int32(0xE87F8, 0x00000000)  # NOP
        rom.write_int16(0xE836C, 0x1000)
        rom.write_int32(0xE8B40, 0x0C0FF3CD)  # JAL 0x803FCF34
        rom.write_int32s(0xBFCF34, Patches.three_hit_item_flags_setter)
        # Villa foyer chandelier-specific functions (yeah, IDK why KCEK made different functions for this one)
        rom.write_int32(0xE7D54, 0x00000000)  # NOP
        rom.write_int16(0xE7908, 0x1000)
        rom.write_byte(0xE7A5C, 0x10)
        rom.write_int32(0xE7F08, 0x0C0FF3DF)  # JAL 0x803FCF7C
        rom.write_int32s(0xBFCF7C, Patches.chandelier_item_flags_setter)

        # New flag values to put in each 3HB vanilla flag's spot
        rom.write_int32(0x10C7C8, 0x8000FF48)  # FoS dirge maiden rock
        rom.write_int32(0x10C7B0, 0x0200FF48)  # FoS S1 bridge rock
        rom.write_int32(0x10C86C, 0x0010FF48)  # CW upper rampart save nub
        rom.write_int32(0x10C878, 0x4000FF49)  # CW Dracula switch slab
        rom.write_int32(0x10CAD8, 0x0100FF49)  # Tunnel twin arrows slab
        rom.write_int32(0x10CAE4, 0x0004FF49)  # Tunnel lonesome bucket pit rock
        rom.write_int32(0x10CB54, 0x4000FF4A)  # UW poison parkour ledge
        rom.write_int32(0x10CB60, 0x0080FF4A)  # UW skeleton crusher ledge
        rom.write_int32(0x10CBF0, 0x0008FF4A)  # CC Behemoth crate
        rom.write_int32(0x10CC2C, 0x2000FF4B)  # CC elevator pedestal
        rom.write_int32(0x10CC70, 0x0200FF4B)  # CC lizard locker slab
        rom.write_int32(0x10CD88, 0x0010FF4B)  # ToE pre-midsavepoint platforms ledge
        rom.write_int32(0x10CE6C, 0x4000FF4C)  # ToSci invisible bridge crate
        rom.write_int32(0x10CF20, 0x0080FF4C)  # CT inverted battery slab
        rom.write_int32(0x10CF2C, 0x0008FF4C)  # CT inverted door slab
        rom.write_int32(0x10CF38, 0x8000FF4D)  # CT final room door slab
        rom.write_int32(0x10CF44, 0x1000FF4D)  # CT Renon slab
        rom.write_int32(0x10C908, 0x0008FF4D)  # Villa foyer chandelier
        rom.write_byte(0x10CF37, 0x04)  # pointer for CT final room door slab item data

    # Remove the flags from the Carrie-only and lizard locker checks if they are not in. This means they can be farmed
    # infinitely, but now they won't decrease the Countdown.
    if not multiworld.carrie_logic[player].value:
        rom.write_byte(0x10CB0D, 0x00)
        rom.write_byte(0x10CB15, 0x00)

    if not multiworld.lizard_locker_items[player].value:
        rom.write_int16(0xBFC9D2, 0x0000)
        rom.write_int16(0xBFC9D6, 0x0000)
        rom.write_int16(0xBFC9DA, 0x0000)
        rom.write_int16(0xBFC9DE, 0x0000)
        rom.write_int16(0xBFC9E2, 0x0000)
        rom.write_int16(0xBFC9E6, 0x0000)

    # Take the Clock Toewr bone pillar chasm sub-weapon off its flag if sub-weapons aren't reandomized anywhere.
    if multiworld.sub_weapon_shuffle[player].value != 2:
        rom.write_byte(0x99BC5B, 0x00)

    # Once-per-frame gameplay checks
    rom.write_int32(0x6C848, 0x080FF40D)   # J 0x803FD034
    rom.write_int32(0xBFD058, 0x0801AEB5)  # J 0x8006BAD4

    # Everything related to dropping the previous sub-weapon
    if multiworld.drop_previous_sub_weapon[player]:
        rom.write_int32(0xBFD034, 0x080FF3FF)  # J 0x803FCFFC
        rom.write_int32(0xBFC18C, 0x080FF3F2)  # J 0x803FCFC8
        rom.write_int32s(0xBFCFC4, Patches.prev_subweapon_spawn_checker)
        rom.write_int32s(0xBFCFFC, Patches.prev_subweapon_fall_checker)
        rom.write_int32s(0xBFD060, Patches.prev_subweapon_dropper)

    # Everything related to the Countdown counter
    if multiworld.countdown[player]:
        rom.write_int32(0xBFD03C, 0x080FF5BF)    # J 0x803FD6FC
        rom.write_int32(0xD5D48, 0x080FF4EC)     # J 0x803FD3B0
        rom.write_int32s(0xBFD3B0, Patches.countdown_number_displayer)
        rom.write_int32s(0xBFD6DC, Patches.countdown_number_updater)
        rom.write_int32(0xBFCE2C, 0x080FF5D2)    # J 0x803FD748
        rom.write_int32s(0xBB168, [0x080FF5F0,   # J 0x803FD7C0
                                   0x8E020028])  # LW	V0, 0x0028 (S0)
        rom.write_int32s(0xBB1D0, [0x080FF5F7,   # J 0x803FD7DC
                                   0x8E020028])  # LW	V0, 0x0028 (S0)
        rom.write_int32(0xBC4A0, 0x080FF5E2)     # J 0x803FD788
        rom.write_int32(0xBC4C4, 0x080FF5E2)     # J 0x803FD788
        rom.write_int32(0x19844, 0x080FF5FE)     # J 0x803FD7F8
        # If the option is set to "all locations", count it down no matter what the item is.
        if multiworld.countdown[player].value == 2:
            rom.write_int32s(0xBFD71C, [0x01010101, 0x01010101, 0x01010101, 0x01010101, 0x01010101, 0x01010101,
                             0x01010101, 0x01010101, 0x01010101, 0x01010101, 0x01010101])
        rom.write_bytes(0xBFD818, countdown_list)

    # Initial Countdown numbers
    rom.write_int32(0xAD6A8, 0x080FF60A)  # J	0x803FD828
    rom.write_int32s(0xBFD828, Patches.new_game_extras)

    # Everything related to shopsanity
    if multiworld.shopsanity[player]:
        rom.write_bytes(0x103868, cv64_string_to_bytes("Not obtained. ", False))
        rom.write_int32s(0xBFD8D0, Patches.shopsanity_stuff)
        rom.write_int32(0xBD828, 0x0C0FF643)     # JAL	0x803FD90C
        rom.write_int32(0xBD5B8, 0x0C0FF651)     # JAL	0x803FD944
        rom.write_int32(0xB0610, 0x0C0FF665)     # JAL	0x803FD994
        rom.write_int32s(0xBD24C, [0x0C0FF677,   # J  	0x803FD9DC
                                   0x00000000])  # NOP
        rom.write_int32(0xBD618, 0x0C0FF684)     # JAL	0x803FDA10

        shopsanity_name_text = []
        shopsanity_desc_text = []
        for i in range(len(shop_name_list)):
            shopsanity_name_text += [0xA0, i] + shop_colors_list[i] + cv64_string_to_bytes(cv64_text_truncate(
                shop_name_list[i], 80), False)

            shopsanity_desc_text += [0xA0, i]
            if shop_desc_list[i][1] is not None:
                shopsanity_desc_text += cv64_string_to_bytes("For " + shop_desc_list[i][1] + ".\n", False, False)
            shopsanity_desc_text += cv64_string_to_bytes(renon_item_dialogue[shop_desc_list[i][0]], False)
        rom.write_bytes(0x1AD00, shopsanity_name_text)
        rom.write_bytes(0x1A800, shopsanity_desc_text)

        if multiworld.shop_prices[player]:
            for i in range(len(shop_price_list)):
                price_offset = 0x103D6E + (i*12)
                rom.write_int16(price_offset, shop_price_list[i])

    # Panther Dash running
    if multiworld.panther_dash[player]:
        rom.write_int32(0x69C8C4, 0x0C0FF77E)     # JAL   0x803FDDF8
        rom.write_int32(0x6AA228, 0x0C0FF77E)     # JAL   0x803FDDF8
        rom.write_int32s(0x69C86C, [0x0C0FF78E,   # JAL   0x803FDE38
                                    0x3C01803E])  # LUI   AT, 0x803E
        rom.write_int32s(0x6AA1D0, [0x0C0FF78E,   # JAL   0x803FDE38
                                    0x3C01803E])  # LUI   AT, 0x803E
        rom.write_int32(0x69D37C, 0x0C0FF79E)     # JAL   0x803FDE78
        rom.write_int32(0x6AACE0, 0x0C0FF79E)     # JAL   0x803FDE78
        rom.write_int32s(0xBFDDF8, Patches.panther_dash)
        # Jump prevention
        if multiworld.panther_dash[player].value == 2:
            rom.write_int32(0xBFDE2C, 0x080FF7BB)     # J     0x803FDEEC
            rom.write_int32(0xBFD044, 0x080FF7B1)     # J     0x803FDEC4
            rom.write_int32s(0x69B630, [0x0C0FF7C6,   # JAL   0x803FDF18
                                        0x8CCD0000])  # LW    T5, 0x0000 (A2)
            rom.write_int32s(0x6A8EC0, [0x0C0FF7C6,   # JAL   0x803FDF18
                                        0x8CCC0000])  # LW    T4, 0x0000 (A2)
            # Fun fact: KCEK put separate code to handle coyote time jumping
            rom.write_int32s(0x69910C, [0x0C0FF7C6,   # JAL   0x803FDF18
                                        0x8C4E0000])  # LW    T6, 0x0000 (V0)
            rom.write_int32s(0x6A6718, [0x0C0FF7C6,   # JAL   0x803FDF18
                                        0x8C4E0000])  # LW    T6, 0x0000 (V0)
            rom.write_int32s(0xBFDEC4, Patches.panther_jump_preventer)

    # Write all the new item and loading zone bytes
    for offset, item_id in offsets_to_ids.items():
        if item_id <= 0xFF:
            rom.write_byte(offset, item_id)
        elif item_id <= 0xFFFF:
            rom.write_int16(offset, item_id)
        elif item_id <= 0xFFFFFF:
            rom.write_int24(offset, item_id)
        else:
            rom.write_int32(offset, item_id)

    # Insert the file containing the Archipelago item icons.
    with open("./worlds/cv64/ap_icons.bin", "rb") as stream:
        rom.write_bytes(0xBB2D88, list(stream.read()))
    # Update the items' Nisitenma-Ichigo table entry to point to the new file's start and end addresses in the ROM.
    rom.write_int32s(0x95F04, [0x80BB2D88, 0x00BB6EEC])
    # Update the items' decompressed file size tables with the new file's decompressed file size.
    rom.write_int16(0x95706, 0x7BF0)
    rom.write_int16(0x104CCE, 0x7BF0)
    # Update the Wooden Stake and Roses' item appearance settings table to point to the Archipelago item graphics.
    rom.write_int16(0xEE5BA, 0x7B38)
    rom.write_int16(0xEE5CA, 0x7280)
    # Change the items' sizes. The progression one will be larger than the non-progression one.
    rom.write_int32(0xEE5BC, 0x3FF00000)
    rom.write_int32(0xEE5CC, 0x3FA00000)

    # Write the slot name
    rom.write_bytes(0xBFBFE0, slot_name)

    # Write the item/player names for other game items
    for loc in active_locations:
        if loc.address is not None and loc.cv64_loc_type != "shop" and loc.item.player != player:
            if len(loc.item.name) > 67:
                item_name = loc.item.name[0x00:0x68]
            else:
                item_name = loc.item.name
            inject_address = 0xBB7164 + (256 * (loc.address - base_id))
            wrapped_name, num_lines = cv64_text_wrap(item_name + "\nfor " + multiworld.get_player_name(
                loc.item.player), 96)
            rom.write_bytes(inject_address, get_item_text_color(loc) + cv64_string_to_bytes(wrapped_name, False))
            rom.write_byte(inject_address + 255, num_lines)

    # Everything relating to loading the other game items text
    rom.write_int32(0xA8D8C, 0x080FF88F)  # J   0x803FE23C
    rom.write_int32(0xBEA98, 0x0C0FF8B4)  # JAL 0x803FE2D0
    rom.write_int32(0xBEAB0, 0x0C0FF8BD)  # JAL 0x803FE2F8
    rom.write_int32(0xBEACC, 0x0C0FF8C5)  # JAL 0x803FE314
    rom.write_int32s(0xBFE23C, Patches.multiworld_item_name_loader)
    rom.write_bytes(0x10F188, [0x00 for i in range(264)])
    rom.write_bytes(0x10F298, [0x00 for i in range(264)])


class CV64DeltaPatch(APDeltaPatch):
    hash = USHASH
    patch_file_ending: str = ".apcv64"
    result_file_ending: str = ".z64"

    game = "Castlevania 64"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

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
        # file_name = options["cv64_options"]["rom_file"]
        file_name = "Castlevania (USA).z64"
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


def get_item_text_color(loc, trap_color: bool = True) -> list:
    if loc.item.advancement:
        return [0xA2, 0x0C]
    elif loc.item.classification == ItemClassification.useful:
        return [0xA2, 0x0A]
    elif loc.item.classification == ItemClassification.trap and trap_color:
        return [0xA2, 0x0B]
    else:
        return [0xA2, 0x02]
