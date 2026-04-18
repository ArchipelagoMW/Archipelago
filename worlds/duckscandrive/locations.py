"""Location definitions for Ducks Can Drive.

Three families:

* **Upgrade locations** — 5 tiers × 5 stats (`Garage.Upgrade*`). Gated
  in logic so tier N ≥ 2 requires N-1 progressives of that stat.
* **Book locations** — 8 collectibles (`Book1`..`Book8`). Free pickups
  scattered around the City scene.
* **Time-trial locations** — for each of the 7 offline tracks, a
  "Finish <track>" location, and for the 6 tracks that have a par
  time, a "Beat par on <track>" location. All free sphere-1 (tracks
  are accessible from the main menu without any AP prerequisite).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .items import BOOK_COUNT, DUCKS_BASE_ID, TIERS_PER_STAT, UPGRADE_STATS

UPGRADES_OFFSET = 0x100
BOOKS_OFFSET = 0x200
TT_FINISH_OFFSET = 0x300
TT_PAR_OFFSET = 0x400


@dataclass(frozen=True)
class UpgradeLocationData:
    id: int
    stat: str
    tier: int


@dataclass(frozen=True)
class TimeTrialTrack:
    scene_name: str   # the Unity scene name, used by the client mod
    display: str      # shown in AP tracker / yaml
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


def _build_time_trial_table() -> dict[str, int]:
    table: dict[str, int] = {}
    for index, track in enumerate(TIME_TRIAL_TRACKS):
        table[f"Finish {track.display}"] = DUCKS_BASE_ID + TT_FINISH_OFFSET + index
        if track.par_seconds is not None:
            table[f"Beat par on {track.display}"] = DUCKS_BASE_ID + TT_PAR_OFFSET + index
    return table


upgrade_location_table: dict[str, UpgradeLocationData] = _build_upgrade_table()
book_location_table: dict[str, int] = _build_book_table()
time_trial_location_table: dict[str, int] = _build_time_trial_table()

location_name_to_id: dict[str, int] = {
    **{name: data.id for name, data in upgrade_location_table.items()},
    **book_location_table,
    **time_trial_location_table,
}
