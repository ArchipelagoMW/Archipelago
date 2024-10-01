import os
from typing import BinaryIO, Optional

import Utils
from worlds.Files import APDeltaPatch


USHASH = '6e9c94511d04fac6e0a1e582c170be3a'


class SoEDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Secret of Evermore"
    patch_file_ending = ".apsoe"

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_base_rom_path(), "rb") as stream:
            return read_rom(stream)


def get_base_rom_path(file_name: Optional[str] = None) -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["soe_options"]["rom_file"]
    if not file_name:
        raise ValueError("Missing soe_options -> rom_file from host.yaml")
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def read_rom(stream: BinaryIO, strip_header: bool = True) -> bytes:
    """Reads rom into bytearray and optionally strips off any smc header"""
    data = stream.read()
    if strip_header and len(data) % 0x400 == 0x200:
        return data[0x200:]
    return data


if __name__ == '__main__':
    import sys
    print('Please use ../../patch.py', file=sys.stderr)
    sys.exit(1)
