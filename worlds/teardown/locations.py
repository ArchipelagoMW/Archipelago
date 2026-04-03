from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import TeardownWorld

# Locations and their IDs, must include any options or not enabled locations
LOCATION_NAME_TO_ID = {
    "Old Building Problem": 1,
    "Lee Computers Target 1": 11,
    "Lee Computers Target 2": 12,
    "Lee Computers Target 3": 13,
    "Login Devices 1": 21,
    "Login Devices 2": 22,
    "Login Devices 3": 23,
    "Making Space 1": 31,
    "Making Space 2": 32,
    "Making Space 3": 33,
    "Temp": 34,
}


class TeardownLocation(Location):
    game = "Teardown"


# Helper that helps later
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

# Creates all locations above
def create_all_locations(world: TeardownWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: TeardownWorld) -> None:
# We set our objects
    level_1 = world.get_region("Level 1")
    level_2 = world.get_region("Level 2")
    level_3 = world.get_region("Level 3")



# Sets our locations to our regions, this is easier method
    level_1_locations = get_location_names_with_ids(["Old Building Problem"])
    level_1.add_locations(level_1_locations, TeardownLocation)

    level_2_locations = get_location_names_with_ids(["Lee Computers Target 1", "Lee Computers Target 2", "Lee Computers Target 3"])
    level_2.add_locations(level_2_locations, TeardownLocation)

    level_3_locations = get_location_names_with_ids(["Login Devices 1", "Login Devices 2", "Login Devices 3", "Temp"])
    level_3.add_locations(level_3_locations, TeardownLocation)


    # Locations may be in different regions depending on the player's options.
    # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    bonus_level_4_locations = get_location_names_with_ids(["Making Space 1", "Making Space 2", "Making Space 3"])
    if world.options.Bonus_Level:
        bonus_level_4 = world.get_region("Bonus Level 4")
        bonus_level_4.add_locations(bonus_level_4_locations, TeardownLocation)
    #else:
    #    level_1.add_locations(bonus_level_4_locations, TeardownLocation)

# If bonus level is enabled, create locations and add them to bonus level 4
    #if world.options.Bonus_Level:
    #    making_space = get_location_names_with_ids(["Making Space 1", "Making Space 2", "Making Space 3"])
    #    bonus_level_4.add_locations(making_space, TeardownLocation)


#def create_events(world: TeardownWorld) -> None:
#    level_3 = world.get_region("Level 3")
#    bonus_level_4 = world.get_region("Bonus Level 4")
#
#    if world.options.Bonus_Level:
#        bonus_level_4.add_event(
#            "Final Mission Completed", "Victory", location_type=TeardownLocation, item_type=items.TeardownItem)
#    else:
#        level_3.add_event(
#        "Final Mission Completed", "Victory", location_type=TeardownLocation, item_type=items.TeardownItem)


def create_events(world: TeardownWorld) -> None:
    if world.options.Bonus_Level:
        bonus_level_4 = world.get_region("Bonus Level 4")
        bonus_level_4.add_event(
            "Final Mission Completed", "Victory", location_type=TeardownLocation, item_type=items.TeardownItem)
    else:
        level_3 = world.get_region("Level 3")
        level_3.add_event(
            "Final Mission Completed", "Victory", location_type=TeardownLocation, item_type=items.TeardownItem)
