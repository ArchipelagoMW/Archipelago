import hashlib
import os
import math
import pkgutil
import bsdiff4
import struct
import Utils
from typing import Callable, Dict, TYPE_CHECKING
from BaseClasses import ItemClassification
from Utils import read_snes_rom
from worlds.AutoWorld import World
from worlds.Files import APDeltaPatch
from .Names import Addresses, ItemID
from .Items import SoulBlazerItem, SoulBlazerItemData
from .Locations import SoulBlazerLocation, LocationType, SoulBlazerLocationData
from .patches import get_patch_bytes

if TYPE_CHECKING:
    from . import SoulBlazerWorld

USHASH = "83cf41d53a1b94aeea1a645037a24004"

equipment_power_vanilla = [1, 2, 3, 4, 5, 8, 10, 12]
equipment_power_improved = [1, 3, 5, 7, 9, 12, 12, 12]
equipment_power_strong = [2, 4, 6, 9, 12, 12, 12, 12]
equipment_power_weak = [1, 1, 2, 2, 3, 4, 5, 6]
equipment_power_broken = [1, 1, 1, 1, 1, 1, 1, 1]

# Level requirements are stored as 2-byte SNES BCD - Their hex representation is interpreted as decimal.
sword_level_requirements = [0x01, 0x05, 0x11, 0x15, 0x16, 0x19, 0x22, 0x24]


class LocalRom(object):
    def __init__(self, file, patch=True, vanillaRom=None, name: bytes = None, hash=None):
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
        basepatch = get_patch_bytes("basepatch")
        self.buffer = bytearray(bsdiff4.patch(bytes(self.buffer), basepatch))

    def apply_patch(self, name: str):
        patch = get_patch_bytes(name)
        self.buffer = bytearray(bsdiff4.patch(bytes(self.buffer), patch))

    def place_lair(self, index: int, id: int, operand: int):
        # Compute address of our lair entry
        lair_addr = Addresses.LAIR_DATA + 0x18 + (0x20 * index)
        self.write_bytes(lair_addr, [id, *operand.to_bytes(2, "little")])

    def place_chest(self, index: int, id: int, operand: int):
        # Pull chest address from table
        for chest_addr in Addresses.CHEST_ADDRESSES[index]:
            self.write_bytes(chest_addr + 0x03, [id, *operand.to_bytes(2, "little")])

    def place_npcreward(self, index: int, id: int, operand: int):
        npcreward_addr = Addresses.NPC_REWARD_DATA + (0x04 * index)
        self.write_bytes(npcreward_addr, [id, 0x00, *operand.to_bytes(2, "little")])

    place_dict: Dict[LocationType, Callable] = {
        LocationType.CHEST: place_chest,
        LocationType.LAIR: place_lair,
        LocationType.NPC_REWARD: place_npcreward,
    }

    def place(self, location: SoulBlazerLocation):
        if location.address == None:
            return
        location_data = location.data
        if location.item.player == location.player:
            item: SoulBlazerItem = location.item
            LocalRom.place_dict[location_data.type](self, location_data.id, item.id, item.operand_for_id)
        else:
            # TODO: Better handling of remote items item and player name stored in ROM somewhere.
            # Or let the client populate info in RAM?
            LocalRom.place_dict[location_data.type](
                self,
                location_data.id,
                ItemID.REMOTE_ITEM,
                1 if location.item.classification == ItemClassification.progression else 0,
            )


def patch_rom(world: "SoulBlazerWorld", rom: LocalRom):
    if world.options.equipment_stats == "semi_progressive":
        rom.apply_patch("semiprogressive")

    # Determine stat pool to use
    equipment_power_lookup = {
        "Vanilla": equipment_power_vanilla,
        "Improved": equipment_power_improved,
        "Strong": equipment_power_strong,
        "Weak": equipment_power_weak,
        "Broken": equipment_power_broken,
    }
    stats = [*equipment_power_lookup[world.options.equipment_scaling.current_option_name]]
    
    # The indexes into our stat pool which could potentially be shuffled
    indicies_wep = list(range(len(stats)))
    indicies_arm = list(range(len(stats)))
    # Shuffle which sword/arm gets which stats
    # Shuffling the index ensures that the same level requirement is needed for a given weapon power
    if world.options.equipment_stats == "shuffle":
        world.random.shuffle(indicies_wep)
        world.random.shuffle(indicies_arm)
    # Write stats to ROM
    for i in range(len(stats)):
        rom.write_byte(Addresses.WEAPON_STRENGTH_DATA + i, stats[indicies_wep[i]])
        rom.write_byte(Addresses.ARMOR_DEFENSE_DATA + i, stats[indicies_arm[i]])
        # Semi-progressive sets all sword level requirements to 1.
        if world.options.equipment_stats != "semi_progressive":
            # Weapon level requirements are stored as 2-byte values even if they only use 1 byte.
            rom.write_byte(Addresses.WEAPON_REQUIRED_LEVEL_DATA + (2*i), sword_level_requirements[indicies_wep[i]])
        
    rom.write_byte(Addresses.TEXT_SPEED, world.options.text_speed.value)
    rom.write_byte(Addresses.STONES_REQUIRED, world.options.stones_count.value)
    rom.write_byte(Addresses.ACT_PROGRESSION, world.options.act_progression.value)
    rom.write_byte(Addresses.OPEN_DEATHTOLL, world.options.open_deathtoll.value)

    rom.write_bytes(Addresses.SNES_ROMNAME_START, rom.name)

    for location in world.multiworld.get_locations(world.player):
        rom.place(location)


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
