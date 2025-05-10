import io
import json
import os
import traceback
import typing
import zlib
from typing import Dict, List, Tuple

import Utils
from BaseClasses import Location, ItemClassification
from settings import get_settings

from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin

from .Arrays import item_dict, level_address, level_header, level_locations, level_size
from .Items import items_by_id, ItemData
from .Locations import location_data, GLLocation

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld


def get_base_rom_as_bytes() -> bytes:
    try:
        with open(get_settings().gl_options.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
    except Exception:
        traceback.print_exc()

    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


# Contains header info and raw data for level item positions and rotations.
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
    portal_addr: int
    items: List[bytearray]
    spawners: List[bytearray]
    objects: List[bytearray]
    chests: List[bytearray]
    end: bytes
    items_replaced_by_obelisks: int = 0
    chests_replaced_by_obelisks: int = 0
    chests_replaced_by_items: int = 0
    obelisks_replaced_by_items: int = 0

    def __init__(self):
        self.items = []
        self.spawners = []
        self.objects = []
        self.chests = []
        self.end = b""


class GLPatchExtension(APPatchExtension):
    game = "Gauntlet Legends"

    # Patch max item stack values
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
        data.seek(0x212, 0)
        data.write(bytes([0xFF, 0xFF]))
        for i in range(25):
            data.seek(0x1A, 1)
            data.write(bytes([0xFF, 0xFF]))
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
        stream.seek(0x67E7E0, 0)
        stream.write(zenc(data.getvalue()))
        return stream.getvalue()

    # Decompress all levels, place all items in the levels.
    @staticmethod
    def patch_items(caller: APProcedurePatch, rom: bytes):
        stream = io.BytesIO(rom)
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        for i in range(len(level_locations)):
            level: Dict[str, Tuple] = json.loads(caller.get_file(f"level_{i}.json").decode("utf-8"))
            stream.seek(level_address[i], 0)
            stream, data = get_level_data(stream, level_size[i], i)
            for j, (location_name, item) in enumerate(level.items()):
                if item[0] == 0:
                    continue
                if "Mirror" in location_name:
                    continue
                if "Obelisk" in location_name and "Obelisk" not in items_by_id.get(item[0], ItemData(0, "", ItemClassification.filler)).item_name:
                    try:
                        index = [index for index in range(len(data.objects)) if data.objects[index][8] == 0x26][0]
                        data.items += [
                            bytearray(data.objects[index][0:6])
                            + bytes(item_dict[item[0]] if item[1] == options["player"] else [0x27, 0x4])
                            + bytes([0x0, 0x0, 0x0, 0x0]),
                        ]
                        del data.objects[index]
                        data.obelisks_replaced_by_items += 1
                    except Exception as e:
                        print(item[0])
                        print(e)
                    continue
                if item[1] is not options["player"]:
                    if "Chest" in location_name or (
                        "Barrel" in location_name and "Barrel of Gold" not in location_name
                    ):
                        data.chests[j - (len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][12:14] = [0x27, 0x4]
                        if "Chest" in location_name:
                            data.chests[j - (len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][9] = 0x1
                    else:
                        data.items[j - data.items_replaced_by_obelisks][6:8] = [0x27, 0x4]
                else:
                    if "Obelisk" in items_by_id[item[0]].item_name and "Obelisk" not in location_name:
                        if chest_barrel(location_name):
                            slice_ = bytearray(data.chests[j - (len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][0:6])
                        else:
                            slice_ = bytearray(data.items[j - data.items_replaced_by_obelisks][0:6])
                        data.objects += [
                            slice_
                            + bytearray(
                                [
                                    0x0, 0x0, 0x26, 0x1, 0x0,
                                    location_data[location_name].difficulty,
                                    0x0, 0x0, 0x0,
                                    item[0] - 77780054,
                                    0x3F, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
                                ],
                            ),
                        ]
                        if chest_barrel(location_name):
                            del data.chests[j - (len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)]
                            data.chests_replaced_by_obelisks += 1
                        else:
                            del data.items[j - data.items_replaced_by_obelisks]
                            data.items_replaced_by_obelisks += 1
                    elif (items_by_id[item[0]].progression == ItemClassification.useful or items_by_id[item[0]].progression == ItemClassification.progression) and chest_barrel(location_name):
                        chest_index = j - (
                                    len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)
                        chest = data.chests[chest_index]
                        slice_ = bytearray(chest[0:6])
                        data.items += [
                            slice_
                            + bytes(item_dict[item[0]] if item[1] == options["player"] else [0x27, 0x4])
                            + bytes([chest[11], 0x0, 0x0, 0x0]),
                        ]
                        del data.chests[chest_index]
                        data.chests_replaced_by_items += 1
                    else:
                        if chest_barrel(location_name):
                            data.chests[j - (len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][12:14] = item_dict[item[0]]
                            if "Chest" in location_name:
                                data.chests[j - (len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][9] = 0x2
                        else:
                            data.items[j - data.items_replaced_by_obelisks][6:8] = item_dict[item[0]]
            uncompressed = level_data_reformat(data)
            compressed = zenc(uncompressed)
            stream.seek(level_header[i] + 4, 0)
            stream.write(len(compressed).to_bytes(4, byteorder="big"))
            stream.write(len(uncompressed).to_bytes(4, byteorder="big"))
            write_pos = 0xFA1000 + (0x1500 * i)
            stream.write((write_pos - 0x636E0).to_bytes(4, byteorder="big"))
            stream.seek(write_pos, 0)
            stream.write(compressed)
        return stream.getvalue()


class GLProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Gauntlet Legends"
    hash = "9cb963e8b71f18568f78ec1af120362e"
    patch_file_ending = ".apgl"
    result_file_ending = ".z64"

    procedure = [("patch_items", []), ("patch_counts", [])]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


# Write data on all placed items into json files.
# Also save options
def write_files(world: "GauntletLegendsWorld", patch: GLProcedurePatch) -> None:
    options_dict = {
        "seed": world.multiworld.seed,
        "player": world.player,
    }
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))
    for i, level in enumerate(level_locations.values()):
        locations: List[Location] = []
        for location in level:
            if location.name in world.disabled_locations:
                locations += [GLLocation(world.player, location.name, location.id)]
            else:
                locations += [world.get_location(location.name)]
        patch.write_file(f"level_{i}.json", json.dumps(locations_to_dict(locations)).encode("UTF-8"))


def locations_to_dict(locations: List[Location]) -> Dict[str, Tuple]:
    return {location.name: (location.item.code, location.item.player) if location.item is not None else (0, 0) for location in locations}


def patch_docks(data: LevelData) -> LevelData:
    data.stream.seek(0x19AC, 0)
    data.stream.write(bytes([0x3, 0x20, 0x0, 0x18, 0x1, 0x7C]))
    data.stream.seek(0x74, 0)
    data.stream.write(bytes([0x3, 0x0, 0x0, 0x1A, 0x1, 0x8]))
    return data


def patch_camp(data: LevelData) -> LevelData:
    data.stream.seek(0x1B74, 0)
    data.stream.write(bytes([0xFE, 0xE9, 0x0, 0x3B, 0xFF, 0xDC, 0x0, 0x10]))
    data.stream.seek(0x1B64, 0)
    data.stream.write(bytes([0xFE, 0x84, 0x0, 0x3D, 0xFF, 0xE0, 0xFF, 0xF0]))
    return data

def patch_trenches(data: LevelData) -> LevelData:
    data.stream.seek(0xD4, 0)
    data.stream.write(bytes([0xFB, 0x29, 0x0, 0x82]))
    return data


# Zlib decompression with wbits set to -15
def zdec(data):
    decomp = zlib.decompressobj(-zlib.MAX_WBITS)
    output = bytearray()
    for i in range(0, len(data), 256):
        output.extend(decomp.decompress(data[i : i + 256]))
    output.extend(decomp.flush())
    return output


# Zlib compression with compression set to max and wbits set to -15
def zenc(data):
    compress = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS)
    output = bytearray()
    for i in range(0, len(data), 256):
        output.extend(compress.compress(data[i : i + 256]))
    output.extend(compress.flush())
    return output


# Create a LevelData object from raw decompressed bytes of a level
def get_level_data(stream: io.BytesIO, size: int, level=0) -> (io.BytesIO, LevelData):
    data = LevelData()
    data.stream = io.BytesIO(zdec(stream.read(size)))
    if level == 17:
        data = patch_docks(data)
    if level == 18:
        data = patch_camp(data)
    if level == 23:
        data = patch_trenches(data)
    data.header = data.stream.read(0x5C)
    data.stream.seek(0)
    data.item_addr = int.from_bytes(data.stream.read(4), "big")
    data.spawner_addr = int.from_bytes(data.stream.read(4), "big")
    data.stream.seek(4, 1)
    data.obj_addr = int.from_bytes(data.stream.read(4), "big")
    data.end_addr = int.from_bytes(data.stream.read(4), "big")
    data.portal_addr = int.from_bytes(data.stream.read(4), "big")
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
    return stream, data


# Format a LevelData object back into a bytes object
# Format is header, items, spawners, objects, barrels/chests, then traps.
def level_data_reformat(data: LevelData) -> bytes:
    stream = io.BytesIO()
    obelisk_offset = 24 * (data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks - data.obelisks_replaced_by_items)
    item_offset = 12 * (data.chests_replaced_by_items + data.obelisks_replaced_by_items - data.items_replaced_by_obelisks)
    chest_offset = 16 * (data.chests_replaced_by_obelisks + data.chests_replaced_by_items)
    stream.write(int.to_bytes(0x5C, 4, "big"))
    stream.write(int.to_bytes(data.spawner_addr + item_offset, 4, "big"))
    stream.write(int.to_bytes(data.spawner_addr + item_offset, 4, "big"))
    stream.write(int.to_bytes(data.obj_addr + item_offset, 4, "big"))
    stream.write(int.to_bytes(data.end_addr + item_offset + obelisk_offset - chest_offset, 4, "big"))
    stream.write(int.to_bytes(data.portal_addr + item_offset + obelisk_offset - chest_offset, 4, "big"))
    stream.write(int.to_bytes(data.chest_addr + item_offset + obelisk_offset, 4, "big"))
    stream.write(int.to_bytes(data.end_addr2 + item_offset + obelisk_offset - chest_offset, 4, "big"))
    stream.write(int.to_bytes(data.end_addr3 + item_offset + obelisk_offset - chest_offset, 4, "big"))
    stream.seek(1, 1)
    stream.write(bytes([len(data.items)]))
    stream.write(bytes([0x0, 0x0, 0x0]))
    stream.write(bytes([len(data.spawners)]))
    stream.write(bytes([0x0]))
    stream.write(bytes([len(data.objects)]))
    data.stream.seek(stream.tell())
    temp = bytearray(data.stream.read(48))
    temp[7] = len(data.chests)
    stream.write(temp)
    for item in data.items + data.spawners + data.objects + data.chests:
        stream.write(bytes(item))
    stream.write(data.end)
    return stream.getvalue()

def chest_barrel(name: str):
    return ("Chest" in name or ("Barrel" in name and "Barrel of Gold" not in name))
