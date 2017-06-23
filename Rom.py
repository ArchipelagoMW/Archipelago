from Dungeons import dungeon_music_addresses
from Text import string_to_alttp_text, text_addresses, credits_addresses, string_to_credits
from Text import Uncle_texts, Ganon1_texts, PyramidFairy_texts, TavernMan_texts, Sahasrahla2_texts, Triforce_texts, Blind_texts, BombShop2_texts
from Text import KingsReturn_texts, Sanctuary_texts, Kakariko_texts, Blacksmiths_texts, DeathMountain_texts, LostWoods_texts, WishingWell_texts, DesertPalace_texts, MountainTower_texts, LinksHouse_texts, Lumberjacks_texts, SickKid_texts, FluteBoy_texts, Zora_texts, MagicShop_texts
import random
import json
import hashlib
import logging

JAP10HASH = '03a63945398191337e896e5771f77173'
RANDOMIZERBASEHASH = '89fcdb48446bd858878f14e8a994d0b8'


def patch_rom(world, rom, hashtable, quickswap=False, beep='normal', sprite=None):
    # patch items
    for location in world.get_locations():
        itemid = location.item.code if location.item is not None else 0x5A

        if itemid is None or location.address is None:
            continue

        locationaddress = location.address
        if not location.crystal:
            # regular items
            write_byte(rom, locationaddress, itemid)
        else:
            # crystals
            for address, value in zip(locationaddress, itemid):
                write_byte(rom, address, value)

            # patch music
            music_addresses = dungeon_music_addresses[location.name]
            music = 0x11 if 'Pendant' in location.item.name else 0x16
            for music_address in music_addresses:
                write_byte(rom, music_address, music)

    # store old door overlay table
    door_overlays = bytearray(rom[0x15488:0x15488+0x10A])

    # patch entrances
    for region in world.regions:
        for exit in region.exits:
            if exit.target is not None:
                addresses = [exit.addresses] if isinstance(exit.addresses, int) else exit.addresses
                for address in addresses:
                    write_byte(rom, address, exit.target)

                # this does not yet seem to fix our door headaches ...
                if world.fix_door_frames and exit.vanilla is not None:
                    # patch door overlay table. The value of where this now leads is patched into the location where this entrance would lead in vanilla
                    write_byte(rom, 0x15488 + (2*exit.vanilla), door_overlays[2*exit.target])
                    write_byte(rom, 0x15489 + (2 * exit.vanilla), door_overlays[(2 * exit.target) + 1])

    # patch medallion requirements
    if world.required_medallions[0] == 'Bombos':
        write_byte(rom, 0x180022, 0x00)  # requirement
        write_byte(rom, 0x4FF2, 0x31)  # sprite
        write_byte(rom, 0x50D1, 0x80)
        write_byte(rom, 0x51B0, 0x00)
    elif world.required_medallions[0] == 'Quake':
        write_byte(rom, 0x180022, 0x02)  # requirement
        write_byte(rom, 0x4FF2, 0x31)  # sprite
        write_byte(rom, 0x50D1, 0x88)
        write_byte(rom, 0x51B0, 0x00)
    if world.required_medallions[1] == 'Bombos':
        write_byte(rom, 0x180023, 0x00)  # requirement
        write_byte(rom, 0x5020, 0x31)  # sprite
        write_byte(rom, 0x50FF, 0x90)
        write_byte(rom, 0x51DE, 0x00)
    elif world.required_medallions[1] == 'Ether':
        write_byte(rom, 0x180023, 0x01)  # requirement
        write_byte(rom, 0x5020, 0x31)  # sprite
        write_byte(rom, 0x50FF, 0x98)
        write_byte(rom, 0x51DE, 0x00)

    # set open mode:
    if world.mode == 'open':
        write_byte(rom, 0x180032, 0x01)  # open mode

        # disable sword sprite from uncle
        write_bytes(rom, 0x6D263, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        write_bytes(rom, 0x6D26B, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        write_bytes(rom, 0x6D293, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        write_bytes(rom, 0x6D29B, [0x00, 0x00, 0xf7, 0xff, 0x00, 0x0E])
        write_bytes(rom, 0x6D2B3, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
        write_bytes(rom, 0x6D2BB, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
        write_bytes(rom, 0x6D2E3, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
        write_bytes(rom, 0x6D2EB, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
        write_bytes(rom, 0x6D31B, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])
        write_bytes(rom, 0x6D323, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])
    else:
        write_byte(rom, 0x180032, 0x00)  # standard mode

    # set light cones
    write_byte(rom, 0x180038, 0x01 if world.sewer_light_cone else 0x00)
    write_byte(rom, 0x180039, 0x01 if world.light_world_light_cone else 0x00)
    write_byte(rom, 0x18003A, 0x01 if world.dark_world_light_cone else 0x00)

    # disable light world cane in minor glitches
    if world.logic == 'minorglitches':
        write_byte(rom, 0x180039, 0x00)  # light world light cone disable
        write_byte(rom, 0x18003A, 0x00)  # dark world light cone disable

    # handle difficulty
    if world.difficulty == 'hard':
        # Spike Cave Damage
        write_byte(rom, 0x180168, 0x02)
        # Powdered Fairies Prize
        write_byte(rom, 0x36DD0, 0x79)  # Bee
        # potion heal amount
        write_byte(rom, 0x180084, 0x08)  # One Heart
        # potion magic restore amount
        write_byte(rom, 0x180085, 0x20)  # Quarter Magic
    else:
        # Spike Cave Damage
        write_byte(rom, 0x180168, 0x08)
        # Powdered Fairies Prize
        write_byte(rom, 0x36DD0, 0xE3)  # fairy
        # potion heal amount
        write_byte(rom, 0x180084, 0xA0)  # full
        # potion magic restore amount
        write_byte(rom, 0x180085, 0x80)  # full

    # set up game internal RNG seed
    for i in range(1024):
        write_byte(rom, 0x178000 + i, random.randint(0, 255))

    # shuffle prize packs
    prizes = [0xD8, 0xD8, 0xD8, 0xD8, 0xD9, 0xD8, 0xD8, 0xD9, 0xDA, 0xD9, 0xDA, 0xDB, 0xDA, 0xD9, 0xDA, 0xDA, 0xE0, 0xDF, 0xDF, 0xDA, 0xE0, 0xDF, 0xD8, 0xDF,
              0xDC, 0xDC, 0xDC, 0xDD, 0xDC, 0xDC, 0xDE, 0xDC, 0xE1, 0xD8, 0xE1, 0xE2, 0xE1, 0xD8, 0xE1, 0xE2, 0xDF, 0xD9, 0xD8, 0xE1, 0xDF, 0xDC, 0xD9, 0xD8,
              0xD8, 0xE3, 0xE0, 0xDB, 0xDE, 0xD8, 0xDB, 0xE2, 0xD9, 0xDA, 0xDB, 0xD9, 0xDB, 0xD9, 0xDB]
    random.shuffle(prizes)

    # write tree pull prizes
    write_byte(rom, 0xEFBD4, prizes.pop())
    write_byte(rom, 0xEFBD5, prizes.pop())
    write_byte(rom, 0xEFBD6, prizes.pop())

    # rupee crab prizes
    write_byte(rom, 0x329C8, prizes.pop())  # first prize
    write_byte(rom, 0x329C4, prizes.pop())  # final prize

    # stunned enemy prize
    write_byte(rom, 0x37993, prizes.pop())

    # saved fish prize
    write_byte(rom, 0xE82CC, prizes.pop())

    # fill enemy prize packs
    write_bytes(rom, 0x37A78, prizes)

    # prize pack drop chances
    if world.difficulty == 'hard':
        droprates = [0x01, 0x02, 0x03, 0x03, 0x03, 0x04, 0x04]  # 50%, 25%, 3* 12.5%, 2* 6.25%
    else:
        droprates = [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]  # 50%

    random.shuffle(droprates)
    write_bytes(rom, 0x37A62, droprates)

    # shuffle enemies to prize packs
    for i in range(243):
        if rom[0x6B632 + i] & 0x0F != 0x00:
            rom[0x6B632 + i] = (rom[0x6B632 + i] & 0xF0) | random.randint(1, 7)

    # set bonk prizes
    bonk_prizes = [0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xAC, 0xE3, 0xE3, 0xDA, 0xE3, 0xDA, 0xD8, 0xAC, 0xAC, 0xE3, 0xD8, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xDC, 0xDB, 0xE3, 0xDA, 0x79, 0x79, 0xE3, 0xE3,
                   0xDA, 0x79, 0xAC, 0xAC, 0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xE3, 0x79, 0xDE, 0xE3, 0xAC, 0xDB, 0x79, 0xE3, 0xD8, 0xAC, 0x79, 0xE3, 0xDB, 0xDB, 0xE3, 0xE3, 0x79, 0xD8, 0xDD]
    bonk_addresses = [0x4CF6C, 0x4CFBA, 0x4CFE0, 0x4CFFB, 0x4D018, 0x4D01B, 0x4D028, 0x4D03C, 0x4D059, 0x4D07A, 0x4D09E, 0x4D0A8, 0x4D0AB, 0x4D0AE, 0x4D0BE, 0x4D0DD,
                      0x4D16A, 0x4D1E5, 0x4D1EE, 0x4D20B, 0x4CBBF, 0x4CBBF, 0x4CC17, 0x4CC1A, 0x4CC4A, 0x4CC4D, 0x4CC53, 0x4CC69, 0x4CC6F, 0x4CC7C, 0x4CCEF, 0x4CD51,
                      0x4CDC0, 0x4CDC3, 0x4CDC6, 0x4CE37, 0x4D2DE, 0x4D32F, 0x4D355, 0x4D367, 0x4D384, 0x4D387, 0x4D397, 0x4D39E, 0x4D3AB, 0x4D3AE, 0x4D3D1, 0x4D3D7,
                      0x4D3F8, 0x4D416, 0x4D420, 0x4D423, 0x4D42D, 0x4D449, 0x4D48C, 0x4D4D9, 0x4D4DC, 0x4D4E3, 0x4D504, 0x4D507, 0x4D55E, 0x4D56A]
    random.shuffle(bonk_prizes)
    for prize, address in zip(bonk_prizes, bonk_addresses):
        write_byte(rom, address, prize)

    # set Fountain bottle exchange items
    write_byte(rom, 0x348FF, [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)])
    write_byte(rom, 0x3493B, [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)])
    # set Fat Fairy Bow/Sword prizes to be disappointing
    write_byte(rom, 0x34914, 0x3A)  # Bow and Arrow
    write_byte(rom, 0x180028, 0x49)  # Fighter Sword

    # set swordless mode settings
    write_byte(rom, 0x18003F, 0x01 if world.mode == 'swordless' else 0x00)  # hammer can harm ganon
    write_byte(rom, 0x180040, 0x01 if world.mode == 'swordless' else 0x00)  # open curtains
    write_byte(rom, 0x180041, 0x01 if world.mode == 'swordless' else 0x00)  # swordless medallions
    write_byte(rom, 0x180042, 0xFF if world.mode == 'swordless' else 0x00)  # starting sword for link

    # set up clocks for timed modes
    if world.clock_mode == 'off':
        write_bytes(rom, 0x180190, [0x00, 0x00, 0x00])  # turn off clock mode
        write_bytes(rom, 0x180200, [0x00, 0x00, 0x00, 0x00])  # red clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x180204, [0x00, 0x00, 0x00, 0x00])  # blue clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x180208, [0x00, 0x00, 0x00, 0x00])  # green clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x18020C, [0x00, 0x00, 0x00, 0x00])  # starting time (in frames, sint32)
    elif world.clock_mode == 'ohko':
        write_bytes(rom, 0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
        write_bytes(rom, 0x180200, [0x00, 0x00, 0x00, 0x00])  # red clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x180204, [0x00, 0x00, 0x00, 0x00])  # blue clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x180208, [0x50, 0x46, 0x00, 0x00])  # green clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x18020C, [0xA0, 0x8C, 0x00, 0x00])  # starting time (in frames, sint32)
    if world.clock_mode == 'stopwatch':
        write_bytes(rom, 0x180190, [0x02, 0x01, 0x00])  # set stopwatch mode
        write_bytes(rom, 0x180200, [0xE0, 0xE3, 0xFF, 0xFF])  # red clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x180204, [0x20, 0x1C, 0x00, 0x00])  # blue clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x180208, [0x40, 0x38, 0x00, 0x00])  # green clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x18020C, [0x00, 0x00, 0x00, 0x00])  # starting time (in frames, sint32)
    if world.clock_mode == 'countdown':
        write_bytes(rom, 0x180190, [0x01, 0x01, 0x00])  # set countdown, with no reset available
        write_bytes(rom, 0x180200, [0xE0, 0xE3, 0xFF, 0xFF])  # red clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x180204, [0x20, 0x1C, 0x00, 0x00])  # blue clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x180208, [0x40, 0x38, 0x00, 0x00])  # green clock adjustment time (in frames, sint32)
        write_bytes(rom, 0x18020C, [0x80, 0x32, 0x02, 0x00])  # starting time (in frames, sint32)

    # set up goals for treasure hunt
    write_bytes(rom, 0x180165, [0x0E, 0x28] if world.treasure_hunt_icon == 'Triforce Piece' else [0x0D, 0x28])
    write_byte(rom, 0x180167, world.treasure_hunt_count % 256)

    # assorted fixes
    write_byte(rom, 0x180030, 0x00)  # Disable SRAM trace
    write_byte(rom, 0x180036, 0x0A)  # Rupoor negative value
    write_byte(rom, 0x180169, 0x01 if world.lock_aga_door_in_escape else 0x00)  # Lock or unlock aga tower door during escape sequence.
    write_byte(rom, 0x180086, 0x00 if world.aga_randomness else 0x01)  # set blue ball and ganon warp randomness
    write_byte(rom, 0x1800A1, 0x01)  # enable overworld screen transition draining for water level inside swamp
    if world.goal in ['pedestal', 'starhunt', 'triforcehunt']:
        write_byte(rom, 0x18003E, 0x01)  # make ganon invincible
    elif world.goal in ['dungeons']:
        write_byte(rom, 0x18003E, 0x02)  # make ganon invincible until all dungeons are beat
    write_byte(rom, 0x18016A, 0x00)  # disable free roaming item text boxes
    write_byte(rom, 0x18003B, 0x00)  # disable maps showing crystals on overworld
    write_byte(rom, 0x18003C, 0x00)  # disable compasses showing dungeon count
    digging_game_rng = random.randint(1, 30)  # set rng for digging game
    write_byte(rom, 0x180020, digging_game_rng)
    write_byte(rom, 0xEFD95, digging_game_rng)
    write_byte(rom, 0x1800A3, 0x01)  # enable correct world setting behaviour after agahnim kills
    write_byte(rom, 0x180042, 0x01 if world.save_and_quite_from_boss else 0x00)  # Allow Save and Quite after boss kill

    # remove shield from uncle
    write_bytes(rom, 0x6D253, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    write_bytes(rom, 0x6D25B, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    write_bytes(rom, 0x6D283, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    write_bytes(rom, 0x6D28B, [0x00, 0x00, 0xf7, 0xff, 0x00, 0x0E])
    write_bytes(rom, 0x6D2CB, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
    write_bytes(rom, 0x6D2FB, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
    write_bytes(rom, 0x6D313, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])

    if world.swamp_patch_required:
        # patch swamp: Need to enable permanent drain of water as dam or swamp were moved
        write_byte(rom, 0x18003D, 0x01)

    # set correct flag for hera basement item
    if world.get_location('[dungeon-L3-1F] Tower of Hera - Freestanding Key').item is not None and world.get_location('[dungeon-L3-1F] Tower of Hera - Freestanding Key').item.name == 'Small Key (Tower of Hera)':
        write_byte(rom, 0x4E3BB, 0xE4)
    else:
        write_byte(rom, 0x4E3BB, 0xEB)

    # disable open door sprites when exiting caves
    # this does not seem to work completely yet
    if world.fix_door_frames:
        for i in range(0x85):
            write_byte(rom, 0x15274 + i, 0x00)
        for i in range(0x86):
            write_byte(rom, 0x15488 + i, 0x02)
        # leave the entry marking tavern north a north facing exit
        for i in range(0x82):
            write_byte(rom, 0x15510 + i, 0x02)

    # fix trock doors for reverse entrances
    if world.fix_trock_doors:
        write_byte(rom, 0xFED31, 0x0E)  # preopen bombable exit
        write_byte(rom, 0xFEE41, 0x0E)  # preopen bombable exit
        write_byte(rom, 0xFE465, 0x1E)  # remove small key door on backside of big key door

    # enable quick item swapping with L and R (ported by Amazing Ampharos)
    if quickswap:
        write_bytes(rom, 0x107fb, [0x22, 0x50, 0xFF, 0x1F])
        write_bytes(rom, 0x12451, [0x22, 0x50, 0xFF, 0x1F])
        write_bytes(rom, 0xfff50, [0x20, 0x58, 0xFF, 0xA5, 0xF6, 0x29, 0x40, 0x6B, 0xA5, 0xF6, 0x89, 0x10, 0xF0, 0x03, 0x4C, 0x69,
                                   0xFF, 0x89, 0x20, 0xF0, 0x03, 0x4C, 0xAA, 0xFF, 0x60, 0xAD, 0x02, 0x02, 0xF0, 0x3B, 0xDA, 0xAA,
                                   0xE0, 0x0F, 0xF0, 0x14, 0xE0, 0x10, 0xF0, 0x14, 0xE0, 0x14, 0xD0, 0x02, 0xA2, 0x00, 0xE8, 0xBF,
                                   0x3F, 0xF3, 0x7E, 0xF0, 0xEB, 0x4C, 0xEB, 0xFF, 0xA2, 0x01, 0x80, 0x0A, 0xAF, 0x4F, 0xF3, 0x7E,
                                   0xAA, 0xE0, 0x04, 0xF0, 0x10, 0xE8, 0xBF, 0x5B, 0xF3, 0x7E, 0xF0, 0xF5, 0x8A, 0x8F, 0x4F, 0xF3,
                                   0x7E, 0xA2, 0x10, 0x80, 0xE0, 0xA2, 0x11, 0x80, 0xD6, 0x60, 0xAD, 0x02, 0x02, 0xF0, 0x3B, 0xDA,
                                   0xAA, 0xE0, 0x11, 0xF0, 0x14, 0xE0, 0x10, 0xF0, 0x14, 0xE0, 0x01, 0xD0, 0x02, 0xA2, 0x15, 0xCA,
                                   0xBF, 0x3F, 0xF3, 0x7E, 0xF0, 0xEB, 0x4C, 0xEB, 0xFF, 0xA2, 0x04, 0x80, 0x0A, 0xAF, 0x4F, 0xF3,
                                   0x7E, 0xAA, 0xE0, 0x01, 0xF0, 0x10, 0xCA, 0xBF, 0x5B, 0xF3, 0x7E, 0xF0, 0xF5, 0x8A, 0x8F, 0x4F,
                                   0xF3, 0x7E, 0xA2, 0x10, 0x80, 0xE0, 0xA2, 0x0F, 0x80, 0xD6, 0x60, 0xA9, 0x20, 0x8D, 0x2F, 0x01,
                                   0x8E, 0x02, 0x02, 0x22, 0x7F, 0xDB, 0x0D, 0xFA, 0x60, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

    write_strings(rom, world)

    # set rom name
    # 21 bytes
    write_bytes(rom, 0x7FC0, bytearray('ER_030_%09d_' % world.seed, 'utf8') + world.option_identifier.to_bytes(4, 'big'))

    # set heart beep rate
    write_byte(rom, 0x180033, {'off': 0x00, 'half': 0x40, 'quarter': 0x80, 'normal': 0x20}[beep])

    # store hash table for main menu hash
    write_bytes(rom, 0x181000, hashtable)

    # write link sprite if required
    if sprite is not None:
        write_bytes(rom, 0x80000, sprite)

    return rom


def write_byte(rom, address, value):
    rom[address] = value


def write_bytes(rom, startaddress, values):
    for i, value in enumerate(values):
        write_byte(rom, startaddress + i, value)


def write_string_to_rom(rom, target, string):
    address, maxbytes = text_addresses[target]
    write_bytes(rom, address, string_to_alttp_text(string, maxbytes))


def write_credits_string_to_rom(rom, target, string):
    address, length = credits_addresses[target]
    write_bytes(rom, address, string_to_credits(string, length))


def write_strings(rom, world):
    silverarrows = world.find_items('Silver Arrows')
    silverarrow_hint = (' %s?' % silverarrows[0].hint_text) if silverarrows else '?\nI think not!'
    write_string_to_rom(rom, 'Ganon2', 'Did you find the silver arrows%s' % silverarrow_hint)

    crystal5 = world.find_items('Crystal 5')[0]
    crystal6 = world.find_items('Crystal 6')[0]
    write_string_to_rom(rom, 'BombShop1', 'Big Bomb?\nMy supply is blocked until you clear %s and %s.' % (crystal5.hint_text, crystal6.hint_text))

    greenpendant = world.find_items('Green Pendant')[0]
    write_string_to_rom(rom, 'Sahasrahla1', 'I lost my family heirloom in %s' % greenpendant.hint_text)

    write_string_to_rom(rom, 'Uncle', Uncle_texts[random.randint(0, len(Uncle_texts) - 1)])
    write_string_to_rom(rom, 'Triforce', Triforce_texts[random.randint(0, len(Triforce_texts) - 1)])
    write_string_to_rom(rom, 'BombShop2', BombShop2_texts[random.randint(0, len(BombShop2_texts) - 1)])
    write_string_to_rom(rom, 'PyramidFairy', PyramidFairy_texts[random.randint(0, len(PyramidFairy_texts) - 1)])
    write_string_to_rom(rom, 'Sahasrahla2', Sahasrahla2_texts[random.randint(0, len(Sahasrahla2_texts) - 1)])
    write_string_to_rom(rom, 'Blind', Blind_texts[random.randint(0, len(Blind_texts) - 1)])
    if world.goal in ['pedestal', 'starhunt', 'triforcehunt']:
        write_string_to_rom(rom, 'Ganon1', 'Why are you even here?\n You can\'t even hurt me!')
    else:
        write_string_to_rom(rom, 'Ganon1', Ganon1_texts[random.randint(0, len(Ganon1_texts) - 1)])
    write_string_to_rom(rom, 'TavernMan', TavernMan_texts[random.randint(0, len(TavernMan_texts) - 1)])

    altaritem = world.get_location('Altar').item
    altar_text = 'Some Hot Air' if altaritem is None else altaritem.altar_hint_text if altaritem.altar_hint_text is not None else 'Unknown Item.'
    write_string_to_rom(rom, 'Altar', altar_text)
    altar_credit_text = 'and the Hot Air' if altaritem is None else altaritem.altar_credit_text if altaritem.altar_credit_text is not None else ' and the Unknown Item.'
    write_credits_string_to_rom(rom, 'Altar', altar_credit_text)

    write_credits_string_to_rom(rom, 'KingsReturn', KingsReturn_texts[random.randint(0, len(KingsReturn_texts) - 1)])
    write_credits_string_to_rom(rom, 'Sanctuary', Sanctuary_texts[random.randint(0, len(Sanctuary_texts) - 1)])
    write_credits_string_to_rom(rom, 'Kakariko', Kakariko_texts[random.randint(0, len(Kakariko_texts) - 1)])
    write_credits_string_to_rom(rom, 'Blacksmiths', Blacksmiths_texts[random.randint(0, len(Blacksmiths_texts) - 1)])
    write_credits_string_to_rom(rom, 'DeathMountain', DeathMountain_texts[random.randint(0, len(DeathMountain_texts) - 1)])
    write_credits_string_to_rom(rom, 'LostWoods', LostWoods_texts[random.randint(0, len(LostWoods_texts) - 1)])
    write_credits_string_to_rom(rom, 'WishingWell', WishingWell_texts[random.randint(0, len(WishingWell_texts) - 1)])
    write_credits_string_to_rom(rom, 'DesertPalace', DesertPalace_texts[random.randint(0, len(DesertPalace_texts) - 1)])
    write_credits_string_to_rom(rom, 'MountainTower', MountainTower_texts[random.randint(0, len(MountainTower_texts) - 1)])
    write_credits_string_to_rom(rom, 'LinksHouse', LinksHouse_texts[random.randint(0, len(LinksHouse_texts) - 1)])
    write_credits_string_to_rom(rom, 'Lumberjacks', Lumberjacks_texts[random.randint(0, len(Lumberjacks_texts) - 1)])

    sickkiditem = world.get_location('Sick Kid').item
    sickkiditem_text = SickKid_texts[random.randint(0, len(SickKid_texts) - 1)] if sickkiditem is None or sickkiditem.sickkid_credit_text is None else sickkiditem.sickkid_credit_text
    write_credits_string_to_rom(rom, 'SickKid', sickkiditem_text) 
    
    zoraitem = world.get_location('King Zora').item
    zoraitem_text = Zora_texts[random.randint(0, len(Zora_texts) - 1)] if zoraitem is None or zoraitem.zora_credit_text is None else zoraitem.zora_credit_text
    write_credits_string_to_rom(rom, 'Zora', zoraitem_text) 
    
    magicshopitem = world.get_location('Witch').item
    magicshopitem_text = MagicShop_texts[random.randint(0, len(MagicShop_texts) - 1)] if magicshopitem is None or magicshopitem.magicshop_credit_text is None else magicshopitem.magicshop_credit_text
    write_credits_string_to_rom(rom, 'MagicShop', magicshopitem_text) 
    
    fluteboyitem = world.get_location('Flute Boy').item
    fluteboyitem_text = FluteBoy_texts[random.randint(0, len(FluteBoy_texts) - 1)] if fluteboyitem is None or fluteboyitem.fluteboy_credit_text is None else fluteboyitem.fluteboy_credit_text
    write_credits_string_to_rom(rom, 'FluteBoy', fluteboyitem_text)


def patch_base_rom(rom):
    # verify correct checksum of baserom
    basemd5 = hashlib.md5()
    basemd5.update(rom)
    if not JAP10HASH == basemd5.hexdigest():
        logging.getLogger('').warning('Supplied Base Rom does not match known MD5 for JAP(1.0) release. Will try to patch anyway.')

    # extend to 2MB
    rom.extend(bytearray([0x00]*(2097152 - len(rom))))

    # load randomizer patches
    patches = json.load(open('base2current.json', 'r'))
    for patch in patches:
        if isinstance(patch, dict):
            for baseaddress, values in patch.items():
                write_bytes(rom, int(baseaddress), values)

    # verify md5
    patchedmd5 = hashlib.md5()
    patchedmd5.update(rom)
    if not RANDOMIZERBASEHASH == patchedmd5.hexdigest():
        raise RuntimeError('Provided Base Rom unsuitable for patching. Please provide a JAP(1.0) "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc" rom to use as a base.')
