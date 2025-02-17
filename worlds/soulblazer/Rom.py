import dataclasses
import hashlib
import os
import math
import pkgutil
import bsdiff4
import struct
import json
import Utils
from typing import Callable, Dict, Optional, TYPE_CHECKING
from BaseClasses import ItemClassification
from Options import PerGameCommonOptions
from Utils import read_snes_rom
from worlds.AutoWorld import World
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from .Names import Addresses, ItemID
from .Items import SoulBlazerItem, SoulBlazerItemData
from .Locations import SoulBlazerLocation, LocationType, SoulBlazerLocationData
from .Options import SoulBlazerOptions, EquipmentStats
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


class RomData:
    def __init__(self, buffer: bytes, name: Optional[bytes] = None):
        self.name = name
        self.buffer = bytearray(buffer)

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

    def get_bytes(self) -> bytes:
        return bytes(self.buffer)

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
            RomData.place_dict[location_data.type](self, location_data.id, item.id, item.operand_for_id)
        else:
            # TODO: Better handling of remote items item and player name stored in ROM somewhere.
            # Or let the client populate info in RAM?
            RomData.place_dict[location_data.type](
                self,
                location_data.id,
                ItemID.REMOTE_ITEM,
                1 if location.item.classification == ItemClassification.progression else 0,
            )


class SoulBlazerPatchExtensions(APPatchExtension):
    game = "Soul Blazer"

    @staticmethod
    def apply_patches(caller: APProcedurePatch, rom: bytes, options_file: str) -> bytes:
        rom_data = RomData(rom)
        options = json.loads(caller.get_file(options_file).decode("utf-8"))

        rom_data.apply_basepatch()

        if options["equipment_stats"] == EquipmentStats.option_semi_progressive:
            rom_data.apply_patch("semiprogressive")

        return rom_data.get_bytes()


class SoulBlazerProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = USHASH
    game = "Soul Blazer"
    patch_file_ending = ".apsb"

    procedure = [
        ("apply_patches", ["options.json"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def place_lair(self, index: int, id: int, operand: int):
        # Compute address of our lair entry
        lair_addr = Addresses.LAIR_DATA + 0x18 + (0x20 * index)
        self.write_token(APTokenTypes.WRITE, lair_addr, bytes([id, *operand.to_bytes(2, "little")]))

    def place_chest(self, index: int, id: int, operand: int):
        # Pull chest address from table
        for chest_addr in Addresses.CHEST_ADDRESSES[index]:
            self.write_token(APTokenTypes.WRITE, chest_addr + 0x03, bytes([id, *operand.to_bytes(2, "little")]))

    def place_npcreward(self, index: int, id: int, operand: int):
        npcreward_addr = Addresses.NPC_REWARD_DATA + (0x04 * index)
        self.write_token(APTokenTypes.WRITE, npcreward_addr, bytes([id, 0x00, *operand.to_bytes(2, "little")]))

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
            SoulBlazerProcedurePatch.place_dict[location_data.type](
                self, location_data.id, item.id, item.operand_for_id
            )
        else:
            # TODO: Better handling of remote items item and player name stored in ROM somewhere.
            # Or let the client populate info in RAM?
            SoulBlazerProcedurePatch.place_dict[location_data.type](
                self,
                location_data.id,
                ItemID.REMOTE_ITEM,
                1 if location.item.classification == ItemClassification.progression else 0,
            )


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


def write_patch(world: "SoulBlazerWorld", patch: SoulBlazerProcedurePatch) -> None:
    # TODO: Add bsdiff patches to patch file?

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
        patch.write_token(
            APTokenTypes.WRITE, Addresses.WEAPON_STRENGTH_DATA + i, stats[indicies_wep[i]].to_bytes(1, "little")
        )
        patch.write_token(
            APTokenTypes.WRITE, Addresses.ARMOR_DEFENSE_DATA + i, stats[indicies_arm[i]].to_bytes(1, "little")
        )

        # Semi-progressive sets all sword level requirements to 1.
        if world.options.equipment_stats != "semi_progressive":
            # Weapon level requirements are stored as 2-byte values even if they only use 1 byte.
            patch.write_token(
                APTokenTypes.WRITE,
                Addresses.WEAPON_REQUIRED_LEVEL_DATA + (2 * i),
                sword_level_requirements[indicies_wep[i]],
            )

    patch.write_token(APTokenTypes.WRITE, Addresses.TEXT_SPEED, world.options.text_speed.value.to_bytes(1, "little"))
    patch.write_token(
        APTokenTypes.WRITE, Addresses.STONES_REQUIRED, world.options.stones_count.value.to_bytes(1, "little")
    )
    patch.write_token(
        APTokenTypes.WRITE, Addresses.ACT_PROGRESSION, world.options.act_progression.value.to_bytes(1, "little")
    )
    patch.write_token(
        APTokenTypes.WRITE, Addresses.OPEN_DEATHTOLL, world.options.open_deathtoll.value.to_bytes(1, "little")
    )

    patch.write_token(APTokenTypes.WRITE, Addresses.SNES_ROMNAME_START, world.rom_name)

    for location in world.multiworld.get_locations(world.player):
        patch.place(location)

    # end TODO

    patch.write_file("token_data.bin", patch.get_token_binary())

    # Write slot options to a JSON.
    options_dict = {
        option_name: getattr(world.options, option_name).value
        for option_name in (
            attr.name
            for attr in dataclasses.fields(SoulBlazerOptions)
            if attr not in dataclasses.fields(PerGameCommonOptions)
        )
    }

    patch.write_file("options.json", json.dumps(options_dict).encode("utf-8"))
