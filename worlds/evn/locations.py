from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, TypedDict, Set
# NOTE: This allows us to log to the console. However, we dev'ed in a venv setup
# that VSCode setup for python 3.13.11...
# If we include this import in final build, AP launcher will fail to generate yaml
# due to bad reference (it won't have the virtual environment)
# NOTE: Include only when testing!
# from venv import logger
import logging
logger = logging.getLogger("EV Nova")

from BaseClasses import Location

from .rezdata import misns
from .apdata.customoutf import cust_outf_table
from .logics import possible_regions, misns_to_ignore

from .apdata.offsets import offsets_table as loc_type_offset, STARTING_ID, MAX_OUTFITS, HIGHEST_OUTFIT_ID, custom_outfits_ratio

# import random

if TYPE_CHECKING:
    from .world import EVNWorld

GAME_NAME = "EV Nova"

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location isn't used based on specific options settings, it must be present in this lookup.
# "Locations" == "checks". (Namely missions, with additional from custom outfits)
# We may be able to expand that later, depending on game engine bit setting logic.

# NOTE: A word of caution - the custom locations is... messy.
#   In an attempt to make them dynamically created, some awkward this have been done
#   that I generally wouldn't recommend following as a design style.
#   We lose IDs and have to regularly re-lookup our own locations because of this.

class EVNLocationData(TypedDict, total=False): 
    name: str
    address: Optional[int]
    #parent_region: Optional[Region]

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class EVNLocation(Location):
    game = GAME_NAME

# NOTE: This is *NOT* the base class get_locations of multiworld.
# Accidentally named the same thing. Ref'd only by ev_location_bank.
def get_locations() -> Dict[int, EVNLocationData]:
    """
    Returns a dictionary of EVN Locations that include:
    Missions, Custom Outfits.
    These are not filtered. Contains all data from source data files.
    """
    # wild. For some reason this was updating ev_item_bank, but treating item_name_to_id as a local variable and not updating it, even though we declared it as global. So, explicity informing the function that both are globals.
    ret_data: Dict[int, EVNLocationData] = {}

    # Missions
    for mission in misns.misn_table.keys():
        temp_mission = misns.misn_table[mission]
        #logger.info(f"loc type offset {loc_type_offset['misn']}")
        loc_id = loc_type_offset.get("misn", 0) + (int)(temp_mission["id"]) # Probably a safer way to test this? Fails if not int somehow probably.
        #logger.info(f"creating location for mission {temp_mission['name']} with id {loc_id}. final name: {temp_mission['name'].strip() + '-' + temp_mission['id']}")
        ret_data[loc_id] = EVNLocationData(
            # adding ID to name to ensure uniqueness. We could also add the subname if we wanted, but ID is probably safer.
            name=temp_mission["name"].strip() + "-" + temp_mission["id"], 
            address=loc_id,
        )

    # # Custom outf checks

    # Dynamically fill up on shop checks (custom outfits)
    # NOTE: The client starts IDs at STARTING_ID and, for this resource, has MAX_OUTFITS of IDs.
    #   HIGHEST_OUTFIT_ID is the highest ID currently consumed by game data.
    start_id = HIGHEST_OUTFIT_ID
    total_entries = STARTING_ID + MAX_OUTFITS - start_id
    
    # Calculate how many entries each ShopCheck should get based on chance
    allocations = []
    total_allocated = 0
    for check in custom_outfits_ratio.values():
        count = int(check["chance"] * total_entries)
        allocations.append((check, count))
        total_allocated += count
    
    # Handle rounding remainder by adding to the first item
    remainder = total_entries - total_allocated
    if remainder > 0 and allocations:
        allocations[0] = (allocations[0][0], allocations[0][1] + remainder)
    
    # Create location entries
    current_id = start_id + loc_type_offset.get("outf_cks", 0)  # Start after the last outf ID
    for check, count in allocations:
        for _ in range(count):
            ret_data[current_id] = EVNLocationData(
                name=check["name"].strip() + " - (" + str(current_id) + ")",
                address=current_id
            )
            current_id += 1

    return ret_data
    

# the int key will be our control bit used by the client to identify the item
ev_location_bank = get_locations()

def get_location_ids() -> Dict[str, int]:
    global ev_location_bank

    return {data["name"]: item_id for item_id, data in ev_location_bank.items()}

loc_name_to_id = get_location_ids()

def get_location_inverted_lookup() -> Dict[int, str]:
    global loc_name_to_id
    return {v: k for k, v in loc_name_to_id.items()}

loc_id_to_name = get_location_inverted_lookup()

def get_location_name_groups() -> Dict[str, Set[str]]:
    """
    Returns a dictionary of region names (from logics) with their used missions' names.
    A mission might be in multiple regions, but not all regions are used for every run.
    Includes a region for custom outfits (shop checks).
    Does *not* include the universe region at this time (all missions not in other regions).
    """
    # NOTE: Our "regions" from logics.py are not inherrently true regions.
    #       We use them as model data for creating our server regions, and 
    #       they serve well for location name groups too.
    # Let's utilize our own id to name lookup
    global loc_id_to_name
    # This is the expected structure for worlds.location_name_groups
    ret_dict: Dict[str, Set[str]] = {}
    outf_locations: Set[str] = set() # apparently {} is specifically a dictionary

    # Let's loop through our definied regions from logics. Not filtered - all regions.
    for region_id, region_data in possible_regions.items():
        region_locations: Set[str] = set()
        # loop through the missions used by that region.
        for mission_id in region_data["missions"]:
            loc_id = mission_id + loc_type_offset["misn"]
            region_locations.add(loc_id_to_name[loc_id])
        ret_dict[region_data["name"]] = region_locations

    # TODO: 1. No longer using this file
    #   2. If we still want to include cust_outf name groups, then we should separate based on value
    #   ex: "Custom Outf - 5k", "Custom Outf - 750k"
    #   So users can exclude price points they don't want.
    # # Add out custom outf (shop checks)
    # for coutf in cust_outf_table.keys():
    #     temp_outf = cust_outf_table[coutf]
    #     loc_id = loc_type_offset["outf_cks"] + (int)(temp_outf["id"])
    #     outf_locations.add(loc_id_to_name[loc_id])

    # ret_dict["Custom Outf (Shop Checks)"] = outf_locations

    return ret_dict

location_name_groups = get_location_name_groups()
    

def get_location_names_with_ids(world: EVNWorld, location_names: list[str]) -> Dict[str, int | None]:
    ret_dict: Dict[str, int | None] = {}
    for name in location_names:
        if name in loc_name_to_id:
            ret_dict[name] = loc_name_to_id[name]
        else:
            ret_dict[name] = None
            # logger.info(f"location id not found for {name}")
    return ret_dict

def create_all_locations(world: EVNWorld) -> None:
    total_locations = 0
    total_locations += create_universe_locations(world)
    #logger.info(f"Total universe locations created: {total_locations}")
    total_locations += create_regular_locations(world)
    #logger.info(f"Total regular locations created: {total_locations}")
    total_locations += create_custom_locations(world, total_locations)
    #logger.info(f"Total locations created: {total_locations}")
  
  
def create_universe_locations(world: EVNWorld) -> int:
    """
    Populates the default universe region with all locations not used by a story string.
    This may not technically need to be separate from create_regular_locations, but it is for now.
    
    :param world: the current world object being populated with data
    :type world: EVNWorld
    """
    # Get our default region, "Universe", as defined in world (Other games may use a different name)
    universe = world.get_region("Universe")
    misn_offset = loc_type_offset.get("misn", 0)
    coutf_offset = loc_type_offset.get("outf_cks", 0)
    total_locations = 0

    chosen_route = world.get_chosen_string()

    # Check if location used by any story regions
    for key, loc in ev_location_bank.items():
        loc_found = False

        # We already handled the custom outfits, so skip them here.
        if key > coutf_offset: # misn is 2k but outf_cks is 4k, so we know here this is an okay check
            continue

        # misns
        # Find the original misn ID before offset
        offset_key = key - misn_offset

        # first, check if it is a link mission and auto-ignore
        if offset_key in misns_to_ignore:
            continue

        # is the mission used by a storyline?
        # If the misn id is listed in the region of *any* storyline (not just the chosen one)
        # then it will be skipped.
        # However, it will only get added to the pool (in the next function) if it is part of
        # the *chosen* storyline.
        # This is neat in that a storyline doesn't have to list missions that belong to another
        # storyline and thus won't be accessible in game (as saves can only play through 1 storyline)
        # This side effect is that the size of the pool of locations *changes* based on the storyline chosen.
        for rid, sreg in possible_regions.items():
            if offset_key in sreg["missions"]:
                loc_found = True
                #logger.info(f"found offset {offset_key} key in {sreg['name']}")
                break
        
        # if so, skip it. It is populated in the next function.
        if loc_found:
            continue

        # If it wasn't found, add it to our default region
        universe.add_locations(
            get_location_names_with_ids(world, [loc["name"]])
            , EVNLocation
        )
        total_locations += 1
        #logger.info(f"added to universe: {key} - {offset_key} - {loc['name']}")

    return total_locations


def create_regular_locations(world: EVNWorld) -> int:
    """
    Populate regions other than the default universe with their defined locations
    based on logics.py
    """
    # Finally, we need to put the Locations ("checks") into their regions.
    total_locations = 0

    misn_offset = loc_type_offset.get("misn", 0)

    chosen_route = world.get_chosen_string()
    for key in chosen_route["regions"]:
        sregion = possible_regions[key]
        # get the region object we'll add locations to
        world_region = world.get_region(sregion["name"])
        for misnid in sregion["missions"]:
            loc = ev_location_bank[misnid + misn_offset]
            world_region.add_locations(
                get_location_names_with_ids(world, [loc["name"]])
                , EVNLocation
            )
            total_locations += 1
    return total_locations

def create_custom_locations(world: EVNWorld, current_location_count: int) -> int:
    """
    Populate shop checks
    """
    # Finally, we need to put the Locations ("checks") into their regions.
    total_locations = 0

    coutf_offset = loc_type_offset.get("outf_cks", 0)
    chosen_route = world.get_chosen_string()
    universe = world.get_region("Universe")

    # 1. We need to determine how many locations we still need
    #   This can be affected by multiple things:
    #   a. We *could* try to get how many items will be in the pool, but that's weird
    #       cross contamination... For now, we'll stick with chosen_string's "use_cust_outfs_count"
    #   b. Any excluded locations OR location name groups...
    #       If we overshoot, it's fine, the filler items can pick up the slack later. We just can't undershoot.
    chosen_routes_outf_count = chosen_route.get("use_cust_outfs_count", 0)

    exclusions = world.options.exclude_locations
    total_excluded = 0

    # TODO: Test that this is behaving as expected
    for ex_loc in exclusions.value:
        # Is it a name group
        if ex_loc in location_name_groups:
            for _ in location_name_groups.get(ex_loc):
                total_excluded += 1
        # or just a regular location
        else:
            total_excluded += 1

    total_needed = chosen_routes_outf_count + total_excluded
    # NOTE: Why aren't we using total_locations?
    #   Well, if we were calculating the actual total items, then it would be
    #   total_needed = total_excluded + (total_items - total_locations)
  

    # 2. Get the custom locations from the index and copy into a list we can manipulate
    #   We know where these start due to the offset.
    custom_locations_dict = {key: value for key, value in ev_location_bank.items() if key > coutf_offset}
    custom_locations_list = list(custom_locations_dict.keys())

    # 3. Randomize the list (using world's seeded random) and pull the amount we need.
    world.random.shuffle(custom_locations_list)

    while world.options.include_outfits and total_locations < total_needed and len(custom_locations_list) > 0:
        #logger.info(f"copied chosen route cust out list: {len(pick_list)}; {pick_list}")
        coutf = custom_locations_list.pop()
        # The offset is important, otherwise we'd pick the id of a different item
        loc = ev_location_bank[coutf] # + loc_type_offset["outf_cks"]]
        universe.add_locations(
            get_location_names_with_ids(world, [loc["name"]])
            , EVNLocation
        )
        total_locations += 1

    return total_locations
