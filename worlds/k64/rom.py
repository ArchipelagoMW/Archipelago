import pkgutil
import typing

import Utils
from typing import Optional, Dict, List, Tuple, Union
import hashlib
import os
import struct

import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
import bsdiff4
from io import BytesIO

from .aesthetics import write_aesthetics
from .regions import default_levels
from .calculate_crc import recalculate_6103_crcs

if typing.TYPE_CHECKING:
    from . import K64World

K64UHASH = "d33e4254336383a17ff4728360562ada"

stage_locations: Dict[int, Tuple[int, int]] = {
    0x0001: (0, 0),
    0x0002: (0, 1),
    0x0003: (0, 2),
    0x0004: (1, 0),
    0x0005: (1, 1),
    0x0006: (1, 2),
    0x0007: (1, 3),
    0x0008: (2, 0),
    0x0009: (2, 1),
    0x000A: (2, 2),
    0x000B: (2, 3),
    0x000C: (3, 0),
    0x000D: (3, 1),
    0x000E: (3, 2),
    0x000F: (3, 3),
    0x0010: (4, 0),
    0x0011: (4, 1),
    0x0012: (4, 2),
    0x0013: (4, 3),
    0x0014: (5, 0),
    0x0015: (5, 1),
    0x0016: (5, 2),
    0x0200: (0, 3),
    0x0201: (1, 4),
    0x0202: (2, 4),
    0x0203: (3, 4),
    0x0204: (4, 4),
    0x0205: (5, 3),
}

stage_select_ptrs: Dict[int, Tuple[int, int]] = {  # un-cleared pal, uncleared, cleared pal, cleared
    0x0001: (0x713A0, 0x713A8),
    0x0002: (0x713B0, 0x713B8),
    0x0003: (0x713C0, 0x713C8),
    0x0004: (0x71408, 0x71410),
    0x0005: (0x71418, 0x71420),
    0x0006: (0x71428, 0x71430),
    0x0007: (0x71438, 0x71440),
    0x0008: (0x71470, 0x71478),
    0x0009: (0x71480, 0x71488),
    0x000A: (0x71490, 0x71498),
    0x000B: (0x714A0, 0x714A8),
    0x000C: (0x714D8, 0x714E0),
    0x000D: (0x714E8, 0x714F0),
    0x000E: (0x714F8, 0x71500),
    0x000F: (0x71508, 0x71510),
    0x0010: (0x71540, 0x71548),
    0x0011: (0x71550, 0x71558),
    0x0012: (0x71560, 0x71568),
    0x0013: (0x71570, 0x71578),
    0x0014: (0x715A8, 0x715B0),
    0x0015: (0x715B8, 0x715C0),
    0x0016: (0x715C8, 0x715D0),
    0x0200: (0x713D0, 0x713D8),
    0x0201: (0x71448, 0x71450),
    0x0202: (0x714B0, 0x714B8),
    0x0203: (0x71518, 0x71520),
    0x0204: (0x71580, 0x71588),
    0x0205: (0x715D8, 0x715E0),
}

stage_select_vals: Dict[int, Tuple[int, int, int, int]] = {
    0x0001: (0x9912B0, 0x9914D0, 0x9914D0, 0x991820),
    0x0002: (0x991820, 0x991A40, 0x991A40, 0x991C60),
    0x0003: (0x991C60, 0x991E80, 0x991E80, 0x9920A0),
    0x0004: (0x9949A0, 0x994C60, 0x994C60, 0x994F20),
    0x0005: (0x994F20, 0x9951E0, 0x9951E0, 0x9954A0),
    0x0006: (0x9954A0, 0x995760, 0x995760, 0x995A20),
    0x0007: (0x995A20, 0x995CE0, 0x995CE0, 0x995FA0),
    0x0008: (0x998DC0, 0x999080, 0x999080, 0x999340),
    0x0009: (0x999340, 0x999600, 0x999600, 0x9998C0),
    0x000A: (0x9998C0, 0x999B80, 0x999B80, 0x999E40),
    0x000B: (0x999E40, 0x99A100, 0x99A100, 0x99A3C0),
    0x000C: (0x99C340, 0x99C600, 0x99C600, 0x99C8C0),
    0x000D: (0x99C8C0, 0x99CB80, 0x99CB80, 0x99CE40),
    0x000E: (0x99CE40, 0x99D100, 0x99D100, 0x99D3C0),
    0x000F: (0x99D3C0, 0x99D680, 0x99D680, 0x99D940),
    0x0010: (0x99FD70, 0x9A0030, 0x9A0030, 0x9A02F0),
    0x0011: (0x9A02F0, 0x9A05B0, 0x9A05B0, 0x9A0870),
    0x0012: (0x9A0870, 0x9A0B30, 0x9A0B30, 0x9A0DF0),
    0x0013: (0x9A0DF0, 0x9A10B0, 0x9A10B0, 0x9A1370),
    0x0014: (0x9A36B0, 0x9A3970, 0x9A3970, 0x9A3D70),
    0x0015: (0x9A3D70, 0x9A4030, 0x9A4030, 0x9A42F0),
    0x0016: (0x9A42F0, 0x9A45B0, 0x9A45B0, 0x9A49B0),
    0x0200: (0x9920A0, 0x9922C0, 0x9922C0, 0x9924E0),
    0x0201: (0x995FA0, 0x996260, 0x996260, 0x996520),
    0x0202: (0x99A3C0, 0x99A680, 0x99A680, 0x99A940),
    0x0203: (0x99D940, 0x99DC00, 0x99DC00, 0x99DEC0),
    0x0204: (0x9A1370, 0x9A1630, 0x9A1630, 0x9A18F0),
    0x0205: (0x9A49B0, 0x9A4C70, 0x9A4C70, 0x9A4F30),
}

stage_select_param_ptrs = {
    0x0001: [0x991470, 0x9917CC],
    0x0002: [0x9919E0, 0x991C00],
    0x0003: [0x991E20, 0x992040],
    0x0004: [0x994C0C, 0x994ECC],
    0x0005: [0x99518C, 0x99544C],
    0x0006: [0x99570C, 0x9959CC],
    0x0007: [0x995C8C, 0x995F4C],
    0x0008: [0x99902C, 0x9992EC],
    0x0009: [0x9995AC, 0x99986C],
    0x000A: [0x999B2C, 0x999DEC],
    0x000B: [0x99A0AC, 0x99A36C],
    0x000C: [0x99C5AC, 0x99C86C],
    0x000D: [0x99CB2C, 0x99CDEC],
    0x000E: [0x99D0AC, 0x99D36C],
    0x000F: [0x99D62C, 0x99D8EC],
    0x0010: [0x99FFDC, 0x9A029C],
    0x0011: [0x9A055C, 0x9A081C],
    0x0012: [0x9A0ADC, 0x9A0D9C],
    0x0013: [0x9A105C, 0x9A131C],
    0x0014: [0x9A391C, 0x9A3D18],
    0x0015: [0x9A3FDC, 0x9A429C],
    0x0016: [0x9A455C, 0x9A4958],
    0x0200: [0x992260, 0x992480],
    0x0201: [0x99620C, 0x9964CC],
    0x0202: [0x99A62C, 0x99A8EC],
    0x0203: [0x99DBAC, 0x99DE6C],
    0x0204: [0x9A15DC, 0x9A189C],
    0x0205: [0x9A4C1C, 0x9A4EDC],
}

stage_select_param_vals: Dict[int, List[float]] = {
    0x0001: [-7, 22, -31],
    0x0002: [68, 22, -24],
    0x0003: [-48, 22, 44],
    0x0004: [-5, 21, -34],
    0x0005: [70, 21, -25],
    0x0006: [-75, 21, 47],
    0x0007: [-3, 21, 43],
    0x0008: [-4, 22, -31],
    0x0009: [67, 22, -21],
    0x000A: [-74, 22, 47],
    0x000B: [-2, 22, 43],
    0x000C: [-3, 21, -33],
    0x000D: [70, 21, -22],
    0x000E: [-77, 21, 51],
    0x000F: [-2, 21, 43],
    0x0010: [-7, 21, -33],
    0x0011: [73, 21, -25],
    0x0012: [-75, 21, 47],
    0x0013: [-3, 21, 38],
    0x0014: [-6, 21, -37],
    0x0015: [72, 21, -21],
    0x0016: [-53, 21, 42],
    0x0200: [40, 22, 46],
    0x0201: [71, 21, 51],
    0x0202: [72, 22, 47],
    0x0203: [70, 21, 49],
    0x0204: [71, 21.5, 49],
    0x0205: [38, 21, 46],
}

crystal_requirements = 720664
slot_data = 720672
level_index = 720688
stage_index = 720880


class RomData:
    def __init__(self, file: str, name: typing.Optional[str] = None):
        self.file = bytearray()
        self.read_from_file(file)
        self.name = name

    def read_byte(self, offset: int):
        return self.file[offset]

    def read_bytes(self, offset: int, length: int):
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int):
        self.file[offset] = value

    def write_bytes(self, offset: int, values):
        self.file[offset:offset + len(values)] = values

    def write_to_file(self, file: str):
        with open(file, 'wb') as outfile:
            outfile.write(self.file)

    def read_from_file(self, file: str):
        with open(file, 'rb') as stream:
            self.file = bytearray(stream.read())


class K64PatchExtension(APPatchExtension):
    game = "Kirby 64 - The Crystal Shards"
    
    @staticmethod
    def apply_basepatch(_: APProcedurePatch, rom: bytes):
        return bsdiff4.patch(rom, pkgutil.get_data(__name__, os.path.join("data", "k64_basepatch.bsdiff4")))

    @staticmethod
    def calc_6103_crc(_: APProcedurePatch, rom: bytes):
        return recalculate_6103_crcs(rom)


class K64ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [K64UHASH]
    game = "Kirby 64 - The Crystal Shards"
    patch_file_ending = ".apk64cs"
    result_file_ending = ".z64"
    procedure = [
        ("apply_basepatch", []),
        ("apply_tokens", ["token_data.bin"]),
        ("calc_6103_crc", []),
    ]
    name: bytearray | None= None

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, bytes([value]))

    def write_bytes(self, offset: int, values: Union[List[int], bytes]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(values))


def patch_rom(world: "K64World", player: int, patch: K64ProcedurePatch):
    # now just apply slot data
    # first stage shuffle
    if world.stage_shuffle_enabled:
        for i in range(1, 7):
            stages = [stage_locations[world.player_levels[i][stage]] if stage < len(world.player_levels[i])
                      else (-1, -1) for stage in range(8)]
            patch.write_bytes(level_index + ((i - 1) * 32), struct.pack(">iiiiiiii", *[stage[0] for stage in stages]))
            patch.write_bytes(stage_index + ((i - 1) * 32), struct.pack(">iiiiiiii", *[stage[1] for stage in stages]))
            for j in range(len(world.player_levels[i])):
                for k, addr in enumerate(stage_select_ptrs[default_levels[i][j]]):
                    patch.write_bytes(addr,
                                      struct.pack(">II",
                                                  *(stage_select_vals[world.player_levels[i][j]][(k * 2):(k * 2)+2])))
                for k in range(2):
                    addr = stage_select_param_ptrs[world.player_levels[i][j]][k]
                    value = stage_select_param_vals[default_levels[i][j]]
                    patch.write_bytes(addr, struct.pack(">fff", *value))

    patch.write_bytes(crystal_requirements, world.boss_requirements)

    write_aesthetics(world, patch)

    from Utils import __version__
    patch.name = bytearray(f'K64{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x1FFF200, patch.name)

    patch.write_byte(slot_data, world.options.split_power_combos.value)
    patch.write_byte(slot_data + 1, world.options.death_link.value)
    patch.write_byte(slot_data + 2, world.options.goal_speed.value)
    consumable_val = 0
    if "1-Ups" in world.options.consumables:
        consumable_val |= 1
    if "Food" in world.options.consumables:
        consumable_val |= 2
    if "Stars" in world.options.consumables:
        consumable_val |= 4
    patch.write_byte(slot_data + 3, consumable_val)

    level_counter = 0
    for level in world.player_levels:
        for stage in world.player_levels[level]:
            patch.write_bytes(0x1FFF230 + level_counter, struct.pack(">H", stage & 0xFFFF))
            level_counter += 2

    patch.write_file("token_data.bin", patch.get_token_binary())

def read_n64_rom(path: str) -> bytes:
    with open(path, "rb", buffering=0) as f:
        if path.endswith(".n64"):
            # little endian, byteswap on the half
            byte_data = bytearray(f.read())
            for i in range(0, len(byte_data), 2):
                temp = byte_data[i]
                byte_data[i] = byte_data[i + 1]
                byte_data[i + 1] = temp
            f = BytesIO(byte_data)
        elif path.endswith(".v64"):
            # byteswapped, byteswap on the word
            byte_data = bytearray(f.read())
            for i in range(0, len(byte_data), 4):
                temp = byte_data[i]
                byte_data[i] = byte_data[i + 3]
                byte_data[i + 1] = byte_data[i + 2]
                byte_data[i + 2] = byte_data[i + 1]
                byte_data[i + 3] = temp
            f = BytesIO(byte_data)
        return f.read()

def get_base_rom_bytes() -> bytes:
    rom_file: str = get_base_rom_path()
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        base_rom_bytes = bytes(read_n64_rom(rom_file))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {K64UHASH}:
            raise Exception("Supplied Base Rom does not match known MD5 for US or JP release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = settings.get_settings()
    if not file_name:
        file_name = options["k64_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
