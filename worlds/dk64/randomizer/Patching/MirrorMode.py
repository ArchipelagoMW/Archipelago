"""Changes for Mirror Mode."""

import js
from randomizer.Patching.Patcher import LocalROM
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
