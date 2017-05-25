from Regions import location_addresses, crystal_locations, dungeon_music_addresses
from EntranceShuffle import door_addresses, single_doors
from Text import string_to_alttp_text, text_addresses, altar_text
import random


def patch_rom(world, rom):
    # patch items
    for location in world.get_locations():
        if location.name == 'Ganon':
            # cannot shuffle this yet
            continue

        itemid = location.item.code if location.item is not None else 0x5A

        try:
            # regular items
            locationaddress = location_addresses[location.name]
            write_byte(rom, locationaddress, itemid)
        except KeyError:
            # crystals
            locationaddress = crystal_locations[location.name]
            for address, value in zip(locationaddress, itemid):
                write_byte(rom, address, value)

            # patch music
            music_addresses = dungeon_music_addresses[location.name]
            music = 0x11 if 'Pendant' in location.item.name else 0x16
            for music_address in music_addresses:
                write_byte(rom, music_address, music)

    # patch entrances
    for region in world.regions:
        for exit in region.exits:
            if exit.target is not None:
                try:
                    # ugly fix for agahnim fix in simple dungeon shuffle mode
                    if world.agahnim_fix_required and exit.name == 'Dark Death Mountain Ledge (East)':
                        write_byte(rom, door_addresses[exit.name][0], exit.target)
                        continue

                    addresses = door_addresses[exit.name]
                    write_byte(rom, addresses[0], exit.target[0])
                    write_byte(rom, addresses[1], exit.target[1])
                except KeyError:
                    # probably cave

                    # ugly fix for agahnim fix in simple dungeon shuffle mode
                    if world.agahnim_fix_required and exit.name == 'Mimic Cave Mirror Spot':
                        write_byte(rom, single_doors[exit.name], exit.target[0])
                        write_byte(rom, door_addresses['Dark Death Mountain Ledge (East)'][1], exit.target[1])
                        continue

                    addresses = single_doors[exit.name]
                    if not isinstance(addresses, tuple):
                        addresses = (addresses,)
                    for address in addresses:
                        write_byte(rom, address, exit.target)

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
        write_byte(rom, 0x180038, 0x00)  # sewers light cone disable
        write_byte(rom, 0x180039, 0x00)  # light world light cone disable
        write_byte(rom, 0x18003A, 0x00)  # dark world light cone disable

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
        write_byte(rom, 0x180038, 0x01)  # sewers light cone enabled
        write_byte(rom, 0x180039, 0x01)  # light world light cone enabled
        write_byte(rom, 0x18003A, 0x00)  # dark world light cone disable

    # disable light world cane in minor glitches
    if world.logic == 'minorglitches':
        write_byte(rom, 0x180039, 0x00)  # light world light cone disable
        write_byte(rom, 0x18003A, 0x00)  # dark world light cone disable

    # handle difficulty
    if world.difficulty == 'normal':
        # Spike Cave Damage
        write_byte(rom, 0x180168, 0x08)
        # Powdered Fairies Prize
        write_byte(rom, 0x36DD0, 0xE3)  # fairy
        # potion heal amount
        write_byte(rom, 0x180084, 0xA0)  # full
        # potion magic restore amount
        write_byte(rom, 0x180085, 0x80)  # full
    elif world.difficulty == 'hard':
        # Spike Cave Damage
        write_byte(rom, 0x180168, 0x02)
        # Powdered Fairies Prize
        write_byte(rom, 0x36DD0, 0x79)  # Bee
        # potion heal amount
        write_byte(rom, 0x180084, 0x08)  # One Heart
        # potion magic restore amount
        write_byte(rom, 0x180085, 0x20)  # Quarter Magic

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
    # in open mode with shuffled caves, cannot guarantee access to rupees or a shop. Make 4 kill tree pull single bombs always to give guaranteed access
    if world.shuffle not in ['default', 'dungeonsfull', 'dungeonssimple']:
        write_byte(rom, 0xEFBD6, 0xDC)

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
    if world.difficulty == 'normal':
        droprates = [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]  # 50%
    else:
        droprates = [0x01, 0x02, 0x03, 0x03, 0x03, 0x04, 0x04]  # 50%, 25%, 3* 12.5%, 2* 6.25%
    random.shuffle(droprates)
    write_bytes(rom, 0x37A62, droprates)

    # deal with sprize prize packs (ToDo: figure out what this ACTUALLY does Probably assigns sprites to drop classes
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

    if world.swamp_patch_required:
        # patch swamp: Need to enable permanent drain of water as dam or swamp were moved
        rom = rom.replace(bytearray([0xAF, 0xBB, 0xF2, 0x7E, 0x29, 0xDF, 0x8F, 0xBB, 0xF2, 0x7E]), bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))
        rom = rom.replace(bytearray([0xAF, 0xFB, 0xF2, 0x7E, 0x29, 0xDF, 0x8F, 0xFB, 0xF2, 0x7E]), bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))
        rom = rom.replace(bytearray([0xAF, 0x16, 0xF2, 0x7E, 0x29, 0x7F, 0x8F, 0x16, 0xF2, 0x7E]), bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))
        rom = rom.replace(bytearray([0xAF, 0x51, 0xF0, 0x7E, 0x29, 0xFE, 0x8F, 0x51, 0xF0, 0x7E]), bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))

    # set correct flag for hera basement item
    if world.get_location('[dungeon-L3-1F] Tower of Hera - Freestanding Key').item is not None and world.get_location('[dungeon-L3-1F] Tower of Hera - Freestanding Key').item.name == 'Small Key (Tower of Hera)':
        write_byte(rom, 0x4E3BB, 0xE4)
    else:
        write_byte(rom, 0x4E3BB, 0xEB)

    # write strings
    write_string_to_rom(rom, 'Ganon2', 'Did you find the silver arrows in Hyrule?')
    write_string_to_rom(rom, 'Uncle', 'Good Luck!\nYou will need it.')
    write_string_to_rom(rom, 'Triforce', 'Product has Hole in center. Bad seller, 0 out of 5.')
    write_string_to_rom(rom, 'BombShop1', 'Big Bomb?\nI Uh … Never heard of that. Move along.')
    write_string_to_rom(rom, 'BombShop2', 'Bombs!\nBombs!\nBiggest!\nBestest!\nGreatest!\nBoomest!')
    write_string_to_rom(rom, 'PyramidFairy', 'May I talk to you about our lord and savior, Ganon?')
    write_string_to_rom(rom, 'Sahasrahla1', 'How Did you Find me?')
    write_string_to_rom(rom, 'Sahasrahla2', 'You already got my item, idiot.')
    write_string_to_rom(rom, 'Blind', 'I bet you expected a vision related pun?\n\nNot Today.\n Didn\'t see that coming, did you?')
    write_string_to_rom(rom, 'Ganon1', '\n\n\n\n\n\n\n\n\nWhy are you reading an empty textbox?')
    write_string_to_rom(rom, 'TavernMan', 'Did you know that talking to random NPCs wastes time in a race? I hope this information may be of use to you in the future.')

    # disable open door sprites when exiting caves
    if world.shuffle not in ['default', 'dungeonssimple', 'dungeonsfull']:
        for i in range(0x85):
            write_byte(rom, 0x15274 + i, 0x00)

    altaritem = world.get_location('Altar').item.name if world.get_location('Altar').item is not None else 'Nothing'
    write_string_to_rom(rom, 'Altar', altar_text.get(altaritem, 'Unknown Item.'))

    return rom


def write_byte(rom, address, value):
    rom[address] = value


def write_bytes(rom, startaddress, values):
    for i, value in enumerate(values):
        write_byte(rom, startaddress + i, value)


def write_string_to_rom(rom, target, string):
    address, maxbytes = text_addresses[target]
    write_bytes(rom, address, string_to_alttp_text(string, maxbytes))