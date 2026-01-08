# The primary distinction between this file and `fe8py` is that this file is
# primarily concerned with interfacing the FE8 world with Archipelago, whereas
# `fe8py` makes semantic changes to the game itself (meaning the core
# randomization, stat tweaks, etc).

import json
from random import Random
from typing import TYPE_CHECKING

from worlds.Files import (
    APTokenMixin,
    APTokenTypes,
    APProcedurePatch,
    APPatchExtension,
)
from settings import get_settings

from .items import FE8Item
from .locations import FE8Location
from .constants import FE8_NAME, ROM_BASE_ADDRESS
from .options import FE8Options
from .connector_config import (
    SLOT_NAME_ADDR,
    SUPER_DEMON_KING_OFFS,
    LOCKPICK_USABILITY_OFFS,
    DEATH_LINK_KIND_OFFS,
    LOCATION_INFO_OFFS,
    LOCATION_INFO_SIZE,
)
from .fe8py import FE8Randomizer

if TYPE_CHECKING:
    from . import FE8World

SLOT_NAME_OFFS = SLOT_NAME_ADDR - ROM_BASE_ADDRESS

BASE_PATCH = "data/base_patch.bsdiff4"
PATCH_FILE_EXT = ".apfe8"

AP_ITEM_KIND = 1
SELF_ITEM_KIND = 2


class FE8PatchExtension(APPatchExtension):
    game = FE8_NAME

    @staticmethod
    def apply_gameplay_changes(caller: APProcedurePatch, rom: bytes) -> bytes:
        config = json.loads(caller.get_file("config.json").decode("UTF-8"))
        random = Random(config["seed"] + config["player"])
        mut_rom = bytearray(rom)
        randomizer = FE8Randomizer(rom=mut_rom, random=random, config=config)
        randomizer.apply_base_changes()

        if config["shuffle_skirmish_tables"]:
            randomizer.randomize_monster_gen()

        if config["easier_5x"]:
            randomizer.apply_5x_buffs()

        if config["unbreakable_regalia"]:
            randomizer.apply_infinite_holy_weapons()

        if config["normalize_genders"]:
            randomizer.normalize_genders()

        randomizer.randomize_growths(*config["growth_rando"])
        randomizer.randomize_music(config["music_rando"])

        return bytes(mut_rom)


class FE8ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = FE8_NAME
    hash = "005531fef9efbb642095fb8f64645236"
    patch_file_ending = PATCH_FILE_EXT
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
        ("apply_gameplay_changes", []),
    ]

    # CR-someday cam: Should we implement size checks?
    def write_byte(self, offs: int, val: int):
        self.write_token(APTokenTypes.WRITE, offs, bytes([val]))

    def write_bytes_le(self, offs: int, val: int, size: int):
        data = bytes((val >> 8 * i) & 0xFF for i in range(size))
        self.write_token(APTokenTypes.WRITE, offs, data)

    def write_short_le(self, addr: int, val: int):
        self.write_bytes_le(addr, val, 2)

    @classmethod
    def get_source_data(cls):
        return get_base_rom_as_bytes()


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().fe8_settings.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


def rom_location(loc: FE8Location):
    return LOCATION_INFO_OFFS + loc.local_address * LOCATION_INFO_SIZE


def write_tokens(world: "FE8World", patch: FE8ProcedurePatch):
    player = world.player
    multiworld = world.multiworld
    options: FE8Options = world.options
    config_dict = {
        "player_rando": bool(options.player_unit_rando),
        "player_monster": bool(options.player_unit_monsters),
        "easier_5x": bool(options.easier_5x),
        "unbreakable_regalia": bool(options.unbreakable_regalia),
        "shuffle_skirmish_tables": bool(options.shuffle_skirmish_tables),
        "normalize_genders": bool(options.normalize_genders),
        "growth_rando": (
            int(options.growth_rando),
            int(options.growth_rando_min),
            int(options.growth_rando_max),
        ),
        "music_rando": int(options.music_rando),
        "seed": multiworld.seed,
        "player": player,
    }
    patch.write_file("config.json", json.dumps(config_dict).encode("UTF-8"))

    # Player name
    player_name = multiworld.player_name[player]
    name_bytes = player_name.encode("utf-8")
    if len(name_bytes) > 63:
        raise Exception(f"FE8: Player name {player_name} is too long (max 63 bytes)")

    patch.write_token(APTokenTypes.WRITE, SLOT_NAME_OFFS, name_bytes)

    for location in multiworld.get_locations(player):
        assert isinstance(location, FE8Location)
        rom_loc = rom_location(location)
        if location.item and location.item.player == player:
            assert isinstance(location.item, FE8Item)
            patch.write_short_le(rom_loc, SELF_ITEM_KIND)
            patch.write_short_le(rom_loc + 2, location.item.local_code)
        else:
            patch.write_short_le(rom_loc, AP_ITEM_KIND)

    patch.write_byte(SUPER_DEMON_KING_OFFS, int(bool(options.super_demon_king)))
    patch.write_byte(LOCKPICK_USABILITY_OFFS, int(options.lockpick_usability))
    patch.write_byte(DEATH_LINK_KIND_OFFS, int(options.death_link))

    patch.write_file("token_data.bin", patch.get_token_binary())
