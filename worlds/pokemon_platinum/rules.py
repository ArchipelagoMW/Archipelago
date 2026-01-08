# rules.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, set_rule

from .data import encounters as encounterdata, Hm, items as itemdata, regions as regiondata, rules as ruledata
from .locations import is_location_in_world, get_parent_region
from .regions import is_event_region_enabled, is_region_enabled

if TYPE_CHECKING:
    from . import PokemonPlatinumWorld

def always_true(_: CollectionState) -> bool:
    return True

def is_location_present(label: str, world: "PokemonPlatinumWorld") -> bool:
    if label.startswith("event_") and is_event_region_enabled(label, world.options):
        return True
    parent_region = get_parent_region(label, world)
    return is_region_enabled(parent_region, world.options) and is_location_in_world(label, world)

def set_rules(world: "PokemonPlatinumWorld") -> None:
    common_rules = {}
    for hm in Hm:
        if world.options.requires_badge(hm.name):
            rule = ruledata.create_hm_badge_rule(hm, world.player)
        else:
            rule = always_true
        common_rules[f"{hm.name.lower()}_badge"] = rule
    rules = ruledata.Rules(world.player, common_rules, world.options)

    rules.fill_rules()

    for (src, dest), rule in rules.exit_rules.items():
        if is_region_enabled(src, world.options) and is_region_enabled(dest, world.options):
            set_rule(world.multiworld.get_entrance(f"{src} -> {dest}", world.player), rule)

    for name, rule in rules.location_rules.items():
        if is_location_present(name, world):
            set_rule(world.multiworld.get_location(name, world.player), rule)

    for loc in world.multiworld.get_locations(world.player):
        if loc.type in rules.location_type_rules: # type: ignore
            add_rule(loc, rules.location_type_rules[loc.type]) # type: ignore

    for region_name, region_data in regiondata.regions.items():
        header = region_data.header
        if is_region_enabled(region_name, world.options) and header in encounterdata.encounters:
            for type, rule in rules.encounter_type_rules.items():
                if type in region_data.accessible_encounters and getattr(encounterdata.encounters[header], type):
                    add_rule(world.multiworld.get_entrance(f"{region_name} -> {header}_{type}", world.player), rule)

    match world.options.goal.value:
        case 0:
            goal_event = "event_beat_cynthia"
        case _:
            raise ValueError(f"invalid goal {world.options.goal}")
    world.multiworld.completion_condition[world.player] = lambda state : state.has(goal_event, world.player)

