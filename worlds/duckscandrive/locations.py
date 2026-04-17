"""Location definitions for Ducks Can Drive.

Two families, both in the City scene:

* **Upgrade locations** — 5 tiers × 5 stats (`Garage.Upgrade*`). Gated
  in logic so tier N ≥ 2 requires N-1 progressives of that stat.
* **Book locations** — 8 collectibles (`Book1`..`Book8`). Free sphere-1
  — any player who can reach the city can pick them up.
"""
from __future__ import annotations

from dataclasses import dataclass

from .items import BOOK_COUNT, DUCKS_BASE_ID, TIERS_PER_STAT, UPGRADE_STATS

UPGRADES_OFFSET = 0x100
BOOKS_OFFSET = 0x200


@dataclass(frozen=True)
class UpgradeLocationData:
    id: int
    stat: str
    tier: int


def _build_upgrade_table() -> dict[str, UpgradeLocationData]:
    table: dict[str, UpgradeLocationData] = {}
    for stat_index, stat in enumerate(UPGRADE_STATS):
        for tier in range(1, TIERS_PER_STAT + 1):
            loc_id = DUCKS_BASE_ID + UPGRADES_OFFSET + stat_index * 0x10 + tier
            table[f"Upgrade {stat} Tier {tier}"] = UpgradeLocationData(id=loc_id, stat=stat, tier=tier)
    return table


def _build_book_table() -> dict[str, int]:
    return {
        f"Book {n}": DUCKS_BASE_ID + BOOKS_OFFSET + n
        for n in range(1, BOOK_COUNT + 1)
    }


upgrade_location_table: dict[str, UpgradeLocationData] = _build_upgrade_table()
book_location_table: dict[str, int] = _build_book_table()

location_name_to_id: dict[str, int] = {
    **{name: data.id for name, data in upgrade_location_table.items()},
    **book_location_table,
}
