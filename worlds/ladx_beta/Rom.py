import worlds.Files
import hashlib
import Utils
import os
import json
import pkgutil
import bsdiff4
import binascii
from typing import TYPE_CHECKING
from Options import OptionError
from .Common import *
from .LADXR import generator
from .LADXR.main import get_parser

LADX_HASH = "07c211479386825042efb4ad31bb525f"

if TYPE_CHECKING:
    from . import LinksAwakeningWorld

class LADXPatchExtensions(worlds.Files.APPatchExtension):
    game = LINKS_AWAKENING

    @staticmethod
    def generate_rom(caller: worlds.Files.APProcedurePatch, rom: bytes, data_file: str) -> bytes:
        patch_data = json.loads(caller.get_file(data_file).decode("utf-8"))
        apply_overrides(patch_data)
        rom_name = get_base_rom_path()
        out_name = f"{patch_data['out_base']}{caller.result_file_ending}"
        parser = get_parser()
        args = parser.parse_args([rom_name, "-o", out_name, "--dump"])
        return generator.generateRom(rom, args, patch_data)

    @staticmethod
    def patch_title_screen(caller: worlds.Files.APProcedurePatch, rom: bytes, data_file: str) -> bytes:
        patch_data = json.loads(caller.get_file(data_file).decode("utf-8"))
        apply_overrides(patch_data)
        if patch_data["ladxr_settings_dict"]["aptitlescreen"] == 'true':
            return bsdiff4.patch(rom, pkgutil.get_data(__name__, "LADXR/patches/title_screen.bdiff4"))
        return rom

class LADXProcedurePatch(worlds.Files.APProcedurePatch):
    hash = LADX_HASH
    game = LINKS_AWAKENING
    patch_file_ending: str = ".apladxb"
    result_file_ending: str = ".gbc"

    procedure = [
        ("generate_rom", ["data.json"]),
        ("patch_title_screen", ["data.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def write_patch_data(world: "LinksAwakeningWorld", patch: LADXProcedurePatch):
    data_dict = {
        "generated_world_version": world.world_version.as_simple_string(),
        "out_base": world.multiworld.get_out_file_name_base(patch.player),
        "is_race": world.multiworld.is_race,
        "seed": world.multiworld.seed,
        "seed_name": world.multiworld.seed_name,
        "multi_key": binascii.hexlify(world.multi_key).decode(),
        "player": patch.player,
        "player_name": patch.player_name,
        "other_player_names": list(world.multiworld.player_name.values()),
        "rom_item_placements": world.rom_item_placements,
        "hint_texts": {
            k: (v["text"] if v is not None else None)
            for k, v in world.ladx_in_game_hints.items()
        },
        "world_setup": {
            "goal": world.ladxr_logic.world_setup.goal,
            "multichest": world.ladxr_logic.world_setup.multichest,
            "entrance_mapping": world.ladxr_logic.world_setup.entrance_mapping,
            "boss_mapping": world.ladxr_logic.world_setup.boss_mapping,
            "miniboss_mapping": world.ladxr_logic.world_setup.miniboss_mapping,
        },
        "ladxr_settings_dict": world.ladxr_settings_dict,
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
    from . import LinksAwakeningWorld
    if not file_name:
        file_name = LinksAwakeningWorld.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def apply_overrides(patch_data: dict) -> None:
    from . import LinksAwakeningWorld
    option_overrides = getattr(LinksAwakeningWorld.settings, "option_overrides", None)
    if not option_overrides:
        return
    wrapped_overrides = {
        "game": LINKS_AWAKENING,
        LINKS_AWAKENING: option_overrides,
    }
    from Generate import roll_settings
    try:
        rolled_settings = roll_settings(wrapped_overrides)
    except OptionError:
        logger = logging.getLogger("Link's Awakening Logger")
        logger.warning("Failed to apply option overrides, check that they are formatted correctly.")
        return

    overridable_options = {
        "gfxmod",
        "link_palette",
        "music",
        "music_change_condition",
        "palette",
        "ap_title_screen",
        "boots_controls",
        "nag_messages",
        "text_shuffle",
        "low_hp_beep",
        "text_mode",
        "no_flash",
        "quickswap",
    }
    if not patch_data["is_race"]:
        overridable_options.update([
            "trendy_game",
            "warps",
        ])
    for option_name in option_overrides.keys():
        if (option_name not in patch_data["options"]) or (option_name not in overridable_options):
            continue
        patch_data["options"][option_name] = getattr(rolled_settings, option_name).value

