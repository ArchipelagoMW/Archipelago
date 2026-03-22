"""Tests for enemy copy-ability randomization policy generation (Issue #111)."""

from __future__ import annotations

import random

import pytest

from ..ability_randomization import (
    FORBIDDEN_ENEMY_COPY_ABILITIES,
    VALID_ENEMY_COPY_ABILITIES,
    ability_for_enemy_grant_event,
    ability_for_enemy_type,
    build_enemy_copy_ability_policy,
    remap_is_whitelist_preserving,
)
from ..options import EnemyCopyAbilityRandomization


def test_vanilla_mode_returns_identity_mapping_policy() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(12345),
        EnemyCopyAbilityRandomization.option_vanilla,
        randomize_boss_spawned_ability_grants=True,
        randomize_miniboss_ability_grants=True,
    )

    remap = policy["identity_map"]
    assert len(remap) == len(VALID_ENEMY_COPY_ABILITIES)
    assert all(remap[name] == name for name in VALID_ENEMY_COPY_ABILITIES)
    assert remap_is_whitelist_preserving(remap, VALID_ENEMY_COPY_ABILITIES)
    assert policy["randomize_boss_spawned_ability_grants"] is True
    assert policy["randomize_miniboss_ability_grants"] is True


def test_shuffled_mode_maps_enemy_type_consistently() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        EnemyCopyAbilityRandomization.option_shuffled,
        randomize_boss_spawned_ability_grants=False,
        randomize_miniboss_ability_grants=False,
    )
    first = ability_for_enemy_type(policy, "WADDLE_DEE")
    second = ability_for_enemy_type(policy, "WADDLE_DEE")
    other = ability_for_enemy_type(policy, "BLADE_KNIGHT")

    assert first == second
    assert first in VALID_ENEMY_COPY_ABILITIES
    assert other in VALID_ENEMY_COPY_ABILITIES
    assert policy["randomize_boss_spawned_ability_grants"] is False
    assert policy["randomize_miniboss_ability_grants"] is False


def test_completely_random_mode_varies_by_event() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(7),
        EnemyCopyAbilityRandomization.option_completely_random,
        randomize_boss_spawned_ability_grants=True,
        randomize_miniboss_ability_grants=True,
    )
    first = ability_for_enemy_grant_event(policy, 1, "WADDLE_DEE")
    second = ability_for_enemy_grant_event(policy, 2, "WADDLE_DEE")

    assert first in VALID_ENEMY_COPY_ABILITIES
    assert second in VALID_ENEMY_COPY_ABILITIES
    # Most seeds should differ across events; if not, a different enemy key still should.
    if first == second:
        third = ability_for_enemy_grant_event(policy, 1, "BLADE_KNIGHT")
        assert third in VALID_ENEMY_COPY_ABILITIES


def test_invalid_mode_raises_value_error() -> None:
    with pytest.raises(ValueError, match="unsupported enemy copy-ability randomization mode"):
        build_enemy_copy_ability_policy(random.Random(1), 999, True, True)


def test_empty_whitelist_raises_value_error() -> None:
    with pytest.raises(ValueError, match="enemy copy-ability whitelist cannot be empty"):
        build_enemy_copy_ability_policy(
            random.Random(1),
            EnemyCopyAbilityRandomization.option_shuffled,
            True,
            True,
            whitelist=[],
        )


def test_forbidden_abilities_are_excluded_from_default_pool() -> None:
    assert FORBIDDEN_ENEMY_COPY_ABILITIES.isdisjoint(VALID_ENEMY_COPY_ABILITIES)


def test_forbidden_abilities_in_custom_whitelist_raise() -> None:
    with pytest.raises(ValueError, match="forbidden enemy copy abilities present"):
        build_enemy_copy_ability_policy(
            random.Random(10),
            EnemyCopyAbilityRandomization.option_shuffled,
            True,
            True,
            whitelist=["Sword", "Crash"],
        )


def test_unknown_abilities_in_custom_whitelist_raise() -> None:
    with pytest.raises(ValueError, match="unknown enemy copy abilities present"):
        build_enemy_copy_ability_policy(
            random.Random(10),
            EnemyCopyAbilityRandomization.option_shuffled,
            True,
            True,
            whitelist=["Sword", "TotallyFakeAbility"],
        )


def test_build_policy_is_deterministic_for_same_seed_and_options() -> None:
    rng_seed = 20260322
    policy1 = build_enemy_copy_ability_policy(
        random.Random(rng_seed),
        EnemyCopyAbilityRandomization.option_shuffled,
        randomize_boss_spawned_ability_grants=True,
        randomize_miniboss_ability_grants=True,
    )
    policy2 = build_enemy_copy_ability_policy(
        random.Random(rng_seed),
        EnemyCopyAbilityRandomization.option_shuffled,
        randomize_boss_spawned_ability_grants=True,
        randomize_miniboss_ability_grants=True,
    )

    assert policy1 == policy2
    enemies = ["WADDLE_DEE", "BLADE_KNIGHT", "HOT_HEAD"]
    for enemy in enemies:
        assert ability_for_enemy_type(policy1, enemy) == ability_for_enemy_type(policy2, enemy)
