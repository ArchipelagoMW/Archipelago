from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import Schedule1World

# Every location must have a unique integer ID associated with it.
LOCATION_NAME_TO_ID = {}
def load_locations_data(data):
    """Load location data from JSON and populate LOCATION_NAME_TO_ID."""
    global LOCATION_NAME_TO_ID
    LOCATION_NAME_TO_ID = {name: loc.modern_id for name, loc in data.locations.items()}

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class Schedule1Location(Location):
    game = "Schedule1"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: Schedule1World, locationData, eventData) -> None:
    create_regular_locations(world, locationData)
    create_events(world, eventData)


def create_regular_locations(world: Schedule1World, data) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    overworld = world.get_region("Overworld")
    missions = world.get_region("Missions")
    if world.options.randomize_business_properties or world.options.randomize_drug_making_properties:
        realtor = world.get_region("Realtor")
    
    # Customer unlock locations - add to their respective regions
    customer_region_northtown = world.get_region("Customer Northtown")
    customer_region_westville = world.get_region("Customer Westville")
    customer_region_downtown = world.get_region("Customer Downtown")
    customer_region_docks = world.get_region("Customer Docks")
    customer_region_suburbia = world.get_region("Customer Suburbia")
    customer_region_uptown = world.get_region("Customer Uptown")

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.
    # So dirty, this is horrible
    missions.add_locations(get_location_names_with_ids([loc.name for loc in data.locations.values() 
                                                        if loc.region == "Missions"]), Schedule1Location)

    # Level Unlocks
    if world.options.randomize_level_unlocks:
        level_unlocks = world.get_region("Level Unlocks")
        level_unlocks.add_locations(get_location_names_with_ids(
            [loc.name for loc in data.locations.values() if loc.region == "Level Unlocks"]), Schedule1Location)

    # property checks
    if world.options.randomize_business_properties:
        realtor.add_locations(get_location_names_with_ids([loc.name for loc in data.locations.values() 
                                                        if loc.region == "Realtor"
                                                        and "Business Property" in loc.tags]), Schedule1Location)

    # Note: Motel Room, and sweatshop aren't included in checks for realtor
    # These checks are already included within missions
    if world.options.randomize_drug_making_properties:
        realtor.add_locations(get_location_names_with_ids([loc.name for loc in data.locations.values() 
                                                        if loc.region == "Realtor"
                                                        and "Drug Making Property" in loc.tags]), Schedule1Location)

    # Customer locations - extract from LOCATION_NAME_TO_ID and group by region
    customer_region_northtown.add_locations(get_location_names_with_ids(
        loc.name for loc in data.locations.values() 
            if loc.region == "Customer Northtown"), Schedule1Location)
    customer_region_northtown.add_locations(get_location_names_with_ids(
        loc.name for loc in data.locations.values() 
            if loc.region == "Customer Westville"), Schedule1Location)
    customer_region_northtown.add_locations(get_location_names_with_ids(
        loc.name for loc in data.locations.values() 
            if loc.region == "Customer Downtown"), Schedule1Location)
    customer_region_northtown.add_locations(get_location_names_with_ids(
        loc.name for loc in data.locations.values() 
            if loc.region == "Customer Docks"), Schedule1Location)
    customer_region_northtown.add_locations(get_location_names_with_ids(
        loc.name for loc in data.locations.values() 
            if loc.region == "Customer Suburbia"), Schedule1Location)
    customer_region_northtown.add_locations(get_location_names_with_ids(
        loc.name for loc in data.locations.values() 
            if loc.region == "Customer Uptown"), Schedule1Location)
    
    if not world.options.randomize_cartel_influence:
        cartel_region_westville = world.get_region("Cartel Westville")
        cartel_region_downtown = world.get_region("Cartel Downtown")
        cartel_region_docks = world.get_region("Cartel Docks")
        cartel_region_suburbia = world.get_region("Cartel Suburbia")
        cartel_region_uptown = world.get_region("Cartel Uptown")

        cartel_region_westville.add_locations(get_location_names_with_ids(
            [loc.name for loc in data.locations.values() 
                if loc.region == "Cartel Westville"]), Schedule1Location)
        cartel_region_downtown.add_locations(get_location_names_with_ids(
            [loc.name for loc in data.locations.values() 
                if loc.region == "Cartel Downtown"]), Schedule1Location)
        cartel_region_docks.add_locations(get_location_names_with_ids(
            [loc.name for loc in data.locations.values() 
                if loc.region == "Cartel Docks"]), Schedule1Location)
        cartel_region_suburbia.add_locations(get_location_names_with_ids(
            [loc.name for loc in data.locations.values() 
                if loc.region == "Cartel Suburbia"]), Schedule1Location)
        cartel_region_uptown.add_locations(get_location_names_with_ids(
            [loc.name for loc in data.locations.values() 
                if loc.region == "Cartel Uptown"]), Schedule1Location)

    # Recipe checks - Only include the number specified by the RecipeChecks option
    if world.options.recipe_checks > 0:
        # Get each recipe region
        weed_recipe_region = world.get_region("Weed Recipe Checks")
        meth_recipe_region = world.get_region("Meth Recipe Checks")
        shrooms_recipe_region = world.get_region("Shrooms Recipe Checks")
        cocaine_recipe_region = world.get_region("Cocaine Recipe Checks")
        
        # Drug types with their regions and starting IDs in LOCATION_NAME_TO_ID
        # These magic numbers correspond to reserved IDs for recipe checks
        drug_types = [
            ("Weed Recipe", 195, weed_recipe_region),
            ("Meth Recipe", 210, meth_recipe_region),
            ("Shrooms Recipe", 225, shrooms_recipe_region),
            ("Cocaine Recipe", 240, cocaine_recipe_region),
        ]
        # Add needed recipe locations to location name to id
        for drug_name, start_id, region in drug_types:
            recipe_locations = []
            for i in range(1, world.options.recipe_checks + 1):
                LOCATION_NAME_TO_ID[f"{drug_name} Recipe Check, {i}"] = start_id + (i - 1)
                recipe_locations.append(f"{drug_name} Recipe Check, {i}")
        
            recipe_locations_dict = get_location_names_with_ids(recipe_locations)
            region.add_locations(recipe_locations_dict, Schedule1Location)
        
    # Cash for Trash checks - Only include the number specified by the CashForTrash option
    cash_for_trash_count = world.options.cash_for_trash
    if cash_for_trash_count > 0:
        start_id = 255  # Starting ID for Cash for Trash locations
        cash_for_trash_locations = []
        for i in range(1, cash_for_trash_count + 1):
            LOCATION_NAME_TO_ID[f"Cash for Trash {i}, Collect {i * 10} pieces of trash"] = start_id + (i - 1)
            cash_for_trash_locations.append(f"Cash for Trash {i}, Collect {i * 10} pieces of trash")
        cash_for_trash_locations_dict = get_location_names_with_ids(cash_for_trash_locations)
        overworld.add_locations(cash_for_trash_locations_dict, Schedule1Location)

    # Recruit Dealer locations - add to their respective regions - match them to customer regions
    # Hardcoding these are fine as it's 1 name for each region.
    if not world.options.randomize_dealers:
        westville_dealer_location = get_location_names_with_ids(["Recruit Westville Dealer: Molly Presley"])
        customer_region_westville.add_locations(westville_dealer_location, Schedule1Location)
        downtown_dealer_location = get_location_names_with_ids(["Recruit Downtown Dealer: Brad Crosby"])
        customer_region_downtown.add_locations(downtown_dealer_location, Schedule1Location)
        docks_dealer_location = get_location_names_with_ids(["Recruit Docks Dealer: Jane Lucero"])
        customer_region_docks.add_locations(docks_dealer_location, Schedule1Location)
        suburbia_dealer_location = get_location_names_with_ids(["Recruit Suburbia Dealer: Wei Long"])
        customer_region_suburbia.add_locations(suburbia_dealer_location, Schedule1Location)
        uptown_dealer_location = get_location_names_with_ids(["Recruit Uptown Dealer: Leo Rivers"])
        customer_region_uptown.add_locations(uptown_dealer_location, Schedule1Location)


def create_events(world: Schedule1World, data) -> None:
    # All mission completions are checks, however, they don't have an item associated with them.
    # We need to associate an event location/ event item for each mission completion.
    # This gives us a way to link missions
    regions = { "Overworld" : world.get_region("Overworld"),
                "Missions" : world.get_region("Missions") }
    
    # If goal is not "Reach Networth Goal", include Cartel Defeated event
    if world.options.goal != 1:
        for event in data.events.values():
            # "Cartel" here is the tag we're looking for for this goal
            if "Cartel" in event.tags:
                regions[event.region].add_event(
                    event.locationName, event.itemName, 
                    location_type=Schedule1Location, item_type=items.Schedule1Item)

    # if goal includes networth, include Networth Goal Reached event
    if world.options.goal < 2:
        for event in data.events.values():
            if "Networth" in event.tags:
                regions[event.region].add_event(
                    event.locationName, event.itemName, 
                    location_type=Schedule1Location, item_type=items.Schedule1Item)
                
    # Checks to see if 700 cartel cleared when cartel are not randomized
    for event in data.events.values():
        # Permanent events are always included regardless of options
        if "Permanent" in event.tags:
            regions[event.region].add_event(
                event.locationName, event.itemName, 
                location_type=Schedule1Location, item_type=items.Schedule1Item)