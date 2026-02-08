from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

import re

if TYPE_CHECKING:
    from .world import EVNWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).

# Should probably create a subclass that inherits from Region for EVN-specific behavior, similar to how we did for Location.
# TODO: Add the other regions
REGION_KEYS = {
    "Universe" : [],
    "Fed String" : ["Fed"], # Fed story mission string
    "Vellos" : ["Vellos", "Vell-os"],
}

### Region subclass helper functions ###

# Let's make one more helper method before we begin actually creating locations.
# Here's a function that extracts the value following a specific character in a given text.
# Google AI
def get_value_after_char(text, char):
    # Pattern explanation:
    # (?<={char}\s*) - Positive lookbehind: asserts the position is immediately 
    #                   after the specified character and zero or more whitespaces.
    # (.*?)          - Capturing group 1: lazily matches any character (except newline) 
    #                   until the end of the line.
    #pattern = re.compile(rf'(?<={re.escape(char)}\s*)(.*?)')
    pattern = re.compile(rf'^(.*?)(?=\s+{re.escape(char)})(.*)$')
    match = pattern.search(text)
    if match:
        # returns the captured group, with leading/trailing whitespace removed
        #return match.group(1).strip() 
        return match.group(3).strip() 
    return None

def string_has_value(text, substring):
    return get_value_after_char(text.lower(), substring.lower()) is not None

def string_has_value_after_char(text, char, substring):
    value = get_value_after_char(text, char)
    if value is None:
        return False
    return substring.lower() in value.lower()

def can_accept_location(evnregion: Region, location_name: str) -> bool:
    """Helper function to determine if a region can accept a location based on keywords."""
    keywords = REGION_KEYS.get(evnregion.name, [])
    for keyword in keywords:
        #if keyword in location_name:
        if string_has_value_after_char(location_name, ";", keyword):
            return True
    return False

### End Region subclass helper functions ###


def create_and_connect_regions(world: EVNWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: EVNWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    #universe = Region("Universe", world.player, world.multiworld)
    #fed_string = Region("Fed String", world.player, world.multiworld) # Fed story mission string

    # Let's put all these regions in a list.
    #regions = [universe, fed_string]
    regions = []

    for evregion in REGION_KEYS.keys():
        regions.append(Region(evregion, world.player, world.multiworld))

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # if world.options.hammer:
    #     top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #     regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: EVNWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    universe = world.get_region("Universe")
    # fed_string = world.get_region("Fed String")

    # universe.connect(fed_string, "Universe to Fed String")
    for evregion in REGION_KEYS.keys():
        if evregion != "Universe":
            universe.connect(world.get_region(evregion), f"Universe to {evregion}")

    # Okay, now we can get connecting. For this, we need to create Entrances.
    # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    # One way to create an Entrance is by calling the Entrance constructor.
    # overworld_to_bottom_right_room = Entrance(world.player, "Overworld to Bottom Right Room", parent=overworld)
    # overworld.exits.append(overworld_to_bottom_right_room)

    # # You can then connect the Entrance to the target region.
    # overworld_to_bottom_right_room.connect(bottom_right_room)

    # # An even easier way is to use the region.connect helper.
    # overworld.connect(right_room, "Overworld to Right Room")
    # right_room.connect(final_boss_room, "Right Room to Final Boss Room")

    # # The region.connect helper even allows adding a rule immediately.
    # # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    # overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", world.player))

    # # Some Entrances may only exist if the player enables certain options.
    # # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     overworld.connect(top_middle_room, "Overworld to Top Middle Room")
