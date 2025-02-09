from BaseClasses import Location, Region, MultiWorld
from .data import full_location_list


class PeaksOfYoreLocation(Location):
    game = "Peaks of Yore"


def get_locations(region_num: int) -> dict[str, int]:
    return {loc.name: loc.id for loc in full_location_list if loc.region == region_num}


def get_location_names_by_type(region_num: int, type: str):
    return {loc.name for loc in full_location_list if loc.region == region_num and loc.type == type}