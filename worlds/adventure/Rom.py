import hashlib
import os
import zipfile
from typing import Optional, Any

import Utils
from .Locations import AdventureLocation
from Utils import OptionsType
from worlds.Files import APDeltaPatch
from itertools import chain

import bsdiff4

ADVENTUREHASH: str = "157bddb7192754a45372be196797f284"


class AdventureAutoCollectLocation:
    short_location_id: int = 0
    room_id: int = 0

    def __init__(self, short_location_id: int, room_id: int):
        self.short_location_id = short_location_id
        self.room_id = room_id

    def get_dict(self):
        return {
            "short_location_id": self.short_location_id,
            "room_id": self.room_id,
        }


class AdventureForeignItemInfo:
    short_location_id: int = 0
    room_id: int = 0
    room_x: int = 0
    room_y: int = 0

    def __init__(self, short_location_id: int, room_id: int, room_x: int, room_y: int):
        self.short_location_id = short_location_id
        self.room_id = room_id
        self.room_x = room_x
        self.room_y = room_y

    def get_dict(self):
        return {
            "short_location_id": self.short_location_id,
            "room_id": self.room_id,
            "room_x": self.room_x,
            "room_y": self.room_y,
        }


class AdventureDeltaPatch(APDeltaPatch):
    hash = ADVENTUREHASH
    game = "Adventure"
    patch_file_ending = ".apadvn"
    foreign_items: [AdventureForeignItemInfo] = None
    autocollect_items: [AdventureAutoCollectLocation] = None
    patched_rom_sha256: str = None
    seedName: bytes = None

    def __init__(self, *args: Any, locations: [], autocollect: [], seed_name: bytes, **kwargs: Any) -> None:
        self.foreign_items = [AdventureForeignItemInfo(loc.short_location_id, loc.room_id, loc.room_x, loc.room_y)
                              for loc in locations]
        self.autocollect_items = autocollect
        self.seedName = seed_name
        super(AdventureDeltaPatch, self).__init__(*args, **kwargs)
        with open(self.patched_path, "rb") as file:
            patched_rom_bytes = bytes(file.read())
            patchedsha256 = hashlib.sha256()
            patchedsha256.update(patched_rom_bytes)
            self.patched_rom_sha256 = patchedsha256.hexdigest()

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        super(AdventureDeltaPatch, self).write_contents(opened_zipfile)
        # write Delta
        if self.foreign_items is not None:
            loc_bytes = []
            for foreign_item in self.foreign_items:
                loc_bytes.append(foreign_item.short_location_id)
                loc_bytes.append(foreign_item.room_id)
                loc_bytes.append(foreign_item.room_x)
                loc_bytes.append(foreign_item.room_y)
            opened_zipfile.writestr("adventure_locations",
                                    bytes(loc_bytes),
                                    compress_type=zipfile.ZIP_LZMA)
        if self.autocollect_items is not None:
            loc_bytes = []
            for item in self.autocollect_items:
                loc_bytes.append(item.short_location_id)
                loc_bytes.append(item.room_id)
            opened_zipfile.writestr("adventure_autocollect",
                                    bytes(loc_bytes),
                                    compress_type=zipfile.ZIP_LZMA)
        if self.patched_rom_sha256 is not None:
            opened_zipfile.writestr("hash",
                                    bytes(self.patched_rom_sha256, encoding='ascii'),
                                    compress_type=zipfile.ZIP_STORED)
        if self.player_name is not None:
            opened_zipfile.writestr("player",
                                    self.player_name,  # UTF-8
                                    compress_type=zipfile.ZIP_STORED)
        if self.seedName is not None:
            opened_zipfile.writestr("seedName",
                                    self.seedName,
                                    compress_type=zipfile.ZIP_STORED)

    def read_contents(self, opened_zipfile: zipfile.ZipFile):
        super(AdventureDeltaPatch, self).read_contents(opened_zipfile)
        self.foreign_items = AdventureDeltaPatch.read_foreign_items(opened_zipfile)
        self.autocollect_items = AdventureDeltaPatch.read_autocollect_items(opened_zipfile)


    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    @classmethod
    def read_rom_info(cls, opened_zipfile: zipfile.ZipFile) -> (bytes, bytes, str):
        hashbytes: bytes = opened_zipfile.read("hash")
        seedbytes: bytes = opened_zipfile.read("seedName")
        namebytes: bytes = opened_zipfile.read("player")
        namestr: str = namebytes.decode("utf-8")
        return hashbytes, seedbytes, namestr


    @classmethod
    def read_foreign_items(cls, opened_zipfile: zipfile.ZipFile) -> [AdventureForeignItemInfo]:
        foreign_items = []
        readbytes: bytes = opened_zipfile.read("adventure_locations")
        bytelist = list(readbytes)
        for i in range(round(len(bytelist)/4)):
            offset = i * 4
            foreign_items.append(AdventureForeignItemInfo(bytelist[offset],
                                                          bytelist[offset + 1],
                                                          bytelist[offset + 2],
                                                          bytelist[offset + 3]))
        return foreign_items

    @classmethod
    def read_autocollect_items(cls, opened_zipfile: zipfile.ZipFile) -> [AdventureForeignItemInfo]:
        autocollect_items = []
        readbytes: bytes = opened_zipfile.read("adventure_autocollect")
        bytelist = list(readbytes)
        for i in range(round(len(bytelist)/2)):
            offset = i * 2
            autocollect_items.append(AdventureAutoCollectLocation(bytelist[offset], bytelist[offset + 1]))
        return autocollect_items


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
