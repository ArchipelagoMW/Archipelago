import io
import json
import hashlib
import logging
import os
import random
import struct
import subprocess

from BaseClasses import ShopType, Region, Location, Item
from Dungeons import dungeon_music_addresses
from Text import MultiByteTextMapper, CompressedTextMapper, text_addresses, Credits, TextTable
from Text import Uncle_texts, Ganon1_texts, TavernMan_texts, Sahasrahla2_texts, Triforce_texts, Blind_texts, BombShop2_texts, junk_texts
from Text import KingsReturn_texts, Sanctuary_texts, Kakariko_texts, Blacksmiths_texts, DeathMountain_texts, LostWoods_texts, WishingWell_texts, DesertPalace_texts, MountainTower_texts, LinksHouse_texts, Lumberjacks_texts, SickKid_texts, FluteBoy_texts, Zora_texts, MagicShop_texts, Sahasrahla_names
from Utils import output_path, local_path, int16_as_bytes, int32_as_bytes, snes_to_pc
from Items import ItemFactory, item_table
from EntranceShuffle import door_addresses


JAP10HASH = '03a63945398191337e896e5771f77173'
RANDOMIZERBASEHASH = 'cb560220b7b1b8202e92381aee19cd36'


class JsonRom(object):

    def __init__(self):
        self.name = None
        self.patches = {}

    def write_byte(self, address, value):
        self.patches[str(address)] = [value]

    def write_bytes(self, startaddress, values):
        if not values:
            return
        self.patches[str(startaddress)] = list(values)

    def write_int16(self, address, value):
        self.write_bytes(address, int16_as_bytes(value))

    def write_int16s(self, startaddress, values):
        byte_list = [int16_as_bytes(value) for value in values]
        self.patches[str(startaddress)] = [byte for bytes in byte_list for byte in bytes]
    
    def write_int32(self, address, value):
        self.write_bytes(address, int32_as_bytes(value))

    def write_to_file(self, file):
        with open(file, 'w') as stream:
            json.dump([self.patches], stream)

    def get_hash(self):
        h = hashlib.md5()
        h.update(json.dumps([self.patches]).encode('utf-8'))
        return h.hexdigest()



class LocalRom(object):

    def __init__(self, file, patch=True):
        self.name = None
        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        if patch:
            self.patch_base_rom()

    def write_byte(self, address, value):
        self.buffer[address] = value

    def write_bytes(self, startaddress, values):
        for i, value in enumerate(values):
            self.write_byte(startaddress + i, value)

    def write_int16(self, address, value):
        self.write_bytes(address, int16_as_bytes(value))

    def write_int16s(self, startaddress, values):
        for i, value in enumerate(values):
            self.write_int16(startaddress + (i * 2), value)
 
    def write_int32(self, address, value):
        self.write_bytes(address, int32_as_bytes(value))

    def write_int32s(self, startaddress, values):
        for i, value in enumerate(values):
            self.write_int32(startaddress + (i * 2), value)

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
        self.buffer.extend(bytearray([0x00] * (0x200000 - len(self.buffer))))

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

    def patch_enemizer(self, rando_patch, base_enemizer_patch_path, enemizer_patch):
        # extend to 4MB
        self.buffer.extend(bytearray([0x00] * (0x400000 - len(self.buffer))))

        # apply randomizer patches
        for address, values in rando_patch.items():
            self.write_bytes(int(address), values)

        # load base enemizer patches
        with open(base_enemizer_patch_path, 'r') as f:
            base_enemizer_patch = json.load(f)
        for patch in base_enemizer_patch:
            self.write_bytes(patch["address"], patch["patchData"])

        # apply enemizer patches
        for patch in enemizer_patch:
            self.write_bytes(patch["address"], patch["patchData"])

    def write_crc(self):
        crc = (sum(self.buffer[:0x7FDC] + self.buffer[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])

    def get_hash(self):
        h = hashlib.md5()
        h.update(self.buffer)
        return h.hexdigest()

def read_rom(stream):
    "Reads rom into bytearray and strips off any smc header"
    buffer = bytearray(stream.read())
    if len(buffer)%0x400 == 0x200:
        buffer = buffer[0x200:]
    return buffer

def get_enemizer_patch(world, player, rom, baserom_path, enemizercli, shuffleenemies, enemy_health, enemy_damage, shufflepalette, shufflepots):
    baserom_path = os.path.abspath(baserom_path)
    basepatch_path = os.path.abspath(local_path('data/base2current.json'))
    randopatch_path = os.path.abspath(output_path('enemizer_randopatch.json'))
    options_path = os.path.abspath(output_path('enemizer_options.json'))
    enemizer_output_path = os.path.abspath(output_path('enemizer_output.json'))

    # write options file for enemizer
    options = {
        'RandomizeEnemies': shuffleenemies,
        'RandomizeEnemiesType': 3,
        'RandomizeBushEnemyChance': True,
        'RandomizeEnemyHealthRange': enemy_health != 'default',
        'RandomizeEnemyHealthType': {'default': 0, 'easy': 0, 'normal': 1, 'hard': 2, 'expert': 3}[enemy_health],
        'OHKO': False,
        'RandomizeEnemyDamage': enemy_damage != 'default',
        'AllowEnemyZeroDamage': True,
        'ShuffleEnemyDamageGroups': enemy_damage != 'default',
        'EnemyDamageChaosMode': enemy_damage == 'chaos',
        'EasyModeEscape': False,
        'EnemiesAbsorbable': False,
        'AbsorbableSpawnRate': 10,
        'AbsorbableTypes': {
            'FullMagic': True, 'SmallMagic': True, 'Bomb_1': True, 'BlueRupee': True, 'Heart': True, 'BigKey': True, 'Key': True,
            'Fairy': True, 'Arrow_10': True, 'Arrow_5': True, 'Bomb_8': True, 'Bomb_4': True, 'GreenRupee': True, 'RedRupee': True
        },
        'BossMadness': False,
        'RandomizeBosses': True,
        'RandomizeBossesType': 0,
        'RandomizeBossHealth': False,
        'RandomizeBossHealthMinAmount': 0,
        'RandomizeBossHealthMaxAmount': 300,
        'RandomizeBossDamage': False,
        'RandomizeBossDamageMinAmount': 0,
        'RandomizeBossDamageMaxAmount': 200,
        'RandomizeBossBehavior': False,
        'RandomizeDungeonPalettes': shufflepalette,
        'SetBlackoutMode': False,
        'RandomizeOverworldPalettes': shufflepalette,
        'RandomizeSpritePalettes': shufflepalette,
        'SetAdvancedSpritePalettes': False,
        'PukeMode': False,
        'NegativeMode': False,
        'GrayscaleMode': False,
        'GenerateSpoilers': False,
        'RandomizeLinkSpritePalette': False,
        'RandomizePots': shufflepots,
        'ShuffleMusic': False,
        'BootlegMagic': True,
        'CustomBosses': False,
        'AndyMode': False,
        'HeartBeepSpeed': 0,
        'AlternateGfx': False,
        'ShieldGraphics': "shield_gfx/normal.gfx",
        'SwordGraphics': "sword_gfx/normal.gfx",
        'BeeMizer': False,
        'BeesLevel': 0,
        'RandomizeTileTrapPattern': True,
        'RandomizeTileTrapFloorTile': False,
        'AllowKillableThief': shuffleenemies,
        'RandomizeSpriteOnHit': False,
        'DebugMode': False,
        'DebugForceEnemy': False,
        'DebugForceEnemyId': 0,
        'DebugForceBoss': False,
        'DebugForceBossId': 0,
        'DebugOpenShutterDoors': False,
        'DebugForceEnemyDamageZero': False,
        'DebugShowRoomIdInRupeeCounter': False,
        'UseManualBosses': True,
        'ManualBosses': {
            'EasternPalace': world.get_dungeon("Eastern Palace", player).boss.enemizer_name,
            'DesertPalace': world.get_dungeon("Desert Palace", player).boss.enemizer_name,
            'TowerOfHera': world.get_dungeon("Tower of Hera", player).boss.enemizer_name,
            'AgahnimsTower': 'Agahnim',
            'PalaceOfDarkness': world.get_dungeon("Palace of Darkness", player).boss.enemizer_name,
            'SwampPalace': world.get_dungeon("Swamp Palace", player).boss.enemizer_name,
            'SkullWoods': world.get_dungeon("Skull Woods", player).boss.enemizer_name,
            'ThievesTown': world.get_dungeon("Thieves Town", player).boss.enemizer_name,
            'IcePalace': world.get_dungeon("Ice Palace", player).boss.enemizer_name,
            'MiseryMire': world.get_dungeon("Misery Mire", player).boss.enemizer_name,
            'TurtleRock': world.get_dungeon("Turtle Rock", player).boss.enemizer_name,
            'GanonsTower4': 'Agahnim2',
            'Ganon': 'Ganon',
        }
    }

    if world.mode != 'inverted':
        options['ManualBosses']['GanonsTower1'] = world.get_dungeon('Ganons Tower', player).bosses['bottom'].enemizer_name
        options['ManualBosses']['GanonsTower2'] = world.get_dungeon('Ganons Tower', player).bosses['middle'].enemizer_name
        options['ManualBosses']['GanonsTower3'] = world.get_dungeon('Ganons Tower', player).bosses['top'].enemizer_name
    else:
        options['ManualBosses']['GanonsTower1'] = world.get_dungeon('Inverted Ganons Tower', player).bosses['bottom'].enemizer_name
        options['ManualBosses']['GanonsTower2'] = world.get_dungeon('Inverted Ganons Tower', player).bosses['middle'].enemizer_name
        options['ManualBosses']['GanonsTower3'] = world.get_dungeon('Inverted Ganons Tower', player).bosses['top'].enemizer_name


    rom.write_to_file(randopatch_path)

    with open(options_path, 'w') as f:
        json.dump(options, f)

    subprocess.check_call([os.path.abspath(enemizercli),
                           '--rom', baserom_path,
                           '--seed', str(world.rom_seeds[player]),
                           '--base', basepatch_path,
                           '--randomizer', randopatch_path,
                           '--enemizer', options_path,
                           '--output', enemizer_output_path],
                          cwd=os.path.dirname(enemizercli), stdout=subprocess.DEVNULL)

    with open(enemizer_output_path, 'r') as f:
        ret = json.load(f)

    if os.path.exists(randopatch_path):
        os.remove(randopatch_path)

    if os.path.exists(options_path):
        os.remove(options_path)

    if os.path.exists(enemizer_output_path):
        os.remove(enemizer_output_path)

    return ret

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

def patch_rom(world, player, rom):
    random.seed(world.rom_seeds[player])

    # progressive bow silver arrow hint hack
    prog_bow_locs = world.find_items('Progressive Bow', player)
    if len(prog_bow_locs) > 1:
        # only pick a distingushed bow if we have at least two
        distinguished_prog_bow_loc = random.choice(prog_bow_locs)
        distinguished_prog_bow_loc.item.code = 0x65

    # patch items
    for location in world.get_locations():
        if location.player != player:
            continue

        itemid = location.item.code if location.item is not None else 0x5A

        if location.address is None:
            continue

        if not location.crystal:
            # Keys in their native dungeon should use the orignal item code for keys
            if location.parent_region.dungeon:
                dungeon = location.parent_region.dungeon
                if location.item is not None and location.item.key and dungeon.is_dungeon_item(location.item):
                    if location.item.type == "BigKey":
                        itemid = 0x32
                    if location.item.type == "SmallKey":
                        itemid = 0x24
            rom.write_byte(location.address, itemid)
        else:
            # crystals
            for address, value in zip(location.address, itemid):
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
            if exit.target is not None and exit.player == player:
                if isinstance(exit.addresses, tuple):
                    offset = exit.target
                    room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2 = exit.addresses
                    #room id is deliberately not written


                    rom.write_byte(0x15B8C + offset, ow_area)
                    rom.write_int16(0x15BDB + 2 * offset, vram_loc)
                    rom.write_int16(0x15C79 + 2 * offset, scroll_y)
                    rom.write_int16(0x15D17 + 2 * offset, scroll_x)

                    # for positioning fixups we abuse the roomid as a way of identifying which exit data we are appling
                    # Thanks to Zarby89 for originally finding these values
                    # todo fix screen scrolling

                    if world.shuffle not in ['insanity', 'insanity_legacy', 'madness_legacy'] and \
                        exit.name in ['Eastern Palace Exit', 'Tower of Hera Exit', 'Thieves Town Exit', 'Skull Woods Final Section Exit', 'Ice Palace Exit', 'Misery Mire Exit',
                                      'Palace of Darkness Exit', 'Swamp Palace Exit', 'Ganons Tower Exit', 'Desert Palace Exit (North)', 'Agahnims Tower Exit', 'Spiral Cave Exit (Top)',
                                      'Superbunny Cave Exit (Bottom)', 'Turtle Rock Ledge Exit (East)']:
                        # For exits that connot be reached from another, no need to apply offset fixes.
                        rom.write_int16(0x15DB5 + 2 * offset, link_y) # same as final else
                    elif room_id == 0x0059 and world.fix_skullwoods_exit:
                        rom.write_int16(0x15DB5 + 2 * offset, 0x00F8)
                    elif room_id == 0x004a and world.fix_palaceofdarkness_exit:
                        rom.write_int16(0x15DB5 + 2 * offset, 0x0640)
                    elif room_id == 0x00d6 and world.fix_trock_exit:
                        rom.write_int16(0x15DB5 + 2 * offset, 0x0134)
                    elif room_id == 0x000c and world.fix_gtower_exit: # fix ganons tower exit point
                        rom.write_int16(0x15DB5 + 2 * offset, 0x00A4)
                    else:
                        rom.write_int16(0x15DB5 + 2 * offset, link_y)

                    rom.write_int16(0x15E53 + 2 * offset, link_x)
                    rom.write_int16(0x15EF1 + 2 * offset, camera_y)
                    rom.write_int16(0x15F8F + 2 * offset, camera_x)
                    rom.write_byte(0x1602D + offset, unknown_1)
                    rom.write_byte(0x1607C + offset, unknown_2)
                    rom.write_int16(0x160CB + 2 * offset, door_1)
                    rom.write_int16(0x16169 + 2 * offset, door_2)
                elif isinstance(exit.addresses, list):
                    # is hole
                    for address in exit.addresses:
                        rom.write_byte(address, exit.target)
                else:
                    # patch door table
                    rom.write_byte(0xDBB73 + exit.addresses, exit.target)
    if world.mode == 'inverted':
        patch_shuffled_dark_sanc(world, rom, player)
        
    write_custom_shops(rom, world, player)

    # patch medallion requirements
    if world.required_medallions[player][0] == 'Bombos':
        rom.write_byte(0x180022, 0x00)  # requirement
        rom.write_byte(0x4FF2, 0x31)  # sprite
        rom.write_byte(0x50D1, 0x80)
        rom.write_byte(0x51B0, 0x00)
    elif world.required_medallions[player][0] == 'Quake':
        rom.write_byte(0x180022, 0x02)  # requirement
        rom.write_byte(0x4FF2, 0x31)  # sprite
        rom.write_byte(0x50D1, 0x88)
        rom.write_byte(0x51B0, 0x00)
    if world.required_medallions[player][1] == 'Bombos':
        rom.write_byte(0x180023, 0x00)  # requirement
        rom.write_byte(0x5020, 0x31)  # sprite
        rom.write_byte(0x50FF, 0x90)
        rom.write_byte(0x51DE, 0x00)
    elif world.required_medallions[player][1] == 'Ether':
        rom.write_byte(0x180023, 0x01)  # requirement
        rom.write_byte(0x5020, 0x31)  # sprite
        rom.write_byte(0x50FF, 0x98)
        rom.write_byte(0x51DE, 0x00)

    # set open mode:
    if world.mode in ['open', 'inverted']:
        rom.write_byte(0x180032, 0x01)  # open mode
    if world.mode == 'inverted':
        set_inverted_mode(world, rom)
    elif world.mode == 'standard':
        rom.write_byte(0x180032, 0x00)  # standard mode

    uncle_location = world.get_location('Link\'s Uncle', player)
    if uncle_location.item is None or uncle_location.item.name not in ['Master Sword', 'Tempered Sword', 'Fighter Sword', 'Golden Sword', 'Progressive Sword']:
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

    # set light cones
    rom.write_byte(0x180038, 0x01 if world.sewer_light_cone else 0x00)
    rom.write_byte(0x180039, 0x01 if world.light_world_light_cone else 0x00)
    rom.write_byte(0x18003A, 0x01 if world.dark_world_light_cone else 0x00)

    GREEN_TWENTY_RUPEES = 0x47
    TRIFORCE_PIECE = ItemFactory('Triforce Piece', player).code
    GREEN_CLOCK = ItemFactory('Green Clock', player).code

    rom.write_byte(0x18004F, 0x01) # Byrna Invulnerability: on

    # handle difficulty_adjustments
    if world.difficulty_adjustments == 'hard':
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xD8)  # One Heart
        # potion heal amount
        rom.write_byte(0x180084, 0x38)  # Seven Hearts
        # potion magic restore amount
        rom.write_byte(0x180085, 0x40)  # Half Magic
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x04, 0x08])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        #Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        rom.write_int16(0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x02) # Hookshot only
    elif world.difficulty_adjustments == 'expert':
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xD8)  # One Heart
        # potion heal amount
        rom.write_byte(0x180084, 0x20)  # 4 Hearts
        # potion magic restore amount
        rom.write_byte(0x180085, 0x20)  # Quarter Magic
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x04, 0x08])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        #Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        rom.write_int16(0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x00) # Nothing
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
        # Rupoor negative value
        rom.write_int16(0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x03) # All standard items
        #Set overflow items for progressive equipment
        if world.timer in ['timed', 'timed-countdown', 'timed-ohko']:
            overflow_replacement = GREEN_CLOCK
        else:
            overflow_replacement = GREEN_TWENTY_RUPEES

    rom.write_byte(0x180181, 0x00) # Make silver arrows freely usable
    rom.write_byte(0x180182, 0x01) # auto equip silvers on pickup

    #Byrna residual magic cost
    rom.write_bytes(0x45C42, [0x04, 0x02, 0x01])

    difficulty = world.difficulty_requirements

    if difficulty.progressive_bow_limit < 2 and world.swords == 'swordless':
        # TODO: write 2 to progressive bow limit byte
        rom.write_byte(0x180181, 0x01) # Make silver arrows work on on ganon
    else:
        # TODO: write difficulty.progressive_bow_limit to progressive bow limit byte
        pass


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
    dig_prizes = [0xB2, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8,
                  0xD9, 0xD9, 0xD9, 0xD9, 0xD9, 0xDA, 0xDA, 0xDA, 0xDA, 0xDA,
                  0xDB, 0xDB, 0xDB, 0xDB, 0xDB, 0xDC, 0xDC, 0xDC, 0xDC, 0xDC,
                  0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDE, 0xDE, 0xDE, 0xDE, 0xDE,
                  0xDF, 0xDF, 0xDF, 0xDF, 0xDF, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0,
                  0xE1, 0xE1, 0xE1, 0xE1, 0xE1, 0xE2, 0xE2, 0xE2, 0xE2, 0xE2,
                  0xE3, 0xE3, 0xE3, 0xE3, 0xE3]

    def chunk(l,n):
        return [l[i:i+n] for i in range(0, len(l), n)]

    # randomize last 7 slots
    prizes [-7:] = random.sample(prizes, 7)

    #shuffle order of 7 main packs
    packs = chunk(prizes[:56], 8)
    random.shuffle(packs)
    prizes[:56] = [drop for pack in packs for drop in pack]

    if world.difficulty_adjustments in ['hard', 'expert']:
        prize_replacements = {0xE0: 0xDF, # Fairy -> heart
                              0xE3: 0xD8} # Big magic -> small magic
        prizes = [prize_replacements.get(prize, prize) for prize in prizes]
        dig_prizes = [prize_replacements.get(prize, prize) for prize in dig_prizes]

    if world.retro:
        prize_replacements = {0xE1: 0xDA, #5 Arrows -> Blue Rupee
                              0xE2: 0xDB} #10 Arrows -> Red Rupee
        prizes = [prize_replacements.get(prize, prize) for prize in prizes]
        dig_prizes = [prize_replacements.get(prize, prize) for prize in dig_prizes]
    rom.write_bytes(0x180100, dig_prizes)

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
    rom.write_bytes(0x184000, [
        # original_item, limit, replacement_item, filler
        0x12, 0x01, 0x35, 0xFF, # lamp -> 5 rupees
        0x51, 0x06, 0x52, 0xFF, # 6 +5 bomb upgrades -> +10 bomb upgrade
        0x53, 0x06, 0x54, 0xFF, # 6 +5 arrow upgrades -> +10 arrow upgrade
        0x58, 0x01, 0x36 if world.retro else 0x43, 0xFF, # silver arrows -> single arrow (red 20 in retro mode)
        0x3E, difficulty.boss_heart_container_limit, 0x47, 0xff, # boss heart -> green 20
        0x17, difficulty.heart_piece_limit, 0x47, 0xff, # piece of heart -> green 20
        0xFF, 0xFF, 0xFF, 0xFF, # end of table sentinel
    ])

    # set Fountain bottle exchange items
    if world.difficulty in ['hard', 'expert']:
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

    # Remove Statues for upgrade fairy
    rom.write_bytes(0x01F810, [0x1A, 0x1E, 0x01, 0x1A, 0x1E, 0x01])


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
        rom.write_int32(0x180200, 0)  # red clock adjustment time (in frames, sint32)
        rom.write_int32(0x180204, 0)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32(0x180208, 0)  # green clock adjustment time (in frames, sint32)
        rom.write_int32(0x18020C, 0)  # starting time (in frames, sint32)
    elif world.clock_mode == 'ohko':
        rom.write_bytes(0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
        rom.write_int32(0x180200, 0)  # red clock adjustment time (in frames, sint32)
        rom.write_int32(0x180204, 0)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32(0x180208, 0)  # green clock adjustment time (in frames, sint32)
        rom.write_int32(0x18020C, 0)  # starting time (in frames, sint32)
    elif world.clock_mode == 'countdown-ohko':
        rom.write_bytes(0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
        rom.write_int32(0x180200, -100 * 60 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        rom.write_int32(0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32(0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        if world.difficulty_adjustments == 'normal':
            rom.write_int32(0x18020C, (10 + ERtimeincrease) * 60 * 60)  # starting time (in frames, sint32)
        else:
            rom.write_int32(0x18020C, int((5 + ERtimeincrease / 2) * 60 * 60))  # starting time (in frames, sint32)
    if world.clock_mode == 'stopwatch':
        rom.write_bytes(0x180190, [0x02, 0x01, 0x00])  # set stopwatch mode
        rom.write_int32(0x180200, -2 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        rom.write_int32(0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32(0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        rom.write_int32(0x18020C, 0)  # starting time (in frames, sint32)
    if world.clock_mode == 'countdown':
        rom.write_bytes(0x180190, [0x01, 0x01, 0x00])  # set countdown, with no reset available
        rom.write_int32(0x180200, -2 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        rom.write_int32(0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32(0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        rom.write_int32(0x18020C, (40 + ERtimeincrease) * 60 * 60)  # starting time (in frames, sint32)

    # set up goals for treasure hunt
    rom.write_bytes(0x180165, [0x0E, 0x28] if world.treasure_hunt_icon == 'Triforce Piece' else [0x0D, 0x28])
    rom.write_byte(0x180167, world.treasure_hunt_count % 256)

    # TODO: a proper race rom mode should be implemented, that changes the following flag, and rummages the table (or uses the future encryption feature, etc)
    rom.write_bytes(0x180213, [0x00, 0x01]) # Not a Tournament Seed

    rom.write_byte(0x180211, 0x06) #Game type, we set the Entrance and item randomization flags

    # assorted fixes
    rom.write_byte(0x1800A2, 0x01)  # remain in real dark world when dying in dark world dungeon before killing aga1
    rom.write_byte(0x180169, 0x01 if world.lock_aga_door_in_escape else 0x00)  # Lock or unlock aga tower door during escape sequence.
    if world.mode == 'inverted':
        rom.write_byte(0x180169, 0x02)  # lock aga/ganon tower door with crystals in inverted
    rom.write_byte(0x180171, 0x01 if world.ganon_at_pyramid[player] else 0x00)  # Enable respawning on pyramid after ganon death
    rom.write_byte(0x180173, 0x01) # Bob is enabled
    rom.write_byte(0x180168, 0x08)  # Spike Cave Damage
    rom.write_bytes(0x18016B, [0x04, 0x02, 0x01]) #Set spike cave and MM spike room Cape usage
    rom.write_bytes(0x18016E, [0x04, 0x08, 0x10]) #Set spike cave and MM spike room Cape usage
    rom.write_bytes(0x50563, [0x3F, 0x14]) # disable below ganon chest
    rom.write_byte(0x50599, 0x00) # disable below ganon chest
    rom.write_bytes(0xE9A5, [0x7E, 0x00, 0x24]) # disable below ganon chest
    rom.write_byte(0x18008B, 0x00) # Pyramid Hole not pre-opened
    rom.write_byte(0x18008C, 0x01 if world.crystals_needed_for_gt == 0 else 0x00) # Pyramid Hole pre-opened if crystal requirement is 0
    rom.write_byte(0xF5D73, 0xF0) # bees are catchable
    rom.write_byte(0xF5F10, 0xF0) # bees are catchable
    rom.write_byte(0x180086, 0x00 if world.aga_randomness else 0x01)  # set blue ball and ganon warp randomness
    rom.write_byte(0x1800A0, 0x01)  # return to light world on s+q without mirror
    rom.write_byte(0x1800A1, 0x01)  # enable overworld screen transition draining for water level inside swamp
    rom.write_byte(0x180174, 0x01 if world.fix_fake_world else 0x00)
    rom.write_byte(0x18017E, 0x01) # Fairy fountains only trade in bottles
    rom.write_byte(0x180034, 0x0A) # starting max bombs
    rom.write_byte(0x180035, 30) # starting max arrows
    for x in range(0x183000, 0x18304F):
        rom.write_byte(x, 0) # Zero the initial equipment array
    rom.write_byte(0x18302C, 0x18) # starting max health
    rom.write_byte(0x18302D, 0x18) # starting current health
    rom.write_byte(0x183039, 0x68) # starting abilities, bit array
    
    for item in world.precollected_items:
        if item.player != player:
            continue

        if item.name == 'Fighter Sword':
            rom.write_byte(0x183000+0x19, 0x01)
            rom.write_byte(0x0271A6+0x19, 0x01)
            rom.write_byte(0x180043, 0x01) # special starting sword byte
        else:
            raise RuntimeError("Unsupported pre-collected item: {}".format(item))

    rom.write_byte(0x18004A, 0x00 if world.mode != 'inverted' else 0x01)  # Inverted mode
    rom.write_byte(0x18005D, 0x00) # Hammer always breaks barrier
    rom.write_byte(0x2AF79, 0xD0 if world.mode != 'inverted' else 0xF0) # vortexes: Normal  (D0=light to dark, F0=dark to light, 42 = both)
    rom.write_byte(0x3A943, 0xD0 if world.mode != 'inverted' else 0xF0) # Mirror: Normal  (D0=Dark to Light, F0=light to dark, 42 = both)
    rom.write_byte(0x3A96D, 0xF0 if world.mode != 'inverted' else 0xD0) # Residual Portal: Normal  (F0= Light Side, D0=Dark Side, 42 = both (Darth Vader))
    rom.write_byte(0x3A9A7, 0xD0) # Residual Portal: Normal  (D0= Light Side, F0=Dark Side, 42 = both (Darth Vader))

    rom.write_bytes(0x180080, [50, 50, 70, 70]) # values to fill for Capacity Upgrades (Bomb5, Bomb10, Arrow5, Arrow10)

    rom.write_byte(0x18004D, 0x00) # Escape assist (off)

    if world.goal in ['pedestal', 'triforcehunt']:
        rom.write_byte(0x18003E, 0x01)  # make ganon invincible
    elif world.goal in ['dungeons']:
        rom.write_byte(0x18003E, 0x02)  # make ganon invincible until all dungeons are beat
    elif world.goal in ['crystals']:
        rom.write_byte(0x18003E, 0x04)  # make ganon invincible until all crystals
    else:
        rom.write_byte(0x18003E, 0x03)  # make ganon invincible until all crystals and aga 2 are collected

    rom.write_byte(0x18005E, world.crystals_needed_for_gt)
    rom.write_byte(0x18005F, world.crystals_needed_for_ganon)
    rom.write_byte(0x18008A, 0x01 if world.mode == "standard" else 0x00) # block HC upstairs doors in rain state in standard mode

    rom.write_byte(0x18016A, 0x01 if world.keysanity else 0x00)  # free roaming item text boxes
    rom.write_byte(0x18003B, 0x01 if world.keysanity else 0x00)  # maps showing crystals on overworld

    # compasses showing dungeon count
    if world.clock_mode != 'off':
        rom.write_byte(0x18003C, 0x00)  # Currently must be off if timer is on, because they use same HUD location
    elif world.keysanity:
        rom.write_byte(0x18003C, 0x01)  # show on pickup
    else:
        rom.write_byte(0x18003C, 0x00)

    rom.write_byte(0x180045, 0xFF if world.keysanity else 0x00)  # free roaming items in menu

    # Map reveals
    reveal_bytes = {
        "Eastern Palace": 0x2000,
        "Desert Palace": 0x1000,
        "Tower of Hera": 0x0020,
        "Palace of Darkness": 0x0200,
        "Thieves Town": 0x0010,
        "Skull Woods": 0x0080,
        "Swamp Palace": 0x0400,
        "Ice Palace": 0x0040,
        "Misery Mire'": 0x0100,
        "Turtle Rock": 0x0008,
    }

    def get_reveal_bytes(itemName):
        locations = world.find_items(itemName, player)
        if len(locations) < 1:
            return 0x0000
        location = locations[0]
        if location.parent_region and location.parent_region.dungeon:
            return reveal_bytes.get(location.parent_region.dungeon.name, 0x0000)
        return 0x0000

    rom.write_int16(0x18017A, get_reveal_bytes('Green Pendant') if world.keysanity else 0x0000) # Sahasrahla reveal
    rom.write_int16(0x18017C, get_reveal_bytes('Crystal 5')|get_reveal_bytes('Crystal 6') if world.keysanity else 0x0000) # Bomb Shop Reveal

    rom.write_byte(0x180172, 0x01 if world.retro else 0x00)  # universal keys
    rom.write_byte(0x180175, 0x01 if world.retro else 0x00)  # rupee bow
    rom.write_byte(0x180176, 0x0A if world.retro else 0x00)  # wood arrow cost
    rom.write_byte(0x180178, 0x32 if world.retro else 0x00)  # silver arrow cost
    rom.write_byte(0x301FC, 0xDA if world.retro else 0xE1)  # rupees replace arrows under pots
    rom.write_byte(0x30052, 0xDB if world.retro else 0xE2) # replace arrows in fish prize from bottle merchant
    rom.write_bytes(0xECB4E, [0xA9, 0x00, 0xEA, 0xEA] if world.retro else [0xAF, 0x77, 0xF3, 0x7E])  # Thief steals rupees instead of arrows
    rom.write_bytes(0xF0D96, [0xA9, 0x00, 0xEA, 0xEA] if world.retro else [0xAF, 0x77, 0xF3, 0x7E])  # Pikit steals rupees instead of arrows
    rom.write_bytes(0xEDA5, [0x35, 0x41] if world.retro else [0x43, 0x44])  # Chest game gives rupees instead of arrows
    digging_game_rng = random.randint(1, 30)  # set rng for digging game
    rom.write_byte(0x180020, digging_game_rng)
    rom.write_byte(0xEFD95, digging_game_rng)
    rom.write_byte(0x1800A3, 0x01)  # enable correct world setting behaviour after agahnim kills
    rom.write_byte(0x1800A4, 0x01 if world.logic != 'nologic' else 0x00)  # enable POD EG fix
    rom.write_byte(0x180042, 0x01 if world.save_and_quit_from_boss else 0x00)  # Allow Save and Quit after boss kill

    # remove shield from uncle
    rom.write_bytes(0x6D253, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D25B, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D283, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D28B, [0x00, 0x00, 0xf7, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D2CB, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
    rom.write_bytes(0x6D2FB, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
    rom.write_bytes(0x6D313, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])

    rom.write_byte(0x18004E, 0) # Escape Fill (nothing)
    rom.write_int16(0x180183, 300) # Escape fill rupee bow
    rom.write_bytes(0x180185, [0,0,0]) # Uncle respawn refills (magic, bombs, arrows)
    rom.write_bytes(0x180188, [0,0,0]) # Zelda respawn refills (magic, bombs, arrows)
    rom.write_bytes(0x18018B, [0,0,0]) # Mantle respawn refills (magic, bombs, arrows)
    if world.mode == 'standard':
        if uncle_location.item is not None and uncle_location.item.name in ['Bow', 'Progressive Bow']:
            rom.write_byte(0x18004E, 1) # Escape Fill (arrows)
            rom.write_int16(0x180183, 300) # Escape fill rupee bow
            rom.write_bytes(0x180185, [0,0,70]) # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [0,0,10]) # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [0,0,10]) # Mantle respawn refills (magic, bombs, arrows)
        elif uncle_location.item is not None and uncle_location.item.name in ['Cane of Somaria', 'Cane of Byrna', 'Fire Rod']:
            rom.write_byte(0x18004E, 4) # Escape Fill (magic)
            rom.write_bytes(0x180185, [0x80,0,0]) # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [0x20,0,0]) # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [0x20,0,0]) # Mantle respawn refills (magic, bombs, arrows)

    # patch swamp: Need to enable permanent drain of water as dam or swamp were moved
    rom.write_byte(0x18003D, 0x01 if world.swamp_patch_required[player] else 0x00)

    # powder patch: remove the need to leave the screen after powder, since it causes problems for potion shop at race game
    # temporarally we are just nopping out this check we will conver this to a rom fix soon.
    rom.write_bytes(0x02F539, [0xEA, 0xEA, 0xEA, 0xEA, 0xEA] if world.powder_patch_required[player] else [0xAD, 0xBF, 0x0A, 0xF0, 0x4F])

    # allow smith into multi-entrance caves in appropriate shuffles
    if world.shuffle in ['restricted', 'full', 'crossed', 'insanity']:
        rom.write_byte(0x18004C, 0x01)

    # set correct flag for hera basement item
    hera_basement = world.get_location('Tower of Hera - Basement Cage', player)
    if hera_basement.item is not None and hera_basement.item.name == 'Small Key (Tower of Hera)' and hera_basement.item.player == player:
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

    write_strings(rom, world, player)

    # set rom name
    # 21 bytes
    from Main import __version__
    rom.name = bytearray('ER_{0}_{1:09}\0'.format(__version__,world.seed), 'utf8')
    assert len(rom.name) <= 21
    rom.write_bytes(0x7FC0, rom.name)

    # Write title screen Code
    hashint = int(rom.get_hash(), 16)
    code = [
        (hashint >> 20) & 0x1F,
        (hashint >> 15) & 0x1F,
        (hashint >> 10) & 0x1F,
        (hashint >> 5) & 0x1F,
        hashint & 0x1F,
    ]
    rom.write_bytes(0x180215, code)

    return rom

def write_custom_shops(rom, world, player):
    shops = [shop for shop in world.shops if shop.replaceable and shop.active and shop.region.player == player]

    shop_data = bytearray()
    items_data = bytearray()
    sram_offset = 0

    for shop_id, shop in enumerate(shops):
        if shop_id == len(shops) - 1:
            shop_id = 0xFF
        bytes = shop.get_bytes()
        bytes[0] = shop_id
        bytes[-1] = sram_offset
        if shop.type == ShopType.TakeAny:
            sram_offset += 1
        else:
            sram_offset += shop.item_count
        shop_data.extend(bytes)
        # [id][item][price-low][price-high][max][repl_id][repl_price-low][repl_price-high]
        for item in shop.inventory:
            if item is None:
                break
            item_data = [shop_id, ItemFactory(item['item'], player).code] + int16_as_bytes(item['price']) + [item['max'], ItemFactory(item['replacement'], player).code if item['replacement'] else 0xFF] + int16_as_bytes(item['replacement_price'])
            items_data.extend(item_data)

    rom.write_bytes(0x184800, shop_data)

    items_data.extend([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    rom.write_bytes(0x184900, items_data)



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
    rom.write_byte(0x180033, {'off': 0x00, 'half': 0x40, 'quarter': 0x80, 'normal': 0x20, 'double': 0x10}[beep])

    # set heart color
    if color == 'random':
        color = random.choice(['red', 'blue', 'green', 'yellow'])
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
    rom.write_bytes(address, MultiByteTextMapper.convert(string, maxbytes))


def write_strings(rom, world, player):
    tt = TextTable()
    tt.removeUnwantedText()

    # Let's keep this guy's text accurate to the shuffle setting.
    if world.shuffle in ['vanilla', 'dungeonsfull', 'dungeonssimple']:
        tt['kakariko_flophouse_man_no_flippers'] = 'I really hate mowing my yard.\n{PAGEBREAK}\nI should move.'
        tt['kakariko_flophouse_man'] = 'I really hate mowing my yard.\n{PAGEBREAK}\nI should move.'

    def hint_text(dest, ped_hint=False):
        hint = dest.hint_text if not ped_hint else dest.pedestal_hint_text
        if dest.player != player:
            if ped_hint:
                hint += " for p%d!" % dest.player
            elif type(dest) in [Region, Location]:
                hint += " in p%d's world" % dest.player
            elif type(dest) is Item:
                hint += " for p%d" % dest.player
        return hint

    # For hints, first we write hints about entrances, some from the inconvenient list others from all reasonable entrances.
    if world.hints:
        tt['sign_north_of_links_house'] = '> Randomizer The telepathic tiles can have hints!'
        entrances_to_hint = {}
        entrances_to_hint.update(InconvenientEntrances)
        if world.shuffle_ganon:
            entrances_to_hint.update({'Ganons Tower': 'Ganon\'s Tower'})
        hint_locations = HintLocations.copy()
        random.shuffle(hint_locations)
        all_entrances = [entrance for entrance in world.get_entrances() if entrance.player == player]
        random.shuffle(all_entrances)
        hint_count = 4 if world.shuffle != 'vanilla' else 0
        for entrance in all_entrances:
            if entrance.name in entrances_to_hint:
                if hint_count > 0:
                    this_hint = entrances_to_hint[entrance.name] + ' leads to ' + hint_text(entrance.connected_region) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                    entrances_to_hint.pop(entrance.name)
                    hint_count -= 1
                else:
                    break

        entrances_to_hint.update(OtherEntrances)
        if world.shuffle in ['insanity', 'madness_legacy', 'insanity_legacy']:
            entrances_to_hint.update(InsanityEntrances)
            if world.shuffle_ganon:
                entrances_to_hint.update({'Pyramid Ledge': 'The pyramid ledge'})
        hint_count = 4 if world.shuffle != 'vanilla' else 0
        for entrance in all_entrances:
            if entrance.name in entrances_to_hint:
                if hint_count > 0:
                    this_hint = entrances_to_hint[entrance.name] + ' leads to ' + hint_text(entrance.connected_region) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                    entrances_to_hint.pop(entrance.name)
                    hint_count -= 1
                else:
                    break

        # Next we write a few hints for specific inconvenient locations. We don't make many because in entrance this is highly unpredictable.
        locations_to_hint = InconvenientLocations.copy()
        random.shuffle(locations_to_hint)
        hint_count = 3 if world.shuffle != 'vanilla' else 4
        del locations_to_hint[hint_count:]
        for location in locations_to_hint:
            if location == 'Swamp Left':
                if random.randint(0, 1) == 0:
                    first_item = hint_text(world.get_location('Swamp Palace - West Chest', player).item)
                    second_item = hint_text(world.get_location('Swamp Palace - Big Key Chest', player).item)
                else:
                    second_item = hint_text(world.get_location('Swamp Palace - West Chest', player).item)
                    first_item = hint_text(world.get_location('Swamp Palace - Big Key Chest', player).item)
                this_hint = ('The westmost chests in Swamp Palace contain ' + first_item + ' and ' + second_item + '.')
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Mire Left':
                if random.randint(0, 1) == 0:
                    first_item = hint_text(world.get_location('Misery Mire - Compass Chest', player).item)
                    second_item = hint_text(world.get_location('Misery Mire - Big Key Chest', player).item)
                else:
                    second_item = hint_text(world.get_location('Misery Mire - Compass Chest', player).item)
                    first_item = hint_text(world.get_location('Misery Mire - Big Key Chest', player).item)
                this_hint = ('The westmost chests in Misery Mire contain ' + first_item + ' and ' + second_item + '.')
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Tower of Hera - Big Key Chest':
                this_hint = 'Waiting in the Tower of Hera basement leads to ' + hint_text(world.get_location(location, player).item) + '.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Ganons Tower - Big Chest':
                this_hint = 'The big chest in Ganon\'s Tower contains ' + hint_text(world.get_location(location, player).item) + '.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Thieves\' Town - Big Chest':
                this_hint = 'The big chest in Thieves\' Town contains ' + hint_text(world.get_location(location, player).item) + '.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Ice Palace - Big Chest':
                this_hint = 'The big chest in Ice Palace contains ' + hint_text(world.get_location(location, player).item) + '.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Eastern Palace - Big Key Chest':
                this_hint = 'The antifairy guarded chest in Eastern Palace contains ' + hint_text(world.get_location(location, player).item) + '.'
                tt[hint_locations.pop(0)] = this_hint
            else:
                this_hint = location + ' leads to ' + hint_text(world.get_location(location, player).item) + '.'
                tt[hint_locations.pop(0)] = this_hint

        # Lastly we write hints to show where certain interesting items are. It is done the way it is to re-use the silver code and also to give one hint per each type of item regardless of how many exist. This supports many settings well.
        items_to_hint = RelevantItems.copy()
        if world.keysanity:
            items_to_hint.extend(KeysanityItems)
        random.shuffle(items_to_hint)
        hint_count = 5 if world.shuffle != 'vanilla' else 7
        while hint_count > 0:
            this_item = items_to_hint.pop(0)
            this_location = world.find_items(this_item, player)
            random.shuffle(this_location)
            if this_location:
                this_hint = this_location[0].item.hint_text + ' can be found ' + hint_text(this_location[0]) + '.'
                tt[hint_locations.pop(0)] = this_hint
                hint_count -= 1

        # All remaining hint slots are filled with junk hints. It is done this way to ensure the same junk hint isn't selected twice.
        junk_hints = junk_texts.copy()
        random.shuffle(junk_hints)
        for location in hint_locations:
            tt[location] = junk_hints.pop(0)

    # We still need the older hints of course. Those are done here.


    silverarrows = world.find_items('Silver Arrows', player)
    random.shuffle(silverarrows)
    silverarrow_hint = (' %s?' % hint_text(silverarrows[0]).replace('Ganon\'s', 'my')) if silverarrows else '?\nI think not!'
    tt['ganon_phase_3_no_silvers'] = 'Did you find the silver arrows%s' % silverarrow_hint

    prog_bow_locs = world.find_items('Progressive Bow', player)
    distinguished_prog_bow_loc = next((location for location in prog_bow_locs if location.item.code == 0x65), None)
    if distinguished_prog_bow_loc:
        prog_bow_locs.remove(distinguished_prog_bow_loc)
        silverarrow_hint = (' %s?' % hint_text(distinguished_prog_bow_loc).replace('Ganon\'s', 'my'))
        tt['ganon_phase_3_no_silvers'] = 'Did you find the silver arrows%s' % silverarrow_hint

    if any(prog_bow_locs):
        silverarrow_hint = (' %s?' % hint_text(random.choice(prog_bow_locs)).replace('Ganon\'s', 'my'))
        tt['ganon_phase_3_no_silvers_alt'] = 'Did you find the silver arrows%s' % silverarrow_hint


    silverarrow_hint = (' %s?' % hint_text(silverarrows[0]).replace('Ganon\'s', 'my')) if silverarrows else '?\nI think not!'


    crystal5 = world.find_items('Crystal 5', player)[0]
    crystal6 = world.find_items('Crystal 6', player)[0]
    tt['bomb_shop'] = 'Big Bomb?\nMy supply is blocked until you clear %s and %s.' % (crystal5.hint_text, crystal6.hint_text)

    greenpendant = world.find_items('Green Pendant', player)[0]
    tt['sahasrahla_bring_courage'] = 'I lost my family heirloom in %s' % greenpendant.hint_text

    tt['sign_ganons_tower'] = ('You need %d crystal to enter.' if world.crystals_needed_for_gt == 1 else 'You need %d crystals to enter.') % world.crystals_needed_for_gt
    tt['sign_ganon'] = ('You need %d crystal to beat Ganon.' if world.crystals_needed_for_ganon == 1 else 'You need %d crystals to beat Ganon.') % world.crystals_needed_for_ganon

    tt['uncle_leaving_text'] = Uncle_texts[random.randint(0, len(Uncle_texts) - 1)]
    tt['end_triforce'] = "{NOBORDER}\n" + Triforce_texts[random.randint(0, len(Triforce_texts) - 1)]
    tt['bomb_shop_big_bomb'] = BombShop2_texts[random.randint(0, len(BombShop2_texts) - 1)]

    # this is what shows after getting the green pendant item in rando
    tt['sahasrahla_quest_have_master_sword'] = Sahasrahla2_texts[random.randint(0, len(Sahasrahla2_texts) - 1)]
    tt['blind_by_the_light'] = Blind_texts[random.randint(0, len(Blind_texts) - 1)]

    if world.goal in ['pedestal', 'triforcehunt']:
        tt['ganon_fall_in_alt'] = 'Why are you even here?\n You can\'t even hurt me!'
        tt['ganon_phase_3_alt'] = 'Seriously? Go Away, I will not Die.'
    else:
        tt['ganon_fall_in'] = Ganon1_texts[random.randint(0, len(Ganon1_texts) - 1)]
        tt['ganon_fall_in_alt'] = 'You cannot defeat me until you finish your goal!'
        tt['ganon_phase_3_alt'] = 'Got wax in\nyour ears?\nI can not die!'
    tt['kakariko_tavern_fisherman'] = TavernMan_texts[random.randint(0, len(TavernMan_texts) - 1)]

    pedestalitem = world.get_location('Master Sword Pedestal', player).item
    pedestal_text = 'Some Hot Air' if pedestalitem is None else hint_text(pedestalitem, True) if pedestalitem.pedestal_hint_text is not None else 'Unknown Item'
    tt['mastersword_pedestal_translated'] = pedestal_text
    pedestal_credit_text = 'and the Hot Air' if pedestalitem is None else pedestalitem.pedestal_credit_text if pedestalitem.pedestal_credit_text is not None else 'and the Unknown Item'

    etheritem = world.get_location('Ether Tablet', player).item
    ether_text = 'Some Hot Air' if etheritem is None else hint_text(etheritem, True) if etheritem.pedestal_hint_text is not None else 'Unknown Item'
    tt['tablet_ether_book'] = ether_text
    bombositem = world.get_location('Bombos Tablet', player).item
    bombos_text = 'Some Hot Air' if bombositem is None else hint_text(bombositem, True) if bombositem.pedestal_hint_text is not None else 'Unknown Item'
    tt['tablet_bombos_book'] = bombos_text

    # inverted spawn menu changes
    if world.mode == 'inverted':
        tt['menu_start_2'] = "{MENU}\n{SPEED0}\n≥@'s house\n Dark Chapel\n{CHOICE3}"
        tt['menu_start_3'] = "{MENU}\n{SPEED0}\n≥@'s house\n Dark Chapel\n Mountain Cave\n{CHOICE2}"
        tt['intro_main'] = CompressedTextMapper.convert(
                            "{INTRO}\n Episode  III\n{PAUSE3}\n A Link to\n   the Past\n"
                            + "{PAUSE3}\nInverted\n  Randomizer\n{PAUSE3}\nAfter mostly disregarding what happened in the first two games.\n"
                            + "{PAUSE3}\nLink has been transported to the Dark World\n{PAUSE3}\nWhile he was slumbering\n"
                            + "{PAUSE3}\nWhatever will happen?\n{PAUSE3}\n{CHANGEPIC}\nGanon has moved around all the items in Hyrule.\n"
                            + "{PAUSE7}\nYou will have to find all the items necessary to beat Ganon.\n"
                            + "{PAUSE7}\nThis is your chance to be a hero.\n{PAUSE3}\n{CHANGEPIC}\n"
                            + "You must get the 7 crystals to beat Ganon.\n{PAUSE9}\n{CHANGEPIC}", False)
    rom.write_bytes(0xE0000, tt.getBytes())

    credits = Credits()

    sickkiditem = world.get_location('Sick Kid', player).item
    sickkiditem_text = random.choice(SickKid_texts) if sickkiditem is None or sickkiditem.sickkid_credit_text is None else sickkiditem.sickkid_credit_text

    zoraitem = world.get_location('King Zora', player).item
    zoraitem_text = random.choice(Zora_texts) if zoraitem is None or zoraitem.zora_credit_text is None else zoraitem.zora_credit_text

    magicshopitem = world.get_location('Potion Shop', player).item
    magicshopitem_text = random.choice(MagicShop_texts) if magicshopitem is None or magicshopitem.magicshop_credit_text is None else magicshopitem.magicshop_credit_text

    fluteboyitem = world.get_location('Flute Spot', player).item
    fluteboyitem_text = random.choice(FluteBoy_texts) if fluteboyitem is None or fluteboyitem.fluteboy_credit_text is None else fluteboyitem.fluteboy_credit_text

    credits.update_credits_line('castle', 0, random.choice(KingsReturn_texts))
    credits.update_credits_line('sanctuary', 0, random.choice(Sanctuary_texts))

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

def set_inverted_mode(world, rom):
    rom.write_byte(snes_to_pc(0x0283E0), 0xF0)  # residual portals
    rom.write_byte(snes_to_pc(0x02B34D), 0xF0)
    rom.write_byte(snes_to_pc(0x06DB78), 0x8B)
    rom.write_byte(snes_to_pc(0x05AF79), 0xF0)
    rom.write_byte(snes_to_pc(0x0DB3C5), 0xC6)
    rom.write_byte(snes_to_pc(0x07A3F4), 0xF0)  # duck
    rom.write_int16s(snes_to_pc(0x02E849), [0x0043, 0x0056, 0x0058, 0x006C, 0x006F, 0x0070, 0x007B, 0x007F, 0x001B])  # dw flute
    rom.write_int16(snes_to_pc(0x02E8D5), 0x07C8)
    rom.write_int16(snes_to_pc(0x02E8F7), 0x01F8)
    rom.write_byte(0x7A943, 0xF0)
    rom.write_byte(0x7A96D, 0xD0)
    rom.write_byte(snes_to_pc(0x08D40C), 0xD0)  # morph proof
    # the following bytes should only be written in vanilla
    # or they'll overwrite the randomizer's shuffles
    if world.shuffle == 'vanilla':
        rom.write_byte(0x15B8C, 0x6C)
        rom.write_byte(0xDBB73 + 0x00, 0x53)  # switch bomb shop and links house
        rom.write_byte(0xDBB73 + 0x52, 0x01)
        rom.write_byte(0xDBB73 + 0x23, 0x37)  # switch AT and GT
        rom.write_byte(0xDBB73 + 0x36, 0x24)
        rom.write_int16(0x15AEE + 2*0x38, 0x00E0)
        rom.write_int16(0x15AEE + 2*0x25, 0x000C)
        rom.write_byte(0xDBB73 + 0x15, 0x06)  # bumper and old man cave
        rom.write_int16(0x15AEE + 2*0x17, 0x00F0)
        rom.write_byte(0xDBB73 + 0x05, 0x16)
        rom.write_int16(0x15AEE + 2*0x07, 0x00FB)
        rom.write_byte(0xDBB73 + 0x2D, 0x17)
        rom.write_int16(0x15AEE + 2*0x2F, 0x00EB)
        rom.write_byte(0xDBB73 + 0x06, 0x2E)
        rom.write_int16(0x15AEE + 2*0x08, 0x00E6)
        rom.write_byte(0xDBB73 + 0x16, 0x5E)
        rom.write_byte(0xDBB73 + 0x6F, 0x07)  # DDM fairy to old man cave
        rom.write_int16(0x15AEE + 2*0x18, 0x00F1)
        rom.write_byte(0x15B8C + 0x18, 0x43)
        rom.write_int16(0x15BDB + 2 * 0x18, 0x1400)
        rom.write_int16(0x15C79 + 2 * 0x18, 0x0294)
        rom.write_int16(0x15D17 + 2 * 0x18, 0x0600)
        rom.write_int16(0x15DB5 + 2 * 0x18, 0x02E8)
        rom.write_int16(0x15E53 + 2 * 0x18, 0x0678)
        rom.write_int16(0x15EF1 + 2 * 0x18, 0x0303)
        rom.write_int16(0x15F8F + 2 * 0x18, 0x0685)
        rom.write_byte(0x1602D + 0x18, 0x0A)
        rom.write_byte(0x1607C + 0x18, 0xF6)
        rom.write_int16(0x160CB + 2 * 0x18, 0x0000)
        rom.write_int16(0x16169 + 2 * 0x18, 0x0000)
    rom.write_int16(0x15AEE + 2 * 0x3D, 0x0003)  # pyramid exit and houlihan
    rom.write_byte(0x15B8C + 0x3D, 0x5B)
    rom.write_int16(0x15BDB + 2 * 0x3D, 0x0B0E)
    rom.write_int16(0x15C79 + 2 * 0x3D, 0x075A)
    rom.write_int16(0x15D17 + 2 * 0x3D, 0x0674)
    rom.write_int16(0x15DB5 + 2 * 0x3D, 0x07A8)
    rom.write_int16(0x15E53 + 2 * 0x3D, 0x06E8)
    rom.write_int16(0x15EF1 + 2 * 0x3D, 0x07C7)
    rom.write_int16(0x15F8F + 2 * 0x3D, 0x06F3)
    rom.write_byte(0x1602D + 0x3D, 0x06)
    rom.write_byte(0x1607C + 0x3D, 0xFA)
    rom.write_int16(0x160CB + 2 * 0x3D, 0x0000)
    rom.write_int16(0x16169 + 2 * 0x3D, 0x0000)
    rom.write_int16(snes_to_pc(0x02D8D4), 0x112)  # change sactuary spawn point to dark sanc
    rom.write_bytes(snes_to_pc(0x02D8E8), [0x22, 0x22, 0x22, 0x23, 0x04, 0x04, 0x04, 0x05])
    rom.write_int16(snes_to_pc(0x02D91A), 0x0400)
    rom.write_int16(snes_to_pc(0x02D928), 0x222E)
    rom.write_int16(snes_to_pc(0x02D936), 0x229A)
    rom.write_int16(snes_to_pc(0x02D944), 0x0480)
    rom.write_int16(snes_to_pc(0x02D952), 0x00A5)
    rom.write_int16(snes_to_pc(0x02D960), 0x007F)
    rom.write_byte(snes_to_pc(0x02D96D), 0x14)
    rom.write_byte(snes_to_pc(0x02D974), 0x00)
    rom.write_byte(snes_to_pc(0x02D97B), 0xFF)
    rom.write_byte(snes_to_pc(0x02D982), 0x00)
    rom.write_byte(snes_to_pc(0x02D989), 0x02)
    rom.write_byte(snes_to_pc(0x02D990), 0x00)
    rom.write_int16(snes_to_pc(0x02D998), 0x0000)
    rom.write_int16(snes_to_pc(0x02D9A6), 0x005A)
    rom.write_byte(snes_to_pc(0x02D9B3), 0x12)
    # keep the old man spawn point at old man house unless shuffle is vanilla
    if world.shuffle == 'vanilla':
        rom.write_bytes(snes_to_pc(0x308350), [0x00, 0x00, 0x01])
        rom.write_int16(snes_to_pc(0x02D8DE), 0x00F1) 
        rom.write_bytes(snes_to_pc(0x02D910), [0x1F, 0x1E, 0x1F, 0x1F, 0x03, 0x02, 0x03, 0x03])
        rom.write_int16(snes_to_pc(0x02D924), 0x0300)
        rom.write_int16(snes_to_pc(0x02D932), 0x1F10)
        rom.write_int16(snes_to_pc(0x02D940), 0x1FC0)
        rom.write_int16(snes_to_pc(0x02D94E), 0x0378)
        rom.write_int16(snes_to_pc(0x02D95C), 0x0187)
        rom.write_int16(snes_to_pc(0x02D96A), 0x017F)
        rom.write_byte(snes_to_pc(0x02D972), 0x06)
        rom.write_byte(snes_to_pc(0x02D979), 0x00)
        rom.write_byte(snes_to_pc(0x02D980), 0xFF)
        rom.write_byte(snes_to_pc(0x02D987), 0x00)
        rom.write_byte(snes_to_pc(0x02D98E), 0x22)
        rom.write_byte(snes_to_pc(0x02D995), 0x12)
        rom.write_int16(snes_to_pc(0x02D9A2), 0x0000)
        rom.write_int16(snes_to_pc(0x02D9B0), 0x0007)
        rom.write_byte(snes_to_pc(0x02D9B8), 0x12)
        rom.write_bytes(0x180247, [0x00, 0x5A, 0x00, 0x00, 0x00, 0x00, 0x00])
    rom.write_int16(0x15AEE + 2 * 0x06, 0x0020)  # post aga hyrule castle spawn
    rom.write_byte(0x15B8C + 0x06, 0x1B)
    rom.write_int16(0x15BDB + 2 * 0x06, 0x00AE)
    rom.write_int16(0x15C79 + 2 * 0x06, 0x0610)
    rom.write_int16(0x15D17 + 2 * 0x06, 0x077E)
    rom.write_int16(0x15DB5 + 2 * 0x06, 0x0672)
    rom.write_int16(0x15E53 + 2 * 0x06, 0x07F8)
    rom.write_int16(0x15EF1 + 2 * 0x06, 0x067D)
    rom.write_int16(0x15F8F + 2 * 0x06, 0x0803)
    rom.write_byte(0x1602D + 0x06, 0x00)
    rom.write_byte(0x1607C + 0x06, 0xF2)
    rom.write_int16(0x160CB + 2 * 0x06, 0x0000)
    rom.write_int16(0x16169 + 2 * 0x06, 0x0000)
    rom.write_int16(snes_to_pc(0x02E87B), 0x00AE)  # move flute splot 9
    rom.write_int16(snes_to_pc(0x02E89D), 0x0610)
    rom.write_int16(snes_to_pc(0x02E8BF), 0x077E)
    rom.write_int16(snes_to_pc(0x02E8E1), 0x0672)
    rom.write_int16(snes_to_pc(0x02E903), 0x07F8)
    rom.write_int16(snes_to_pc(0x02E925), 0x067D)
    rom.write_int16(snes_to_pc(0x02E947), 0x0803)
    rom.write_int16(snes_to_pc(0x02E969), 0x0000)
    rom.write_int16(snes_to_pc(0x02E98B), 0xFFF2)
    rom.write_byte(snes_to_pc(0x1AF696), 0xF0)  # bat sprite retreat
    rom.write_byte(snes_to_pc(0x1AF6B2), 0x33)
    rom.write_bytes(snes_to_pc(0x1AF730), [0x6A, 0x9E, 0x0C, 0x00, 0x7A, 0x9E, 0x0C,
                                           0x00, 0x8A, 0x9E, 0x0C, 0x00, 0x6A, 0xAE,
                                           0x0C, 0x00, 0x7A, 0xAE, 0x0C, 0x00, 0x8A,
                                           0xAE, 0x0C, 0x00, 0x67, 0x97, 0x0C, 0x00,
                                           0x8D, 0x97, 0x0C, 0x00])
    rom.write_int16s(snes_to_pc(0x0FF1C8), [0x190F, 0x190F, 0x190F, 0x194C, 0x190F,
                                                 0x194B, 0x190F, 0x195C, 0x594B, 0x194C,
                                                 0x19EE, 0x19EE, 0x194B, 0x19EE, 0x19EE,
                                                 0x19EE, 0x594B, 0x190F, 0x595C, 0x190F,
                                                 0x190F, 0x195B, 0x190F, 0x190F, 0x19EE,
                                                 0x19EE, 0x195C, 0x19EE, 0x19EE, 0x19EE,
                                                 0x19EE, 0x595C, 0x595B, 0x190F, 0x190F,
                                                 0x190F])
    rom.write_int16s(snes_to_pc(0x0FA480), [0x190F, 0x196B, 0x9D04, 0x9D04, 0x196B,
                                                 0x190F, 0x9D04, 0x9D04])
    rom.write_int16s(snes_to_pc(0x1bb810), [0x00BE, 0x00C0, 0x013E])
    rom.write_int16s(snes_to_pc(0x1bb836), [0x001B, 0x001B, 0x001B])
    rom.write_int16(snes_to_pc(0x308300), 0x0140)
    rom.write_int16(snes_to_pc(0x308320), 0x001B)
    if world.shuffle == 'vanilla':
        rom.write_byte(snes_to_pc(0x308340), 0x7B)
    rom.write_int16(snes_to_pc(0x1af504), 0x148B)
    rom.write_int16(snes_to_pc(0x1af50c), 0x149B)
    rom.write_int16(snes_to_pc(0x1af514), 0x14A4)
    rom.write_int16(snes_to_pc(0x1af51c), 0x1489)
    rom.write_int16(snes_to_pc(0x1af524), 0x14AC)
    rom.write_int16(snes_to_pc(0x1af52c), 0x54AC)
    rom.write_int16(snes_to_pc(0x1af534), 0x148C)
    rom.write_int16(snes_to_pc(0x1af53c), 0x548C)
    rom.write_int16(snes_to_pc(0x1af544), 0x1484)
    rom.write_int16(snes_to_pc(0x1af54c), 0x5484)
    rom.write_int16(snes_to_pc(0x1af554), 0x14A2)
    rom.write_int16(snes_to_pc(0x1af55c), 0x54A2)
    rom.write_int16(snes_to_pc(0x1af564), 0x14A0)
    rom.write_int16(snes_to_pc(0x1af56c), 0x54A0)
    rom.write_int16(snes_to_pc(0x1af574), 0x148E)
    rom.write_int16(snes_to_pc(0x1af57c), 0x548E)
    rom.write_int16(snes_to_pc(0x1af584), 0x14AE)
    rom.write_int16(snes_to_pc(0x1af58c), 0x54AE)
    rom.write_byte(snes_to_pc(0x00DB9D), 0x1A)  # castle hole graphics
    rom.write_byte(snes_to_pc(0x00DC09), 0x1A)
    rom.write_byte(snes_to_pc(0x00D009), 0x31)
    rom.write_byte(snes_to_pc(0x00D0e8), 0xE0)
    rom.write_byte(snes_to_pc(0x00D1c7), 0x00)
    rom.write_int16(snes_to_pc(0x1BE8DA), 0x39AD)
    rom.write_byte(0xF6E58, 0x80)  # no whirlpool under castle gate
    rom.write_bytes(0x0086E, [0x5C, 0x00, 0xA0, 0xA1])  # TR tail
    rom.write_bytes(snes_to_pc(0x1BC67A), [0x2E, 0x0B, 0x82])  # add warps under rocks
    rom.write_bytes(snes_to_pc(0x1BC81E), [0x94, 0x1D, 0x82])
    rom.write_bytes(snes_to_pc(0x1BC655), [0x4A, 0x1D, 0x82])
    rom.write_bytes(snes_to_pc(0x1BC80D), [0xB2, 0x0B, 0x82])
    rom.write_bytes(snes_to_pc(0x1BC3DF), [0xD8, 0xD1])
    rom.write_bytes(snes_to_pc(0x1BD1D8), [0xA8, 0x02, 0x82, 0xFF, 0xFF])
    rom.write_bytes(snes_to_pc(0x1BC85A), [0x50, 0x0F, 0x82])
    rom.write_int16(0xDB96F + 2 * 0x35, 0x001B)  # move pyramid exit door
    rom.write_int16(0xDBA71 + 2 * 0x35, 0x06A4)
    if world.shuffle == 'vanilla':
        rom.write_byte(0xDBB73 + 0x35, 0x36)
    rom.write_byte(snes_to_pc(0x09D436), 0xF3)  # remove castle gate warp
    if world.shuffle == 'vanilla':
        rom.write_int16(0x15AEE + 2 * 0x37, 0x0010)  # pyramid exit to new hc area
        rom.write_byte(0x15B8C + 0x37, 0x1B)
        rom.write_int16(0x15BDB + 2 * 0x37, 0x0418)
        rom.write_int16(0x15C79 + 2 * 0x37, 0x0679)
        rom.write_int16(0x15D17 + 2 * 0x37, 0x06B4)
        rom.write_int16(0x15DB5 + 2 * 0x37, 0x06C6)
        rom.write_int16(0x15E53 + 2 * 0x37, 0x0738)
        rom.write_int16(0x15EF1 + 2 * 0x37, 0x06E6)
        rom.write_int16(0x15F8F + 2 * 0x37, 0x0733)
        rom.write_byte(0x1602D + 0x37, 0x07)
        rom.write_byte(0x1607C + 0x37, 0xF9)
        rom.write_int16(0x160CB + 2 * 0x37, 0x0000)
        rom.write_int16(0x16169 + 2 * 0x37, 0x0000)
    rom.write_bytes(snes_to_pc(0x1BC387), [0xDD, 0xD1])
    rom.write_bytes(snes_to_pc(0x1BD1DD), [0xA4, 0x06, 0x82, 0x9E, 0x06, 0x82, 0xFF, 0xFF])
    rom.write_byte(0x180089, 0x01)  # open TR after exit
    rom.write_byte(snes_to_pc(0x0ABFBB), 0x90)
    rom.write_byte(snes_to_pc(0x0280A6), 0xD0)
    rom.write_bytes(snes_to_pc(0x06B2AB), [0xF0, 0xE1, 0x05])

def patch_shuffled_dark_sanc(world, rom, player):
    dark_sanc_entrance = str(world.get_region('Inverted Dark Sanctuary', player).entrances[0].name)
    room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2 = door_addresses[dark_sanc_entrance][1]
    if dark_sanc_entrance == 'Skull Woods Final Section':
        link_y = 0x00F8
    door_index = door_addresses[str(dark_sanc_entrance)][0]
    
    rom.write_byte(0x180241, 0x01)
    rom.write_byte(0x180248, door_index + 1) 
    rom.write_int16(0x180250, room_id)
    rom.write_byte(0x180252, ow_area)
    rom.write_int16s(0x180253, [vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x])
    rom.write_bytes(0x180262, [unknown_1, unknown_2, 0x00])

InconvenientEntrances = {'Turtle Rock': 'Turtle Rock Main',
                         'Misery Mire': 'Misery Mire',
                         'Ice Palace': 'Ice Palace',
                         'Skull Woods Final Section': 'The back of Skull Woods',
                         'Death Mountain Return Cave (West)': 'The SW DM foothills cave',
                         'Mimic Cave': 'Mimic Ledge',
                         'Dark World Hammer Peg Cave': 'The rows of pegs',
                         'Pyramid Fairy': 'The crack on the pyramid'
                         }

OtherEntrances = {'Eastern Palace': 'Eastern Palace',
                  'Elder House (East)': 'Elder House',
                  'Elder House (West)': 'Elder House',
                  'Two Brothers House (East)': 'Eastern Quarreling Brothers\' house',
                  'Old Man Cave (West)': 'The lower DM entrance',
                  'Hyrule Castle Entrance (South)': 'The ground level castle door',
                  'Thieves Town': 'Thieves\' Town',
                  'Bumper Cave (Bottom)': 'The lower Bumper Cave',
                  'Swamp Palace': 'Swamp Palace',
                  'Dark Death Mountain Ledge (West)': 'The East dark DM connector ledge',
                  'Dark Death Mountain Ledge (East)': 'The East dark DM connector ledge',
                  'Superbunny Cave (Top)': 'The summit of dark DM cave',
                  'Superbunny Cave (Bottom)': 'The base of east dark DM',
                  'Hookshot Cave': 'The rock on dark DM',
                  'Desert Palace Entrance (South)': 'The book sealed passage',
                  'Tower of Hera': 'The Tower of Hera',
                  'Two Brothers House (West)': 'The door near the race game',
                  'Old Man Cave (East)': 'The SW-most cave on west DM',
                  'Old Man House (Bottom)': 'A cave with a door on west DM',
                  'Old Man House (Top)': 'The eastmost cave on west DM',
                  'Death Mountain Return Cave (East)': 'The westmost cave on west DM',
                  'Spectacle Rock Cave Peak': 'The highest cave on west DM',
                  'Spectacle Rock Cave': 'The right ledge on west DM',
                  'Spectacle Rock Cave (Bottom)': 'The left ledge on west DM',
                  'Paradox Cave (Bottom)': 'The southmost cave on east DM',
                  'Paradox Cave (Middle)': 'The right paired cave on east DM',
                  'Paradox Cave (Top)': 'The east DM summit cave',
                  'Fairy Ascension Cave (Bottom)': 'The east DM cave behind rocks',
                  'Fairy Ascension Cave (Top)': 'The central ledge on east DM',
                  'Spiral Cave': 'The left ledge on east DM',
                  'Spiral Cave (Bottom)': 'The SWmost cave on east DM',
                  'Palace of Darkness': 'Palace of Darkness',
                  'Hyrule Castle Entrance (West)': 'The left castle door',
                  'Hyrule Castle Entrance (East)': 'The right castle door',
                  'Agahnims Tower': 'The sealed castle door',
                  'Desert Palace Entrance (West)': 'The westmost building in the desert',
                  'Desert Palace Entrance (North)': 'The northmost cave in the desert',
                  'Blinds Hideout': 'Blind\'s old house',
                  'Lake Hylia Fairy': 'A cave NE of Lake Hylia',
                  'Light Hype Fairy': 'The cave south of your house',
                  'Desert Fairy': 'The cave near the desert',
                  'Chicken House': 'The chicken lady\'s house',
                  'Aginahs Cave': 'The open desert cave',
                  'Sahasrahlas Hut': 'The house near armos',
                  'Cave Shop (Lake Hylia)': 'The cave NW Lake Hylia',
                  'Blacksmiths Hut': 'The old smithery',
                  'Sick Kids House': 'The central house in Kakariko',
                  'Lost Woods Gamble': 'A tree trunk door',
                  'Fortune Teller (Light)': 'A building NE of Kakariko',
                  'Snitch Lady (East)': 'A house guarded by a snitch',
                  'Snitch Lady (West)': 'A house guarded by a snitch',
                  'Bush Covered House': 'A house with an uncut lawn',
                  'Tavern (Front)': 'A building with a backdoor',
                  'Light World Bomb Hut': 'A Kakariko building with no door',
                  'Kakariko Shop': 'The old Kakariko shop',
                  'Mini Moldorm Cave': 'The cave south of Lake Hylia',
                  'Long Fairy Cave': 'The eastmost portal cave',
                  'Good Bee Cave': 'The open cave SE Lake Hylia',
                  '20 Rupee Cave': 'The rock SE Lake Hylia',
                  '50 Rupee Cave': 'The rock near the desert',
                  'Ice Rod Cave': 'The sealed cave SE Lake Hylia',
                  'Library': 'The old library',
                  'Potion Shop': 'The witch\'s building',
                  'Dam': 'The old dam',
                  'Lumberjack House': 'The lumberjack house',
                  'Lake Hylia Fortune Teller': 'The building NW Lake Hylia',
                  'Kakariko Gamble Game': 'The old Kakariko gambling den',
                  'Waterfall of Wishing': 'Going behind the waterfall',
                  'Capacity Upgrade': 'The cave on the island',
                  'Bonk Rock Cave': 'The rock pile near Sanctuary',
                  'Graveyard Cave': 'The graveyard ledge',
                  'Checkerboard Cave': 'The NE desert ledge',
                  'Cave 45': 'The ledge south of haunted grove',
                  'Kings Grave': 'The northeastmost grave',
                  'Bonk Fairy (Light)': 'The rock pile near your home',
                  'Hookshot Fairy': 'The left paired cave on east DM',
				  'Bonk Fairy (Dark)': 'The rock pile near the old bomb shop',
                  'Dark Sanctuary Hint': 'The dark sanctuary cave',
                  'Dark Lake Hylia Fairy': 'The cave NE dark Lake Hylia',
                  'C-Shaped House': 'The NE house in Village of Outcasts',
                  'Big Bomb Shop': 'The old bomb shop',
                  'Dark Death Mountain Fairy': 'The SW cave on dark DM',
                  'Dark Lake Hylia Shop': 'The building NW dark Lake Hylia',
                  'Dark World Shop': 'The hammer sealed building',
                  'Red Shield Shop': 'The fenced in building',
                  'Mire Shed': 'The western hut in the mire',
                  'East Dark World Hint': 'The dark cave near the eastmost portal',
                  'Dark Desert Hint': 'The cave east of the mire',
                  'Spike Cave': 'The ledge cave on west dark DM',
                  'Palace of Darkness Hint': 'The building south of Kiki',
                  'Dark Lake Hylia Ledge Spike Cave': 'The rock SE dark Lake Hylia',
                  'Cave Shop (Dark Death Mountain)': 'The base of east dark DM',
                  'Dark World Potion Shop': 'The building near the catfish',
                  'Archery Game': 'The old archery game',
                  'Dark World Lumberjack Shop': 'The northmost Dark World building',
                  'Hype Cave': 'The cave south of the old bomb shop',
                  'Brewery': 'The Village of Outcasts building with no door',
                  'Dark Lake Hylia Ledge Hint': 'The open cave SE dark Lake Hylia',
                  'Chest Game': 'The westmost building in the Village of Outcasts',
                  'Dark Desert Fairy': 'The eastern hut in the mire',
                  'Dark Lake Hylia Ledge Fairy': 'The sealed cave SE dark Lake Hylia',
                  'Fortune Teller (Dark)': 'The building NE the Village of Outcasts'
                  }

InsanityEntrances = {'Sanctuary': 'Sanctuary',
                     'Lumberjack Tree Cave': 'The cave Behind Lumberjacks',
                     'Lost Woods Hideout Stump': 'The stump in Lost Woods',
                     'North Fairy Cave': 'The cave East of Graveyard',
                     'Bat Cave Cave': 'The cave in eastern Kakariko',
                     'Kakariko Well Cave': 'The cave in northern Kakariko',
                     'Hyrule Castle Secret Entrance Stairs': 'The tunnel near the castle',
                     'Skull Woods First Section Door': 'The southeastmost skull',
                     'Skull Woods Second Section Door (East)': 'The central open skull',
                     'Skull Woods Second Section Door (West)': 'The westmost open skull',
                     'Desert Palace Entrance (East)': 'The eastern building in the desert',
                     'Turtle Rock Isolated Ledge Entrance': 'The isolated ledge on east dark DM',
                     'Bumper Cave (Top)': 'The upper Bumper Cave',
                     'Hookshot Cave Back Entrance': 'The stairs on the floating island'
                     }

HintLocations = ['telepathic_tile_eastern_palace',
                 'telepathic_tile_tower_of_hera_floor_4',
                 'telepathic_tile_spectacle_rock',
                 'telepathic_tile_swamp_entrance',
                 'telepathic_tile_thieves_town_upstairs',
                 'telepathic_tile_misery_mire',
                 'telepathic_tile_palace_of_darkness',
                 'telepathic_tile_desert_bonk_torch_room',
                 'telepathic_tile_castle_tower',
                 'telepathic_tile_ice_large_room',
                 'telepathic_tile_turtle_rock',
                 'telepathic_tile_ice_entrace',
                 'telepathic_tile_ice_stalfos_knights_room',
                 'telepathic_tile_tower_of_hera_entrance',
                 'telepathic_tile_south_east_darkworld_cave',
                 'dark_palace_tree_dude',
                 'dark_sanctuary_hint_0',
                 'dark_sanctuary_hint_1',
                 'dark_sanctuary_yes',
                 'dark_sanctuary_hint_2']

InconvenientLocations = ['Spike Cave',
                         'Sahasrahla',
                         'Purple Chest',
                         'Swamp Left',
                         'Mire Left',
                         'Tower of Hera - Big Key Chest',
                         'Eastern Palace - Big Key Chest',
                         'Thieves\' Town - Big Chest',
                         'Ice Palace - Big Chest',
                         'Ganons Tower - Big Chest',
                         'Magic Bat']
RelevantItems = ['Bow',
                 'Book of Mudora',
                 'Hammer',
                 'Hookshot',
                 'Magic Mirror',
                 'Ocarina',
                 'Pegasus Boots',
                 'Power Glove',
                 'Cape',
                 'Mushroom',
                 'Shovel',
                 'Lamp',
                 'Magic Powder',
                 'Moon Pearl',
                 'Cane of Somaria',
                 'Fire Rod',
                 'Flippers',
                 'Ice Rod',
                 'Titans Mitts',
                 'Ether',
                 'Bombos',
                 'Quake',
                 'Bottle',
                 'Bottle (Red Potion)',
                 'Bottle (Green Potion)',
                 'Bottle (Blue Potion)',
                 'Bottle (Fairy)',
                 'Bottle (Bee)',
                 'Bottle (Good Bee)',
                 'Master Sword',
                 'Tempered Sword',
                 'Fighter Sword',
                 'Golden Sword',
                 'Progressive Sword',
                 'Progressive Glove',
                 'Master Sword',
                 'Power Star',
                 'Triforce Piece',
                 'Single Arrow',
                 'Blue Mail',
                 'Red Mail',
                 'Progressive Armor',
                 'Blue Boomerang',
                 'Red Boomerang',
                 'Blue Shield',
                 'Red Shield',
                 'Mirror Shield',
                 'Progressive Shield',
                 'Bug Catching Net',
                 'Cane of Byrna',
                 'Magic Upgrade (1/2)',
                 'Magic Upgrade (1/4)'
                 ]

KeysanityItems = ['Small Key (Eastern Palace)',
                  'Big Key (Eastern Palace)',
                  'Small Key (Escape)',
				  'Small Key (Desert Palace)',
                  'Big Key (Desert Palace)',
				  'Small Key (Tower of Hera)',
                  'Big Key (Tower of Hera)',
				  'Small Key (Agahnims Tower)',
				  'Small Key (Palace of Darkness)',
                  'Big Key (Palace of Darkness)',
				  'Small Key (Thieves Town)',
                  'Big Key (Thieves Town)',
				  'Small Key (Swamp Palace)',
                  'Big Key (Swamp Palace)',
				  'Small Key (Skull Woods)',
                  'Big Key (Skull Woods)',
				  'Small Key (Ice Palace)',
                  'Big Key (Ice Palace)',
                  'Small Key (Misery Mire)',
                  'Big Key (Misery Mire)',
                  'Small Key (Turtle Rock)',
                  'Big Key (Turtle Rock)',
                  'Small Key (Ganons Tower)',
                  'Big Key (Ganons Tower)'
				  ]
