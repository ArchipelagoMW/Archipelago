"""This module represents location definitions for Trails in the Sky the 3rd"""
from typing import Callable, Dict, Optional, Set

from BaseClasses import CollectionState, MultiWorld, Location
from .names.location_name import LocationName
from .tables.location_list import (
    location_table,
    estelle_craft_locations,
    joshua_craft_locations,
    scherazard_craft_locations,
    olivier_craft_locations,
    kloe_craft_locations,
    agate_craft_locations,
    tita_craft_locations,
    zin_craft_locations,
    kevin_craft_locations,
    anelace_craft_locations,
    josette_craft_locations,
    richard_craft_locations,
    mueller_craft_locations,
    julia_craft_locations,
    ries_craft_locations,
    renne_craft_locations
)
from .options import TitsThe3rdOptions, CraftPlacement
from .spoiler_mapping import scrub_spoiler_data

MIN_CRAFT_LOCATION_ID = 100000
MAX_CRAFT_LOCATION_ID = 100000 + 10000

class TitsThe3rdLocation(Location):
    """Trails in the Sky the 3rd Location Definition"""
    game: str = "Trails in the Sky the 3rd"


def get_location_id(location_name: LocationName):
    """
    Get the location id for a given location name.
    """
    if location_name not in location_table:
        raise RuntimeError(f"{location_name} is not part of location list. Something went wrong?")
    return location_table[location_name].flag


def create_location(multiworld: MultiWorld, player: int, location_name: str, options: TitsThe3rdOptions, rule: Optional[Callable[[CollectionState], bool]] = None):
    """
    Create a location in accordance with the location table in location_list.py

    Args:
        multiworld: The multiworld object.
        player: The player number.
        location_name: The name of the location to create.
        rule: A rule to apply to the location.
    """
    region = multiworld.get_region(location_table[location_name].region, player)
    shown_location_name = location_name
    if options.name_spoiler_option:
        shown_location_name = scrub_spoiler_data(location_name)
    location = TitsThe3rdLocation(player, shown_location_name, location_table[location_name].flag, region)
    if rule:
        location.access_rule = rule
    region.locations.append(location)


def create_locations(multiworld: MultiWorld, player: int, options: TitsThe3rdOptions):
    """
    Define AP locations for Trails in the Sky the 3rd.
    Assumes regions have already been created.

    Args:
        multiworld: The multiworld object.
        player: The player number.
    """
    for location_name in location_table:
        if location_table[location_name].check_type == "Craft" and options.craft_placement == CraftPlacement.option_default and not options.craft_shuffle:
            continue
        rule = None
        if location_table[location_name].item_requirements:
            rule = lambda state, loc_name=location_name: all(
                state.has(scrub_spoiler_data(item_name) if options.name_spoiler_option else item_name, quantity, player)
                for item_name, quantity in location_table[loc_name].item_requirements
            )
        create_location(multiworld, player, location_name, options, rule)


location_groups: Dict[str, Set[str]] = {
    "Estelle Crafts": set(estelle_craft_locations.keys()),
    "Joshua Crafts": set(joshua_craft_locations.keys()),
    "Scherazard Crafts": set(scherazard_craft_locations.keys()),
    "Olivier Crafts": set(olivier_craft_locations.keys()),
    "Kloe Crafts": set(kloe_craft_locations.keys()),
    "Agate Crafts": set(agate_craft_locations.keys()),
    "Tita Crafts": set(tita_craft_locations.keys()),
    "Zin Crafts": set(zin_craft_locations.keys()),
    "Kevin Crafts": set(kevin_craft_locations.keys()),
    "Anelace Crafts": set(anelace_craft_locations.keys()),
    "Josette Crafts": set(josette_craft_locations.keys()),
    "Richard Crafts": set(richard_craft_locations.keys()),
    "Mueller Crafts": set(mueller_craft_locations.keys()),
    "Julia Crafts": set(julia_craft_locations.keys()),
    "Ries Crafts": set(ries_craft_locations.keys()),
    "Renne Crafts": set(renne_craft_locations.keys()),
}