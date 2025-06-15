import typing

from BaseClasses import ItemClassification
from worlds.generic.Rules import add_rule, forbid_item

from .Arrays import difficulty_lambda, level_locations, no_obelisks
from .Items import item_list, obelisks
from .Locations import all_locations, chimeras_keep, dragons_lair, gates_of_the_underworld

if typing.TYPE_CHECKING:
    from . import GauntletLegendsWorld

def set_rules(world: "GauntletLegendsWorld"):
    for location in [
        location
        for location in all_locations
            if "Mirror" in location.name
            or location in dragons_lair
            or location in chimeras_keep
            or location in gates_of_the_underworld
            or location.id in no_obelisks
    ] + [location for location in all_locations if "Obelisk" in location.name and world.options.obelisks == 1]:
        for item in obelisks:
            if location.name not in world.disabled_locations:
                forbid_item(world.get_location(location.name), item, world.player)

    if not world.options.instant_max:
        for level_id, locations in level_locations.items():
            for location in locations:
                if location.difficulty > 1:
                    if location.name not in world.disabled_locations:
                        add_rule(
                            world.get_location(location.name),
                            lambda state, level_id_=level_id >> 4, difficulty=location.difficulty - 1:
                            state.has("stones", world.player, difficulty_lambda[level_id_][difficulty])
                            )
