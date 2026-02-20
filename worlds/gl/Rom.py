import io
import json
import os
import pkgutil
import traceback
import typing
import zlib
from random import Random

import bsdiff4

import Utils
from BaseClasses import Location, ItemClassification

from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin

from .Data import level_address, level_header, level_locations, level_size, boss_location_offsets, spawner_trap_ids
from .Items import ItemData, items_by_id
from .Locations import locationName_to_data, GLLocation

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld

TABLE_START_OFFSET = 0x12E0
EXPANDED_GAME_ROM_OFFSET = 0x1000000  # 16MB mark


def create_spawner_from_item(item_data: bytearray, spawner_rom_id: int, difficulty: int) -> bytearray:
    spawner = bytearray(16)
    spawner[0:6] = item_data[0:6]
    spawner[6:8] = (0).to_bytes(2, "big")
    spawner[8:12] = spawner_rom_id.to_bytes(4, "big")
    spawner[12:14] = (0x0003).to_bytes(2, "big")
    spawner[14] = difficulty
    spawner[15] = 0x00
    return spawner


def create_spawner_from_chest(chest_data: bytearray, spawner_rom_id: int, difficulty: int) -> bytearray:
    spawner = bytearray(16)
    spawner[0:6] = chest_data[0:6]
    spawner[6:8] = chest_data[6:8]
    spawner[8:12] = spawner_rom_id.to_bytes(4, "big")
    spawner[12:14] = (0x0003).to_bytes(2, "big")
    spawner[14] = difficulty
    spawner[15] = 0x00
    return spawner


def be32(b: bytes) -> int:
    return int.from_bytes(b, "big")


def write_be32(buf: bytearray, off: int, val: int):
    buf[off:off + 4] = (val & 0xFFFFFFFF).to_bytes(4, "big")


def ensure_len(buf: bytearray, size: int, fill: int = 0):
    if len(buf) < size:
        buf.extend(bytes([fill]) * (size - len(buf)))


def n64_crc(rom: bytes, cic: int = 6102) -> tuple[int, int]:
    """Calculate N64 CRC checksums."""
    if cic in (6101, 6102):
        seed = 0xF8CA4DDC
    elif cic == 6103:
        seed = 0xA3886759
    elif cic == 6105:
        seed = 0xDF26F436
    elif cic == 6106:
        seed = 0x1FEA617A
    else:
        raise ValueError("Unsupported CIC")

    t1 = t2 = t3 = t4 = t5 = t6 = seed

    for i in range(0x1000, 0x101000, 4):
        d = int.from_bytes(rom[i:i + 4], "big")

        if (t6 + d) & 0xFFFFFFFF < t6:
            t4 = (t4 + 1) & 0xFFFFFFFF

        t6 = (t6 + d) & 0xFFFFFFFF
        t3 ^= d

        r = ((d << (d & 31)) | (d >> (32 - (d & 31)))) & 0xFFFFFFFF
        t5 = (t5 + r) & 0xFFFFFFFF

        if t2 > d:
            t2 ^= r
        else:
            t2 ^= t6 ^ d

        if cic == 6105:
            extra = int.from_bytes(rom[0x0750 + (i & 0xFF):0x0754 + (i & 0xFF)], "big")
            t1 = (t1 + (extra ^ d)) & 0xFFFFFFFF
        else:
            t1 = (t1 + (t5 ^ d)) & 0xFFFFFFFF

    if cic == 6103:
        crc1 = (t6 ^ t4) & 0xFFFFFFFF
        crc2 = (t5 ^ t3) & 0xFFFFFFFF
    elif cic == 6106:
        crc1 = ((t6 * t4) + t3) & 0xFFFFFFFF
        crc2 = ((t5 * t2) + t1) & 0xFFFFFFFF
    else:
        crc1 = (t6 ^ t4 ^ t3) & 0xFFFFFFFF
        crc2 = (t5 ^ t2 ^ t1) & 0xFFFFFFFF

    return crc1, crc2


def get_base_rom_as_bytes() -> bytes:
    """
    Read the base ROM file and verify its MD5 hash.
    Raises an exception if the ROM doesn't match the expected hash.
    """
    try:
        from . import GauntletLegendsWorld
        GauntletLegendsWorld.settings.rom_file.validate(GauntletLegendsWorld.settings.rom_file)
        with open(GauntletLegendsWorld.settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
    except Exception:
        traceback.print_exc()
        raise Exception('Failed to read ROM file. Check file path and permissions.')
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
    items: list[bytearray]
    spawners: list[bytearray]
    objects: list[bytearray]
    chests: list[bytearray]
    end: bytes
    items_replaced_by_obelisks: int = 0
    chests_replaced_by_obelisks: int = 0
    chests_replaced_by_items: int = 0
    obelisks_replaced_by_items: int = 0
    obelisks_kept: int = 0
    items_replaced_by_spawners: int = 0
    chests_replaced_by_spawners: int = 0

    def __init__(self):
        self.items = []
        self.spawners = []
        self.objects = []
        self.chests = []
        self.end = b""


class GLPatchExtension(APPatchExtension):
    game = "Gauntlet Legends"

    # Patched ROM requires updated CRC values.
    @staticmethod
    def finalize_crc(caller: APProcedurePatch, rom: bytes) -> bytes:
        options = json.loads(caller.get_file("options.json").decode("utf-8"))
        rom = bytearray(rom)

        SEED_ROM_OFFSET = 0xFFFFF0
        SEED_LEN = 16

        seed = options["seed_name"].encode("utf-8")[:SEED_LEN]
        rom[SEED_ROM_OFFSET:SEED_ROM_OFFSET + SEED_LEN] = seed.ljust(SEED_LEN, b"\x00")

        rom = bytearray(rom)
        crc1, crc2 = n64_crc(rom, cic=6102)
        rom[0x10:0x14] = crc1.to_bytes(4, "big")
        rom[0x14:0x18] = crc2.to_bytes(4, "big")
        return bytes(rom)


    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str) -> bytes:
        return bsdiff4.patch(rom, pkgutil.get_data(__name__, f"data/basepatch.bsdiff4"))

    # Decompress all levels, place all items in the levels.
    @staticmethod
    def patch_items(caller: APProcedurePatch, rom: bytes):
        stream = io.BytesIO(rom)
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        local_random = Random(options["seed"])
        player = options["player"]

        for i in range(len(level_locations)):
            level: dict[str, tuple] = json.loads(caller.get_file(f"level_{i}.json").decode("utf-8"))
            level_address_ = level_address[i]
            if level_address_ == 0:
                continue
            stream.seek(level_address_, 0)
            stream, data = get_level_data(stream, level_size[i], i)

            # Track deletions for index calculations
            items_deleted = 0
            chests_deleted = 0
            chests_seen = 0

            for j, (location_name, item) in enumerate(level.items()):
                if item[0] == 0:
                    continue

                item_data = items_by_id.get(item[0], ItemData())
                rom_id = item_data.rom_id
                if rom_id == 0x0302:
                    rom_id = local_random.choices(
                        [0x0300, 0x0301, 0x0302, 0x0303, 0x0304],
                        weights=[10, 20, 40, 20, 10]
                    )[0]

                if "Mirror" in location_name:
                    continue

                # Handle obelisk locations
                if "Obelisk" in location_name:
                    if "Obelisk" not in item_data.item_name:
                        # Non-obelisk item at obelisk location - convert obelisk to item
                        try:
                            index = next(idx for idx in range(len(data.objects)) if data.objects[idx][8] == 0x26)
                            data.items.append(
                                bytearray(data.objects[index][0:6])
                                + (rom_id.to_bytes(2) if item[1] == player else bytes([0x27, 0x1C]))
                                + bytes([0x0, 0x0, 0x0, 0x0])
                            )
                            del data.objects[index]
                            data.obelisks_replaced_by_items += 1
                        except (StopIteration, Exception):
                            pass
                    else:
                        # Obelisk item at obelisk location
                        try:
                            index = next(idx for idx in range(len(data.objects)) if data.objects[idx][8] == 0x26)
                            if item[1] == player:
                                data.objects[index][15] = item[0] - 77780054
                                data.obelisks_kept += 1
                            else:
                                data.items.append(
                                    bytearray(data.objects[index][0:6])
                                    + bytes([0x27, 0x1C, 0x0, 0x0, 0x0, 0x0])
                                )
                                del data.objects[index]
                                data.obelisks_replaced_by_items += 1
                        except (StopIteration, Exception):
                            pass
                    continue

                # Calculate indices
                is_chest = chest_barrel(location_name)
                item_index = j - data.obelisks_kept - items_deleted
                if is_chest:
                    chest_index = chests_seen - chests_deleted
                    chests_seen += 1

                # Handle spawner trap items (local player only)
                if item[1] == player and item[0] in spawner_trap_ids:
                    difficulty = locationName_to_data[location_name].difficulty
                    spawner_rom_id = items_by_id[item[0]].rom_id
                    if is_chest:
                        data.spawners.append(create_spawner_from_chest(data.chests[chest_index], spawner_rom_id, difficulty))
                        del data.chests[chest_index]
                        chests_deleted += 1
                        data.chests_replaced_by_spawners += 1
                    else:
                        data.spawners.append(create_spawner_from_item(data.items[item_index], spawner_rom_id, difficulty))
                        del data.items[item_index]
                        items_deleted += 1
                        data.items_replaced_by_spawners += 1
                    continue

                # Handle non-local player items
                if item[1] != player:
                    if is_chest:
                        data.chests[chest_index][12:14] = [0x27, 0x1C]
                        if "Chest" in location_name:
                            data.chests[chest_index][9] = 0x1
                    else:
                        data.items[item_index][6:8] = [0x27, 0x1C]
                    continue

                # Handle local player items
                if "Obelisk" in items_by_id[item[0]].item_name:
                    # Convert item/chest to obelisk
                    if is_chest:
                        slice_ = bytearray(data.chests[chest_index][0:6])
                        del data.chests[chest_index]
                        chests_deleted += 1
                        data.chests_replaced_by_obelisks += 1
                    else:
                        slice_ = bytearray(data.items[item_index][0:6])
                        del data.items[item_index]
                        items_deleted += 1
                        data.items_replaced_by_obelisks += 1
                    data.objects.append(
                        slice_ + bytearray([
                            0x0, 0x0, 0x26, 0x1, 0x0,
                            locationName_to_data[location_name].difficulty,
                            0x0, 0x0, 0x0, item[0] - 77780054,
                            0x3F, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
                        ])
                    )
                elif item_data.progression in (ItemClassification.useful, ItemClassification.progression) and is_chest:
                    # Convert chest to item for useful/progression items
                    chest = data.chests[chest_index]
                    data.items.append(
                        bytearray(chest[0:6])
                        + rom_id.to_bytes(2)
                        + bytes([chest[11], 0x0, 0x0, 0x0])
                    )
                    del data.chests[chest_index]
                    chests_deleted += 1
                    data.chests_replaced_by_items += 1
                else:
                    # Regular item placement
                    if is_chest:
                        data.chests[chest_index][12:14] = rom_id.to_bytes(2)
                        if "Chest" in location_name:
                            data.chests[chest_index][9] = 0x2
                    else:
                        data.items[item_index][6:8] = item_data.rom_id.to_bytes(2)

            # Write level data
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

    @staticmethod
    def patch_bins(caller: APProcedurePatch, rom: bytes) -> bytes:
        boss_items_data = json.loads(caller.get_file("boss_items.json").decode("UTF-8"))
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        local_random = Random(options["seed"])

        boss_entry_offset = TABLE_START_OFFSET + (2 * 0x30)

        rom = bytearray(rom)

        boss_rom_offset = be32(rom[boss_entry_offset + 0x10:boss_entry_offset + 0x14])
        boss_comp_size = be32(rom[boss_entry_offset + 0x14:boss_entry_offset + 0x18])

        boss_compressed = bytes(rom[boss_rom_offset:boss_rom_offset + boss_comp_size])
        boss_decompressed = bytearray(zdec(boss_compressed))

        FILLER_ROM_ID = 0x271C

        for location_name, item_data in boss_items_data.items():
            if location_name not in boss_location_offsets:
                continue

            item_code, item_player = item_data
            if not item_code:
                continue

            if item_player != options["player"]:
                rom_id = FILLER_ROM_ID
            else:
                rom_id = items_by_id[item_code].rom_id

            if rom_id == 0x0302:
                rom_id = local_random.choices([0x0300, 0x0301, 0x0302, 0x0303, 0x0304], weights=[10, 20, 40, 20, 10])[0]

            hi_byte = (rom_id >> 8) & 0xFF
            lo_byte = rom_id & 0xFF

            offset = boss_location_offsets[location_name]
            boss_decompressed[offset:offset + 2] = hi_byte.to_bytes(2, "big")
            boss_decompressed[offset + 2:offset + 4] = lo_byte.to_bytes(2, "big")

        boss_recompressed = zenc(boss_decompressed)
        new_boss_comp_size = len(boss_recompressed)

        if new_boss_comp_size > boss_comp_size:
            new_boss_rom_offset = EXPANDED_GAME_ROM_OFFSET + 0x100000
            new_boss_end = new_boss_rom_offset + new_boss_comp_size
            ensure_len(rom, new_boss_end, fill=0xFF)
            rom[new_boss_rom_offset:new_boss_end] = boss_recompressed
            write_be32(rom, boss_entry_offset + 0x10, new_boss_rom_offset)
            write_be32(rom, boss_entry_offset + 0x14, new_boss_comp_size)
        else:
            rom[boss_rom_offset:boss_rom_offset + new_boss_comp_size] = boss_recompressed
            write_be32(rom, boss_entry_offset + 0x14, new_boss_comp_size)
            if new_boss_comp_size < boss_comp_size:
                leftover_start = boss_rom_offset + new_boss_comp_size
                leftover_end = boss_rom_offset + boss_comp_size
                rom[leftover_start:leftover_end] = bytes(leftover_end - leftover_start)

        # Write portals option
        rom[0xFFFFE0] = options["portals"]
        rom[0xFFFFE1] = options["instant_max"]
        rom[0xFFFFE2] = options["max"]
        rom[0xFFFFE4] = options["keys"]
        rom[0xFFFFE5] = options["speed"]
        characters = options["characters"].copy()
        characters.reverse()
        rom[0xFFFFE8:0xFFFFEC] = characters
        return bytes(rom)


class GLProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Gauntlet Legends"
    hash = "9cb963e8b71f18568f78ec1af120362e"
    patch_file_ending = ".apgl"
    result_file_ending = ".z64"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("patch_bins", []),
        ("patch_items", []),
        ("finalize_crc", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


# Write data on all placed items into json files.
# Also save options
def write_files(world: "GauntletLegendsWorld", patch: GLProcedurePatch) -> None:
    options_dict = {
        "seed": world.multiworld.seed,
        "seed_name": world.multiworld.seed_name,
        "player": world.player,
        "portals": world.options.portals.value,
        "instant_max": world.options.instant_max.value,
        "max": world.options.max_difficulty.value,
        "keys": world.options.infinite_keys.value,
        "speed": world.options.permanent_speed.value,
        "characters": [world.options.unlock_character_one.value, world.options.unlock_character_two.value,
                       world.options.unlock_character_three.value, world.options.unlock_character_four.value]
    }
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))
    patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff4"))

    # Write level files
    for i, level in enumerate(level_locations.values()):
        locations: list[Location] = []
        for location in level:
            if location.name in world.disabled_locations:
                locations += [GLLocation(world.player, location.name, location.id)]
            else:
                locations += [world.get_location(location.name)]
        patch.write_file(f"level_{i}.json", json.dumps(locations_to_dict(locations)).encode("UTF-8"))

    # Write boss items file
    boss_location_names = [
        "Dragon's Lair - Dragon Mirror Shard",
        "Yeti's Cavern - Yeti Mirror Shard",
        "Chimera's Keep - Chimera Mirror Shard",
        "Vat of the Plague Fiend - Plague Fiend Mirror Shard",
        "Altar of Skorne - Skorne's Mask",
        "Altar of Skorne - Skorne's Horns",
        "Altar of Skorne - Skorne's Left Gauntlet",
        "Altar of Skorne - Skorne's Right Gauntlet"
    ]

    boss_locations: list[Location] = []
    for location_name in boss_location_names:
        if location_name in world.disabled_locations:
            # Get location ID from locationName_to_data
            location_data = locationName_to_data.get(location_name)
            if location_data:
                boss_locations += [GLLocation(world.player, location_name, location_data.id)]
        else:
            boss_locations += [world.get_location(location_name)]

    patch.write_file("boss_items.json", json.dumps(locations_to_dict(boss_locations)).encode("UTF-8"))


def locations_to_dict(locations: list[Location]) -> dict[str, tuple]:
    return {location.name: (location.item.code, location.item.player) if location.item is not None else (0, 0) for
            location in locations}


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
    data.stream.write(bytes([0xFB, 0x68, 0x0, 0x82]))
    return data


# Zlib decompression with wbits set to -15
def zdec(data):
    decomp = zlib.decompressobj(-zlib.MAX_WBITS)
    output = bytearray()
    for i in range(0, len(data), 256):
        output.extend(decomp.decompress(data[i: i + 256]))
    output.extend(decomp.flush())
    return output


# Zlib compression with compression set to max and wbits set to -15
def zenc(data):
    compress = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS)
    output = bytearray()
    for i in range(0, len(data), 256):
        output.extend(compress.compress(data[i: i + 256]))
    output.extend(compress.flush())
    return output


# Create a LevelData object from raw decompressed bytes of a level
def get_level_data(stream: io.BytesIO, size: int, level: int = 0) -> tuple[io.BytesIO, LevelData]:
    data = LevelData()
    data.stream = io.BytesIO(zdec(stream.read(size)))
    if level == 17:
        data = patch_docks(data)
    if level == 18:
        data = patch_camp(data)
    if level == 24:
        data = patch_trenches(data)
    data.header = bytearray(data.stream.read(0x5C))
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
    obelisk_offset = 24 * (
            data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks - data.obelisks_replaced_by_items)
    item_offset = 12 * (
            data.chests_replaced_by_items + data.obelisks_replaced_by_items - data.items_replaced_by_obelisks - data.items_replaced_by_spawners)
    chest_offset = 16 * (
                data.chests_replaced_by_obelisks + data.chests_replaced_by_items + data.chests_replaced_by_spawners)
    spawner_offset = 16 * (data.items_replaced_by_spawners + data.chests_replaced_by_spawners)

    stream.write(int.to_bytes(0x5C, 4, "big"))
    stream.write(int.to_bytes(data.spawner_addr + item_offset, 4, "big"))
    stream.write(int.to_bytes(data.spawner_addr + item_offset, 4, "big"))
    stream.write(int.to_bytes(data.obj_addr + item_offset + spawner_offset, 4, "big"))
    stream.write(int.to_bytes(data.end_addr + item_offset + spawner_offset + obelisk_offset - chest_offset, 4, "big"))
    stream.write(
        int.to_bytes(data.portal_addr + item_offset + spawner_offset + obelisk_offset - chest_offset, 4, "big"))
    stream.write(int.to_bytes(data.chest_addr + item_offset + spawner_offset + obelisk_offset, 4, "big"))
    stream.write(int.to_bytes(data.end_addr2 + item_offset + spawner_offset + obelisk_offset - chest_offset, 4, "big"))
    stream.write(int.to_bytes(data.end_addr3 + item_offset + spawner_offset + obelisk_offset - chest_offset, 4, "big"))
    # Counts are 2 bytes each, big-endian
    stream.write(len(data.items).to_bytes(2, "big"))
    stream.write(bytes([0x0, 0x0]))
    stream.write(len(data.spawners).to_bytes(2, "big"))
    stream.write(len(data.objects).to_bytes(2, "big"))
    data.stream.seek(stream.tell())
    temp = bytearray(data.stream.read(48))
    temp[7] = len(data.chests)
    stream.write(temp)
    for item in data.items + data.spawners + data.objects + data.chests:
        stream.write(bytes(item))
    stream.write(data.end)
    return stream.getvalue()


def chest_barrel(name: str):
    return "Chest" in name or ("Barrel" in name and "Barrel of Gold" not in name)
