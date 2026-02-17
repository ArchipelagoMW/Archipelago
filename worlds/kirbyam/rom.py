"""ROM patch support for Kirby & The Amazing Mirror.

At this stage, patching is kept minimal: we only produce a valid AP procedure
patch file so the world can generate. Full ROM integration (writing the auth
token, location tables, incoming item queue, etc.) should be added once
addresses.json contains the required ROM symbols and the injected base patch is
Kirby-specific.
"""

import os
from typing import TYPE_CHECKING

from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .data import data

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

    patch.write_file("token_data.bin", patch.get_token_binary())
