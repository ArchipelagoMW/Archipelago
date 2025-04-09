from typing import NamedTuple, List

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import SDLocation, location_table, get_locations_by_category
from . import SDWorld


class SDRegionData(NamedTuple):
    locations: [List[str]]
    region_exits: [List[str]]

def create_regions(world: "SDWorld"):
    regions = {
        "GeoRoom":      SDRegionData([],    []),
        "GreyZone1":    SDRegionData([],    []),
        "GreyZone2":    SDRegionData([],    []),
        "RedZone1":     SDRegionData([],    []),
        "RedZone2":     SDRegionData([],    []),
    }