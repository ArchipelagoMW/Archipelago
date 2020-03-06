import bsdiff4
import yaml
import os
import lzma
import hashlib
import logging

import Utils
from Rom import JAP10HASH, read_rom

base_rom_bytes = None


def get_base_rom_bytes() -> bytes:
    global base_rom_bytes
    if not base_rom_bytes:
        with open("host.yaml") as f:
            options = Utils.parse_yaml(f.read())
        file_name = options["general_options"]["rom_file"]
        base_rom_bytes = bytes(read_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if JAP10HASH != basemd5.hexdigest():
            logging.warning('Supplied Base Rom does not match known MD5 for JAP(1.0) release.'
                            ' Will try to patch anyway.')
    return base_rom_bytes


def generate_patch(rom: bytes, metadata=None) -> bytes:
    if metadata is None:
        metadata = {}
    patch = bsdiff4.diff(get_base_rom_bytes(), rom)
    patch = yaml.dump({"meta": metadata,
                       "patch": patch})
    return patch.encode()


def create_patch_file(rom_file_to_patch: str, server: str = "") -> str:
    bytes = generate_patch(load_bytes(rom_file_to_patch),
                           {
                               "server": server})  # allow immediate connection to server in multiworld. Empty string otherwise
    target = os.path.splitext(rom_file_to_patch)[0] + ".bmbp"
    write_lzma(bytes, target)
    return target


def create_rom_file(patch_file) -> dict:
    data = Utils.parse_yaml(lzma.decompress(load_bytes(patch_file)).decode("utf-8-sig"))
    patched_data = bsdiff4.patch(get_base_rom_bytes(), data["patch"])
    with open(os.path.splitext(patch_file)[0] + ".sfc", "wb") as f:
        f.write(patched_data)
    return data["meta"]


def load_bytes(path: str):
    with open(path, "rb") as f:
        return f.read()


def write_lzma(data: bytes, path: str):
    with lzma.LZMAFile(path, 'wb') as f:
        f.write(data)
