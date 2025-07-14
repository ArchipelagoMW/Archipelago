import settings
import worlds.Files
import hashlib
import Utils
import os
import json
import pkgutil
import bsdiff4
import binascii
import pickle
from typing import TYPE_CHECKING
from .Common import *
from .LADXR import generator
from .LADXR.main import get_parser
from .LADXR.hints import generate_hint_texts
from .LADXR.locations.keyLocation import KeyLocation
LADX_HASH = "07c211479386825042efb4ad31bb525f"

if TYPE_CHECKING:
    from . import LinksAwakeningWorld


class LADXPatchExtensions(worlds.Files.APPatchExtension):
    game = LINKS_AWAKENING

    @staticmethod
    def generate_rom(caller: worlds.Files.APProcedurePatch, rom: bytes, data_file: str) -> bytes:
        patch_data = json.loads(caller.get_file(data_file).decode("utf-8"))
        # TODO local option overrides
        rom_name = get_base_rom_path()
        out_name = f"{patch_data['out_base']}{caller.result_file_ending}"
        parser = get_parser()
        args = parser.parse_args([rom_name, "-o", out_name, "--dump"])
        return generator.generateRom(rom, args, patch_data)

    @staticmethod
    def patch_title_screen(caller: worlds.Files.APProcedurePatch, rom: bytes, data_file: str) -> bytes:
        patch_data = json.loads(caller.get_file(data_file).decode("utf-8"))
        if patch_data["options"]["ap_title_screen"]:
            return bsdiff4.patch(rom, pkgutil.get_data(__name__, "LADXR/patches/title_screen.bdiff4"))
        return rom

class LADXProcedurePatch(worlds.Files.APProcedurePatch):
    hash = LADX_HASH
    game = LINKS_AWAKENING
    patch_file_ending: str = ".apladx"
    result_file_ending: str = ".gbc"

    procedure = [
        ("generate_rom", ["data.json"]),
        ("patch_title_screen", ["data.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def write_patch_data(world: "LinksAwakeningWorld", patch: LADXProcedurePatch):
    item_list = pickle.dumps([item for item in world.ladxr_logic.iteminfo_list if not isinstance(item, KeyLocation)])
    data_dict = {
        "out_base": world.multiworld.get_out_file_name_base(patch.player),
        "is_race": world.multiworld.is_race,
        "seed": world.multiworld.seed,
        "seed_name": world.multiworld.seed_name,
        "multi_key": binascii.hexlify(world.multi_key).decode(),
        "player": patch.player,
        "player_name": patch.player_name,
        "other_player_names": list(world.multiworld.player_name.values()),
        "item_list": binascii.hexlify(item_list).decode(),
        "hint_texts": generate_hint_texts(world),
        "world_setup": {
            "goal": world.ladxr_logic.world_setup.goal,
            "bingo_goals": world.ladxr_logic.world_setup.bingo_goals,
            "multichest": world.ladxr_logic.world_setup.multichest,
            "entrance_mapping": world.ladxr_logic.world_setup.entrance_mapping,
            "boss_mapping": world.ladxr_logic.world_setup.boss_mapping,
            "miniboss_mapping": world.ladxr_logic.world_setup.miniboss_mapping,
        },
        "options": world.options.as_dict(
            "tradequest",
            "rooster",
            "experimental_dungeon_shuffle",
            "experimental_entrance_shuffle",
            "goal",
            "instrument_count",
            "link_palette",
            "warps",
            "trendy_game",
            "gfxmod",
            "palette",
            "text_shuffle",
            "shuffle_nightmare_keys",
            "shuffle_small_keys",
            "music",
            "music_change_condition",
            "nag_messages",
            "ap_title_screen",
            "boots_controls",
            # "stealing",
            "quickswap",
            "hard_mode",
            "low_hp_beep",
            "text_mode",
            "no_flash",
            "overworld",
        ),
    }
    patch.write_file("data.json", json.dumps(data_dict).encode('utf-8'))


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if LADX_HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for USA release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = settings.get_settings()
    if not file_name:
        file_name = options["ladx_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
