"""Regression tests for Kirby AM patch ROM tooling."""

from __future__ import annotations

import importlib.util
import os
import tempfile
from pathlib import Path

import pytest


PATCH_ROM_PATH = Path(__file__).resolve().parents[1] / "kirby_ap_payload" / "patch_rom.py"
PATCH_ROM_SPEC = importlib.util.spec_from_file_location("kirbyam_patch_rom", PATCH_ROM_PATH)
if PATCH_ROM_SPEC is None or PATCH_ROM_SPEC.loader is None:
    raise RuntimeError(f"Failed to load patch_rom module from {PATCH_ROM_PATH}")
patch_rom = importlib.util.module_from_spec(PATCH_ROM_SPEC)
PATCH_ROM_SPEC.loader.exec_module(patch_rom)


def test_patch_rom_accepts_expected_usa_rom_size() -> None:
    assert patch_rom.get_rom_size_warning(0x1000000) is None


def test_patch_rom_warns_for_unexpected_rom_size() -> None:
    warning = patch_rom.get_rom_size_warning(0x400000)
    assert warning == "Warning: ROM size is 0x400000, expected 0x1000000. Proceeding anyway."


def test_thumb_bl_bytes_matches_existing_main_hook_patch() -> None:
    assert patch_rom.thumb_bl_bytes(0x08152696, 0x0815E000) == bytes.fromhex("0B F0 B3 FC")


def test_big_chest_collect_call_offset_matches_verified_hook_site() -> None:
    assert patch_rom.BIG_CHEST_COLLECT_CALL_OFFSET == 0x0000B144


def test_vitality_chest_collect_call_offset_matches_verified_hook_site() -> None:
    assert patch_rom.VITALITY_CHEST_COLLECT_CALL_OFFSET == 0x0000B0CC


# ── Negative-path tests: parse_args ──────────────────────────────────────────

def test_parse_args_source_type_arg_missing_rom_positional() -> None:
    """--source-type arg with no positional args should raise SystemExit."""
    with pytest.raises(SystemExit, match="Usage with --source-type arg"):
        patch_rom.parse_args(["patch_rom.py", "--source-type", "arg"])


def test_parse_args_source_type_arg_too_many_positionals() -> None:
    """--source-type arg with 3+ positionals should raise SystemExit."""
    with pytest.raises(SystemExit, match="Usage with --source-type arg"):
        patch_rom.parse_args(["patch_rom.py", "--source-type", "arg", "a.gba", "b.gba", "c.gba"])


def test_parse_args_source_type_file_too_many_positionals() -> None:
    """--source-type file with 2+ positionals should raise SystemExit."""
    with pytest.raises(SystemExit, match="Usage"):
        patch_rom.parse_args(["patch_rom.py", "--source-type", "file", "a.gba", "b.gba"])


# ── Negative-path tests: read_rom_path_from_tmp ───────────────────────────────

def test_read_rom_path_from_tmp_missing_file() -> None:
    """Missing rom_path.tmp should raise SystemExit with an actionable message."""
    with tempfile.TemporaryDirectory() as tmpdir:
        missing = os.path.join(tmpdir, "rom_path.tmp")
        with pytest.raises(SystemExit) as exc_info:
            patch_rom.read_rom_path_from_tmp(missing)
        assert "not found" in str(exc_info.value)


def test_read_rom_path_from_tmp_empty_file() -> None:
    """Empty rom_path.tmp (whitespace only) should raise SystemExit with an actionable message."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_file = os.path.join(tmpdir, "rom_path.tmp")
        with open(tmp_file, "w") as f:
            f.write("   \n\n")
        with pytest.raises(SystemExit) as exc_info:
            patch_rom.read_rom_path_from_tmp(tmp_file)
        assert "no usable ROM path" in str(exc_info.value)