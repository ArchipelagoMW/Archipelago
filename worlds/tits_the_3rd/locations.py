"""This module represents location definitions for Trails in the Sky the 3rd"""
from typing import Dict

from BaseClasses import MultiWorld, Location

class TitsThe3rdLocation(Location):
    """Trails in the Sky the 3rd Location Definition"""
    game: str = "Trails in the Sky the 3rd"

def create_locations(multiworld: MultiWorld, player: int, location_name_to_id: Dict[str, int]):
    """Define AP locations for Trails in the Sky the 3rd"""
    regions = multiworld.regions.region_cache[player]
    menu_region = regions["Menu"]
    menu_region.locations.append(TitsThe3rdLocation(player, "Dummy Location", location_name_to_id["Dummy Location"], menu_region))
