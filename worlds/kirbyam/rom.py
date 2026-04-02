"""ROM patch support for Kirby & The Amazing Mirror.

The world emits AP procedure patches that apply:
- the shipped KirbyAM base bsdiff patch artifact
- per-seed token writes (auth token and selected runtime feature writes)

Issue #338 adds deterministic enemy copy-ability remap token writes for
non-vanilla enemy randomization modes.
"""

import os
from typing import TYPE_CHECKING

from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .data import data
from .enemy_ability_runtime_patch import build_enemy_copy_runtime_patch_writes
from .options import AbilityRandomizationMode

if TYPE_CHECKING:
    from . import KirbyAmWorld


class KirbyAmProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Kirby & The Amazing Mirror"
    hash = "DF5EFE075B35859529EBF82A4D824458" # md5 hash of base USA rom
        # Calculated with PowerShell Command: Get-FileHash "D:\...\Kirby & The Amazing Mirror (USA).gba" -Algorithm MD5
    patch_file_ending = ".apkirbyam"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().kirby_am_settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


def write_tokens(world: "KirbyAmWorld", patch: KirbyAmProcedurePatch) -> None:
    # Only write the auth token if a ROM address has been configured.
    # The injected base patch is expected to reserve 16 bytes for this.
    auth_addr = data.rom_addresses.get("auth_token") or data.rom_addresses.get("gArchipelagoInfo")
    if auth_addr is not None:
        patch.write_token(APTokenTypes.WRITE, auth_addr, world.auth)

    mode = int(world.options.ability_randomization_mode.value)
    policy = getattr(world, "_enemy_copy_ability_policy", None)
    if mode != AbilityRandomizationMode.option_vanilla and not isinstance(policy, dict):
        raise ValueError(
            "enemy_copy_ability_policy must be initialized before writing non-vanilla "
            "enemy copy-ability runtime patch tokens"
        )

    if isinstance(policy, dict):
        ability_writes = build_enemy_copy_runtime_patch_writes(policy)
        for rom_offset, ability_id in sorted(ability_writes.items()):
            patch.write_token(APTokenTypes.WRITE, rom_offset, bytes([ability_id]))

    patch.write_file("token_data.bin", patch.get_token_binary())
