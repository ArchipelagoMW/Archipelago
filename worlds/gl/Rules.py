import typing

from worlds.generic.Rules import add_rule, forbid_item
from .Locations import all_locations, chimerasKeep, dragonsLair, LocationData, gatesOfTheUnderworld
from .Items import itemList
from .Arrays import level_locations, difficulty_lambda

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld

def prog_count(state, player):
    count = 0
    for i in range(1, 14):
        if state.has(f"Runestone {i}", player):
            count += 1
    if state.has("Dragon Mirror Shard", player):
        count += 1
    if state.has("Yeti Mirror Shard", player):
        count += 1
    if state.has("Chimera Mirror Shard", player):
        count += 1
    if state.has("Plague Fiend Mirror Shard", player):
        count += 1
    if state.has("Valley of Fire Obelisk", player):
        count += 1
    if state.has("Dagger Peak Obelisk", player):
        count += 1
    if state.has("Cliffs of Desolation Obelisk", player):
        count += 1
    if state.has("Castle Courtyard Obelisk", player):
        count += 1
    if state.has("Dungeon of Torment Obelisk", player):
        count += 1
    if state.has("Poisoned Fields Obelisk", player):
        count += 1
    if state.has("Haunted Cemetery Obelisk", player):
        count += 1
    return count


def name_convert(location: "LocationData") -> str:
    return location.name + (f" {sum(1 for l in all_locations[:all_locations.index(location) + 1] if l.name == location.name)}" if "Chest" in location.name or "Barrel" in location.name else "") + (f" (Dif. {location.difficulty})" if location.difficulty > 1 else "")


def set_rules(world: "GauntletLegendsWorld"):
    for location in [location for location in all_locations if "Obelisk" in location.name or "Chest" in location.name or "Mirror" in location.name or ("Barrel" in location.name and "Barrel of Gold" not in location.name) or location in dragonsLair or location in chimerasKeep or location in gatesOfTheUnderworld]:
        for item in [item for item in itemList if "Obelisk" in item.itemName]:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(name_convert(location)), item.itemName, world.player)

    for level_id, locations in level_locations.items():
        for location in locations:
            if location.difficulty > 1:
                if location.name not in world.disabled_locations:
                    add_rule(world.get_location(name_convert(location)), lambda state: prog_count(state, world.player) >= difficulty_lambda[level_id >> 4][location.difficulty - 1])

