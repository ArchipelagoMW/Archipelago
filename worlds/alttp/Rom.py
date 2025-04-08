from __future__ import annotations

import Utils
import worlds.Files

LTTPJPN10HASH: str = "03a63945398191337e896e5771f77173"
RANDOMIZERBASEHASH: str = "8704fb9b9fa4fad52d4d2f9a95fb5360"
ROM_PLAYER_LIMIT: int = 255

import io
import json
import hashlib
import logging
import os
import random
import struct
import subprocess
import threading
import concurrent.futures
import bsdiff4
from typing import Collection, Optional, List, SupportsIndex

from BaseClasses import CollectionState, Region, Location, MultiWorld
from Utils import local_path, user_path, int16_as_bytes, int32_as_bytes, snes_to_pc, is_frozen, parse_yaml, read_snes_rom

from .Shops import ShopType, ShopPriceType
from .Dungeons import dungeon_music_addresses
from .Regions import old_location_address_to_new_location_address, key_drop_data
from .Text import MultiByteTextMapper, text_addresses, Credits, TextTable
from .Text import Uncle_texts, Ganon1_texts, TavernMan_texts, Sahasrahla2_texts, Triforce_texts, \
    Blind_texts, \
    BombShop2_texts, junk_texts
from .Text import KingsReturn_texts, Sanctuary_texts, Kakariko_texts, Blacksmiths_texts, \
    DeathMountain_texts, \
    LostWoods_texts, WishingWell_texts, DesertPalace_texts, MountainTower_texts, LinksHouse_texts, Lumberjacks_texts, \
    SickKid_texts, FluteBoy_texts, Zora_texts, MagicShop_texts, Sahasrahla_names
from .Items import item_table, item_name_groups, progression_items
from .EntranceShuffle import door_addresses
from .Options import small_key_shuffle

try:
    from maseya import z3pr
    from maseya.z3pr.palette_randomizer import build_offset_collections
except:
    z3pr = None

try:
    import xxtea
except:
    xxtea = None

enemizer_logger = logging.getLogger("Enemizer")


class LocalRom:

    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_snes_rom(stream)
        if patch:
            self.patch_base_rom()
            self.orig_buffer = self.buffer.copy()
        if vanillaRom:
            with open(vanillaRom, 'rb') as vanillaStream:
                self.orig_buffer = read_snes_rom(vanillaStream)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytearray:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values: Collection[SupportsIndex]) -> None:
        self.buffer[startaddress:startaddress + len(values)] = values

    def encrypt_range(self, startaddress: int, length: int, key: bytes):
        for i in range(0, length, 8):
            data = bytes(self.read_bytes(startaddress + i, 8))
            data = xxtea.encrypt(data, key, padding=False)
            self.write_bytes(startaddress + i, bytearray(data))

    def encrypt(self, world, player):
        global xxtea
        if xxtea is None:
            # cause crash to provide traceback
            import xxtea

        local_random = world.per_slot_randoms[player]
        key = bytes(local_random.getrandbits(8 * 16).to_bytes(16, 'big'))
        self.write_bytes(0x1800B0, bytearray(key))
        self.write_int16(0x180087, 1)

        itemtable = []
        locationtable = []
        itemplayertable = []
        for i in range(168):
            itemtable.append(self.read_byte(0xE96E + (i * 3)))
            itemplayertable.append(self.read_byte(0x186142 + (i * 3)))
            locationtable.append(self.read_byte(0xe96C + (i * 3)))
            locationtable.append(self.read_byte(0xe96D + (i * 3)))
        self.write_bytes(0xE96C, locationtable)
        self.write_bytes(0xE96C + 0x150, itemtable)
        self.encrypt_range(0xE96C + 0x150, 168, key)
        self.write_bytes(0x186140, [0] * 0x150)
        self.write_bytes(0x186140 + 0x150, itemplayertable)
        self.encrypt_range(0x186140 + 0x150, 168, key)
        self.encrypt_range(0x186338, 56, key)
        self.encrypt_range(0x180000, 32, key)
        self.encrypt_range(0x180140, 32, key)
        self.encrypt_range(0xEDA1, 8, key)

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())

    @staticmethod
    def verify(buffer, expected: str = RANDOMIZERBASEHASH) -> bool:
        buffermd5 = hashlib.md5()
        buffermd5.update(buffer)
        return expected == buffermd5.hexdigest()

    def patch_base_rom(self):
        if os.path.isfile(user_path('basepatch.sfc')):
            with open(user_path('basepatch.sfc'), 'rb') as stream:
                buffer = bytearray(stream.read())

            if self.verify(buffer):
                self.buffer = buffer
                return

        with open(local_path("data", "basepatch.bsdiff4"), "rb") as f:
            delta = f.read()

        buffer = bsdiff4.patch(get_base_rom_bytes(), delta)
        if self.verify(buffer):
            self.buffer = bytearray(buffer)
            with open(user_path('basepatch.sfc'), 'wb') as stream:
                stream.write(buffer)
            return
        raise RuntimeError('Base patch unverified.  Unable to continue.')

    def write_crc(self):
        crc = (sum(self.buffer[:0x7FDC] + self.buffer[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])

    def get_hash(self) -> str:
        h = hashlib.md5()
        h.update(self.buffer)
        return h.hexdigest()

    def write_int16(self, address: int, value: int):
        self.write_bytes(address, int16_as_bytes(value))

    def write_int32(self, address: int, value: int):
        self.write_bytes(address, int32_as_bytes(value))

    def write_int16s(self, startaddress: int, values):
        for i, value in enumerate(values):
            self.write_int16(startaddress + (i * 2), value)

    def write_int32s(self, startaddress: int, values):
        for i, value in enumerate(values):
            self.write_int32(startaddress + (i * 4), value)


check_lock = threading.Lock()


def check_enemizer(enemizercli):
    if getattr(check_enemizer, "done", None):
        return
    if not os.path.exists(enemizercli) and not os.path.exists(enemizercli + ".exe"):
        raise Exception(f"Enemizer not found at {enemizercli}, please install it."
                        f"Such as https://github.com/Ijwu/Enemizer/releases")

    with check_lock:
        # some time may have passed since the lock was acquired, as such a quick re-check doesn't hurt
        if getattr(check_enemizer, "done", None):
            return
        wanted_version = (7, 1, 0)
        # version info is saved on the lib, for some reason
        library_info = os.path.join(os.path.dirname(enemizercli), "EnemizerCLI.Core.deps.json")
        with open(library_info) as f:
            info = json.load(f)

        for lib in info["libraries"]:
            if lib.startswith("EnemizerLibrary/"):
                version = lib.split("/")[-1]
                version = tuple(int(element) for element in version.split("."))
                enemizer_logger.debug(f"Found Enemizer version {version}")
                if version < wanted_version:
                    raise Exception(
                        f"Enemizer found at {enemizercli} is outdated ({version}) < ({wanted_version}), "
                        f"please update your Enemizer. "
                        f"Such as from https://github.com/Ijwu/Enemizer/releases")
                break
        else:
            raise Exception(f"Could not find Enemizer library version information in {library_info}")

    check_enemizer.done = True


def apply_random_sprite_on_event(rom: LocalRom, sprite, local_random, allow_random_on_event, sprite_pool):
    userandomsprites = False
    if sprite and not isinstance(sprite, Sprite):
        sprite = sprite.lower()
        userandomsprites = sprite.startswith('randomon')

        racerom = rom.read_byte(0x180213)
        if allow_random_on_event or not racerom:
            # Changes to this byte for race rom seeds are only permitted on initial rolling of the seed.
            # However, if the seed is not a racerom seed, then it is always allowed.
            rom.write_byte(0x186381, 0x00 if userandomsprites else 0x01)

        onevent = 0
        if sprite == 'randomonall':
            onevent = 0xFFFF  # Support all current and future events that can cause random sprite changes.
        elif sprite == 'randomonnone':
            # Allows for opting into random on events on race rom seeds, without actually enabling any of the events initially.
            onevent = 0x0000
        elif sprite == 'randomonrandom':
            # Allows random to take the wheel on which events apply. (at least one event will be applied.)
            onevent = local_random.randint(0x0001, 0x003F)
        elif userandomsprites:
            onevent = 0x01 if 'hit' in sprite else 0x00
            onevent += 0x02 if 'enter' in sprite else 0x00
            onevent += 0x04 if 'exit' in sprite else 0x00
            onevent += 0x08 if 'slash' in sprite else 0x00
            onevent += 0x10 if 'item' in sprite else 0x00
            onevent += 0x20 if 'bonk' in sprite else 0x00

        rom.write_int16(0x18637F, onevent)

        sprite = Sprite(sprite) if os.path.isfile(sprite) else Sprite.get_sprite_from_name(sprite, local_random)

    # write link sprite if required
    if sprite:
        sprites = list()
        sprite.write_to_rom(rom)

        _populate_sprite_table()
        if userandomsprites:
            if sprite_pool:
                if isinstance(sprite_pool, str):
                    sprite_pool = sprite_pool.split(':')
                for spritename in sprite_pool:
                    sprite = Sprite(spritename) if os.path.isfile(spritename) else Sprite.get_sprite_from_name(
                        spritename, local_random)
                    if sprite:
                        sprites.append(sprite)
                    else:
                        logging.info(f"Sprite {spritename} was not found.")
            else:
                sprites = list(set(_sprite_table.values()))  # convert to list and remove dupes
        else:
            sprites.append(sprite)
        if sprites:
            while len(sprites) < 32:
                sprites.extend(sprites)
            local_random.shuffle(sprites)

            for i, sprite in enumerate(sprites[:32]):
                if not i and not userandomsprites:
                    continue
                rom.write_bytes(0x300000 + (i * 0x8000), sprite.sprite)
                rom.write_bytes(0x307000 + (i * 0x8000), sprite.palette)
                rom.write_bytes(0x307078 + (i * 0x8000), sprite.glove_palette)


def patch_enemizer(world, rom: LocalRom, enemizercli, output_directory):
    player = world.player
    multiworld = world.multiworld
    check_enemizer(enemizercli)
    randopatch_path = os.path.abspath(os.path.join(output_directory, f'enemizer_randopatch_{player}.sfc'))
    options_path = os.path.abspath(os.path.join(output_directory, f'enemizer_options_{player}.json'))
    enemizer_output_path = os.path.abspath(os.path.join(output_directory, f'enemizer_output_{player}.sfc'))

    # write options file for enemizer
    options = {
        'RandomizeEnemies': multiworld.enemy_shuffle[player].value,
        'RandomizeEnemiesType': 3,
        'RandomizeBushEnemyChance': multiworld.bush_shuffle[player].value,
        'RandomizeEnemyHealthRange': multiworld.enemy_health[player] != 'default',
        'RandomizeEnemyHealthType': {'default': 0, 'easy': 0, 'normal': 1, 'hard': 2, 'expert': 3}[
            multiworld.enemy_health[player].current_key],
        'OHKO': False,
        'RandomizeEnemyDamage': multiworld.enemy_damage[player] != 'default',
        'AllowEnemyZeroDamage': True,
        'ShuffleEnemyDamageGroups': multiworld.enemy_damage[player] != 'default',
        'EnemyDamageChaosMode': multiworld.enemy_damage[player] == 'chaos',
        'EasyModeEscape': multiworld.mode[player] == "standard",
        'EnemiesAbsorbable': False,
        'AbsorbableSpawnRate': 10,
        'AbsorbableTypes': {
            'FullMagic': True, 'SmallMagic': True, 'Bomb_1': True, 'BlueRupee': True, 'Heart': True, 'BigKey': True,
            'Key': True,
            'Fairy': True, 'Arrow_10': True, 'Arrow_5': True, 'Bomb_8': True, 'Bomb_4': True, 'GreenRupee': True,
            'RedRupee': True
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
        'RandomizeDungeonPalettes': False,
        'SetBlackoutMode': False,
        'RandomizeOverworldPalettes': False,
        'RandomizeSpritePalettes': False,
        'SetAdvancedSpritePalettes': False,
        'PukeMode': False,
        'NegativeMode': False,
        'GrayscaleMode': False,
        'GenerateSpoilers': False,
        'RandomizeLinkSpritePalette': False,
        'RandomizePots': multiworld.pot_shuffle[player].value,
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
        'RandomizeTileTrapPattern': False,
        'RandomizeTileTrapFloorTile': False,
        'AllowKillableThief': multiworld.killable_thieves[player].value,
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
            'EasternPalace': world.dungeons["Eastern Palace"].boss.enemizer_name,
            'DesertPalace': world.dungeons["Desert Palace"].boss.enemizer_name,
            'TowerOfHera': world.dungeons["Tower of Hera"].boss.enemizer_name,
            'AgahnimsTower': 'Agahnim',
            'PalaceOfDarkness': world.dungeons["Palace of Darkness"].boss.enemizer_name,
            'SwampPalace': world.dungeons["Swamp Palace"].boss.enemizer_name,
            'SkullWoods': world.dungeons["Skull Woods"].boss.enemizer_name,
            'ThievesTown': world.dungeons["Thieves Town"].boss.enemizer_name,
            'IcePalace': world.dungeons["Ice Palace"].boss.enemizer_name,
            'MiseryMire': world.dungeons["Misery Mire"].boss.enemizer_name,
            'TurtleRock': world.dungeons["Turtle Rock"].boss.enemizer_name,
            'GanonsTower1':
                world.dungeons["Ganons Tower" if multiworld.mode[player] != 'inverted' else
                               "Inverted Ganons Tower"].bosses['bottom'].enemizer_name,
            'GanonsTower2':
                world.dungeons["Ganons Tower" if multiworld.mode[player] != 'inverted' else
                               "Inverted Ganons Tower"].bosses['middle'].enemizer_name,
            'GanonsTower3':
                world.dungeons["Ganons Tower" if multiworld.mode[player] != 'inverted' else
                               "Inverted Ganons Tower"].bosses['top'].enemizer_name,
            'GanonsTower4': 'Agahnim2',
            'Ganon': 'Ganon',
        }
    }

    rom.write_to_file(randopatch_path)

    with open(options_path, 'w') as f:
        json.dump(options, f)

    max_enemizer_tries = 5
    for i in range(max_enemizer_tries):
        enemizer_seed = str(multiworld.per_slot_randoms[player].randint(0, 999999999))
        enemizer_command = [os.path.abspath(enemizercli),
                            '--rom', randopatch_path,
                            '--seed', enemizer_seed,
                            '--binary',
                            '--enemizer', options_path,
                            '--output', enemizer_output_path]

        p_open = subprocess.Popen(enemizer_command,
                                  cwd=os.path.dirname(enemizercli),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True)

        enemizer_logger.debug(
            f"Enemizer attempt {i + 1} of {max_enemizer_tries} for player {player} using enemizer seed {enemizer_seed}")
        for stdout_line in iter(p_open.stdout.readline, ""):
            if i == max_enemizer_tries - 1:
                enemizer_logger.warning(stdout_line.rstrip())
            else:
                enemizer_logger.debug(stdout_line.rstrip())
        p_open.stdout.close()

        return_code = p_open.wait()
        if return_code:
            if i == max_enemizer_tries - 1:
                raise subprocess.CalledProcessError(return_code, enemizer_command)
            continue

        for j in range(i + 1, max_enemizer_tries):
            multiworld.per_slot_randoms[player].randint(0, 999999999)
            # Sacrifice all remaining random numbers that would have been used for unused enemizer tries.
            # This allows for future enemizer bug fixes to NOT affect the rest of the seed's randomness
        break

    rom.read_from_file(enemizer_output_path)
    os.remove(enemizer_output_path)

    if world.dungeons["Thieves Town"].boss.enemizer_name == "Blind":
        rom.write_byte(0x04DE81, 6)
        rom.write_byte(0x1B0101, 0)  # Do not close boss room door on entry.

    # Moblins attached to "key drop" locations crash the game when dropping their item when Key Drop Shuffle is on.
    # Replace them with a Slime enemy if they are placed.
    if multiworld.key_drop_shuffle[player]:
        key_drop_enemies = {
            0x4DA20, 0x4DA5C, 0x4DB7F, 0x4DD73, 0x4DDC3, 0x4DE07, 0x4E201,
            0x4E20A, 0x4E326, 0x4E4F7, 0x4E687, 0x4E70C, 0x4E7C8, 0x4E7FA
        }
        for enemy in key_drop_enemies:
            if rom.read_byte(enemy) == 0x12:
                logging.debug(f"Moblin found and replaced at {enemy} in world {player}")
                rom.write_byte(enemy, 0x8F)

    for used in (randopatch_path, options_path):
        try:
            os.remove(used)
        except OSError:
            pass


tile_list_lock = threading.Lock()
_tile_collection_table = []


def _populate_tile_sets():
    with tile_list_lock:
        if not _tile_collection_table:
            def load_tileset_from_file(file):
                tileset = TileSet(file)
                _tile_collection_table.append(tileset)

            with concurrent.futures.ThreadPoolExecutor() as pool:
                for dir in [local_path('data', 'tiles')]:
                    for file in os.listdir(dir):
                        pool.submit(load_tileset_from_file, os.path.join(dir, file))


class TileSet:
    def __init__(self, filename):
        with open(filename, 'rt', encoding='utf-8-sig') as file:
            jsondata = json.load(file)
        self.speed = jsondata['Speed']
        self.tiles = jsondata['Items']
        self.name = os.path.basename(os.path.splitext(filename)[0])

    def __hash__(self):
        return hash(self.name)

    def get_bytes(self):
        data = []
        for tile in self.tiles:
            data.append((tile['x'] + 3) * 16)
        while len(data) < 22:
            data.append(0)
        for tile in self.tiles:
            data.append((tile['y'] + 4) * 16)
        return data

    def get_speed(self):
        return self.speed

    def get_len(self):
        return len(self.tiles)

    @staticmethod
    def get_random_tile_set(localrandom=random):
        _populate_tile_sets()
        tile_sets = list(set(_tile_collection_table))
        tile_sets.sort(key=lambda x: x.name)
        return localrandom.choice(tile_sets)


sprite_list_lock = threading.Lock()
_sprite_table = {}


def _populate_sprite_table():
    with sprite_list_lock:
        if not _sprite_table:
            def load_sprite_from_file(file):
                sprite = Sprite(file)
                if sprite.valid:
                    _sprite_table[sprite.name.lower()] = sprite
                    _sprite_table[os.path.basename(file).split(".")[0].lower()] = sprite  # alias for filename base
                else:
                    logging.debug(f"Spritefile {file} could not be loaded as a valid sprite.")

            with concurrent.futures.ThreadPoolExecutor() as pool:
                sprite_paths = [user_path('data', 'sprites', 'alttpr'), user_path('data', 'sprites', 'custom')]
                for dir in [dir for dir in sprite_paths if os.path.isdir(dir)]:
                    for file in os.listdir(dir):
                        pool.submit(load_sprite_from_file, os.path.join(dir, file))

            if "link" not in _sprite_table:
                logging.info("Link sprite was not loaded. Loading link from base rom")
                load_sprite_from_file(get_base_rom_path())


class Sprite():
    sprite_size = 28672
    palette_size = 120
    glove_size = 4
    author_name: Optional[str] = None
    base_data: bytes

    def __init__(self, filename):
        if not hasattr(Sprite, "base_data"):
            self.get_vanilla_sprite_data()
        with open(filename, 'rb') as file:
            filedata = file.read()
        self.name = os.path.basename(filename)
        self.valid = True
        if filename.endswith(".apsprite"):
            self.from_ap_sprite(filedata)
        elif len(filedata) == 0x7000:
            # sprite file with graphics and without palette data
            self.sprite = filedata[:0x7000]
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
        elif len(filedata) in [0x100000, 0x200000, 0x400000]:
            # full rom with patched sprite, extract it
            self.sprite = filedata[0x80000:0x87000]
            self.palette = filedata[0xDD308:0xDD380]
            self.glove_palette = filedata[0xDEDF5:0xDEDF9]
            h = hashlib.md5()
            h.update(filedata)
            if h.hexdigest() == LTTPJPN10HASH:
                self.name = "Link"
                self.author_name = "Nintendo"
        elif filedata.startswith(b'ZSPR'):
            self.from_zspr(filedata, filename)
        else:
            self.valid = False

    def get_vanilla_sprite_data(self):
        file_name = get_base_rom_path()
        base_rom_bytes = bytes(read_snes_rom(open(file_name, "rb")))
        Sprite.sprite = base_rom_bytes[0x80000:0x87000]
        Sprite.palette = base_rom_bytes[0xDD308:0xDD380]
        Sprite.glove_palette = base_rom_bytes[0xDEDF5:0xDEDF9]
        Sprite.base_data = Sprite.sprite + Sprite.palette + Sprite.glove_palette

    def from_ap_sprite(self, filedata):
        # noinspection PyBroadException
        try:
            obj = parse_yaml(filedata.decode("utf-8-sig"))
            if obj["min_format_version"] > 1:
                raise Exception("Sprite file requires an updated reader.")
            self.author_name = obj["author"]
            self.name = obj["name"]
            if obj["data"]:  # skip patching for vanilla content
                data = bsdiff4.patch(Sprite.base_data, obj["data"])
                self.sprite = data[:self.sprite_size]
                self.palette = data[self.sprite_size:self.palette_size]
                self.glove_palette = data[self.sprite_size + self.palette_size:]
        except Exception:
            logger = logging.getLogger("apsprite")
            logger.exception("Error parsing apsprite file")
            self.valid = False

    @property
    def author_game_display(self) -> str:
        name = getattr(self, "_author_game_display", "")
        if not name:
            name = self.author_name

        # At this point, may need some filtering to displayable characters
        return name

    def to_ap_sprite(self, path):
        import yaml
        payload = {"format_version": 1,
                   "min_format_version": 1,
                   "sprite_version": 1,
                   "name": self.name,
                   "author": self.author_name,
                   "game": "A Link to the Past",
                   "data": self.get_delta()}
        with open(path, "w") as f:
            f.write(yaml.safe_dump(payload))

    def get_delta(self):
        modified_data = self.sprite + self.palette + self.glove_palette
        return bsdiff4.diff(Sprite.base_data, modified_data)

    def from_zspr(self, filedata, filename):
        result = self.parse_zspr(filedata, 1)
        if result is None:
            self.valid = False
            return
        (sprite, palette, self.name, self.author_name, self._author_game_display) = result
        if self.name == "":
            self.name = os.path.split(filename)[1].split(".")[0]

        if len(sprite) != 0x7000:
            self.valid = False
            return
        self.sprite = sprite
        if len(palette) == 0:
            pass
        elif len(palette) == 0x78:
            self.palette = palette
        elif len(palette) == 0x7C:
            self.palette = palette[:0x78]
            self.glove_palette = palette[0x78:]
        else:
            self.valid = False

    @staticmethod
    def get_sprite_from_name(name: str, local_random=random) -> Optional[Sprite]:
        _populate_sprite_table()
        name = name.lower()
        if name.startswith('random'):
            sprites = list(set(_sprite_table.values()))
            sprites.sort(key=lambda x: x.name)
            return local_random.choice(sprites)
        return _sprite_table.get(name, None)

    @staticmethod
    def default_link_sprite():
        return Sprite(local_path('data', 'default.apsprite'))

    def decode8(self, pos):
        arr = [[0 for _ in range(8)] for _ in range(8)]
        for y in range(8):
            for x in range(8):
                position = 1 << (7 - x)
                val = 0
                if self.sprite[pos + 2 * y] & position:
                    val += 1
                if self.sprite[pos + 2 * y + 1] & position:
                    val += 2
                if self.sprite[pos + 2 * y + 16] & position:
                    val += 4
                if self.sprite[pos + 2 * y + 17] & position:
                    val += 8
                arr[y][x] = val
        return arr

    def decode16(self, pos):
        arr = [[0 for _ in range(16)] for _ in range(16)]
        top_left = self.decode8(pos)
        top_right = self.decode8(pos + 0x20)
        bottom_left = self.decode8(pos + 0x200)
        bottom_right = self.decode8(pos + 0x220)
        for x in range(8):
            for y in range(8):
                arr[y][x] = top_left[y][x]
                arr[y][x + 8] = top_right[y][x]
                arr[y + 8][x] = bottom_left[y][x]
                arr[y + 8][x + 8] = bottom_right[y][x]
        return arr

    @staticmethod
    def parse_zspr(filedata, expected_kind):
        logger = logging.getLogger("ZSPR")
        headerstr = "<4xBHHIHIHH6x"
        headersize = struct.calcsize(headerstr)
        if len(filedata) < headersize:
            return None
        version, csum, icsum, sprite_offset, sprite_size, palette_offset, palette_size, kind = struct.unpack_from(
            headerstr, filedata)
        if version not in [1]:
            logger.error("Error parsing ZSPR file: Version %g not supported", version)
            return None
        if kind != expected_kind:
            return None

        stream = io.BytesIO(filedata)
        stream.seek(headersize)

        def read_utf16le(stream):
            """Decodes a null-terminated UTF-16_LE string of unknown size from a stream"""
            raw = bytearray()
            while True:
                char = stream.read(2)
                if char in [b"", b"\x00\x00"]:
                    break
                raw += char
            return raw.decode("utf-16_le")

        # noinspection PyBroadException
        try:
            sprite_name = read_utf16le(stream)
            author_name = read_utf16le(stream)
            author_credits_name = stream.read().split(b"\x00", 1)[0].decode()

            # Ignoring the Author Rom name for the time being.

            real_csum = sum(filedata) % 0x10000
            if real_csum != csum or real_csum ^ 0xFFFF != icsum:
                logger.warning("ZSPR file has incorrect checksum. It may be corrupted.")

            sprite = filedata[sprite_offset:sprite_offset + sprite_size]
            palette = filedata[palette_offset:palette_offset + palette_size]

            if len(sprite) != sprite_size or len(palette) != palette_size:
                logger.error("Error parsing ZSPR file: Unexpected end of file")
                return None

            return sprite, palette, sprite_name, author_name, author_credits_name

        except Exception:
            logger.exception("Error parsing ZSPR file")
            return None

    def decode_palette(self):
        """Returns the palettes as an array of arrays of 15 colors"""

        def array_chunk(arr, size):
            return list(zip(*[iter(arr)] * size))

        def make_int16(pair):
            return pair[1] << 8 | pair[0]

        def expand_color(i):
            return (i & 0x1F) * 8, (i >> 5 & 0x1F) * 8, (i >> 10 & 0x1F) * 8

        # turn palette data into a list of RGB tuples with 8 bit values
        palette_as_colors = [expand_color(make_int16(chnk)) for chnk in array_chunk(self.palette, 2)]

        # split into palettes of 15 colors
        return array_chunk(palette_as_colors, 15)

    def __hash__(self):
        return hash(self.name)

    def write_to_rom(self, rom: LocalRom):
        if not self.valid:
            logging.warning("Tried writing invalid sprite to rom, skipping.")
            return
        rom.write_bytes(0x80000, self.sprite)
        rom.write_bytes(0xDD308, self.palette)
        rom.write_bytes(0xDEDF5, self.glove_palette)
        rom.write_bytes(0x300000, self.sprite)
        rom.write_bytes(0x307000, self.palette)
        rom.write_bytes(0x307078, self.glove_palette)


bonk_addresses = [0x4CF6C, 0x4CFBA, 0x4CFE0, 0x4CFFB, 0x4D018, 0x4D01B, 0x4D028, 0x4D03C, 0x4D059, 0x4D07A,
                  0x4D09E, 0x4D0A8, 0x4D0AB, 0x4D0AE, 0x4D0BE, 0x4D0DD,
                  0x4D16A, 0x4D1E5, 0x4D1EE, 0x4D20B, 0x4CBBF, 0x4CBBF, 0x4CC17, 0x4CC1A, 0x4CC4A, 0x4CC4D,
                  0x4CC53, 0x4CC69, 0x4CC6F, 0x4CC7C, 0x4CCEF, 0x4CD51,
                  0x4CDC0, 0x4CDC3, 0x4CDC6, 0x4CE37, 0x4D2DE, 0x4D32F, 0x4D355, 0x4D367, 0x4D384, 0x4D387,
                  0x4D397, 0x4D39E, 0x4D3AB, 0x4D3AE, 0x4D3D1, 0x4D3D7,
                  0x4D3F8, 0x4D416, 0x4D420, 0x4D423, 0x4D42D, 0x4D449, 0x4D48C, 0x4D4D9, 0x4D4DC, 0x4D4E3,
                  0x4D504, 0x4D507, 0x4D55E, 0x4D56A]


def get_nonnative_item_sprite(code: int) -> int:
    if 84173 >= code >= 84007:  # LttP item in SMZ3
        return code - 84000
    return 0x6B  # set all non-native sprites to Power Star as per 13 to 2 vote at
    # https://discord.com/channels/731205301247803413/827141303330406408/852102450822905886


def patch_rom(world: MultiWorld, rom: LocalRom, player: int, enemized: bool):
    local_world = world.worlds[player]
    local_random = local_world.random

    # patch items

    for location in world.get_locations(player):
        if location.address is None or location.shop_slot is not None:
            continue

        itemid = location.item.code if location.item is not None else 0x5A

        if not location.crystal:

            if location.item is not None:
                if not location.native_item:
                    if location.item.trap:
                        itemid = 0x5A  # Nothing, which disguises
                    else:
                        itemid = get_nonnative_item_sprite(location.item.code)
                # Keys in their native dungeon should use the orignal item code for keys
                elif location.parent_region.dungeon:
                    if location.parent_region.dungeon.is_dungeon_item(location.item):
                        if location.item.bigkey:
                            itemid = 0x32
                        elif location.item.smallkey:
                            itemid = 0x24
                        elif location.item.map:
                            itemid = 0x33
                        elif location.item.compass:
                            itemid = 0x25
                # if world.worlds[player].remote_items:  # remote items does not currently work
                #     itemid = list(location_table.keys()).index(location.name) + 1
                #     assert itemid < 0x100
                #     rom.write_byte(location.player_address, 0xFF)
                if location.item.player != player:
                    if location.player_address is not None:
                        rom.write_byte(location.player_address, min(location.item.player, ROM_PLAYER_LIMIT))
                    else:
                        itemid = 0x5A
            location_address = old_location_address_to_new_location_address.get(location.address, location.address)
            rom.write_byte(location_address, itemid)
        else:
            # crystals
            for address, value in zip(location.address, itemid):
                rom.write_byte(address, value)

            # patch music
            music_addresses = dungeon_music_addresses[location.name]
            if world.map_shuffle[player]:
                music = local_random.choice([0x11, 0x16])
            else:
                music = 0x11 if 'Pendant' in location.item.name else 0x16
            for music_address in music_addresses:
                rom.write_byte(music_address, music)

    if world.map_shuffle[player]:
        rom.write_byte(0x155C9, local_random.choice([0x11, 0x16]))  # Randomize GT music too with map shuffle

    # patch entrance/exits/holes
    for region in world.regions:
        for exit in region.exits:
            if exit.target is not None and exit.player == player:
                if isinstance(exit.addresses, tuple):
                    offset = exit.target
                    room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2 = exit.addresses
                    # room id is deliberately not written

                    rom.write_byte(0x15B8C + offset, ow_area)
                    rom.write_int16(0x15BDB + 2 * offset, vram_loc)
                    rom.write_int16(0x15C79 + 2 * offset, scroll_y)
                    rom.write_int16(0x15D17 + 2 * offset, scroll_x)

                    # for positioning fixups we abuse the roomid as a way of identifying which exit data we are appling
                    # Thanks to Zarby89 for originally finding these values
                    # todo fix screen scrolling

                    if world.entrance_shuffle[player] != 'insanity' and \
                            exit.name in {'Eastern Palace Exit', 'Tower of Hera Exit', 'Thieves Town Exit',
                                          'Skull Woods Final Section Exit', 'Ice Palace Exit', 'Misery Mire Exit',
                                          'Palace of Darkness Exit', 'Swamp Palace Exit', 'Ganons Tower Exit',
                                          'Desert Palace Exit (North)', 'Agahnims Tower Exit', 'Spiral Cave Exit (Top)',
                                          'Superbunny Cave Exit (Bottom)', 'Turtle Rock Ledge Exit (East)'} and \
                            (world.glitches_required[player] not in ['hybrid_major_glitches', 'no_logic'] or
                                exit.name not in {'Palace of Darkness Exit', 'Tower of Hera Exit', 'Swamp Palace Exit'}):
                        # For exits that connot be reached from another, no need to apply offset fixes.
                        rom.write_int16(0x15DB5 + 2 * offset, link_y)  # same as final else
                    elif room_id == 0x0059 and local_world.fix_skullwoods_exit:
                        rom.write_int16(0x15DB5 + 2 * offset, 0x00F8)
                    elif room_id == 0x004a and local_world.fix_palaceofdarkness_exit:
                        rom.write_int16(0x15DB5 + 2 * offset, 0x0640)
                    elif room_id == 0x00d6 and local_world.fix_trock_exit:
                        rom.write_int16(0x15DB5 + 2 * offset, 0x0134)
                    elif room_id == 0x000c and world.shuffle_ganon:  # fix ganons tower exit point
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
    if world.mode[player] == 'inverted':
        patch_shuffled_dark_sanc(world, rom, player)

    write_custom_shops(rom, world, player)

    def credits_digit(num):
        # top: $54 is 1, 55 2, etc , so 57=4, 5C=9
        # bot: $7A is 1, 7B is 2, etc so 7D=4, 82=9 (zero unknown...)
        return 0x53 + int(num), 0x79 + int(num)

    credits_total = 216
    if world.retro_caves[player]:  # Old man cave and Take any caves will count towards collection rate.
        credits_total += 5
    if world.shop_item_slots[player]:  # Potion shop only counts towards collection rate if included in the shuffle.
        credits_total += 30 if world.include_witch_hut[player] else 27
    if world.shuffle_capacity_upgrades[player]:
        credits_total += 2

    rom.write_byte(0x187010, credits_total)  # dynamic credits

    if world.key_drop_shuffle[player]:
        rom.write_byte(0x140000, 1)  # enable key drop shuffle
        credits_total += len(key_drop_data)
        # update dungeon counters
        rom.write_byte(0x187001, 12)  # Hyrule Castle
        rom.write_byte(0x187002, 8)  # Eastern Palace
        rom.write_byte(0x187003, 9)  # Desert Palace
        rom.write_byte(0x187004, 4)  # Agahnims Tower
        rom.write_byte(0x187005, 15)  # Swamp Palace
        rom.write_byte(0x187007, 11)  # Misery Mire
        rom.write_byte(0x187008, 10)  # Skull Woods
        rom.write_byte(0x187009, 12)  # Ice Palace
        rom.write_byte(0x18700B, 10)  # Thieves Town
        rom.write_byte(0x18700C, 14)  # Turtle Rock
        rom.write_byte(0x18700D, 31)  # Ganons Tower
        # update credits GT Big Key counter
        gt_bigkey_top, gt_bigkey_bottom = credits_digit(5)
        rom.write_byte(0x118B6A, gt_bigkey_top)
        rom.write_byte(0x118B88, gt_bigkey_bottom)



    # collection rate address: 238C37
    first_top, first_bot = credits_digit((credits_total / 100) % 10)
    mid_top, mid_bot = credits_digit((credits_total / 10) % 10)
    last_top, last_bot = credits_digit(credits_total % 10)
    # top half
    rom.write_bytes(0x118C46, [first_top, mid_top, last_top])
    # bottom half
    rom.write_bytes(0x118C64, [first_bot, mid_bot, last_bot])

    # patch medallion requirements
    if local_world.required_medallions[0] == 'Bombos':
        rom.write_byte(0x180022, 0x00)  # requirement
        rom.write_byte(0x4FF2, 0x31)  # sprite
        rom.write_byte(0x50D1, 0x80)
        rom.write_byte(0x51B0, 0x00)
    elif local_world.required_medallions[0] == 'Quake':
        rom.write_byte(0x180022, 0x02)  # requirement
        rom.write_byte(0x4FF2, 0x31)  # sprite
        rom.write_byte(0x50D1, 0x88)
        rom.write_byte(0x51B0, 0x00)
    if local_world.required_medallions[1] == 'Bombos':
        rom.write_byte(0x180023, 0x00)  # requirement
        rom.write_byte(0x5020, 0x31)  # sprite
        rom.write_byte(0x50FF, 0x90)
        rom.write_byte(0x51DE, 0x00)
    elif local_world.required_medallions[1] == 'Ether':
        rom.write_byte(0x180023, 0x01)  # requirement
        rom.write_byte(0x5020, 0x31)  # sprite
        rom.write_byte(0x50FF, 0x98)
        rom.write_byte(0x51DE, 0x00)

    # set open mode:
    if world.mode[player] in ['open', 'inverted']:
        rom.write_byte(0x180032, 0x01)  # open mode
    if world.mode[player] == 'inverted':
        set_inverted_mode(world, player, rom)
    elif world.mode[player] == 'standard':
        rom.write_byte(0x180032, 0x00)  # standard mode

    uncle_location = world.get_location('Link\'s Uncle', player)
    if uncle_location.item is None or uncle_location.item.name not in ['Master Sword', 'Tempered Sword',
                                                                       'Fighter Sword', 'Golden Sword',
                                                                       'Progressive Sword']:
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
    rom.write_byte(0x180038, 0x01 if world.mode[player] == "standard" else 0x00)
    rom.write_byte(0x180039, 0x01 if world.light_world_light_cone else 0x00)
    rom.write_byte(0x18003A, 0x01 if world.dark_world_light_cone else 0x00)

    GREEN_TWENTY_RUPEES = 0x47
    GREEN_CLOCK = item_table["Green Clock"].item_code

    rom.write_byte(0x18004F, 0x01)  # Byrna Invulnerability: on

    # handle item_functionality
    if world.item_functionality[player] == 'hard':
        rom.write_byte(0x180181, 0x01)  # Make silver arrows work only on ganon
        rom.write_byte(0x180182, 0x00)  # Don't auto equip silvers on pickup
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xD8)  # One Heart
        # potion heal amount
        rom.write_byte(0x180084, 0x38)  # Seven Hearts
        # potion magic restore amount
        rom.write_byte(0x180085, 0x40)  # Half Magic
        # Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x04, 0x08])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        # Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        rom.write_int16(0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x02)  # Hookshot only
    elif world.item_functionality[player] == 'expert':
        rom.write_byte(0x180181, 0x01)  # Make silver arrows work only on ganon
        rom.write_byte(0x180182, 0x00)  # Don't auto equip silvers on pickup
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xD8)  # One Heart
        # potion heal amount
        rom.write_byte(0x180084, 0x20)  # 4 Hearts
        # potion magic restore amount
        rom.write_byte(0x180085, 0x20)  # Quarter Magic
        # Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x04, 0x08])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        # Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        rom.write_int16(0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x00)  # Nothing
    else:
        rom.write_byte(0x180181, 0x00)  # Make silver arrows freely usable
        rom.write_byte(0x180182, 0x01)  # auto equip silvers on pickup
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xE3)  # fairy
        # potion heal amount
        rom.write_byte(0x180084, 0xA0)  # full
        # potion magic restore amount
        rom.write_byte(0x180085, 0x80)  # full
        # Cape magic cost
        rom.write_bytes(0x3ADA7, [0x04, 0x08, 0x10])
        # Byrna Invulnerability: on
        rom.write_byte(0x18004F, 0x01)
        # Enable catching fairies
        rom.write_byte(0x34FD6, 0xF0)
        # Rupoor negative value
        rom.write_int16(0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x03)  # All standard items
        # Set overflow items for progressive equipment
        if world.timer[player] in ['timed', 'timed_countdown', 'timed_ohko']:
            overflow_replacement = GREEN_CLOCK
        else:
            overflow_replacement = GREEN_TWENTY_RUPEES

    # Byrna residual magic cost
    rom.write_bytes(0x45C42, [0x04, 0x02, 0x01])

    difficulty = local_world.difficulty_requirements

    # Set overflow items for progressive equipment
    rom.write_bytes(0x180090,
                    [difficulty.progressive_sword_limit if not world.swordless[player] else 0,
                     item_table[difficulty.basicsword[-1]].item_code,
                     difficulty.progressive_shield_limit, item_table[difficulty.basicshield[-1]].item_code,
                     difficulty.progressive_armor_limit, item_table[difficulty.basicarmor[-1]].item_code,
                     difficulty.progressive_bottle_limit, overflow_replacement,
                     difficulty.progressive_bow_limit, item_table[difficulty.basicbow[-1]].item_code])

    if difficulty.progressive_bow_limit < 2 and (
            world.swordless[player] or world.glitches_required[player] == 'no_glitches'):
        rom.write_bytes(0x180098, [2, item_table["Silver Bow"].item_code])
        rom.write_byte(0x180181, 0x01)  # Make silver arrows work only on ganon
        rom.write_byte(0x180182, 0x00)  # Don't auto equip silvers on pickup

    # set up game internal RNG seed
    rom.write_bytes(0x178000, local_random.getrandbits(8 * 1024).to_bytes(1024, 'big'))
    prize_replacements = {}
    if world.item_functionality[player] in ['hard', 'expert']:
        prize_replacements[0xE0] = 0xDF  # Fairy -> heart
        prize_replacements[0xE3] = 0xD8  # Big magic -> small magic

    if world.retro_bow[player]:
        prize_replacements[0xE1] = 0xDA  # 5 Arrows -> Blue Rupee
        prize_replacements[0xE2] = 0xDB  # 10 Arrows -> Red Rupee

    if world.shuffle_prizes[player] in ("general", "both"):
        # shuffle prize packs
        prizes = [0xD8, 0xD8, 0xD8, 0xD8, 0xD9, 0xD8, 0xD8, 0xD9, 0xDA, 0xD9, 0xDA, 0xDB, 0xDA, 0xD9, 0xDA, 0xDA, 0xE0,
                  0xDF, 0xDF, 0xDA, 0xE0, 0xDF, 0xD8, 0xDF,
                  0xDC, 0xDC, 0xDC, 0xDD, 0xDC, 0xDC, 0xDE, 0xDC, 0xE1, 0xD8, 0xE1, 0xE2, 0xE1, 0xD8, 0xE1, 0xE2, 0xDF,
                  0xD9, 0xD8, 0xE1, 0xDF, 0xDC, 0xD9, 0xD8,
                  0xD8, 0xE3, 0xE0, 0xDB, 0xDE, 0xD8, 0xDB, 0xE2, 0xD9, 0xDA, 0xDB, 0xD9, 0xDB, 0xD9, 0xDB]
        dig_prizes = [0xB2, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8,
                      0xD9, 0xD9, 0xD9, 0xD9, 0xD9, 0xDA, 0xDA, 0xDA, 0xDA, 0xDA,
                      0xDB, 0xDB, 0xDB, 0xDB, 0xDB, 0xDC, 0xDC, 0xDC, 0xDC, 0xDC,
                      0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDE, 0xDE, 0xDE, 0xDE, 0xDE,
                      0xDF, 0xDF, 0xDF, 0xDF, 0xDF, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0,
                      0xE1, 0xE1, 0xE1, 0xE1, 0xE1, 0xE2, 0xE2, 0xE2, 0xE2, 0xE2,
                      0xE3, 0xE3, 0xE3, 0xE3, 0xE3]

        def chunk(l, n):
            return [l[i:i + n] for i in range(0, len(l), n)]

        # randomize last 7 slots
        prizes[-7:] = local_random.sample(prizes, 7)

        # shuffle order of 7 main packs
        packs = chunk(prizes[:56], 8)
        local_random.shuffle(packs)
        prizes[:56] = [drop for pack in packs for drop in pack]
        if prize_replacements:
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

    elif prize_replacements:
        dig_prizes = list(rom.read_bytes(0x180100, 64))
        dig_prizes = [prize_replacements.get(byte, byte) for byte in dig_prizes]
        rom.write_bytes(0x180100, dig_prizes)

        prizes = list(rom.read_bytes(0x37A78, 56))
        prizes = [prize_replacements.get(byte, byte) for byte in prizes]
        rom.write_bytes(0x37A78, prizes)

        for address in (0xEFBD4, 0xEFBD5, 0xEFBD6, 0x329C8, 0x329C4, 0x37993, 0xE82CC):
            byte = int(rom.read_byte(address))
            rom.write_byte(address, prize_replacements.get(byte, byte))

    if world.shuffle_prizes[player] in ("bonk", "both"):
        # set bonk prizes
        bonk_prizes = [0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xAC, 0xE3, 0xE3, 0xDA, 0xE3, 0xDA, 0xD8, 0xAC,
                       0xAC, 0xE3, 0xD8, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xDC, 0xDB, 0xE3, 0xDA, 0x79, 0x79,
                       0xE3, 0xE3,
                       0xDA, 0x79, 0xAC, 0xAC, 0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xE3, 0x79, 0xDE, 0xE3,
                       0xAC, 0xDB, 0x79, 0xE3, 0xD8, 0xAC, 0x79, 0xE3, 0xDB, 0xDB, 0xE3, 0xE3, 0x79, 0xD8, 0xDD]

        local_random.shuffle(bonk_prizes)

        if prize_replacements:
            bonk_prizes = [prize_replacements.get(prize, prize) for prize in bonk_prizes]

        for prize, address in zip(bonk_prizes, bonk_addresses):
            rom.write_byte(address, prize)

    elif prize_replacements:
        for address in bonk_addresses:
            byte = int(rom.read_byte(address))
            rom.write_byte(address, prize_replacements.get(byte, byte))

    # Fill in item substitutions table
    rom.write_bytes(0x184000, [
        # original_item, limit, replacement_item, filler
        0x12, 0x01, 0x35, 0xFF,  # lamp -> 5 rupees
        0x51, 0x06, 0x52, 0xFF,  # 6 +5 bomb upgrades -> +10 bomb upgrade
        0x53, 0x06, 0x54, 0xFF,  # 6 +5 arrow upgrades -> +10 arrow upgrade
        0x58, 0x01, 0x36 if world.retro_bow[player] else 0x43, 0xFF,  # silver arrows -> single arrow (red 20 in retro mode)
        0x3E, difficulty.boss_heart_container_limit, 0x47, 0xff,  # boss heart -> green 20
        0x17, difficulty.heart_piece_limit, 0x47, 0xff,  # piece of heart -> green 20
        0xFF, 0xFF, 0xFF, 0xFF,  # end of table sentinel
    ])

    # set Fountain bottle exchange items
    rom.write_byte(0x348FF, item_table[local_world.waterfall_fairy_bottle_fill].item_code)
    rom.write_byte(0x3493B, item_table[local_world.pyramid_fairy_bottle_fill].item_code)

    # enable Fat Fairy Chests
    rom.write_bytes(0x1FC16, [0xB1, 0xC6, 0xF9, 0xC9, 0xC6, 0xF9])
    # set Fat Fairy Bow/Sword prizes to be disappointing
    rom.write_byte(0x34914, 0x3A)  # Bow and Arrow
    rom.write_byte(0x180028, 0x49)  # Fighter Sword
    # enable Waterfall fairy chests
    rom.write_bytes(0xE9AE, [0x14, 0x01])
    rom.write_bytes(0xE9CF, [0x14, 0x01])
    rom.write_bytes(0x1F714,
                    [225, 0, 16, 172, 13, 41, 154, 1, 88, 152, 15, 17, 177, 97, 252, 77, 129, 32, 218, 2, 44, 225, 97,
                     252, 190, 129, 97, 177, 98, 84, 218, 2,
                     253, 141, 131, 68, 225, 98, 253, 30, 131, 49, 165, 201, 49, 164, 105, 49, 192, 34, 77, 164, 105,
                     49, 198, 249, 73, 198, 249, 16, 153, 160, 92, 153,
                     162, 11, 152, 96, 13, 232, 192, 85, 232, 192, 11, 146, 0, 115, 152, 96, 254, 105, 0, 152, 163, 97,
                     254, 107, 129, 254, 171, 133, 169, 200, 97, 254,
                     174, 129, 255, 105, 2, 216, 163, 98, 255, 107, 131, 255, 43, 135, 201, 200, 98, 255, 46, 131, 254,
                     161, 0, 170, 33, 97, 254, 166, 129, 255, 33, 2,
                     202, 33, 98, 255, 38, 131, 187, 35, 250, 195, 35, 250, 187, 43, 250, 195, 43, 250, 187, 83, 250,
                     195, 83, 250, 176, 160, 61, 152, 19, 192, 152, 82,
                     192, 136, 0, 96, 144, 0, 96, 232, 0, 96, 240, 0, 96, 152, 202, 192, 216, 202, 192, 216, 19, 192,
                     216, 82, 192, 252, 189, 133, 253, 29, 135, 255,
                     255, 255, 255, 240, 255, 128, 46, 97, 14, 129, 14, 255, 255])
    # set Waterfall fairy prizes to be disappointing
    rom.write_byte(0x348DB, 0x3A)  # Red Boomerang becomes Red Boomerang
    rom.write_byte(0x348EB, 0x05)  # Blue Shield becomes Blue Shield

    # Remove Statues for upgrade fairy
    rom.write_bytes(0x01F810, [0x1A, 0x1E, 0x01, 0x1A, 0x1E, 0x01])

    rom.write_byte(0x180029, 0x01)  # Smithy quick item give

    # set swordless mode settings
    rom.write_byte(0x18003F, 0x01 if world.swordless[player] else 0x00)  # hammer can harm ganon
    rom.write_byte(0x180040, 0x01 if world.swordless[player] else 0x00)  # open curtains
    rom.write_byte(0x180041, 0x01 if world.swordless[player] else 0x00)  # swordless medallions
    rom.write_byte(0x180043, 0xFF if world.swordless[player] else 0x00)  # starting sword for link
    rom.write_byte(0x180044, 0x01 if world.swordless[player] else 0x00)  # hammer activates tablets

    if world.item_functionality[player] == 'easy':
        rom.write_byte(0x18003F, 0x01)  # hammer can harm ganon
        rom.write_byte(0x180041, 0x02)  # Allow swordless medallion use EVERYWHERE.
        rom.write_byte(0x180044, 0x01)  # hammer activates tablets

    # set up clocks for timed modes
    if local_world.clock_mode in ['ohko', 'countdown-ohko']:
        rom.write_bytes(0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
    elif local_world.clock_mode == 'stopwatch':
        rom.write_bytes(0x180190, [0x02, 0x01, 0x00])  # set stopwatch mode
    elif local_world.clock_mode == 'countdown':
        rom.write_bytes(0x180190, [0x01, 0x01, 0x00])  # set countdown, with no reset available
    else:
        rom.write_bytes(0x180190, [0x00, 0x00, 0x00])  # turn off clock mode

    # Set up requested clock settings
    if local_world.clock_mode in ['countdown-ohko', 'stopwatch', 'countdown']:
        rom.write_int32(0x180200,
                        world.red_clock_time[player] * 60 * 60)  # red clock adjustment time (in frames, sint32)
        rom.write_int32(0x180204,
                        world.blue_clock_time[player] * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32(0x180208,
                        world.green_clock_time[player] * 60 * 60)  # green clock adjustment time (in frames, sint32)
    else:
        rom.write_int32(0x180200, 0)  # red clock adjustment time (in frames, sint32)
        rom.write_int32(0x180204, 0)  # blue clock adjustment time (in frames, sint32)
        rom.write_int32(0x180208, 0)  # green clock adjustment time (in frames, sint32)

    # Set up requested start time for countdown modes
    if local_world.clock_mode in ['countdown-ohko', 'countdown']:
        rom.write_int32(0x18020C, world.countdown_start_time[player] * 60 * 60)  # starting time (in frames, sint32)
    else:
        rom.write_int32(0x18020C, 0)  # starting time (in frames, sint32)

    # set up goals for treasure hunt
    rom.write_int16(0x180163, max(0, local_world.treasure_hunt_required -
                    sum(1 for item in world.precollected_items[player] if item.name == "Triforce Piece")))
    rom.write_bytes(0x180165, [0x0E, 0x28])  #  Triforce Piece Sprite
    rom.write_byte(0x180194, 1)  # Must turn in triforced pieces (instant win not enabled)

    rom.write_bytes(0x180213, [0x00, 0x01])  # Not a Tournament Seed

    gametype = 0x04  # item
    if world.entrance_shuffle[player] != 'vanilla':
        gametype |= 0x02  # entrance
    if enemized:
        gametype |= 0x01  # enemizer
    rom.write_byte(0x180211, gametype)  # Game type

    # assorted fixes
    # Toggle whether to be in real/fake dark world when dying in a DW dungeon before killing aga1
    rom.write_byte(0x1800A2, 0x01 if local_world.fix_fake_world else 0x00)
    # Lock or unlock aga tower door during escape sequence.
    rom.write_byte(0x180169, 0x00)
    if world.mode[player] == 'inverted':
        rom.write_byte(0x180169, 0x02)  # lock aga/ganon tower door with crystals in inverted
    rom.write_byte(0x180171,
                   0x01 if local_world.ganon_at_pyramid else 0x00)  # Enable respawning on pyramid after ganon death
    rom.write_byte(0x180173, 0x01)  # Bob is enabled
    rom.write_byte(0x180168, 0x08)  # Spike Cave Damage
    rom.write_bytes(0x18016B, [0x04, 0x02, 0x01])  # Set spike cave and MM spike room Cape usage
    rom.write_bytes(0x18016E, [0x04, 0x08, 0x10])  # Set spike cave and MM spike room Cape usage
    rom.write_bytes(0x50563, [0x3F, 0x14])  # disable below ganon chest
    rom.write_byte(0x50599, 0x00)  # disable below ganon chest
    rom.write_bytes(0xE9A5, [0x7E, 0x00, 0x24])  # disable below ganon chest
    rom.write_byte(0x18008B, 0x01 if world.open_pyramid[player].to_bool(world, player) else 0x00)  # pre-open Pyramid Hole
    rom.write_byte(0x18008C, 0x01 if world.crystals_needed_for_gt[
                                         player] == 0 else 0x00)  # GT pre-opened if crystal requirement is 0
    rom.write_byte(0xF5D73, 0xF0)  # bees are catchable
    rom.write_byte(0xF5F10, 0xF0)  # bees are catchable
    rom.write_byte(0x180086, 0x00 if world.aga_randomness else 0x01)  # set blue ball and ganon warp randomness
    rom.write_byte(0x1800A0, 0x01)  # return to light world on s+q without mirror
    rom.write_byte(0x1800A1, 0x01)  # enable overworld screen transition draining for water level inside swamp
    rom.write_byte(0x180174, 0x01 if local_world.fix_fake_world else 0x00)
    rom.write_byte(0x18017E, 0x01)  # Fairy fountains only trade in bottles

    # Starting equipment
    equip = [0] * (0x340 + 0x4F)
    equip[0x36C] = 0x18
    equip[0x36D] = 0x18
    equip[0x379] = 0x68
    starting_max_bombs = 0 if world.bombless_start[player] else 10
    starting_max_arrows = 30

    startingstate = CollectionState(world)

    if startingstate.has('Silver Bow', player):
        equip[0x340] = 1
        equip[0x38E] |= 0x60
        if not world.retro_bow[player]:
            equip[0x38E] |= 0x80
    elif startingstate.has('Bow', player):
        equip[0x340] = 1
        equip[0x38E] |= 0x20  # progressive flag to get the correct hint in all cases
        if not world.retro_bow[player]:
            equip[0x38E] |= 0x80
    if startingstate.has('Silver Arrows', player):
        equip[0x38E] |= 0x40

    if startingstate.has('Titans Mitts', player):
        equip[0x354] = 2
    elif startingstate.has('Power Glove', player):
        equip[0x354] = 1

    if startingstate.has('Golden Sword', player):
        equip[0x359] = 4
    elif startingstate.has('Tempered Sword', player):
        equip[0x359] = 3
    elif startingstate.has('Master Sword', player):
        equip[0x359] = 2
    elif startingstate.has('Fighter Sword', player):
        equip[0x359] = 1

    if startingstate.has('Mirror Shield', player):
        equip[0x35A] = 3
    elif startingstate.has('Red Shield', player):
        equip[0x35A] = 2
    elif startingstate.has('Blue Shield', player):
        equip[0x35A] = 1

    if startingstate.has('Red Mail', player):
        equip[0x35B] = 2
    elif startingstate.has('Blue Mail', player):
        equip[0x35B] = 1

    if startingstate.has('Magic Upgrade (1/4)', player):
        equip[0x37B] = 2
        equip[0x36E] = 0x80
    elif startingstate.has('Magic Upgrade (1/2)', player):
        equip[0x37B] = 1
        equip[0x36E] = 0x80

    for item in world.precollected_items[player]:

        if item.name in {'Bow', 'Silver Bow', 'Silver Arrows', 'Progressive Bow', 'Progressive Bow (Alt)',
                         'Titans Mitts', 'Power Glove', 'Progressive Glove',
                         'Golden Sword', 'Tempered Sword', 'Master Sword', 'Fighter Sword', 'Progressive Sword',
                         'Mirror Shield', 'Red Shield', 'Blue Shield', 'Progressive Shield',
                         'Red Mail', 'Blue Mail', 'Progressive Mail',
                         'Magic Upgrade (1/4)', 'Magic Upgrade (1/2)', 'Triforce Piece'}:
            continue

        set_table = {'Book of Mudora': (0x34E, 1), 'Hammer': (0x34B, 1), 'Bug Catching Net': (0x34D, 1),
                     'Hookshot': (0x342, 1), 'Magic Mirror': (0x353, 2),
                     'Cape': (0x352, 1), 'Lamp': (0x34A, 1), 'Moon Pearl': (0x357, 1), 'Cane of Somaria': (0x350, 1),
                     'Cane of Byrna': (0x351, 1),
                     'Fire Rod': (0x345, 1), 'Ice Rod': (0x346, 1), 'Bombos': (0x347, 1), 'Ether': (0x348, 1),
                     'Quake': (0x349, 1)}
        or_table = {'Green Pendant': (0x374, 0x04), 'Red Pendant': (0x374, 0x01), 'Blue Pendant': (0x374, 0x02),
                    'Crystal 1': (0x37A, 0x02), 'Crystal 2': (0x37A, 0x10), 'Crystal 3': (0x37A, 0x40),
                    'Crystal 4': (0x37A, 0x20),
                    'Crystal 5': (0x37A, 0x04), 'Crystal 6': (0x37A, 0x01), 'Crystal 7': (0x37A, 0x08),
                    'Big Key (Eastern Palace)': (0x367, 0x20), 'Compass (Eastern Palace)': (0x365, 0x20),
                    'Map (Eastern Palace)': (0x369, 0x20),
                    'Big Key (Desert Palace)': (0x367, 0x10), 'Compass (Desert Palace)': (0x365, 0x10),
                    'Map (Desert Palace)': (0x369, 0x10),
                    'Big Key (Tower of Hera)': (0x366, 0x20), 'Compass (Tower of Hera)': (0x364, 0x20),
                    'Map (Tower of Hera)': (0x368, 0x20),
                    'Big Key (Hyrule Castle)': (0x367, 0xC0), 'Compass (Hyrule Castle)': (0x365, 0xC0),
                    'Map (Hyrule Castle)': (0x369, 0xC0),
                    # doors-specific items
                    'Big Key (Agahnims Tower)': (0x367, 0x08), 'Compass (Agahnims Tower)': (0x365, 0x08),
                    'Map (Agahnims Tower)': (0x369, 0x08),
                    # end of doors-specific items
                    'Big Key (Palace of Darkness)': (0x367, 0x02), 'Compass (Palace of Darkness)': (0x365, 0x02),
                    'Map (Palace of Darkness)': (0x369, 0x02),
                    'Big Key (Thieves Town)': (0x366, 0x10), 'Compass (Thieves Town)': (0x364, 0x10),
                    'Map (Thieves Town)': (0x368, 0x10),
                    'Big Key (Skull Woods)': (0x366, 0x80), 'Compass (Skull Woods)': (0x364, 0x80),
                    'Map (Skull Woods)': (0x368, 0x80),
                    'Big Key (Swamp Palace)': (0x367, 0x04), 'Compass (Swamp Palace)': (0x365, 0x04),
                    'Map (Swamp Palace)': (0x369, 0x04),
                    'Big Key (Ice Palace)': (0x366, 0x40), 'Compass (Ice Palace)': (0x364, 0x40),
                    'Map (Ice Palace)': (0x368, 0x40),
                    'Big Key (Misery Mire)': (0x367, 0x01), 'Compass (Misery Mire)': (0x365, 0x01),
                    'Map (Misery Mire)': (0x369, 0x01),
                    'Big Key (Turtle Rock)': (0x366, 0x08), 'Compass (Turtle Rock)': (0x364, 0x08),
                    'Map (Turtle Rock)': (0x368, 0x08),
                    'Big Key (Ganons Tower)': (0x366, 0x04), 'Compass (Ganons Tower)': (0x364, 0x04),
                    'Map (Ganons Tower)': (0x368, 0x04)}
        set_or_table = {'Flippers': (0x356, 1, 0x379, 0x02), 'Pegasus Boots': (0x355, 1, 0x379, 0x04),
                        'Shovel': (0x34C, 1, 0x38C, 0x04),
                        'Flute': (0x34C, 2, 0x38C, 0x02),
                        'Activated Flute': (0x34C, 3, 0x38C, 0x01),
                        'Mushroom': (0x344, 1, 0x38C, 0x20 | 0x08), 'Magic Powder': (0x344, 2, 0x38C, 0x10),
                        'Blue Boomerang': (0x341, 1, 0x38C, 0x80), 'Red Boomerang': (0x341, 2, 0x38C, 0x40)}
        keys = {'Small Key (Eastern Palace)': [0x37E], 'Small Key (Desert Palace)': [0x37F],
                'Small Key (Tower of Hera)': [0x386],
                'Small Key (Agahnims Tower)': [0x380], 'Small Key (Palace of Darkness)': [0x382],
                'Small Key (Thieves Town)': [0x387],
                'Small Key (Skull Woods)': [0x384], 'Small Key (Swamp Palace)': [0x381],
                'Small Key (Ice Palace)': [0x385],
                'Small Key (Misery Mire)': [0x383], 'Small Key (Turtle Rock)': [0x388],
                'Small Key (Ganons Tower)': [0x389],
                'Small Key (Universal)': [0x38B], 'Small Key (Hyrule Castle)': [0x37C, 0x37D]}
        bottles = {'Bottle': 2, 'Bottle (Red Potion)': 3, 'Bottle (Green Potion)': 4, 'Bottle (Blue Potion)': 5,
                   'Bottle (Fairy)': 6, 'Bottle (Bee)': 7, 'Bottle (Good Bee)': 8}
        rupees = {'Rupee (1)': 1, 'Rupees (5)': 5, 'Rupees (20)': 20, 'Rupees (50)': 50, 'Rupees (100)': 100,
                  'Rupees (300)': 300}
        bomb_caps = {'Bomb Upgrade (+5)': 5, 'Bomb Upgrade (+10)': 10, 'Bomb Upgrade (50)': 50}
        arrow_caps = {'Arrow Upgrade (+5)': 5, 'Arrow Upgrade (+10)': 10, 'Arrow Upgrade (70)': 70}
        bombs = {'Single Bomb': 1, 'Bombs (3)': 3, 'Bombs (10)': 10}
        arrows = {'Single Arrow': 1, 'Arrows (10)': 10}

        if item.name in set_table:
            equip[set_table[item.name][0]] = set_table[item.name][1]
        elif item.name in or_table:
            equip[or_table[item.name][0]] |= or_table[item.name][1]
        elif item.name in set_or_table:
            equip[set_or_table[item.name][0]] = set_or_table[item.name][1]
            equip[set_or_table[item.name][2]] |= set_or_table[item.name][3]
        elif item.name in keys:
            for address in keys[item.name]:
                equip[address] = min(equip[address] + 1, 99)
        elif item.name in bottles:
            if equip[0x34F] < local_world.difficulty_requirements.progressive_bottle_limit:
                equip[0x35C + equip[0x34F]] = bottles[item.name]
                equip[0x34F] += 1
        elif item.name in rupees:
            equip[0x360:0x362] = list(
                min(equip[0x360] + (equip[0x361] << 8) + rupees[item.name], 9999).to_bytes(2, byteorder='little',
                                                                                           signed=False))
            equip[0x362:0x364] = list(
                min(equip[0x362] + (equip[0x363] << 8) + rupees[item.name], 9999).to_bytes(2, byteorder='little',
                                                                                           signed=False))
        elif item.name in bomb_caps:
            starting_max_bombs = min(starting_max_bombs + bomb_caps[item.name], 50)
        elif item.name in arrow_caps:
            starting_max_arrows = min(starting_max_arrows + arrow_caps[item.name], 70)
        elif item.name in bombs:
            equip[0x343] += bombs[item.name]
        elif item.name in arrows:
            if world.retro_bow[player]:
                equip[0x38E] |= 0x80
                equip[0x377] = 1
            else:
                equip[0x377] += arrows[item.name]
        elif item.name in ['Piece of Heart', 'Boss Heart Container', 'Sanctuary Heart Container']:
            if item.name == 'Piece of Heart':
                equip[0x36B] = (equip[0x36B] + 1) % 4
            if item.name != 'Piece of Heart' or equip[0x36B] == 0:
                equip[0x36C] = min(equip[0x36C] + 0x08, 0xA0)
                equip[0x36D] = min(equip[0x36D] + 0x08, 0xA0)
        else:
            raise RuntimeError(f'Unsupported item in starting equipment: {item.name}')

    equip[0x343] = min(equip[0x343], starting_max_bombs)
    rom.write_byte(0x180034, starting_max_bombs)
    equip[0x377] = min(equip[0x377], starting_max_arrows)
    rom.write_byte(0x180035, starting_max_arrows)
    rom.write_bytes(0x180046, equip[0x360:0x362])
    if equip[0x359]:
        rom.write_byte(0x180043, equip[0x359])

    assert equip[:0x340] == [0] * 0x340
    rom.write_bytes(0x183000, equip[0x340:])
    rom.write_bytes(0x271A6, equip[0x340:0x340 + 60])

    rom.write_byte(0x18004A, 0x00 if world.mode[player] != 'inverted' else 0x01)  # Inverted mode
    rom.write_byte(0x18005D, 0x00)  # Hammer always breaks barrier
    rom.write_byte(0x2AF79, 0xD0 if world.mode[
                                        player] != 'inverted' else 0xF0)  # vortexes: Normal  (D0=light to dark, F0=dark to light, 42 = both)
    rom.write_byte(0x3A943, 0xD0 if world.mode[
                                        player] != 'inverted' else 0xF0)  # Mirror: Normal  (D0=Dark to Light, F0=light to dark, 42 = both)
    rom.write_byte(0x3A96D, 0xF0 if world.mode[
                                        player] != 'inverted' else 0xD0)  # Residual Portal: Normal  (F0= Light Side, D0=Dark Side, 42 = both (Darth Vader))
    rom.write_byte(0x3A9A7, 0xD0)  # Residual Portal: Normal  (D0= Light Side, F0=Dark Side, 42 = both (Darth Vader))
    if world.shuffle_capacity_upgrades[player]:
        rom.write_bytes(0x180080,
                        [5, 10, 5, 10])  # values to fill for Capacity Upgrades (Bomb5, Bomb10, Arrow5, Arrow10)
    else:
        rom.write_bytes(0x180080,
                        [50, 50, 70, 70])  # values to fill for Capacity Upgrades (Bomb5, Bomb10, Arrow5, Arrow10)

    rom.write_byte(0x18004D, ((0x01 if 'arrows' in local_world.escape_assist else 0x00) |
                              (0x02 if 'bombs' in local_world.escape_assist else 0x00) |
                              (0x04 if 'magic' in local_world.escape_assist else 0x00)))  # Escape assist

    if world.goal[player] in ['pedestal', 'triforce_hunt', 'local_triforce_hunt']:
        rom.write_byte(0x18003E, 0x01)  # make ganon invincible
    elif world.goal[player] in ['ganon_triforce_hunt', 'local_ganon_triforce_hunt']:
        rom.write_byte(0x18003E, 0x05)  # make ganon invincible until enough triforce pieces are collected
    elif world.goal[player] in ['ganon_pedestal']:
        rom.write_byte(0x18003E, 0x06)
    elif world.goal[player] in ['bosses']:
        rom.write_byte(0x18003E, 0x02)  # make ganon invincible until all bosses are beat
    elif world.goal[player] in ['crystals']:
        rom.write_byte(0x18003E, 0x04)  # make ganon invincible until all crystals
    else:
        rom.write_byte(0x18003E, 0x03)  # make ganon invincible until all crystals and aga 2 are collected

    rom.write_byte(0x18005E, world.crystals_needed_for_gt[player])
    rom.write_byte(0x18005F, world.crystals_needed_for_ganon[player])

    # Bitfield - enable text box to show with free roaming items
    #
    # ---o bmcs
    # o - enabled for outside dungeon items
    # b - enabled for inside big keys
    # m - enabled for inside maps
    # c - enabled for inside compasses
    # s - enabled for inside small keys
    # block HC upstairs doors in rain state in standard mode
    rom.write_byte(0x18008A, 0x01 if world.mode[player] == "standard" and world.entrance_shuffle[player] != 'vanilla' else 0x00)

    rom.write_byte(0x18016A, 0x10 | ((0x01 if world.small_key_shuffle[player] else 0x00)
                                     | (0x02 if world.compass_shuffle[player] else 0x00)
                                     | (0x04 if world.map_shuffle[player] else 0x00)
                                     | (0x08 if world.big_key_shuffle[
                player] else 0x00)))  # free roaming item text boxes
    rom.write_byte(0x18003B, 0x01 if world.map_shuffle[player] else 0x00)  # maps showing crystals on overworld

    # compasses showing dungeon count
    if local_world.clock_mode or world.dungeon_counters[player] == 'off':
        rom.write_byte(0x18003C, 0x00)  # Currently must be off if timer is on, because they use same HUD location
    elif world.dungeon_counters[player] == 'on':
        rom.write_byte(0x18003C, 0x02)  # always on
    elif world.compass_shuffle[player] or world.dungeon_counters[player] == 'pickup':
        rom.write_byte(0x18003C, 0x01)  # show on pickup
    else:
        rom.write_byte(0x18003C, 0x00)

    # Bitfield - enable free items to show up in menu
    #
    # ----dcba
    # d - Compass
    # c - Map
    # b - Big Key
    # a - Small Key
    #
    rom.write_byte(0x180045, ((0x00 if (world.small_key_shuffle[player] == small_key_shuffle.option_original_dungeon or
                                        world.small_key_shuffle[player] == small_key_shuffle.option_universal) else 0x01)
                              | (0x02 if world.big_key_shuffle[player] else 0x00)
                              | (0x04 if world.map_shuffle[player] else 0x00)
                              | (0x08 if world.compass_shuffle[player] else 0x00)))  # free roaming items in menu

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
        "Misery Mire": 0x0100,
        "Turtle Rock": 0x0008,
    }

    def get_reveal_bytes(itemName):
        locations = world.find_item_locations(itemName, player)
        if len(locations) < 1:
            return 0x0000
        location = locations[0]
        if location.parent_region and location.parent_region.dungeon:
            return reveal_bytes.get(location.parent_region.dungeon.name, 0x0000)
        return 0x0000

    rom.write_int16(0x18017A,
                    get_reveal_bytes('Green Pendant') if world.map_shuffle[player] else 0x0000)  # Sahasrahla reveal
    rom.write_int16(0x18017C, get_reveal_bytes('Crystal 5') | get_reveal_bytes('Crystal 6') if world.map_shuffle[
        player] else 0x0000)  # Bomb Shop Reveal

    rom.write_byte(0x180172, 0x01 if world.small_key_shuffle[
                                         player] == small_key_shuffle.option_universal else 0x00)  # universal keys
    rom.write_byte(0x18637E, 0x01 if world.retro_bow[player] else 0x00)  # Skip quiver in item shops once bought
    rom.write_byte(0x180175, 0x01 if world.retro_bow[player] else 0x00)  # rupee bow
    rom.write_byte(0x180176, 0x0A if world.retro_bow[player] else 0x00)  # wood arrow cost
    rom.write_byte(0x180178, 0x32 if world.retro_bow[player] else 0x00)  # silver arrow cost
    rom.write_byte(0x301FC, 0xDA if world.retro_bow[player] else 0xE1)  # rupees replace arrows under pots
    rom.write_byte(0x30052, 0xDB if world.retro_bow[player] else 0xE2)  # replace arrows in fish prize from bottle merchant
    rom.write_bytes(0xECB4E, [0xA9, 0x00, 0xEA, 0xEA] if world.retro_bow[player] else [0xAF, 0x77, 0xF3,
                                                                                   0x7E])  # Thief steals rupees instead of arrows
    rom.write_bytes(0xF0D96, [0xA9, 0x00, 0xEA, 0xEA] if world.retro_bow[player] else [0xAF, 0x77, 0xF3,
                                                                                   0x7E])  # Pikit steals rupees instead of arrows
    rom.write_bytes(0xEDA5,
                    [0x35, 0x41] if world.retro_bow[player] else [0x43, 0x44])  # Chest game gives rupees instead of arrows
    digging_game_rng = local_random.randint(1, 30)  # set rng for digging game
    rom.write_byte(0x180020, digging_game_rng)
    rom.write_byte(0xEFD95, digging_game_rng)
    rom.write_byte(0x1800A3, 0x01)  # enable correct world setting behaviour after agahnim kills
    rom.write_byte(0x1800A4, 0x01 if world.glitches_required[player] != 'no_logic' else 0x00)  # enable POD EG fix
    rom.write_byte(0x186383, 0x01 if world.glitches_required[
        player] == 'no_logic' else 0x00)  # disable glitching to Triforce from Ganons Room
    rom.write_byte(0x180042, 0x01 if world.save_and_quit_from_boss else 0x00)  # Allow Save and Quit after boss kill

    # remove shield from uncle
    rom.write_bytes(0x6D253, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D25B, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D283, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D28B, [0x00, 0x00, 0xf7, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D2CB, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
    rom.write_bytes(0x6D2FB, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
    rom.write_bytes(0x6D313, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])

    rom.write_byte(0x18004E, 0)  # Escape Fill (nothing)
    rom.write_int16(0x180183, 300)  # Escape fill rupee bow
    rom.write_bytes(0x180185, [0, 0, 0])  # Uncle respawn refills (magic, bombs, arrows)
    rom.write_bytes(0x180188, [0, 0, 0])  # Zelda respawn refills (magic, bombs, arrows)
    rom.write_bytes(0x18018B, [0, 0, 0])  # Mantle respawn refills (magic, bombs, arrows)
    if world.mode[player] == 'standard' and uncle_location.item and uncle_location.item.player == player:
        if uncle_location.item.name in {'Bow', 'Progressive Bow'}:
            rom.write_byte(0x18004E, 1)  # Escape Fill (arrows)
            rom.write_int16(0x180183, 300)  # Escape fill rupee bow
            rom.write_bytes(0x180185, [0, 0, 70])  # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [0, 0, 10])  # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [0, 0, 10])  # Mantle respawn refills (magic, bombs, arrows)
        elif uncle_location.item.name in {'Bombs (10)'}:
            rom.write_byte(0x18004E, 2)  # Escape Fill (bombs)
            rom.write_bytes(0x180185, [0, 50, 0])  # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [0, 3, 0])  # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [0, 3, 0])  # Mantle respawn refills (magic, bombs, arrows)
        elif uncle_location.item.name in {'Cane of Somaria', 'Cane of Byrna', 'Fire Rod'}:
            rom.write_byte(0x18004E, 4)  # Escape Fill (magic)
            rom.write_bytes(0x180185, [0x80, 0, 0])  # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [0x20, 0, 0])  # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [0x20, 0, 0])  # Mantle respawn refills (magic, bombs, arrows)

    # patch swamp: Need to enable permanent drain of water as dam or swamp were moved
    rom.write_byte(0x18003D, 0x01 if local_world.swamp_patch_required else 0x00)

    # powder patch: remove the need to leave the screen after powder, since it causes problems for potion shop at race game
    # temporarally we are just nopping out this check we will conver this to a rom fix soon.
    rom.write_bytes(0x02F539,
                    [0xEA, 0xEA, 0xEA, 0xEA, 0xEA] if local_world.powder_patch_required else [
                        0xAD, 0xBF, 0x0A, 0xF0, 0x4F])

    # allow smith into multi-entrance caves in appropriate shuffles
    if world.entrance_shuffle[player] in ['restricted', 'full', 'crossed', 'insanity'] or (
            world.entrance_shuffle[player] == 'simple' and world.mode[player] == 'inverted'):
        rom.write_byte(0x18004C, 0x01)

    # set correct flag for hera basement item
    hera_basement = world.get_location('Tower of Hera - Basement Cage', player)
    if hera_basement.item is not None and hera_basement.item.name == 'Small Key (Tower of Hera)' and hera_basement.item.player == player:
        rom.write_byte(0x4E3BB, 0xE4)
    else:
        rom.write_byte(0x4E3BB, 0xEB)

    # fix trock doors for reverse entrances
    if local_world.fix_trock_doors:
        rom.write_byte(0xFED31, 0x0E)  # preopen bombable exit
        rom.write_byte(0xFEE41, 0x0E)  # preopen bombable exit
        # included unconditionally in base2current
        # rom.write_byte(0xFE465, 0x1E)  # remove small key door on backside of big key door
    else:
        rom.write_byte(0xFED31, 0x2A)  # bombable exit
        rom.write_byte(0xFEE41, 0x2A)  # bombable exit

    if world.tile_shuffle[player]:
        tile_set = TileSet.get_random_tile_set(world.per_slot_randoms[player])
        rom.write_byte(0x4BA21, tile_set.get_speed())
        rom.write_byte(0x4BA1D, tile_set.get_len())
        rom.write_bytes(0x4BA2A, tile_set.get_bytes())

    write_strings(rom, world, player)

    # remote items flag, does not currently work
    rom.write_byte(0x18637C, 0)

    # set rom name
    # 21 bytes
    from Utils import __version__
    rom.name = bytearray(f'AP{__version__.replace(".", "")[0:3]}_{player}_{world.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)

    # set player names
    encoded_players = world.players + len(world.groups)
    for p in range(1, min(encoded_players, ROM_PLAYER_LIMIT) + 1):
        rom.write_bytes(0x195FFC + ((p - 1) * 32), hud_format_text(world.player_name[p]))
    if encoded_players > ROM_PLAYER_LIMIT:
        rom.write_bytes(0x195FFC + ((ROM_PLAYER_LIMIT - 1) * 32), hud_format_text("Archipelago"))

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
    rom.hash = code

    return rom


def patch_race_rom(rom, world, player):
    rom.write_bytes(0x180213, [0x01, 0x00])  # Tournament Seed
    rom.encrypt(world, player)


def get_price_data(price: int, price_type: int) -> List[int]:
    if price_type != ShopPriceType.Rupees:
        # Set special price flag 0x8000
        # Then set the type of price we're setting 0x7F00 (this starts from Hearts, not Rupees, subtract 1)
        # Then append the price/index into the second byte 0x00FF
        return int16_as_bytes(0x8000 | 0x100 * (price_type - 1) | price)
    else:
        return int16_as_bytes(price)


def write_custom_shops(rom, world, player):
    shops = sorted([shop for shop in world.shops if shop.custom and shop.region.player == player],
                   key=lambda shop: shop.sram_offset)

    shop_data = bytearray()
    items_data = bytearray()
    retro_shop_slots = bytearray()

    for shop_id, shop in enumerate(shops):
        if shop_id == len(shops) - 1:
            shop_id = 0xFF
        bytes = shop.get_bytes()
        bytes[0] = shop_id
        bytes[-1] = shop.sram_offset
        shop_data.extend(bytes)

        arrow_mask = 0x00
        for index, item in enumerate(shop.inventory):
            slot = 0 if shop.type == ShopType.TakeAny else index
            if item is None:
                break
            if world.shop_item_slots[player] or shop.type == ShopType.TakeAny:
                count_shop = (shop.region.name != 'Potion Shop' or world.include_witch_hut[player]) and \
                             (shop.region.name != 'Capacity Upgrade' or world.shuffle_capacity_upgrades[player])
                rom.write_byte(0x186560 + shop.sram_offset + slot, 1 if count_shop else 0)
            if item['item'] == 'Single Arrow' and item['player'] == 0:
                arrow_mask |= 1 << index
                retro_shop_slots.append(shop.sram_offset + slot)

        # [id][item][price-low][price-high][max][repl_id][repl_price-low][repl_price-high][player]
        for index, item in enumerate(shop.inventory):
            if item is None:
                break
            price_data = get_price_data(item['price'], item["price_type"])
            replacement_price_data = get_price_data(item['replacement_price'], item['replacement_price_type'])
            slot = 0 if shop.type == ShopType.TakeAny else index
            if item['player'] and world.game[item['player']] != "A Link to the Past":  # item not native to ALTTP
                item_code = get_nonnative_item_sprite(world.worlds[item['player']].item_name_to_id[item['item']])
            else:
                item_code = item_table[item["item"]].item_code
                if item['item'] == 'Single Arrow' and item['player'] == 0 and world.retro_bow[player]:
                    rom.write_byte(0x186500 + shop.sram_offset + slot, arrow_mask)

            item_data = [shop_id, item_code] + price_data + \
                        [item["max"], item_table[item["replacement"]].item_code if item["replacement"] else 0xFF] + \
                        replacement_price_data + [0 if item["player"] == player else min(ROM_PLAYER_LIMIT, item["player"])]
            items_data.extend(item_data)

    rom.write_bytes(0x184800, shop_data)

    items_data.extend([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    rom.write_bytes(0x184900, items_data)

    if world.retro_bow[player]:
        retro_shop_slots.append(0xFF)
        rom.write_bytes(0x186540, retro_shop_slots)


def hud_format_text(text):
    output = bytes()
    for char in text.lower():
        if 'a' <= char <= 'z':
            output += bytes([0x5d + ord(char) - ord('a'), 0x29])
        elif '0' <= char <= '8':
            output += bytes([0x77 + ord(char) - ord('0'), 0x29])
        elif char == '9':
            output += b'\x4b\x29'
        elif char == ' ' or char == '_':
            output += b'\x7f\x00'
        else:
            output += b'\x2a\x29'
    while len(output) < 32:
        output += b'\x7f\x00'
    return output[:32]

def apply_oof_sfx(rom, oof: str):
    with open(oof, 'rb') as stream:
        oof_bytes = bytearray(stream.read())

    oof_len_bytes = len(oof_bytes).to_bytes(2, byteorder='little')

    # Credit to kan for this method, and Nyx for initial C# implementation
    # this is ported from, with both of their permission for use by AP
    # Original C# implementation:
    # https://github.com/Nyx-Edelstein/The-Unachievable-Ideal-of-Chibi-Elf-Grunting-Noises-When-They-Get-Punched-A-Z3-Rom-Patcher

    # Jump execution from the SPC load routine to new code
    rom.write_bytes(0x8CF, [0x5C, 0x00, 0x80, 0x25])

    # Change the pointer for instrument 9 in SPC memory to point to the new data we'll be inserting:
    rom.write_bytes(0x1A006C, [0x88, 0x31, 0x00, 0x00])

    # Insert a sigil so we can branch on it later
    # We will recover the value it overwrites after we're done with insertion
    rom.write_bytes(0x1AD38C, [0xBE, 0xBE])

    # Change the "oof" sound effect to use instrument 9:
    rom.write_byte(0x1A9C4E, 0x09)

    # Correct the pitch shift value:
    rom.write_byte(0x1A9C51, 0xB6)

    # Modify parameters of instrument 9
    # (I don't actually understand this part, they're just magic values to me)
    rom.write_bytes(0x1A9CAE, [0x7F, 0x7F, 0x00, 0x10, 0x1A, 0x00, 0x00, 0x7F, 0x01])

    # Hook from SPC load routine:
    #  * Check for the read of the sigil
    #  * Once we find it, change the SPC load routine's data pointer to read from the location containing the new sample
    #  * Note: XXXX in the string below is a placeholder for the number of bytes in the .brr sample (little endian)
    #  * Another sigil "$EBEB" is inserted at the end of the data
    #  * When the second sigil is read, we know we're done inserting our data so we can change the data pointer back
    #  * Effect: The new data gets loaded into SPC memory without having to relocate the SPC load routine
    # Slight variation from VT-compatible algorithm: We need to change the data pointer to $00 00 35 and load 538E into Y to pick back up where we left off
    rom.write_bytes(0x128000, [0xB7, 0x00, 0xC8, 0xC8, 0xC9, 0xBE, 0xBE, 0xF0, 0x09, 0xC9, 0xEB, 0xEB, 0xF0, 0x1B, 0x5C, 0xD3, 0x88, 0x00, 0xA2, oof_len_bytes[0], oof_len_bytes[1], 0xA9, 0x80, 0x25, 0x85, 0x01, 0xA9, 0x3A, 0x80, 0x85, 0x00, 0xA0, 0x00, 0x00, 0xA9, 0x88, 0x31, 0x5C, 0xD8, 0x88, 0x00, 0xA9, 0x80, 0x35, 0x64, 0x00, 0x85, 0x01, 0xA2, 0x00, 0x00, 0xA0, 0x8E, 0x53, 0x5C, 0xD4, 0x88, 0x00])

    # The new sample data
    # (We need to insert the second sigil at the end)
    rom.write_bytes(0x12803A, oof_bytes)
    rom.write_bytes(0x12803A + len(oof_bytes), [0xEB, 0xEB])

    # Enemizer patch: prevent Enemizer from overwriting $3188 in SPC memory with an unused sound effect ("WHAT")
    rom.write_bytes(0x13000D, [0x00, 0x00, 0x00, 0x08])


def apply_rom_settings(rom, beep, color, quickswap, menuspeed, music: bool, sprite: str, oof: str, palettes_options,
                       world=None, player=1, allow_random_on_event=False, reduceflashing=False,
                       triforcehud: str = None, deathlink: bool = False, allowcollect: bool = False):
    local_random = random if not world else world.worlds[player].random
    disable_music: bool = not music
    # enable instant item menu
    if menuspeed == 'instant':
        rom.write_byte(0x6DD9A, 0x20)
        rom.write_byte(0x6DF2A, 0x20)
        rom.write_byte(0x6E0E9, 0x20)
    else:
        rom.write_byte(0x6DD9A, 0x11)
        rom.write_byte(0x6DF2A, 0x12)
        rom.write_byte(0x6E0E9, 0x12)
    if menuspeed == 'instant':
        rom.write_byte(0x180048, 0xE8)
    elif menuspeed == 'double':
        rom.write_byte(0x180048, 0x10)
    elif menuspeed == 'triple':
        rom.write_byte(0x180048, 0x18)
    elif menuspeed == 'quadruple':
        rom.write_byte(0x180048, 0x20)
    elif menuspeed == 'half':
        rom.write_byte(0x180048, 0x04)
    else:
        rom.write_byte(0x180048, 0x08)

    # Reduce flashing by nopping out instructions
    if reduceflashing:
        rom.write_bytes(0x17E07, [
            0x06])  # reduce amount of colors changed, add this branch if we need to reduce more  ""+ [0x80] + [(0x81-0x08)]""
        rom.write_bytes(0x17EAB,
                        [0xD0, 0x03, 0xA9, 0x40, 0x29, 0x60])  # nullifies aga lightning, cutscene, vitreous, bat, ether
        # ONLY write to black values with this low pale blue to indicate flashing, that's IT.  ""BNE + : LDA #$2940 : + : RTS""
        rom.write_bytes(0x123FE, [0x72])  # set lightning flash in misery mire (and standard) to brightness 0x72
        rom.write_bytes(0x3FA7B, [0x80, 0xac - 0x7b])  # branch from palette writing lightning on death mountain
        rom.write_byte(0x10817F, 0x01)  # internal rom option
        rom.write_byte(0x3FAB6, 0x80)  # GT flashing
        rom.write_byte(0x3FAC2, 0x80)  # GT flashing
    else:
        rom.write_bytes(0x17E07, [0x00])
        rom.write_bytes(0x17EAB, [0x85, 0x00, 0x29, 0x1F, 0x00, 0x18])
        rom.write_bytes(0x123FE, [0x32])  # original weather flash value
        rom.write_bytes(0x3FA7B, [0xc2, 0x20])  # rep #$20
        rom.write_byte(0x10817F, 0x00)  # internal rom option
        rom.write_byte(0x3FAB6, 0xF0)  # GT flashing
        rom.write_byte(0x3FAC2, 0xD0)  # GT flashing

    rom.write_byte(0x18004B, 0x01 if quickswap else 0x00)

    rom.write_byte(0x0CFE18, 0x00 if disable_music else rom.orig_buffer[0x0CFE18] if rom.orig_buffer else 0x70)
    rom.write_byte(0x0CFEC1, 0x00 if disable_music else rom.orig_buffer[0x0CFEC1] if rom.orig_buffer else 0xC0)
    rom.write_bytes(0x0D0000,
                    [0x00, 0x00] if disable_music else rom.orig_buffer[0x0D0000:0x0D0002] if rom.orig_buffer else [0xDA,
                                                                                                                   0x58])
    rom.write_bytes(0x0D00E7,
                    [0xC4, 0x58] if disable_music else rom.orig_buffer[0x0D00E7:0x0D00E9] if rom.orig_buffer else [0xDA,
                                                                                                                   0x58])

    rom.write_byte(0x18021A, 1 if disable_music else 0x00)

    # set heart beep rate
    rom.write_byte(0x180033, {'off': 0x00, 'half': 0x40, 'quarter': 0x80, 'normal': 0x20, 'double': 0x10}[beep])

    # set heart color
    if color == 'random':
        color = local_random.choice(['red', 'blue', 'green', 'yellow'])
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

    if triforcehud:
        # set triforcehud
        triforce_flag = (rom.read_byte(0x180167) & 0x80) | \
                        {'normal': 0x00, 'hide_goal': 0x01, 'hide_required': 0x02, 'hide_both': 0x03}[triforcehud]
        rom.write_byte(0x180167, triforce_flag)

    if z3pr:
        def buildAndRandomize(option_name, mode):
            options = {
                option_name: True
            }

            data_dir = local_path("data") if is_frozen() else None
            offsets_array = build_offset_collections(options, data_dir)
            restore_maseya_colors(rom, offsets_array)
            if mode == 'default':
                return
            ColorF = z3pr.ColorF

            def next_color_generator():
                while True:
                    yield ColorF(local_random.random(), local_random.random(), local_random.random())

            if mode == 'good':
                mode = 'maseya'
            z3pr.randomize(rom.buffer, mode, offset_collections=offsets_array, random_colors=next_color_generator())

        uw_palettes = palettes_options['dungeon']
        ow_palettes = palettes_options['overworld']
        hud_palettes = palettes_options['hud']
        sword_palettes = palettes_options['sword']
        shield_palettes = palettes_options['shield']
        # link_palettes = palettes_options['link']
        buildAndRandomize("randomize_dungeon", uw_palettes)
        buildAndRandomize("randomize_overworld", ow_palettes)
        buildAndRandomize("randomize_hud", hud_palettes)
        buildAndRandomize("randomize_sword", sword_palettes)
        buildAndRandomize("randomize_shield", shield_palettes)
        # link palette shuffle does not work very well and it's incompatible with random sprite on event
        # buildAndRandomize("randomize_link_sprite", link_palettes)

    else:
        # reset palette if it was adjusted already
        default_ow_palettes(rom)
        default_uw_palettes(rom)
        logging.warning("Could not find z3pr palette shuffle. "
                        "If you want improved palette shuffling please install the maseya-z3pr package.")
        if palettes_options['overworld'] == 'random':
            randomize_ow_palettes(rom, local_random)
        elif palettes_options['overworld'] == 'blackout':
            blackout_ow_palettes(rom)

        if palettes_options['dungeon'] == 'blackout':
            blackout_uw_palettes(rom)
        elif palettes_options['dungeon'] == 'random':
            randomize_uw_palettes(rom, local_random)

    rom.write_byte(0x18008D, (0b00000001 if deathlink else 0) |
                   #          0b00000010 is already used for death_link_allow_survive in super metroid.
                             (0b00000100 if allowcollect else 0))

    apply_random_sprite_on_event(rom, sprite, local_random, allow_random_on_event,
                                 world.sprite_pool[player] if world else [])

    if oof is not None:
        apply_oof_sfx(rom, oof)

    if isinstance(rom, LocalRom):
        rom.write_crc()


def restore_maseya_colors(rom, offsets_array):
    if not rom.orig_buffer:
        return
    for offsetC in offsets_array:
        for address in offsetC:
            rom.write_bytes(address, rom.orig_buffer[address:address + 2])


def set_color(rom, address, color, shade):
    r = round(min(color[0], 0xFF) * pow(0.8, shade) * 0x1F / 0xFF)
    g = round(min(color[1], 0xFF) * pow(0.8, shade) * 0x1F / 0xFF)
    b = round(min(color[2], 0xFF) * pow(0.8, shade) * 0x1F / 0xFF)

    rom.write_bytes(address, ((b << 10) | (g << 5) | (r << 0)).to_bytes(2, byteorder='little', signed=False))


def default_ow_palettes(rom):
    if not rom.orig_buffer:
        return
    rom.write_bytes(0xDE604, rom.orig_buffer[0xDE604:0xDEBB4])

    for address in [0x067FB4, 0x067F94, 0x067FC6, 0x067FE6, 0x067FE1, 0x05FEA9, 0x05FEB3]:
        rom.write_bytes(address, rom.orig_buffer[address:address + 2])


def randomize_ow_palettes(rom, local_random):
    grass, grass2, grass3, dirt, dirt2, water, clouds, dwdirt, \
    dwgrass, dwwater, dwdmdirt, dwdmgrass, dwdmclouds1, dwdmclouds2 = [[local_random.randint(60, 215) for _ in range(3)]
                                                                       for _ in range(14)]
    dwtree = [c + local_random.randint(-20, 10) for c in dwgrass]
    treeleaf = [c + local_random.randint(-20, 10) for c in grass]

    patches = {0x067FB4: (grass, 0), 0x067F94: (grass, 0), 0x067FC6: (grass, 0), 0x067FE6: (grass, 0),
               0x067FE1: (grass, 3), 0x05FEA9: (grass, 0), 0x05FEB3: (dwgrass, 1),
               0x0DD4AC: (grass, 2), 0x0DE6DE: (grass2, 2), 0x0DE6E0: (grass2, 1), 0x0DD4AE: (grass2, 1),
               0x0DE9FA: (grass2, 1), 0x0DEA0E: (grass2, 1), 0x0DE9FE: (grass2, 0),
               0x0DD3D2: (grass2, 2), 0x0DE88C: (grass2, 2), 0x0DE8A8: (grass2, 2), 0x0DE9F8: (grass2, 2),
               0x0DEA4E: (grass2, 2), 0x0DEAF6: (grass2, 2), 0x0DEB2E: (grass2, 2), 0x0DEB4A: (grass2, 2),
               0x0DE892: (grass, 1), 0x0DE886: (grass, 0), 0x0DE6D2: (grass, 0), 0x0DE6FA: (grass, 3),
               0x0DE6FC: (grass, 0), 0x0DE6FE: (grass, 0), 0x0DE70A: (grass, 0), 0x0DE708: (grass, 2),
               0x0DE70C: (grass, 1),
               0x0DE6D4: (dirt, 2), 0x0DE6CA: (dirt, 5), 0x0DE6CC: (dirt, 4), 0x0DE6CE: (dirt, 3), 0x0DE6E2: (dirt, 2),
               0x0DE6D8: (dirt, 5), 0x0DE6DA: (dirt, 4), 0x0DE6DC: (dirt, 2),
               0x0DE6F0: (dirt, 2), 0x0DE6E6: (dirt, 5), 0x0DE6E8: (dirt, 4), 0x0DE6EA: (dirt, 2), 0x0DE6EC: (dirt, 4),
               0x0DE6EE: (dirt, 2),
               0x0DE91E: (grass, 0),
               0x0DE920: (dirt, 2), 0x0DE916: (dirt, 3), 0x0DE934: (dirt, 3),
               0x0DE92C: (grass, 0), 0x0DE93A: (grass, 0), 0x0DE91C: (grass, 1), 0x0DE92A: (grass, 1),
               0x0DEA1C: (grass, 0), 0x0DEA2A: (grass, 0), 0x0DEA30: (grass, 0),
               0x0DEA2E: (dirt, 5),
               0x0DE884: (grass, 3), 0x0DE8AE: (grass, 3), 0x0DE8BE: (grass, 3), 0x0DE8E4: (grass, 3),
               0x0DE938: (grass, 3), 0x0DE9C4: (grass, 3), 0x0DE6D0: (grass, 4),
               0x0DE890: (treeleaf, 1), 0x0DE894: (treeleaf, 0),
               0x0DE924: (water, 3), 0x0DE668: (water, 3), 0x0DE66A: (water, 2), 0x0DE670: (water, 1),
               0x0DE918: (water, 1), 0x0DE66C: (water, 0), 0x0DE91A: (water, 0), 0x0DE92E: (water, 1),
               0x0DEA1A: (water, 1), 0x0DEA16: (water, 3), 0x0DEA10: (water, 4),
               0x0DE66E: (dirt, 3), 0x0DE672: (dirt, 2), 0x0DE932: (dirt, 4), 0x0DE936: (dirt, 2), 0x0DE93C: (dirt, 1),
               0x0DE756: (dirt2, 4), 0x0DE764: (dirt2, 4), 0x0DE772: (dirt2, 4), 0x0DE994: (dirt2, 4),
               0x0DE9A2: (dirt2, 4), 0x0DE758: (dirt2, 3), 0x0DE766: (dirt2, 3), 0x0DE774: (dirt2, 3),
               0x0DE996: (dirt2, 3), 0x0DE9A4: (dirt2, 3), 0x0DE75A: (dirt2, 2), 0x0DE768: (dirt2, 2),
               0x0DE776: (dirt2, 2), 0x0DE778: (dirt2, 2), 0x0DE998: (dirt2, 2), 0x0DE9A6: (dirt2, 2),
               0x0DE9AC: (dirt2, 1), 0x0DE99E: (dirt2, 1), 0x0DE760: (dirt2, 1), 0x0DE77A: (dirt2, 1),
               0x0DE77C: (dirt2, 1), 0x0DE798: (dirt2, 1), 0x0DE980: (dirt2, 1),
               0x0DE75C: (grass3, 2), 0x0DE786: (grass3, 2), 0x0DE794: (grass3, 2), 0x0DE99A: (grass3, 2),
               0x0DE75E: (grass3, 1), 0x0DE788: (grass3, 1), 0x0DE796: (grass3, 1), 0x0DE99C: (grass3, 1),
               0x0DE76A: (clouds, 2), 0x0DE9A8: (clouds, 2), 0x0DE76E: (clouds, 0), 0x0DE9AA: (clouds, 0),
               0x0DE8DA: (clouds, 0), 0x0DE8D8: (clouds, 0), 0x0DE8D0: (clouds, 0), 0x0DE98C: (clouds, 2),
               0x0DE990: (clouds, 0),
               0x0DEB34: (dwtree, 4), 0x0DEB30: (dwtree, 3), 0x0DEB32: (dwtree, 1),
               0x0DE710: (dwdirt, 5), 0x0DE71E: (dwdirt, 5), 0x0DE72C: (dwdirt, 5), 0x0DEAD6: (dwdirt, 5),
               0x0DE712: (dwdirt, 4), 0x0DE720: (dwdirt, 4), 0x0DE72E: (dwdirt, 4), 0x0DE660: (dwdirt, 4),
               0x0DEAD8: (dwdirt, 4), 0x0DEADA: (dwdirt, 3), 0x0DE714: (dwdirt, 3), 0x0DE722: (dwdirt, 3),
               0x0DE730: (dwdirt, 3), 0x0DE732: (dwdirt, 3), 0x0DE734: (dwdirt, 2), 0x0DE736: (dwdirt, 2),
               0x0DE728: (dwdirt, 2), 0x0DE71A: (dwdirt, 2), 0x0DE664: (dwdirt, 2), 0x0DEAE0: (dwdirt, 2),
               0x0DE716: (dwgrass, 3), 0x0DE740: (dwgrass, 3), 0x0DE74E: (dwgrass, 3), 0x0DEAC0: (dwgrass, 3),
               0x0DEACE: (dwgrass, 3), 0x0DEADC: (dwgrass, 3), 0x0DEB24: (dwgrass, 3), 0x0DE752: (dwgrass, 2),
               0x0DE718: (dwgrass, 1), 0x0DE742: (dwgrass, 1), 0x0DE750: (dwgrass, 1), 0x0DEB26: (dwgrass, 1),
               0x0DEAC2: (dwgrass, 1), 0x0DEAD0: (dwgrass, 1), 0x0DEADE: (dwgrass, 1),
               0x0DE65A: (dwwater, 5), 0x0DE65C: (dwwater, 3), 0x0DEAC8: (dwwater, 3), 0x0DEAD2: (dwwater, 2),
               0x0DEABC: (dwwater, 2), 0x0DE662: (dwwater, 2), 0x0DE65E: (dwwater, 1), 0x0DEABE: (dwwater, 1),
               0x0DEA98: (dwwater, 2),
               0x0DE79A: (dwdmdirt, 6), 0x0DE7A8: (dwdmdirt, 6), 0x0DE7B6: (dwdmdirt, 6), 0x0DEB60: (dwdmdirt, 6),
               0x0DEB6E: (dwdmdirt, 6), 0x0DE93E: (dwdmdirt, 6), 0x0DE94C: (dwdmdirt, 6), 0x0DEBA6: (dwdmdirt, 6),
               0x0DE79C: (dwdmdirt, 4), 0x0DE7AA: (dwdmdirt, 4), 0x0DE7B8: (dwdmdirt, 4), 0x0DEB70: (dwdmdirt, 4),
               0x0DEBA8: (dwdmdirt, 4), 0x0DEB72: (dwdmdirt, 3), 0x0DEB74: (dwdmdirt, 3), 0x0DE79E: (dwdmdirt, 3),
               0x0DE7AC: (dwdmdirt, 3), 0x0DEBAA: (dwdmdirt, 3), 0x0DE7A0: (dwdmdirt, 3),
               0x0DE7BC: (dwdmgrass, 3),
               0x0DEBAC: (dwdmdirt, 2), 0x0DE7AE: (dwdmdirt, 2), 0x0DE7C2: (dwdmdirt, 2), 0x0DE7A6: (dwdmdirt, 2),
               0x0DEB7A: (dwdmdirt, 2), 0x0DEB6C: (dwdmdirt, 2), 0x0DE7C0: (dwdmdirt, 2),
               0x0DE7A2: (dwdmgrass, 3), 0x0DE7BE: (dwdmgrass, 3), 0x0DE7CC: (dwdmgrass, 3), 0x0DE7DA: (dwdmgrass, 3),
               0x0DEB6A: (dwdmgrass, 3), 0x0DE948: (dwdmgrass, 3), 0x0DE956: (dwdmgrass, 3), 0x0DE964: (dwdmgrass, 3),
               0x0DE7CE: (dwdmgrass, 1), 0x0DE7A4: (dwdmgrass, 1), 0x0DEBA2: (dwdmgrass, 1), 0x0DEBB0: (dwdmgrass, 1),
               0x0DE644: (dwdmclouds1, 2), 0x0DEB84: (dwdmclouds1, 2), 0x0DE648: (dwdmclouds1, 1),
               0x0DEB88: (dwdmclouds1, 1),
               0x0DEBAE: (dwdmclouds2, 2), 0x0DE7B0: (dwdmclouds2, 2), 0x0DE7B4: (dwdmclouds2, 0),
               0x0DEB78: (dwdmclouds2, 0), 0x0DEBB2: (dwdmclouds2, 0)
               }
    for address, (color, shade) in patches.items():
        set_color(rom, address, color, shade)


def blackout_ow_palettes(rom):
    rom.write_bytes(0xDE604, [0] * 0xC4)
    for i in range(0xDE6C8, 0xDE86C, 70):
        rom.write_bytes(i, [0] * 64)
        rom.write_bytes(i + 66, [0] * 4)
    rom.write_bytes(0xDE86C, [0] * 0x348)

    for address in [0x067FB4, 0x067F94, 0x067FC6, 0x067FE6, 0x067FE1, 0x05FEA9, 0x05FEB3]:
        rom.write_bytes(address, [0, 0])


def default_uw_palettes(rom):
    if not rom.orig_buffer:
        return
    rom.write_bytes(0xDD734, rom.orig_buffer[0xDD734:0xDE544])


def randomize_uw_palettes(rom, local_random):
    for dungeon in range(20):
        wall, pot, chest, floor1, floor2, floor3 = [[local_random.randint(60, 240) for _ in range(3)] for _ in range(6)]

        for i in range(5):
            shade = 10 - (i * 2)
            set_color(rom, 0x0DD734 + (0xB4 * dungeon) + (i * 2), wall, shade)
            set_color(rom, 0x0DD770 + (0xB4 * dungeon) + (i * 2), wall, shade)
            set_color(rom, 0x0DD744 + (0xB4 * dungeon) + (i * 2), wall, shade)
            if dungeon == 0:
                set_color(rom, 0x0DD7CA + (0xB4 * dungeon) + (i * 2), wall, shade)

        if dungeon == 2:
            set_color(rom, 0x0DD74E + (0xB4 * dungeon), wall, 3)
            set_color(rom, 0x0DD750 + (0xB4 * dungeon), wall, 5)
            set_color(rom, 0x0DD73E + (0xB4 * dungeon), wall, 3)
            set_color(rom, 0x0DD740 + (0xB4 * dungeon), wall, 5)

        set_color(rom, 0x0DD7E4 + (0xB4 * dungeon), wall, 4)
        set_color(rom, 0x0DD7E6 + (0xB4 * dungeon), wall, 2)

        set_color(rom, 0xDD7DA + (0xB4 * dungeon), wall, 10)
        set_color(rom, 0xDD7DC + (0xB4 * dungeon), wall, 8)

        set_color(rom, 0x0DD75A + (0xB4 * dungeon), pot, 7)
        set_color(rom, 0x0DD75C + (0xB4 * dungeon), pot, 1)
        set_color(rom, 0x0DD75E + (0xB4 * dungeon), pot, 3)

        set_color(rom, 0x0DD76A + (0xB4 * dungeon), wall, 7)
        set_color(rom, 0x0DD76C + (0xB4 * dungeon), wall, 2)
        set_color(rom, 0x0DD76E + (0xB4 * dungeon), wall, 4)

        set_color(rom, 0x0DD7AE + (0xB4 * dungeon), chest, 2)
        set_color(rom, 0x0DD7B0 + (0xB4 * dungeon), chest, 0)

        for i in range(3):
            shade = 6 - (i * 2)
            set_color(rom, 0x0DD764 + (0xB4 * dungeon) + (i * 2), floor1, shade)
            set_color(rom, 0x0DD782 + (0xB4 * dungeon) + (i * 2), floor1, shade + 3)

            set_color(rom, 0x0DD7A0 + (0xB4 * dungeon) + (i * 2), floor2, shade)
            set_color(rom, 0x0DD7BE + (0xB4 * dungeon) + (i * 2), floor2, shade + 3)

        set_color(rom, 0x0DD7E2 + (0xB4 * dungeon), floor3, 3)
        set_color(rom, 0x0DD796 + (0xB4 * dungeon), floor3, 4)


def blackout_uw_palettes(rom):
    for i in range(0xDD734, 0xDE544, 180):
        rom.write_bytes(i, [0] * 38)
        rom.write_bytes(i + 44, [0] * 76)
        rom.write_bytes(i + 136, [0] * 44)


def get_hash_string(hash):
    return ", ".join([hash_alphabet[code & 0x1F] for code in hash])


def write_string_to_rom(rom, target, string):
    address, maxbytes = text_addresses[target]
    rom.write_bytes(address, MultiByteTextMapper.convert(string, maxbytes))


def write_strings(rom, world, player):
    from . import ALTTPWorld

    w: ALTTPWorld = world.worlds[player]
    local_random = w.random

    tt = TextTable()
    tt.removeUnwantedText()

    # Let's keep this guy's text accurate to the shuffle setting.
    if world.entrance_shuffle[player] in ['vanilla', 'dungeons_full', 'dungeons_simple', 'dungeons_crossed']:
        tt['kakariko_flophouse_man_no_flippers'] = 'I really hate mowing my yard.\n{PAGEBREAK}\nI should move.'
        tt['kakariko_flophouse_man'] = 'I really hate mowing my yard.\n{PAGEBREAK}\nI should move.'

    if world.mode[player] == 'inverted':
        tt['sign_village_of_outcasts'] = 'attention\nferal ducks sighted\nhiding in statues\n\nflute players beware\n'

    def hint_text(dest, ped_hint=False):
        if not dest:
            return "nothing"
        if ped_hint:
            hint = dest.pedestal_hint_text
        else:
            hint = dest.hint_text
        if dest.player != player:
            if ped_hint:
                hint += f" for {world.player_name[dest.player]}!"
            elif isinstance(dest, (Region, Location)):
                hint += f" in {world.player_name[dest.player]}'s world"
            else:
                hint += f" for {world.player_name[dest.player]}"
        return hint

    if world.scams[player].gives_king_zora_hint:
        # Zora hint
        zora_location = world.get_location("King Zora", player)
        tt['zora_tells_cost'] = f"You got 500 rupees to buy {hint_text(zora_location.item)}" \
                                f"\n  ≥ Duh\n    Oh carp\n{{CHOICE}}"
    if world.scams[player].gives_bottle_merchant_hint:
        # Bottle Vendor hint
        vendor_location = world.get_location("Bottle Merchant", player)
        tt['bottle_vendor_choice'] = f"I gots {hint_text(vendor_location.item)}\nYous gots 100 rupees?" \
                                     f"\n  ≥ I want\n    no way!\n{{CHOICE}}"

    # First we write hints about entrances, some from the inconvenient list others from all reasonable entrances.
    if world.hints[player]:
        if world.hints[player].value >= 2:
            if world.hints[player] == "full":
                tt['sign_north_of_links_house'] = '> Randomizer The telepathic tiles have hints!'
            else:
                tt['sign_north_of_links_house'] = '> Randomizer The telepathic tiles can have hints!'
            hint_locations = HintLocations.copy()
            local_random.shuffle(hint_locations)
            all_entrances = list(world.get_entrances(player))
            local_random.shuffle(all_entrances)

            # First we take care of the one inconvenient dungeon in the appropriately simple shuffles.
            entrances_to_hint = {}
            entrances_to_hint.update(InconvenientDungeonEntrances)
            if world.shuffle_ganon:
                if world.mode[player] == 'inverted':
                    entrances_to_hint.update({'Inverted Ganons Tower': 'The sealed castle door'})
                else:
                    entrances_to_hint.update({'Ganons Tower': 'Ganon\'s Tower'})
            if world.entrance_shuffle[player] in ['simple', 'restricted']:
                for entrance in all_entrances:
                    if entrance.name in entrances_to_hint:
                        this_hint = entrances_to_hint[entrance.name] + ' leads to ' + hint_text(
                            entrance.connected_region) + '.'
                        tt[hint_locations.pop(0)] = this_hint
                        entrances_to_hint = {}
                        break
            # Now we write inconvenient locations for most shuffles and finish taking care of the less chaotic ones.
            entrances_to_hint.update(InconvenientOtherEntrances)
            if world.entrance_shuffle[player] in ['vanilla', 'dungeons_simple', 'dungeons_full', 'dungeons_crossed']:
                hint_count = 0
            elif world.entrance_shuffle[player] in ['simple', 'restricted']:
                hint_count = 2
            else:
                hint_count = 4
            for entrance in all_entrances:
                if entrance.name in entrances_to_hint:
                    if hint_count:
                        this_hint = entrances_to_hint[entrance.name] + ' leads to ' + hint_text(
                            entrance.connected_region) + '.'
                        tt[hint_locations.pop(0)] = this_hint
                        entrances_to_hint.pop(entrance.name)
                        hint_count -= 1
                    else:
                        break

            # Next we handle hints for randomly selected other entrances,
            # curating the selection intelligently based on shuffle.
            if world.entrance_shuffle[player] not in ['simple', 'restricted']:
                entrances_to_hint.update(ConnectorEntrances)
                entrances_to_hint.update(DungeonEntrances)
                if world.mode[player] == 'inverted':
                    entrances_to_hint.update({'Inverted Agahnims Tower': 'The dark mountain tower'})
                else:
                    entrances_to_hint.update({'Agahnims Tower': 'The sealed castle door'})
            elif world.entrance_shuffle[player] == 'restricted':
                entrances_to_hint.update(ConnectorEntrances)
            entrances_to_hint.update(OtherEntrances)
            if world.mode[player] == 'inverted':
                entrances_to_hint.update({'Inverted Dark Sanctuary': 'The dark sanctuary cave'})
                entrances_to_hint.update({'Inverted Big Bomb Shop': 'The old hero\'s dark home'})
                entrances_to_hint.update({'Inverted Links House': 'The old hero\'s light home'})
            else:
                entrances_to_hint.update({'Dark Sanctuary Hint': 'The dark sanctuary cave'})
                entrances_to_hint.update({'Big Bomb Shop': 'The old bomb shop'})
            if world.entrance_shuffle[player] != 'insanity':
                entrances_to_hint.update(InsanityEntrances)
                if world.shuffle_ganon:
                    if world.mode[player] == 'inverted':
                        entrances_to_hint.update({'Inverted Pyramid Entrance': 'The extra castle passage'})
                    else:
                        entrances_to_hint.update({'Pyramid Ledge': 'The pyramid ledge'})
            hint_count = 4 if world.entrance_shuffle[player] not in ['vanilla', 'dungeons_simple', 'dungeons_full',
                                                            'dungeons_crossed'] else 0
            for entrance in all_entrances:
                if entrance.name in entrances_to_hint:
                    if hint_count:
                        this_hint = entrances_to_hint[entrance.name] + ' leads to ' + hint_text(
                            entrance.connected_region) + '.'
                        tt[hint_locations.pop(0)] = this_hint
                        entrances_to_hint.pop(entrance.name)
                        hint_count -= 1
                    else:
                        break

            # Next we write a few hints for specific inconvenient locations. We don't make many because in entrance this is highly unpredictable.
            locations_to_hint = InconvenientLocations.copy()
            if world.entrance_shuffle[player] in ['vanilla', 'dungeons_simple', 'dungeons_full', 'dungeons_crossed']:
                locations_to_hint.extend(InconvenientVanillaLocations)
            local_random.shuffle(locations_to_hint)
            hint_count = 3 if world.entrance_shuffle[player] not in ['vanilla', 'dungeons_simple', 'dungeons_full',
                                                            'dungeons_crossed'] else 5
            for location in locations_to_hint[:hint_count]:
                if location == 'Swamp Left':
                    if local_random.randint(0, 1):
                        first_item = hint_text(world.get_location('Swamp Palace - West Chest', player).item)
                        second_item = hint_text(world.get_location('Swamp Palace - Big Key Chest', player).item)
                    else:
                        second_item = hint_text(world.get_location('Swamp Palace - West Chest', player).item)
                        first_item = hint_text(world.get_location('Swamp Palace - Big Key Chest', player).item)
                    this_hint = ('The westmost chests in Swamp Palace contain ' + first_item + ' and ' + second_item + '.')
                    tt[hint_locations.pop(0)] = this_hint
                elif location == 'Mire Left':
                    if local_random.randint(0, 1):
                        first_item = hint_text(world.get_location('Misery Mire - Compass Chest', player).item)
                        second_item = hint_text(world.get_location('Misery Mire - Big Key Chest', player).item)
                    else:
                        second_item = hint_text(world.get_location('Misery Mire - Compass Chest', player).item)
                        first_item = hint_text(world.get_location('Misery Mire - Big Key Chest', player).item)
                    this_hint = ('The westmost chests in Misery Mire contain ' + first_item + ' and ' + second_item + '.')
                    tt[hint_locations.pop(0)] = this_hint
                elif location == 'Tower of Hera - Big Key Chest':
                    this_hint = 'Waiting in the Tower of Hera basement leads to ' + hint_text(
                        world.get_location(location, player).item) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                elif location == 'Ganons Tower - Big Chest':
                    this_hint = 'The big chest in Ganon\'s Tower contains ' + hint_text(
                        world.get_location(location, player).item) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                elif location == 'Thieves\' Town - Big Chest':
                    this_hint = 'The big chest in Thieves\' Town contains ' + hint_text(
                        world.get_location(location, player).item) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                elif location == 'Ice Palace - Big Chest':
                    this_hint = 'The big chest in Ice Palace contains ' + hint_text(
                        world.get_location(location, player).item) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                elif location == 'Eastern Palace - Big Key Chest':
                    this_hint = 'The antifairy guarded chest in Eastern Palace contains ' + hint_text(
                        world.get_location(location, player).item) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                elif location == 'Sahasrahla':
                    this_hint = 'Sahasrahla seeks a green pendant for ' + hint_text(
                        world.get_location(location, player).item) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                elif location == 'Graveyard Cave':
                    this_hint = 'The cave north of the graveyard contains ' + hint_text(
                        world.get_location(location, player).item) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                else:
                    this_hint = location + ' contains ' + hint_text(world.get_location(location, player).item) + '.'
                    tt[hint_locations.pop(0)] = this_hint

            # Lastly we write hints to show where certain interesting items are.
            items_to_hint = RelevantItems.copy()
            if world.small_key_shuffle[player].hints_useful:
                items_to_hint |= item_name_groups["Small Keys"]
            if world.big_key_shuffle[player].hints_useful:
                items_to_hint |= item_name_groups["Big Keys"]

            if world.hints[player] == "full":
                hint_count = len(hint_locations)  # fill all remaining hint locations with Item hints.
            else:
                hint_count = 5 if world.entrance_shuffle[player] not in ['vanilla', 'dungeons_simple', 'dungeons_full',
                                                                'dungeons_crossed'] else 8
            hint_count = min(hint_count, len(items_to_hint), len(hint_locations))
            if hint_count:
                locations = world.find_items_in_locations(items_to_hint, player, True)
                local_random.shuffle(locations)
                # make locked locations less likely to appear as hint,
                # chances are the lock means the player already knows.
                locations.sort(key=lambda sorting_location: not sorting_location.locked)
                for x in range(min(hint_count, len(locations))):
                    this_location = locations.pop()
                    this_hint = this_location.item.hint_text + ' can be found ' + hint_text(this_location) + '.'
                    tt[hint_locations.pop(0)] = this_hint

            if hint_locations:
                # All remaining hint slots are filled with junk hints.
                # It is done this way to ensure the same junk hint isn't selected twice.
                junk_hints = junk_texts.copy()
                local_random.shuffle(junk_hints)
                for location, text in zip(hint_locations, junk_hints):
                    tt[location] = text

    # We still need the older hints of course. Those are done here.

    silverarrows = world.find_item_locations('Silver Bow', player, True)
    local_random.shuffle(silverarrows)
    silverarrow_hint = (
            ' %s?' % hint_text(silverarrows[0]).replace('Ganon\'s', 'my')) if silverarrows else '?\nI think not!'
    tt['ganon_phase_3_no_silvers'] = 'Did you find the silver arrows%s' % silverarrow_hint
    tt['ganon_phase_3_no_silvers_alt'] = 'Did you find the silver arrows%s' % silverarrow_hint
    if world.worlds[player].has_progressive_bows and (w.difficulty_requirements.progressive_bow_limit >= 2 or (
            world.swordless[player] or world.glitches_required[player] == 'no_glitches')):
        prog_bow_locs = world.find_item_locations('Progressive Bow', player, True)
        local_random.shuffle(prog_bow_locs)
        found_bow = False
        found_bow_alt = False
        while prog_bow_locs and not (found_bow and found_bow_alt):
            bow_loc = prog_bow_locs.pop()
            if bow_loc.item.code == 0x65 or (found_bow and not prog_bow_locs):
                found_bow_alt = True
                target = 'ganon_phase_3_no_silvers'
            else:
                found_bow = True
                target = 'ganon_phase_3_no_silvers_alt'
            silverarrow_hint = (' %s?' % hint_text(bow_loc).replace('Ganon\'s', 'my'))
            tt[target] = 'Did you find the silver arrows%s' % silverarrow_hint

    crystal5 = world.find_item('Crystal 5', player)
    crystal6 = world.find_item('Crystal 6', player)
    tt['bomb_shop'] = 'Big Bomb?\nMy supply is blocked until you clear %s and %s.' % (
        crystal5.hint_text, crystal6.hint_text)

    greenpendant = world.find_item('Green Pendant', player)
    tt['sahasrahla_bring_courage'] = 'I lost my family heirloom in %s' % greenpendant.hint_text

    if world.crystals_needed_for_gt[player] == 1:
        tt['sign_ganons_tower'] = 'You need a crystal to enter.'
    else:
        tt['sign_ganons_tower'] = f'You need {world.crystals_needed_for_gt[player]} crystals to enter.'

    if world.goal[player] == 'bosses':
        tt['sign_ganon'] = 'You need to kill all bosses, Ganon last.'
    elif world.goal[player] == 'ganon_pedestal':
        tt['sign_ganon'] = 'You need to pull the pedestal to defeat Ganon.'
    elif world.goal[player] == "ganon":
        if world.crystals_needed_for_ganon[player] == 1:
            tt['sign_ganon'] = 'You need a crystal to beat Ganon and have beaten Agahnim atop Ganons Tower.'
        else:
            tt['sign_ganon'] = f'You need {world.crystals_needed_for_ganon[player]} crystals to beat Ganon and ' \
                               f'have beaten Agahnim atop Ganons Tower'
    else:
        if world.crystals_needed_for_ganon[player] == 1:
            tt['sign_ganon'] = 'You need a crystal to beat Ganon.'
        else:
            tt['sign_ganon'] = f'You need {world.crystals_needed_for_ganon[player]} crystals to beat Ganon.'

    tt['uncle_leaving_text'] = Uncle_texts[local_random.randint(0, len(Uncle_texts) - 1)]
    tt['end_triforce'] = "{NOBORDER}\n" + Triforce_texts[local_random.randint(0, len(Triforce_texts) - 1)]
    tt['bomb_shop_big_bomb'] = BombShop2_texts[local_random.randint(0, len(BombShop2_texts) - 1)]

    # this is what shows after getting the green pendant item in rando
    tt['sahasrahla_quest_have_master_sword'] = Sahasrahla2_texts[local_random.randint(0, len(Sahasrahla2_texts) - 1)]
    tt['blind_by_the_light'] = Blind_texts[local_random.randint(0, len(Blind_texts) - 1)]

    triforce_pieces_required = max(0, w.treasure_hunt_required -
                                   sum(1 for item in world.precollected_items[player] if item.name == "Triforce Piece"))

    if world.goal[player] in ['triforce_hunt', 'local_triforce_hunt']:
        tt['ganon_fall_in_alt'] = 'Why are you even here?\n You can\'t even hurt me! Get the Triforce Pieces.'
        tt['ganon_phase_3_alt'] = 'Seriously? Go Away, I will not Die.'
        if world.goal[player] == 'triforce_hunt' and world.players > 1:
            tt['sign_ganon'] = 'Go find the Triforce pieces with your friends... Ganon is invincible!'
        else:
            tt['sign_ganon'] = 'Go find the Triforce pieces... Ganon is invincible!'
        if triforce_pieces_required > 1:
            tt['murahdahla'] = "Hello @. I\nam Murahdahla, brother of\nSahasrahla and Aginah. Behold the power of\n" \
                               "invisibility.\n\n\n\n… … …\n\nWait! you can see me? I knew I should have\n" \
                               "hidden in  a hollow tree. If you bring\n%d Triforce pieces out of %d, I can reassemble it." % \
                               (triforce_pieces_required, w.treasure_hunt_total)
        else:
            tt['murahdahla'] = "Hello @. I\nam Murahdahla, brother of\nSahasrahla and Aginah. Behold the power of\n" \
                               "invisibility.\n\n\n\n… … …\n\nWait! you can see me? I knew I should have\n" \
                               "hidden in  a hollow tree. If you bring\n%d Triforce piece out of %d, I can reassemble it." % \
                               (triforce_pieces_required, w.treasure_hunt_total)
    elif world.goal[player] in ['pedestal']:
        tt['ganon_fall_in_alt'] = 'Why are you even here?\n You can\'t even hurt me! Your goal is at the pedestal.'
        tt['ganon_phase_3_alt'] = 'Seriously? Go Away, I will not Die.'
        tt['sign_ganon'] = 'You need to get to the pedestal... Ganon is invincible!'
    else:
        tt['ganon_fall_in'] = Ganon1_texts[local_random.randint(0, len(Ganon1_texts) - 1)]
        tt['ganon_fall_in_alt'] = 'You cannot defeat me until you finish your goal!'
        tt['ganon_phase_3_alt'] = 'Got wax in\nyour ears?\nI can not die!'
        if triforce_pieces_required > 1:
            if world.goal[player] == 'ganon_triforce_hunt' and world.players > 1:
                tt['sign_ganon'] = 'You need to find %d Triforce pieces out of %d with your friends to defeat Ganon.' % \
                                   (triforce_pieces_required, w.treasure_hunt_total)
            elif world.goal[player] in ['ganon_triforce_hunt', 'local_ganon_triforce_hunt']:
                tt['sign_ganon'] = 'You need to find %d Triforce pieces out of %d to defeat Ganon.' % \
                                   (triforce_pieces_required, w.treasure_hunt_total)
        else:
            if world.goal[player] == 'ganon_triforce_hunt' and world.players > 1:
                tt['sign_ganon'] = 'You need to find %d Triforce piece out of %d with your friends to defeat Ganon.' % \
                                   (triforce_pieces_required, w.treasure_hunt_total)
            elif world.goal[player] in ['ganon_triforce_hunt', 'local_ganon_triforce_hunt']:
                tt['sign_ganon'] = 'You need to find %d Triforce piece out of %d to defeat Ganon.' % \
                                   (triforce_pieces_required, w.treasure_hunt_total)

    tt['kakariko_tavern_fisherman'] = TavernMan_texts[local_random.randint(0, len(TavernMan_texts) - 1)]

    pedestalitem = world.get_location('Master Sword Pedestal', player).item
    pedestal_text = 'Some Hot Air' if pedestalitem is None else hint_text(pedestalitem,
                                                                          True) if pedestalitem.pedestal_hint_text is not None else 'Unknown Item'
    tt['mastersword_pedestal_translated'] = pedestal_text
    pedestal_credit_text = 'and the Hot Air' if pedestalitem is None else \
        w.pedestal_credit_texts.get(pedestalitem.code, 'and the Unknown Item')

    etheritem = world.get_location('Ether Tablet', player).item
    ether_text = 'Some Hot Air' if etheritem is None else hint_text(etheritem,
                                                                    True) if etheritem.pedestal_hint_text is not None else 'Unknown Item'
    tt['tablet_ether_book'] = ether_text
    bombositem = world.get_location('Bombos Tablet', player).item
    bombos_text = 'Some Hot Air' if bombositem is None else hint_text(bombositem,
                                                                      True) if bombositem.pedestal_hint_text is not None else 'Unknown Item'
    tt['tablet_bombos_book'] = bombos_text

    # inverted spawn menu changes
    if world.mode[player] == 'inverted':
        tt['menu_start_2'] = "{MENU}\n{SPEED0}\n≥@'s house\n Dark Chapel\n{CHOICE3}"
        tt['menu_start_3'] = "{MENU}\n{SPEED0}\n≥@'s house\n Dark Chapel\n Mountain Cave\n{CHOICE2}"

    for at, text, _ in world.plando_texts[player]:

        if at not in tt:
            raise Exception(f"No text target \"{at}\" found.")
        else:
            tt[at] = "\n".join(text)

    rom.write_bytes(0xE0000, tt.getBytes())

    credits = Credits()

    sickkiditem = world.get_location('Sick Kid', player).item
    sickkiditem_text = local_random.choice(SickKid_texts) \
        if sickkiditem is None or sickkiditem.code not in w.sickkid_credit_texts \
        else w.sickkid_credit_texts[sickkiditem.code]

    zoraitem = world.get_location('King Zora', player).item
    zoraitem_text = local_random.choice(Zora_texts) \
        if zoraitem is None or zoraitem.code not in w.zora_credit_texts \
        else w.zora_credit_texts[zoraitem.code]

    magicshopitem = world.get_location('Potion Shop', player).item
    magicshopitem_text = local_random.choice(MagicShop_texts) \
        if magicshopitem is None or magicshopitem.code not in w.magicshop_credit_texts \
        else w.magicshop_credit_texts[magicshopitem.code]

    fluteboyitem = world.get_location('Flute Spot', player).item
    fluteboyitem_text = local_random.choice(FluteBoy_texts) \
        if fluteboyitem is None or fluteboyitem.code not in w.fluteboy_credit_texts \
        else w.fluteboy_credit_texts[fluteboyitem.code]

    credits.update_credits_line('castle', 0, local_random.choice(KingsReturn_texts))
    credits.update_credits_line('sanctuary', 0, local_random.choice(Sanctuary_texts))

    credits.update_credits_line('kakariko', 0,
                                local_random.choice(Kakariko_texts).format(local_random.choice(Sahasrahla_names)))
    credits.update_credits_line('desert', 0, local_random.choice(DesertPalace_texts))
    credits.update_credits_line('hera', 0, local_random.choice(MountainTower_texts))
    credits.update_credits_line('house', 0, local_random.choice(LinksHouse_texts))
    credits.update_credits_line('zora', 0, zoraitem_text)
    credits.update_credits_line('witch', 0, magicshopitem_text)
    credits.update_credits_line('lumberjacks', 0, local_random.choice(Lumberjacks_texts))
    credits.update_credits_line('grove', 0, fluteboyitem_text)
    credits.update_credits_line('well', 0, local_random.choice(WishingWell_texts))
    credits.update_credits_line('smithy', 0, local_random.choice(Blacksmiths_texts))
    credits.update_credits_line('kakariko2', 0, sickkiditem_text)
    credits.update_credits_line('bridge', 0, local_random.choice(DeathMountain_texts))
    credits.update_credits_line('woods', 0, local_random.choice(LostWoods_texts))
    credits.update_credits_line('pedestal', 0, pedestal_credit_text)

    (pointers, data) = credits.get_bytes()
    rom.write_bytes(0x181500, data)
    rom.write_bytes(0x76CC0, [byte for p in pointers for byte in [p & 0xFF, p >> 8 & 0xFF]])


def set_inverted_mode(world, player, rom):
    rom.write_byte(snes_to_pc(0x0283E0), 0xF0)  # residual portals
    rom.write_byte(snes_to_pc(0x02B34D), 0xF0)
    rom.write_byte(snes_to_pc(0x06DB78), 0x8B)
    rom.write_byte(snes_to_pc(0x05AF79), 0xF0)
    rom.write_byte(snes_to_pc(0x0DB3C5), 0xC6)
    rom.write_byte(snes_to_pc(0x07A3F4), 0xF0)  # duck
    rom.write_byte(0xDC21D, 0x6B)  # inverted mode flute activation (skip weathervane overlay)
    rom.write_bytes(0x48DB3, [0xF8, 0x01])  # inverted mode (bird X)
    rom.write_byte(0x48D5E, 0x01)  # inverted mode (rock X)
    rom.write_bytes(0x48CC1 + 36, bytes([0xF8] * 12))  # (rock X)
    rom.write_int16s(snes_to_pc(0x02E849),
                     [0x0043, 0x0056, 0x0058, 0x006C, 0x006F, 0x0070, 0x007B, 0x007F, 0x001B])  # dw flute
    rom.write_int16(snes_to_pc(0x02E8D5), 0x07C8)
    rom.write_int16(snes_to_pc(0x02E8F7), 0x01F8)
    rom.write_byte(snes_to_pc(0x08D40C), 0xD0)  # morph proof
    # the following bytes should only be written in vanilla
    # or they'll overwrite the randomizer's shuffles
    if world.entrance_shuffle[player] == 'vanilla':
        rom.write_byte(0xDBB73 + 0x23, 0x37)  # switch AT and GT
        rom.write_byte(0xDBB73 + 0x36, 0x24)
        rom.write_int16(0x15AEE + 2 * 0x38, 0x00E0)
        rom.write_int16(0x15AEE + 2 * 0x25, 0x000C)
    if world.entrance_shuffle[player] in ['vanilla', 'dungeons_simple', 'dungeons_full', 'dungeons_crossed']:
        rom.write_byte(0x15B8C, 0x6C)
        rom.write_byte(0xDBB73 + 0x00, 0x53)  # switch bomb shop and links house
        rom.write_byte(0xDBB73 + 0x52, 0x01)
        rom.write_byte(0xDBB73 + 0x15, 0x06)  # bumper and old man cave
        rom.write_int16(0x15AEE + 2 * 0x17, 0x00F0)
        rom.write_byte(0xDBB73 + 0x05, 0x16)
        rom.write_int16(0x15AEE + 2 * 0x07, 0x00FB)
        rom.write_byte(0xDBB73 + 0x2D, 0x17)
        rom.write_int16(0x15AEE + 2 * 0x2F, 0x00EB)
        rom.write_byte(0xDBB73 + 0x06, 0x2E)
        rom.write_int16(0x15AEE + 2 * 0x08, 0x00E6)
        rom.write_byte(0xDBB73 + 0x16, 0x5E)
        rom.write_byte(0xDBB73 + 0x6F, 0x07)  # DDM fairy to old man cave
        rom.write_int16(0x15AEE + 2 * 0x18, 0x00F1)
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
    if world.entrance_shuffle[player] in ['vanilla', 'dungeons_full', 'dungeons_simple', 'dungeons_crossed']:
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
    rom.write_int16(snes_to_pc(0x02E87B), 0x00AE)  # move flute spot 9
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
    rom.write_int16(snes_to_pc(0x308300), 0x0140)  # new pyramid hole entrance
    rom.write_int16(snes_to_pc(0x308320), 0x001B)
    if world.entrance_shuffle[player] in ['vanilla', 'dungeons_simple', 'dungeons_full', 'dungeons_crossed']:
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
    if world.entrance_shuffle[player] in ['vanilla', 'dungeons_simple', 'dungeons_full', 'dungeons_crossed']:
        rom.write_byte(0xDBB73 + 0x35, 0x36)
    rom.write_byte(snes_to_pc(0x09D436), 0xF3)  # remove castle gate warp
    if world.entrance_shuffle[player] in ['vanilla', 'dungeons_simple', 'dungeons_full', 'dungeons_crossed']:
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
    dark_sanc = world.get_region('Inverted Dark Sanctuary', player)
    dark_sanc_entrance = str([i for i in dark_sanc.entrances if i.parent_region.name != 'Menu'][0].name)
    room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2 = \
        door_addresses[dark_sanc_entrance][1]
    door_index = door_addresses[str(dark_sanc_entrance)][0]

    rom.write_byte(0x180241, 0x01)
    rom.write_byte(0x180248, door_index + 1)
    rom.write_int16(0x180250, room_id)
    rom.write_byte(0x180252, ow_area)
    rom.write_int16s(0x180253, [vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x])
    rom.write_bytes(0x180262, [unknown_1, unknown_2, 0x00])


InconvenientDungeonEntrances = {'Turtle Rock': 'Turtle Rock Main',
                                'Misery Mire': 'Misery Mire',
                                'Ice Palace': 'Ice Palace',
                                'Skull Woods Final Section': 'The back of Skull Woods',
                                }

InconvenientOtherEntrances = {'Death Mountain Return Cave (West)': 'The SW DM foothills cave',
                              'Mimic Cave': 'Mimic Ledge',
                              'Dark World Hammer Peg Cave': 'The rows of pegs',
                              'Pyramid Fairy': 'The crack on the pyramid'
                              }

ConnectorEntrances = {'Elder House (East)': 'Elder House',
                      'Elder House (West)': 'Elder House',
                      'Two Brothers House (East)': 'Eastern Quarreling Brothers\' house',
                      'Old Man Cave (West)': 'The lower DM entrance',
                      'Bumper Cave (Bottom)': 'The lower Bumper Cave',
                      'Superbunny Cave (Top)': 'The summit of dark DM cave',
                      'Superbunny Cave (Bottom)': 'The base of east dark DM',
                      'Hookshot Cave': 'The rock on dark DM',
                      'Two Brothers House (West)': 'The door near the race game',
                      'Old Man Cave (East)': 'The SW-most cave on west DM',
                      'Old Man House (Bottom)': 'A cave with a door on west DM',
                      'Old Man House (Top)': 'The eastmost cave on west DM',
                      'Death Mountain Return Cave (East)': 'The westmost cave on west DM',
                      'Spectacle Rock Cave Peak': 'The highest cave on west DM',
                      'Spectacle Rock Cave': 'The right ledge on west DM',
                      'Spectacle Rock Cave (Bottom)': 'The left ledge on west DM',
                      'Paradox Cave (Bottom)': 'The right paired cave on east DM',
                      'Paradox Cave (Middle)': 'The southmost cave on east DM',
                      'Paradox Cave (Top)': 'The east DM summit cave',
                      'Fairy Ascension Cave (Bottom)': 'The east DM cave behind rocks',
                      'Fairy Ascension Cave (Top)': 'The central ledge on east DM',
                      'Spiral Cave': 'The left ledge on east DM',
                      'Spiral Cave (Bottom)': 'The SWmost cave on east DM'
                      }

DungeonEntrances = {'Eastern Palace': 'Eastern Palace',
                    'Hyrule Castle Entrance (South)': 'The ground level castle door',
                    'Thieves Town': 'Thieves\' Town',
                    'Swamp Palace': 'Swamp Palace',
                    'Dark Death Mountain Ledge (West)': 'The East dark DM connector ledge',
                    'Dark Death Mountain Ledge (East)': 'The East dark DM connector ledge',
                    'Desert Palace Entrance (South)': 'The book sealed passage',
                    'Tower of Hera': 'The Tower of Hera',
                    'Palace of Darkness': 'Palace of Darkness',
                    'Hyrule Castle Entrance (West)': 'The left castle door',
                    'Hyrule Castle Entrance (East)': 'The right castle door',
                    'Desert Palace Entrance (West)': 'The westmost building in the desert',
                    'Desert Palace Entrance (North)': 'The northmost cave in the desert'
                    }

OtherEntrances = {'Blinds Hideout': 'Blind\'s old house',
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
                  'Dark Lake Hylia Fairy': 'The cave NE dark Lake Hylia',
                  'C-Shaped House': 'The NE house in Village of Outcasts',
                  'Dark Death Mountain Fairy': 'The SW cave on dark DM',
                  'Dark Lake Hylia Shop': 'The building NW dark Lake Hylia',
                  'Village of Outcasts Shop': 'The hammer sealed building',
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
                 'telepathic_tile_ice_entrance',
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

InconvenientVanillaLocations = ['Graveyard Cave',
                                'Mimic Cave']


RelevantItems = progression_items - {"Triforce", "Activated Flute"} - item_name_groups["Small Keys"] - item_name_groups["Big Keys"] \
             | item_name_groups["Mails"] | item_name_groups["Shields"]


hash_alphabet = [
    "Bow", "Boomerang", "Hookshot", "Bomb", "Mushroom", "Powder", "Rod", "Pendant", "Bombos", "Ether", "Quake",
    "Lamp", "Hammer", "Shovel", "Flute", "Bug Net", "Book", "Bottle", "Potion", "Cane", "Cape", "Mirror", "Boots",
    "Gloves", "Flippers", "Pearl", "Shield", "Tunic", "Heart", "Map", "Compass", "Key"
]


class LttPDeltaPatch(worlds.Files.APDeltaPatch):
    hash = LTTPJPN10HASH
    game = "A Link to the Past"
    patch_file_ending = ".aplttp"

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
        if LTTPJPN10HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for Japan(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_settings()
    if not file_name:
        file_name = options["lttp_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
