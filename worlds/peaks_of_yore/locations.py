from BaseClasses import Location, Region
from .data import full_location_table


class PeaksOfYoreLocation(Location):
    game = "Peaks of Yore"


def get_locations(region_num: int) -> dict[str, int]:
    return {loc["name"]: loc["id"] for loc in full_location_table if loc["region"] == region_num}
