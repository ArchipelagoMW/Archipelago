from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from .locationData import questLocations

if TYPE_CHECKING:
    from .world import CatQuestWorld


def set_all_rules(world: CatQuestWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_location_rules(world: CatQuestWorld) -> None:
    for loc in questLocations:
        if loc["art"] == "water":
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has("Royal Art of Water Walking", world.player))
        elif loc["art"] == "flight":
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has("Royal Art of Flight", world.player))
        elif loc["art"] == "both":
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has_all("Royal Art of Flight", "Royal Art of Water Walking", world.player))
        elif loc["art"] == "either":
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has_any("Royal Art of Flight", "Royal Art of Water Walking", world.player))
        
        if loc["hasFist"]:
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has_any("Flamepurr", "Lightnyan", "Freezepaw", "Cattrap", "Astropaw", world.player))

        #if world.options.include_temples:
        #for loc in templeLocations:
        #   if loc["art"] == "either":
        #    add_rule(world.get_location(loc["name"]),
        #    lambda state: state.has_any("Royal Art of Flight", "Royal Art of Water Walking", world.player))

def set_completion_condition(world: CatQuestWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has_all(("Royal Art of Water Walking", "Royal Art of Flight"), world.player)

    world.multiworld.completion_condition[world.player] = lambda state: (
        state.has("Flamepurr", world.player) or 
        state.has("Lightnyan", world.player) or 
        state.has("Cattrap", world.player) or 
        state.has("Astropaw", world.player) or 
        state.has("Freezepaw", world.player))
