from ..constants import game_data as gd
from .constants.reserved_space import ReservedConstantsMF
from .data import get_data_path
from ..patching import BpsDecoder, IpsDecoder
from ..rom import Rom
import os
import pkgutil


def _get_patch_path(rom: Rom, subfolder: str, filename: str) -> str:
    dir = f"{rom.game.name}_{rom.region.name}".lower()
    return get_data_path("patches", dir, subfolder, filename)


def _internal_apply_ips_patch(rom: Rom, patch_name: str, subfolder: str) -> None:
    path = _get_patch_path(rom, subfolder, patch_name)
    patch = pkgutil.get_data("", path)
    IpsDecoder().apply_patch(patch, rom.data)


def apply_patch_in_data_path(rom: Rom, patch_name: str) -> None:
    path = os.path.join("data", "patches", "mf_u", patch_name)
    patch = pkgutil.get_data(__name__, path)
    IpsDecoder().apply_patch(patch, rom.data)
    #_internal_apply_ips_patch(rom, patch_name, "")


def apply_patch_in_asm_path(rom: Rom, patch_name: str) -> None:
    path = os.path.join("data", "patches", "mf_u", "asm", patch_name)
    patch = pkgutil.get_data(__name__, path)
    IpsDecoder().apply_patch(patch, rom.data)
    #_internal_apply_ips_patch(rom, patch_name, "asm")


def apply_base_patch(rom: Rom) -> None:
    path = os.path.join("data", "patches", "mf_u", "asm", "m4rs.bps")
    patch = pkgutil.get_data(__name__, path)
    rom.data = BpsDecoder().apply_patch(patch, rom.data)


def disable_demos(rom: Rom) -> None:
    # b 0x8087460
    rom.write_16(0x87436, 0xE013)


def skip_door_transitions(rom: Rom) -> None:
    rom.write_32(0x69500, 0x3000BDE)
    rom.write_8(0x694E2, 0xC)


def stereo_default(rom: Rom) -> None:
    rom.write_8(rom.read_ptr(ReservedConstantsMF.DEFAULT_STEREO_FLAG_POINTER_ADDR), 1)


def disable_sounds(rom: Rom, start: int, end: int, exclude: set[int] = set()) -> None:
    sound_data_addr = gd.sound_data_entries(rom)
    for idx in range(start, end):
        if idx not in exclude:
            addr = sound_data_addr + idx * 8
            rom.write_8(rom.read_ptr(addr), 0)


def disable_music(rom: Rom) -> None:
    # Exclude jingles
    exclude = {
        16,  # Major obtained
        17,  # Loading save
        20,  # Minor obtained
        59,  # Event
    }
    disable_sounds(rom, 0, 100, exclude)


def disable_sound_effects(rom: Rom) -> None:
    disable_sounds(rom, 100, gd.sound_count(rom))


def change_missile_limit(rom: Rom, limit: int) -> None:
    rom.write_8(rom.read_ptr(ReservedConstantsMF.MISSILE_LIMIT_ADDR), limit)


def apply_unexplored_map(rom: Rom) -> None:
    apply_patch_in_asm_path(rom, "unhidden_map.ips")


def apply_pbs_without_bombs(rom: Rom) -> None:
    apply_patch_in_asm_path(rom, "bombless_pbs.ips")


def apply_reveal_hidden_tiles(rom: Rom) -> None:
    rom.write_8(rom.read_ptr(ReservedConstantsMF.REVEAL_HIDDEN_TILES_ADDR), 1)


def apply_reveal_unexplored_doors(rom: Rom) -> None:
    apply_patch_in_asm_path(rom, "unhidden_map_doors.ips")


def apply_accessibility_patch(rom: Rom) -> None:
    apply_patch_in_asm_path(rom, "accessibility.ips")
