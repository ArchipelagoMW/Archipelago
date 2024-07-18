import typing

from worlds.generic.Rules import add_rule, forbid_item

from .Arrays import difficulty_lambda, level_locations
from .Items import item_list
from .Locations import all_locations, chimeras_keep, dragons_lair, gates_of_the_underworld

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld


def prog_count(state, player, diff):
    count = 0
    for i in range(1, 14):
        if state.has(f"Runestone {i}", player):
            count += 1
    return count >= diff


def set_rules(world: "GauntletLegendsWorld"):
    runestones = [item.item_name for item in item_list if "Runestone" in item.item_name]
    obelisks = [item.item_name for item in item_list if "Obelisk" in item.item_name]
    mirror_shards = [item.item_name for item in item_list if "Mirror" in item.item_name]

    for location in [
        location
        for location in all_locations
           if "Chest" in location.name
           or "Mirror" in location.name
           or ("Barrel" in location.name and "Barrel of Gold" not in location.name)
           or location in dragons_lair
           or location in chimeras_keep
           or location in gates_of_the_underworld
    ] + [location for location in all_locations if "Obelisk" in location.name and world.options.obelisks == 1]:
        for item in obelisks:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(location.name), item, world.player)

    for location in [
        location for location in all_locations if "Barrel" in location.name and "Barrel of Gold" not in location.name
    ]:
        for item in runestones + mirror_shards:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(location.name), item, world.player)

    if not world.options.instant_max:
        for level_id, locations in level_locations.items():
            for location in locations:
                if location.difficulty > 1:
                    if location.name not in world.disabled_locations:
                        add_rule(
                            world.get_location(location.name),
                            lambda state, level_id_=level_id >> 4, difficulty=location.difficulty - 1: prog_count(
                                state, world.player, difficulty_lambda[level_id_][difficulty],
                            ),
                        )
