import bsdiff4
import yaml
from typing import Optional
import Utils
from Patch import APDeltaPatch
import os


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
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def read_rom(stream, strip_header=True) -> bytes:
    """Reads rom into bytearray and optionally strips off any smc header"""
    data = stream.read()
    if strip_header and len(data) % 0x400 == 0x200:
        return data[0x200:]
    return data


def generate_yaml(patch: bytes, metadata: Optional[dict] = None) -> bytes:
    """Generate old (<4) apbp format yaml"""
    patch = yaml.dump({"meta": metadata,
                       "patch": patch,
                       "game": "Secret of Evermore",
                       # minimum version of patch system expected for patching to be successful
                       "compatible_version": 1,
                       "version": 2,
                       "base_checksum": USHASH})
    return patch.encode(encoding="utf-8-sig")


def generate_patch(vanilla_file, randomized_file, metadata: Optional[dict] = None) -> bytes:
    """Generate old (<4) apbp format patch data. Run through lzma to get a complete apbp file."""
    with open(vanilla_file, "rb") as f:
        vanilla = read_rom(f)
    with open(randomized_file, "rb") as f:
        randomized = read_rom(f)
    if metadata is None:
        metadata = {}
    patch = bsdiff4.diff(vanilla, randomized)
    return generate_yaml(patch, metadata)


if __name__ == '__main__':
    import sys
    print('Please use ../../Patch.py', file=sys.stderr)
    sys.exit(1)
