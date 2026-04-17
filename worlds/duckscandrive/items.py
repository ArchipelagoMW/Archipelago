"""Item definitions for Ducks Can Drive.

A progressive item per upgrade stat, five of each. The client mod translates
one received `Progressive <Stat>` item into permission to buy the next tier of
that stat in-game.
"""
from __future__ import annotations

from dataclasses import dataclass

DUCKS_BASE_ID = 0xDCD000  # 14,471,168 — distinctive local-dev range.

UPGRADE_STATS: tuple[str, ...] = ("Speed", "Acceleration", "Offroad", "Boost", "Handling")
TIERS_PER_STAT: int = 5


@dataclass(frozen=True)
class ItemData:
    id: int
    count: int
    progression: bool


item_table: dict[str, ItemData] = {
    f"Progressive {stat}": ItemData(id=DUCKS_BASE_ID + i, count=TIERS_PER_STAT, progression=True)
    for i, stat in enumerate(UPGRADE_STATS)
}

item_name_to_id: dict[str, int] = {name: data.id for name, data in item_table.items()}

item_name_groups: dict[str, set[str]] = {
    "Upgrades": {f"Progressive {stat}" for stat in UPGRADE_STATS},
}
