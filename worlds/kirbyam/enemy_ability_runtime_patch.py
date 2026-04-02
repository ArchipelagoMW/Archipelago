"""Runtime ROM patch generation for enemy copy-ability randomization (Issue #338).

This module converts slot-data policy into deterministic byte writes against
known enemy/object ability table addresses in the Kirby AM ROM.

Address evidence source:
- kamrandomizer enemy/object ability tables (kamrandomizer.py)

Notes:
- We only patch entries that natively grant a non-zero ability.
- Wait remains excluded via the existing policy whitelist.
"""

from __future__ import annotations

from typing import Any

from .ability_randomization import (
    ability_for_enemy_grant_event,
    ability_for_enemy_type,
)
from .enemy_ability_data import (
    AbilitySource,
    ABILITY_NAME_TO_ID,
    ABILITY_SOURCES,
    LEGACY_ABILITY_ALIASES,
    VALID_ENEMY_COPY_ABILITIES,
)
from .options import EnemyCopyAbilityRandomization

_MISSING_RUNTIME_ABILITY_NAMES = set(VALID_ENEMY_COPY_ABILITIES) - set(ABILITY_NAME_TO_ID)


def _validate_runtime_ability_ids() -> None:
    if _MISSING_RUNTIME_ABILITY_NAMES:
        raise ValueError(
            "runtime ability ID mapping missing for whitelist entries (by name): "
            f"{sorted(_MISSING_RUNTIME_ABILITY_NAMES)}"
        )


def _ability_name_to_id(name: str) -> int:
    normalized_name = LEGACY_ABILITY_ALIASES.get(name, name)
    if normalized_name not in ABILITY_NAME_TO_ID:
        raise ValueError(f"unsupported runtime enemy ability name in policy: {name}")
    return ABILITY_NAME_TO_ID[normalized_name]


def _is_source_enabled(source: AbilitySource, policy: dict[str, Any]) -> bool:
    if source.kind == "miniboss" and not bool(policy.get("randomize_miniboss_ability_grants", True)):
        return False
    if source.kind == "boss_spawned" and not bool(policy.get("randomize_boss_spawned_ability_grants", True)):
        return False
    return True


def build_enemy_copy_runtime_patch_writes(policy: dict[str, Any]) -> dict[int, int]:
    """Return deterministic ROM writes for enemy copy-ability randomization.

    Returns a dict of ROM file offsets -> byte value (ability id).

    Note: `option_completely_random` is implemented as deterministic
    per-ability-source variation (each patched source entry can map differently),
    not per-live-grant re-roll at runtime.
    """
    mode = int(policy.get("mode", EnemyCopyAbilityRandomization.option_vanilla))
    if mode == EnemyCopyAbilityRandomization.option_vanilla:
        return {}

    _validate_runtime_ability_ids()

    writes: dict[int, int] = {}
    for source_index, source in enumerate(ABILITY_SOURCES):
        # Preserve vanilla no-ability entries.
        if source.default_ability_id == 0:
            continue
        if not _is_source_enabled(source, policy):
            continue

        if mode == EnemyCopyAbilityRandomization.option_shuffled:
            ability_name = ability_for_enemy_type(policy, source.key)
        elif mode == EnemyCopyAbilityRandomization.option_completely_random:
            # Keep mapping stable per source independent of category toggles.
            source_event_index = source_index + 1
            ability_name = ability_for_enemy_grant_event(policy, source_event_index, source.key)
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

    return writes
