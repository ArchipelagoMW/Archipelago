from typing import BinaryIO, Optional, cast
import Utils
from worlds.Files import APDeltaPatch
import os

USHASH = 'd4bf9e7bcf9a48da53785d2ae7bc4270'


class ZillionDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Zillion"
    patch_file_ending = ".apzl"
    result_file_ending = ".sms"

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_base_rom_path(), "rb") as stream:
            return read_rom(stream)


def get_base_rom_path(file_name: Optional[str] = None) -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = cast(str, options["zillion_options"]["rom_file"])
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def read_rom(stream: BinaryIO) -> bytes:
    """ reads rom into bytearray """
    data = stream.read()
    # I'm not aware of any sms header.
    return data
