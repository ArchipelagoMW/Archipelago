"""Regression tests for Kirby AM patch ROM tooling."""

from __future__ import annotations

import importlib.util
from pathlib import Path


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
