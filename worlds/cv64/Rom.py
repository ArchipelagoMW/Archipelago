import Utils
from Utils import read_snes_rom
from worlds.Files import APDeltaPatch

import hashlib
import os

from .Names import Patches, RegionName
from .Stages import stage_dict

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
    0xBFC983: 0x10,
    0x10C987: 0x10,
    0x10C98F: 0x0D,
    0x10C997: 0x0F,

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

    0x99BC5A: 0x0D,  # Clock Tower
    0x10CECB: 0x10,
    0x10CED3: 0x0F,
    0x10CEDB: 0x0E,
    0x10CEE3: 0x0D,
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


def patch_rom(world, rom, player, offsets_to_ids, active_stage_list, active_warp_list, sub_weapon_dict, required_s2s):
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
    rom.write_bytes(0xBFC534, Patches.coffin_time_checker)

    # Fix both Castle Center elevator bridges for both characters
    rom.write_bytes(0x6CEAA0, [0x24, 0x0B, 0x00, 0x01])
    rom.write_bytes(0x6CEAA4, [0x24, 0x0D, 0x00, 0x01])

    # Were-bull arena flag hack
    rom.write_bytes(0x6E38F0, [0x0C, 0x0F, 0xF1, 0x57])
    rom.write_bytes(0xBFC55C, Patches.werebull_flag_unsetter)

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
    rom.write_bytes(0xBFC5B4, Patches.give_powerup_stopper)

    # Rename "Wooden stake" and "Rose" to "Sent major" and "Sent" respectively
    rom.write_bytes(0xEFE34, cv64_text_converter("Sent major  ", False))
    rom.write_bytes(0xEFE4E, cv64_text_converter("Sent", False))

    # Change the Stage Select menu options
    rom.write_bytes(0xADF64, Patches.warp_menu_rewrite)
    rom.write_bytes(0x10E0C8, Patches.warp_pointer_table)
    rom.write_byte(0xADF67, stage_dict[active_stage_list[0]].start_map_id)
    for warp in range(len(active_warp_list)):
        rom.write_byte(warp_scene_offsets[warp], stage_dict[active_warp_list[warp]].mid_map_id)
        rom.write_byte(warp_scene_offsets[warp] + 4, stage_dict[active_warp_list[warp]].mid_spawn_id)

    # Play the "teleportation" sound effect when teleporting
    rom.write_bytes(0xAE088, [0x08, 0x00, 0x4F, 0xAB,   # J 0x80013EAC
                              0x24, 0x04, 0x01, 0x9E])  # ADDIU A0, R0, 0x019E

    # Change the Stage Select menu's text to reflect its new purpose
    rom.write_bytes(0xEFAD0, cv64_text_converter(f"Where to...?\t{active_stage_list[0]}\t"
                                                 f"`{w1} {active_warp_list[0]}\t"
                                                 f"`{w2} {active_warp_list[1]}\t"
                                                 f"`{w3} {active_warp_list[2]}\t"
                                                 f"`{w4} {active_warp_list[3]}\t"
                                                 f"`{w5} {active_warp_list[4]}\t"
                                                 f"`{w6} {active_warp_list[5]}\t"
                                                 f"`{w7} {active_warp_list[6]}", False))

    # Lizard-man save proofing
    rom.write_bytes(0xA99AC, [0x08, 0x0F, 0xF0, 0xB8])  # J 0x803FC2E0
    rom.write_bytes(0xBFC2E0, Patches.boss_save_stopper)

    # Disable or guarantee vampire Vincent's fight
    if world.vincent_fight_condition[player] == "never":
        rom.write_bytes(0xAACC0, [0x24, 0x01, 0x00, 0x01])  # ADDIU AT, R0, 0x0001
    elif world.vincent_fight_condition[player] == "always":
        rom.write_bytes(0xAACE0, [0x24, 0x18, 0x00, 0x10])  # ADDIU	T8, R0, 0x0010
    else:
        rom.write_bytes(0xAACE0, [0x24, 0x18, 0x00, 0x00])  # ADDIU	T8, R0, 0x0000

    # Disable or guarantee Renon's fight
    rom.write_bytes(0xAACB4, [0x08, 0x0F, 0xF1, 0xA4])  # J 0x803FC690
    if world.renon_fight_condition[player] == "never":
        rom.write_byte(0xB804F0, 0x00)
        rom.write_byte(0xB80632, 0x00)
        rom.write_byte(0xB807E3, 0x00)
        rom.write_byte(0xB80988, 0xB8)
        rom.write_byte(0xB816BD, 0xB8)
        rom.write_byte(0xB817CF, 0x00)
        rom.write_bytes(0xBFC690, Patches.renon_cutscene_checker_jr)
    elif world.renon_fight_condition[player] == "always":
        rom.write_byte(0xB804F0, 0x0C)
        rom.write_byte(0xB80632, 0x0C)
        rom.write_byte(0xB807E3, 0x0C)
        rom.write_byte(0xB80988, 0xC4)
        rom.write_byte(0xB816BD, 0xC4)
        rom.write_byte(0xB817CF, 0x0C)
        # rom.write_bytes(0xB816C9, 0x00, 0x00)
        rom.write_bytes(0xBFC690, Patches.renon_cutscene_checker_jr)
    else:
        rom.write_bytes(0xBFC690, Patches.renon_cutscene_checker)

    # Disable or guarantee the Bad Ending
    if world.bad_ending_condition[player] == "never":
        rom.write_bytes(0xAEE5C6, [0x3C, 0x0A, 0x00, 0x00])  # LUI  T2, 0x0000
    elif world.bad_ending_condition[player] == "always":
        rom.write_bytes(0xAEE5C6, [0x3C, 0x0A, 0x00, 0x40])  # LUI  T2, 0x0040

    # Play Castle Keep's song if teleporting in front of Dracula's door outside the escape sequence
    rom.write_bytes(0x6E937C, [0x08, 0x0F, 0xF1, 0x2E])
    rom.write_bytes(0xBFC4B8, Patches.ck_door_music_player)

    # Increase item capacity to 100
    if world.increase_item_limit[player]:
        rom.write_byte(0xBF30B, 0x64)  # Most items
        rom.write_byte(0xBF3F7, 0x64)  # Sun/Moon cards
    rom.write_byte(0xBF353, 0x64)  # Keys (increase regardless)

    # Prevent the vanilla Magical Nitro transport's "can explode" flag from setting
    rom.write_bytes(0xB5D7AA, [0x00, 0x00, 0x00, 0x00])

    # Enable the Game Over's "Continue" menu starting the cursor on whichever checkpoint is most recent
    rom.write_bytes(0xB4DDC, [0x0C, 0x06, 0x0D, 0x58])  # JAL 0x80183560
    rom.write_bytes(0x106750, Patches.continue_cursor_start_checker)
    rom.write_bytes(0x1C444, [0x08, 0x0F, 0xF0, 0x90])  # J   0x803FC240
    rom.write_bytes(0xBFC240, Patches.savepoint_cursor_updater)
    rom.write_bytes(0x1C2D0, [0x08, 0x0F, 0xF0, 0x94])  # J   0x803FC250
    rom.write_bytes(0xBFC250, Patches.stage_start_cursor_updater)
    rom.write_byte(0xB585C8, 0xFF)

    # Add data for White Jewel #22 (the new Duel Tower savepoint) at the end of the White Jewel ID data list
    rom.write_bytes(0x104AC8, [0x00, 0x00, 0x00, 0x06,
                               0x00, 0x13, 0x00, 0x15])

    # Spawn coordinates list extension
    rom.write_bytes(0xD5BF4, [0x08, 0x0F, 0xF1, 0x03])  # J	0x803FC40C
    rom.write_bytes(0xBFC40C, Patches.spawn_coordinates_extension)
    rom.write_bytes(0x108A5E, Patches.waterway_end_coordinates)

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
    for stage in range(len(active_stage_list) - 1):
        for offset in stage_dict[active_stage_list[stage]].stage_number_offset_list:
            rom.write_byte(offset, stage_number)
        if active_stage_list[stage - 2] == RegionName.castle_center:
            stage_number -= 1
        elif active_stage_list[stage - 1] != RegionName.villa:
            stage_number += 1

    # Top elevator switch check
    rom.write_bytes(0x6CF0A0, [0x0C, 0x0F, 0xF0, 0xAF])  # JAL 0x803FC2BC
    rom.write_bytes(0xBFC2BC, Patches.elevator_flag_checker)

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
    rom.write_bytes(0x1067B0, Patches.custom_code_loader)

    # Custom remote item rewarding and DeathLink receiving code
    rom.write_bytes(0x19B98, [0x08, 0x0F, 0xF0, 0x00])  # J 0x803FC000
    rom.write_bytes(0xBFC000, Patches.remote_item_giver)

    # DeathLink counter decrementer code
    rom.write_bytes(0x1C2A0, [0x08, 0x0F, 0xF0, 0x52])  # J 0x803FC148
    rom.write_bytes(0x1C340, [0x08, 0x0F, 0xF0, 0x52])  # J 0x803FC148
    rom.write_bytes(0xBFC148, Patches.deathlink_counter_decrementer)

    # Death flag un-setter on "Beginning of stage" state overwrite code
    rom.write_bytes(0x1C2B0, [0x08, 0x0F, 0xF0, 0x47])  # J 0x803FC11C
    rom.write_bytes(0xBFC11C, Patches.death_flag_unsetter)

    # Warp menu-opening code
    rom.write_bytes(0xB9BA8, [0x08, 0x0F, 0xF0, 0x9B])  # J	0x803FC26C
    rom.write_bytes(0xBFC26C, Patches.warp_menu_opener)

    # NPC item textbox hack
    rom.write_bytes(0xBF1DC, [0x08, 0x0F, 0xF0, 0x67])  # J 0x803FC19C
    rom.write_bytes(0xBF1E0, [0x27, 0xBD, 0xFF, 0xE0])  # ADDIU SP, SP, -0x20
    rom.write_bytes(0xBFC19C, Patches.npc_item_hack)

    # Sub-weapon check function hook
    rom.write_bytes(0xBF32C, [0x00, 0x00, 0x00, 0x00])  # NOP
    rom.write_bytes(0xBF330, [0x08, 0x0F, 0xF0, 0x5D])  # J	0x803FC174
    rom.write_bytes(0xBFC174, Patches.give_subweapon_stopper)

    # Warp menu Special1 restriction
    rom.write_bytes(0xADD68, [0x0C, 0x04, 0xAB, 0x12])  # JAL 0x8012AC48
    rom.write_bytes(0xADE28, Patches.stage_select_overwrite)
    rom.write_byte(0xADE47, world.special1s_per_warp[player])

    # Dracula's door text pointer hijack
    rom.write_bytes(0xD69F0, [0x08, 0x0F, 0xF1, 0x41])  # J 0x803FC504
    rom.write_bytes(0xBFC504, Patches.dracula_door_text_redirector)

    # Dracula's chamber condition
    rom.write_bytes(0xE2FDC, [0x08, 0x04, 0xAB, 0x25])  # J 0x8012AC78
    rom.write_bytes(0xADE84, Patches.special_goal_checker)
    rom.write_bytes(0xBFCC3C, [0xA0, 0x00, 0xFF, 0xFF, 0xA0, 0x01, 0xFF, 0xFF, 0xA0, 0x02, 0xFF, 0xFF, 0xA0, 0x03, 0xFF,
                               0xFF, 0xA0, 0x04, 0xFF, 0xFF, 0xA0, 0x05, 0xFF, 0xFF, 0xA0, 0x06, 0xFF, 0xFF, 0xA0, 0x07,
                               0xFF, 0xFF, 0xA0, 0x08, 0xFF, 0xFF, 0xA0, 0x09])
    if world.draculas_condition[player] == 1:
        rom.write_bytes(0x6C8A54, [0x0C, 0x0F, 0xF0, 0x89])  # JAL 0x803FC224
        rom.write_bytes(0xBFC224, Patches.crystal_special2_giver)
        rom.write_byte(0xADE8F, 0x01)
        rom.write_bytes(0xBFCC62, cv64_text_converter(f"It won't budge!\n"
                                                      f"You'll need the power\n"
                                                      f"of the basement crystal\n"
                                                      f"to undo the seal.", True))
    elif world.draculas_condition[player] == 2:
        rom.write_bytes(0xBBD50, [0x08, 0x0F, 0xF1, 0x8C])  # J	0x803FC630
        rom.write_bytes(0xBFC630, Patches.boss_special2_giver)
        rom.write_bytes(0xBFC55C, Patches.werebull_flag_unsetter_special2_electric_boogaloo)
        rom.write_byte(0xADE8F, world.bosses_required[player].value)
        rom.write_bytes(0xBFCC62, cv64_text_converter(f"It won't budge!\n"
                                                      f"You'll need to defeat\n"
                                                      f"{required_s2s} powerful monsters\n"
                                                      f"to undo the seal.", True))
    elif world.draculas_condition[player] == 3:
        rom.write_byte(0xADE8F, world.special2s_required[player].value)
        rom.write_bytes(0xBFCC62, cv64_text_converter(f"It won't budge!\n"
                                                      f"You'll need to find\n"
                                                      f"{required_s2s} Special2 jewels\n"
                                                      f"to undo the seal.", True))
    else:
        rom.write_byte(0xADE8F, 0x00)

    # On-the-fly TLB script modifier
    rom.write_bytes(0xBFC338, Patches.double_component_checker)
    rom.write_bytes(0xBFC3D4, Patches.downstairs_seal_checker)
    rom.write_bytes(0xBFC700, Patches.tlb_modifiers)

    # On-the-fly scene object data modifier hook
    rom.write_bytes(0xEAB04, [0x08, 0x0F, 0xF2, 0x40])  # J 0x803FC900
    rom.write_bytes(0xBFC8F8, Patches.scene_data_modifiers)

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
    rom.write_bytes(0x10AB50, [0x0D, 0x0C, 0x00, 0x00, 0x80, 0x15, 0xFB, 0xD4])
    rom.write_bytes(0x10AB64, [0x0D, 0x0C, 0x00, 0x00, 0x80, 0x15, 0xFB, 0xD4])
    rom.write_bytes(0xE2E14, Patches.normal_door_hook)
    rom.write_bytes(0xBFC5D0, Patches.normal_door_code)
    rom.write_bytes(0x6EF298, Patches.ct_door_hook)
    rom.write_bytes(0xBFC608, Patches.ct_door_code)
    # Fix key counter not decrementing if 2 or above
    rom.write_bytes(0xAA0E0, [0x24, 0x02, 0x00, 0x00])  # ADDIU	V0, R0, 0x0000

    # Make the Easy-only candle drops in Room of Clocks appear on any difficulty
    rom.write_byte(0x9B518F, 0x01)

    # Slightly move some once-invisible freestanding items to be more visible
    # if world.reveal_invisible_items[player]:
    rom.write_byte(0x7C7F95, 0xEF)  # Forest dirge maiden statue
    rom.write_byte(0x7C7FA8, 0xAB)  # Forest werewolf statue
    rom.write_byte(0x8099C4, 0x8C)  # Villa courtyard tombstone
    rom.write_byte(0x83A626, 0xC2)  # Villa living room painting
    # rom.write_byte(0x83A62F, 0x64)  # Villa Mary's room table
    rom.write_byte(0x8985DD, 0xF5)  # CC torture instrument rack
    rom.write_byte(0x8C44D5, 0x22)  # CC red carpet hallway knight
    rom.write_byte(0x8DF57C, 0xF1)  # CC cracked wall hallway flamethrower
    rom.write_byte(0x90FCD6, 0xA5)  # CC nitro hallway flamethrower
    rom.write_byte(0x90FB9F, 0x9A)  # CC invention room round machine
    rom.write_byte(0x90FBAF, 0x03)  # CC invention room giant famicart
    rom.write_byte(0x90FE54, 0x97)  # CC staircase knight (x)
    rom.write_byte(0x90FE58, 0xFB)  # CC staircase knight (z)

    # Item property table extension (for the remaining invisible items)
    # rom.write_bytes(0xBFCD20, Patches.item_property_list_extension)

    # Write the new scene/spawn IDs for Stage Shuffle
    if world.stage_shuffle[player]:
        rom.write_byte(0xB73308, stage_dict[active_stage_list[0]].start_map_id)
        rom.write_byte(0xD9DAB, stage_dict[active_stage_list[active_stage_list.index(RegionName.villa) + 2]].start_map_id)
        rom.write_byte(0x109CCF, stage_dict[active_stage_list[active_stage_list.index(RegionName.castle_center) + 3]].start_map_id)
        for stage in range(len(active_stage_list) - 1):
            if active_stage_list[stage - 1] == RegionName.villa:
                rom.write_byte(stage_dict[active_stage_list[stage]].endzone_map_offset,
                               stage_dict[active_stage_list[stage + 2]].start_map_id)
                rom.write_byte(stage_dict[active_stage_list[stage]].endzone_spawn_offset,
                               stage_dict[active_stage_list[stage + 2]].start_spawn_id)
            elif active_stage_list[stage - 2] == RegionName.castle_center:
                rom.write_byte(stage_dict[active_stage_list[stage]].endzone_map_offset,
                               stage_dict[active_stage_list[stage + 3]].start_spawn_id)
                rom.write_byte(stage_dict[active_stage_list[stage]].endzone_spawn_offset,
                               stage_dict[active_stage_list[stage + 3]].start_spawn_id)
            elif active_stage_list[stage - 1] != RegionName.villa and active_stage_list[stage - 2] != RegionName.castle_center:
                rom.write_byte(stage_dict[active_stage_list[stage]].endzone_map_offset,
                               stage_dict[active_stage_list[stage + 1]].start_map_id)
                rom.write_byte(stage_dict[active_stage_list[stage]].endzone_spawn_offset,
                               stage_dict[active_stage_list[stage + 1]].start_spawn_id)

            if stage_dict[active_stage_list[stage]].startzone_map_offset != 0xFFFFFF:
                if stage - 1 < 0:
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_map_offset,
                                   stage_dict[active_stage_list[stage]].start_map_id)
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_spawn_offset,
                                   stage_dict[active_stage_list[stage]].start_spawn_id)
                elif active_stage_list[stage - 2] == RegionName.villa:
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_map_offset, 0x1A)
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_spawn_offset, 0x03)
                elif active_stage_list[stage - 3] == RegionName.villa:
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_map_offset,
                                   stage_dict[active_stage_list[stage - 2]].end_map_id)
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_spawn_offset,
                                   stage_dict[active_stage_list[stage - 2]].end_spawn_id)
                elif active_stage_list[stage - 3] == RegionName.castle_center:
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_map_offset, 0x0F)
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_spawn_offset, 0x03)
                elif active_stage_list[stage - 5] == RegionName.castle_center:
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_map_offset,
                                   stage_dict[active_stage_list[stage - 3]].end_map_id)
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_spawn_offset,
                                   stage_dict[active_stage_list[stage - 3]].end_spawn_id)
                else:
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_map_offset,
                                   stage_dict[active_stage_list[stage - 1]].end_map_id)
                    rom.write_byte(stage_dict[active_stage_list[stage]].startzone_spawn_offset,
                                   stage_dict[active_stage_list[stage - 1]].end_spawn_id)

    # Write the new item bytes
    for offset, item_id in offsets_to_ids.items():
        rom.write_byte(offset, item_id)

    # Write the new sub-weapon bytes (if Sub-weapon Shuffle is on)
    if world.sub_weapon_shuffle[player]:
        for offset, sub_id in sub_weapon_dict.items():
            rom.write_byte(offset, sub_id)


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
        # file_name = options["cv64_options"]["rom_file"]
        file_name = "Castlevania (USA).z64"
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

