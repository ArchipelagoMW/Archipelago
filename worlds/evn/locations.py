from __future__ import annotations

from typing import TYPE_CHECKING, Dict
from venv import logger

from BaseClasses import ItemClassification, Location
from worlds.evn.regions import can_accept_location  # Is this an improper import?

from .rezdata import misns

# import re

if TYPE_CHECKING:
    from .world import EVNWorld


GAME_NAME = "EV Nova"

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
# I feel like "location" is a misnomer for a "check"
# Possible types:
#   mission completes
#   purchase items
#   first explore of a sys
#   _
# FOR TESTING
# LOCATION_NAME_TO_ID = {
#     # Location IDs don't need to be sequential, as long as they're unique and greater than 0.
#     # "Example_Mission": 10,
#     # "Fed Mission 1": 11,
#     # "Fed Mission Final": 12,
#     "Delivery to Earth; Vellos1-128": 128,
#     "Visit Vell-os Homeworld; Vellos2-129": 129,
#     "Head to Sol;Tutorial 001-251": 251,
#     "Trade between Earth and Port Kane;Tutorial 002-630": 630, # Do *not* lock progression behind this mission
#     "United Shipping Intro;United Shipping1-504": 504,
#     "Un. Shipping Delivery;United Shipping1a-505": 505,
#     "Take Polaris Home;Rebel I22 LAST-354": 354,
#     "Take Llyrell to Korell; Vellos31 LAST-417": 417,
#     "Take Krane to Earth;Fed43 LAST-474": 474,
#     "A Parting Gift;Fed26 (forced) LAST-596": 596,
#     "Return to Heraan;Auroran 029 LAST-686": 686,
#     "Destroy McGowan;Pirate 011 LAST-712": 712,
#     "Return to Ar'Za Iusia;Polaris 46-887": 887,
# }

# to add other checks, such as outfits, give them their own offset and range.
loc_type_offset: Dict[str, int] = {
    "misn": 2000,   # 2000 - 2999 will be missions. We have 1000 misns, so this should be safe.
}

# the int key will be our control bit used by the client to identify the item
ev_location_bank: Dict[int, EVNLocation] = {}

loc_name_to_id: Dict[str, int] = {}


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class EVNLocation(Location):
    #game = EVNWorld.game
    game = GAME_NAME
    # player: int
    # name: str
    # address: Optional[int]    # I think this is the location ID
    # parent_region: Optional[Region]
    # locked: bool = False
    # show_in_spoiler: bool = True
    # progress_type: LocationProgressType = LocationProgressType.DEFAULT
    # always_allow: Callable[[CollectionState, Item], bool] = staticmethod(lambda state, item: False)
    # access_rule: Callable[[CollectionState], bool] = staticmethod(lambda state: True)
    # item_rule: Callable[[Item], bool] = staticmethod(lambda item: True)
    # item: Optional[Item] = None

def create_loc_bank(world: EVNWorld) -> None:
    # wild. For some reason this was updating ev_item_bank, but treating item_name_to_id as a local variable and not updating it, even though we declared it as global. So, explicity informing the function that both are globals.
    global ev_location_bank, loc_name_to_id
    
    # Missions
    for mission in misns.misn_table.keys():
        temp_mission = misns.misn_table[mission]
        loc_id = loc_type_offset["misn"] + (int)(temp_mission["id"]) # Probably a safer way to test this? Fails if not int somehow probably.
        #logger.info(f"creating location for mission {temp_mission['name']} with id {loc_id}. final name: {temp_mission['name'].strip() + '-' + temp_mission['id']}")
        ev_location_bank[loc_id] = EVNLocation(
            world.player,
            temp_mission["name"].strip() + "-" + temp_mission["id"], # adding ID to name to ensure uniqueness. We could also add the subname if we wanted, but ID is probably safer.
            loc_id,
            world.player,
        )
    
    loc_name_to_id = {data.name: loc_id for loc_id, data in ev_location_bank.items()}  
    # logger.info(f"example location name: {ev_location_bank[2630].name}")
    # logger.info(f"mission table keys: {ev_location_bank.keys()}")
    # logger.info(f"location name to id: {loc_name_to_id.keys()}")
    # logger.info(f"example lookup: {loc_name_to_id['Trade between Earth and Port Kane;Tutorial 002-630']}")

# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
#def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    #return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}
def get_location_names_with_ids(world: EVNWorld, location_names: list[str]) -> dict[str, int | None]:
    if (not ev_location_bank or ev_location_bank == {}):
        create_loc_bank(world)
    # Surely there is a simpler way? This seems inefficient. 
    #return ev_location_bank[[loc_id for loc_id in ev_location_bank if ev_location_bank[loc_id].name == name][0]]
    #return ev_location_bank[loc_name_to_id[name]]
    return {name: loc_name_to_id[name] for name in location_names if name in loc_name_to_id}


def create_all_locations(world: EVNWorld) -> None:
    create_regular_locations(world)
    #create_events(world)


def create_regular_locations(world: EVNWorld) -> None:

    if (not ev_location_bank or ev_location_bank == {}):
        create_loc_bank(world)

    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    universe = world.get_region("Universe")

    # One way to create locations is by just creating them directly via their constructor.
    # example_mission = EVNLocation(
    #     world.player, "Example Mission", world.location_name_to_id["Example_Mission"], universe
    # )

    # # You can then add them to the region.
    # universe.locations.append(example_mission)
    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.
    # bottom_right_room_locations = get_location_names_with_ids(
    #     ["Bottom Right Room Left Chest", "Bottom Right Room Right Chest"]
    # )
    # bottom_right_room.add_locations(bottom_right_room_locations, EVNLocation)

    # universe.add_locations(
    #     get_location_names_with_ids(["Example_Mission"])
    #     , EVNLocation
    # )

    # top_left_room_locations = get_location_names_with_ids(["Top Left Room Chest"])
    # top_left_room.add_locations(top_left_room_locations, EVNLocation)

    # right_room_locations = get_location_names_with_ids(["Right Room Enemy Drop"])
    # right_room.add_locations(right_room_locations, EVNLocation)

    # # Locations may be in different regions depending on the player's options.
    # # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    # top_middle_room_locations = get_location_names_with_ids(["Top Middle Chest"])
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     top_middle_room.add_locations(top_middle_room_locations, EVNLocation)
    # else:
    #     overworld.add_locations(top_middle_room_locations, EVNLocation)

    # # Locations may exist only if the player enables certain options.
    # # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    # if world.options.extra_starting_chest:
    #     # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
    #     # exist, it must still always be present in the world's location_name_to_id.
    #     # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
    #     bottom_left_extra_chest = get_location_names_with_ids(["Bottom Left Extra Chest"])
    #     overworld.add_locations(bottom_left_extra_chest, EVNLocation)

    # fed_string = world.get_region("Fed String")
    # fed_string.add_locations(
    #     get_location_names_with_ids(["Fed Mission 1", "Fed Mission Final"])
    #     , EVNLocation
    # )

    # for evnloc in LOCATION_NAME_TO_ID.keys():
    #     if string_has_value(evnloc, "Fed Mission"):
    #         fed_string.add_locations(
    #             get_location_names_with_ids([evnloc])
    #             , EVNLocation
    #         )

    # TODO: replace with looping through out mission bank
    #for loc_name in LOCATION_NAME_TO_ID.keys():
        # for evregion in world.get_regions():
        #     if can_accept_location(evregion, loc_name):
        #         evregion.add_locations(
        #             get_location_names_with_ids(world, [loc_name])
        #             , EVNLocation
        #         )
        #         break
        # # If found above, then it should break out back to the top of this loop right?
        # # So if we are here, we can assume that it is not a universe specific location and we can add it to universe.
        # universe.add_locations(
        #     get_location_names_with_ids(world, [loc_name])
        #     , EVNLocation
        # )


    for key, loc in ev_location_bank.items():
        for evregion in world.get_regions():
            if can_accept_location(evregion, loc.name):
                evregion.add_locations(
                    get_location_names_with_ids(world, [loc.name])
                    , EVNLocation
                )
                break
        # If found above, then it should break out back to the top of this loop right?
        # So if we are here, we can assume that it is not a universe specific location and we can add it to universe.
        universe.add_locations(
            get_location_names_with_ids(world, [loc.name])
            , EVNLocation
        )

    # I don't know how I want to handle the victory conditions yet.
    # fed_string.add_event(
    #     "Fed Final Mission Complete", "Victory", location_type=EVNLocation, item_type=items.EVNItem
    # )

    # universe.add_event(
    #     "String Complete", STRING_COMPLETE_BIT, location_type=EVNLocation, item_type=items.EVNItem
    # )


# NOTE: I think that event locations and items have null ID because they exist purely for AP logic, and don't actually trade to/from the game.