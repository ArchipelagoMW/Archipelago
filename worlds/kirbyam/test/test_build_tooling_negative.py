"""Negative-path tests for KirbyAM build tooling (build.py).

Covers the key failure modes required by issue #306:
- Missing/invalid manifest (archipelago.json).
- Missing patch_rom.py script.
- Missing data/ output directory.
- Invalid CLI argument combinations (--source-type arg without --rom, uppercase world name).
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest


BUILD_PY_PATH = Path(__file__).resolve().parents[1] / "build.py"
_build_spec = importlib.util.spec_from_file_location("kirbyam_build", BUILD_PY_PATH)
if _build_spec is None or _build_spec.loader is None:
    raise RuntimeError(f"Failed to load build module from {BUILD_PY_PATH}")
build_mod = importlib.util.module_from_spec(_build_spec)
_build_spec.loader.exec_module(build_mod)


# ── load_json ─────────────────────────────────────────────────────────────────

def test_load_json_missing_file(tmp_path: Path) -> None:
    """Missing JSON file raises SystemExit with an actionable 'Missing manifest' message."""
    with pytest.raises(SystemExit) as exc_info:
        build_mod.load_json(tmp_path / "archipelago.json")
    assert "Missing manifest" in str(exc_info.value)


def test_load_json_invalid_json(tmp_path: Path) -> None:
    """Malformed JSON raises SystemExit with a descriptive message."""
    bad_json = tmp_path / "archipelago.json"
    bad_json.write_text("{ this is not valid json }", encoding="utf-8")
    with pytest.raises(SystemExit) as exc_info:
        build_mod.load_json(bad_json)
    assert "Invalid JSON" in str(exc_info.value)


# ── run_patch_rom ─────────────────────────────────────────────────────────────

def test_run_patch_rom_missing_patch_script(tmp_path: Path) -> None:
    """Missing kirby_ap_payload/patch_rom.py raises SystemExit with an actionable message."""
    (tmp_path / "data").mkdir()
    # kirby_ap_payload/ dir does not exist → patch_rom.py cannot be found
    with pytest.raises(SystemExit) as exc_info:
        build_mod.run_patch_rom(tmp_path, source_type="file", rom_arg=None)
    assert "patch_rom.py not found" in str(exc_info.value)


def test_run_patch_rom_missing_data_dir(tmp_path: Path) -> None:
    """Missing data/ output directory raises SystemExit before any subprocess call."""
    (tmp_path / "kirby_ap_payload").mkdir()
    (tmp_path / "kirby_ap_payload" / "patch_rom.py").write_text("# placeholder")
    # data/ is intentionally absent
    with pytest.raises(SystemExit) as exc_info:
        build_mod.run_patch_rom(tmp_path, source_type="file", rom_arg=None)
    assert "Missing data folder" in str(exc_info.value)


def test_run_patch_rom_source_type_arg_without_rom(tmp_path: Path) -> None:
    """--source-type arg without a ROM path raises SystemExit before any subprocess call."""
    (tmp_path / "data").mkdir()
    (tmp_path / "kirby_ap_payload").mkdir()
    (tmp_path / "kirby_ap_payload" / "patch_rom.py").write_text("# placeholder")
    with pytest.raises(SystemExit) as exc_info:
        build_mod.run_patch_rom(tmp_path, source_type="arg", rom_arg=None)
    assert "did not provide --rom" in str(exc_info.value)


# ── main() top-level guards ───────────────────────────────────────────────────

def test_build_main_uppercase_world_name() -> None:
    """Uppercase characters in --world raise SystemExit before any filesystem access."""
    orig = sys.argv
    sys.argv = ["build.py", "--world", "KirbyAM", "--skip-patch"]
    try:
        with pytest.raises(SystemExit) as exc_info:
            build_mod.main()
        assert "lowercase" in str(exc_info.value)
    finally:
        sys.argv = orig


def test_build_main_missing_manifest(tmp_path: Path) -> None:
    """Missing archipelago.json in the working directory raises SystemExit."""
    orig_argv = sys.argv
    orig_cwd = Path.cwd()
    sys.argv = ["build.py", "--skip-patch"]
    os.chdir(tmp_path)
    try:
        with pytest.raises(SystemExit) as exc_info:
            build_mod.main()
        assert "manifest" in str(exc_info.value).lower() or "archipelago.json" in str(exc_info.value)
    finally:
        os.chdir(orig_cwd)
        sys.argv = orig_argv
