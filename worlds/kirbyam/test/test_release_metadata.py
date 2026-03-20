"""Tests for KirbyAM APWorld release metadata generation."""

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