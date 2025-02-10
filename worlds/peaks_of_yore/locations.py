from BaseClasses import Location
from .data import full_location_list, PeaksOfYoreRegion


class PeaksOfYoreLocation(Location):
    game = "Peaks of Yore"


def get_locations(region: PeaksOfYoreRegion) -> dict[str, int]:
    return {loc.name: loc.id for loc in full_location_list if loc.region == region}


def get_location_names_by_type(region: PeaksOfYoreRegion, location_type: str) -> list[str]:
    return [loc.name for loc in full_location_list if loc.region == region and loc.type == location_type]
