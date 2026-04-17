"""Location definitions for Ducks Can Drive.

Five tiers per stat gives 25 upgrade locations. Tier N is reached when the
player buys the N-th upgrade of that stat at the garage; the client mod sends
a `LocationChecks` packet at that moment.
"""
from __future__ import annotations

from dataclasses import dataclass

from .items import DUCKS_BASE_ID, TIERS_PER_STAT, UPGRADE_STATS

LOCATIONS_OFFSET = 0x100  # keep location IDs clearly separated from item IDs


@dataclass(frozen=True)
class LocationData:
    id: int
    stat: str
    tier: int


def _build_table() -> dict[str, LocationData]:
    table: dict[str, LocationData] = {}
    for stat_index, stat in enumerate(UPGRADE_STATS):
        for tier in range(1, TIERS_PER_STAT + 1):
            loc_id = DUCKS_BASE_ID + LOCATIONS_OFFSET + stat_index * 0x10 + tier
            table[f"Upgrade {stat} Tier {tier}"] = LocationData(id=loc_id, stat=stat, tier=tier)
    return table


location_table: dict[str, LocationData] = _build_table()
location_name_to_id: dict[str, int] = {name: data.id for name, data in location_table.items()}
