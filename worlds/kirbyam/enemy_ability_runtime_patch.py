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

from dataclasses import dataclass
from typing import Any

from .ability_randomization import (
    VALID_ENEMY_COPY_ABILITIES,
    ability_for_enemy_grant_event,
    ability_for_enemy_type,
)
from .options import EnemyCopyAbilityRandomization


# Native ability IDs (katam/include/constants/kirby.h)
_ABILITY_NAME_TO_ID: dict[str, int] = {
    "Beam": 7,
    "Bomb": 9,
    "Cook": 12,
    "Crash": 24,
    "Cupid": 19,
    "Fighter": 20,
    "Fire": 1,
    "Burning": 3,
    "Ice": 2,
    "Magic": 21,
    "Parasol": 5,
    "Cutter": 6,
    "Throw": 10,
    "Wheel": 4,
    "Stone": 8,
    "Sleep": 11,
    "Laser": 13,
    "UFO": 14,
    "Spark": 15,
    "Tornado": 16,
    "Hammer": 17,
    "Sword": 18,
    "Smash": 22,
    "Mini": 23,
    "Missile": 25,
}

_LEGACY_ABILITY_ALIASES: dict[str, str] = {
    # Legacy policy/snapshot compatibility: historical name "Needle" maps to Beam.
    "Needle": "Beam",
}

_MISSING_RUNTIME_ABILITY_NAMES = set(VALID_ENEMY_COPY_ABILITIES) - set(_ABILITY_NAME_TO_ID)


def _validate_runtime_ability_ids() -> None:
    if _MISSING_RUNTIME_ABILITY_NAMES:
        raise ValueError(
            "runtime ability ID mapping missing for whitelist entries (by name): "
            f"{sorted(_MISSING_RUNTIME_ABILITY_NAMES)}"
        )


@dataclass(frozen=True)
class _AbilitySource:
    key: str
    addresses: tuple[int, ...]
    default_ability_id: int
    kind: str  # enemy | miniboss | boss_spawned


# Curated from kamrandomizer enemy/object ability tables.
# We intentionally include only entries that natively grant a non-zero ability.
_ABILITY_SOURCES: tuple[_AbilitySource, ...] = (
    # Normal enemies
    _AbilitySource("BANG_BANG", (0x351AB6,), 0x19, "enemy"),
    _AbilitySource("BOMBER", (0x351A0E,), 0x18, "enemy"),
    _AbilitySource("BOXIN", (0x3519C6,), 0x14, "enemy"),
    _AbilitySource("COOKIN", (0x3519DE,), 0x0C, "enemy"),
    _AbilitySource("CUPIE", (0x35176E,), 0x13, "enemy"),
    _AbilitySource("FLAMER", (0x351816,), 0x03, "enemy"),
    _AbilitySource("FOLEY", (0x35197E,), 0x09, "enemy"),
    _AbilitySource("GIANT_ROCKY", (0x351A3E,), 0x08, "enemy"),
    _AbilitySource("HEAVY_KNIGHT", (0x351A26,), 0x12, "enemy"),
    _AbilitySource("HOT_HEAD", (0x35182E,), 0x01, "enemy"),
    _AbilitySource("LASER_BALL", (0x351846,), 0x0D, "enemy"),
    _AbilitySource("METAL_GUARDIAN", (0x351A56,), 0x0D, "enemy"),
    _AbilitySource("MINNY", (0x3519F6,), 0x17, "enemy"),
    _AbilitySource("NODDY", (0x35191E,), 0x0B, "enemy"),
    _AbilitySource("PENGY", (0x35185E,), 0x02, "enemy"),
    _AbilitySource("ROCKY", (0x351876,), 0x08, "enemy"),
    _AbilitySource("SIR_KIBBLE", (0x35188E,), 0x06, "enemy"),
    _AbilitySource("SNAPPER", (0x352536,), 0x12, "enemy"),
    _AbilitySource("SPARKY", (0x3518A6,), 0x0F, "enemy"),
    _AbilitySource("SWORD_KNIGHT", (0x3518BE,), 0x12, "enemy"),
    _AbilitySource("TWISTER", (0x3518EE,), 0x10, "enemy"),
    _AbilitySource("UFO", (0x3518D6,), 0x0E, "enemy"),
    _AbilitySource("WADDLE_DOO", (0x3517FE,), 0x07, "enemy"),
    _AbilitySource("WHEELIE", (0x351906,), 0x04, "enemy"),
    # Mini-bosses
    _AbilitySource("BATAFIRE", (0x351BD6,), 0x03, "miniboss"),
    _AbilitySource("BOMBAR", (0x351C36,), 0x19, "miniboss"),
    _AbilitySource("BONKERS", (0x351BA6,), 0x11, "miniboss"),
    _AbilitySource("BOX_BOXER", (0x351BEE,), 0x14, "miniboss"),
    _AbilitySource("BOXY", (0x351C06,), 0x15, "miniboss"),
    _AbilitySource("MASTER_HAND", (0x351C1E,), 0x16, "miniboss"),
    _AbilitySource("MR_FROSTY", (0x351B8E,), 0x02, "miniboss"),
    _AbilitySource("PHAN_PHAN", (0x351BBE,), 0x0A, "miniboss"),
    # Boss-spawned / special spawned objects
    _AbilitySource("BOMBAR_BOMB", (0x3526FE,), 0x09, "boss_spawned"),
    _AbilitySource("BOMBAR_MISSILE", (0x352716,), 0x19, "boss_spawned"),
    _AbilitySource("DARK_MIND_BLUE_STAR", (0x35296E,), 0x02, "boss_spawned"),
    _AbilitySource("DARK_MIND_BOMB", (0x351ACE,), 0x18, "boss_spawned"),
    _AbilitySource("DARK_MIND_PURPLE_STAR", (0x352986,), 0x0F, "boss_spawned"),
    _AbilitySource("DARK_MIND_RED_STAR", (0x352956,), 0x01, "boss_spawned"),
    _AbilitySource("MOLEY_BOMB", (0x3528AE,), 0x09, "boss_spawned"),
    _AbilitySource("MOLEY_LARGE_ROCK", (0x3528C6,), 0x08, "boss_spawned"),
    _AbilitySource("MOLEY_OIL_DRUM", (0x3528DE,), 0x03, "boss_spawned"),
    _AbilitySource("MOLEY_SPINY", (0x3528F6,), 0x06, "boss_spawned"),
    _AbilitySource("MOLEY_TIRE", (0x352896,), 0x04, "boss_spawned"),
    _AbilitySource("PARASOL_OBJECT", (0x35257E,), 0x05, "boss_spawned"),
    _AbilitySource("PRANK_BOMB", (0x352686,), 0x09, "boss_spawned"),
    _AbilitySource("PRANK_FIREBALL", (0x352656,), 0x01, "boss_spawned"),
    _AbilitySource("PRANK_ICE", (0x35266E,), 0x02, "boss_spawned"),
    _AbilitySource("WIZ_BOMB", (0x35278E,), 0x09, "boss_spawned"),
    _AbilitySource("WIZ_CAR", (0x35275E,), 0x04, "boss_spawned"),
    _AbilitySource("WIZ_CLOUD", (0x3527A6,), 0x0F, "boss_spawned"),
    _AbilitySource("WIZ_POISON_APPLE", (0x3527BE,), 0x0B, "boss_spawned"),
)


def _ability_name_to_id(name: str) -> int:
    normalized_name = _LEGACY_ABILITY_ALIASES.get(name, name)
    if normalized_name not in _ABILITY_NAME_TO_ID:
        raise ValueError(f"unsupported runtime enemy ability name in policy: {name}")
    return _ABILITY_NAME_TO_ID[normalized_name]


def _is_source_enabled(source: _AbilitySource, policy: dict[str, Any]) -> bool:
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
    for source_index, source in enumerate(_ABILITY_SOURCES):
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
