from Dungeons import dungeon_music_addresses
from Text import string_to_alttp_text, text_addresses, credits_addresses, string_to_credits
from Text import Uncle_texts, Ganon1_texts, PyramidFairy_texts, TavernMan_texts, Sahasrahla2_texts, Triforce_texts, Blind_texts, BombShop2_texts
from Text import KingsReturn_texts, Sanctuary_texts, Kakariko_texts, Blacksmiths_texts, DeathMountain_texts, LostWoods_texts, WishingWell_texts, DesertPalace_texts, MountainTower_texts, LinksHouse_texts, Lumberjacks_texts, SickKid_texts, FluteBoy_texts, Zora_texts, MagicShop_texts
import random
import json
import hashlib
import logging

JAP10HASH = '03a63945398191337e896e5771f77173'
RANDOMIZERBASEHASH = '7f112e52921bf72c67296848f3f4ad97'


class JsonRom(object):

    def __init__(self):
        self.patches = {}

    def write_byte(self, address, value):
        self.patches[str(address)] = [value]

    def write_bytes(self, startaddress, values):
        self.patches[str(startaddress)] = list(values)

    def write_to_file(self, file):
        json.dump([self.patches], open(file, 'w'))


class LocalRom(object):

    def __init__(self, file):
        self.buffer = bytearray(open(file, 'rb').read())
        self.patch_base_rom()

    def write_byte(self, address, value):
        self.buffer[address] = value

    def write_bytes(self, startaddress, values):
        for i, value in enumerate(values):
            self.write_byte(startaddress + i, value)

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def patch_base_rom(self):
        # verify correct checksum of baserom
        basemd5 = hashlib.md5()
        basemd5.update(self.buffer)
        if not JAP10HASH == basemd5.hexdigest():
            logging.getLogger('').warning('Supplied Base Rom does not match known MD5 for JAP(1.0) release. Will try to patch anyway.')

        # extend to 2MB
        self.buffer.extend(bytearray([0x00] * (2097152 - len(self.buffer))))

        # load randomizer patches
        patches = json.load(open('base2current.json', 'r'))
        for patch in patches:
            if isinstance(patch, dict):
                for baseaddress, values in patch.items():
                    self.write_bytes(int(baseaddress), values)

        # verify md5
        patchedmd5 = hashlib.md5()
        patchedmd5.update(self.buffer)
        if not RANDOMIZERBASEHASH == patchedmd5.hexdigest():
           raise RuntimeError('Provided Base Rom unsuitable for patching. Please provide a JAP(1.0) "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc" rom to use as a base.')

    def write_crc(self):
        # this does not seem to work
        crc = sum(self.buffer[:0x7FEB] + self.buffer[0x7FF5:]) % 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])


def patch_rom(world, rom, hashtable, beep='normal', sprite=None):
    # patch items
    for location in world.get_locations():
        itemid = location.item.code if location.item is not None else 0x5A

        if itemid is None or location.address is None:
            continue

        locationaddress = location.address
        if not location.crystal:
            #Keys in their native dungeon should use the orignal item code for keys
            if location.parent_region.dungeon:
                dungeon=location.parent_region.dungeon
                if location.item.key and dungeon.is_dungeon_item(location.item):
                    if location.item.type == "BigKey": itemid = 0x32
                    if location.item.type == "SmallKey": itemid = 0x24
            rom.write_byte(locationaddress, itemid)
        else:
            # crystals
            for address, value in zip(locationaddress, itemid):
                rom.write_byte(address, value)

            # patch music
            music_addresses = dungeon_music_addresses[location.name]
            if world.keysanity:
                music = random.choice([0x11, 0x16])
            else:
                music = 0x11 if 'Pendant' in location.item.name else 0x16
            for music_address in music_addresses:
                rom.write_byte(music_address, music)
    
    if world.keysanity:
        rom.write_byte(0x155C9, random.choice([0x11, 0x16])) #Randomize GT music too in keysanity mode

    # patch entrances
    for region in world.regions:
        for exit in region.exits:
            if exit.target is not None:
                addresses = [exit.addresses] if isinstance(exit.addresses, int) else exit.addresses
                for address in addresses:
                    rom.write_byte(address, exit.target)

    # patch medallion requirements
    if world.required_medallions[0] == 'Bombos':
        rom.write_byte(0x180022, 0x00)  # requirement
        rom.write_byte(0x4FF2, 0x31)  # sprite
        rom.write_byte(0x50D1, 0x80)
        rom.write_byte(0x51B0, 0x00)
    elif world.required_medallions[0] == 'Quake':
        rom.write_byte(0x180022, 0x02)  # requirement
        rom.write_byte(0x4FF2, 0x31)  # sprite
        rom.write_byte(0x50D1, 0x88)
        rom.write_byte(0x51B0, 0x00)
    if world.required_medallions[1] == 'Bombos':
        rom.write_byte(0x180023, 0x00)  # requirement
        rom.write_byte(0x5020, 0x31)  # sprite
        rom.write_byte(0x50FF, 0x90)
        rom.write_byte(0x51DE, 0x00)
    elif world.required_medallions[1] == 'Ether':
        rom.write_byte(0x180023, 0x01)  # requirement
        rom.write_byte(0x5020, 0x31)  # sprite
        rom.write_byte(0x50FF, 0x98)
        rom.write_byte(0x51DE, 0x00)

    # set open mode:
    if world.mode in ['open', 'swordless']:
        rom.write_byte(0x180032, 0x01)  # open mode

        # disable sword sprite from uncle
        rom.write_bytes(0x6D263, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        rom.write_bytes(0x6D26B, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        rom.write_bytes(0x6D293, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        rom.write_bytes(0x6D29B, [0x00, 0x00, 0xf7, 0xff, 0x00, 0x0E])
        rom.write_bytes(0x6D2B3, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
        rom.write_bytes(0x6D2BB, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
        rom.write_bytes(0x6D2E3, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
        rom.write_bytes(0x6D2EB, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
        rom.write_bytes(0x6D31B, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])
        rom.write_bytes(0x6D323, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])
    else:
        rom.write_byte(0x180032, 0x00)  # standard mode

    # set light cones
    rom.write_byte(0x180038, 0x01 if world.sewer_light_cone else 0x00)
    rom.write_byte(0x180039, 0x01 if world.light_world_light_cone else 0x00)
    rom.write_byte(0x18003A, 0x01 if world.dark_world_light_cone else 0x00)

    # handle difficulty
    if world.difficulty == 'hard':
        # Spike Cave Damage
        rom.write_byte(0x180168, 0x02)
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0x79)  # Bee
        # potion heal amount
        rom.write_byte(0x180084, 0x08)  # One Heart
        # potion magic restore amount
        rom.write_byte(0x180085, 0x20)  # Quarter Magic
    else:
        # Spike Cave Damage
        rom.write_byte(0x180168, 0x08)
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xE3)  # fairy
        # potion heal amount
        rom.write_byte(0x180084, 0xA0)  # full
        # potion magic restore amount
        rom.write_byte(0x180085, 0x80)  # full

    # set up game internal RNG seed
    for i in range(1024):
        rom.write_byte(0x178000 + i, random.randint(0, 255))

    # shuffle prize packs
    prizes = [0xD8, 0xD8, 0xD8, 0xD8, 0xD9, 0xD8, 0xD8, 0xD9, 0xDA, 0xD9, 0xDA, 0xDB, 0xDA, 0xD9, 0xDA, 0xDA, 0xE0, 0xDF, 0xDF, 0xDA, 0xE0, 0xDF, 0xD8, 0xDF,
              0xDC, 0xDC, 0xDC, 0xDD, 0xDC, 0xDC, 0xDE, 0xDC, 0xE1, 0xD8, 0xE1, 0xE2, 0xE1, 0xD8, 0xE1, 0xE2, 0xDF, 0xD9, 0xD8, 0xE1, 0xDF, 0xDC, 0xD9, 0xD8,
              0xD8, 0xE3, 0xE0, 0xDB, 0xDE, 0xD8, 0xDB, 0xE2, 0xD9, 0xDA, 0xDB, 0xD9, 0xDB, 0xD9, 0xDB]
    random.shuffle(prizes)

    # write tree pull prizes
    rom.write_byte(0xEFBD4, prizes.pop())
    rom.write_byte(0xEFBD5, prizes.pop())
    rom.write_byte(0xEFBD6, prizes.pop())

    # rupee crab prizes
    rom.write_byte(0x329C8, prizes.pop())  # first prize
    rom.write_byte(0x329C4, prizes.pop())  # final prize

    # stunned enemy prize
    rom.write_byte(0x37993, prizes.pop())

    # saved fish prize
    rom.write_byte(0xE82CC, prizes.pop())

    # fill enemy prize packs
    rom.write_bytes(0x37A78, prizes)

    # prize pack drop chances
    if world.difficulty == 'hard':
        droprates = [0x01, 0x02, 0x03, 0x03, 0x03, 0x04, 0x04]  # 50%, 25%, 3* 12.5%, 2* 6.25%
    else:
        droprates = [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]  # 50%

    random.shuffle(droprates)
    rom.write_bytes(0x37A62, droprates)

    vanilla_prize_pack_assignment = [131, 150, 132, 128, 128, 128, 128, 128, 2, 0, 2, 128, 160, 131, 151, 128, 128, 148, 145, 7, 0, 128, 0, 128, 146, 150, 128, 160, 0, 0, 0, 128, 4, 128,
                                     130, 6, 6, 0, 0, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 128, 128, 144, 128, 145, 145,
                                     145, 151, 145, 149, 149, 147, 151, 20, 145, 146, 129, 130, 130, 128, 133, 128, 128, 128, 4, 4, 128, 145, 128, 128, 128, 128, 128, 128, 128, 128, 0, 128,
                                     128, 130, 138, 128, 128, 128, 128, 146, 145, 128, 130, 129, 129, 128, 129, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 151, 128, 128, 128, 128, 194,
                                     128, 21, 21, 23, 6, 0, 128, 0, 192, 19, 64, 0, 2, 6, 16, 20, 0, 0, 64, 0, 0, 0, 0, 19, 70, 17, 128, 128, 0, 0, 0, 16, 0, 0, 0, 22, 22, 22, 129, 135, 130,
                                     0, 128, 128, 0, 0, 0, 0, 128, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 0, 0, 23, 0, 18, 0, 0, 0, 0, 0, 16, 23, 0, 64, 1, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 0, 0, 0, 0, 0]

    # shuffle enemies to prize packs
    for i in range(243):
        if vanilla_prize_pack_assignment[i] & 0x0F != 0x00:
            rom.write_byte(0x6B632 + i, (vanilla_prize_pack_assignment[i] & 0xF0) | random.randint(1, 7))

    # set bonk prizes
    if world.shuffle_bonk_prizes:
        bonk_prizes = [0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xAC, 0xE3, 0xE3, 0xDA, 0xE3, 0xDA, 0xD8, 0xAC, 0xAC, 0xE3, 0xD8, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xDC, 0xDB, 0xE3, 0xDA, 0x79, 0x79, 0xE3, 0xE3,
                       0xDA, 0x79, 0xAC, 0xAC, 0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xE3, 0x79, 0xDE, 0xE3, 0xAC, 0xDB, 0x79, 0xE3, 0xD8, 0xAC, 0x79, 0xE3, 0xDB, 0xDB, 0xE3, 0xE3, 0x79, 0xD8, 0xDD]
        bonk_addresses = [0x4CF6C, 0x4CFBA, 0x4CFE0, 0x4CFFB, 0x4D018, 0x4D01B, 0x4D028, 0x4D03C, 0x4D059, 0x4D07A, 0x4D09E, 0x4D0A8, 0x4D0AB, 0x4D0AE, 0x4D0BE, 0x4D0DD,
                          0x4D16A, 0x4D1E5, 0x4D1EE, 0x4D20B, 0x4CBBF, 0x4CBBF, 0x4CC17, 0x4CC1A, 0x4CC4A, 0x4CC4D, 0x4CC53, 0x4CC69, 0x4CC6F, 0x4CC7C, 0x4CCEF, 0x4CD51,
                          0x4CDC0, 0x4CDC3, 0x4CDC6, 0x4CE37, 0x4D2DE, 0x4D32F, 0x4D355, 0x4D367, 0x4D384, 0x4D387, 0x4D397, 0x4D39E, 0x4D3AB, 0x4D3AE, 0x4D3D1, 0x4D3D7,
                          0x4D3F8, 0x4D416, 0x4D420, 0x4D423, 0x4D42D, 0x4D449, 0x4D48C, 0x4D4D9, 0x4D4DC, 0x4D4E3, 0x4D504, 0x4D507, 0x4D55E, 0x4D56A]
        random.shuffle(bonk_prizes)
        for prize, address in zip(bonk_prizes, bonk_addresses):
            rom.write_byte(address, prize)

    # set Fountain bottle exchange items
    rom.write_byte(0x348FF, [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)])
    rom.write_byte(0x3493B, [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)])
    # set Fat Fairy Bow/Sword prizes to be disappointing
    rom.write_byte(0x34914, 0x3A)  # Bow and Arrow
    rom.write_byte(0x180028, 0x49)  # Fighter Sword
    # enable Waterfall fairy chests
    rom.write_bytes(0xE9AE, [0x14, 0x01])
    rom.write_bytes(0xE9CF, [0x14, 0x01])
    rom.write_bytes(0x1F714, [225, 0, 16, 172, 13, 41, 154, 1, 88, 152, 15, 17, 177, 97, 252, 77, 129, 32, 218, 2, 44, 225, 97, 252, 190, 129, 97, 177, 98, 84, 218, 2,
                              253, 141, 131, 68, 225, 98, 253, 30, 131, 49, 165, 201, 49, 164, 105, 49, 192, 34, 77, 164, 105, 49, 198, 249, 73, 198, 249, 16, 153, 160, 92, 153,
                              162, 11, 152, 96, 13, 232, 192, 85, 232, 192, 11, 146, 0, 115, 152, 96, 254, 105, 0, 152, 163, 97, 254, 107, 129, 254, 171, 133, 169, 200, 97, 254,
                              174, 129, 255, 105, 2, 216, 163, 98, 255, 107, 131, 255, 43, 135, 201, 200, 98, 255, 46, 131, 254, 161, 0, 170, 33, 97, 254, 166, 129, 255, 33, 2,
                              202, 33, 98, 255, 38, 131, 187, 35, 250, 195, 35, 250, 187, 43, 250, 195, 43, 250, 187, 83, 250, 195, 83, 250, 176, 160, 61, 152, 19, 192, 152, 82,
                              192, 136, 0, 96, 144, 0, 96, 232, 0, 96, 240, 0, 96, 152, 202, 192, 216, 202, 192, 216, 19, 192, 216, 82, 192, 252, 189, 133, 253, 29, 135, 255,
                              255, 255, 255, 240, 255, 128, 46, 97, 14, 129, 14, 255, 255])
    # set Waterfall fairy prizes to be disappointing
    rom.write_byte(0x348DB, 0x3A)  # Red Boomerang becomes Red Boomerang
    rom.write_byte(0x348EB, 0x05)  # Blue Shield becomes Blue Shield

    # set swordless mode settings
    rom.write_byte(0x18003F, 0x01 if world.mode == 'swordless' else 0x00)  # hammer can harm ganon
    rom.write_byte(0x180040, 0x01 if world.mode == 'swordless' else 0x00)  # open curtains
    rom.write_byte(0x180041, 0x01 if world.mode == 'swordless' else 0x00)  # swordless medallions
    rom.write_byte(0x180043, 0xFF if world.mode == 'swordless' else 0x00)  # starting sword for link
    rom.write_byte(0x180044, 0x01 if world.mode == 'swordless' else 0x00)  # hammer activates tablets

    # set up clocks for timed modes
    if world.clock_mode == 'off':
        rom.write_bytes(0x180190, [0x00, 0x00, 0x00])  # turn off clock mode
        rom.write_bytes(0x180200, [0x00, 0x00, 0x00, 0x00])  # red clock adjustment time (in frames, sint32)
        rom.write_bytes(0x180204, [0x00, 0x00, 0x00, 0x00])  # blue clock adjustment time (in frames, sint32)
        rom.write_bytes(0x180208, [0x00, 0x00, 0x00, 0x00])  # green clock adjustment time (in frames, sint32)
        rom.write_bytes(0x18020C, [0x00, 0x00, 0x00, 0x00])  # starting time (in frames, sint32)
    elif world.clock_mode == 'ohko':
        rom.write_bytes(0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
        rom.write_bytes(0x180200, [0x00, 0x00, 0x00, 0x00])  # red clock adjustment time (in frames, sint32)
        rom.write_bytes(0x180204, [0x00, 0x00, 0x00, 0x00])  # blue clock adjustment time (in frames, sint32)
        rom.write_bytes(0x180208, [0x50, 0x46, 0x00, 0x00])  # green clock adjustment time (in frames, sint32)
        rom.write_bytes(0x18020C, [0xA0, 0x8C, 0x00, 0x00])  # starting time (in frames, sint32)
    if world.clock_mode == 'stopwatch':
        rom.write_bytes(0x180190, [0x02, 0x01, 0x00])  # set stopwatch mode
        rom.write_bytes(0x180200, [0xE0, 0xE3, 0xFF, 0xFF])  # red clock adjustment time (in frames, sint32)
        rom.write_bytes(0x180204, [0x20, 0x1C, 0x00, 0x00])  # blue clock adjustment time (in frames, sint32)
        rom.write_bytes(0x180208, [0x40, 0x38, 0x00, 0x00])  # green clock adjustment time (in frames, sint32)
        rom.write_bytes(0x18020C, [0x00, 0x00, 0x00, 0x00])  # starting time (in frames, sint32)
    if world.clock_mode == 'countdown':
        rom.write_bytes(0x180190, [0x01, 0x01, 0x00])  # set countdown, with no reset available
        rom.write_bytes(0x180200, [0xE0, 0xE3, 0xFF, 0xFF])  # red clock adjustment time (in frames, sint32)
        rom.write_bytes(0x180204, [0x20, 0x1C, 0x00, 0x00])  # blue clock adjustment time (in frames, sint32)
        rom.write_bytes(0x180208, [0x40, 0x38, 0x00, 0x00])  # green clock adjustment time (in frames, sint32)
        rom.write_bytes(0x18020C, [0x80, 0x32, 0x02, 0x00])  # starting time (in frames, sint32)

    # set up goals for treasure hunt
    rom.write_bytes(0x180165, [0x0E, 0x28] if world.treasure_hunt_icon == 'Triforce Piece' else [0x0D, 0x28])
    rom.write_byte(0x180167, world.treasure_hunt_count % 256)

    # assorted fixes
    rom.write_byte(0x180030, 0x00)  # Disable SRAM trace
    rom.write_byte(0x180036, 0x0A)  # Rupoor negative value
    rom.write_byte(0x180169, 0x01 if world.lock_aga_door_in_escape else 0x00)  # Lock or unlock aga tower door during escape sequence.
    rom.write_byte(0x180170, 0x01 if world.ganon_at_pyramid else 0x00)  # Enable respawning on pyramid after ganon death
    rom.write_byte(0x180086, 0x00 if world.aga_randomness else 0x01)  # set blue ball and ganon warp randomness
    rom.write_byte(0x1800A1, 0x01)  # enable overworld screen transition draining for water level inside swamp
    if world.goal in ['ganon']:
        rom.write_byte(0x18003E, 0x03)  # make ganon invincible until all crystals and aga 2 are collected
    elif world.goal in ['pedestal', 'triforcehunt']:
        rom.write_byte(0x18003E, 0x01)  # make ganon invincible
    elif world.goal in ['dungeons']:
        rom.write_byte(0x18003E, 0x02)  # make ganon invincible until all dungeons are beat
    elif world.goal in ['crystals']:
        rom.write_byte(0x18003E, 0x04)  # make ganon invincible until all crystals
    rom.write_byte(0x18016A, 0x01 if world.keysanity else 0x00)  # free roaming item text boxes
    rom.write_byte(0x18003B, 0x01 if world.keysanity else 0x00)  # maps showing crystals on overworld
    
    # compasses showing dungeon count
    if world.clock_mode != 'off':
        rom.write_byte(0x18003C, 0x00) #Currently must be off if timer is on, because they use same HUD location
    elif world.keysanity:
        rom.write_byte(0x18003C, 0x01) #show on pickup
    else:
        rom.write_byte(0x18003C, 0x00)
        
    rom.write_byte(0x180045, 0x01 if world.keysanity else 0x00)  # free roaming items in menu
    digging_game_rng = random.randint(1, 30)  # set rng for digging game
    rom.write_byte(0x180020, digging_game_rng)
    rom.write_byte(0xEFD95, digging_game_rng)
    rom.write_byte(0x1800A3, 0x01)  # enable correct world setting behaviour after agahnim kills
    rom.write_byte(0x180042, 0x01 if world.save_and_quite_from_boss else 0x00)  # Allow Save and Quite after boss kill

    # remove shield from uncle
    rom.write_bytes(0x6D253, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D25B, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D283, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D28B, [0x00, 0x00, 0xf7, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D2CB, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
    rom.write_bytes(0x6D2FB, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
    rom.write_bytes(0x6D313, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])

    if world.swamp_patch_required:
        # patch swamp: Need to enable permanent drain of water as dam or swamp were moved
        rom.write_byte(0x18003D, 0x01)

    # set correct flag for hera basement item
    if world.get_location('[dungeon-L3-1F] Tower of Hera - Freestanding Key').item is not None and world.get_location('[dungeon-L3-1F] Tower of Hera - Freestanding Key').item.name == 'Small Key (Tower of Hera)':
        rom.write_byte(0x4E3BB, 0xE4)
    else:
        rom.write_byte(0x4E3BB, 0xEB)

    # fix trock doors for reverse entrances
    if world.fix_trock_doors:
        rom.write_byte(0xFED31, 0x0E)  # preopen bombable exit
        rom.write_byte(0xFEE41, 0x0E)  # preopen bombable exit
        rom.write_byte(0xFE465, 0x1E)  # remove small key door on backside of big key door

    # Thanks to Zarby89 for finding these values
    # fix skull woods exit point
    if world.fix_skullwoods_exit:
        rom.write_byte(0x15E0D, 0xF8)

    # fix palace of darkness exit point
    if world.fix_palaceofdarkness_exit:
        rom.write_byte(0x15E03, 0x40)

    # fix turtle rock exit point
    if world.fix_trock_exit:
        rom.write_byte(0x15E1D, 0x34)

    # fix ganons tower exit point
    if world.fix_gtower_exit:
        rom.write_byte(0x15E25, 0xA4)
        # todo fix screen scrolling

    #enable instant item menu
    if world.fastmenu: 
        rom.write_byte(0x180048, 0x01)
        # Sound twekas for fastmenu:
        rom.write_byte(0x6DD9A, 0x20)
        rom.write_byte(0x6DF2A, 0x20)
        rom.write_byte(0x6E0E9, 0x20)
    
    # enable quick item swapping with L and R (ported by Amazing Ampharos)
    if world.quickswap:
        rom.write_bytes(0x107fb, [0x22, 0x50, 0xFF, 0x1F])
        rom.write_bytes(0x12451, [0x22, 0x50, 0xFF, 0x1F])
        rom.write_bytes(0xfff50, [0x20, 0x58, 0xFF, 0xA5, 0xF6, 0x29, 0x40, 0x6B, 0xA5, 0xF6, 0x89, 0x10, 0xF0, 0x03, 0x4C, 0x69,
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
    rom.write_bytes(0x7FC0, bytearray('ER_047_%09d_' % world.seed, 'utf8') + world.option_identifier.to_bytes(4, 'big'))

    # set heart beep rate
    rom.write_byte(0x180033, {'off': 0x00, 'half': 0x40, 'quarter': 0x80, 'normal': 0x20}[beep])

    # store hash table for main menu hash
    rom.write_bytes(0x187F00, hashtable)

    # write link sprite if required
    if sprite is not None:
        write_sprite(rom, sprite)

    if isinstance(rom, LocalRom):
        rom.write_crc()

    return rom


def write_sprite(rom, sprite):
    if len(sprite) == 0x7000:
        # sprite file with graphics and without palette data
        rom.write_bytes(0x80000, sprite[:0x7000])
    elif len(sprite) == 0x7078:
        # sprite file with graphics and palette data
        rom.write_bytes(0x80000, sprite[:0x7000])
        rom.write_bytes(0xDD308, sprite[0x7000:])
        rom.write_bytes(0xDEDF5, sprite[0x7036:0x7038])
        rom.write_bytes(0xDEDF7, sprite[0x7054:0x7056])
    elif len(sprite) in [0x100000, 0x200000]:
        # full rom with patched sprite, extract it
        rom.write_bytes(0x80000, sprite[0x80000:0x87000])
        rom.write_bytes(0xDD308, sprite[0xDD308:0xDD380])
        rom.write_bytes(0xDEDF5, sprite[0xDEDF5:0xDEDF9])


def write_string_to_rom(rom, target, string):
    address, maxbytes = text_addresses[target]
    rom.write_bytes(address, string_to_alttp_text(string, maxbytes))


def write_credits_string_to_rom(rom, target, string):
    address, length = credits_addresses[target]
    rom.write_bytes(address, string_to_credits(string, length))


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
    if world.goal in ['pedestal', 'triforcehunt']:
        write_string_to_rom(rom, 'Ganon1Invincible', 'Why are you even here?\n You can\'t even hurt me!')
        write_string_to_rom(rom, 'Ganon2Invincible', 'Seriously? Go Away, I will not Die.')
    else:
        write_string_to_rom(rom, 'Ganon1', Ganon1_texts[random.randint(0, len(Ganon1_texts) - 1)])
        write_string_to_rom(rom, 'Ganon1Invincible', 'You cannot defeat me until you finish your goal!')
        write_string_to_rom(rom, 'Ganon2Invincible', 'Got wax in\nyour ears?\nI can not die!')
    write_string_to_rom(rom, 'TavernMan', TavernMan_texts[random.randint(0, len(TavernMan_texts) - 1)])

    altaritem = world.get_location('Altar').item
    altar_text = 'Some Hot Air' if altaritem is None else altaritem.altar_hint_text if altaritem.altar_hint_text is not None else 'Unknown Item'
    write_string_to_rom(rom, 'Altar', altar_text)
    altar_credit_text = 'and the Hot Air' if altaritem is None else altaritem.altar_credit_text if altaritem.altar_credit_text is not None else 'and the Unknown Item'
    write_credits_string_to_rom(rom, 'Altar', altar_credit_text)

    etheritem = world.get_location('Ether Tablet').item
    ether_text = 'Some Hot Air' if etheritem is None else etheritem.altar_hint_text if etheritem.altar_hint_text is not None else 'Unknown Item'
    write_string_to_rom(rom, 'EtherTablet', ether_text)
    bombositem = world.get_location('Bombos Tablet').item
    bombos_text = 'Some Hot Air' if bombositem is None else bombositem.altar_hint_text if bombositem.altar_hint_text is not None else 'Unknown Item'
    write_string_to_rom(rom, 'BombosTablet', bombos_text)

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
