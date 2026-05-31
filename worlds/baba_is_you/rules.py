from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from . import items
from .levels import LEVEL_DATA, can_win, can_bonus, can_transform, is_level_winnable, has_any_transform
from .locations import BabaIsYouLocation
from rule_builder.rules import And, CanReachRegion, Has, HasAny, HasAll, Or, Rule, True_

if TYPE_CHECKING:
    from .world import BabaIsYouWorld


def set_all_rules(world: BabaIsYouWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_up_gates(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_up_gates(world: BabaIsYouWorld) -> None:
    # Set up gates for specific areas
    def check_first_gate(state: CollectionState):
        return get_blossom_count(state, world) >= world.options.first_gate_blossoms

    def check_second_gate(state: CollectionState):
        return get_blossom_count(state, world) >= world.options.second_gate_blossoms
    
    def check_third_gate(state: CollectionState):
        return get_blossom_count(state, world) >= world.options.third_gate_blossoms
    
    # Gate to A Way Out?
    a_way_out = world.get_region("Map-Finale")
    for entrance in a_way_out.entrances:
        if entrance.parent_region.name == "Map": continue # exception for Baba transform
        add_rule(entrance, check_first_gate)

    # Gate to Cavern
    cavern = world.get_region("Cavern")
    for entrance in cavern.entrances:
        if entrance.parent_region.name == "Map": continue # exception for Baba transform
        add_rule(entrance, check_second_gate)

    # Gate to Slideshow
    if world.options.area_access > 0:
        slideshow = world.get_region("Map-8")
        if world.options.level_shuffle != 0:
            slideshow = world.get_region(world.level_shuffle_dict.get("Map-8", "Map-8"))
        for entrance in slideshow.entrances:
            add_rule(entrance, check_third_gate)

    # Conditions for ending
    if world.options.goal == 0:
        ending = world.get_location("Goal Reached")
        a_way_out_rule = can_win("Map-Finale", world.options.logic_difficulty)
        world.set_rule(ending, a_way_out_rule & Has("End"))

def set_all_location_rules(world: BabaIsYouWorld) -> None:
    # Set up win, clear, complete, transform, and bonus location logic
    for name in LEVEL_DATA:
        data = LEVEL_DATA[name]
        if data.get("areaAccess", 0) > world.options.area_access or data.get("checkAreaAccess", 0) > world.options.area_access:
            continue # skip non-accessible areas

        parent = data.get("parent") # Get parent of old level
        if world.options.level_shuffle != 0:
            name = world.level_shuffle_dict.get(name, name)
            data = LEVEL_DATA[name]

        # Win rule
        if is_level_winnable(data):
            locationName = data["name"] + ": Win"
            location = world.get_location(locationName)

            rule = can_win(name, world.options.logic_difficulty)
            world.set_rule(location, rule)

            # Create win event with same logic as winning using parent
            if parent is not None:
                region = world.get_region(name)
                region.add_event(location_name = locationName + " Event", item_name = f"{parent} Win", location_type=BabaIsYouLocation, item_type=items.BabaIsYouItem, rule=rule)

        # Bonus rule
        if data.get("bonusLogic") is not None:
            locationName = data["name"] + ": Bonus"
            location = world.get_location(locationName)

            rule = can_bonus(name, world.options.logic_difficulty)
            world.set_rule(location, rule)
        
        # Transform rules
        if has_any_transform(data, world):
            for transform in data["transforms"]:
                locationName = f"{data["name"]}: {transform} Transform"
                rule = can_transform(name, transform, world.options.logic_difficulty)
                
                if world.options.transformsanity and transform.find("+") == -1: # combo transforms are only used for logic
                    location = world.get_location(locationName)
                    world.set_rule(location, rule)
                
                # Create event with same logic
                region = world.get_region(name)
                region.add_event(location_name = locationName + " Event", item_name = f"{data["name"]} -> {transform}", location_type=BabaIsYouLocation, item_type=items.BabaIsYouItem, rule=rule)
        
        # Add clear and completion checks for maps
        if data.get("clearCount") is not None:
            wins = data.get("clearCount")
            locationName = data["name"] + ": Clear"
            itemName = f"{name} Win"
            location = world.get_location(locationName)
            
            world.set_rule(location, Has(itemName, wins))
        if world.options.complete_checks and data.get("completeCount") is not None:
            wins = data.get("completeCount")
            locationName = data["name"] + ": Complete"
            itemName = f"{name} Win"
            location = world.get_location(locationName)
            
            world.set_rule(location, Has(itemName, wins))

def set_completion_condition(world: BabaIsYouWorld) -> None:
    if world.options.goal <= 4: # end, flower, depths, meta
        world.set_completion_rule(Has("goal_reached"))
    elif world.options.goal == 5: # levels
        world.multiworld.completion_condition[world.player] = lambda state: get_win_count(state, world) >= world.options.goal_levels
    elif world.options.goal == 6: # blossoms
        world.multiworld.completion_condition[world.player] = lambda state: get_blossom_count(state, world) >= world.options.goal_blossoms

# Count blossoms from petals and normal
def get_blossom_count(state: CollectionState, world: BabaIsYouWorld):
    petals = state.count("Blossom Petal", world.player)
    blossoms = state.count("Blossom", world.player) + (petals // 8)
    return blossoms

# Manually count the wins from each map.
# NOTE: Needs to be manually updated when late game is added
def get_win_count(state: CollectionState, world: BabaIsYouWorld):
    wins = state.count("Map Win", world.player)
    wins += state.count("Lake Win", world.player)
    wins += state.count("Island Win", world.player)
    wins += state.count("Ruins Win", world.player)
    wins += state.count("Fall Win", world.player)
    wins += state.count("Forest Win", world.player)
    wins += state.count("Space Win", world.player)
    wins += state.count("Garden Win", world.player)
    wins += state.count("Chasm Win", world.player)
    wins += state.count("Cavern Win", world.player)
    wins += state.count("Mountain Win", world.player)
    wins += state.count("??? Win", world.player)
    wins += state.count("ABC Win", world.player)
    wins += state.count("Null Win", world.player)
    wins += state.count("Depths Win", world.player)
    wins += state.count("Meta Win", world.player)
    wins += state.count("Center Win", world.player)
    return wins