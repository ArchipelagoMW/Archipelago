import io
import json
import hashlib
import logging
import os
import struct
import random

from Dungeons import dungeon_music_addresses
from Text import string_to_alttp_text, text_addresses, Credits
from Text import Uncle_texts, Ganon1_texts, PyramidFairy_texts, TavernMan_texts, Sahasrahla2_texts, Triforce_texts, Blind_texts, BombShop2_texts
from Text import KingsReturn_texts, Sanctuary_texts, Kakariko_texts, Blacksmiths_texts, DeathMountain_texts, LostWoods_texts, WishingWell_texts, DesertPalace_texts, MountainTower_texts, LinksHouse_texts, Lumberjacks_texts, SickKid_texts, FluteBoy_texts, Zora_texts, MagicShop_texts, Sahasrahla_names
from Utils import local_path
from Items import ItemFactory


JAP10HASH = '03a63945398191337e896e5771f77173'
RANDOMIZERBASEHASH = 'dc5840f0d1ef7b51009c5625a054b3dd'


class JsonRom(object):

    def __init__(self):
        self.patches = {}

    def write_byte(self, address, value):
        self.patches[str(address)] = [value]

    def write_bytes(self, startaddress, values):
        self.patches[str(startaddress)] = list(values)

    def write_int16_to_rom(self, address, value):
        self.write_bytes(address, int16_as_bytes(value))

    def write_int32_to_rom(self, address, value):
        self.write_bytes(address, int32_as_bytes(value))

    def write_to_file(self, file):
        with open(file, 'w') as stream:
            json.dump([self.patches], stream)


class LocalRom(object):

    def __init__(self, file, patch=True):
        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        if patch:
            self.patch_base_rom()

    def write_byte(self, address, value):
        self.buffer[address] = value

    def write_bytes(self, startaddress, values):
        for i, value in enumerate(values):
            self.write_byte(startaddress + i, value)

    def write_int16_to_rom(self, address, value):
        self.write_bytes(address, int16_as_bytes(value))

    def write_int32_to_rom(self, address, value):
        self.write_bytes(address, int32_as_bytes(value))

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def patch_base_rom(self):
        # verify correct checksum of baserom
        basemd5 = hashlib.md5()
        basemd5.update(self.buffer)
        if JAP10HASH != basemd5.hexdigest():
            logging.getLogger('').warning('Supplied Base Rom does not match known MD5 for JAP(1.0) release. Will try to patch anyway.')

        # extend to 2MB
        self.buffer.extend(bytearray([0x00] * (2097152 - len(self.buffer))))

        # load randomizer patches
        with open(local_path('data/base2current.json'), 'r') as stream:
            patches = json.load(stream)
        for patch in patches:
            if isinstance(patch, dict):
                for baseaddress, values in patch.items():
                    self.write_bytes(int(baseaddress), values)

        # verify md5
        patchedmd5 = hashlib.md5()
        patchedmd5.update(self.buffer)
        if RANDOMIZERBASEHASH != patchedmd5.hexdigest():
            raise RuntimeError('Provided Base Rom unsuitable for patching. Please provide a JAP(1.0) "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc" rom to use as a base.')

    def write_crc(self):
        crc = (sum(self.buffer[:0x7FDC] + self.buffer[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])

def read_rom(stream):
    "Reads rom into bytearray and strips off any smc header"
    buffer = bytearray(stream.read())
    if len(buffer)%0x400 == 0x200:
        buffer = buffer[0x200:]
    return buffer

class Sprite(object):
    default_palette = [255, 127, 126, 35, 183, 17, 158, 54, 165, 20, 255, 1, 120, 16, 157,
                       89, 71, 54, 104, 59, 74, 10, 239, 18, 92, 42, 113, 21, 24, 122,
                       255, 127, 126, 35, 183, 17, 158, 54, 165, 20, 255, 1, 120, 16, 157,
                       89, 128, 105, 145, 118, 184, 38, 127, 67, 92, 42, 153, 17, 24, 122,
                       255, 127, 126, 35, 183, 17, 158, 54, 165, 20, 255, 1, 120, 16, 157,
                       89, 87, 16, 126, 69, 243, 109, 185, 126, 92, 42, 39, 34, 24, 122,
                       255, 127, 126, 35, 218, 17, 158, 54, 165, 20, 255, 1, 120, 16, 151,
                       61, 71, 54, 104, 59, 74, 10, 239, 18, 126, 86, 114, 24, 24, 122]

    default_glove_palette = [246, 82, 118, 3]

    def __init__(self, filename):
        with open(filename, 'rb') as file:
            filedata = bytearray(file.read())
        self.name = os.path.basename(filename)
        self.author_name = None
        self.valid = True
        if len(filedata) == 0x7000:
            # sprite file with graphics and without palette data
            self.sprite = filedata[:0x7000]
            self.palette = list(self.default_palette)
            self.glove_palette = list(self.default_glove_palette)
        elif len(filedata) == 0x7078:
            # sprite file with graphics and palette data
            self.sprite = filedata[:0x7000]
            self.palette = filedata[0x7000:]
            self.glove_palette = filedata[0x7036:0x7038] + filedata[0x7054:0x7056]
        elif len(filedata) == 0x707C:
            # sprite file with graphics and palette data including gloves
            self.sprite = filedata[:0x7000]
            self.palette = filedata[0x7000:0x7078]
            self.glove_palette = filedata[0x7078:]
        elif len(filedata) in [0x100000, 0x200000]:
            # full rom with patched sprite, extract it
            self.sprite = filedata[0x80000:0x87000]
            self.palette = filedata[0xDD308:0xDD380]
            self.glove_palette = filedata[0xDEDF5:0xDEDF9]
        elif filedata.startswith(b'ZSPR'):
            result = self.parse_zspr(filedata, 1)
            if result is None:
                self.valid = False
                return
            (sprite, palette, self.name, self.author_name) = result
            if len(sprite) != 0x7000:
                self.valid = False
                return
            self.sprite = sprite
            if len(palette) == 0:
                self.palette = list(self.default_palette)
                self.glove_palette = list(self.default_glove_palette)
            elif len(palette) == 0x78:
                self.palette = palette
                self.glove_palette = list(self.default_glove_palette)
            elif len(palette) == 0x7C:
                self.palette = palette[:0x78]
                self.glove_palette = palette[0x78:]
            else:
                self.valid = False
        else:
            self.valid = False

    @staticmethod
    def default_link_sprite():
        return Sprite(local_path('data/default.zspr'))

    def decode8(self, pos):
        arr = [[0 for _ in range(8)] for _ in range(8)]
        for y in range(8):
            for x in range(8):
                position = 1<<(7-x)
                val = 0
                if self.sprite[pos+2*y] & position:
                    val += 1
                if self.sprite[pos+2*y+1] & position:
                    val += 2
                if self.sprite[pos+2*y+16] & position:
                    val += 4
                if self.sprite[pos+2*y+17] & position:
                    val += 8
                arr[y][x] = val
        return arr

    def decode16(self, pos):
        arr = [[0 for _ in range(16)] for _ in range(16)]
        top_left = self.decode8(pos)
        top_right = self.decode8(pos+0x20)
        bottom_left = self.decode8(pos+0x200)
        bottom_right = self.decode8(pos+0x220)
        for x in range(8):
            for y in range(8):
                arr[y][x] = top_left[y][x]
                arr[y][x+8] = top_right[y][x]
                arr[y+8][x] = bottom_left[y][x]
                arr[y+8][x+8] = bottom_right[y][x]
        return arr

    def parse_zspr(self, filedata, expected_kind):
        logger = logging.getLogger('')
        headerstr = "<4xBHHIHIHH6x"
        headersize = struct.calcsize(headerstr)
        if len(filedata) < headersize:
            return None
        (version, csum, icsum, sprite_offset, sprite_size, palette_offset, palette_size, kind) = struct.unpack_from(headerstr, filedata)
        if version not in [1]:
            logger.error('Error parsing ZSPR file: Version %g not supported', version)
            return None
        if kind != expected_kind:
            return None

        stream = io.BytesIO(filedata)
        stream.seek(headersize)

        def read_utf16le(stream):
            "Decodes a null-terminated UTF-16_LE string of unknown size from a stream"
            raw = bytearray()
            while True:
                char = stream.read(2)
                if char in [b'', b'\x00\x00']:
                    break
                raw += char
            return raw.decode('utf-16_le')

        sprite_name = read_utf16le(stream)
        author_name = read_utf16le(stream)

        # Ignoring the Author Rom name for the time being.

        real_csum = sum(filedata) % 0x10000
        if real_csum != csum or real_csum ^ 0xFFFF != icsum:
            logger.warning('ZSPR file has incorrect checksum. It may be corrupted.')

        sprite = filedata[sprite_offset:sprite_offset + sprite_size]
        palette = filedata[palette_offset:palette_offset + palette_size]

        if len(sprite) != sprite_size or len(palette) != palette_size:
            logger.error('Error parsing ZSPR file: Unexpected end of file')
            return None

        return (sprite, palette, sprite_name, author_name)

    def decode_palette(self):
        "Returns the palettes as an array of arrays of 15 colors"
        def array_chunk(arr, size):
            return list(zip(*[iter(arr)] * size))
        def make_int16(pair):
            return pair[1]<<8 | pair[0]
        def expand_color(i):
            return ((i & 0x1F) * 8, (i>>5 & 0x1F) * 8, (i>>10 & 0x1F) * 8)
        raw_palette = self.palette
        if raw_palette is None:
            raw_palette = Sprite.default_palette
        # turn palette data into a list of RGB tuples with 8 bit values
        palette_as_colors = [expand_color(make_int16(chnk)) for chnk in array_chunk(raw_palette, 2)]

        # split into palettes of 15 colors
        return array_chunk(palette_as_colors, 15)


def int16_as_bytes(value):
    value = value & 0xFFFF
    return [value & 0xFF, (value >> 8) & 0xFF]

def int32_as_bytes(value):
    value = value & 0xFFFFFFFF
    return [value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF]

def patch_rom(world, rom, hashtable, beep='normal', color='red', sprite=None):
    # patch items
    for location in world.get_locations():
        itemid = location.item.code if location.item is not None else 0x5A

        if itemid is None or location.address is None:
            continue

        locationaddress = location.address
        if not location.crystal:
            # Keys in their native dungeon should use the orignal item code for keys
            if location.parent_region.dungeon:
                dungeon = location.parent_region.dungeon
                if location.item is not None and location.item.key and dungeon.is_dungeon_item(location.item):
                    if location.item.type == "BigKey":
                        itemid = 0x32
                    if location.item.type == "SmallKey":
                        itemid = 0x24
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
        rom.write_byte(0x155C9, random.choice([0x11, 0x16]))  # Randomize GT music too in keysanity mode

    # patch entrance/exits/holes
    for region in world.regions:
        for exit in region.exits:
            if exit.target is not None:
                if isinstance(exit.addresses, tuple):
                    offset = exit.target
                    room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2 = exit.addresses
                    #room id is deliberately not written


                    rom.write_byte(0x15B8C + offset, ow_area)
                    rom.write_int16_to_rom(0x15BDB + 2 * offset, vram_loc)
                    rom.write_int16_to_rom(0x15C79 + 2 * offset, scroll_y)
                    rom.write_int16_to_rom(0x15D17 + 2 * offset, scroll_x)

                    # for positioning fixups we abuse the roomid as a way of identifying which exit data we are appling
                    # Thanks to Zarby89 for originally finding these values
                    # todo fix screen scrolling

                    if world.shuffle not in ['insanity', 'insanity_legacy', 'madness_legacy'] and \
                        exit.name in ['Eastern Palace Exit', 'Tower of Hera Exit', 'Thieves Town Exit', 'Skull Woods Final Section Exit', 'Ice Palace Exit', 'Misery Mire Exit',
                                      'Palace of Darkness Exit', 'Swamp Palace Exit', 'Ganons Tower Exit', 'Desert Palace Exit (North)', 'Agahnims Tower Exit', 'Spiral Cave Exit (Top)',
                                      'Superbunny Cave Exit (Bottom)', 'Turtle Rock Ledge Exit (East)']:
                        # For exits that connot be reached from another, no need to apply offset fixes.
                        rom.write_int16_to_rom(0x15DB5 + 2 * offset, link_y) # same as final else
                    elif room_id == 0x0059 and world.fix_skullwoods_exit:
                        rom.write_int16_to_rom(0x15DB5 + 2 * offset, 0x00F8)
                    elif room_id == 0x004a and world.fix_palaceofdarkness_exit:
                        rom.write_int16_to_rom(0x15DB5 + 2 * offset, 0x0640)
                    elif room_id == 0x00d6 and world.fix_trock_exit:
                        rom.write_int16_to_rom(0x15DB5 + 2 * offset, 0x0134)
                    elif room_id == 0x000c and world.fix_gtower_exit: # fix ganons tower exit point
                        rom.write_int16_to_rom(0x15DB5 + 2 * offset, 0x00A4)
                    else:
                        rom.write_int16_to_rom(0x15DB5 + 2 * offset, link_y)

                    rom.write_int16_to_rom(0x15E53 + 2 * offset, link_x)
                    rom.write_int16_to_rom(0x15EF1 + 2 * offset, camera_y)
                    rom.write_int16_to_rom(0x15F8F + 2 * offset, camera_x)
                    rom.write_byte(0x1602D + offset, unknown_1)
                    rom.write_byte(0x1607C + offset, unknown_2)
                    rom.write_int16_to_rom(0x160CB + 2 * offset, door_1)
                    rom.write_int16_to_rom(0x16169 + 2 * offset, door_2)
                elif isinstance(exit.addresses, list):
                    # is hole
                    for address in exit.addresses:
                        rom.write_byte(address, exit.target)
                else:
                    # patch door table
                    rom.write_byte(0xDBB73 + exit.addresses, exit.target)


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

    GREEN_TWENTY_RUPEES = 0x47
    TRIFORCE_PIECE = ItemFactory('Triforce Piece').code
    GREEN_CLOCK = ItemFactory('Green Clock').code

    rom.write_byte(0x18004F, 0x01) # Byrna Invulnerability: on
    # handle difficulty
    if world.difficulty == 'hard':
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xD8)  # One Heart
        # potion heal amount
        rom.write_byte(0x180084, 0x28)  # Five Hearts
        # potion magic restore amount
        rom.write_byte(0x180085, 0x40)  # Half Magic
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x02, 0x02])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        #Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        rom.write_int16_to_rom(0x180036, world.rupoor_cost)
        #Make Blue Shield more expensive
        rom.write_bytes(0xF73D2, [0xFC, 0xFF])
        rom.write_bytes(0xF73DA, [0x04, 0x00])
        rom.write_bytes(0xF73E2, [0x0C, 0x00])
        rom.write_byte(0xF73D6, 0x31)
        rom.write_byte(0xF73DE, 0x30)
        rom.write_byte(0xF73E6, 0x30)
        rom.write_byte(0xF7201, 0x00)
        rom.write_byte(0xF71FF, 0x64)
        #Make Red Shield more expensive
        rom.write_bytes(0xF73FA, [0xFC, 0xFF])
        rom.write_bytes(0xF7402, [0x04, 0x00])
        rom.write_bytes(0xF740A, [0x0C, 0x00])
        rom.write_byte(0xF73FE, 0x33)
        rom.write_byte(0xF7406, 0x33)
        rom.write_byte(0xF740E, 0x33)
        rom.write_byte(0xF7241, 0x03)
        rom.write_byte(0xF723F, 0xE7)
    elif world.difficulty == 'expert':
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0x79)  # Bees
        # potion heal amount
        rom.write_byte(0x180084, 0x08)  # One Heart
        # potion magic restore amount
        rom.write_byte(0x180085, 0x20)  # Quarter Magic
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x02, 0x02])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        #Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        rom.write_int16_to_rom(0x180036, 20)
        #Make Blue Shield more expensive
        rom.write_bytes(0xF73D2, [0xFC, 0xFF])
        rom.write_bytes(0xF73DA, [0x04, 0x00])
        rom.write_bytes(0xF73E2, [0x0C, 0x00])
        rom.write_byte(0xF73D6, 0x3C)
        rom.write_byte(0xF73DE, 0x3C)
        rom.write_byte(0xF73E6, 0x3C)
        rom.write_byte(0xF7201, 0x27)
        rom.write_byte(0xF71FF, 0x06)
        #Make Red Shield more expensive
        rom.write_bytes(0xF73FA, [0xFC, 0xFF])
        rom.write_bytes(0xF7402, [0x04, 0x00])
        rom.write_bytes(0xF740A, [0x0C, 0x00])
        rom.write_byte(0xF73FE, 0x3C)
        rom.write_byte(0xF7406, 0x3C)
        rom.write_byte(0xF740E, 0x3C)
        rom.write_byte(0xF7241, 0x27)
        rom.write_byte(0xF723F, 0x06)
    elif world.difficulty == 'insane':
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0x79)  # Bees
        # potion heal amount
        rom.write_byte(0x180084, 0x00)  # No healing
        # potion magic restore amount
        rom.write_byte(0x180085, 0x00)  # No healing
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x02, 0x02])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        #Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        rom.write_int16_to_rom(0x180036, 9999)
        #Make Blue Shield more expensive
        rom.write_bytes(0xF73D2, [0xFC, 0xFF])
        rom.write_bytes(0xF73DA, [0x04, 0x00])
        rom.write_bytes(0xF73E2, [0x0C, 0x00])
        rom.write_byte(0xF73D6, 0x3C)
        rom.write_byte(0xF73DE, 0x3C)
        rom.write_byte(0xF73E6, 0x3C)
        rom.write_byte(0xF7201, 0x27)
        rom.write_byte(0xF71FF, 0x10)
        #Make Red Shield more expensive
        rom.write_bytes(0xF73FA, [0xFC, 0xFF])
        rom.write_bytes(0xF7402, [0x04, 0x00])
        rom.write_bytes(0xF740A, [0x0C, 0x00])
        rom.write_byte(0xF73FE, 0x3C)
        rom.write_byte(0xF7406, 0x3C)
        rom.write_byte(0xF740E, 0x3C)
        rom.write_byte(0xF7241, 0x27)
        rom.write_byte(0xF723F, 0x10)
    else:
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xE3)  # fairy
        # potion heal amount
        rom.write_byte(0x180084, 0xA0)  # full
        # potion magic restore amount
        rom.write_byte(0x180085, 0x80)  # full
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x04, 0x08, 0x10])
        # Byrna Invulnerability: on
        rom.write_byte(0x18004F, 0x01)
        #Enable catching fairies
        rom.write_byte(0x34FD6, 0xF0)
        #Set overflow items for progressive equipment
        if world.goal == 'triforcehunt':
            overflow_replacement = TRIFORCE_PIECE
        elif world.timer in ['timed', 'timed-countdown', 'timed-ohko']:
            overflow_replacement = GREEN_CLOCK
        else:
            overflow_replacement = GREEN_TWENTY_RUPEES

    #Byrna residual magic cost
    rom.write_bytes(0x45C42, [0x04, 0x02, 0x01])

    difficulty = world.difficulty_requirements
    #Set overflow items for progressive equipment
    rom.write_bytes(0x180090,
                    [difficulty.progressive_sword_limit, overflow_replacement,
                     difficulty.progressive_shield_limit, overflow_replacement,
                     difficulty.progressive_armor_limit, overflow_replacement,
                     difficulty.progressive_bottle_limit, overflow_replacement])

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
    if world.difficulty in ['hard', 'expert', 'insane']:
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
    bonk_prizes = [0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xAC, 0xE3, 0xE3, 0xDA, 0xE3, 0xDA, 0xD8, 0xAC, 0xAC, 0xE3, 0xD8, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xDC, 0xDB, 0xE3, 0xDA, 0x79, 0x79, 0xE3, 0xE3,
                   0xDA, 0x79, 0xAC, 0xAC, 0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xE3, 0x79, 0xDE, 0xE3, 0xAC, 0xDB, 0x79, 0xE3, 0xD8, 0xAC, 0x79, 0xE3, 0xDB, 0xDB, 0xE3, 0xE3, 0x79, 0xD8, 0xDD]
    bonk_addresses = [0x4CF6C, 0x4CFBA, 0x4CFE0, 0x4CFFB, 0x4D018, 0x4D01B, 0x4D028, 0x4D03C, 0x4D059, 0x4D07A, 0x4D09E, 0x4D0A8, 0x4D0AB, 0x4D0AE, 0x4D0BE, 0x4D0DD,
                      0x4D16A, 0x4D1E5, 0x4D1EE, 0x4D20B, 0x4CBBF, 0x4CBBF, 0x4CC17, 0x4CC1A, 0x4CC4A, 0x4CC4D, 0x4CC53, 0x4CC69, 0x4CC6F, 0x4CC7C, 0x4CCEF, 0x4CD51,
                      0x4CDC0, 0x4CDC3, 0x4CDC6, 0x4CE37, 0x4D2DE, 0x4D32F, 0x4D355, 0x4D367, 0x4D384, 0x4D387, 0x4D397, 0x4D39E, 0x4D3AB, 0x4D3AE, 0x4D3D1, 0x4D3D7,
                      0x4D3F8, 0x4D416, 0x4D420, 0x4D423, 0x4D42D, 0x4D449, 0x4D48C, 0x4D4D9, 0x4D4DC, 0x4D4E3, 0x4D504, 0x4D507, 0x4D55E, 0x4D56A]
    if world.shuffle_bonk_prizes:
        random.shuffle(bonk_prizes)
    for prize, address in zip(bonk_prizes, bonk_addresses):
        rom.write_byte(address, prize)

    # Fill in item substitutions table
    if world.difficulty in ['easy']:
        rom.write_bytes(0x184000, [
            # original_item, limit, replacement_item, filler
            0x12, 0x01, 0x35, 0xFF, # lamp -> 5 rupees
            0x58, 0x01, 0x43, 0xFF, # silver arrows -> 1 arrow
            0xFF, 0xFF, 0xFF, 0xFF, # end of table sentinel
        ])
    else:
        rom.write_bytes(0x184000, [
            # original_item, limit, replacement_item, filler
            0x12, 0x01, 0x35, 0xFF, # lamp -> 5 rupees
            0xFF, 0xFF, 0xFF, 0xFF, # end of table sentinel
        ])

    # set Fountain bottle exchange items
    if world.difficulty in ['hard', 'expert', 'insane']:
        rom.write_byte(0x348FF, [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x48][random.randint(0, 5)])
        rom.write_byte(0x3493B, [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x48][random.randint(0, 5)])
    else:
        rom.write_byte(0x348FF, [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)])
        rom.write_byte(0x3493B, [0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)])

    #enable Fat Fairy Chests
    rom.write_bytes(0x1FC16, [0xB1, 0xC6, 0xF9, 0xC9, 0xC6, 0xF9])
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

    rom.write_byte(0x180029, 0x01) # Smithy quick item give

    # set swordless mode settings
    rom.write_byte(0x18003F, 0x01 if world.mode == 'swordless' else 0x00)  # hammer can harm ganon
    rom.write_byte(0x180040, 0x01 if world.mode == 'swordless' else 0x00)  # open curtains
    rom.write_byte(0x180041, 0x01 if world.mode == 'swordless' else 0x00)  # swordless medallions
    rom.write_byte(0x180043, 0xFF if world.mode == 'swordless' else 0x00)  # starting sword for link
    rom.write_byte(0x180044, 0x01 if world.mode == 'swordless' else 0x00)  # hammer activates tablets

    # set up clocks for timed modes
    if world.shuffle == 'vanilla':
        ERtimeincrease = 0
    elif world.shuffle in ['dungeonssimple', 'dungeonsfull']:
        ERtimeincrease = 10
    else:
        ERtimeincrease = 20
    if world.keysanity:
        ERtimeincrease = ERtimeincrease + 15
    if world.clock_mode == 'off':
        rom.write_bytes(0x180190, [0x00, 0x00, 0x00])  # turn off clock mode
        rom.write_int32_to_rom(0x180200, 0)  # red clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180204, 0)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180208, 0)  # green clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x18020C, 0)  # starting time (in frames, sint32)
    elif world.clock_mode == 'ohko':
        rom.write_bytes(0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
        rom.write_int32_to_rom(0x180200, 0)  # red clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180204, 0)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180208, 0)  # green clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x18020C, 0)  # starting time (in frames, sint32)
    elif world.clock_mode == 'countdown-ohko':
        rom.write_bytes(0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
        rom.write_int32_to_rom(0x180200, -100 * 60 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        if world.difficulty == 'easy':
            rom.write_int32_to_rom(0x18020C, (20 + ERtimeincrease) * 60 * 60)  # starting time (in frames, sint32)
        elif world.difficulty == 'normal':
            rom.write_int32_to_rom(0x18020C, (10 + ERtimeincrease) * 60 * 60)  # starting time (in frames, sint32)
        else:
            rom.write_int32_to_rom(0x18020C, int((5 + ERtimeincrease / 2) * 60 * 60))  # starting time (in frames, sint32)
    if world.clock_mode == 'stopwatch':
        rom.write_bytes(0x180190, [0x02, 0x01, 0x00])  # set stopwatch mode
        rom.write_int32_to_rom(0x180200, -2 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x18020C, 0)  # starting time (in frames, sint32)
    if world.clock_mode == 'countdown':
        rom.write_bytes(0x180190, [0x01, 0x01, 0x00])  # set countdown, with no reset available
        rom.write_int32_to_rom(0x180200, -2 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        rom.write_int32_to_rom(0x18020C, (40 + ERtimeincrease) * 60 * 60)  # starting time (in frames, sint32)

    # set up goals for treasure hunt
    rom.write_bytes(0x180165, [0x0E, 0x28] if world.treasure_hunt_icon == 'Triforce Piece' else [0x0D, 0x28])
    rom.write_byte(0x180167, world.treasure_hunt_count % 256)

    # TODO: a proper race rom mode should be implemented, that changes the following flag, and rummages the table (or uses the future encryption feature, etc)
    rom.write_bytes(0x180213, [0x00, 0x01]) # Not a Tournament Seed

    rom.write_byte(0x180211, 0x06) #Game type, we set the Entrance and item randomization flags

    # assorted fixes
    rom.write_byte(0x180030, 0x00)  # Disable SRAM trace
    rom.write_byte(0x1800A2, 0x01)  # remain in real dark world when dying in dark word dungion before killing aga1
    rom.write_byte(0x180169, 0x01 if world.lock_aga_door_in_escape else 0x00)  # Lock or unlock aga tower door during escape sequence.
    rom.write_byte(0x180171, 0x01 if world.ganon_at_pyramid else 0x00)  # Enable respawning on pyramid after ganon death
    rom.write_byte(0x180173, 0x01) # Bob is enabled
    rom.write_byte(0x180168, 0x08)  # Spike Cave Damage
    rom.write_bytes(0x18016B, [0x04, 0x02, 0x01]) #Set spike cave and MM spike room Cape usage
    rom.write_bytes(0x18016E, [0x04, 0x08, 0x10]) #Set spike cave and MM spike room Cape usage
    rom.write_bytes(0x50563, [0x3F, 0x14]) # disable below ganon chest
    rom.write_byte(0x50599, 0x00) # disable below ganon chest
    rom.write_bytes(0xE9A5, [0x7E, 0x00, 0x24]) # disable below ganon chest
    rom.write_byte(0xF5D73, 0xF0) # bees are catchable
    rom.write_byte(0xF5F10, 0xF0) # bees are catchable
    rom.write_byte(0x180086, 0x00 if world.aga_randomness else 0x01)  # set blue ball and ganon warp randomness
    rom.write_byte(0x1800A0, 0x01)  # return to light world on s+q without mirror
    rom.write_byte(0x1800A1, 0x01)  # enable overworld screen transition draining for water level inside swamp
    rom.write_byte(0x180174, 0x01 if world.fix_fake_world else 0x00)
    rom.write_byte(0x180175, 0x00) # Arrow mode: normal
    rom.write_int16_to_rom(0x180176, 0) # Wood Arrow Cost (rupee arrow mode)
    rom.write_int16_to_rom(0x180178, 0) # Silver Arrow Cost (rupee arrow mode)
    rom.write_byte(0x180034, 0x0A) # starting max bombs
    rom.write_byte(0x180035, 30) # starting max arrows
    for x in range(0x183000, 0x18304F):
        rom.write_byte(x, 0) # Zero the initial equipment array
    rom.write_byte(0x18302C, 0x18) # starting max health
    rom.write_byte(0x18302D, 0x18) # starting current health
    rom.write_byte(0x183039, 0x68) # starting abilities, bit array
    rom.write_byte(0x18004A, 0x00) # Inverted mode (off)
    rom.write_byte(0x2AF79, 0xD0) # vortexes: Normal  (D0=light to dark, F0=dark to light, 42 = both)
    rom.write_byte(0x3A943, 0xD0) # Mirror: Normal  (D0=Dark to Light, F0=light to dark, 42 = both)
    rom.write_byte(0x3A96D, 0xF0) # Residual Portal: Normal  (F0= Light Side, D0=Dark Side, 42 = both (Darth Vader))
    rom.write_byte(0x3A9A7, 0xD0) # Residual Portal: Normal  (D0= Light Side, F0=Dark Side, 42 = both (Darth Vader))

    rom.write_byte(0x18004D, 0x00) # Escape assist (off)
    rom.write_byte(0x18004E, 0x00) # uncle Refill (off)


    if world.goal in ['pedestal', 'triforcehunt']:
        rom.write_byte(0x18003E, 0x01)  # make ganon invincible
    elif world.goal in ['dungeons']:
        rom.write_byte(0x18003E, 0x02)  # make ganon invincible until all dungeons are beat
    elif world.goal in ['crystals']:
        rom.write_byte(0x18003E, 0x04)  # make ganon invincible until all crystals
    else:
        rom.write_byte(0x18003E, 0x03)  # make ganon invincible until all crystals and aga 2 are collected

    rom.write_byte(0x18016A, 0x01 if world.keysanity else 0x00)  # free roaming item text boxes
    rom.write_byte(0x18003B, 0x01 if world.keysanity else 0x00)  # maps showing crystals on overworld

    # compasses showing dungeon count
    if world.clock_mode != 'off':
        rom.write_byte(0x18003C, 0x00)  # Currently must be off if timer is on, because they use same HUD location
    elif world.difficulty == 'easy':
        rom.write_byte(0x18003C, 0x02)  # always on
    elif world.keysanity:
        rom.write_byte(0x18003C, 0x01)  # show on pickup
    else:
        rom.write_byte(0x18003C, 0x00)

    rom.write_byte(0x180045, 0xFF if world.keysanity else 0x00)  # free roaming items in menu
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

    # Shop table
    rom.write_bytes(0x184800, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

    # patch swamp: Need to enable permanent drain of water as dam or swamp were moved
    rom.write_byte(0x18003D, 0x01 if world.swamp_patch_required else 0x00)

    # powder patch: remove the need to leave the scrren after powder, since it causes problems for potion shop at race game
    # temporarally we are just nopping out this check we will conver this to a rom fix soon.
    rom.write_bytes(0x02F539,[0xEA,0xEA,0xEA,0xEA,0xEA] if world.powder_patch_required else [0xAD, 0xBF, 0x0A, 0xF0, 0x4F])

    # allow smith into multi-entrance caves in appropriate shuffles
    if world.shuffle in ['restricted', 'full', 'crossed', 'insanity']:
        rom.write_byte(0x18004C, 0x01)

    # set correct flag for hera basement item
    if world.get_location('Tower of Hera - Basement Cage').item is not None and world.get_location('Tower of Hera - Basement Cage').item.name == 'Small Key (Tower of Hera)':
        rom.write_byte(0x4E3BB, 0xE4)
    else:
        rom.write_byte(0x4E3BB, 0xEB)

    # fix trock doors for reverse entrances
    if world.fix_trock_doors:
        rom.write_byte(0xFED31, 0x0E)  # preopen bombable exit
        rom.write_byte(0xFEE41, 0x0E)  # preopen bombable exit
        # included unconditionally in base2current
        #rom.write_byte(0xFE465, 0x1E)  # remove small key door on backside of big key door
    else:
        rom.write_byte(0xFED31, 0x2A)  # preopen bombable exit
        rom.write_byte(0xFEE41, 0x2A)  # preopen bombable exit

    write_strings(rom, world)

    # set rom name
    # 21 bytes
    rom.write_bytes(0x7FC0, bytearray('ER_060_%09d\0' % world.seed, 'utf8') + world.option_identifier.to_bytes(4, 'big'))

    # store hash table for main menu hash
    rom.write_bytes(0x187F00, hashtable)

    apply_rom_settings(rom, beep, color, world.quickswap, world.fastmenu, world.disable_music, sprite)

    return rom

def apply_rom_settings(rom, beep, color, quickswap, fastmenu, disable_music, sprite):

    # enable instant item menu
    if fastmenu == 'instant':
        rom.write_byte(0x6DD9A, 0x20)
        rom.write_byte(0x6DF2A, 0x20)
        rom.write_byte(0x6E0E9, 0x20)
    else:
        rom.write_byte(0x6DD9A, 0x11)
        rom.write_byte(0x6DF2A, 0x12)
        rom.write_byte(0x6E0E9, 0x12)
    if fastmenu == 'instant':
        rom.write_byte(0x180048, 0xE8)
    elif fastmenu == 'double':
        rom.write_byte(0x180048, 0x10)
    elif fastmenu == 'triple':
        rom.write_byte(0x180048, 0x18)
    elif fastmenu == 'quadruple':
        rom.write_byte(0x180048, 0x20)
    elif fastmenu == 'half':
        rom.write_byte(0x180048, 0x04)
    else:
        rom.write_byte(0x180048, 0x08)

    rom.write_byte(0x18004B, 0x01 if quickswap else 0x00)

    music_volumes = [
        (0x00, [0xD373B, 0xD375B, 0xD90F8]),
        (0x14, [0xDA710, 0xDA7A4, 0xDA7BB, 0xDA7D2]),
        (0x3C, [0xD5954, 0xD653B, 0xDA736, 0xDA752, 0xDA772, 0xDA792]),
        (0x50, [0xD5B47, 0xD5B5E]),
        (0x54, [0xD4306]),
        (0x64, [0xD6878, 0xD6883, 0xD6E48, 0xD6E76, 0xD6EFB, 0xD6F2D, 0xDA211, 0xDA35B, 0xDA37B, 0xDA38E, 0xDA39F, 0xDA5C3, 0xDA691, 0xDA6A8, 0xDA6DF]),
        (0x78, [0xD2349, 0xD3F45, 0xD42EB, 0xD48B9, 0xD48FF, 0xD543F, 0xD5817, 0xD5957, 0xD5ACB, 0xD5AE8, 0xD5B4A, 0xDA5DE, 0xDA608, 0xDA635,
                0xDA662, 0xDA71F, 0xDA7AF, 0xDA7C6, 0xDA7DD]),
        (0x82, [0xD2F00, 0xDA3D5]),
        (0xA0, [0xD249C, 0xD24CD, 0xD2C09, 0xD2C53, 0xD2CAF, 0xD2CEB, 0xD2D91, 0xD2EE6, 0xD38ED, 0xD3C91, 0xD3CD3, 0xD3CE8, 0xD3F0C,
                0xD3F82, 0xD405F, 0xD4139, 0xD4198, 0xD41D5, 0xD41F6, 0xD422B, 0xD4270, 0xD42B1, 0xD4334, 0xD4371, 0xD43A6, 0xD43DB,
                0xD441E, 0xD4597, 0xD4B3C, 0xD4BAB, 0xD4C03, 0xD4C53, 0xD4C7F, 0xD4D9C, 0xD5424, 0xD65D2, 0xD664F, 0xD6698, 0xD66FF,
                0xD6985, 0xD6C5C, 0xD6C6F, 0xD6C8E, 0xD6CB4, 0xD6D7D, 0xD827D, 0xD960C, 0xD9828, 0xDA233, 0xDA3A2, 0xDA49E, 0xDA72B,
                0xDA745, 0xDA765, 0xDA785, 0xDABF6, 0xDAC0D, 0xDAEBE, 0xDAFAC]),
        (0xAA, [0xD9A02, 0xD9BD6]),
        (0xB4, [0xD21CD, 0xD2279, 0xD2E66, 0xD2E70, 0xD2EAB, 0xD3B97, 0xD3BAC, 0xD3BE8, 0xD3C0D, 0xD3C39, 0xD3C68, 0xD3C9F, 0xD3CBC,
                0xD401E, 0xD4290, 0xD443E, 0xD456F, 0xD47D3, 0xD4D43, 0xD4DCC, 0xD4EBA, 0xD4F0B, 0xD4FE5, 0xD5012, 0xD54BC, 0xD54D5,
                0xD54F0, 0xD5509, 0xD57D8, 0xD59B9, 0xD5A2F, 0xD5AEB, 0xD5E5E, 0xD5FE9, 0xD658F, 0xD674A, 0xD6827, 0xD69D6, 0xD69F5,
                0xD6A05, 0xD6AE9, 0xD6DCF, 0xD6E20, 0xD6ECB, 0xD71D4, 0xD71E6, 0xD7203, 0xD721E, 0xD8724, 0xD8732, 0xD9652, 0xD9698,
                0xD9CBC, 0xD9DC0, 0xD9E49, 0xDAA68, 0xDAA77, 0xDAA88, 0xDAA99, 0xDAF04]),
        (0x8c, [0xD1D28, 0xD1D41, 0xD1D5C, 0xD1D77, 0xD1EEE, 0xD311D, 0xD31D1, 0xD4148, 0xD5543, 0xD5B6F, 0xD65B3, 0xD6760, 0xD6B6B,
                0xD6DF6, 0xD6E0D, 0xD73A1, 0xD814C, 0xD825D, 0xD82BE, 0xD8340, 0xD8394, 0xD842C, 0xD8796, 0xD8903, 0xD892A, 0xD91E8,
                0xD922B, 0xD92E0, 0xD937E, 0xD93C1, 0xDA958, 0xDA971, 0xDA98C, 0xDA9A7]),
        (0xC8, [0xD1D92, 0xD1DBD, 0xD1DEB, 0xD1F5D, 0xD1F9F, 0xD1FBD, 0xD1FDC, 0xD1FEA, 0xD20CA, 0xD21BB, 0xD22C9, 0xD2754, 0xD284C,
                0xD2866, 0xD2887, 0xD28A0, 0xD28BA, 0xD28DB, 0xD28F4, 0xD293E, 0xD2BF3, 0xD2C1F, 0xD2C69, 0xD2CA1, 0xD2CC5, 0xD2D05,
                0xD2D73, 0xD2DAF, 0xD2E3D, 0xD2F36, 0xD2F46, 0xD2F6F, 0xD2FCF, 0xD2FDF, 0xD302B, 0xD3086, 0xD3099, 0xD30A5, 0xD30CD,
                0xD30F6, 0xD3154, 0xD3184, 0xD333A, 0xD33D9, 0xD349F, 0xD354A, 0xD35E5, 0xD3624, 0xD363C, 0xD3672, 0xD3691, 0xD36B4,
                0xD36C6, 0xD3724, 0xD3767, 0xD38CB, 0xD3B1D, 0xD3B2F, 0xD3B55, 0xD3B70, 0xD3B81, 0xD3BBF, 0xD3F65, 0xD3FA6, 0xD404F,
                0xD4087, 0xD417A, 0xD41A0, 0xD425C, 0xD4319, 0xD433C, 0xD43EF, 0xD440C, 0xD4452, 0xD4494, 0xD44B5, 0xD4512, 0xD45D1,
                0xD45EF, 0xD4682, 0xD46C3, 0xD483C, 0xD4848, 0xD4855, 0xD4862, 0xD486F, 0xD487C, 0xD4A1C, 0xD4A3B, 0xD4A60, 0xD4B27,
                0xD4C7A, 0xD4D12, 0xD4D81, 0xD4E90, 0xD4ED6, 0xD4EE2, 0xD5005, 0xD502E, 0xD503C, 0xD5081, 0xD51B1, 0xD51C7, 0xD51CF,
                0xD51EF, 0xD520C, 0xD5214, 0xD5231, 0xD5257, 0xD526D, 0xD5275, 0xD52AF, 0xD52BD, 0xD52CD, 0xD52DB, 0xD549C, 0xD5801,
                0xD58A4, 0xD5A68, 0xD5A7F, 0xD5C12, 0xD5D71, 0xD5E10, 0xD5E9A, 0xD5F8B, 0xD5FA4, 0xD651A, 0xD6542, 0xD65ED, 0xD661D,
                0xD66D7, 0xD6776, 0xD68BD, 0xD68E5, 0xD6956, 0xD6973, 0xD69A8, 0xD6A51, 0xD6A86, 0xD6B96, 0xD6C3E, 0xD6D4A, 0xD6E9C,
                0xD6F80, 0xD717E, 0xD7190, 0xD71B9, 0xD811D, 0xD8139, 0xD816B, 0xD818A, 0xD819E, 0xD81BE, 0xD829C, 0xD82E1, 0xD8306,
                0xD830E, 0xD835E, 0xD83AB, 0xD83CA, 0xD83F0, 0xD83F8, 0xD844B, 0xD8479, 0xD849E, 0xD84CB, 0xD84EB, 0xD84F3, 0xD854A,
                0xD8573, 0xD859D, 0xD85B4, 0xD85CE, 0xD862A, 0xD8681, 0xD87E3, 0xD87FF, 0xD887B, 0xD88C6, 0xD88E3, 0xD8944, 0xD897B,
                0xD8C97, 0xD8CA4, 0xD8CB3, 0xD8CC2, 0xD8CD1, 0xD8D01, 0xD917B, 0xD918C, 0xD919A, 0xD91B5, 0xD91D0, 0xD91DD, 0xD9220,
                0xD9273, 0xD9284, 0xD9292, 0xD92AD, 0xD92C8, 0xD92D5, 0xD9311, 0xD9322, 0xD9330, 0xD934B, 0xD9366, 0xD9373, 0xD93B6,
                0xD97A6, 0xD97C2, 0xD97DC, 0xD97FB, 0xD9811, 0xD98FF, 0xD996F, 0xD99A8, 0xD99D5, 0xD9A30, 0xD9A4E, 0xD9A6B, 0xD9A88,
                0xD9AF7, 0xD9B1D, 0xD9B43, 0xD9B7C, 0xD9BA9, 0xD9C84, 0xD9C8D, 0xD9CAC, 0xD9CE8, 0xD9CF3, 0xD9CFD, 0xD9D46, 0xDA35E,
                0xDA37E, 0xDA391, 0xDA478, 0xDA4C3, 0xDA4D7, 0xDA4F6, 0xDA515, 0xDA6E2, 0xDA9C2, 0xDA9ED, 0xDAA1B, 0xDAA57, 0xDABAF,
                0xDABC9, 0xDABE2, 0xDAC28, 0xDAC46, 0xDAC63, 0xDACB8, 0xDACEC, 0xDAD08, 0xDAD25, 0xDAD42, 0xDAD5F, 0xDAE17, 0xDAE34,
                0xDAE51, 0xDAF2E, 0xDAF55, 0xDAF6B, 0xDAF81, 0xDB14F, 0xDB16B, 0xDB180, 0xDB195, 0xDB1AA]),
        (0xD2, [0xD2B88, 0xD364A, 0xD369F, 0xD3747]),
        (0xDC, [0xD213F, 0xD2174, 0xD229E, 0xD2426, 0xD4731, 0xD4753, 0xD4774, 0xD4795, 0xD47B6, 0xD4AA5, 0xD4AE4, 0xD4B96, 0xD4CA5,
                0xD5477, 0xD5A3D, 0xD6566, 0xD672C, 0xD67C0, 0xD69B8, 0xD6AB1, 0xD6C05, 0xD6DB3, 0xD71AB, 0xD8E2D, 0xD8F0D, 0xD94E0,
                0xD9544, 0xD95A8, 0xD9982, 0xD9B56, 0xDA694, 0xDA6AB, 0xDAE88, 0xDAEC8, 0xDAEE6, 0xDB1BF]),
        (0xE6, [0xD210A, 0xD22DC, 0xD2447, 0xD5A4D, 0xD5DDC, 0xDA251, 0xDA26C]),
        (0xF0, [0xD945E, 0xD967D, 0xD96C2, 0xD9C95, 0xD9EE6, 0xDA5C6]),
        (0xFA, [0xD2047, 0xD24C2, 0xD24EC, 0xD25A4, 0xD51A8, 0xD51E6, 0xD524E, 0xD529E, 0xD6045, 0xD81DE, 0xD821E, 0xD94AA, 0xD9A9E,
                0xD9AE4, 0xDA289]),
        (0xFF, [0xD2085, 0xD21C5, 0xD5F28])
    ]
    for volume, addresses in music_volumes:
        for address in addresses:
            rom.write_byte(address, volume if not disable_music else 0x00)

    # restore Mirror sound effect volumes (for existing seeds that lack it)
    rom.write_byte(0xD3E04, 0xC8)
    rom.write_byte(0xD3DC6, 0xC8)
    rom.write_byte(0xD3D6E, 0xC8)
    rom.write_byte(0xD3D34, 0xC8)
    rom.write_byte(0xD3D55, 0xC8)
    rom.write_byte(0xD3E38, 0xC8)
    rom.write_byte(0xD3DAA, 0xFA)

    # set heart beep rate
    rom.write_byte(0x180033, {'off': 0x00, 'half': 0x40, 'quarter': 0x80, 'normal': 0x20}[beep])

    # set heart color
    rom.write_byte(0x6FA1E, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA20, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA22, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA24, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA26, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA28, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA2A, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA2C, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA2E, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x6FA30, {'red': 0x24, 'blue': 0x2C, 'green': 0x3C, 'yellow': 0x28}[color])
    rom.write_byte(0x65561, {'red': 0x05, 'blue': 0x0D, 'green': 0x19, 'yellow': 0x09}[color])

    # write link sprite if required
    if sprite is not None:
        write_sprite(rom, sprite)

    if isinstance(rom, LocalRom):
        rom.write_crc()


def write_sprite(rom, sprite):
    if not sprite.valid:
        return
    rom.write_bytes(0x80000, sprite.sprite)
    rom.write_bytes(0xDD308, sprite.palette)
    rom.write_bytes(0xDEDF5, sprite.glove_palette)


def write_string_to_rom(rom, target, string):
    address, maxbytes = text_addresses[target]
    rom.write_bytes(address, string_to_alttp_text(string, maxbytes))


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

    pedestalitem = world.get_location('Master Sword Pedestal').item
    pedestal_text = 'Some Hot Air' if pedestalitem is None else pedestalitem.pedestal_hint_text if pedestalitem.pedestal_hint_text is not None else 'Unknown Item'
    write_string_to_rom(rom, 'Pedestal', pedestal_text)
    pedestal_credit_text = 'and the Hot Air' if pedestalitem is None else pedestalitem.pedestal_credit_text if pedestalitem.pedestal_credit_text is not None else 'and the Unknown Item'

    etheritem = world.get_location('Ether Tablet').item
    ether_text = 'Some Hot Air' if etheritem is None else etheritem.pedestal_hint_text if etheritem.pedestal_hint_text is not None else 'Unknown Item'
    write_string_to_rom(rom, 'EtherTablet', ether_text)
    bombositem = world.get_location('Bombos Tablet').item
    bombos_text = 'Some Hot Air' if bombositem is None else bombositem.pedestal_hint_text if bombositem.pedestal_hint_text is not None else 'Unknown Item'
    write_string_to_rom(rom, 'BombosTablet', bombos_text)

    credits = Credits()

    sickkiditem = world.get_location('Sick Kid').item
    sickkiditem_text = random.choice(SickKid_texts) if sickkiditem is None or sickkiditem.sickkid_credit_text is None else sickkiditem.sickkid_credit_text

    zoraitem = world.get_location('King Zora').item
    zoraitem_text = random.choice(Zora_texts) if zoraitem is None or zoraitem.zora_credit_text is None else zoraitem.zora_credit_text

    magicshopitem = world.get_location('Potion Shop').item
    magicshopitem_text = random.choice(MagicShop_texts) if magicshopitem is None or magicshopitem.magicshop_credit_text is None else magicshopitem.magicshop_credit_text

    fluteboyitem = world.get_location('Flute Spot').item
    fluteboyitem_text = random.choice(FluteBoy_texts) if fluteboyitem is None or fluteboyitem.fluteboy_credit_text is None else fluteboyitem.fluteboy_credit_text

    credits.update_credits_line('castle', 0, random.choice(KingsReturn_texts))
    credits.update_credits_line('sancturary', 0, random.choice(Sanctuary_texts))

    credits.update_credits_line('kakariko', 0, random.choice(Kakariko_texts).format(random.choice(Sahasrahla_names)))
    credits.update_credits_line('desert', 0, random.choice(DesertPalace_texts))
    credits.update_credits_line('hera', 0, random.choice(MountainTower_texts))
    credits.update_credits_line('house', 0, random.choice(LinksHouse_texts))
    credits.update_credits_line('zora', 0, zoraitem_text)
    credits.update_credits_line('witch', 0, magicshopitem_text)
    credits.update_credits_line('lumberjacks', 0, random.choice(Lumberjacks_texts))
    credits.update_credits_line('grove', 0, fluteboyitem_text)
    credits.update_credits_line('well', 0, random.choice(WishingWell_texts))
    credits.update_credits_line('smithy', 0, random.choice(Blacksmiths_texts))
    credits.update_credits_line('kakariko2', 0, sickkiditem_text)
    credits.update_credits_line('bridge', 0, random.choice(DeathMountain_texts))
    credits.update_credits_line('woods', 0, random.choice(LostWoods_texts))
    credits.update_credits_line('pedestal', 0, pedestal_credit_text)

    (pointers, data) = credits.get_bytes()
    rom.write_bytes(0x181500, data)
    rom.write_bytes(0x76CC0, [byte for p in pointers for byte in [p & 0xFF, p >> 8 & 0xFF]])
