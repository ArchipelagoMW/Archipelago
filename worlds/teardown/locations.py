from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import TeardownWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
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
}


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class TeardownLocation(Location):
    game = "Teardown"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: TeardownWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: TeardownWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    level_1 = world.get_region("Level 1")
    level_2 = world.get_region("Level 2")
    level_3 = world.get_region("Level 3")
    bonus_level_4 = world.get_region("Bonus Level 4")


    # One way to create locations is by just creating them directly via their constructor.
    old_building_problem = TeardownLocation(
        world.player, "Old Building Problem", world.location_name_to_id["Old Building Problem"], level_1
    )

    # You can then add them to the region.
    level_1.locations.append(old_building_problem)

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.
    level_2_locations = get_location_names_with_ids(
        ["Lee Computers Target 1", "Lee Computers Target 2", "Lee Computers Target 3"]
    )
    level_2.add_locations(level_2_locations, TeardownLocation)

    level_3_locations = get_location_names_with_ids(["Login Devices 1", "Login Devices 2", "Login Devices 3"])
    level_3.add_locations(level_3_locations, TeardownLocation)

   # level_2_locations = get_location_names_with_ids(["Lee Computers Target 1", "Lee Computers Target 2", "Lee Computers Target 3"])
   # level_2.add_locations(level_2_locations, TeardownLocation)

    # Locations may be in different regions depending on the player's options.
    # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    #bonus_level_3_locations = get_location_names_with_ids(["Login Devices 1", "Login Devices 2", "Login Devices 3"])
    #if world.options.bonus:
    #    bonus_level_3 = world.get_region("Bonus Level 3")
    #    bonus_level_3.add_locations(bonus_level_3_locations, TeardownLocation)
    #else:
    #    level_1.add_locations(bonus_level_3_locations, TeardownLocation)

    # Locations may exist only if the player enables certain options.
    # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    if world.options.Bonus_Level:
        # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
        # exist, it must still always be present in the world's location_name_to_id.
        # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
        making_space = get_location_names_with_ids(["Making Space 1", "Making Space 2", "Making Space 3"])
        bonus_level_4.add_locations(making_space, TeardownLocation)


def create_events(world: TeardownWorld) -> None:
    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    level_3 = world.get_region("Level 3")
    bonus_level_4 = world.get_region("Bonus Level 4")

        # One way to create an event is simply to use one of the normal methods of creating a location.
    #button_in_region_2 = TeardownLocation(world.player, "Region 2 Button", None, level_2)
    #level_2.locations.append(button_in_region_2)

         # We then need to put an event item onto the location.
         # An event item is an item whose code is "None" (same as the event location's address),
         # and whose classification is "progression". Item creation will be discussed more in items.py.
         # Note: Usually, items are created in world.create_items(), which for us happens in items.py.
        # However, when the location of an item is known ahead of time (as is the case with an event location/item pair),
        # it is common practice to create the item when creating the location.
        # Since locations also have to be finalized after world.create_regions(), which runs before world.create_items(),
        # we'll create both the event location and the event item in our locations.py code.
    #button_item = items.TeardownItem("Region 2 Button Pressed", ItemClassification.progression, None, world.player)
    #button_in_region_2.place_locked_item(button_item)

    # A way simpler way to do create an event location/item pair is by using the region.create_event helper.
    # Luckily, we have another event we want to create: The Victory event.
    # We will use this event to track whether the player can win the game.
    # The Victory event is a completely optional abstraction - This will be discussed more in set_rules().
    if world.options.Bonus_Level:
        bonus_level_4.add_event(
            "Final Mission Completed", "Victory", location_type=TeardownLocation, item_type=items.TeardownItem)
    else:
        level_3.add_event(
        "Final Mission Completed", "Victory", location_type=TeardownLocation, item_type=items.TeardownItem)

    # If you create all your regions and locations line-by-line like this,
    # the length of your create_regions might get out of hand.
    # Many worlds use more data-driven approaches using dataclasses or NamedTuples.
    # However, it is worth understanding how the actual creation of regions and locations works,
    # That way, we're not just mindlessly copy-pasting! :)
