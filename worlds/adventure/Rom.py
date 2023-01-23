import hashlib
import os
from typing import Optional

import Utils
from Utils import OptionsType
from worlds.Files import APDeltaPatch

import bsdiff4

ADVENTUREHASH: str = "157bddb7192754a45372be196797f284"


class AdventureDeltaPatch(APDeltaPatch):
    hash = ADVENTUREHASH
    game = "Adventure"
    patch_file_ending = ".apadvn"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def apply_basepatch(base_rom_bytes: bytes) -> bytes:
    with open(os.path.join(os.path.dirname(__file__), "adventure_basepatch.bsdiff4"), "rb") as basepatch:
        delta: bytes = basepatch.read()
    return bsdiff4.patch(base_rom_bytes, delta)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    file_name = get_base_rom_path(file_name)
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())
    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    if ADVENTUREHASH != basemd5.hexdigest():
        raise Exception(f"Supplied Base Rom does not match known MD5 for Adventure. "
                        "Get the correct game and version, then dump it")
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["adventure_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
