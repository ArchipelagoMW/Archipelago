import typing

from worlds.generic.Rules import add_rule, forbid_item
from .Locations import all_locations, chimerasKeep, dragonsLair, LocationData, gatesOfTheUnderworld
from .Items import itemList
from .Arrays import level_locations, difficulty_lambda

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld


def prog_count(state, player, diff):
    count = 0
    for i in range(1, 14):
        if state.has(f"Runestone {i}", player):
            count += 1
    return count >= diff


def set_rules(world: "GauntletLegendsWorld"):
    # runestones = [item.itemName for item in itemList if "Runestone" in item.itemName] # This is for 0.4.7
    for location in [location for location in all_locations if "Obelisk" in location.name or "Chest" in location.name or "Mirror" in location.name or ("Barrel" in location.name and "Barrel of Gold" not in location.name) or location in dragonsLair or location in chimerasKeep or location in gatesOfTheUnderworld]:
        for item in [item for item in itemList if "Obelisk" in item.itemName]:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(location.name), item.itemName, world.player)

    for location in [location for location in all_locations if "Barrel" in location.name and "Barrel of Gold" not in location.name]:
        for item in [item for item in itemList if "Runestone" in item.itemName]:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(location.name), item.itemName, world.player)

    for level_id, locations in level_locations.items():
        for location in locations:
            if location.difficulty > 1:
                if location.name not in world.disabled_locations:
                    add_rule(world.get_location(location.name), lambda state, level_id_=level_id >> 4, difficulty=location.difficulty - 1: prog_count(state, world.player, difficulty_lambda[level_id_][difficulty]))

