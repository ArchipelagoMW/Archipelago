"""Tests for KirbyAM APWorld release metadata generation."""

import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[3] / ".github" / "scripts" / "kirbyam_release_metadata.py"
SPEC = spec_from_file_location("kirbyam_release_metadata", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load release metadata script from {SCRIPT_PATH}")
MODULE = module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_build_release_metadata_for_valid_tag_ref() -> None:
    metadata = MODULE.build_release_metadata("refs/tags/kirbyam-v0.0.1")

    assert metadata.release_enabled is True
    assert metadata.version == "0.0.1"
    assert metadata.release_tag == "kirbyam-v0.0.1"
    assert metadata.release_name == "KirbyAM APWorld v0.0.1"
    assert metadata.apworld_name == "kirbyam.apworld"


def test_build_release_metadata_for_branch_ref_disables_release() -> None:
    metadata = MODULE.build_release_metadata("refs/heads/main")

    assert metadata.release_enabled is False
    assert metadata.version == ""
    assert metadata.release_tag == ""
    assert metadata.release_name == ""
    assert metadata.apworld_name == "kirbyam.apworld"


def test_build_release_metadata_for_branch_ref_matching_tag_pattern_disables_release() -> None:
    metadata = MODULE.build_release_metadata("refs/heads/kirbyam-v0.0.1")

    assert metadata.release_enabled is False
    assert metadata.version == ""
    assert metadata.release_tag == ""
    assert metadata.release_name == ""
    assert metadata.apworld_name == "kirbyam.apworld"


def test_build_release_metadata_rejects_malformed_release_tag() -> None:
    with pytest.raises(ValueError, match="Malformed KirbyAM release tag"):
        MODULE.build_release_metadata("refs/tags/kirbyam-v0.0")


def test_inject_world_version_updates_manifest(tmp_path: Path) -> None:
    manifest_path = tmp_path / "archipelago.json"
    manifest_path.write_text(
        json.dumps({"game": "Kirby & The Amazing Mirror", "world_version": "0.0.1"}, indent=2) + "\n",
        encoding="utf-8",
    )

    changed = MODULE.inject_world_version(manifest_path, "0.0.2")
    result = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert changed is True
    assert result["world_version"] == "0.0.2"


def test_inject_world_version_noop_when_already_matching(tmp_path: Path) -> None:
    manifest_path = tmp_path / "archipelago.json"
    manifest_path.write_text(
        json.dumps({"game": "Kirby & The Amazing Mirror", "world_version": "0.0.2"}, indent=2) + "\n",
        encoding="utf-8",
    )

    changed = MODULE.inject_world_version(manifest_path, "0.0.2")
    result = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert changed is False
    assert result["world_version"] == "0.0.2"


def test_main_injects_world_version_for_release_tag(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest_path = tmp_path / "archipelago.json"
    manifest_path.write_text(
        json.dumps({"game": "Kirby & The Amazing Mirror", "world_version": "0.0.1"}, indent=2) + "\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "github_output.txt"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "kirbyam_release_metadata.py",
            "--github-ref",
            "refs/tags/kirbyam-v0.0.2",
            "--github-output",
            str(output_path),
            "--world-manifest",
            str(manifest_path),
        ],
    )

    assert MODULE.main() == 0

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    output_text = output_path.read_text(encoding="utf-8")

    assert manifest["world_version"] == "0.0.2"
    assert "version=0.0.2" in output_text
    assert "release_enabled=true" in output_text


def test_main_does_not_inject_world_version_for_branch_ref(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest_path = tmp_path / "archipelago.json"
    manifest_path.write_text(
        json.dumps({"game": "Kirby & The Amazing Mirror", "world_version": "0.0.1"}, indent=2) + "\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "github_output.txt"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "kirbyam_release_metadata.py",
            "--github-ref",
            "refs/heads/main",
            "--github-output",
            str(output_path),
            "--world-manifest",
            str(manifest_path),
        ],
    )

    assert MODULE.main() == 0

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    output_text = output_path.read_text(encoding="utf-8")

    assert manifest["world_version"] == "0.0.1"
    assert "version=" in output_text
    assert "release_enabled=false" in output_text