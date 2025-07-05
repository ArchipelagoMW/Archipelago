"""This module represents location definitions for Trails in the Sky the 3rd"""
from typing import Callable, Dict, Optional, Set
import re

from BaseClasses import CollectionState, MultiWorld, Location
from .names.location_name import LocationName
from .names.region_name import RegionName
from .names.item_name import ItemName
from .tables.location_list import location_table, LocationData

MIN_CRAFT_LOCATION_ID = 100000
MAX_CRAFT_LOCATION_ID = 100000 + 10000

class TitsThe3rdLocation(Location):
    """Trails in the Sky the 3rd Location Definition"""
    game: str = "Trails in the Sky the 3rd"


def get_location_id(location_name: LocationName):
    if location_name not in location_table:
        raise Exception(f"{location_name} is not part of location list. Something went wrong?")
    return location_table[location_name].flag


def create_location(multiworld: MultiWorld, player: int, location_name: str, rule: Optional[Callable[[CollectionState], bool]] = None):
    """
    Create a location in accordance with the location table in location_list.py

    Args:
        multiworld: The multiworld object.
        player: The player number.
        location_name: The name of the location to create.
        rule: A rule to apply to the location.
    """
    region = multiworld.get_region(location_table[location_name].region, player)
    location = TitsThe3rdLocation(player, location_name, location_table[location_name].flag, region)
    if rule:
        location.access_rule = rule
    region.locations.append(location)


def create_locations(multiworld: MultiWorld, player: int, spoiler_mode: bool = False):
    """
    Define AP locations for Trails in the Sky the 3rd.
    Assumes regions have already been created.

    Args:
        multiworld: The multiworld object.
        player: The player number.
    """
    for location_name in location_table:
        rule = None
        if location_table[location_name].item_requirements:
            rule = lambda state: all(
                state.has(item_name, quantity, player)
                for item_name, quantity in location_table[location_name].item_requirements
            )
        if spoiler_mode & (location_table[location_name].spoiler_name != ""):
            create_location(multiworld, player, location_table[location_name].spoiler_name, rule)
        else:
            create_location(multiworld, player, location_name, rule)


# TODO: move below to tables?
def _get_craft_locations(character_name: str) -> Dict[str, LocationData]:
    return {
        location_name: location_data for location_name, location_data in location_table.items() if
        (
            location_data.check_type == "Craft"
            and location_name.lower().startswith(character_name)
        )
    }

estelle_craft_locations: Dict[str, LocationData] = _get_craft_locations("estelle")
joshua_craft_locations: Dict[str, LocationData] = _get_craft_locations("joshua")
scherazard_craft_locations: Dict[str, LocationData] = _get_craft_locations("scherazard")
olivier_craft_locations: Dict[str, LocationData] = _get_craft_locations("olivier")
kloe_craft_locations: Dict[str, LocationData] = _get_craft_locations("kloe")
agate_craft_locations: Dict[str, LocationData] = _get_craft_locations("agate")
tita_craft_locations: Dict[str, LocationData] = _get_craft_locations("tita")
zin_craft_locations: Dict[str, LocationData] = _get_craft_locations("zin")
kevin_craft_locations: Dict[str, LocationData] = _get_craft_locations("kevin")
anelace_craft_locations: Dict[str, LocationData] = _get_craft_locations("anelace")
josette_craft_locations: Dict[str, LocationData] = _get_craft_locations("josette")
richard_craft_locations: Dict[str, LocationData] = _get_craft_locations("richard")
mueller_craft_locations: Dict[str, LocationData] = _get_craft_locations("mueller")
julia_craft_locations: Dict[str, LocationData] = _get_craft_locations("julia")
ries_craft_locations: Dict[str, LocationData] = _get_craft_locations("ries")
renne_craft_locations: Dict[str, LocationData] = _get_craft_locations("renne")

craft_locations: Dict[str, LocationData] = {
    **estelle_craft_locations,
    **joshua_craft_locations,
    **scherazard_craft_locations,
    **olivier_craft_locations,
    **kloe_craft_locations,
    **agate_craft_locations,
    **tita_craft_locations,
    **zin_craft_locations,
    **kevin_craft_locations,
    **anelace_craft_locations,
    **josette_craft_locations,
    **richard_craft_locations,
    **mueller_craft_locations,
    **julia_craft_locations,
    **ries_craft_locations,
    **renne_craft_locations,
}

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

character_name_to_id = {
    "estelle": 0,
    "joshua": 1,
    "scherazard": 2,
    "olivier": 3,
    "kloe": 4,
    "agate": 5,
    "tita": 6,
    "zin": 7,
    "kevin": 8,
    "anelace": 9,
    "josette": 10,
    "richard": 11,
    "mueller": 12,
    "julia": 13,
    "ries": 14,
    "renne": 15
}
craft_location_id_to_character_id_and_level_threshold = {}
for craft in craft_locations:
    # Parse the level threshold and character from the craft name to build the above table
    character_name = craft.split(" ")[0].lower()
    character_id = character_name_to_id[character_name]
    level_match = re.search(r'\(Level (\d+)\)', craft)
    if level_match:
        level_threshold = int(level_match.group(1))
        craft_location_id_to_character_id_and_level_threshold[craft_locations[craft].flag] = (character_id, level_threshold)

