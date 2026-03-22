"""Golden snapshot tests for deterministic KirbyAM outputs (Issue #311)."""

from __future__ import annotations

import json
import os
import random
from pathlib import Path
from unittest.mock import Mock

from .. import KirbyAmWorld
from ..ability_randomization import (
    ability_for_enemy_grant_event,
    ability_for_enemy_type,
    build_enemy_copy_ability_policy,
)
from ..options import EnemyCopyAbilityRandomization

SNAPSHOT_DIR = Path(__file__).resolve().parent / "data" / "snapshots"
UPDATE_SNAPSHOTS = os.environ.get("KIRBYAM_UPDATE_SNAPSHOTS") == "1"


def _write_or_assert_snapshot(snapshot_name: str, payload: dict[str, object]) -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path = SNAPSHOT_DIR / snapshot_name
    actual = json.dumps(payload, indent=2, sort_keys=True) + "\n"

    if UPDATE_SNAPSHOTS:
        snapshot_path.write_text(actual, encoding="utf-8", newline="\n")

    if not snapshot_path.exists():
        raise AssertionError(
            f"Missing snapshot file: {snapshot_path}. "
            "Run with KIRBYAM_UPDATE_SNAPSHOTS=1 to generate it."
        )

    expected = snapshot_path.read_text(encoding="utf-8")
    assert actual == expected, (
        f"Snapshot mismatch for {snapshot_name}. "
        "If this behavior change is intentional, regenerate snapshots with "
        "KIRBYAM_UPDATE_SNAPSHOTS=1 and commit the updated files."
    )


def _build_representative_slot_data() -> dict[str, object]:
    world = KirbyAmWorld.__new__(KirbyAmWorld)

    options = Mock()
    options.as_dict.return_value = {
        "goal": 0,
        "shards": 2,
        "death_link": True,
        "enemy_copy_ability_randomization": 1,
        "randomize_boss_spawned_ability_grants": True,
        "randomize_miniboss_ability_grants": False,
    }

    world.options = options
    world._enemy_copy_ability_policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        EnemyCopyAbilityRandomization.option_shuffled,
        randomize_boss_spawned_ability_grants=True,
        randomize_miniboss_ability_grants=False,
    )
    return KirbyAmWorld.fill_slot_data(world)


def _build_deterministic_mapping_artifacts() -> dict[str, object]:
    enemy_keys = [
        "WADDLE_DEE",
        "BLADE_KNIGHT",
        "HOT_HEAD",
        "SIR_KIBBLE",
        "SPARKY",
    ]

    shuffled_policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        EnemyCopyAbilityRandomization.option_shuffled,
        randomize_boss_spawned_ability_grants=False,
        randomize_miniboss_ability_grants=False,
    )
    shuffled_mapping = {
        key: ability_for_enemy_type(shuffled_policy, key)
        for key in enemy_keys
    }

    random_policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        EnemyCopyAbilityRandomization.option_completely_random,
        randomize_boss_spawned_ability_grants=True,
        randomize_miniboss_ability_grants=True,
    )
    random_mapping = {
        key: {
            str(event): ability_for_enemy_grant_event(random_policy, event, key)
            for event in (1, 2, 3)
        }
        for key in enemy_keys
    }

    return {
        "shuffled_policy": shuffled_policy,
        "shuffled_enemy_mapping": shuffled_mapping,
        "random_policy": random_policy,
        "random_enemy_event_mapping": random_mapping,
    }


def test_slot_data_snapshot_matches_golden() -> None:
    _write_or_assert_snapshot(
        "slot_data_representative.json",
        _build_representative_slot_data(),
    )


def test_generated_mapping_snapshot_matches_golden() -> None:
    _write_or_assert_snapshot(
        "enemy_mapping_seed_20260322.json",
        _build_deterministic_mapping_artifacts(),
    )
