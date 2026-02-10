from __future__ import annotations

from typing import TYPE_CHECKING

from worlds.generic.Rules import add_rule
from .locationData import questLocations, templeLocations #, monumentLocations
from .itemData import prog_skill_uprades, prog_skills

if TYPE_CHECKING:
    from .world import CatQuestWorld


def set_all_rules(world: CatQuestWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_location_rules(world: CatQuestWorld) -> None:
    included_locations = []

    included_locations.extend(questLocations)

    if world.options.include_temples:
        included_locations.extend(templeLocations)
    
    #if world.options.include_monuments:
    #    included_locations.extend(monumentLocations)

    for loc in included_locations:
        if loc["art"] == "water":
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has("Royal Art of Water Walking", world.player))
        elif loc["art"] == "flight":
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has("Royal Art of Flight", world.player))
        elif loc["art"] == "both":
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has_all(("Royal Art of Flight", "Royal Art of Water Walking"), world.player))
        elif loc["art"] == "either":
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has_any(("Royal Art of Flight", "Royal Art of Water Walking"), world.player))
        
        if loc["hasFist"]:
            add_rule(world.get_location(loc["name"]),
            lambda state: state.has_any(
                ("Flamepurr", "Lightnyan", "Freezepaw", "Cattrap", "Astropaw",
                 "Progressive Flamepurr", "Progressive Lightnyan", "Progressive Freezepaw", "Progressive Cattrap", "Progressive Astropaw"
                ), world.player))
            

def set_completion_condition(world: CatQuestWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: (
        state.has_all(("Royal Art of Water Walking", "Royal Art of Flight"), world.player) and 
        state.has_any(("Flamepurr", "Lightnyan", "Freezepaw", "Cattrap", "Astropaw",
                       "Progressive Flamepurr", "Progressive Lightnyan", "Progressive Freezepaw", "Progressive Cattrap", "Progressive Astropaw"
                       ), world.player)
    )
