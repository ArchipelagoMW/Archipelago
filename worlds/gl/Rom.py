import traceback
import zlib
import io
import os

import Utils
from BaseClasses import ItemClassification
from settings import get_settings
from worlds.Files import APDeltaPatch
from .Arrays import level_locations, level_size, level_address, item_dict, level_header
from worlds.AutoWorld import World
from .Items import items_by_id, ItemData
from .Rules import name_convert


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
    items: list[bytearray]
    spawners: list[bytearray]
    objects: list[bytearray]
    chests: list[bytearray]
    end: bytes
    obelisk = 0
    item = 0

    def __init__(self):
        self.items = []
        self.spawners = []
        self.objects = []
        self.chests = []
        self.end = bytes()


class GLDeltaPatch(APDeltaPatch):
    game = "Gauntlet Legends"
    hash = "9cb963e8b71f18568f78ec1af120362e"
    patch_file_ending = ".apgl"
    result_file_ending = ".z64"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


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


class Rom:
    def __init__(self, world: "World"):
        try:
            self.random = world.multiworld.per_slot_randoms[world.player]
            self.stream = io.BytesIO(get_base_rom_as_bytes())
            self.world = world
            self.player = world.player
        except Exception as e:
            traceback.print_exc()

    def crc32(self, chunk_size=1024):
        self.stream.seek(0)
        crc32_checksum = 0
        while True:
            chunk = self.stream.read(chunk_size)
            if not chunk:
                break
            crc32_checksum = zlib.crc32(chunk, crc32_checksum)
        return format(crc32_checksum & 0xFFFFFFFF, 'x')

    def write_items(self):
        for i, level in enumerate(level_locations.values()):
            print(i)
            self.stream.seek(level_address[i], 0)
            data = self.get_level_data(level_size[i])
            print("Data Acquired")
            try:
                self.print_data(i, level, data)
            except Exception as e:
                print(e)
            for j, location in enumerate(level):
                location = self.world.multiworld.get_location(name_convert(location), self.player)
                print(location.item.name)
                if "Obelisk" in location.name:
                    print("Obelisk in item name")
                    try:
                        print(len(data.objects))
                        index = [index for index in range(len(data.objects)) if data.objects[index][8] == 0x26][0]
                        data.items += [
                            bytearray(data.objects[index][0:6]) + bytes(item_dict.get(location.item.code, [0x27, 0x4])) + bytes(
                                [0x0, 0x0, 0x0, 0x0])]
                        del data.objects[index]
                        data.item += 1
                    except Exception as e:
                        print(location.item.code)
                        print(traceback.print_exc())
                    continue
                if location.item.player is not self.player:
                    if "Chest" in location.name:
                        print(j - len(data.items))
                        data.chests[j - len(data.items)][12] = 0x27
                        data.chests[j - len(data.items)][13] = 0x4
                    else:
                        data.items[j - data.obelisk][6] = 0x27
                        data.items[j - data.obelisk][7] = 0x4
                else:
                    if "Obelisk" in location.item.name:
                        data.objects += [bytearray(data.items[j - data.obelisk][0:6]) +
                                         bytearray([0x0, 0x0, 0x26, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0,
                                                    location.item.code - 77780054,
                                                    0x3F, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0])]
                        del data.items[j - data.obelisk]
                        data.obelisk += 1
                    else:
                        if "Chest" in location.name:
                            print(j - len(data.items))
                            data.chests[j - len(data.items)][12] = item_dict[location.item.code][0]
                            data.chests[j - len(data.items)][13] = item_dict[location.item.code][1]
                        else:
                            data.items[j - data.obelisk][6] = item_dict[location.item.code][0]
                            data.items[j - data.obelisk][7] = item_dict[location.item.code][1]
            self.stream.seek(level_address[i], 0)
            print("Reformatting")
            compressed = zenc(self.level_data_reformat(data))
            self.stream.seek(level_header[i] + 4, 0)
            self.stream.write(len(compressed).to_bytes(4, byteorder='big'))
            self.stream.seek(4, 1)
            write_pos = 0xFA1000 + (0x1500 * i)
            self.stream.write((write_pos - 0x636E0).to_bytes(4, byteorder='big'))
            self.stream.seek(write_pos, 0)
            self.stream.write(compressed)

    def get_level_data(self, addr: int) -> LevelData:
        data = LevelData()
        print("Data Created")
        data.stream = io.BytesIO(zdec(self.stream.read(addr)))
        print("Stream Created")
        data.header = data.stream.read(0x5C)
        print("Header Read")
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
        print("Reading Items")
        print(format(data.item_addr, 'x'))
        for i in range(data.stream.tell(), data.spawner_addr, 12):
            data.stream.seek(i)
            data.items += [bytearray(data.stream.read(12))]
        print("Items Done")
        print(format(data.spawner_addr, 'x'))
        for i in range(data.stream.tell(), data.obj_addr, 16):
            data.stream.seek(i)
            data.spawners += [bytearray(data.stream.read(16))]
        print("Spawners Done")
        print(format(data.obj_addr, 'x'))
        for i in range(data.stream.tell(), data.chest_addr, 24):
            data.stream.seek(i)
            data.objects += [bytearray(data.stream.read(24))]
        print("Objects Done")
        print(format(data.chest_addr, 'x'))
        for i in range(data.stream.tell(), data.end_addr, 16):
            data.stream.seek(i)
            data.chests += [bytearray(data.stream.read(16))]
        print("Chests Done")
        data.end = data.stream.read()
        print("Read End")
        return data

    def print_data(self, i: int, level, data: LevelData) -> None:
        name = level[0].name.find('-')
        name = level[0].name[:name - 1]
        try:
            with open(f"C:\\Users\\james\\gl_docs\\{i}_names.txt", "w") as file:
                    for _i, chests in enumerate(data.chests):
                        file.write(f"LocationData(\"{name} Chest - {items_by_id.get(next((key for key, value in item_dict.items() if value == [chests[12], chests[13]]), -1), ItemData(0, 'Unknown', ItemClassification.filler)).itemName}\", 8887{i if i > 10 else 30 + i}{_i}, {chests[11]}),\n")
        except Exception as e:
            print(traceback.print_exception(e))

    def level_data_reformat(self, data: LevelData) -> bytes:
        stream = io.BytesIO()
        obelisk_offset = (24 * (data.obelisk if data.obelisk > 0 else -data.item))
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

    def patch_counts(self):
        self.stream.seek(0x67E7E0)
        data = io.BytesIO(zdec(self.stream.read(0x380)))
        data.seek(0x1B, 0)
        data.write(bytes([0xFF]))
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
        data.seek(0x53E, 0)
        data.write(bytes([0xFF, 0xFF]))
        data.seek(0x96C, 0)
        data.write(bytes([0x4, 0x3]))
        self.stream.seek(0x67E7E0, 0)
        self.stream.write(zenc(data.getvalue()))

    def close(self, path):
        print("closing")
        output_path = os.path.join(path,
                                   f"AP_{self.world.multiworld.seed_name}_P{self.player}_{self.world.multiworld.player_name[self.player]}.z64")
        with open(output_path, 'wb') as outfile:
            outfile.write(self.stream.getvalue())
        patch = GLDeltaPatch(os.path.splitext(output_path)[0] + ".apgl", player=self.player,
                             player_name=self.world.multiworld.player_name[self.player], patched_path=output_path)
        patch.write()
        os.unlink(output_path)
        self.stream.close()
