from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from BaseClasses import ItemClassification, Location

from . import items

from math import ceil

if TYPE_CHECKING:
    from .world import Schedule1World

# Every location must have a unique integer ID associated with it.
LOCATION_NAME_TO_ID = {}
def load_locations_data(data):
    """Load location data from JSON and populate LOCATION_NAME_TO_ID."""
    global LOCATION_NAME_TO_ID
    LOCATION_NAME_TO_ID = {name: loc.modern_id for name, loc in data.locations.items()}
    # must include all locations, even those not created based on options
    drug_types = [
    ("Weed", 195),
    ("Meth", 210),
    ("Shrooms", 225),
    ("Cocaine", 240),
    ]
    for drug_name, start_id in drug_types:
        for i in range(1, 16):
            LOCATION_NAME_TO_ID[f"{drug_name} Recipe Check, {i}"] = start_id + (i - 1)
    
    start_id = 600  # Starting ID for Cash for Trash locations
    for i in range(1, 51):
        LOCATION_NAME_TO_ID[f"Cash for Trash {i}, Collect {i * 10} pieces of trash"] = start_id + (i - 1)
# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class Schedule1Location(Location):
    game = "Schedule I"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: Schedule1World, locationData) -> None:
    create_regular_locations(world, locationData)


def create_regular_locations(world: Schedule1World, data) -> None:
    # Get all unique region names from location data
    region_names = set(loc.region for loc in data.locations.values())
    
    # Load all regions into a dictionary once for efficient access
    regions_dict: Dict[str, any] = {}
    for region_name in region_names:
        regions_dict[region_name] = world.get_region(region_name)
    
    # Group locations by region, excluding suppliers if randomized
    locations_by_region: Dict[str, list[str]] = {region: [] for region in region_names}
    
    for loc_name, loc_data in data.locations.items():
        # Skip supplier locations if randomize_suppliers is enabled
        if world.options.randomize_suppliers and "Supplier" in loc_data.tags:
            continue
        locations_by_region[loc_data.region].append(loc_name)
    
    # Add all locations to their respective regions
    for region_name, location_names in locations_by_region.items():
        if location_names:  # Only add if there are locations
            region = regions_dict[region_name]
            region.add_locations(get_location_names_with_ids(location_names), Schedule1Location)
    
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
            ("Weed", weed_recipe_region),
            ("Meth", meth_recipe_region),
            ("Shrooms", shrooms_recipe_region),
            ("Cocaine", cocaine_recipe_region),
        ]
        # Add needed recipe locations to location name to id
        for drug_name, region in drug_types:
            recipe_locations = []
            for i in range(1, world.options.recipe_checks + 1):
                recipe_locations.append(f"{drug_name} Recipe Check, {i}")
        
            recipe_locations_dict = get_location_names_with_ids(recipe_locations)
            region.add_locations(recipe_locations_dict, Schedule1Location)
        
    # Cash for Trash checks - Only include the number specified by the CashForTrash option
    # Add to Overworld region
    cash_for_trash_count = world.options.cash_for_trash
    if cash_for_trash_count > 0:
        regions = {
            100 : regions_dict["Overworld"],
            200 : regions_dict["Dodgy Dealing"],
            300 : regions_dict["Mixing Mania"],
            400 : regions_dict["We Need To Cook|2"],
            500 : regions_dict["Finishing the Job"]
        }
        cash_for_trash_locations = []
        for i in range(1, cash_for_trash_count + 1):
            cash_for_trash_locations.append(f"Cash for Trash {i}, Collect {i * 10} pieces of trash")
        cash_for_trash_locations_dict = get_location_names_with_ids(cash_for_trash_locations)
        regions[ceil(201 / 100) * 100].add_locations(cash_for_trash_locations_dict, Schedule1Location)