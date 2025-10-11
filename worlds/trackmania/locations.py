from enum import Enum
from BaseClasses import Location
from .options import SeriesNumber, SeriesMinimumMapNumber
from .data import base_id

class TrackmaniaLocation(Location):  # or from Locations import MyGameLocation
    game = "Trackmania"  # name of the game/world this location is in

class MapCheckTypes(Enum):
    Bronze = 0
    Silver = 1
    Gold   = 2
    Author = 3
    Target = 4

def build_locations() -> dict[str, int]:
    trackmania_locations : dict[str, int] = {}
    id_offset = 0

    #since we don't have preferences yet, we have to return every possible location, not just the ones we need ;-;
    for x in range(SeriesNumber.range_end):
        for y in range(SeriesMinimumMapNumber.range_end):
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Bronze)] = base_id + id_offset
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Silver)] = base_id + id_offset + 1
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Gold)]   = base_id + id_offset + 2
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Author)] = base_id + id_offset + 3
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Target)] = base_id + id_offset + 4
            id_offset += 5
        

    return trackmania_locations

def get_location_name(series: int, number : int, check : MapCheckTypes) -> str:
    return f"{get_series_name(series)} {get_map_name(number)} - {get_check_type_name(check)}"

def get_map_name(number: int):
    return f"Map {str(number+1)}"

def get_series_name(number:int):
    return f"Series {str(number+1)}"

def get_check_type_name(check: MapCheckTypes) -> str:
    match check:
        case MapCheckTypes.Bronze:
            return "Bronze Time"
        case MapCheckTypes.Silver:
            return "Silver Time"
        case MapCheckTypes.Gold:
            return "Gold Time"
        case MapCheckTypes.Author:
            return "Author Time"
        case MapCheckTypes.Target:
            return "Target Time"
        case _:
            return ""
        
