from __future__ import annotations

import abc
import json
import zipfile
from enum import IntEnum
import os
import threading
from io import BytesIO

from typing import ClassVar, Dict, List, Literal, Tuple, Any, Optional, Union, BinaryIO, overload, Sequence

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


class AutoPatchExtensionRegister(abc.ABCMeta):
    extension_types: ClassVar[Dict[str, AutoPatchExtensionRegister]] = {}
    required_extensions: Tuple[str, ...] = ()

    def __new__(mcs, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoPatchExtensionRegister:
        # construct class
        new_class = super().__new__(mcs, name, bases, dct)
        if "game" in dct:
            AutoPatchExtensionRegister.extension_types[dct["game"]] = new_class
        return new_class

    @staticmethod
    def get_handler(game: Optional[str]) -> Union[AutoPatchExtensionRegister, List[AutoPatchExtensionRegister]]:
        if not game:
            return APPatchExtension
        handler = AutoPatchExtensionRegister.extension_types.get(game, APPatchExtension)
        if handler.required_extensions:
            handlers = [handler]
            for required in handler.required_extensions:
                ext = AutoPatchExtensionRegister.extension_types.get(required)
                if not ext:
                    raise NotImplementedError(f"No handler for {required}.")
                handlers.append(ext)
            return handlers
        else:
            return handler


container_version: int = 6


def is_ap_player_container(game: str, data: bytes, player: int):
    if not zipfile.is_zipfile(BytesIO(data)):
        return False
    with zipfile.ZipFile(BytesIO(data), mode='r') as zf:
        if "archipelago.json" in zf.namelist():
            manifest = json.loads(zf.read("archipelago.json"))
            if "game" in manifest and "player" in manifest:
                if game == manifest["game"] and player == manifest["player"]:
                    return True
    return False


class InvalidDataError(Exception):
    """
    Since games can override `read_contents` in APContainer,
    this is to report problems in that process.
    """


class APContainer:
    """A zipfile containing at least archipelago.json, which contains a manifest json payload."""
    version: ClassVar[int] = container_version
    compression_level: ClassVar[int] = 9
    compression_method: ClassVar[int] = zipfile.ZIP_DEFLATED

    path: Optional[str]

    def __init__(self, path: Optional[str] = None):
        self.path = path

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
            try:
                self.read_contents(zf)
            except Exception as e:
                message = ""
                if len(e.args):
                    arg0 = e.args[0]
                    if isinstance(arg0, str):
                        message = f"{arg0} - "
                raise InvalidDataError(f"{message}This might be the incorrect world version for this file") from e

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        with opened_zipfile.open("archipelago.json", "r") as f:
            manifest = json.load(f)
        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new "
                            f"for this handler (version: {self.version})")
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
        return {
            # minimum version of patch system expected for patching to be successful
            "compatible_version": 5,
            "version": container_version,
        }


class APPlayerContainer(APContainer):
    """A zipfile containing at least archipelago.json meant for a player"""
    game: ClassVar[Optional[str]] = None
    patch_file_ending: str = ""

    player: Optional[int]
    player_name: str
    server: str

    def __init__(self, path: Optional[str] = None, player: Optional[int] = None,
                 player_name: str = "", server: str = ""):
        super().__init__(path)
        self.player = player
        self.player_name = player_name
        self.server = server

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        self.player = manifest["player"]
        self.server = manifest["server"]
        self.player_name = manifest["player_name"]
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        manifest.update({
            "server": self.server,  # allow immediate connection to server in multiworld. Empty string otherwise
            "player": self.player,
            "player_name": self.player_name,
            "game": self.game,
            "patch_file_ending": self.patch_file_ending,
        })
        return manifest


class APPatch(APPlayerContainer):
    """
    An `APPlayerContainer` that represents a patch file.
    It includes the `procedure` key in the manifest to indicate that it is a patch.

    Your implementation should inherit from this if your output file
    represents a patch file, but will not be applied with AP's `Patch.py`
    """
    procedure: Union[Literal["custom"], List[Tuple[str, List[Any]]]] = "custom"

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super(APPatch, self).get_manifest()
        manifest["procedure"] = self.procedure
        manifest["compatible_version"] = 6
        return manifest


class APAutoPatchInterface(APPatch, abc.ABC, metaclass=AutoPatchRegister):
    """
    An abstract `APPatch` that defines the requirements for a patch
    to be applied with AP's `Patch.py`
    """
    result_file_ending: str = ".sfc"

    @abc.abstractmethod
    def patch(self, target: str) -> None:
        """ create the output file with the file name `target` """


class APProcedurePatch(APAutoPatchInterface):
    """
    An APPatch that defines a procedure to produce the desired file.
    """
    hash: Optional[str]  # base checksum of source file
    source_data: bytes
    files: Dict[str, bytes]

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
        self.files = {}

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super(APProcedurePatch, self).get_manifest()
        manifest["base_checksum"] = self.hash
        manifest["result_file_ending"] = self.result_file_ending
        manifest["procedure"] = self.procedure
        if self.procedure == APDeltaPatch.procedure:
            manifest["compatible_version"] = 5
        return manifest

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super(APProcedurePatch, self).read_contents(opened_zipfile)
        with opened_zipfile.open("archipelago.json", "r") as f:
            manifest = json.load(f)
        if "procedure" not in manifest:
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
        assert not isinstance(self.procedure, str), f"{type(self)} must define procedures"
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

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
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
    _tokens: Sequence[
        Tuple[APTokenTypes, int, Union[
            bytes,  # WRITE
            Tuple[int, int],  # COPY, RLE
            int  # AND_8, OR_8, XOR_8
        ]]] = ()

    def get_token_binary(self) -> bytes:
        """
        Returns the token binary created from stored tokens.
        :return: A bytes object representing the token data.
        """
        data = bytearray()
        data.extend(len(self._tokens).to_bytes(4, "little"))
        for token_type, offset, args in self._tokens:
            data.append(token_type)
            data.extend(offset.to_bytes(4, "little"))
            if token_type in [APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8]:
                assert isinstance(args, int), f"Arguments to AND/OR/XOR must be of type int, not {type(args)}"
                data.extend(int.to_bytes(1, 4, "little"))
                data.append(args)
            elif token_type in [APTokenTypes.COPY, APTokenTypes.RLE]:
                assert isinstance(args, tuple), f"Arguments to COPY/RLE must be of type tuple, not {type(args)}"
                data.extend(int.to_bytes(8, 4, "little"))
                data.extend(args[0].to_bytes(4, "little"))
                data.extend(args[1].to_bytes(4, "little"))
            elif token_type == APTokenTypes.WRITE:
                assert isinstance(args, bytes), f"Arguments to WRITE must be of type bytes, not {type(args)}"
                data.extend(len(args).to_bytes(4, "little"))
                data.extend(args)
            else:
                raise ValueError(f"Unknown token type {token_type}")
        return bytes(data)

    @overload
    def write_token(self,
                    token_type: Literal[APTokenTypes.AND_8, APTokenTypes.OR_8, APTokenTypes.XOR_8],
                    offset: int,
                    data: int) -> None:
        ...

    @overload
    def write_token(self,
                    token_type: Literal[APTokenTypes.COPY, APTokenTypes.RLE],
                    offset: int,
                    data: Tuple[int, int]) -> None:
        ...

    @overload
    def write_token(self,
                    token_type: Literal[APTokenTypes.WRITE],
                    offset: int,
                    data: bytes) -> None:
        ...

    def write_token(self, token_type: APTokenTypes, offset: int, data: Union[bytes, Tuple[int, int], int]) -> None:
        """
        Stores a token to be used by patching.
        """
        if not isinstance(self._tokens, list):
            assert len(self._tokens) == 0, f"{type(self)}._tokens was tampered with."
            self._tokens = []
        self._tokens.append((token_type, offset, data))


class APPatchExtension(metaclass=AutoPatchExtensionRegister):
    """Class that defines patch extension functions for a given game.
    Patch extension functions must have the following two arguments in the following order:

    caller: APProcedurePatch (used to retrieve files from the patch container)

    rom: bytes (the data to patch)

    Further arguments are passed in from the procedure as defined.

    Patch extension functions must return the changed bytes.
    """
    game: str
    required_extensions: ClassVar[Tuple[str, ...]] = ()

    @staticmethod
    def apply_bsdiff4(caller: APProcedurePatch, rom: bytes, patch: str) -> bytes:
        """Applies the given bsdiff4 from the patch onto the current file."""
        return bsdiff4.patch(rom, caller.get_file(patch))

    @staticmethod
    def apply_tokens(caller: APProcedurePatch, rom: bytes, token_file: str) -> bytes:
        """Applies the given token file from the patch onto the current file."""
        token_data = caller.get_file(token_file)
        rom_data = bytearray(rom)
        token_count = int.from_bytes(token_data[0:4], "little")
        bpr = 4
        for _ in range(token_count):
            token_type = token_data[bpr:bpr + 1][0]
            offset = int.from_bytes(token_data[bpr + 1:bpr + 5], "little")
            size = int.from_bytes(token_data[bpr + 5:bpr + 9], "little")
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
                length = int.from_bytes(data[:4], "little")
                value = int.from_bytes(data[4:], "little")
                if token_type == APTokenTypes.COPY:
                    rom_data[offset: offset + length] = rom_data[value: value + length]
                else:
                    rom_data[offset: offset + length] = bytes([value] * length)
            else:
                rom_data[offset:offset + len(data)] = data
            bpr += 9 + size
        return bytes(rom_data)

    @staticmethod
    def calc_snes_crc(caller: APProcedurePatch, rom: bytes) -> bytes:
        """Calculates and applies a valid CRC for the SNES rom header."""
        rom_data = bytearray(rom)
        if len(rom) < 0x8000:
            raise Exception("Tried to calculate SNES CRC on file too small to be a SNES ROM.")
        crc = (sum(rom_data[:0x7FDC] + rom_data[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        rom_data[0x7FDC:0x7FE0] = [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF]
        return bytes(rom_data)
