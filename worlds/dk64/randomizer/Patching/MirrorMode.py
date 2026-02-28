"""Changes for Mirror Mode."""

import js
import gzip
import zlib
import time
from randomizer.Patching.Patcher import LocalROM, ROM
from randomizer.Settings import Settings
from randomizer.Patching.Library.Assets import TableNames, getRawFile, writeRawFile


def FlipDisplayList(ROM_COPY: LocalROM, data: bytearray, start: int, end: int, table: int, file: int):
    """Flip the 2nd and 3rd vertices on any G_TRI, G_TRI2 or G_QUAD f3dex2 call."""
    instruction_count = int((end - start) / 8)
    for ins in range(instruction_count):
        ins_start = start + (8 * ins)
        ins_type = data[ins_start]
        if ins_type in (5, 6, 7):
            for offset in (2, 6):
                v1 = data[ins_start + offset]
                v2 = data[ins_start + offset + 1]
                data[ins_start + offset] = v2
                data[ins_start + offset + 1] = v1
    writeRawFile(table, file, True, data, ROM_COPY)


def readDataFromBytestream(data: bytearray, offset: int, size: int) -> int:
    """Read data from a byte stream and output an int."""
    value = 0
    for x in range(size):
        value <<= 8
        value += data[offset + x]
    return value


def ApplyMirrorMode(settings: Settings, ROM_COPY: LocalROM):
    """Apply all Mirror Mode changes."""
    if not settings.mirror_mode:
        return
    for tbl in (TableNames.ActorGeometry, TableNames.ModelTwoGeometry, TableNames.MapGeometry):
        file_count = len(js.pointer_addresses[tbl]["entries"])
        for file_index in range(file_count):
            data = bytearray(getRawFile(ROM_COPY, tbl, file_index, True))
            if len(data) == 0:
                continue
            if tbl == TableNames.MapGeometry:
                dl_start = readDataFromBytestream(data, 0x34, 4)
                dl_end = readDataFromBytestream(data, 0x38, 4)
            elif tbl == TableNames.ActorGeometry:
                addr_offset = readDataFromBytestream(data, 0, 4)
                dl_end = 0x28 + (readDataFromBytestream(data, 4, 4) - addr_offset)
                dl_start = 0x28 + (readDataFromBytestream(data, dl_end, 4) - addr_offset)
            elif tbl == TableNames.ModelTwoGeometry:
                dl_start = readDataFromBytestream(data, 0x40, 4)
                dl_end = readDataFromBytestream(data, 0x48, 4)
            FlipDisplayList(ROM_COPY, data, dl_start, dl_end, tbl, file_index)


def trimData(data: bytes, alignment: int = 0x10) -> bytes:
    """Trim a bytes object to remove trailing null bytes, and then align the size of the object to a certain modulo."""
    if alignment <= 0:
        raise ValueError("alignment must be positive")

    i = len(data) - 1
    while i >= 0 and data[i] == 0:
        i -= 1
    if i < 0:
        return b""
    trimmed = data[: i + 1]

    pad = (-len(trimmed)) % alignment
    if pad:
        trimmed += b"\x00" * pad

    return trimmed


def truncateFiles(ROM_COPY: ROM):
    """Truncate the size of compressed files."""
    start = time.perf_counter()
    POINTER_OFFSET = 0x101C50
    uncompressed_tables = [
        TableNames.TexturesUncompressed,
        TableNames.Cutscenes,
        TableNames.Setups,
        TableNames.InstanceScripts,
        TableNames.Text,
        TableNames.Spawners,
        TableNames.Triggers,
        TableNames.Unknown20,
        TableNames.Autowalks,
        TableNames.Exits,
        TableNames.RaceCheckpoints,
    ]
    total_bytes_overwritten = 0
    for table_id in range(26):
        if table_id in uncompressed_tables:
            # These tables are always uncompressed, ignore
            continue
        if table_id in (TableNames.MapWalls, TableNames.MapFloors):
            # messing with these tables causes the game to take a hard angry nap
            continue
        ROM_COPY.seek(POINTER_OFFSET + (32 * 4) + (table_id * 4))
        entry_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        files = []
        ROM_COPY.seek(POINTER_OFFSET + (table_id * 4))
        table_start = POINTER_OFFSET + int.from_bytes(ROM_COPY.readBytes(4), "big")
        please_shift = False
        for entry in range(entry_count):
            ROM_COPY.seek(table_start + (entry * 4))
            file_start = POINTER_OFFSET + (int.from_bytes(ROM_COPY.readBytes(4), "big") & 0x7FFFFFFF)
            file_end = POINTER_OFFSET + (int.from_bytes(ROM_COPY.readBytes(4), "big") & 0x7FFFFFFF)
            file_size = file_end - file_start
            if file_size <= 0:
                files.append(b"")
                continue
            ROM_COPY.seek(file_start)
            data = ROM_COPY.readBytes(file_size)
            ROM_COPY.seek(file_start)
            indicator = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if indicator == 0x1F8B:
                truncated_data = gzip.compress(zlib.decompress(data, (15 + 32)), compresslevel=9)
                if len(data) != len(truncated_data):
                    please_shift = True
            elif table_id == TableNames.MusicMIDI:
                truncated_data = trimData(data, 0x10)
                please_shift = True
            else:
                truncated_data = data
            files.append(truncated_data)
        if please_shift:
            ROM_COPY.seek(table_start)
            head = POINTER_OFFSET + (int.from_bytes(ROM_COPY.readBytes(4), "big") & 0x7FFFFFFF)
            total_offset = 0
            for entry in range(entry_count):
                ROM_COPY.seek(table_start + (entry * 4) + 4)
                entry_size = len(files[entry])
                append_byte = False
                if (entry_size % 2) == 1:
                    entry_size += 1
                    append_byte = True
                file_head = head + total_offset
                new_location = (head + total_offset + entry_size) - POINTER_OFFSET
                ROM_COPY.writeMultipleBytes(new_location, 4)
                ROM_COPY.seek(file_head)
                ROM_COPY.writeBytes(files[entry])
                if append_byte:
                    ROM_COPY.write(0)
                total_offset += entry_size
                total_bytes_overwritten += entry_size + 4
    end = time.perf_counter()
    print(f"File truncating took {end - start:.6f} seconds. Processed {hex(total_bytes_overwritten)} bytes")
