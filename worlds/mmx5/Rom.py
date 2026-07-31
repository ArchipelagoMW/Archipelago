"""AP patch container for Mega Man X5 (PS1, NTSC-U SLUS-01334).

Follows the MMX4 apworld's shape (APProcedurePatch producing a .bin + .cue)
with one deliberate improvement: no external xdelta executable and no
separate basepatch file. The edit list is tiny and lives in disc.py, so
apply_basepatch() patches the vanilla image in pure Python - including the
MANDATORY per-sector EDC/ECC regeneration (emulator disc layers error-correct
un-reparitied edits back to vanilla).

Per-seed data rides inside the .apmmx5 as a JSON file ("seed_edits.json")
rather than APTokenMixin tokens: raw token pokes would bypass parity
regeneration, so every write must funnel through disc.apply_basepatch().
"""
import hashlib
import json
import logging
import os
from typing import TYPE_CHECKING

import settings
import Utils
from worlds.Files import APPatchExtension, APProcedurePatch

from . import disc

if TYPE_CHECKING:
    from . import MMX5World

logger = logging.getLogger()

# MD5 of the raw 2352-byte NTSC-U image (SLUS-01334) this patch was developed
# against. Extend the set if other verified dumps (e.g. Redump variants that
# differ only in pregap handling) surface during testing.
HASH_US = "09e670f6e666211b7fcdbb7d48b716e1"


class MMX5PatchExtension(APPatchExtension):
    game = "Mega Man X5"

    @staticmethod
    def apply_basepatch(caller: APProcedurePatch, rom: bytes) -> bytes:
        extra = []
        try:
            seed_edits = json.loads(caller.get_file("seed_edits.json").decode("utf-8"))
            for entry in seed_edits:
                extra.append((entry["addr"], bytes.fromhex(entry["hex"]), entry["region"]))
        except KeyError:
            pass  # no per-seed edits in this patch
        return disc.apply_basepatch(rom, extra)


class MMX5ProcedurePatch(APProcedurePatch):
    hash = [HASH_US]
    game = "Mega Man X5"
    patch_file_ending = ".apmmx5"
    result_file_ending = ".cue"
    procedure = [
        ("apply_basepatch", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def patch(self, target: str) -> None:
        file_name = target[:-4]
        if os.path.exists(file_name + ".bin") and os.path.exists(file_name + ".cue"):
            logger.info("Patched ROM + CUE already exist!")
            return

        super().patch(target)
        os.rename(target, file_name + ".bin")

        rom_name = os.path.basename(file_name)
        cue = (f'FILE "{rom_name}.bin" BINARY\n'
               f'  TRACK 01 MODE2/2352\n'
               f'    INDEX 01 00:00:00\n')
        with open(file_name + ".cue", "w", newline="\n") as f:
            f.write(cue)


def patch_rom(world: "MMX5World", patch: MMX5ProcedurePatch) -> None:
    """Collect per-seed edits. The scaffold ships none - option-driven edits
    (countdown behavior, launch determinism, seed/slot stamp once a canary-
    validated free-space home exists) land here as {addr, hex, region} rows."""
    seed_edits: list = []
    patch.write_file("seed_edits.json", json.dumps(seed_edits).encode("utf-8"))


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        md5 = hashlib.md5()
        md5.update(base_rom_bytes)
        if md5.hexdigest() not in {HASH_US}:
            raise Exception("Supplied base disc image does not match the known "
                            "MD5 for the US (SLUS-01334) release. Verify your dump "
                            "(raw 2352-byte .bin, single data track).")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["mmx5_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
