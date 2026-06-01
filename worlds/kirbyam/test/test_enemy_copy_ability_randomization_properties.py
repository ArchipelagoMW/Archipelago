# mypy: disable-error-code=untyped-decorator
"""Property-based tests for enemy copy-ability randomization invariants (Issue #301)."""

from __future__ import annotations

import random

import pytest

from ..ability_randomization import (
    NO_ABILITY_NAME,
    ability_for_enemy_grant_event,
    ability_for_enemy_type,
    build_enemy_copy_ability_policy,
    build_shuffled_enemy_type_assignments,
    policy_is_whitelist_preserving,
)
from ..enemy_ability_data import FORBIDDEN_ENEMY_COPY_ABILITIES, VALID_ENEMY_COPY_ABILITIES
from ..options import AbilityRandomizationMode

hypothesis = pytest.importorskip(
    "hypothesis",
    reason="Hypothesis is required for property-based KirbyAM enemy randomization tests.",
)
given = hypothesis.given
settings = hypothesis.settings
st = hypothesis.strategies


_ABILITY_POOL = sorted(VALID_ENEMY_COPY_ABILITIES)
_ENEMY_KEY_STRATEGY = st.text(
    alphabet=st.characters(min_codepoint=48, max_codepoint=90),
    min_size=1,
    max_size=24,
)
_WHITELIST_STRATEGY = st.lists(st.sampled_from(_ABILITY_POOL), min_size=1, unique=True)


@settings(max_examples=120, deadline=None)
@given(
    seed=st.integers(min_value=0, max_value=2**63 - 1),
    mode=st.sampled_from(
        [
            AbilityRandomizationMode.option_shuffled,
            AbilityRandomizationMode.option_completely_random,
        ]
    ),
    whitelist=_WHITELIST_STRATEGY,
    no_ability_weight=st.integers(min_value=0, max_value=100),
    enemy_type_key=_ENEMY_KEY_STRATEGY,
    event_index=st.one_of(st.integers(min_value=0, max_value=10_000), _ENEMY_KEY_STRATEGY),
)
def test_property_policy_outputs_whitelist_or_normal_and_never_forbidden(
    seed: int,
    mode: int,
    whitelist: list[str],
    no_ability_weight: int,
    enemy_type_key: str,
    event_index: int | str,
) -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(seed),
        mode,
        include_boss_spawns=True,
        include_minibosses=True,
        whitelist=whitelist,
        no_ability_weight=no_ability_weight,
    )

    assert policy_is_whitelist_preserving(policy, whitelist)

    if mode == AbilityRandomizationMode.option_shuffled:
        ability = ability_for_enemy_type(policy, enemy_type_key)
    else:
        ability = ability_for_enemy_grant_event(policy, event_index, enemy_type_key)

    assert ability == NO_ABILITY_NAME or ability in whitelist
    assert ability == NO_ABILITY_NAME or ability not in FORBIDDEN_ENEMY_COPY_ABILITIES


@settings(max_examples=120, deadline=None)
@given(
    seed=st.integers(min_value=0, max_value=2**63 - 1),
    whitelist=_WHITELIST_STRATEGY,
    no_ability_weight=st.integers(min_value=0, max_value=100),
    enemy_type_key=_ENEMY_KEY_STRATEGY,
)
def test_property_shuffled_mode_is_stable_per_enemy_key(
    seed: int,
    whitelist: list[str],
    no_ability_weight: int,
    enemy_type_key: str,
) -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(seed),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
        whitelist=whitelist,
        no_ability_weight=no_ability_weight,
    )

    first = ability_for_enemy_type(policy, enemy_type_key)
    second = ability_for_enemy_type(policy, enemy_type_key)

    assert first == second


@settings(max_examples=120, deadline=None)
@given(
    seed=st.integers(min_value=0, max_value=2**63 - 1),
    whitelist=_WHITELIST_STRATEGY,
    no_ability_weight=st.integers(min_value=0, max_value=100),
    enemy_type_key=_ENEMY_KEY_STRATEGY,
    event_index=st.one_of(st.integers(min_value=0, max_value=10_000), _ENEMY_KEY_STRATEGY),
)
def test_property_completely_random_mode_is_stable_per_enemy_event_key(
    seed: int,
    whitelist: list[str],
    no_ability_weight: int,
    enemy_type_key: str,
    event_index: int | str,
) -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(seed),
        AbilityRandomizationMode.option_completely_random,
        include_boss_spawns=True,
        include_minibosses=True,
        whitelist=whitelist,
        no_ability_weight=no_ability_weight,
    )

    first = ability_for_enemy_grant_event(policy, event_index, enemy_type_key)
    second = ability_for_enemy_grant_event(policy, event_index, enemy_type_key)

    assert first == second


@settings(max_examples=80, deadline=None)
@given(
    seed=st.integers(min_value=0, max_value=2**63 - 1),
    whitelist=_WHITELIST_STRATEGY,
    enemy_type_key=_ENEMY_KEY_STRATEGY,
    event_index=st.one_of(st.integers(min_value=0, max_value=10_000), _ENEMY_KEY_STRATEGY),
)
def test_property_no_ability_weight_boundaries(
    seed: int,
    whitelist: list[str],
    enemy_type_key: str,
    event_index: int | str,
) -> None:
    shuffled_zero = build_enemy_copy_ability_policy(
        random.Random(seed),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
        whitelist=whitelist,
        no_ability_weight=0,
    )
    shuffled_full = build_enemy_copy_ability_policy(
        random.Random(seed),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
        whitelist=whitelist,
        no_ability_weight=100,
    )

    random_zero = build_enemy_copy_ability_policy(
        random.Random(seed),
        AbilityRandomizationMode.option_completely_random,
        include_boss_spawns=True,
        include_minibosses=True,
        whitelist=whitelist,
        no_ability_weight=0,
    )
    random_full = build_enemy_copy_ability_policy(
        random.Random(seed),
        AbilityRandomizationMode.option_completely_random,
        include_boss_spawns=True,
        include_minibosses=True,
        whitelist=whitelist,
        no_ability_weight=100,
    )

    assert ability_for_enemy_type(shuffled_zero, enemy_type_key) in whitelist
    assert ability_for_enemy_type(shuffled_full, enemy_type_key) == NO_ABILITY_NAME

    assert ability_for_enemy_grant_event(random_zero, event_index, enemy_type_key) in whitelist
    assert ability_for_enemy_grant_event(random_full, event_index, enemy_type_key) == NO_ABILITY_NAME


@settings(max_examples=120, deadline=None)
@given(
    seed=st.integers(min_value=0, max_value=2**63 - 1),
    whitelist=_WHITELIST_STRATEGY,
    enemy_type_keys=st.lists(_ENEMY_KEY_STRATEGY, min_size=1, max_size=128),
)
def test_property_shuffled_assignments_are_whitelist_preserving_and_cover_when_possible(
    seed: int,
    whitelist: list[str],
    enemy_type_keys: list[str],
) -> None:
    policy = build_enemy_copy_ability_policy(
        random.Random(seed),
        AbilityRandomizationMode.option_shuffled,
        include_boss_spawns=True,
        include_minibosses=True,
        whitelist=whitelist,
        no_ability_weight=0,
    )

    assignments = build_shuffled_enemy_type_assignments(policy, enemy_type_keys)

    unique_enemy_keys = sorted(set(enemy_type_keys))
    assert set(assignments.keys()) == set(unique_enemy_keys)
    assert all(ability in whitelist for ability in assignments.values())

    if len(unique_enemy_keys) >= len(whitelist):
        assert set(whitelist).issubset(set(assignments.values()))
