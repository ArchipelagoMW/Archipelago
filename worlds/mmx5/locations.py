from BaseClasses import Location

from . import names
from .items import BASE_ID
from .pickups import PICKUPS


class MMX5Location(Location):
    game = "Mega Man X5"


# Location ids: intro at +0; per-stage blocks of 10 starting at +100;
# pickupsanity block at +200. Stage order here fixes the id layout - append
# only, never reorder.
location_table: dict[str, int] = {names.INTRO_CLEAR: BASE_ID + 0}

for i, stage in enumerate(names.STAGES):
    base = BASE_ID + 100 + i * 10
    location_table[names.boss_location(stage)] = base + 0
    location_table[names.heart_location(stage)] = base + 1
    location_table[names.capsule_location(stage)] = base + 2
    if stage in names.STAGE_TANK:
        location_table[names.tank_location(stage)] = base + 3
    # Post-boss DNA reward choice. Keeps id base+4, which an earlier and
    # WRONG "Energy Up pickup" location occupied - Energy Ups are not stage
    # items at all (the stub never once recorded a kind-1 pickup). Reusing the
    # id keeps every other location id stable.
    location_table[names.dna_location(stage)] = base + 4
    # The equippable Part from the level-8+ reward tier - the THIRD thing a
    # Maverick grants (weapon, Life+/Energy+, Part). Uses the slot previously
    # reserved for "rank rewards".
    location_table[names.dna_part_location(stage)] = base + 5
    # +6.. reserved

# Pickupsanity: 32 freestanding consumables, ids +200 in pickups.PICKUPS
# order (the dataset's docstring fixes that order as append-only). Always in
# the id map - the datapackage carries every location the game can define -
# but only created as real locations when the option is on.
for i, (_stage, _area, _idx, _iid, name) in enumerate(PICKUPS):
    location_table[name] = BASE_ID + 200 + i

event_location_table: dict[str, int | None] = {
    names.VICTORY: None,
}

location_groups = {
    "Bosses": {names.boss_location(s) for s in names.STAGES},
    "Heart Tanks": {names.heart_location(s) for s in names.STAGES},
    "Armor Capsules": {names.capsule_location(s) for s in names.STAGES},
    "Tanks": {names.tank_location(s) for s in names.STAGE_TANK},
    "DNA Rewards": {names.dna_location(s) for s in names.STAGES},
    "DNA Parts": {names.dna_part_location(s) for s in names.STAGES},
    "Pickups": {name for _s, _a, _i, _d, name in PICKUPS},
}
