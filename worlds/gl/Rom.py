import json
import traceback
import typing
import zlib
import io
import os

import Utils
from typing import List, Dict, Tuple
from BaseClasses import Location
from settings import get_settings
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin
from .Arrays import level_locations, level_size, level_address, item_dict, level_header
from .Items import items_by_id

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld


def get_base_rom_as_bytes() -> bytes:
    try:
        with open(get_settings().gl_options.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
    except Exception as e:
        traceback.print_exc()

    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


class LevelData:
    stream: io.BytesIO
    header: bytearray
    item_addr: int
    spawner_addr: int
    obj_addr: int
    chest_addr: int
    end_addr: int
    end_addr2: int
    end_addr3: int
    items: List[bytearray]
    spawners: List[bytearray]
    objects: List[bytearray]
    chests: List[bytearray]
    end: bytes
    obelisk = 0
    item = 0

    def __init__(self):
        self.items = []
        self.spawners = []
        self.objects = []
        self.chests = []
        self.end = bytes()


class GLPatchExtension(APPatchExtension):
    game = "Gauntlet Legends"

    @staticmethod
    def patch_counts(caller: APProcedurePatch, rom: bytes) -> bytes:
        stream = io.BytesIO(rom)
        stream.seek(0x67E7E0)
        data = io.BytesIO(zdec(stream.read(0x380)))
        data.seek(0x1A, 0)
        data.write(bytes([0xFF, 0xFF]))
        data.seek(0x37, 0)
        data.write(bytes([0xFF]))
        data.seek(0xDF, 0)
        data.write(bytes([0xFF]))
        data.seek(0xFB, 0)
        data.write(bytes([0xFF]))
        data.seek(0x117, 0)
        data.write(bytes([0xFF]))
        data.seek(0x133, 0)
        data.write(bytes([0xFF]))
        data.seek(0x210, 0)
        data.write(bytes([0xFF, 0xFF, 0xFF, 0xFF]))
        data.seek(0x53E, 0)
        data.write(bytes([0xFF, 0xFF]))
        data.seek(0x55A, 0)
        data.write(bytes([0xFF, 0xFF]))
        data.seek(0x576, 0)
        data.write(bytes([0xFF, 0xFF]))
        data.seek(0x506, 0)
        data.write(bytes([0xFF, 0xFF]))
        data.seek(0x522, 0)
        data.write(bytes([0xFF, 0xFF]))
        data.seek(0x96C, 0)
        data.write(bytes([0x4, 0x3]))
        stream.seek(0x67E7E0, 0)
        stream.write(zenc(data.getvalue()))
        return stream.getvalue()

    @staticmethod
    def patch_items(caller: APProcedurePatch, rom: bytes):
        stream = io.BytesIO(rom)
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        for i in range(len(level_locations)):
            level: Dict[str, Tuple] = json.loads(caller.get_file(f"level_{i}.json").decode("utf-8"))
            stream.seek(level_address[i], 0)
            stream, data = get_level_data(stream, level_size[i])
            for j, (location_name, item) in enumerate(level.items()):
                if "Mirror" in location_name:
                    continue
                if "Obelisk" in location_name:
                    try:
                        index = [index for index in range(len(data.objects)) if data.objects[index][8] == 0x26][0]
                        data.items += [
                            bytearray(data.objects[index][0:6]) + bytes(
                                item_dict[item[0]] if item[1] == options["player"] else [0x27, 0x4]) + bytes(
                                [0x0, 0x0, 0x0, 0x0])]
                        del data.objects[index]
                        data.item += 1
                    except Exception as e:
                        print(item[0])
                        print(e)
                    continue
                if item[1] is not options["player"]:
                    if "Chest" in location_name or (
                            "Barrel" in location_name and "Barrel of Gold" not in location_name):
                        data.chests[j - (len(data.items) + data.obelisk)][12] = 0x27
                        data.chests[j - (len(data.items) + data.obelisk)][13] = 0x4
                    else:
                        data.items[j - data.obelisk][6] = 0x27
                        data.items[j - data.obelisk][7] = 0x4
                else:
                    if "Obelisk" in items_by_id[item[0]].itemName:
                        data.objects += [bytearray(data.items[j - data.obelisk][0:6]) +
                                         bytearray([0x0, 0x0, 0x26, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0,
                                                    item[0] - 77780054,
                                                    0x3F, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0])]
                        del data.items[j - data.obelisk]
                        data.obelisk += 1
                    else:
                        if "Chest" in location_name or (
                                "Barrel" in location_name and "Barrel of Gold" not in location_name):
                            data.chests[j - (len(data.items) + data.obelisk)][12] = item_dict[item[0]][0]
                            data.chests[j - (len(data.items) + data.obelisk)][13] = item_dict[item[0]][1]
                        else:
                            data.items[j - data.obelisk][6] = item_dict[item[0]][0]
                            data.items[j - data.obelisk][7] = item_dict[item[0]][1]
            compressed = zenc(level_data_reformat(data))
            stream.seek(level_header[i] + 4, 0)
            stream.write(len(compressed).to_bytes(4, byteorder='big'))
            stream.seek(4, 1)
            write_pos = 0xFA1000 + (0x1500 * i)
            stream.write((write_pos - 0x636E0).to_bytes(4, byteorder='big'))
            stream.seek(write_pos, 0)
            stream.write(compressed)
        return stream.getvalue()


class GLProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Gauntlet Legends"
    hash = "9cb963e8b71f18568f78ec1af120362e"
    patch_file_ending = ".apgl"
    result_file_ending = ".z64"

    procedure = [
        ("patch_items", []),
        ("patch_counts", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def write_files(world: "GauntletLegendsWorld", patch: GLProcedurePatch) -> None:
    options_dict = {
        "seed": world.multiworld.seed,
        "player": world.player,
    }
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))
    for i, level in enumerate(level_locations.values()):
        locations: List[Location] = []
        for location in level:
            if location.name not in world.disabled_locations:
                locations += [world.get_location(location.name)]
        patch.write_file(f"level_{i}.json", json.dumps(locations_to_dict(locations)).encode("UTF-8"))


def locations_to_dict(locations: List[Location]) -> Dict[str, Tuple]:
    return {location.name: (location.item.code, location.item.player) for location in locations}


def zdec(data):
    """
    Decompresses zlib archives used in Midway titles.
    """
    decomp = zlib.decompressobj(-zlib.MAX_WBITS)
    output = bytearray()
    for i in range(0, len(data), 256):
        output.extend(decomp.decompress(data[i:i + 256]))
    output.extend(decomp.flush())
    return output


def zenc(data):
    """
    Headerless zlib encoding scheme used across games.
    Note you get much better compression routing through gzip
    and stripping off the header and CRC.
    """
    compress = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS)
    output = bytearray()
    for i in range(0, len(data), 256):
        output.extend(compress.compress(data[i:i + 256]))
    output.extend(compress.flush())
    return output


def get_level_data(stream: io.BytesIO, size: int) -> (io.BytesIO, LevelData):
    data = LevelData()
    data.stream = io.BytesIO(zdec(stream.read(size)))
    data.header = data.stream.read(0x5C)
    data.stream.seek(0)
    data.item_addr = int.from_bytes(data.stream.read(4), "big")
    data.spawner_addr = int.from_bytes(data.stream.read(4), "big")
    data.stream.seek(4, 1)
    data.obj_addr = int.from_bytes(data.stream.read(4), "big")
    data.end_addr = int.from_bytes(data.stream.read(4), "big")
    data.stream.seek(4, 1)
    data.chest_addr = int.from_bytes(data.stream.read(4), "big")
    data.end_addr2 = int.from_bytes(data.stream.read(4), "big")
    data.end_addr3 = int.from_bytes(data.stream.read(4), "big")
    data.stream.seek(data.item_addr)
    for i in range(data.stream.tell(), data.spawner_addr, 12):
        data.stream.seek(i)
        data.items += [bytearray(data.stream.read(12))]
    for i in range(data.stream.tell(), data.obj_addr, 16):
        data.stream.seek(i)
        data.spawners += [bytearray(data.stream.read(16))]
    for i in range(data.stream.tell(), data.chest_addr, 24):
        data.stream.seek(i)
        data.objects += [bytearray(data.stream.read(24))]
    for i in range(data.stream.tell(), data.end_addr, 16):
        data.stream.seek(i)
        data.chests += [bytearray(data.stream.read(16))]
    data.end = data.stream.read()
    return (stream, data)


def level_data_reformat(data: LevelData) -> bytes:
    stream = io.BytesIO()
    obelisk_offset = (24 * (data.obelisk - data.item))
    stream.write(int.to_bytes(0x5C, 4, "big"))
    stream.write(int.to_bytes(data.spawner_addr + (12 * (data.item - data.obelisk)), 4, "big"))
    stream.write(int.to_bytes(data.spawner_addr + (12 * (data.item - data.obelisk)), 4, "big"))
    stream.write(int.to_bytes(data.obj_addr + (12 * (data.item - data.obelisk)), 4, "big"))
    stream.write(int.to_bytes(data.end_addr + ((12 * (data.item - data.obelisk)) + obelisk_offset), 4, "big"))
    stream.write(int.to_bytes(data.end_addr + ((12 * (data.item - data.obelisk)) + obelisk_offset), 4, "big"))
    stream.write(int.to_bytes(data.chest_addr + ((12 * (data.item - data.obelisk)) + obelisk_offset), 4, "big"))
    stream.write(int.to_bytes(data.end_addr2 + ((12 * (data.item - data.obelisk)) + obelisk_offset), 4, "big"))
    stream.write(int.to_bytes(data.end_addr3 + ((12 * (data.item - data.obelisk)) + obelisk_offset), 4, "big"))
    stream.seek(1, 1)
    stream.write(bytes([len(data.items)]))
    stream.write(bytes([0x0, 0x0, 0x0]))
    stream.write(bytes([len(data.spawners)]))
    stream.write(bytes([0x0]))
    stream.write(bytes([len(data.objects)]))
    data.stream.seek(stream.tell())
    stream.write(data.stream.read(48))
    for item in data.items + data.spawners + data.objects + data.chests:
        stream.write(bytes(item))
    stream.write(data.end)
    return stream.getvalue()
