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

# Accepted MD5s for the raw 2352-byte NTSC-U image (SLUS-01334).
#
# REDUMP is the canonical dump and the one players will have. The development
# image differs from it by EXACTLY ONE trailing all-zero 2352-byte sector
# (582,957,312 vs 582,954,960 bytes) - verified 2026-08-02 by trimming that
# sector and reproducing Redump's MD5 byte for byte.
#
# Crucially the padding is at the END, not a leading pregap: 'CD001' sits at
# sector 16 in both, so sector numbering is IDENTICAL and every patch offset
# in disc.py is valid against either image unchanged. Nothing needed rebasing;
# the Redump hash simply has to be accepted. All edits land in sectors
# 23433-24319, nowhere near the tail.
HASH_US_REDUMP = "98c0d278dc4a795a0a7562d950d37cc9"   # Redump, canonical
HASH_US_PADDED = "09e670f6e666211b7fcdbb7d48b716e1"   # dev image, +1 zero sector
ACCEPTED_HASHES = {HASH_US_REDUMP, HASH_US_PADDED}
HASH_US = HASH_US_REDUMP   # kept for callers importing the old name


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
    hash = sorted(ACCEPTED_HASHES)
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


# REMOVED 2026-08-04 - do not re-add: the story-chapter shuttle threshold.
#
# 0x800EEFBC held `addiu v0, zero, 6`, the kill count at which the chapter
# ladder advances to the shuttle era, and all_mavericks used to raise it to 8.
# It was disassembled correctly, mapped correctly, and verified live to move
# the chapter transition from 6 kills to 8 - and it still did NOT gate the
# endgame, because the ladder never controlled access in the first place. The
# Enigma/Shuttle menu entries are always present, the shuttle appears once the
# Enigma has been used, and a player at 6 kills reached Zero Space on a disc
# carrying this edit.
#
# All it actually did was delay the story announcement and Dynamo (who is tied
# to chapter 4) by two Mavericks, so it was dropped.
#
# The real gate is ACT 0x800D1C79 >= 5, handled by the client - see
# ENDGAME_ACT in client.py. Full account in mmx5-ram-notes.md.


# Text skip. Both sites are in the message STATE MACHINE in the static EXE -
# NOT the render loop. Four attempts at the render loop failed (one killed the
# advance button, one broke the box display entirely); the working layer is the
# one the game's own Y/advance handling uses. Full account, including the dead
# ends and why each failed, in mmx5-ram-notes.md "Text control".
#
#   0x80023D48  beqz $v1, 0x80023d54   guards `sb $zero, 0xf($s0)` - zeroing
#                                      that flag is exactly what Y does, so
#                                      NOPping the guard completes every box
#   0x80023D84  beqz $v1, 0x80024138   guards the end-of-box "return unless a
#                                      button is down" wait
#
# Both read the pad word 0x800C9320 (bit 0x10 = confirm, live-verified).
# Choice prompts are NOT affected - tested live: Alia's DNA reward prompt
# pauses and waits, and the Enigma/Shuttle launch is a stage-select menu that
# never routes through here.
TEXT_INSTANT_ADDR = 0x80023D48
TEXT_INSTANT_VANILLA = bytes.fromhex("02006010")   # beqz $v1, +2
TEXT_ADVANCE_ADDR = 0x80023D84
TEXT_ADVANCE_VANILLA = bytes.fromhex("ec006010")   # beqz $v1, +0xEC
TEXT_NOP = bytes(4)
TEXT_REGION = "SLUS exe"


# Launch resolution roll (launch overlay, disassembled from the disc):
#   0x800FA0C8  jal  0x8002df78     RNG
#   0x800FA0D0  sra  $v0, $v0, 2
#   0x800FA0D4  andi $v1, $v0, 0xf  roll = (rand>>2) & 0xF -> 0..15
#   0x800FA0D8  slti $v0, $s0, 0x51 s0 = score, then a band ladder:
#     <=0 never | 0x01-0x14 roll==0 6.25% | 0x15-0x28 roll<2 12.5%
#     | 0x29-0x3C roll<6 37.5% | 0x3D-0x50 roll<12 75% | >=0x51 roll<15 93.75%
#
# BASE_EDITS replaces the andi with `li $v1,0` so the roll is always 0 and
# success reduces to score > 0. Under `vanilla` launch odds we put the andi
# BACK - seed edits are applied after BASE_EDITS into the same image, so this
# restore wins - and the client then writes a score that lands in the band
# matching the player's part count instead of a flat 0/1.
LAUNCH_ROLL_ADDR = 0x800FA0D4
LAUNCH_ROLL_VANILLA = bytes.fromhex("0f004330")   # andi $v1, $v0, 0xf
LAUNCH_ROLL_REGION = "launch overlay"


def patch_rom(world: "MMX5World", patch: MMX5ProcedurePatch) -> None:
    """Collect per-seed edits as {addr, hex, region} rows."""
    seed_edits: list = []

    if world.options.launch_odds == "vanilla":
        seed_edits.append({"addr": LAUNCH_ROLL_ADDR,
                           "hex": LAUNCH_ROLL_VANILLA.hex(),
                           "region": LAUNCH_ROLL_REGION})

    if world.options.text_skip:
        # One toggle drives both: anyone who wants instant text wants it to
        # advance too, and instant-without-advance just moves the waiting.
        for addr in (TEXT_INSTANT_ADDR, TEXT_ADVANCE_ADDR):
            seed_edits.append({"addr": addr, "hex": TEXT_NOP.hex(),
                               "region": TEXT_REGION})

    if world.options.pickupsanity:
        # Consumable-pickup stub + jump-table redirects for kinds 0x02-0x08.
        # Per-seed on purpose: without the option the disc stays byte-identical
        # to the validated base, and consumables keep their vanilla effects.
        for addr, payload, region in disc.pickupsanity_edits():
            seed_edits.append({"addr": addr, "hex": payload.hex(),
                               "region": region})

    # NOTE: all_mavericks emits NO disc edit. Its endgame gate is entirely
    # client-side (ACT 0x800D1C79) - see the removal note above.

    patch.write_file("seed_edits.json", json.dumps(seed_edits).encode("utf-8"))


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        md5 = hashlib.md5()
        md5.update(base_rom_bytes)
        if md5.hexdigest() not in ACCEPTED_HASHES:
            raise Exception("Supplied base disc image does not match a known "
                            "MD5 for the US (SLUS-01334) release. Expected the "
                            f"Redump dump ({HASH_US_REDUMP}); a variant with one "
                            "extra trailing zero sector is also accepted. Verify "
                            "your dump (raw 2352-byte .bin, single data track).")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["mmx5_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
