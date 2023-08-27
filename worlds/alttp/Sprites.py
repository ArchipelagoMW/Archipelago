from __future__ import annotations

import concurrent.futures
import io
import json
import logging
import os
import random
import struct
import threading
from typing import Optional, TYPE_CHECKING

import bsdiff4

from Utils import user_path, read_snes_rom, parse_yaml, local_path
if TYPE_CHECKING:
    from .Rom import LocalRom

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
                for dir in [user_path('data', 'sprites', 'alttpr'), user_path('data', 'sprites', 'custom')]:
                    for file in os.listdir(dir):
                        pool.submit(load_sprite_from_file, os.path.join(dir, file))


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
        elif filedata.startswith(b'ZSPR'):
            self.from_zspr(filedata, filename)
        else:
            self.valid = False

    def get_vanilla_sprite_data(self):
        from .Rom import get_base_rom_path
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

    def write_to_rom(self, rom: "LocalRom"):
        if not self.valid:
            logging.warning("Tried writing invalid sprite to rom, skipping.")
            return
        rom.write_bytes(0x80000, self.sprite)
        rom.write_bytes(0xDD308, self.palette)
        rom.write_bytes(0xDEDF5, self.glove_palette)
        rom.write_bytes(0x300000, self.sprite)
        rom.write_bytes(0x307000, self.palette)
        rom.write_bytes(0x307078, self.glove_palette)


def update_sprites():
    from tkinter import Tk
    from LttPAdjuster import get_image_for_sprite
    from LttPAdjuster import BackgroundTaskProgress
    from LttPAdjuster import BackgroundTaskProgressNullWindow
    from LttPAdjuster import update_sprites

    # Target directories
    input_dir = user_path("data", "sprites", "alttpr")
    output_dir = local_path("WebHostLib", "static", "generated")  # TODO: move to user_path

    os.makedirs(os.path.join(output_dir, "sprites"), exist_ok=True)
    # update sprites through gui.py's functions
    done = threading.Event()
    try:
        top = Tk()
    except:
        task = BackgroundTaskProgressNullWindow(update_sprites, lambda successful, resultmessage: done.set())
    else:
        top.withdraw()
        task = BackgroundTaskProgress(top, update_sprites, "Updating Sprites", lambda succesful, resultmessage: done.set())
    while not done.isSet():
        task.do_events()

    spriteData = []

    for file in (file for file in os.listdir(input_dir) if not file.startswith(".")):
        sprite = Sprite(os.path.join(input_dir, file))

        if not sprite.name:
            print("Warning:", file, "has no name.")
            sprite.name = file.split(".", 1)[0]
        if sprite.valid:
            with open(os.path.join(output_dir, "sprites", f"{os.path.splitext(file)[0]}.gif"), 'wb') as image:
                image.write(get_image_for_sprite(sprite, True))
            spriteData.append({"file": file, "author": sprite.author_name, "name": sprite.name})
        else:
            print(file, "dropped, as it has no valid sprite data.")
    spriteData.sort(key=lambda entry: entry["name"])
    with open(f'{output_dir}/spriteData.json', 'w') as file:
        json.dump({"sprites": spriteData}, file, indent=1)
    return spriteData


def apply_random_sprite_on_event(rom: "LocalRom", sprite, local_random, allow_random_on_event, sprite_pool):
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
