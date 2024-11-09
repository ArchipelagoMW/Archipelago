import typing
import Utils
import hashlib
import os
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import DKC2World

from .Names import ItemName
from .Items import item_groups

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

HASH_US = '98458530599b9dff8a7414a7f20b777a'
HASH_US_REV_1 = 'd323e6bb4ccc85fd7b416f58350bc1a2'

STARTING_ID = 0xBF0000

rom_start_inventory = {
    ItemName.carry: 0x3DFF83,
    ItemName.climb: 0x3DFF84,
    ItemName.cling: 0x3DFF85,
    ItemName.cartwheel: 0x3DFF86,
    ItemName.swim: 0x3DFF87,
    ItemName.team_attack: 0x3DFF88,
    ItemName.helicopter_spin: 0x3DFF89,
    ItemName.rambi: 0x3DFF8A,
    ItemName.squawks: 0x3DFF8B,
    ItemName.enguarde: 0x3DFF8C,
    ItemName.squitter: 0x3DFF8D,
    ItemName.rattly: 0x3DFF8E,
    ItemName.clapper: 0x3DFF8F,
    ItemName.glimmer: 0x3DFF90,
    ItemName.skull_kart: 0x3DFF91,
    ItemName.barrel_kannons: 0x3DFF92,
    ItemName.barrel_exclamation: 0x3DFF93,
    ItemName.barrel_kong: 0x3DFF93,
    ItemName.barrel_warp: 0x3DFF94,
    ItemName.barrel_control: 0x3DFF95,
}

unlock_data = {
    STARTING_ID + 0x0001: [0x28, 0x56], # Galleon
    STARTING_ID + 0x0002: [0x29, 0x56], # Cauldron
    STARTING_ID + 0x0003: [0x2A, 0x56], # Quay
    STARTING_ID + 0x0004: [0x2B, 0x56], # Kremland
    STARTING_ID + 0x0005: [0x2C, 0x56], # Gulch
    STARTING_ID + 0x0006: [0x2D, 0x56], # Keep
    STARTING_ID + 0x0007: [0x2E, 0x56], # Flying Krock
    STARTING_ID + 0x000B: [0x30, 0x56], # Lost World (Cauldron)
    STARTING_ID + 0x000C: [0x31, 0x56], # Lost World (Quay)
    STARTING_ID + 0x000D: [0x32, 0x56], # Lost World (C)
    STARTING_ID + 0x000E: [0x33, 0x56], # Lost World (Cauldron)
    STARTING_ID + 0x000F: [0x34, 0x56], # Lost World (Cauldron)
    STARTING_ID + 0x0010: [0x0E, 0x05], # Diddy
    STARTING_ID + 0x0011: [0x0E, 0x05], # Dixie
    STARTING_ID + 0x0012: [0x00, 0x36], # Carry
    STARTING_ID + 0x0013: [0x02, 0x36], # Climb
    STARTING_ID + 0x0014: [0x03, 0x36], # Cling
    STARTING_ID + 0x0015: [0x01, 0x36], # Cartwheel
    STARTING_ID + 0x0016: [0x05, 0x36], # Swim
    STARTING_ID + 0x0017: [0x06, 0x05], # Team Attack
    STARTING_ID + 0x0018: [0x04, 0x36], # Helicopter Spin
    STARTING_ID + 0x0019: [0x07, 0x35], # Rambi
    STARTING_ID + 0x001A: [0x08, 0x35], # Squawks
    STARTING_ID + 0x001B: [0x09, 0x35], # Enaguarde
    STARTING_ID + 0x001C: [0x0A, 0x35], # Squitter
    STARTING_ID + 0x001D: [0x0B, 0x35], # Rattly 
    STARTING_ID + 0x001E: [0x0C, 0x35], # Clapper
    STARTING_ID + 0x001F: [0x0D, 0x35], # Glimmer
    STARTING_ID + 0x0020: [0x0F, 0x4B], # Barrel Kannons
    STARTING_ID + 0x0021: [0x12, 0x4B], # Barrel Exclamation
    STARTING_ID + 0x0022: [0x10, 0x4B], # Barrel Kong
    STARTING_ID + 0x0023: [0x13, 0x4B], # Barrel Warp
    STARTING_ID + 0x0024: [0x11, 0x4B], # Barrel Control 
    STARTING_ID + 0x0025: [0x14, 0x35], # Skull Kart
}

currency_data = {
    STARTING_ID + 0x0008: [0x802F, 0x36], # Lost World Rock
    STARTING_ID + 0x0009: [0x08CE, 0x56], # DK Coin
    STARTING_ID + 0x000A: [0x08CC, 0x36], # Kremkoin
    STARTING_ID + 0x0030: [0x08CA, 0x2D], # Banana Coin
    STARTING_ID + 0x0031: [0x08BE, 0x2C], # 1-Up
}

trap_data = {
    STARTING_ID + 0x0040: [0x40, 0x00], # Freeze Trap
    STARTING_ID + 0x0041: [0x42, 0x00], # Reverse Trap
}


class DKC2PatchExtension(APPatchExtension):
    game = "Donkey Kong Country 2"

    @staticmethod
    def shuffle_levels(caller: APProcedurePatch, rom: bytes) -> bytes:
        unshuffled_rom = bytearray(rom)
        rom = bytearray(rom)
        rom_connections = json.loads(caller.get_file("levels.json").decode("UTF-8"))
        
        from .Levels import level_rom_data, boss_rom_data
        dkc2_level_rom_data = dict(level_rom_data, **boss_rom_data)


        for level, selected_level in rom_connections.items():
            addr = dkc2_level_rom_data[level][0]
            rom[addr] = selected_level[1]

            source_ptr = dkc2_level_rom_data[selected_level[0]][1]
            name_size = unshuffled_rom[source_ptr]
            name = unshuffled_rom[source_ptr + 1:source_ptr + name_size + 2]

            destination_ptr = dkc2_level_rom_data[level][1]
            rom[destination_ptr] = name_size
            rom[destination_ptr + 1:destination_ptr + name_size + 2] = bytearray(name)

        return bytes(rom)

class DKC2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US, HASH_US_REV_1]
    game = "Donkey Kong Country 2"
    patch_file_ending = ".apdkc2"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["dkc2_basepatch.bsdiff4"]),
        ("shuffle_levels", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

def patch_rom(world: "DKC2World", patch: DKC2ProcedurePatch):
    # Edit the ROM header
    from Utils import __version__
    patch.name = bytearray(f'DKC2{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0xFFC0, patch.name)

    # Set goal
    patch.write_byte(0x3DFF81, world.options.goal.value)
    patch.write_byte(0x3DFF82, world.options.lost_world_rocks.value)

    # Set starting lives
    patch.write_byte(0x008FA1, world.options.starting_life_count.value)

    # Write starting inventory
    patch.write_byte(0x3DFF80, world.options.starting_kong.value)

    for item in item_groups["Abilities"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_abilities.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)
    for item in item_groups["Animals"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_animals.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)
    for item in item_groups["Barrels"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_barrels.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)

    # Save shuffled levels data
    patch.write_file("levels.json", json.dumps(world.rom_connections).encode("UTF-8"))

    patch.write_file("token_patch.bin", patch.get_token_binary())

    
def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US, HASH_US_REV_1}:
            raise Exception('Supplied Base Rom does not match known MD5 for US 1.0 or 1.1 release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["dkc2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
