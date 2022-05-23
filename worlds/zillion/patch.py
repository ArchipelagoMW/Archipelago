import bsdiff4  # type: ignore
import yaml
from typing import Any, BinaryIO, Dict, Optional, cast
import Utils
from Patch import APDeltaPatch
import os

# TODO: most of this file is just copied from another game and not implemented for Zillion yet

USHASH = ''


class ZillionDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Zillion"
    patch_file_ending = ".apzl"

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


def generate_yaml(patch: bytes, metadata: Optional[Dict[str, Any]] = None) -> bytes:
    """Generate old (<4) apbp format yaml"""
    patch_yaml = yaml.dump({
        "meta": metadata,
        "patch": patch,
        "game": "Zillion",
        # minimum version of patch system expected for patching to be successful
        "compatible_version": 1,
        "version": 2,
        "base_checksum": USHASH
    })
    return cast(bytes, patch_yaml.encode(encoding="utf-8-sig"))


def generate_patch(vanilla_file: str, randomized_file: str, metadata: Optional[Dict[str, Any]] = None) -> bytes:
    """Generate old (<4) apbp format patch data. Run through lzma to get a complete apbp file."""
    with open(vanilla_file, "rb") as f:
        vanilla = read_rom(f)
    with open(randomized_file, "rb") as f:
        randomized = read_rom(f)
    if metadata is None:
        metadata = {}
    patch = bsdiff4.diff(vanilla, randomized)  # type: ignore
    return generate_yaml(patch, metadata)
