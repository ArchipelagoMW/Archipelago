import io
import json
import os
import subprocess
import shutil
import traceback
import typing
import zlib

import Utils
from BaseClasses import Location, ItemClassification

from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin

from .Data import level_address, level_header, level_locations, level_size, boss_location_offsets
from .Items import ItemData, items_by_id
from .Locations import locationName_to_data, GLLocation

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld

# ============================================================
# Repack constants
# ============================================================
FILE_COUNT_OFFSET = 0x12C4
TABLE_START_OFFSET = 0x12E0
CUSTOM_ENTRY_OFFSET = TABLE_START_OFFSET + (6 * 0x30)  # 0x1400
NEW_CUSTOM_ROM_OFFSET = 0xFFB000
EXPANDED_GAME_ROM_OFFSET = 0x1000000  # 16MB mark


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


def next_cart_size(size: int) -> int:
    """Round up to next valid N64 cart size."""
    cart_sizes = [0x00800000, 0x01000000, 0x02000000, 0x04000000]
    for s in cart_sizes:
        if size <= s:
            return s
    raise RuntimeError(f"ROM too large: 0x{size:X}")


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

    def __init__(self):
        self.items = []
        self.spawners = []
        self.objects = []
        self.chests = []
        self.end = b""


class GLPatchExtension(APPatchExtension):
    game = "Gauntlet Legends"

    @staticmethod
    def patch_repack(caller: APProcedurePatch, rom: bytes) -> bytes:
        """Apply mod code patches: game.bin patches, loader hook, and custom code injection."""
        import tempfile
        import pkgutil

        # Get the package for resource loading
        from . import __name__ as package_name

        rom = bytearray(rom)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_rom_path = os.path.join(temp_dir, "temp_working.z64")
            game_bin_path = os.path.join(temp_dir, "game.bin")
            custom_bin_path = os.path.join(temp_dir, "mycode.bin")

            # Extract asm files from package to temp directory
            asm_files = ["armips.exe", "CustomCode.asm", "GameBin.asm", "LoaderHook.asm"]
            for asm_file in asm_files:
                try:
                    data = pkgutil.get_data(package_name, f"asm/{asm_file}")
                    if data:
                        with open(os.path.join(temp_dir, asm_file), "wb") as f:
                            f.write(data)
                except FileNotFoundError:
                    pass  # Optional files may not exist

            armips_exe = os.path.join(temp_dir, "armips.exe")
            if not os.path.exists(armips_exe):
                # Try system path
                armips_exe = shutil.which("armips")
                if armips_exe is None:
                    raise FileNotFoundError("armips executable not found in asm folder or system PATH")

            custom_asm_path = os.path.join(temp_dir, "CustomCode.asm")
            game_bin_asm_path = os.path.join(temp_dir, "GameBin.asm")
            loader_hook_asm_path = os.path.join(temp_dir, "LoaderHook.asm")

            # Write ROM to temp file for armips
            with open(temp_rom_path, "wb") as f:
                f.write(rom)

            # ============================================================
            # PART 1: Extract and patch game.bin
            # ============================================================
            game_entry_offset = TABLE_START_OFFSET + (4 * 0x30)
            game_rom_offset = be32(rom[game_entry_offset + 0x10:game_entry_offset + 0x14])
            game_comp_size = be32(rom[game_entry_offset + 0x14:game_entry_offset + 0x18])

            # Extract and decompress game.bin
            game_compressed = bytes(rom[game_rom_offset:game_rom_offset + game_comp_size])
            game_decompressed = zdec(game_compressed)

            # Write decompressed game.bin
            with open(game_bin_path, "wb") as f:
                f.write(game_decompressed)

            # Patch game.bin with armips if asm exists
            if os.path.exists(game_bin_asm_path):
                result = subprocess.run([armips_exe, game_bin_asm_path], cwd=temp_dir, capture_output=True, text=True,
                                        creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode != 0:
                    raise RuntimeError(f"armips failed on GameBin.asm: {result.stderr}")

                game_patched_data = open(game_bin_path, "rb").read()
            else:
                game_patched_data = game_decompressed

            # Recompress and write back
            game_recompressed = zenc(game_patched_data)
            new_game_comp_size = len(game_recompressed)

            if new_game_comp_size > game_comp_size:
                # Need to relocate to expanded area
                new_game_rom_offset = EXPANDED_GAME_ROM_OFFSET
                new_game_end = new_game_rom_offset + new_game_comp_size
                ensure_len(rom, new_game_end, fill=0xFF)
                rom[new_game_rom_offset:new_game_end] = game_recompressed
                write_be32(rom, game_entry_offset + 0x10, new_game_rom_offset)
                write_be32(rom, game_entry_offset + 0x14, new_game_comp_size)
            else:
                rom[game_rom_offset:game_rom_offset + new_game_comp_size] = game_recompressed
                write_be32(rom, game_entry_offset + 0x14, new_game_comp_size)
                if new_game_comp_size < game_comp_size:
                    leftover_start = game_rom_offset + new_game_comp_size
                    leftover_end = game_rom_offset + game_comp_size
                    rom[leftover_start:leftover_end] = bytes(leftover_end - leftover_start)

            # Write updated ROM for LoaderHook
            with open(temp_rom_path, "wb") as f:
                f.write(rom)

            # ============================================================
            # PART 2: Apply LoaderHook
            # ============================================================
            if os.path.exists(loader_hook_asm_path):
                with open(loader_hook_asm_path, 'r') as f:
                    hook_content = f.read()

                # Replace input filename with temp file
                hook_content = hook_content.replace('"input.z64"', f'"{temp_rom_path}"')

                loader_hook_temp_path = os.path.join(temp_dir, "LoaderHook_temp.asm")
                with open(loader_hook_temp_path, 'w') as f:
                    f.write(hook_content)

                result = subprocess.run([armips_exe, loader_hook_temp_path], cwd=temp_dir, capture_output=True,
                                        text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode != 0:
                    raise RuntimeError(f"armips failed on LoaderHook: {result.stderr}")

                # Reload ROM after LoaderHook
                rom = bytearray(open(temp_rom_path, "rb").read())

            # ============================================================
            # PART 3: Assemble and add CustomCode
            # ============================================================
            if os.path.exists(custom_asm_path):
                result = subprocess.run([armips_exe, custom_asm_path], cwd=temp_dir, capture_output=True, text=True,
                                        creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode != 0:
                    raise RuntimeError(f"armips failed on CustomCode.asm: {result.stderr}")

                if not os.path.exists(custom_bin_path):
                    raise FileNotFoundError("armips did not create mycode.bin")

                custom_code = open(custom_bin_path, "rb").read()
                custom_compressed = zenc(custom_code)

                # Custom code parameters
                custom_load_addr = 0xE00D0000
                custom_uncomp_sz = len(custom_code)
                custom_comp_sz = len(custom_compressed)
                custom_bss_sz = 0x00000100
                custom_bss_addr = custom_load_addr + custom_uncomp_sz
                custom_total_sz = custom_uncomp_sz + custom_bss_sz

                # Write compressed custom code to ROM
                custom_rom_off = NEW_CUSTOM_ROM_OFFSET
                custom_end_off = custom_rom_off + custom_comp_sz
                ensure_len(rom, custom_end_off, fill=0x00)
                rom[custom_rom_off:custom_end_off] = custom_compressed

                # Update file table
                old_count = be32(rom[FILE_COUNT_OFFSET:FILE_COUNT_OFFSET + 4])
                write_be32(rom, FILE_COUNT_OFFSET, old_count + 1)

                entry_offset = CUSTOM_ENTRY_OFFSET
                ensure_len(rom, entry_offset + 0x30, fill=0x00)

                for i in range(0x30):
                    rom[entry_offset + i] = 0x00

                name = b"MyCode\x00"
                rom[entry_offset:entry_offset + len(name)] = name
                write_be32(rom, entry_offset + 0x10, custom_rom_off)
                write_be32(rom, entry_offset + 0x14, custom_comp_sz)
                write_be32(rom, entry_offset + 0x18, custom_load_addr)
                write_be32(rom, entry_offset + 0x1C, custom_total_sz)
                write_be32(rom, entry_offset + 0x20, custom_bss_addr)
                write_be32(rom, entry_offset + 0x24, custom_bss_sz)

            # ============================================================
            # PART 4: Finalize ROM
            # ============================================================
            final_size = next_cart_size(len(rom))
            if len(rom) < final_size:
                rom.extend(b"\xFF" * (final_size - len(rom)))

        return bytes(rom)


    @staticmethod
    def finalize_crc(caller: APProcedurePatch, rom: bytes) -> bytes:
        """
        Finalize ROM after all patch steps:
        - pad to a valid cart size
        - calculate CRC once
        """
        rom = bytearray(rom)
        final_size = next_cart_size(len(rom))
        if len(rom) < final_size:
            rom.extend(b"\xFF" * (final_size - len(rom)))

        crc1, crc2 = n64_crc(rom, cic=6102)
        rom[0x10:0x14] = crc1.to_bytes(4, "big")
        rom[0x14:0x18] = crc2.to_bytes(4, "big")
        return bytes(rom)

    @staticmethod
    def patch_seed_name(caller: APProcedurePatch, rom: bytes) -> bytes:
        options = json.loads(caller.get_file("options.json").decode("utf-8"))
        rom = bytearray(rom)

        SEED_ROM_OFFSET = 0xFFFFF0
        SEED_LEN = 16

        seed = options["seed_name"].encode("utf-8")[:SEED_LEN]
        rom[SEED_ROM_OFFSET:SEED_ROM_OFFSET + SEED_LEN] = seed.ljust(SEED_LEN, b"\x00")

        return bytes(rom)

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

        return bytes(rom)

    # Decompress all levels, place all items in the levels.
    @staticmethod
    def patch_items(caller: APProcedurePatch, rom: bytes):
        stream = io.BytesIO(rom)
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))
        stream.seek(0x540, 0)
        stream.write(options["seed_name"].encode("utf-8")[0:16])
        for i in range(len(level_locations)):
            level: dict[str, tuple] = json.loads(caller.get_file(f"level_{i}.json").decode("utf-8"))
            stream.seek(level_address[i], 0)
            stream, data = get_level_data(stream, level_size[i], i)
            for j, (location_name, item) in enumerate(level.items()):
                if item[0] == 0:
                    continue
                if "Mirror" in location_name:
                    continue
                if "Obelisk" in location_name and "Obelisk" not in items_by_id.get(item[0],
                                                                                   ItemData(0, "", "filler")).item_name:
                    try:
                        index = [index for index in range(len(data.objects)) if data.objects[index][8] == 0x26][0]
                        data.items += [
                            bytearray(data.objects[index][0:6])
                            + (items_by_id[item[0]].rom_id.to_bytes(2) if item[1] == options["player"] else bytes(
                                [0x27, 0x4]))
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
                        data.chests[
                            j - (len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][
                        12:14] = [0x27, 0x4]
                        if "Chest" in location_name:
                            data.chests[j - (
                                    len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][
                                9] = 0x1
                    else:
                        data.items[j - data.items_replaced_by_obelisks][6:8] = [0x27, 0x4]
                else:
                    if "Obelisk" in items_by_id[item[0]].item_name and "Obelisk" not in location_name:
                        if chest_barrel(location_name):
                            slice_ = bytearray(data.chests[j - (
                                    len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][
                                               0:6])
                        else:
                            slice_ = bytearray(data.items[j - data.items_replaced_by_obelisks][0:6])
                        data.objects += [
                            slice_
                            + bytearray(
                                [
                                    0x0, 0x0, 0x26, 0x1, 0x0,
                                    locationName_to_data[location_name].difficulty,
                                    0x0, 0x0, 0x0,
                                    item[0] - 77780054,
                                    0x3F, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
                                ],
                            ),
                        ]
                        if chest_barrel(location_name):
                            del data.chests[j - (
                                    len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)]
                            data.chests_replaced_by_obelisks += 1
                        else:
                            del data.items[j - data.items_replaced_by_obelisks]
                            data.items_replaced_by_obelisks += 1
                    elif (items_by_id[item[0]].progression == ItemClassification.useful or items_by_id[
                        item[0]].progression == ItemClassification.progression) and chest_barrel(location_name):
                        chest_index = j - (
                                len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)
                        chest = data.chests[chest_index]
                        slice_ = bytearray(chest[0:6])
                        data.items += [
                            slice_
                            + (items_by_id[item[0]].rom_id.to_bytes(2) if item[1] == options["player"] else bytes(
                                [0x27, 0x4]))
                            + bytes([chest[11], 0x0, 0x0, 0x0]),
                        ]
                        del data.chests[chest_index]
                        data.chests_replaced_by_items += 1
                    else:
                        if chest_barrel(location_name):
                            data.chests[j - (
                                    len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][
                            12:14] = items_by_id[item[0]].rom_id.to_bytes(2)
                            if "Chest" in location_name:
                                data.chests[j - (
                                        len(data.items) + data.items_replaced_by_obelisks + data.chests_replaced_by_obelisks)][
                                    9] = 0x2
                        else:
                            data.items[j - data.items_replaced_by_obelisks][6:8] = items_by_id[item[0]].rom_id.to_bytes(
                                2)
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
    def patch_boss_bin(caller: APProcedurePatch, rom: bytes) -> bytes:
        """
        Patch boss.bin using the same extraction / recompression flow as game.bin.

        boss.bin encodes rewards as two 16-bit integers where each is a BYTE of the 16-bit rom_id:
            rom_id = 0xABCD  -> write 0x00AB, 0x00CD  (i.e. 0x00AB00CD)

        boss_items.json stores (item_code, item_player).
        """
        boss_items_data = json.loads(caller.get_file("boss_items.json").decode("UTF-8"))
        options = json.loads(caller.get_file("options.json").decode("UTF-8"))

        # Boss.bin is entry #2 in the file table (game.bin is entry #4)
        boss_entry_offset = TABLE_START_OFFSET + (2 * 0x30)

        rom = bytearray(rom)

        boss_rom_offset = be32(rom[boss_entry_offset + 0x10:boss_entry_offset + 0x14])
        boss_comp_size = be32(rom[boss_entry_offset + 0x14:boss_entry_offset + 0x18])

        boss_compressed = bytes(rom[boss_rom_offset:boss_rom_offset + boss_comp_size])
        boss_decompressed = bytearray(zdec(boss_compressed))

        FILLER_ROM_ID = 0x2704  # same filler as patch_items (bytes [0x27, 0x04])

        for location_name, item_data in boss_items_data.items():
            if location_name not in boss_location_offsets:
                continue

            item_code, item_player = item_data
            if not item_code:
                continue

            if item_player != options["player"]:
                rom_id = FILLER_ROM_ID
            else:
                rom_id = items_by_id[item_code].rom_id  # 16-bit

            hi_byte = (rom_id >> 8) & 0xFF
            lo_byte = rom_id & 0xFF

            offset = boss_location_offsets[location_name]
            boss_decompressed[offset:offset + 2] = hi_byte.to_bytes(2, "big")
            boss_decompressed[offset + 2:offset + 4] = lo_byte.to_bytes(2, "big")

        # Recompress and write back (same as game.bin flow)
        boss_recompressed = zenc(boss_decompressed)
        new_boss_comp_size = len(boss_recompressed)

        if new_boss_comp_size > boss_comp_size:
            # Relocate to expanded area (same approach as existing working boss patcher)
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

        return bytes(rom)



class GLProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Gauntlet Legends"
    hash = "9cb963e8b71f18568f78ec1af120362e"
    patch_file_ending = ".apgl"
    result_file_ending = ".z64"

    procedure = [
        ("patch_repack", []),  # full ROM rebuild + ASM
        ("patch_items", []),  # level data
        ("patch_boss_bin", []),  # boss.bin
        ("patch_counts", []),  # misc data
        ("patch_seed_name", []),  # 0x540 write
        ("finalize_crc", []),  # ONE CRC, LAST
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


# Write data on all placed items into json files.
# Also save options
def write_files(world: "GauntletLegendsWorld", patch: GLProcedurePatch) -> None:
    options_dict = {
        "seed_name": world.multiworld.seed_name,
        "player": world.player,
    }
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))

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
    data.stream.write(bytes([0xFB, 0x29, 0x0, 0x82]))
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
    if level == 23:
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
            data.chests_replaced_by_items + data.obelisks_replaced_by_items - data.items_replaced_by_obelisks)
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
