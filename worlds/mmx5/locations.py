from typing import Dict, Optional

from BaseClasses import Location

from . import names
from .items import BASE_ID


class MMX5Location(Location):
    game = "Mega Man X5"


# Location ids: intro at +0; per-stage blocks of 10 starting at +100.
# Stage order here fixes the id layout - append only, never reorder.
location_table: Dict[str, int] = {names.INTRO_CLEAR: BASE_ID + 0}

for i, stage in enumerate(names.STAGES):
    base = BASE_ID + 100 + i * 10
    location_table[names.boss_location(stage)] = base + 0
    location_table[names.heart_location(stage)] = base + 1
    location_table[names.capsule_location(stage)] = base + 2
    if stage in names.STAGE_TANK:
        location_table[names.tank_location(stage)] = base + 3
    # Energy-Up pickups (kind 1, ids 0x10-0x17): stub records them; exact
    # per-stage coords still filling in via the harvester, but the ring
    # record's stage byte identifies the location regardless.
    location_table[names.energy_up_location(stage)] = base + 4
    # +5.. reserved: rank rewards (later)

event_location_table: Dict[str, Optional[int]] = {
    names.VICTORY: None,
}

location_groups = {
    "Bosses": {names.boss_location(s) for s in names.STAGES},
    "Heart Tanks": {names.heart_location(s) for s in names.STAGES},
    "Armor Capsules": {names.capsule_location(s) for s in names.STAGES},
    "Tanks": {names.tank_location(s) for s in names.STAGE_TANK},
    "Energy Ups": {names.energy_up_location(s) for s in names.STAGES},
}
