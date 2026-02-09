from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, TypedDict
from venv import logger

from BaseClasses import ItemClassification, Location, Region
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
    "misn-block": 9955,
}

class EVNLocationData(TypedDict, total=False): 
    name: str
    address: Optional[int]
    #parent_region: Optional[Region]




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

def get_locations() -> Dict[int, EVNLocationData]:
    # wild. For some reason this was updating ev_item_bank, but treating item_name_to_id as a local variable and not updating it, even though we declared it as global. So, explicity informing the function that both are globals.
    ret_data: Dict[int, EVNLocationData] = {}

    # Missions
    for mission in misns.misn_table.keys():
        temp_mission = misns.misn_table[mission]
        loc_id = loc_type_offset["misn"] + (int)(temp_mission["id"]) # Probably a safer way to test this? Fails if not int somehow probably.
        #logger.info(f"creating location for mission {temp_mission['name']} with id {loc_id}. final name: {temp_mission['name'].strip() + '-' + temp_mission['id']}")
        ret_data[loc_id] = EVNLocationData(
            name=temp_mission["name"].strip() + "-" + temp_mission["id"], # adding ID to name to ensure uniqueness. We could also add the subname if we wanted, but ID is probably safer.
            address=loc_id,
        )

    return ret_data
    
    #loc_name_to_id = {data.name: loc_id for loc_id, data in ev_location_bank.items()}  


# the int key will be our control bit used by the client to identify the item
ev_location_bank = get_locations()

def get_location_ids() -> Dict[str, int]:
    global ev_location_bank

    return {data["name"]: item_id for item_id, data in ev_location_bank.items()}

loc_name_to_id = get_location_ids()


def get_location_names_with_ids(world: EVNWorld, location_names: list[str]) -> Dict[str, int | None]:
    # Surely there is a simpler way? This seems inefficient. 
    #return ev_location_bank[[loc_id for loc_id in ev_location_bank if ev_location_bank[loc_id].name == name][0]]
    #return ev_location_bank[loc_name_to_id[name]]
    #return {name: loc_name_to_id[name] for name in location_names if name in loc_name_to_id}
    ret_dict: Dict[str, int | None] = {}
    for name in location_names:
        if name in loc_name_to_id:
            ret_dict[name] = loc_name_to_id[name]
        else:
            ret_dict[name] = None
            logger.info(f"location id not found for {name}")
    return ret_dict


def create_all_locations(world: EVNWorld) -> None:
    create_regular_locations(world)
    #create_events(world)


def create_regular_locations(world: EVNWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    universe = world.get_region("Universe")


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
            #if can_accept_location(evregion, loc.name):
            if can_accept_location(evregion, loc["name"]):
                evregion.add_locations(
                    get_location_names_with_ids(world, [loc["name"]])
                    , EVNLocation
                )
                break
        # If found above, then it should break out back to the top of this loop right?
        # So if we are here, we can assume that it is not a universe specific location and we can add it to universe.
        universe.add_locations(
            get_location_names_with_ids(world, [loc["name"]])
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