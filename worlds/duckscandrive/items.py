"""Item definitions for Ducks Can Drive.

A progressive item per upgrade stat (five of each) plus a filler "Rubber Duck"
that lands at the eight book locations. The mod maps received `Progressive
<Stat>` items to permission to buy the next tier of that stat in-game; Rubber
Ducks are pool padding with no gameplay effect.

ID ranges on the shared base `DUCKS_BASE_ID = 0xDCD000`:
* `+0x00..0x04` — Progressive upgrade items
* `+0x10`      — Rubber Duck (single item id, count = 8)
* `+0x100..0x1FF` — Upgrade locations (see `locations.py`)
* `+0x200..0x2FF` — Book locations (see `locations.py`)
"""
from __future__ import annotations

from dataclasses import dataclass

DUCKS_BASE_ID = 0xDCD000  # 14,471,168 — distinctive local-dev range.

UPGRADE_STATS: tuple[str, ...] = ("Speed", "Acceleration", "Offroad", "Boost", "Handling")
TIERS_PER_STAT: int = 5

FILLER_OFFSET: int = 0x10
BOOK_COUNT: int = 8


@dataclass(frozen=True)
class ItemData:
    id: int
    count: int
    progression: bool


item_table: dict[str, ItemData] = {
    **{
        f"Progressive {stat}": ItemData(id=DUCKS_BASE_ID + i, count=TIERS_PER_STAT, progression=True)
        for i, stat in enumerate(UPGRADE_STATS)
    },
    "Rubber Duck": ItemData(id=DUCKS_BASE_ID + FILLER_OFFSET, count=BOOK_COUNT, progression=False),
}

item_name_to_id: dict[str, int] = {name: data.id for name, data in item_table.items()}

item_name_groups: dict[str, set[str]] = {
    "Upgrades": {f"Progressive {stat}" for stat in UPGRADE_STATS},
    "Filler": {"Rubber Duck"},
}
