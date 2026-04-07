"""Shared JSON-backed enemy copy-ability data for KirbyAM."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AbilitySource:
    key: str
    addresses: tuple[int, ...]
    default_ability_name: str
    default_ability_id: int
    kind: str  # enemy | miniboss | boss_spawned
    can_be_swallowed: bool = True


def _load_json_file(filename: str) -> dict[str, Any]:
    raw = pkgutil.get_data(__name__, "data/" + filename)
    if raw is None:
        raise FileNotFoundError(f"Missing data file: worlds/kirbyam/data/{filename}")
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{filename} root must be a JSON object")
    return data


def _parse_address(value: Any) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.lower().startswith("0x"):
            return int(text, 16)
        return int(text)
    raise ValueError(f"unsupported address value type: {type(value).__name__}")


_ABILITY_DATA = _load_json_file("abilities.json")

_runtime_ability_name_to_id: dict[str, int] = {}
_valid_enemy_copy_abilities: list[str] = []
_forbidden_enemy_copy_abilities: set[str] = set()

for ability_name, raw_entry in _ABILITY_DATA.items():
    if not isinstance(ability_name, str) or not ability_name:
        raise ValueError("ability keys in abilities.json must be non-empty strings")
    if not isinstance(raw_entry, dict):
        raise ValueError(f"ability entry for {ability_name} must be an object")

    runtime_id_raw = raw_entry.get("runtime_ability_id")
    runtime_id = None if runtime_id_raw is None else int(runtime_id_raw)
    enemy_copy_allowed = bool(raw_entry.get("enemy_copy_allowed", True))

    if runtime_id is not None:
        _runtime_ability_name_to_id[ability_name] = runtime_id

    if enemy_copy_allowed:
        if runtime_id is None:
            raise ValueError(
                f"ability {ability_name} is enemy_copy_allowed but has no runtime_ability_id"
            )
        _valid_enemy_copy_abilities.append(ability_name)
    else:
        _forbidden_enemy_copy_abilities.add(ability_name)


ABILITY_NAME_TO_ID: dict[str, int] = dict(_runtime_ability_name_to_id)
VALID_ENEMY_COPY_ABILITIES: tuple[str, ...] = tuple(_valid_enemy_copy_abilities)
FORBIDDEN_ENEMY_COPY_ABILITIES: frozenset[str] = frozenset(_forbidden_enemy_copy_abilities)


_ENEMY_DATA = _load_json_file("enemies.json")

_ability_sources: list[AbilitySource] = []
for source_key, raw_entry in _ENEMY_DATA.items():
    if not isinstance(source_key, str) or not source_key:
        raise ValueError("enemy source keys in enemies.json must be non-empty strings")
    if not isinstance(raw_entry, dict):
        raise ValueError(f"enemy source entry for {source_key} must be an object")

    kind = str(raw_entry.get("kind", "")).strip()
    if kind not in {"enemy", "miniboss", "boss_spawned"}:
        raise ValueError(f"enemy source {source_key} has unsupported kind: {kind}")

    can_be_swallowed_raw = raw_entry.get("can_be_swallowed", True)
    if not isinstance(can_be_swallowed_raw, bool):
        raise ValueError(
            f"enemy source {source_key} field can_be_swallowed must be a boolean"
        )
    can_be_swallowed = can_be_swallowed_raw

    addresses_raw = raw_entry.get("addresses")
    if not isinstance(addresses_raw, list) or not addresses_raw:
        raise ValueError(f"enemy source {source_key} must include non-empty addresses")
    addresses = tuple(_parse_address(addr) for addr in addresses_raw)

    default_ability_name = str(raw_entry.get("default_ability", "")).strip()
    if not default_ability_name:
        raise ValueError(f"enemy source {source_key} missing default_ability")
    if default_ability_name not in ABILITY_NAME_TO_ID:
        raise ValueError(
            f"enemy source {source_key} references unknown default ability: {default_ability_name}"
        )

    _ability_sources.append(
        AbilitySource(
            key=source_key,
            addresses=addresses,
            default_ability_name=default_ability_name,
            default_ability_id=ABILITY_NAME_TO_ID[default_ability_name],
            kind=kind,
            can_be_swallowed=can_be_swallowed,
        )
    )

ABILITY_SOURCES: tuple[AbilitySource, ...] = tuple(_ability_sources)
