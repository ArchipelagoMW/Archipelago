from typing import TYPE_CHECKING
from .items import get_progression_medal, determine_item_classification
from .locations import TrackmaniaLocation, get_map_name, get_check_type_name, get_series_name
from .data import MapCheckTypes
from BaseClasses import Region, Location, LocationProgressType
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from . import TrackmaniaWorld

def create_check(world: "TrackmaniaWorld", reg: Region, map_name: str, check_type: MapCheckTypes, 
                 progress_type: LocationProgressType = LocationProgressType.DEFAULT):
    check_name = map_name + " - " + get_check_type_name(check_type)
    location = TrackmaniaLocation(world.player, check_name, world.location_name_to_id[check_name], reg)
    location.progress_type = progress_type
    reg.locations.append(location)

def create_track_checks(world: "TrackmaniaWorld", series: Region, map : int) -> Region:
    map_name = get_map_name(map) + " in " + series.name
    reg = series#Region(map_name, world.player, world.multiworld)

    create_check(world, reg, map_name, MapCheckTypes.Bronze)

    if world.options.target_time >=100:
        create_check(world, reg, map_name, MapCheckTypes.Silver)

    if world.options.target_time >=200:
        create_check(world, reg, map_name, MapCheckTypes.Gold)

    if world.options.target_time >=300:
        create_check(world, reg, map_name, MapCheckTypes.Author)

    create_check(world, reg, map_name, MapCheckTypes.Target)

    #world.multiworld.regions.append(reg)
    return reg

def create_series_region(world: "TrackmaniaWorld", series: int) -> Region:
    series_name = get_series_name(series)
    reg = Region(series_name, world.player, world.multiworld)
    world.multiworld.regions.append(reg)

    for x in range(world.options.series_map_number):
        map_reg = create_track_checks(world, reg, x)
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
