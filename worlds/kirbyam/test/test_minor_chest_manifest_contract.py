"""Contract checks for generated minor chest manifest metadata."""

from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "data" / "minor_chest_manifest.json"


def test_minor_chest_manifest_includes_respawn_policy_metadata() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    metadata = manifest.get("metadata")
    assert isinstance(metadata, dict), "Manifest metadata must be a JSON object"

    respawn_policy = metadata.get("respawn_reopen_policy")
    assert isinstance(respawn_policy, dict), "Manifest metadata must include respawn_reopen_policy"

    assert (
        respawn_policy.get("conclusion") == "no_repeatable_minor_chest_reopen_path_confirmed"
    ), "Respawn policy conclusion should remain explicit and stable"

    evidence = respawn_policy.get("evidence")
    assert isinstance(evidence, list) and evidence, "Respawn policy evidence list must be populated"
    assert any("katam/src/treasures.c" in item for item in evidence), "Expected treasures.c evidence reference"
    assert any("katam/asm/chest.s" in item for item in evidence), "Expected chest.s evidence reference"
