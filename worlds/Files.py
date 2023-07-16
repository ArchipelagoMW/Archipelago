from __future__ import annotations

import json
import struct
import zipfile

from typing import ClassVar, Dict, Tuple, Any, Optional, Union, BinaryIO, List

import bsdiff4


class AutoPatchRegister(type):
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


current_patch_version: int = 5


class AutoPatchExtensionRegister(type):
    patch_types: ClassVar[Dict[str, AutoPatchExtensionRegister]] = {}

    def __new__(mcs, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoPatchExtensionRegister:
        # construct class
        new_class = super().__new__(mcs, name, bases, dct)
        if "game" in dct:
            AutoPatchExtensionRegister.patch_types[dct["game"]] = new_class
        return new_class

    @staticmethod
    def get_handler(game: str) -> Optional[AutoPatchExtensionRegister]:
        for patch_type, handler in AutoPatchExtensionRegister.patch_types.items():
            if patch_type == game:
                return handler
        return None


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
        with zipfile.ZipFile(zip_file, "w", self.compression_method, True, self.compression_level) \
                as zf:
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
            "compatible_version": 5,
            "version": current_patch_version,
        }


class APDeltaPatch(APContainer, metaclass=AutoPatchRegister):
    """An APContainer that additionally has delta.bsdiff4
    containing a delta patch to get the desired file, often a rom."""

    hash: Optional[str]  # base checksum of source file
    patch_file_ending: str = ""
    delta: Optional[bytes] = None
    result_file_ending: str = ".sfc"
    source_data: bytes

    def __init__(self, *args: Any, patched_path: str = "", **kwargs: Any) -> None:
        self.patched_path = patched_path
        super(APDeltaPatch, self).__init__(*args, **kwargs)

    def get_manifest(self) -> Dict[str, Any]:
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


class APProcedurePatch(APContainer, metaclass=AutoPatchRegister):
    """
    An APContainer that defines a procedure to produce the desired file.
    """
    procedure: List[str]
    tokens: List[Tuple[int, bytes]]
    hash: Optional[str]  # base checksum of source file
    source_data: bytes
    patch_file_ending: str = ""
    result_file_ending: str = ".sfc"
    token_data: Optional[bytes] = None


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
        self.tokens = list()
        super(APProcedurePatch, self).__init__(*args, **kwargs)

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super(APProcedurePatch, self).get_manifest()
        manifest["base_checksum"] = self.hash
        manifest["result_file_ending"] = self.result_file_ending
        manifest["patch_file_ending"] = self.patch_file_ending
        return manifest

    def read_tokens(self) -> None:
        if not self.token_data:
            self.read()
        token_count = struct.unpack("I", self.token_data[0:4])[0]
        bpr = 4
        for _ in range(token_count):
            offset = struct.unpack("I", self.token_data[bpr:bpr+4])[0]
            size = struct.unpack("I", self.token_data[bpr+4:bpr+8])[0]
            data = self.token_data[bpr+8:bpr+8+size]
            self.tokens.append((offset, data))
            bpr += 8 + size

    def write_token(self, offset: int, data: bytes) -> None:
        self.tokens.append((offset,data))  # lazy write these when we go to generate the patch

    def get_token_binary(self) -> bytes:
        data = bytearray()
        data.extend(struct.pack("I", len(self.tokens)))
        for offset, bin_data in self.tokens:
            data.extend(struct.pack("I", offset))
            data.extend(struct.pack("I", len(bin_data)))
            data.extend(bin_data)
        return data

    def process_token_binary(self, data: bytes) -> bytes:
        self.read_tokens()
        data = bytearray(data)
        for offset, token_data in self.tokens:
            data[offset:offset+len(token_data)] = token_data
        return data

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super(APProcedurePatch, self).read_contents(opened_zipfile)
        if "token_data.bin" in opened_zipfile.namelist():
            self.token_data = opened_zipfile.read("token_data.bin")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super(APProcedurePatch, self).write_contents(opened_zipfile)
        if len(self.tokens) > 0:
            opened_zipfile.writestr("token_data.bin", self.get_token_binary())

    def patch(self, target: str):
        base_data = self.get_source_data_with_cache()
        patch_extender = AutoPatchExtensionRegister.get_handler(self.game)
        for step in self.procedure:
            if step == "apply_tokens":
                base_data = self.process_token_binary(base_data)
            elif patch_extender is not None:
                extension = getattr(patch_extender, step, None)
                if extension is not None:
                    base_data = extension(base_data)
                else:
                    raise NotImplementedError(f"Unknown procedure {step} for {self.game}.")
            else:
                raise NotImplementedError(f"Unknown procedure {step} for {self.game}.")
        with open(target, 'wb') as f:
            f.write(base_data)


class APPatchExtension(metaclass=AutoPatchExtensionRegister):
    game: str

