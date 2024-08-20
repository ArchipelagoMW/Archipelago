import hashlib
import os
from typing import Optional

import Utils
from settings import get_settings
from worlds.Files import APDeltaPatch

L2USHASH: str = "6efc477d6203ed2b3b9133c1cd9e9c5d"


class L2ACDeltaPatch(APDeltaPatch):
    hash = L2USHASH
    game = "Lufia II Ancient Cave"
    patch_file_ending = ".apl2ac"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_path: str = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_path, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if L2USHASH != basemd5.hexdigest():
            raise Exception("Supplied Base Rom does not match known MD5 for US release. "
                            "Get the correct game and version, then dump it")
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        file_name = get_settings()["lufia2ac_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
