import hashlib
import os
import math

import bsdiff4
import Utils
from BaseClasses import ItemClassification
from Utils import read_snes_rom
from worlds.AutoWorld import World
from worlds.Files import APDeltaPatch
from .Names import Addresses, ItemID
from .Items import SoulBlazerItem, SoulBlazerItemData
from .Locations import SoulBlazerLocation, LocationType, SoulBlazerLocationData

USHASH = "83CF41D53A1B94AEEA1A645037A24004"


class LocalRom(object):
    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        # self.orig_buffer = None

        with open(file, "rb") as stream:
            self.buffer = read_snes_rom(stream)
        if patch:
            self.apply_basepatch()
        #     self.orig_buffer = self.buffer.copy()
        # if vanillaRom:
        #    with open(vanillaRom, 'rb') as vanillaStream:
        #        self.orig_buffer = read_snes_rom(vanillaStream)

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = 1 << bit_number
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress : startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress : startaddress + len(values)] = values

    def write_to_file(self, file):
        with open(file, "wb") as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, "rb") as stream:
            self.buffer = bytearray(stream.read())

    def apply_basepatch(self):
        with open(os.path.join(os.path.dirname(__file__), "patches", "basepatch.bsdiff4"), "rb") as basepatch:
            delta: bytes = basepatch.read()
        buffer = bsdiff4.patch(self.buffer, delta)

    def apply_patch(self, name: str):
        with open(os.path.join(os.path.dirname(__file__), "patches", name), "rb") as basepatch:
            delta: bytes = basepatch.read()
        buffer = bsdiff4.patch(self.buffer, delta)

    def place_lair(self, index: int, id, operand):
        pass

    def place_chest(self, index, id, operand):
        pass

    def place_npcreward(self, index, id, operand):
        pass

    place_dict: dict[LocationType:function] = {
        LocationType.CHEST: place_chest,
        LocationType.LAIR: place_lair,
        LocationType.NPC_REWARD: place_npcreward,
    }

    def place(self, location: SoulBlazerLocation):
        location_data = location.data
        if location.item.player == location.player:
            item: SoulBlazerItem = location.item
            LocalRom.place_dict[location_data.type](location_data.id, item.id, item.operand_for_id)
        else:
            #TODO: Better handling of remote items item and player name stored in ROM somewhere.
            #Or let the client communicate when something was sent?
            LocalRom.place_dict[location_data.type](
                location_data.id,
                ItemID.REMOTE_ITEM,
                1 if location.item.classification == ItemClassification.progression else 0,
            )
        pass


def patch_rom(world: World, rom: LocalRom, active_level_list):
    # TODO: this
    pass


class SoulBlazerDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Soul Blazer"
    patch_file_ending = ".apsb"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception(
                "Supplied Base Rom does not match known MD5 for US release. "
                "Get the correct game and version, then dump it"
            )
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_settings()
    if not file_name:
        file_name = options["soulblazer_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
