"""Enemy copy-ability randomization helpers for KirbyAM.

Issue #111 defines three enemy randomization modes:
- vanilla
- shuffled (enemy type deterministic)
- completely random (deterministic per source/event key)

Enemy statues are intentionally out of scope (issue #209).
"""

from __future__ import annotations

import hashlib
import random
from typing import Any, Iterable

from .enemy_ability_data import FORBIDDEN_ENEMY_COPY_ABILITIES, VALID_ENEMY_COPY_ABILITIES
from .options import AbilityRandomizationMode


NO_ABILITY_NAME = "Normal"


def _normalize_whitelist(values: Iterable[str]) -> list[str]:
    normalized = sorted({value.strip() for value in values if value and value.strip()})
    if not normalized:
        raise ValueError("enemy copy-ability whitelist cannot be empty")
    forbidden = FORBIDDEN_ENEMY_COPY_ABILITIES.intersection(normalized)
    if forbidden:
        raise ValueError(f"forbidden enemy copy abilities present: {sorted(forbidden)}")
    unknown = set(normalized).difference(VALID_ENEMY_COPY_ABILITIES)
    if unknown:
        raise ValueError(f"unknown enemy copy abilities present: {sorted(unknown)}")
    return normalized


def _normalize_no_ability_weight(value: int) -> int:
    normalized = int(value)
    if not 0 <= normalized <= 100:
        raise ValueError("enemy no-ability weight must be between 0 and 100")
    return normalized


def build_enemy_copy_ability_policy(
    rng: random.Random,
    mode: int,
    include_boss_spawns: bool,
    include_minibosses: bool,
    whitelist: Iterable[str] = VALID_ENEMY_COPY_ABILITIES,
    include_passive_enemies: bool = False,
    no_ability_weight: int = 0,
) -> dict[str, Any]:
    """Build deterministic slot-data policy for enemy copy-ability randomization.

    For shuffled mode, enemy types can be mapped with `ability_for_enemy_type`.
    For completely random mode, source/event keys can be mapped with
    `ability_for_enemy_grant_event`.
    """
    ordered = _normalize_whitelist(whitelist)
    normalized_no_ability_weight = _normalize_no_ability_weight(no_ability_weight)

    policy: dict[str, Any] = {
        "mode": int(mode),
        "allowed_abilities": ordered,
        "ability_randomization_boss_spawns": bool(include_boss_spawns),
        "ability_randomization_minibosses": bool(include_minibosses),
        "ability_randomization_passive_enemies": bool(include_passive_enemies),
        "ability_randomization_no_ability_weight": normalized_no_ability_weight,
    }

    if mode == AbilityRandomizationMode.option_vanilla:
        policy["identity_map"] = {name: name for name in ordered}
        return policy

    seed_value = rng.getrandbits(64)
    policy["seed"] = seed_value

    if mode == AbilityRandomizationMode.option_shuffled:
        policy["mapping_style"] = "per_enemy_type"
        return policy

    if mode == AbilityRandomizationMode.option_completely_random:
        policy["mapping_style"] = "per_grant_event"
        return policy

    raise ValueError(f"unsupported enemy copy-ability randomization mode: {mode}")


def _stable_index(seed: int, key: str, pool_size: int) -> int:
    payload = f"{seed}:{key}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "little") % pool_size


def _selects_no_ability(seed: int, key: str, weight: int) -> bool:
    if weight <= 0:
        return False
    if weight >= 100:
        return True
    return _stable_index(seed, f"{key}:no_ability", 100) < weight


def ability_for_enemy_type(policy: dict[str, Any], enemy_type_key: str) -> str:
    """Return the deterministic shuffled ability for an enemy type key."""
    if int(policy.get("mode", -1)) != AbilityRandomizationMode.option_shuffled:
        raise ValueError("ability_for_enemy_type requires shuffled mode policy")

    abilities = list(policy.get("allowed_abilities", []))
    if not abilities:
        raise ValueError("policy allowed_abilities cannot be empty")

    seed = int(policy.get("seed", 0))
    no_ability_weight = _normalize_no_ability_weight(
        policy.get("ability_randomization_no_ability_weight", 0)
    )
    if _selects_no_ability(seed, enemy_type_key, no_ability_weight):
        return NO_ABILITY_NAME
    index = _stable_index(seed, enemy_type_key, len(abilities))
    return abilities[index]


def ability_for_enemy_grant_event(policy: dict[str, Any], event_index: int | str, enemy_type_key: str) -> str:
    """Return the deterministic per-event ability for completely random mode."""
    if int(policy.get("mode", -1)) != AbilityRandomizationMode.option_completely_random:
        raise ValueError("ability_for_enemy_grant_event requires completely random mode policy")

    abilities = list(policy.get("allowed_abilities", []))
    if not abilities:
        raise ValueError("policy allowed_abilities cannot be empty")

    seed = int(policy.get("seed", 0))
    event_key = f"{enemy_type_key}:{event_index}"
    no_ability_weight = _normalize_no_ability_weight(
        policy.get("ability_randomization_no_ability_weight", 0)
    )
    if _selects_no_ability(seed, event_key, no_ability_weight):
        return NO_ABILITY_NAME
    index = _stable_index(seed, event_key, len(abilities))
    return abilities[index]


def policy_is_whitelist_preserving(policy: dict[str, Any], whitelist: Iterable[str]) -> bool:
    ordered = set(_normalize_whitelist(whitelist))
    allowed = set(policy.get("allowed_abilities", []))
    return allowed == ordered


def remap_is_whitelist_preserving(remap: dict[str, str], whitelist: Iterable[str]) -> bool:
    """Backwards-compatible helper for identity/remap tables."""
    ordered = set(_normalize_whitelist(whitelist))
    return set(remap.keys()) == ordered and set(remap.values()) == ordered


def build_enemy_copy_ability_remap(
    rng: random.Random,
    mode: int,
    whitelist: Iterable[str] = VALID_ENEMY_COPY_ABILITIES,
) -> dict[str, str]:
    """Backwards-compatible helper used by older tests/callers.

    - vanilla returns identity
    - shuffled returns deterministic permutation
    - completely random returns a deterministic permutation snapshot
    """
    ordered = _normalize_whitelist(whitelist)

    if mode == AbilityRandomizationMode.option_vanilla:
        return {name: name for name in ordered}

    if mode == AbilityRandomizationMode.option_shuffled:
        shuffled = list(ordered)
        random.Random(rng.getrandbits(64)).shuffle(shuffled)
        return {source: target for source, target in zip(ordered, shuffled)}

    if mode == AbilityRandomizationMode.option_completely_random:
        # Snapshot remap for compatibility only; runtime per-event behavior uses
        # ability_for_enemy_grant_event with policy mode.
        shuffled = list(ordered)
        rng.shuffle(shuffled)
        return {source: target for source, target in zip(ordered, shuffled)}

    raise ValueError(f"unsupported enemy copy-ability randomization mode: {mode}")
