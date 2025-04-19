from typing import Dict, List, TYPE_CHECKING
from BaseClasses import Region, Location, LocationProgressType
from .options import SeriesNumber, SeriesMapNumber
from .data import base_id, MapCheckTypes

if TYPE_CHECKING:
    from . import TrackmaniaWorld

class TrackmaniaLocation(Location):  # or from Locations import MyGameLocation
    game = "Trackmania"  # name of the game/world this location is in

def build_locations() -> Dict[str, int]:
    trackmania_locations : Dict[str, int] = {}
    idOffset = 0
    #since we dont have preferences yet, we have to return every possible location, not just the ones we need ;-;
    #its fine but my inner perfectionist is not
    for x in range(SeriesNumber.range_end):
        for y in range(SeriesMapNumber.range_end):
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Bronze)] = base_id + idOffset
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Silver)] = base_id + idOffset + 1
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Gold)]   = base_id + idOffset + 2
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Author)] = base_id + idOffset + 3
            trackmania_locations[get_location_name(x,y,MapCheckTypes.Target)] = base_id + idOffset + 4
            idOffset += 5
        

    return trackmania_locations

def get_location_name(series: int, number : int, check : MapCheckTypes) -> str:
    return get_series_name(series) + " " +get_map_name(number) + " - " + get_check_type_name(check)

def get_map_name(number: int):
    return "Map " + str(number+1)

def get_series_name(number:int):
    return "Series " + str(number+1)

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
        
