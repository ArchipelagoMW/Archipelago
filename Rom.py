from Dungeons import dungeon_music_addresses
from EntranceShuffle import door_addresses, single_doors
from Text import string_to_alttp_text, text_addresses, credits_addresses, string_to_credits
from Text import Uncle_texts, Ganon1_texts, PyramidFairy_texts, TavernMan_texts, Sahasrahla2_texts, Triforce_texts, Blind_texts, BombShop2_texts
from Text import KingsReturn_texts, Sanctuary_texts, Kakariko_texts, Blacksmiths_texts, DeathMountain_texts, LostWoods_texts, WishingWell_texts, DesertPalace_texts, MountainTower_texts, LinksHouse_texts, Lumberjacks_texts, SickKid_texts, FluteBoy_texts, Zora_texts, MagicShop_texts
import random


def patch_rom(world, rom, hashtable, quickswap=False, beep='normal', sprite=None):
    # patch items
    for location in world.get_locations():
        if location.name == 'Ganon':
            # cannot shuffle this yet
            continue

        itemid = location.item.code if location.item is not None else 0x5A

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

    # disable open door sprites when exiting caves
    if world.shuffle not in ['default', 'dungeonssimple', 'dungeonsfull']:
        for i in range(0x85):
            write_byte(rom, 0x15274 + i, 0x00)

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
    write_bytes(rom, 0x7FC0, [0x45, 0x6E, 0x74, 0x72, 0x61, 0x6E, 0x63, 0x65, 0x52, 0x61, 0x6E, 0x64, 0x6F, 0x6D, 0x69, 0x7A, 0x65, 0x72, 0x00, 0x00, 0x00])

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
    silverarrow_hint = ('in %s?' % silverarrows[0].hint_text) if silverarrows else '?\nI think not!'
    write_string_to_rom(rom, 'Ganon2', 'Did you find the silver arrows %s' % silverarrow_hint)

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
