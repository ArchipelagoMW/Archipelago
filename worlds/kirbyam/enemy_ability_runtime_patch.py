"""Runtime ROM patch generation for copy-ability randomization.

This module converts slot-data policy into deterministic byte writes against
known enemy/object/statue ability table addresses in the Kirby AM ROM.

Address evidence sources:
- kamrandomizer enemy/object ability tables (kamrandomizer.py)
- ability statue lookup tables in katam/src/ability_objects.c

Notes:
- We patch entries that natively grant a non-zero ability, plus zero-id
    sources when `ability_randomization_passive_enemies` is enabled.
- Wait remains excluded via the existing policy whitelist.
- Statue writes are gated by the `ability_randomization_statues` option, inherit
    selected mode, always grant an ability, ignore passive/no-ability toggles,
    and respect the Minny toggle.
"""

from __future__ import annotations

import logging
from typing import Any

from .ability_randomization import (
    build_shuffled_enemy_type_assignments,
    ability_for_enemy_grant_event,
)
from .enemy_ability_data import (
    AbilitySource,
    ABILITY_NAME_TO_ID,
    ABILITY_SOURCES,
    VALID_ENEMY_COPY_ABILITIES,
)
from .options import AbilityRandomizationMode

_MISSING_RUNTIME_ABILITY_NAMES = set(VALID_ENEMY_COPY_ABILITIES) - set(ABILITY_NAME_TO_ID)

logger = logging.getLogger(__name__)


# Ability statue tables from katam/src/ability_objects.c:
# - gUnk_083538FC at ROM offset 0x3538FC (8 entries)
# - gUnk_08353904 at ROM offset 0x353904 (7 entries)
# - gUnk_0835390B at ROM offset 0x35390B (1 entry)
# - gUnk_0835390C at ROM offset 0x35390C (3 entries)
_STATUE_TABLES: tuple[tuple[int, tuple[str, ...]], ...] = (
    (0x3538FC, ("Beam", "Burning", "Laser", "Fire", "Stone", "Fighter", "Bomb", "Tornado")),
    (0x353904, ("Wheel", "Ice", "Spark", "Missile", "Smash", "Throw", "Hammer")),
    (0x35390B, ("Parasol",)),
    (0x35390C, ("Sword", "Cutter", "Cupid")),
)

_STATUE_SLOT_LABELS: dict[str, str] = {
    f"STATUE:{base_address + index:06X}": f"{default_ability} Statue"
    for base_address, default_abilities in _STATUE_TABLES
    for index, default_ability in enumerate(default_abilities)
}

_MINI_ABILITY_NAME = "Mini"


def _validate_runtime_ability_ids() -> None:
    if _MISSING_RUNTIME_ABILITY_NAMES:
        raise ValueError(
            "runtime ability ID mapping missing for whitelist entries (by name): "
            f"{sorted(_MISSING_RUNTIME_ABILITY_NAMES)}"
        )


def _ability_name_to_id(name: str) -> int:
    if name not in ABILITY_NAME_TO_ID:
        raise ValueError(f"unsupported runtime enemy ability name in policy: {name}")
    return ABILITY_NAME_TO_ID[name]


def _normalized_statue_pool(policy: dict[str, Any]) -> list[str]:
    # Statue randomization always grants an ability and uses the current mode.
    pool = [str(name) for name in policy.get("allowed_abilities", [])]
    if not bool(policy.get("ability_randomization_minny", True)):
        pool = [name for name in pool if name != _MINI_ABILITY_NAME]
    if not pool:
        raise ValueError("statue ability pool cannot be empty after Minny filtering")
    return pool


def _build_statue_assignments(policy: dict[str, Any], mode: int) -> dict[str, str]:
    pool = _normalized_statue_pool(policy)
    normalized_policy = dict(policy)
    normalized_policy["allowed_abilities"] = pool
    normalized_policy["ability_randomization_no_ability_weight"] = 0

    slot_keys = [
        f"STATUE:{base_address + index:06X}"
        for base_address, abilities in _STATUE_TABLES
        for index in range(len(abilities))
    ]

    if mode == AbilityRandomizationMode.option_shuffled:
        return build_shuffled_enemy_type_assignments(normalized_policy, slot_keys)
    if mode == AbilityRandomizationMode.option_completely_random:
        return {
            slot_key: ability_for_enemy_grant_event(
                normalized_policy,
                f"statue:{slot_key}",
                slot_key,
            )
            for slot_key in slot_keys
        }
    raise ValueError(f"unsupported enemy copy-ability randomization mode: {mode}")


def _is_source_enabled(source: AbilitySource, policy: dict[str, Any]) -> bool:
    if source.key == "MINNY" and not bool(policy.get("ability_randomization_minny", True)):
        return False
    if source.kind == "miniboss" and not bool(policy.get("ability_randomization_minibosses", True)):
        return False
    if source.kind == "boss_spawned" and not bool(policy.get("ability_randomization_boss_spawns", True)):
        return False
    return True


def _source_event_key(source: AbilitySource) -> str:
    address_fragment = ",".join(f"{address:06X}" for address in source.addresses)
    return f"{source.kind}:{source.key}:{address_fragment}"


def _included_randomizable_sources(policy: dict[str, Any]) -> tuple[list[AbilitySource], set[str]]:
    randomize_non_ability = bool(policy.get("ability_randomization_passive_enemies", False))

    included_sources: list[AbilitySource] = []
    excluded_unswallowable_sources: set[str] = set()
    for source in ABILITY_SOURCES:
        # Preserve vanilla no-ability entries unless the option explicitly enables them.
        if source.default_ability_id == 0 and not randomize_non_ability:
            continue

        if source.kind == "enemy" and not source.can_be_swallowed:
            excluded_unswallowable_sources.add(source.key)
            continue
        if not _is_source_enabled(source, policy):
            continue

        included_sources.append(source)

    return included_sources, excluded_unswallowable_sources


def build_enemy_copy_spoiler_rows(
    policy: dict[str, Any],
    include_statues: bool = False,
) -> list[tuple[str, str, str]]:
    """Return deterministic spoiler rows: (source_kind, source_key, assigned_ability)."""
    mode = int(policy.get("mode", AbilityRandomizationMode.option_off))
    if mode == AbilityRandomizationMode.option_off:
        return []

    included_sources, _ = _included_randomizable_sources(policy)

    shuffled_assignments: dict[str, str] = {}
    if mode == AbilityRandomizationMode.option_shuffled:
        shuffled_assignments = build_shuffled_enemy_type_assignments(
            policy,
            (source.key for source in included_sources),
        )

    rows: list[tuple[str, str, str]] = []
    for source in included_sources:
        if mode == AbilityRandomizationMode.option_shuffled:
            ability_name = shuffled_assignments[source.key]
        elif mode == AbilityRandomizationMode.option_completely_random:
            ability_name = ability_for_enemy_grant_event(policy, _source_event_key(source), source.key)
        else:
            raise ValueError(f"unsupported enemy ability randomization mode: {mode}")
        rows.append((source.kind, source.key, ability_name))

    if include_statues:
        statue_assignments = _build_statue_assignments(policy, mode)
        for base_address, default_abilities in _STATUE_TABLES:
            for index, _ in enumerate(default_abilities):
                slot_key = f"STATUE:{base_address + index:06X}"
                rows.append(("statue", _STATUE_SLOT_LABELS.get(slot_key, slot_key), statue_assignments[slot_key]))

    rows.sort(key=lambda row: (row[0], row[1]))
    return rows


def build_enemy_copy_runtime_patch_writes(
    policy: dict[str, Any],
    include_statues: bool = False,
) -> dict[int, int]:
    """Return deterministic ROM writes for enemy copy-ability randomization.

    Returns a dict of ROM file offsets -> byte value (ability id).

    This function handles the static ROM-patch path: each included enemy ability
    source address is overwritten with a deterministic ability ID at patch time.

    For ``option_shuffled`` mode, each enemy type maps to a fixed ability chosen
    deterministically from the allowed pool.

    For ``option_completely_random`` mode, each patched source entry maps
    independently to a deterministic ability (per source, not per live grant).
    At runtime, the payload's per-swallow reroll hook overrides these static
    values with a fresh random roll on every swallow event using the runtime
    config written by the client (``ability_randomization_*_runtime`` mailbox
    fields); the static writes here serve as a safe fallback when the runtime
    hook has not yet fired.
    """
    mode = int(policy.get("mode", AbilityRandomizationMode.option_off))
    if mode == AbilityRandomizationMode.option_off:
        return {}

    _validate_runtime_ability_ids()

    included_sources, excluded_unswallowable_sources = _included_randomizable_sources(policy)

    shuffled_assignments: dict[str, str] = {}
    if mode == AbilityRandomizationMode.option_shuffled:
        shuffled_assignments = build_shuffled_enemy_type_assignments(
            policy,
            (source.key for source in included_sources),
        )

    writes: dict[int, int] = {}
    for source in included_sources:

        if mode == AbilityRandomizationMode.option_shuffled:
            ability_name = shuffled_assignments[source.key]
        elif mode == AbilityRandomizationMode.option_completely_random:
            # Keep mapping stable per source independent of list ordering and toggles.
            ability_name = ability_for_enemy_grant_event(policy, _source_event_key(source), source.key)
        else:
            raise ValueError(f"unsupported enemy copy-ability randomization mode: {mode}")

        ability_id = _ability_name_to_id(ability_name)
        for address in source.addresses:
            existing = writes.get(address)
            if existing is not None and existing != ability_id:
                raise ValueError(
                    f"conflicting runtime patch writes for address 0x{address:06X}: {existing} vs {ability_id}"
                )
            writes[address] = ability_id

    if include_statues:
        statue_assignments = _build_statue_assignments(policy, mode)
        for base_address, default_abilities in _STATUE_TABLES:
            for index, _ in enumerate(default_abilities):
                slot_key = f"STATUE:{base_address + index:06X}"
                ability_name = statue_assignments[slot_key]
                ability_id = _ability_name_to_id(ability_name)
                writes[base_address + index] = ability_id

    if excluded_unswallowable_sources:
        logger.info(
            "Excluded unswallowable enemies from copy-ability randomization pool: %s",
            ", ".join(sorted(excluded_unswallowable_sources)),
        )

    return writes
