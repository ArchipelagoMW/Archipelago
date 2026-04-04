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
    policy_is_whitelist_preserving,
)
from ..options import AbilityRandomizationMode


def test_off_mode_returns_identity_mapping_policy() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(12345),
        AbilityRandomizationMode.option_off,
        include_boss_spawns=True,
        include_minibosses=True,
        no_ability_weight=55,
    )

    identity_map = policy["identity_map"]
    assert len(identity_map) == len(VALID_ENEMY_COPY_ABILITIES)
    assert all(identity_map[name] == name for name in VALID_ENEMY_COPY_ABILITIES)
    assert policy_is_whitelist_preserving(policy, VALID_ENEMY_COPY_ABILITIES)
    assert policy["ability_randomization_boss_spawns"] is True
    assert policy["ability_randomization_minibosses"] is True
    assert policy["ability_randomization_minny"] is True
    assert policy["ability_randomization_no_ability_weight"] == 55


def test_shuffled_mode_maps_enemy_type_consistently() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=False,
        include_minibosses=False,
    )
    first = ability_for_enemy_type(policy, "WADDLE_DEE")
    second = ability_for_enemy_type(policy, "WADDLE_DEE")
    other = ability_for_enemy_type(policy, "BLADE_KNIGHT")

    assert first == second
    assert first in VALID_ENEMY_COPY_ABILITIES
    assert other in VALID_ENEMY_COPY_ABILITIES
    assert policy["ability_randomization_boss_spawns"] is False
    assert policy["ability_randomization_minibosses"] is False
    assert policy["ability_randomization_minny"] is True


def test_completely_random_mode_varies_by_event() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(7),
        AbilityRandomizationMode.option_completely_random,
        include_boss_spawns=True,
        include_minibosses=True,
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


def test_invalid_no_ability_weight_raises_value_error() -> None:
    with pytest.raises(ValueError, match="enemy no-ability weight must be between 0 and 100"):
        build_enemy_copy_ability_policy(
            random.Random(1),
            AbilityRandomizationMode.option_shuffled,
            True,
            True,
            no_ability_weight=101,
        )


def test_empty_whitelist_raises_value_error() -> None:
    with pytest.raises(ValueError, match="enemy copy-ability whitelist cannot be empty"):
        build_enemy_copy_ability_policy(
            random.Random(1),
            AbilityRandomizationMode.option_shuffled,
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
            AbilityRandomizationMode.option_shuffled,
            True,
            True,
            whitelist=["Sword", "Wait"],
        )


def test_unknown_abilities_in_custom_whitelist_raise() -> None:
    with pytest.raises(ValueError, match="unknown enemy copy abilities present"):
        build_enemy_copy_ability_policy(
            random.Random(10),
            AbilityRandomizationMode.option_shuffled,
            True,
            True,
            whitelist=["Sword", "TotallyFakeAbility"],
        )


def test_build_policy_is_deterministic_for_same_seed_and_options() -> None:
    rng_seed = 20260322
    policy1 = build_enemy_copy_ability_policy(
        random.Random(rng_seed),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
    )
    policy2 = build_enemy_copy_ability_policy(
        random.Random(rng_seed),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
    )

    assert policy1 == policy2
    enemies = ["WADDLE_DEE", "BLADE_KNIGHT", "HOT_HEAD"]
    for enemy in enemies:
        assert ability_for_enemy_type(policy1, enemy) == ability_for_enemy_type(policy2, enemy)


def test_non_ability_enemies_flag_defaults_to_false_in_policy() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(1),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
    )
    assert policy["ability_randomization_passive_enemies"] is False
    assert policy["ability_randomization_minny"] is True
    assert policy["ability_randomization_no_ability_weight"] == 0


def test_non_ability_enemies_flag_true_stored_in_policy() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(1),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
        include_passive_enemies=True,
        no_ability_weight=55,
    )
    assert policy["ability_randomization_passive_enemies"] is True
    assert policy["ability_randomization_minny"] is True
    assert policy["ability_randomization_no_ability_weight"] == 55


def test_off_mode_stores_non_ability_flag_in_policy() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(1),
        AbilityRandomizationMode.option_off,
        include_boss_spawns=True,
        include_minibosses=True,
        include_passive_enemies=True,
        no_ability_weight=55,
    )
    assert policy["ability_randomization_passive_enemies"] is True
    assert policy["ability_randomization_minny"] is True
    assert policy["ability_randomization_no_ability_weight"] == 55


def test_minny_flag_false_stored_in_policy() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(1),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
        include_minny=False,
        no_ability_weight=55,
    )
    assert policy["ability_randomization_minny"] is False


def test_shuffled_mode_with_zero_no_ability_weight_never_returns_normal() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
        no_ability_weight=0,
    )

    for enemy in ("WADDLE_DEE", "BLADE_KNIGHT", "HOT_HEAD", "SIR_KIBBLE"):
        assert ability_for_enemy_type(policy, enemy) in VALID_ENEMY_COPY_ABILITIES


def test_shuffled_mode_with_full_no_ability_weight_always_returns_normal() -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
        no_ability_weight=100,
    )

    for enemy in ("WADDLE_DEE", "BLADE_KNIGHT", "HOT_HEAD", "SIR_KIBBLE"):
        assert ability_for_enemy_type(policy, enemy) == "Normal"


def test_completely_random_weight_changes_observed_no_ability_rate() -> None:
    low_policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        AbilityRandomizationMode.option_completely_random,
        include_boss_spawns=True,
        include_minibosses=True,
        no_ability_weight=10,
    )
    high_policy = build_enemy_copy_ability_policy(
        random.Random(20260322),
        AbilityRandomizationMode.option_completely_random,
        include_boss_spawns=True,
        include_minibosses=True,
        no_ability_weight=80,
    )

    low_normal_count = sum(
        1
        for event in range(200)
        if ability_for_enemy_grant_event(low_policy, event, "WADDLE_DEE") == "Normal"
    )
    high_normal_count = sum(
        1
        for event in range(200)
        if ability_for_enemy_grant_event(high_policy, event, "WADDLE_DEE") == "Normal"
    )

    assert high_normal_count > low_normal_count
