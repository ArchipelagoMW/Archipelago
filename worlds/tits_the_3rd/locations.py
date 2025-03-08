"""This module represents location definitions for Trails in the Sky the 3rd"""
from typing import Callable, Dict, Optional, Set

from BaseClasses import CollectionState, ItemClassification, MultiWorld, Location
from .items import TitsThe3rdItem
from .names.location_name import LocationName
from .names.region_name import RegionName

class TitsThe3rdLocation(Location):
    """Trails in the Sky the 3rd Location Definition"""
    game: str = "Trails in the Sky the 3rd"


def get_location_id(location_name: LocationName):
    if location_name not in location_table:
        raise Exception(f"{location_name} is not part of location list. Something went wrong?")
    return location_table[location_name]


def create_location(multiworld: MultiWorld, player: int, region_name: str, location_name: str, rule: Optional[Callable[[CollectionState], bool]] = None):
    """
    Create a location in the given region.

    Args:
        multiworld: The multiworld object.
        player: The player number.
        region_name: The name of the region to create the location in.
        location_name: The name of the location to create.
        rule: A rule to apply to the location.
    """
    region = multiworld.get_region(region_name, player)
    location = TitsThe3rdLocation(player, location_name, location_table[location_name], region)
    if rule:
        location.access_rule = rule
    region.locations.append(location)

def create_locations(multiworld: MultiWorld, player: int):
    """
    Define AP locations for Trails in the Sky the 3rd.
    Assumes regions have already been created.

    Args:
        multiworld: The multiworld object.
        player: The player number.
    """
    create_location(multiworld, player, RegionName.lusitania, LocationName.lusitania_chest_bedroom_beside_banquet)
    create_location(multiworld, player, RegionName.lusitania, LocationName.lusitania_chest_bedroom_past_library)
    create_location(multiworld, player, RegionName.lusitania, LocationName.lusitania_chest_bedroom_past_casino_left)
    create_location(multiworld, player, RegionName.lusitania, LocationName.lusitania_chest_bedroom_past_casino_right)

    create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.jade_corridor_chest_first_hall_straight_from_start)
    create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.jade_corridor_chest_first_hall_elevated_platform)
    create_location(multiworld, player, RegionName.jade_corridor_start, LocationName.jade_corridor_chest_first_hall_before_first_warp)

    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_second_chest)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_third_chest)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_first_chest)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_left_of_sun_door_one)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_right_of_sun_door_one)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_arseille_deck)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_arseille_confrence_room)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_arseille_kitchen)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_arseille_bedroom_one)
    create_location(multiworld, player, RegionName.jade_corridor_post_tita_gate, LocationName.jade_corridor_chest_arseille_bedroom_two)

    create_location(multiworld, player, RegionName.jade_corridor_post_julia_gate, LocationName.jade_corridor_chest_left_from_checkpoint_first_chest)
    create_location(multiworld, player, RegionName.jade_corridor_post_julia_gate, LocationName.jade_corridor_chest_left_from_checkpoint_second_chest)
    create_location(multiworld, player, RegionName.jade_corridor_post_julia_gate, LocationName.jade_corridor_chest_left_from_checkpoint_third_chest)
    create_location(multiworld, player, RegionName.jade_corridor_post_julia_gate, LocationName.jade_corridor_chest_left_from_checkpoint_fourth_chest)
    create_location(multiworld, player, RegionName.jade_corridor_post_julia_gate, LocationName.chapter1_boss_defeated)


location_table: Dict[str, int] = {
    LocationName.lusitania_chest_bedroom_beside_banquet: 9720,
    LocationName.lusitania_chest_bedroom_past_library: 9721,
    LocationName.lusitania_chest_bedroom_past_casino_left: 9722,
    LocationName.lusitania_chest_bedroom_past_casino_right: 9723,
    LocationName.jade_corridor_chest_first_hall_straight_from_start: 9857,
    LocationName.jade_corridor_chest_first_hall_elevated_platform: 9858,
    LocationName.jade_corridor_chest_first_hall_before_first_warp: 9859,
    LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_second_chest: 9864,
    LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_third_chest: 9865,
    LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_first_chest: 9866,
    LocationName.jade_corridor_chest_left_of_sun_door_one: 9867,
    LocationName.jade_corridor_chest_right_of_sun_door_one: 9868,
    LocationName.jade_corridor_chest_arseille_deck: 9869,
    LocationName.jade_corridor_chest_arseille_confrence_room: 9872,
    LocationName.jade_corridor_chest_arseille_kitchen: 9873,
    LocationName.jade_corridor_chest_arseille_bedroom_one: 9874,
    LocationName.jade_corridor_chest_arseille_bedroom_two: 9875,
    LocationName.jade_corridor_chest_left_from_checkpoint_first_chest: 9880,
    LocationName.jade_corridor_chest_left_from_checkpoint_second_chest: 9881,
    LocationName.jade_corridor_chest_left_from_checkpoint_third_chest: 9884,
    LocationName.jade_corridor_chest_left_from_checkpoint_fourth_chest: 9885,
    LocationName.chapter1_boss_defeated: 9757,
}

location_groups: Dict[str, Set[str]] = {}
