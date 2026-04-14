from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region, CollectionState
from rule_builder.rules import And, CanReachRegion, Has, HasAny, HasAll, Or, Rule, True_

from .levels import LEVEL_DATA, can_win

if TYPE_CHECKING:
    from .world import BabaIsYouWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).

def create_and_connect_regions(world: BabaIsYouWorld) -> None:
    create_all_regions(world)
    handle_level_shuffle(world)
    connect_regions(world)


def create_all_regions(world: BabaIsYouWorld) -> None:
    regions = []

    # Add each map/level as a region
    for name in LEVEL_DATA:
        data = LEVEL_DATA[name]
        level = Region(name, world.player, world.multiworld, data["name"])
        regions.append(level)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: BabaIsYouWorld) -> None:
    # Handle level connections, including rules (considers level shuffle)
    for orgName in LEVEL_DATA:
        name = orgName
        data = LEVEL_DATA[orgName]
        parent = data.get("parent")
        connections = data.get("connects")
        if world.options.level_shuffle != 0 and world.level_shuffle_dict.get(name) != None:
            name = world.level_shuffle_dict.get(name)
            data = LEVEL_DATA[name]

        level = world.get_region(name)
        if connections != None:
            for orgOtherRegion in connections:
                otherRegion = orgOtherRegion
                if world.options.level_shuffle != 0 and world.level_shuffle_dict.get(otherRegion) != None:
                    otherRegion = world.level_shuffle_dict.get(otherRegion)
                
                entranceName = name + " -> " + otherRegion
                subLevel = world.get_region(otherRegion)
                level.connect(subLevel)
                entrance = world.get_entrance(entranceName)

                rule = True_()
                data2 = LEVEL_DATA[otherRegion]
                if world.options.world_keys and data2.get("key") != None:
                    rule = rule & Has(data2.get("key"))
                
                # Add connection rules, ignoring for map levels if open map is enabled
                connectRule = connections.get(orgOtherRegion)
                if (connectRule is not None) and (parent != "Map" or not world.options.open_map):
                    rule = rule & connectRule(name, world.options.logic_difficulty)
                
                world.set_rule(entrance, rule)

# Handle level shuffling
def handle_level_shuffle(world: BabaIsYouWorld) -> None:
    world.level_shuffle_dict = {}
    if world.options.level_shuffle == 0:
        return
    
    # Make a dictionary of each level swap
    clearable_level_list = [] # levels we can already clear
    other_level_list = [] # levels that we still need at least one item for
    starting_level_list = [] # starting levels (Map 0-7)
    level_list = [] # every other level
    for name in LEVEL_DATA:
        data = LEVEL_DATA[name]
        if data.get("map") != True and name != "Map-Finale":
            if data.get("starting") == True:
                starting_level_list.append(name)
            else:
                level_list.append(name)
            rule = can_win(name, world.options.logic_difficulty)
            clearable = (rule is None)

            # When default words is on, include levels that only require those words as clearable
            if (not clearable) and (world.options.start_with_default_words):
                difficulty = data.get("defaultWordOnlyDiff")
                if difficulty is None:
                    difficulty = 99
                clearable = (difficulty <= world.options.logic_difficulty)
            
            if clearable:
                clearable_level_list.append(name)
            else:
                other_level_list.append(name)
    
    # Reverse level list and starting list so they are in order
    starting_level_list.reverse()
    level_list.reverse()
    
    # Shuffle clearable levels and use these for the starting levels
    world.random.shuffle(clearable_level_list)
    while len(starting_level_list) != 0 and len(clearable_level_list) != 0:
        world.level_shuffle_dict[starting_level_list.pop()] = clearable_level_list.pop()
    
    if len(clearable_level_list) != 0:
        # Add left-over clearable levels to the other list
        while len(clearable_level_list) != 0:
            other_level_list.append(clearable_level_list.pop())
    elif len(starting_level_list) != 0:
        # Add left-over starting levels to the full list. Not an ideal scenario, since it could lead to restrictive starts.
        while len(starting_level_list) != 0:
            level_list.append(starting_level_list.pop())
    
    # Shuffle remaining levels
    world.random.shuffle(other_level_list)
    while len(level_list) != 0:
        world.level_shuffle_dict[level_list.pop()] = other_level_list.pop()