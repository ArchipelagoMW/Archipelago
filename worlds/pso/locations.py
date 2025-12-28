from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import ItemClassification, Location, Region

from . import items
from .strings.region_names import Region as RegionName

if TYPE_CHECKING:
    from .world import PSOWorld

# This is the initial implementation for Location Data
# It will likely need to be expanded to include things like memory info
class PSOLocationData(NamedTuple):
    """
    Additional Data for working with Locations in PSO

    :param id: Unique ID used to identify this location to Archipelago
    :param region: Which in-game Region of PSO this item resides
    """

    id: int | None
    region: str

LOCATION_TABLE: dict[str, PSOLocationData] = {
    "Forest Boss Drop": PSOLocationData(
        0, "Forest Boss"
    ),
    "Caves Boss Drop": PSOLocationData(
        1, "Caves Boss"
    ),
    "Mines Boss Drop": PSOLocationData(
        2, "Mines Boss"
    ),
    "Dark Falz Drop": PSOLocationData(
        3, "Dark Falz"
    )
}

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

# TODO: Make sure this actually extracts the ID from the PSOLocationData tuple
def get_location_name_to_id_dict(location_table: dict[str, PSOLocationData]) -> dict[str, int | None]:
    name, id, _ = zip(*location_table)
    return {name: id}

LOCATION_NAME_TO_ID: dict[str, int | None] = get_location_name_to_id_dict(LOCATION_TABLE)

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class PSOLocation(Location):
    game = "PSO"

# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_TABLE[location_name].id for location_name in location_names}
    # return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: PSOWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: PSOWorld) -> None:
    forest_boss = world.get_region(RegionName.forest_boss)
    caves_boss = world.get_region(RegionName.caves_boss)
    mines_boss = world.get_region(RegionName.mines_boss)
    dark_falz = world.get_region(RegionName.dark_falz)

    forest_boss_locations = get_location_names_with_ids(["Forest Boss Drop"])
    forest_boss.add_locations(forest_boss_locations, PSOLocation)

    caves_boss_locations = get_location_names_with_ids(["Cave Boss Drop"])
    caves_boss.add_locations(caves_boss_locations, PSOLocation)

    mines_boss_locations = get_location_names_with_ids(["Mines Boss Drop"])
    mines_boss.add_locations(mines_boss_locations, PSOLocation)

    dark_falz_locations = get_location_names_with_ids(["Dark Falz"])
    dark_falz.add_locations(dark_falz_locations, PSOLocation)

    # Locations may be in different regions depending on the player's options.
    # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    # top_middle_room_locations = get_location_names_with_ids(["Top Middle Chest"])
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     top_middle_room.add_locations(top_middle_room_locations, PSOLocation)
    # else:
    #     overworld.add_locations(top_middle_room_locations, PSOLocation)

    # Locations may exist only if the player enables certain options.
    # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    # if world.options.extra_starting_chest:
    #     # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
    #     # exist, it must still always be present in the world's location_name_to_id.
    #     # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
    #     bottom_left_extra_chest = get_location_names_with_ids(["Bottom Left Extra Chest"])
    #     overworld.add_locations(bottom_left_extra_chest, PSOLocation)


def create_events(world: PSOWorld) -> None:
    dark_falz = world.get_region("Dark Falz")

    dark_falz.add_event(
        "Dark Falz Defeated", "Victory", location_type=PSOLocation, item_type=items.PSOItem
    )

    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    # top_left_room = world.get_region("Top Left Room")
    # final_boss_room = world.get_region("Final Boss Room")

    # One way to create an event is simply to use one of the normal methods of creating a location.
    # button_in_top_left_room = PSOLocation(world.player, "Top Left Room Button", None, top_left_room)
    # top_left_room.locations.append(button_in_top_left_room)

    # We then need to put an event item onto the location.
    # An event item is an item whose code is "None" (same as the event location's address),
    # and whose classification is "progression". Item creation will be discussed more in items.py.
    # Note: Usually, items are created in world.create_items(), which for us happens in items.py.
    # However, when the location of an item is known ahead of time (as is the case with an event location/item pair),
    # it is common practice to create the item when creating the location.
    # Since locations also have to be finalized after world.create_regions(), which runs before world.create_items(),
    # we'll create both the event location and the event item in our locations.py code.
    # button_item = items.PSOItem("Top Left Room Button Pressed", ItemClassification.progression, None, world.player)
    # button_in_top_left_room.place_locked_item(button_item)
