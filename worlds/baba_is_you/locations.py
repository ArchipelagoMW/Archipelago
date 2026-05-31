from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from .levels import LEVEL_DATA, get_level_locations

if TYPE_CHECKING:
    from .world import BabaIsYouWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {}

# Define location groups
location_name_groups = {
    "Level Wins": set(),
    "Level Bonuses": set(),
    "Level Transforms": set(),
    "World Clears": set(),
    "World Completes": set(),
}

# Set up location ids
locationID = 1
for name in LEVEL_DATA:
    data = LEVEL_DATA[name]
    
    for locationName in get_level_locations(data, None):
        LOCATION_NAME_TO_ID[locationName] = locationID
        locationID += 1

        group = ""
        if locationName.endswith("Win"):
            group = "Level Wins"
        elif locationName.endswith("Bonus"):
            group = "Level Bonuses"
        elif locationName.endswith("Transform"):
            group = "Level Transforms"
        elif locationName.endswith("Clear"):
            group = "World Clears"
        elif locationName.endswith("Complete"):
            group = "World Completes"
        if len(group) != 0:
            location_name_groups[group].add(locationName)


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class BabaIsYouLocation(Location):
    game = "Baba Is You"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: BabaIsYouWorld) -> None:
    create_locations(world)
    create_events(world)


def create_locations(world: BabaIsYouWorld) -> None:
    # Add each level's win, clears, completes, and bonuses as locations
    # Also add transforms if transformsanity is enabled
    for name in LEVEL_DATA:
        data = LEVEL_DATA[name]
        if data.get("areaAccess", 0) > world.options.area_access or data.get("checkAreaAccess", 0) > world.options.area_access:
            continue

        if world.options.level_shuffle != 0:
            name = world.level_shuffle_dict.get(name, name)
            data = LEVEL_DATA[name]
        
        level = world.get_region(name)
        loc_list = get_level_locations(data, world)

        level_locations = get_location_names_with_ids(loc_list)
        level.add_locations(level_locations, BabaIsYouLocation)


def create_events(world: BabaIsYouWorld) -> None:
    # Create goal event (not applicable to level or blossom goal)

    region = None
    if world.options.goal == 0:
        region = world.get_region("Map-Finale")
    elif world.options.goal == 1:
        region = world.get_region("???")
    elif world.options.goal == 2:
        region = world.get_region("Depths")
    elif world.options.goal == 3:
        region = world.get_region("Meta")
    elif world.options.goal == 4:
        region = world.get_region("Center")
        
    if region is not None:
        region.add_event(
            "Goal Reached", "goal_reached", location_type=BabaIsYouLocation, item_type=items.BabaIsYouItem
        )
