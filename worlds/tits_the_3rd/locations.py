"""This module represents location definitions for Trails in the Sky the 3rd"""
from typing import Callable, Dict, Optional, Set

from BaseClasses import CollectionState, MultiWorld, Location
from .names.location_name import LocationName
from .names.region_name import RegionName
from .names.item_name import ItemName
from .tables.location_list import location_table
from .names.item_name import ItemName

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
        if spoiler_mode & (location_table[location_name].spoiler_name != ""):
            create_location(multiworld, player, location_table[location_name].spoiler_name)
        else:
            create_location(multiworld, player, location_name)

location_groups: Dict[str, Set[str]] = {}

default_sealing_stone_quartz = {
    # Tita
    LocationName.tita_orbment_item_1: ItemName.ep_cut_2,
    LocationName.tita_orbment_item_2: ItemName.attack_1,
    LocationName.tita_orbment_item_3: ItemName.eagle_eye,
    LocationName.tita_orbment_item_4: ItemName.hp_1,
    # Julia
    LocationName.julia_orbment_item_1: ItemName.ep_cut_2,
    LocationName.julia_orbment_item_2: ItemName.action_1,
    LocationName.julia_orbment_item_3: ItemName.hit_1,
    LocationName.julia_orbment_item_4: ItemName.range_1,
    LocationName.julia_orbment_item_5: ItemName.move_1,
    LocationName.julia_orbment_item_6: ItemName.attack_1,
    LocationName.julia_orbment_item_7: ItemName.shield_1,
}