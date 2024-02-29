from __future__ import annotations

import abc
import json
import struct
import zipfile
from enum import IntEnum
import os
import threading

from typing import ClassVar, Dict, Tuple, Any, Optional, Union, BinaryIO, List

import bsdiff4

semaphore = threading.Semaphore(os.cpu_count() or 4)

del threading
del os


class AutoPatchRegister(abc.ABCMeta):
    patch_types: ClassVar[Dict[str, AutoPatchRegister]] = {}
    file_endings: ClassVar[Dict[str, AutoPatchRegister]] = {}

    def __new__(mcs, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoPatchRegister:
        # construct class
        new_class = super().__new__(mcs, name, bases, dct)
        if "game" in dct:
            AutoPatchRegister.patch_types[dct["game"]] = new_class
            if not dct["patch_file_ending"]:
                raise Exception(f"Need an expected file ending for {name}")
            AutoPatchRegister.file_endings[dct["patch_file_ending"]] = new_class
        return new_class

    @staticmethod
    def get_handler(file: str) -> Optional[AutoPatchRegister]:
        for file_ending, handler in AutoPatchRegister.file_endings.items():
            if file.endswith(file_ending):
                return handler
        return None


current_patch_version: int = 6


class AutoPatchExtensionRegister(type):
    extension_types: ClassVar[Dict[str, AutoPatchExtensionRegister]] = {}
    required_extensions: List[str] = []

    def __new__(mcs, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoPatchExtensionRegister:
        # construct class
        new_class = super().__new__(mcs, name, bases, dct)
        if "game" in dct:
            AutoPatchExtensionRegister.extension_types[dct["game"]] = new_class
        return new_class

    @staticmethod
    def get_handler(game: str) -> Union[AutoPatchExtensionRegister, List[AutoPatchExtensionRegister]]:
        if game in AutoPatchExtensionRegister.extension_types:
            handler = AutoPatchExtensionRegister.extension_types.get(game)
            if handler.required_extensions:
                handlers = [handler]
                for required in handler.required_extensions:
                    if required in AutoPatchExtensionRegister.extension_types:
                        handlers.append(AutoPatchExtensionRegister.extension_types.get(required))
                    else:
                        raise NotImplementedError(f"No handler for {required}.")
                return handlers
            else:
                return handler
        return APPatchExtension


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

    def write(self, file: Optional[Union[str, BinaryIO]] = None) -> None:
        zip_file = file if file else self.path
        if not zip_file:
            raise FileNotFoundError(f"Cannot write {self.__class__.__name__} due to no path provided.")
        with semaphore:  # TODO: remove semaphore once generate_output has a thread limit
            with zipfile.ZipFile(
                    zip_file, "w", self.compression_method, True, self.compression_level) as zf:
                if file:
                    self.path = zf.filename
                self.write_contents(zf)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        manifest = self.get_manifest()
        try:
            manifest_str = json.dumps(manifest)
        except Exception as e:
            raise Exception(f"Manifest {manifest} did not convert to json.") from e
        else:
            opened_zipfile.writestr("archipelago.json", manifest_str)

    def read(self, file: Optional[Union[str, BinaryIO]] = None) -> None:
        """Read data into patch object. file can be file-like, such as an outer zip file's stream."""
        zip_file = file if file else self.path
        if not zip_file:
            raise FileNotFoundError(f"Cannot read {self.__class__.__name__} due to no path provided.")
        with zipfile.ZipFile(zip_file, "r") as zf:
            if file:
                self.path = zf.filename
            self.read_contents(zf)

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        with opened_zipfile.open("archipelago.json", "r") as f:
            manifest = json.load(f)
        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new "
                            f"for this handler (version: {self.version})")
        self.player = manifest["player"]
        self.server = manifest["server"]
        self.player_name = manifest["player_name"]

    def get_manifest(self) -> Dict[str, Any]:
        return {
            "server": self.server,  # allow immediate connection to server in multiworld. Empty string otherwise
            "player": self.player,
            "player_name": self.player_name,
            "game": self.game,
            # minimum version of patch system expected for patching to be successful
            "compatible_version": 6,
            "version": current_patch_version,
        }


class APPatch(APContainer, abc.ABC, metaclass=AutoPatchRegister):
    """
    An abstract `APContainer` that defines the requirements for an object
    to be used by the `Patch.create_rom_file` function.
    """
    result_file_ending: str = ".sfc"

    @abc.abstractmethod
    def patch(self, target: str) -> None:
        """ create the output file with the file name `target` """


class APProcedurePatch(APPatch):
    """
    An APPatch that defines a procedure to produce the desired file.
    """
    procedure: List[Tuple[str, List[Any]]]
    hash: Optional[str]  # base checksum of source file
    source_data: bytes
    patch_file_ending: str = ""
    files: Dict[str, bytes] = {}

    @classmethod
    def get_source_data(cls) -> bytes:
        """Get Base data"""
        raise NotImplementedError()

    @classmethod
    def get_source_data_with_cache(cls) -> bytes:
        if not hasattr(cls, "source_data"):
            cls.source_data = cls.get_source_data()
        return cls.source_data

    def __init__(self, *args: Any, **kwargs: Any):
        super(APProcedurePatch, self).__init__(*args, **kwargs)

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super(APProcedurePatch, self).get_manifest()
        manifest["base_checksum"] = self.hash
        manifest["result_file_ending"] = self.result_file_ending
        manifest["patch_file_ending"] = self.patch_file_ending
        manifest["procedure"] = self.procedure
        return manifest

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super(APProcedurePatch, self).read_contents(opened_zipfile)
        with opened_zipfile.open("archipelago.json", "r") as f:
            manifest = json.load(f)
        if manifest["version"] < 6:
            # support patching files made before moving to procedures
            self.procedure = [("apply_bsdiff4", ["delta.bsdiff4"])]
        else:
            self.procedure = manifest["procedure"]
        for file in opened_zipfile.namelist():
            if file not in ["archipelago.json"]:
                self.files[file] = opened_zipfile.read(file)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super(APProcedurePatch, self).write_contents(opened_zipfile)
        for file in self.files:
            opened_zipfile.writestr(file, self.files[file],
                                    compress_type=zipfile.ZIP_STORED if file.endswith(".bsdiff4") else None)

    def get_file(self, file: str) -> bytes:
        """ Retrieves a file from the patch container."""
        if file not in self.files:
            self.read()
        return self.files[file]

    def write_file(self, file_name: str, file: bytes) -> None:
        """ Writes a file to the patch container, to be retrieved upon patching. """
        self.files[file_name] = file

    def patch(self, target: str) -> None:
        self.read()
        base_data = self.get_source_data_with_cache()
        patch_extender = AutoPatchExtensionRegister.get_handler(self.game)
        for step, args in self.procedure:
            if isinstance(patch_extender, list):
                extension = next((item for item in [getattr(extender, step, None) for extender in patch_extender]
                                  if item is not None), None)
            else:
                extension = getattr(patch_extender, step, None)
            if extension is not None:
                base_data = extension(self, base_data, *args)
            else:
                raise NotImplementedError(f"Unknown procedure {step} for {self.game}.")
        with open(target, 'wb') as f:
            f.write(base_data)


class APDeltaPatch(APProcedurePatch):
    """An APProcedurePatch that additionally has delta.bsdiff4
    containing a delta patch to get the desired file, often a rom."""

    procedure = [
        ("apply_bsdiff4", ["delta.bsdiff4"])
    ]

    def __init__(self, *args: Any, patched_path: str = "", **kwargs: Any) -> None:
        super(APDeltaPatch, self).__init__(*args, **kwargs)
        self.patched_path = patched_path

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        self.write_file("delta.bsdiff4",
                        bsdiff4.diff(self.get_source_data_with_cache(), open(self.patched_path, "rb").read()))
        super(APDeltaPatch, self).write_contents(opened_zipfile)


class APTokenTypes(IntEnum):
    WRITE = 0
    COPY = 1
    RLE = 2
    AND_8 = 3
    OR_8 = 4
    XOR_8 = 5


class APTokenMixin:
    """
    A class that defines functions for generating a token binary, for use in patches.
    """
    tokens: List[
        Tuple[int, int,
              Union[
                    bytes,  # WRITE
                    Tuple[int, int],  # COPY, RLE
                    int  # AND_8, OR_8, XOR_8
              ]]] = []

    def get_token_binary(self) -> bytes:
        """
        Returns the token binary created from stored tokens.
        :return: A bytes object representing the token data.
        """
        data = bytearray()
        data.extend(struct.pack("I", len(self.tokens)))
        for token_type, offset, args in self.tokens:
            data.append(token_type)
            data.extend(struct.pack("I", offset))
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                data.extend(struct.pack("I", 1))
                data.append(args)
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                data.extend(struct.pack("I", 8))
                data.extend(struct.pack("I", args[0]))
                data.extend(struct.pack("I", args[1]))
            else:
                data.extend(struct.pack("I", len(args)))
                data.extend(args)
        return data

    def write_token(self, token_type: APTokenTypes, offset: int, data: Union[bytes, Tuple[int, int], int]):
        """
        Stores a token to be used by patching.
        """
        self.tokens.append((token_type, offset, data))


class APPatchExtension(metaclass=AutoPatchExtensionRegister):
    """Class that defines patch extension functions for a given game.
    Patch extension functions must have the following two arguments in the following order:

    caller: APProcedurePatch (used to retrieve files from the patch container)

    rom: bytes (the data to patch)

    Further arguments are passed in from the procedure as defined.

    Patch extension functions must return the changed bytes.
    """
    game: str
    required_extensions: List[str] = []

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str):
        """Applies the given bsdiff4 from the patch onto the current file."""
        return bsdiff4.patch(rom, caller.get_file(patch))

    @staticmethod
    def apply_tokens(caller: APProcedurePatch, rom: bytes, token_file: str) -> bytes:
        """Applies the given token file from the patch onto the current file."""
        token_data = caller.get_file(token_file)
        rom_data = bytearray(rom)
        token_count = struct.unpack("I", token_data[0:4])[0]
        bpr = 4
        for _ in range(token_count):
            token_type = token_data[bpr:bpr + 1][0]
            offset = struct.unpack("I", token_data[bpr + 1:bpr + 5])[0]
            size = struct.unpack("I", token_data[bpr + 5:bpr + 9])[0]
            data = token_data[bpr + 9:bpr + 9 + size]
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                arg = data[0]
                if token_type == APTokenTypes.AND_8:
                    rom_data[offset] = rom_data[offset] & arg
                elif token_type == APTokenTypes.OR_8:
                    rom_data[offset] = rom_data[offset] | arg
                else:
                    rom_data[offset] = rom_data[offset] ^ arg
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                args = struct.unpack("II", data)
                length = args[0]
                value = args[1]
                if token_type == APTokenTypes.COPY:
                    rom_data[offset: offset + length] = rom_data[value: value + length]
                else:
                    rom_data[offset: offset + length] = bytes([value] * length)
            else:
                rom_data[offset:offset + len(data)] = data
            bpr += 9 + size
        return rom_data

    @staticmethod
    def calc_snes_crc(caller: APProcedurePatch, rom: bytes):
        """Calculates and applies a valid CRC for the SNES rom header."""
        rom_data = bytearray(rom)
        if len(rom) < 0x8000:
            raise Exception("Tried to calculate SNES CRC on file too small to be a SNES ROM.")
        crc = (sum(rom_data[:0x7FDC] + rom_data[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        rom_data[0x7FDC:0x7FE0] = [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF]
        return rom_data

