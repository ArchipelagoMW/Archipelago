from __future__ import annotations

import json
import os
import sys
import zipfile
from typing import Tuple, Optional, Dict, Any, Union, BinaryIO


import ModuleUpdate
ModuleUpdate.update()

import bsdiff4

current_patch_version: int = 5


class AutoPatchRegister(type):
    patch_types: Dict[str, APDeltaPatch] = {}
    file_endings: Dict[str, APDeltaPatch] = {}

    def __new__(cls, name: str, bases, dct: Dict[str, Any]):
        # construct class
        new_class = super().__new__(cls, name, bases, dct)
        if "game" in dct:
            AutoPatchRegister.patch_types[dct["game"]] = new_class
            if not dct["patch_file_ending"]:
                raise Exception(f"Need an expected file ending for {name}")
            AutoPatchRegister.file_endings[dct["patch_file_ending"]] = new_class
        return new_class

    @staticmethod
    def get_handler(file: str) -> Optional[type(APDeltaPatch)]:
        for file_ending, handler in AutoPatchRegister.file_endings.items():
            if file.endswith(file_ending):
                return handler


class APContainer:
    """A zipfile containing at least archipelago.json"""
    version: int = current_patch_version
    compression_level: int = 9
    compression_method: int = zipfile.ZIP_DEFLATED
    game: Optional[str] = None

    # instance attributes:
    path: Optional[str]
    player: Optional[int]
    player_name: str
    server: str

    def __init__(self, path: Optional[str] = None, player: Optional[int] = None,
                 player_name: str = "", server: str = ""):
        self.path = path
        self.player = player
        self.player_name = player_name
        self.server = server

    def write(self, file: Optional[Union[str, BinaryIO]] = None):
        if not self.path and not file:
            raise FileNotFoundError(f"Cannot write {self.__class__.__name__} due to no path provided.")
        with zipfile.ZipFile(file if file else self.path, "w", self.compression_method, True, self.compression_level) \
                as zf:
            if file:
                self.path = zf.filename
            self.write_contents(zf)

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        manifest = self.get_manifest()
        try:
            manifest = json.dumps(manifest)
        except Exception as e:
            raise Exception(f"Manifest {manifest} did not convert to json.") from e
        else:
            opened_zipfile.writestr("archipelago.json", manifest)

    def read(self, file: Optional[Union[str, BinaryIO]] = None):
        """Read data into patch object. file can be file-like, such as an outer zip file's stream."""
        if not self.path and not file:
            raise FileNotFoundError(f"Cannot read {self.__class__.__name__} due to no path provided.")
        with zipfile.ZipFile(file if file else self.path, "r") as zf:
            if file:
                self.path = zf.filename
            self.read_contents(zf)

    def read_contents(self, opened_zipfile: zipfile.ZipFile):
        with opened_zipfile.open("archipelago.json", "r") as f:
            manifest = json.load(f)
        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new "
                            f"for this handler (version: {self.version})")
        self.player = manifest["player"]
        self.server = manifest["server"]
        self.player_name = manifest["player_name"]

    def get_manifest(self) -> dict:
        return {
            "server": self.server,  # allow immediate connection to server in multiworld. Empty string otherwise
            "player": self.player,
            "player_name": self.player_name,
            "game": self.game,
            # minimum version of patch system expected for patching to be successful
            "compatible_version": 4,
            "version": current_patch_version,
        }


class APDeltaPatch(APContainer, metaclass=AutoPatchRegister):
    """An APContainer that additionally has delta.bsdiff4
    containing a delta patch to get the desired file, often a rom."""

    hash = Optional[str]  # base checksum of source file
    patch_file_ending: str = ""
    delta: Optional[bytes] = None
    result_file_ending: str = ".sfc"
    source_data: bytes

    def __init__(self, *args, patched_path: str = "", **kwargs):
        self.patched_path = patched_path
        super(APDeltaPatch, self).__init__(*args, **kwargs)

    def get_manifest(self) -> dict:
        manifest = super(APDeltaPatch, self).get_manifest()
        manifest["base_checksum"] = self.hash
        manifest["result_file_ending"] = self.result_file_ending
        manifest["patch_file_ending"] = self.patch_file_ending
        return manifest

    @classmethod
    def get_source_data(cls) -> bytes:
        """Get Base data"""
        raise NotImplementedError()

    @classmethod
    def get_source_data_with_cache(cls) -> bytes:
        if not hasattr(cls, "source_data"):
            cls.source_data = cls.get_source_data()
        return cls.source_data

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        super(APDeltaPatch, self).write_contents(opened_zipfile)
        # write Delta
        opened_zipfile.writestr("delta.bsdiff4",
                                bsdiff4.diff(self.get_source_data_with_cache(), open(self.patched_path, "rb").read()),
                                compress_type=zipfile.ZIP_STORED)  # bsdiff4 is a format with integrated compression

    def read_contents(self, opened_zipfile: zipfile.ZipFile):
        super(APDeltaPatch, self).read_contents(opened_zipfile)
        self.delta = opened_zipfile.read("delta.bsdiff4")

    def patch(self, target: str):
        """Base + Delta -> Patched"""
        if not self.delta:
            self.read()
        result = bsdiff4.patch(self.get_source_data_with_cache(), self.delta)
        with open(target, "wb") as f:
            f.write(result)


GAME_ALTTP = "A Link to the Past"
GAME_SM = "Super Metroid"
GAME_SOE = "Secret of Evermore"
GAME_SMZ3 = "SMZ3"
GAME_DKC3 = "Donkey Kong Country 3"


def create_rom_file(patch_file: str) -> Tuple[dict, str]:
    auto_handler = AutoPatchRegister.get_handler(patch_file)
    if auto_handler:
        handler: APDeltaPatch = auto_handler(patch_file)
        target = os.path.splitext(patch_file)[0]+handler.result_file_ending
        handler.patch(target)
        return {"server": handler.server,
                "player": handler.player,
                "player_name": handler.player_name}, target
    raise NotImplementedError(f"No Handler for {patch_file} found.")


def read_rom(stream, strip_header=True) -> bytearray:
    """Reads rom into bytearray and optionally strips off any smc header"""
    buffer = bytearray(stream.read())
    if strip_header and len(buffer) % 0x400 == 0x200:
        return buffer[0x200:]
    return buffer


if __name__ == "__main__":
    for file in sys.argv[1:]:
        meta_data, result_file = create_rom_file(file)
        print(f"Patch with meta-data {meta_data} was written to {result_file}")
