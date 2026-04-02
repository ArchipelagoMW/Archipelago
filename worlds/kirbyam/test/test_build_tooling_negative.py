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
    """Missing archipelago.json next to build.py raises SystemExit."""
    orig_argv = sys.argv
    orig_file = build_mod.__file__
    orig_cwd = Path.cwd()
    fake_script = tmp_path / "build.py"
    fake_script.write_text("# placeholder\n", encoding="utf-8")
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    sys.argv = ["build.py", "--skip-patch"]
    os.chdir(run_dir)
    try:
        build_mod.__file__ = str(fake_script)
        with pytest.raises(SystemExit) as exc_info:
            build_mod.main()
        assert "manifest" in str(exc_info.value).lower() or "archipelago.json" in str(exc_info.value)
    finally:
        build_mod.__file__ = orig_file
        os.chdir(orig_cwd)
        sys.argv = orig_argv


def test_build_main_falls_back_when_make_missing_and_existing_patch_present(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """When make/devkit tools are unavailable, main() continues if base_patch.bsdiff4 already exists."""
    world_root = tmp_path
    (world_root / "data").mkdir()
    (world_root / "data" / "base_patch.bsdiff4").write_bytes(b"existing-patch")
    (world_root / "archipelago.json").write_text("{}\n", encoding="utf-8")

    fake_script = world_root / "build.py"
    fake_script.write_text("# placeholder\n", encoding="utf-8")

    built_apworld = world_root / "kirbyam.apworld"
    installed_target = world_root / "installed" / "kirbyam.apworld"
    installed: list[Path] = []

    def _raise_make_missing(*_args: object, **_kwargs: object) -> None:
        raise SystemExit("patch_rom.py failed.\nError: 'make' was not found on PATH.")

    def _build_apworld(_world_root: Path, _world_name: str) -> Path:
        built_apworld.write_bytes(b"apworld")
        return built_apworld

    def _install_apworld(_apworld_path: Path, install_path: Path) -> None:
        install_path.parent.mkdir(parents=True, exist_ok=True)
        install_path.write_bytes(b"installed")
        installed.append(install_path)

    monkeypatch.setattr(build_mod, "run_patch_rom", _raise_make_missing)
    monkeypatch.setattr(build_mod, "build_apworld_in_place", _build_apworld)
    monkeypatch.setattr(build_mod, "install_apworld", _install_apworld)
    monkeypatch.setattr(build_mod, "get_default_install_path", lambda _world: installed_target)

    orig_argv = sys.argv
    orig_file = build_mod.__file__
    orig_cwd = Path.cwd()
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    sys.argv = ["build.py"]
    os.chdir(run_dir)
    try:
        build_mod.__file__ = str(fake_script)
        build_mod.main()
    finally:
        build_mod.__file__ = orig_file
        os.chdir(orig_cwd)
        sys.argv = orig_argv

    assert installed == [installed_target]
    assert built_apworld.exists()


def test_build_main_still_fails_when_make_missing_and_no_existing_patch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Without an existing base patch, toolchain-missing patch build still fails fast."""
    world_root = tmp_path
    (world_root / "data").mkdir()
    (world_root / "archipelago.json").write_text("{}\n", encoding="utf-8")

    fake_script = world_root / "build.py"
    fake_script.write_text("# placeholder\n", encoding="utf-8")

    def _raise_make_missing(*_args: object, **_kwargs: object) -> None:
        raise SystemExit("patch_rom.py failed.\nError: 'make' was not found on PATH.")

    monkeypatch.setattr(build_mod, "run_patch_rom", _raise_make_missing)

    orig_argv = sys.argv
    orig_file = build_mod.__file__
    orig_cwd = Path.cwd()
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    sys.argv = ["build.py"]
    os.chdir(run_dir)
    try:
        build_mod.__file__ = str(fake_script)
        with pytest.raises(SystemExit) as exc_info:
            build_mod.main()
        assert "make" in str(exc_info.value)
    finally:
        build_mod.__file__ = orig_file
        os.chdir(orig_cwd)
        sys.argv = orig_argv
