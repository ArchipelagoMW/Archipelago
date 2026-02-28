"""Library functions for pointer tables (Heavily WIP)."""

import js
import zlib
import gzip
from typing import Dict, List, Tuple, Union
from enum import IntEnum, auto
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Patching.Library.DataTypes import float_to_hex


class TableNames(IntEnum):
    """Pointer Table Enum."""

    MusicMIDI = 0
    MapGeometry = auto()
    MapWalls = auto()
    MapFloors = auto()
    ModelTwoGeometry = auto()
    ActorGeometry = auto()
    Unknown6 = auto()
    TexturesUncompressed = auto()
    Cutscenes = auto()
    Setups = auto()
    InstanceScripts = auto()
    Animations = auto()
    Text = auto()
    Unknown13 = auto()
    TexturesHUD = auto()
    Paths = auto()
    Spawners = auto()
    DKTVInputs = auto()
    Triggers = auto()
    Unknown19 = auto()
    Unknown20 = auto()
    Autowalks = auto()
    Unknown22 = auto()
    Exits = auto()
    RaceCheckpoints = auto()
    TexturesGeometry = auto()
    UncompressedFileSizes = auto()
    Unknown27 = auto()
    Unknown28 = auto()
    Unknown29 = auto()
    Unknown30 = auto()
    Unknown31 = auto()


class ItemPreview(IntEnum):
    """Item Preview Enum."""

    JapesMinecartIntro = 0
    JapesMinecartReward = auto()
    JapesMinecartFail = auto()
    FungiMinecartIntro = auto()
    FungiMinecartFail = auto()
    CastleMinecartIntro = auto()
    CastleMinecartReward = auto()
    FactoryCarRace = auto()
    MermaidIntro = auto()
    MermaidReward = auto()
    MermaidMissing = auto()
    VultureFreedom = auto()
    VulturePreview = auto()
    LlamaTalk = auto()
    LlamaRescue = auto()
    JetpacIntro = auto()
    JetpacReward = auto()
    RabbitFinalRaceIntro = auto()
    RabbitFirstRaceReward = auto()
    RabbitFinalRaceReward = auto()
    AppleIntro = auto()
    ApplePickUp = auto()
    AppleReward = auto()
    Seal = auto()
    RarewareGB = auto()
    IceTomato = auto()
    CastleCarRace = auto()
    OwlRace = auto()
    GoneMicro = auto()
    PortMicro = auto()
    BongosMicro = auto()
    TriangleMicro = auto()
    SaxMicro = auto()
    TromboneMicro = auto()
    GuitarMicro = auto()
    SpiderIntro = auto()
    SlamMicro = auto()
    ChunkyIgloo = auto()
    CrankyMicro = auto()
    FunkyMicro = auto()
    CandyMicro = auto()
    SnideMicro = auto()


class CompTextFiles(IntEnum):
    """Compressed Text Files Enum."""

    PreviewsNormal = 0x40
    PreviewsFlavor = auto()
    Wrinkly = auto()
    WrinklyShort = auto()
    ItemLocations = auto()


class TableData:
    """Class to store information regarding a pointer table."""

    def __init__(
        self,
        vanilla_compressed: bool,
        rando_compressed: bool,
        decode_function=None,
        encode_function=None,
    ):
        """Initialize with given variables."""
        self.vanilla_compressed = vanilla_compressed
        self.rando_compressed = rando_compressed
        self.decode_function = decode_function
        self.encode_function = encode_function


def decoder_exits(data: bytes) -> dict:
    """Decode the exit data."""
    exit_count = int(len(data) / 10)
    ret = {"exits": []}
    for exit_index in range(exit_count):
        exit_data = {}
        ret["exits"].append(exit_data)
    return ret


table_functions = {
    TableNames.MusicMIDI: TableData(False, False, None, None),
    TableNames.MapGeometry: TableData(False, False, None, None),
    TableNames.MapWalls: TableData(False, False, None, None),
    TableNames.MapFloors: TableData(False, False, None, None),
    TableNames.ModelTwoGeometry: TableData(False, False, None, None),
    TableNames.ActorGeometry: TableData(False, False, None, None),
    TableNames.Unknown6: TableData(False, False, None, None),
    TableNames.TexturesUncompressed: TableData(False, False, None, None),
    TableNames.Cutscenes: TableData(False, False, None, None),
    TableNames.Setups: TableData(False, False, None, None),
    TableNames.InstanceScripts: TableData(False, False, None, None),
    TableNames.Animations: TableData(False, False, None, None),
    TableNames.Text: TableData(False, False, None, None),
    TableNames.Unknown13: TableData(False, False, None, None),
    TableNames.TexturesHUD: TableData(False, False, None, None),
    TableNames.Paths: TableData(False, False, None, None),
    TableNames.Spawners: TableData(False, False, None, None),
    TableNames.DKTVInputs: TableData(False, False, None, None),
    TableNames.Triggers: TableData(False, False, None, None),
    TableNames.Unknown19: TableData(False, False, None, None),
    TableNames.Unknown20: TableData(False, False, None, None),
    TableNames.Autowalks: TableData(False, False, None, None),
    TableNames.Unknown22: TableData(False, False, None, None),
    TableNames.Exits: TableData(False, False, None, None),
    TableNames.RaceCheckpoints: TableData(False, False, None, None),
    TableNames.TexturesGeometry: TableData(False, False, None, None),
    TableNames.UncompressedFileSizes: TableData(False, False, None, None),
    TableNames.Unknown27: TableData(False, False, None, None),
    TableNames.Unknown28: TableData(False, False, None, None),
    TableNames.Unknown29: TableData(False, False, None, None),
    TableNames.Unknown30: TableData(False, False, None, None),
    TableNames.Unknown31: TableData(False, False, None, None),
}


class PointerTableFile:
    """Class to store information about a pointer table file."""

    def __init__(self, table: TableNames, start: int, end: int, is_compressed: bool = None):
        """Initialize with given parameters."""
        self.start = start
        self.end = end
        self.size = end - start
        self.is_compressed = is_compressed
        if is_compressed is None:
            self.is_compressed = table_functions[table].rando_compressed


def getPointerLocation(table: TableNames, file_index: int) -> int:
    """Get the address of a pointer table file."""
    return js.pointer_addresses[table]["entries"][file_index]["pointing_to"]


def getPointerFile(table: TableNames, file_index: int, is_compressed: bool = None) -> PointerTableFile:
    """Get pointer table file information."""
    start = getPointerLocation(table, file_index)
    if "compressed_size" in js.pointer_addresses[table]["entries"][file_index]:
        file_size = js.pointer_addresses[table]["entries"][file_index]["compressed_size"]
    else:
        file_end = getPointerLocation(table, file_index + 1)
        file_size = file_end - start
    end = start + file_size
    return PointerTableFile(table, start, end, is_compressed)


def getPointerData(ROM_COPY: LocalROM | ROM, table: TableNames, file_index: int) -> bytes:
    """Get the data inside a pointer table file."""
    ref_data = getPointerFile(table, file_index)
    ROM_COPY.seek(ref_data.start)
    data = ROM_COPY.readBytes(ref_data.size)
    if ref_data.is_compressed:
        return zlib.decompress(data, (15 + 32))
    return data


def writePointerFile(ROM_COPY: LocalROM | ROM, table: TableNames, file_index: int, data: bytes, is_compressed: bool = False):
    """Write data to a pointer file."""
    ref_file = getPointerFile(table, file_index)
    if is_compressed:
        data = gzip.compress(data, compresslevel=9)
    if len(data) > ref_file.size:
        raise Exception(f"Attempted to write data to a file slot which isn't big enough.\n- Table: {table}\n- File {file_index}\n- Attempt size {hex(len(data))}\n- Capacity: {hex(ref_file.size)}")
    ROM_COPY.seek(ref_file.start)
    ROM_COPY.writeBytes(data)


def decodeFile(ROM_COPY: LocalROM | ROM, table: TableNames, file_index: int) -> dict:
    """Decode a pointer table file."""
    function_data = table_functions.get(table, (None, None))
    file_data = getPointerData(ROM_COPY, table, file_index)
    if function_data.decode_function is None:
        return {
            "data": file_data,
        }
    return function_data.decode_function(file_data)


def encodeFile(ROM_COPY: LocalROM | ROM, table: TableNames, file_index: int, data: dict):
    """Encode a pointer table file."""
    function_data = table_functions.get(table, (None, None))
    ref_data = getPointerFile(table, file_index)
    if function_data.encode_function is None:
        writePointerFile(ROM_COPY, table, file_index, data["data"], ref_data.is_compressed)
        return
    output_data = function_data.encode_function(data)
    writePointerFile(ROM_COPY, table, file_index, output_data, ref_data.is_compressed)


def getRawFile(ROM_COPY: Union[ROM, LocalROM], table_index: TableNames, file_index: int, compressed: bool):
    """Get raw file from ROM."""
    file_start = getPointerLocation(table_index, file_index)
    if "compressed_size" in js.pointer_addresses[table_index]["entries"][file_index]:
        file_size = js.pointer_addresses[table_index]["entries"][file_index]["compressed_size"]
        if file_size is None:
            return bytes(bytearray([]))
    else:
        file_end = getPointerLocation(table_index, file_index + 1)
        file_size = file_end - file_start
    ROM_COPY.seek(file_start)
    data = ROM_COPY.readBytes(file_size)
    if compressed:
        data = zlib.decompress(data, (15 + 32))
    return data


def writeRawFile(table_index: TableNames, file_index: int, compressed: bool, data: bytearray, ROM_COPY):
    """Write raw file from ROM."""
    file_start = getPointerLocation(table_index, file_index)
    if "compressed_size" in js.pointer_addresses[table_index]["entries"][file_index]:
        file_size = js.pointer_addresses[table_index]["entries"][file_index]["compressed_size"]
    else:
        file_end = getPointerLocation(table_index, file_index + 1)
        file_size = file_end - file_start
    write_data = bytes(data)
    if compressed:
        write_data = gzip.compress(bytes(data), compresslevel=9)
    if len(write_data) > file_size:
        raise Exception(f"Cannot write file {file_index} in table {table_index} to ROM as it's too big ({hex(len(write_data))} > {hex(file_size)}).")
    ROM_COPY.seek(file_start)
    ROM_COPY.writeBytes(write_data)


icon_db = {
    0x0: "waterfall_tall",
    0x1: "waterfall_short",
    0x2: "water",
    0x3: "lava",
    0x4: "sparkles",
    0x5: "pop_explosion",
    0x6: "lava_explosion",
    0x7: "green_leaf?",
    0x8: "brown_smoke_explosion",
    0x9: "small_explosion",
    0xA: "solar_flare?",
    0xB: "splash",
    0xC: "bubble",
    0xD: "purple_sparkle",
    0xE: "yellow_sparkle",
    0xF: "green_sparkle",
    0x10: "purple_sparkle",
    0x11: "yellow_sparkle",
    0x12: "green_sparkle",
    0x13: "large_smoke_explosion",
    0x14: "pink_implosion",
    0x15: "brown_horizontal_spinning_plank",
    0x16: "birch_horizontal_spinning_plank",
    0x17: "brown_vertical_spinning_plank",
    0x18: "star_water_ripple",
    0x19: "circle_water_ripple",
    0x1A: "small_smoke_explosion",
    0x1B: "static_star",
    0x1C: "static_z",
    0x1D: "white_flare?",
    0x1E: "static_rain?",
    0x1F: "medium_smoke_explosion",
    0x20: "bouncing_melon",
    0x21: "vertical_rolling_melon",
    0x22: "red_flare?",
    0x23: "sparks",
    0x24: "peanut",
    0x25: "star_flare?",
    0x26: "peanut_shell",
    0x27: "small_explosion",
    0x28: "large_smoke_implosion",
    0x29: "blue_lazer",
    0x2A: "pineapple",
    0x2B: "fireball",
    0x2C: "orange",
    0x2D: "grape",
    0x2E: "grape_splatter",
    0x2F: "tnt_sparkle",
    0x30: "fire_explosion",
    0x31: "small_fireball",
    0x32: "diddy_coin",
    0x33: "chunky_coin",
    0x34: "lanky_coin",
    0x35: "dk_coin",
    0x36: "tiny_coin",
    0x37: "dk_coloured_banana",
    0x38: "film",
    0x39: "bouncing_orange",
    0x3A: "crystal_coconut",
    0x3B: "gb",
    0x3C: "banana_medal",
    0x3D: "diddy_coloured_banana",
    0x3E: "chunky_coloured_banana",
    0x3F: "lanky_coloured_banana",
    0x40: "dk_coloured_banana",
    0x41: "tiny_coloured_banana",
    0x42: "exploded_krash_barrel_enemy",
    0x43: "white_explosion_thing",
    0x44: "coconut",
    0x45: "coconut_shell",
    0x46: "spinning_watermelon_slice",
    0x47: "tooth",
    0x48: "ammo_crate",
    0x49: "race_coin",
    0x4A: "lanky_bp",
    0x4B: "cannonball",
    0x4C: "crystal_coconut",
    0x4D: "feather",
    0x4E: "guitar_gazump",
    0x4F: "bongo_blast",
    0x50: "saxophone",
    0x51: "triangle",
    0x52: "trombone",
    0x53: "waving_yellow_double_eighth_note",
    0x54: "waving_yellow_single_eighth_note",
    0x55: "waving_green_single_eighth_note",
    0x56: "waving_purple_double_eighth_note",
    0x57: "waving_red_double_eighth_note",
    0x58: "waving_red_single_eighth_note",
    0x59: "waving_white_double_eighth_note",
    0x5A: "diddy_bp",
    0x5B: "chunky_bp",
    0x5C: "dk_bp",
    0x5D: "tiny_bp",
    0x5E: "spinning_sparkle",
    0x5F: "static_rain?",
    0x60: "translucent_water",
    0x61: "unk61",
    0x62: "black_screen",
    0x63: "white_cloud",
    0x64: "thin_lazer",
    0x65: "blue_bubble",
    0x66: "white_faded_circle",
    0x67: "white_circle",
    0x68: "grape_particle?",
    0x69: "spinning_blue_sparkle",
    0x6A: "white_smoke_explosion",
    0x6B: "l-r_joystick",
    0x6C: "fire_wall",
    0x6D: "static_rain_bubble",
    0x6E: "a_button",
    0x6F: "b_button",
    0x70: "z_button",
    0x71: "c_down_button",
    0x72: "c_up_button",
    0x73: "c_left_button",
    0x74: "acid",
    0x75: "acid_explosion",
    0x76: "race_hoop",
    0x77: "acid_goop?",
    0x78: "unk78",
    0x79: "broken_bridge?",
    0x7A: "white_pole?",
    0x7B: "bridge_chip?",
    0x7C: "wooden_beam_with_rivets",
    0x7D: "chunky_bunch",
    0x7E: "diddy_bunch",
    0x7F: "lanky_bunch",
    0x80: "dk_bunch",
    0x81: "tiny_bunch",
    0x82: "chunky_balloon",
    0x83: "diddy_balloon",
    0x84: "dk_balloon",
    0x85: "lanky_balloon",
    0x86: "tiny_balloon",
    0x87: "r_button",
    0x88: "l_button",
    0x89: "fairy",
    0x8A: "boss_key",
    0x8B: "crown",
    0x8C: "rareware_coin",
    0x8D: "nintendo_coin",
    0x8E: "no_symbol",
    0x8F: "headphones",
    0x90: "opaque_blue_water",
    0x91: "start_button",
    0x92: "white_question_mark",
    0x93: "candy_face",
    0x94: "cranky_face",
    0x95: "snide_face",
    0x96: "funky_face",
    0x97: "left_arrow",
    0x98: "white_spark?",
    0x99: "black_boulder_chunk",
    0x9A: "green_boulder_chunk",
    0x9B: "wood_chip",
    0x9C: "snowflake/dandelion",
    0x9D: "static_water?",
    0x9E: "spinning_leaf",
    0x9F: "flashing_water?",
    0xA0: "rainbow_coin",
    0xA1: "shockwave_orange_particle",
    0xA2: "implosion?",
    0xA3: "rareware_employee_face",
    0xA4: "smoke",
    0xA5: "static_smoke?",
    0xA6: "barrel_bottom_chunk",
    0xA7: "scoff_face",
    0xA8: "multicoloured_bunch",
    0xA9: "dk_face",
    0xAA: "diddy_face",
    0xAB: "lanky_face",
    0xAC: "tiny_face",
    0xAD: "chunky_face",
    0xAE: "fairy_tick",
    0xAF: "wrinkly",
}


def grabText(ROM_COPY: Union[ROM, LocalROM], file_index: int) -> List[List[Dict[str, List[str]]]]:
    """Pull text from ROM with a particular file index."""
    table_index = TableNames.Text
    if (file_index & 0x40) != 0:
        table_index = TableNames.Unknown6
        file_index &= 0x3F
    file = getRawFile(ROM_COPY, table_index, file_index, table_index == TableNames.Unknown6)
    count = file[0]
    text = []
    text_data = []
    text_start = (count * 0xF) + 3
    data_start = 1
    for i in range(count):
        section_1_count = file[data_start + 0]
        section_2_count = file[data_start + 1]
        section_3_count = file[data_start + 2]
        start = int.from_bytes(file[data_start + 5 : data_start + 7], "big")
        int.from_bytes(file[data_start + 7 : data_start + 9], "big")
        block_start = 1
        blocks = []
        for k in range(section_1_count):
            sec2ct = file[data_start + block_start]
            offset = 0
            if (sec2ct & 4) != 0:
                offset += 4
            text_blocks = []
            if (sec2ct & 1) == 0:
                if (sec2ct & 2) != 0:
                    sec3ct = file[data_start + block_start + offset + 1]
                    for j in range(sec3ct):
                        _block = block_start + 2 + offset + (4 * j) - 1
                        _pos = int.from_bytes(file[data_start + _block : data_start + _block + 2], "big")
                        _dat = int.from_bytes(file[data_start + _block : data_start + _block + 4], "big")
                        text_blocks.append(
                            {
                                "type": "sprite",
                                "position": _pos,
                                "data": hex(_dat),
                                "sprite": icon_db[(_dat >> 8) & 0xFF],
                            }
                        )
                    added = block_start + 2 + offset + (4 * sec3ct) + 4
            else:
                sec3ct = file[data_start + block_start + offset + 1]
                for j in range(sec3ct):
                    _block = block_start + 2 + offset + (8 * j) - 1
                    _start = int.from_bytes(file[data_start + _block + 3 : data_start + _block + 5], "big")
                    _size = int.from_bytes(file[data_start + _block + 5 : data_start + _block + 7], "big")
                    text_blocks.append({"type": "normal", "start": _start, "size": _size})
                added = block_start + 2 + offset + (8 * sec3ct) + 4
            # print(f"File {file_index}, Textbox {i}, section {k}")
            blocks.append(
                {
                    "block_start": hex(block_start + data_start),
                    "section2count": sec2ct,
                    "section3count": sec3ct,
                    "offset": offset,
                    "text": text_blocks,
                }
            )
            block_start = added
        if added < data_start:
            info = b""
        else:
            info = file[data_start:added]
        text_data.append(
            {
                "arr": info,
                "text": blocks,
                "section1count": section_1_count,
                "section2count": section_2_count,
                "section3count": section_3_count,
                "data_start": hex(data_start),
            }
        )
        text_start += added - data_start
        data_start += block_start
    for item in text_data:
        text_block = []
        # print(item)
        for item2 in item["text"]:
            # print(item2)
            temp = []
            for item3 in item2["text"]:
                if item3["type"] == "normal":
                    start = item3["start"] + data_start + 2
                    # print(hex(start))
                    start + item3["size"]
                    temp.append(file[start : start + item3["size"]].decode())
                elif item3["type"] == "sprite":
                    temp.append(item3["sprite"])
                    # print(fh.read(item3["size"]))
            text_block.append(temp)
        text.append(text_block)
    formatted_text = []
    for t in text:
        y = []
        for x in t:
            y.append({"text": x})
        formatted_text.append(y)
    return formatted_text


def writeText(ROM_COPY: Union[ROM, LocalROM], file_index: int, text: List[Union[List[Dict[str, List[str]]], Tuple[Dict[str, List[str]]]]]) -> None:
    """Write the text to ROM."""
    file = []
    file.append(len(text))
    position = 0
    for textbox in text:
        file.append(len(textbox))
        for block in textbox:
            # Get Icon State
            icon_id = -1
            for string in block["text"]:
                if string in icon_db.values():
                    for icon in icon_db:
                        if icon_db[icon] == string:
                            icon_id = icon
            if icon_id > -1:
                file.extend([2, 1])
                file.append((icon_id >> 8) & 0xFF)
                file.append(icon_id & 0xFF)
                file.extend([0, 0])
            else:
                file.extend([1, len(block["text"])])
                for string in block["text"]:
                    file.append((position >> 24) & 0xFF)
                    file.append((position >> 16) & 0xFF)
                    file.append((position >> 8) & 0xFF)
                    file.append(position & 0xFF)
                    file.append((len(string) >> 8) & 0xFF)
                    file.append(len(string) & 0xFF)
                    file.extend([0, 0])
                    position += len(string)
            unk0 = 0
            if "unk0" in block:
                unk0 = block["unk0"]
            value = int(float_to_hex(unk0), 16)
            file.append((value >> 24) & 0xFF)
            file.append((value >> 16) & 0xFF)
            file.append((value >> 8) & 0xFF)
            file.append(value & 0xFF)
    file.append((position >> 8) & 0xFF)
    file.append(position & 0xFF)
    for textbox in text:
        for block in textbox:
            is_icon = False
            for string in block["text"]:
                if string in icon_db.values():
                    is_icon = True
            if not is_icon:
                for string in block["text"]:
                    file.extend(list(string.encode("ascii")))
    table_index = TableNames.Text
    data = bytes(file)
    if (file_index & 0x40) != 0:
        table_index = TableNames.Unknown6
        file_index &= 0x3F
        uncompressed_size = len(data)
        unc_data = getPointerLocation(TableNames.UncompressedFileSizes, TableNames.Unknown6)
        ROM_COPY.seek(unc_data + (file_index * 4))
        ROM_COPY.writeMultipleBytes(uncompressed_size, 4)
    # print("Attempting to write", hex(len(data)), "bytes to pointer", int(table_index), "file", int(file_index))
    writeRawFile(table_index, file_index, table_index == TableNames.Unknown6, bytearray(data), ROM_COPY)
