"""Item definitions for Ducks Can Drive.

Three item families:
* Progressive upgrade items (one per stat, 5 copies each) — permit buying the
  next tier of that stat in-game.
* Track-unlock items (one per time-trial, 1 copy each) — gate access to the
  corresponding offline time-trial scene.
* Rubber Duck filler — pure pool padding, no gameplay effect.

ID ranges on the shared base `DUCKS_BASE_ID = 0xDCD000`:
* `+0x00..0x04` — Progressive upgrade items (5)
* `+0x10`      — Rubber Duck filler (single id, count = non-upgrade locations minus unlocks)
* `+0x20..0x26` — Track-unlock items (7)
* `+0x100..0x1FF` — Upgrade locations (see `locations.py`)
* `+0x200..0x2FF` — Book locations
* `+0x300..0x3FF` — Time-trial finish locations
* `+0x400..0x4FF` — Time-trial par-time locations
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

DUCKS_BASE_ID = 0xDCD000  # 14,471,168 — distinctive local-dev range.

UPGRADE_STATS: tuple[str, ...] = ("Speed", "Acceleration", "Offroad", "Boost", "Handling")
TIERS_PER_STAT: int = 5

FILLER_OFFSET: int = 0x10
TRACK_UNLOCK_OFFSET: int = 0x20

BOOK_COUNT: int = 8
TIME_TRIAL_LOCATION_COUNT: int = 13  # 7 finishes + 6 pars (Banana has no par)
TRACK_UNLOCK_COUNT: int = 7
RUBBER_DUCK_COUNT: int = BOOK_COUNT + TIME_TRIAL_LOCATION_COUNT - TRACK_UNLOCK_COUNT  # 14


@dataclass(frozen=True)
class ItemData:
    id: int
    count: int
    progression: bool


@dataclass(frozen=True)
class TimeTrialTrack:
    scene_name: str
    display: str
    par_seconds: Optional[float]


TIME_TRIAL_TRACKS: tuple[TimeTrialTrack, ...] = (
    TimeTrialTrack("Duck Circuit Offline",   "Duck Circuit",   35.0),
    TimeTrialTrack("Lake Loop Offline",      "Lake Loop",      40.0),
    TimeTrialTrack("Quack Crossing Offline", "Quack Crossing", 45.0),
    TimeTrialTrack("Wing Circuit Offline",   "Wing Circuit",   54.0),
    TimeTrialTrack("Blackbill Ship Offline", "Blackbill Ship", 95.0),
    TimeTrialTrack("Bill Beach Offline",     "Bill Beach",     90.0),
    TimeTrialTrack("Banana Offline",         "Banana",         None),
)


item_table: dict[str, ItemData] = {
    **{
        f"Progressive {stat}": ItemData(id=DUCKS_BASE_ID + i, count=TIERS_PER_STAT, progression=True)
        for i, stat in enumerate(UPGRADE_STATS)
    },
    "Rubber Duck": ItemData(id=DUCKS_BASE_ID + FILLER_OFFSET, count=RUBBER_DUCK_COUNT, progression=False),
    **{
        f"{track.display} Unlock": ItemData(
            id=DUCKS_BASE_ID + TRACK_UNLOCK_OFFSET + i, count=1, progression=True,
        )
        for i, track in enumerate(TIME_TRIAL_TRACKS)
    },
}

item_name_to_id: dict[str, int] = {name: data.id for name, data in item_table.items()}

item_name_groups: dict[str, set[str]] = {
    "Upgrades": {f"Progressive {stat}" for stat in UPGRADE_STATS},
    "Track Unlocks": {f"{track.display} Unlock" for track in TIME_TRIAL_TRACKS},
    "Filler": {"Rubber Duck"},
}
