from typing import Dict, List, TYPE_CHECKING
from BaseClasses import Region, Location, LocationProgressType
from worlds.generic.Rules import add_rule, set_rule
from .options import SeriesNumber, SeriesMapNumber
from .data import base_id, MapCheckTypes
from .items import get_progression_medal, determine_item_classification
import logging

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
    return get_map_name(number) + " in " + get_series_name(series) + " - " + get_check_type_name(check)

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
        
def create_track_region(world: "TrackmaniaWorld", series: Region, map : int) -> Region:
    map_name = get_map_name(map) + " in " + series.name
    reg = series#Region(map_name, world.player, world.multiworld)

    bronze_check = map_name + " - " + get_check_type_name(MapCheckTypes.Bronze)
    location_bronze = TrackmaniaLocation(world.player, bronze_check, world.location_name_to_id[bronze_check], reg)
    location_bronze.progress_type = LocationProgressType.DEFAULT
    reg.locations.append(location_bronze)

    if world.options.target_time >=100:
        silver_check = map_name + " - " + get_check_type_name(MapCheckTypes.Silver)
        location_silver = TrackmaniaLocation(world.player, silver_check, world.location_name_to_id[silver_check], reg)
        location_silver.progress_type = LocationProgressType.DEFAULT
        reg.locations.append(location_silver)

    if world.options.target_time >=200:
        gold_check = map_name + " - " + get_check_type_name(MapCheckTypes.Gold)
        location_gold = TrackmaniaLocation(world.player, gold_check, world.location_name_to_id[gold_check], reg)
        location_gold.progress_type = LocationProgressType.DEFAULT
        reg.locations.append(location_gold)

    if world.options.target_time >=300:
        author_check = map_name + " - " + get_check_type_name(MapCheckTypes.Author)
        location_author = TrackmaniaLocation(world.player, author_check, world.location_name_to_id[author_check], reg)
        location_author.progress_type = LocationProgressType.DEFAULT
        reg.locations.append(location_author)

    target_check = map_name + " - " + get_check_type_name(MapCheckTypes.Target)
    location_target = TrackmaniaLocation(world.player, target_check, world.location_name_to_id[target_check], reg)
    location_target.progress_type = LocationProgressType.DEFAULT
    reg.locations.append(location_target)

    #world.multiworld.regions.append(reg)
    return reg

def create_series_region(world: "TrackmaniaWorld", series: int) -> Region:
    series_name = get_series_name(series)
    reg = Region(series_name, world.player, world.multiworld)
    world.multiworld.regions.append(reg)

    for x in range(world.options.series_map_number):
        map_reg = create_track_region(world, reg, x)
        #reg.connect(map_reg, series_name + " -> " + get_map_name(x))

    return reg

def create_regions(world: "TrackmaniaWorld") -> Region:
    menu = Region ("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    previous_region: Region = menu
    medal_requirement: int = 0

    for i in range(world.options.series_number):
        series = create_series_region(world, i)
        previous_region.connect(series, previous_region.name + " -> " + series.name)

        set_rule(series, lambda state: state.has(get_progression_medal(world), world.player, medal_requirement))
        medal_requirement += world.options.medal_requirement

        previous_region = series


    # from Utils import visualize_regions
    # visualize_regions(world.multiworld.get_region("Menu", world.player), "my_world.puml")
