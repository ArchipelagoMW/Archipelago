import Utils
from worlds.Files import APDeltaPatch
from settings import get_settings

import hashlib
import os
import math

USHASH = 'acbb3a2e4a8f865f363dc06df147afa2'


class SOTNDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Symphony of the Night"
    patch_file_ending = ".apsotn"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes() -> bytes:
    with open(get_settings().sotn_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    if USHASH != basemd5.hexdigest():
        raise Exception('Supplied Base Rom does not match known MD5 for SLU067 release. '
                        'Get the correct game and version, then dump it')

    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = get_settings()
    if not file_name:
        file_name = options["sotn_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def write_char(buffer, address: int, value: int):
    # x1 = (value & 0xFF).to_bytes(1, 'little')
    buffer[address] = value


def write_short(buffer, address: int, value: int):
    x1, x2 = (value & 0xFFFF).to_bytes(2, 'little')
    buffer[address] = x1
    buffer[address + 1] = x2


def write_word(buffer, address: int, value):
    x1, x2, x3, x4 = (value & 0xFFFFFFFF).to_bytes(4, 'little')
    buffer[address] = x1
    buffer[address + 1] = x2
    buffer[address + 2] = x3
    buffer[address + 3] = x4
    return address + 4


def write_to_file(buffer, filename=""):
    print(filename)
    if filename == "":
        output_file = get_settings().sotn_settings.rom_file
    else:
        output_file = filename

        cue_file = f'FILE "{filename}" BINARY\n'
        cue_file += f'  TRACK 01 MODE2/2352\n'
        cue_file += f'    INDEX 01 00:00:00\n'
        cue_file += f'FILE "Castlevania - Symphony of the Night (USA) (Track 2).bin" BINARY\n'
        cue_file += f'  TRACK 02 AUDIO\n'
        cue_file += f'    INDEX 00 00:00:00\n'
        cue_file += f'    INDEX 01 00:02:00'

    with open(output_file, 'wb') as outfile:
        outfile.write(buffer)

    """with open("teste.cue", 'wb') as outfile:
        outfile.write(bytes(cue_file, 'utf-8'))"""