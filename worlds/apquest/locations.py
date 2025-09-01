from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import APQuestWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    "Top Left Room Chest": 1,
    "Top Middle Chest": 2,
    "Bottom Left Chest": 3,
    "Bottom Left Extra Chest": 4,
    "Bottom Right Room Left Chest": 5,
    "Bottom Right Room Right Chest": 6,
    "Right Room Enemy Drop": 10,  # Location IDs don't need to be sequential, as long as they're unique
}


# It is common practice to override the base Location class to override the "game" field.
class APQuestLocation(Location):
    game = "APQuest"


def create_all_locations(world: "APQuestWorld") -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: "APQuestWorld") -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    overworld = world.get_region("Overworld")
    top_left_room = world.get_region("Top Left Room")
    bottom_right_room = world.get_region("Bottom Right Room")
    right_room = world.get_region("Right Room")

    # One way to create locations is by just creating them directly via their constructor.
    bottom_left_chest = APQuestLocation(
        world.player, "Bottom Left Chest", world.location_name_to_id["Bottom Left Chest"], overworld
    )

    # You can then add them to the region.
    overworld.locations.append(bottom_left_chest)

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # You also need to pass your overridden Location class.
    bottom_right_room_locations: dict[str, int | None] = {
        "Bottom Right Room Left Chest": world.location_name_to_id["Bottom Right Room Left Chest"],
        "Bottom Right Room Right Chest": world.location_name_to_id["Bottom Right Room Right Chest"],
    }
    bottom_right_room.add_locations(bottom_right_room_locations, APQuestLocation)

    top_left_room_locations: dict[str, int | None] = {
        "Top Left Room Chest": world.location_name_to_id["Top Left Room Chest"],
    }
    top_left_room.add_locations(top_left_room_locations, APQuestLocation)

    right_room_locations: dict[str, int | None] = {
        "Right Room Enemy Drop": world.location_name_to_id["Right Room Enemy Drop"],
    }
    right_room.add_locations(right_room_locations, APQuestLocation)

    # Locations may be in different regions depending on the player's options.
    # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    top_middle_room_locations: dict[str, int | None] = {
        "Top Middle Chest": world.location_name_to_id["Top Middle Chest"],
    }
    if world.options.hammer:
        top_middle_room = world.get_region("Top Middle Room")
        top_middle_room.add_locations(top_middle_room_locations, APQuestLocation)
    else:
        overworld.add_locations(top_middle_room_locations, APQuestLocation)

    # Locations may exist only if the player enables certain options.
    # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    if world.options.extra_starting_chest:
        # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
        # exist, it must still always be present in the world's location_name_to_id.
        # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
        bottom_left_extra_chest = APQuestLocation(
            world.player, "Bottom Left Extra Chest", world.location_name_to_id["Bottom Left Extra Chest"], overworld
        )
        overworld.locations.append(bottom_left_extra_chest)


def create_events(world: "APQuestWorld") -> None:
    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    top_left_room = world.get_region("Top Left Room")
    final_boss_room = world.get_region("Final Boss Room")

    # One way to create an event is simply to use one of the normal methods of creating a location.
    button_in_top_left_room = Location(world.player, "Top Left Room Button", None, top_left_room)
    top_left_room.locations += [button_in_top_left_room]

    # We then need to put an event item onto the location. Item creation is discussed more in create_items().
    button_item = items.APQuestItem("Top Left Room Button Pressed", ItemClassification.progression, None, world.player)
    button_in_top_left_room.place_locked_item(button_item)

    # A way simpler way to do this is by using the region.create_event helper.
    # Luckily, we have another event we want to create: The Victory event.
    # We will use this event to track whether the player can win the game.
    # The Victory event is a completely optional abstraction - This will be discussed more in set_rules().
    final_boss_room.add_event(
        "Final Boss Defeated", "Victory", location_type=APQuestLocation, item_type=items.APQuestItem
    )

    # If you create all your regions and locations line-by-line like this,
    # the length of your create_regions might get out of hand.
    # Many worlds use more data-driven approaches using dataclasses or NamedTuples.
    # However, it is worth understanding how the actual creation of regions and locations works,
    # That way, we're not just mindlessly copy-pasting! :)
