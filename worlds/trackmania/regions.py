from typing import TYPE_CHECKING
from .items import TrackmaniaItem
from .locations import TrackmaniaLocation, MapCheckTypes, get_map_name, get_check_type_name, get_series_name
from BaseClasses import Region, LocationProgressType, ItemClassification

if TYPE_CHECKING:
    from . import TrackmaniaWorld

def create_check(world: "TrackmaniaWorld", reg: Region, map_name: str, check_type: MapCheckTypes, 
                 progress_type: LocationProgressType = LocationProgressType.DEFAULT):
    check_name = f"{map_name} - {get_check_type_name(check_type)}"
    location = TrackmaniaLocation(world.player, check_name, world.location_name_to_id[check_name], reg)

    if check_type == MapCheckTypes.Target:
        r = world.random.randint(0,100)
        if r <= world.options.target_progression_chance.value:
            location.progress_type = LocationProgressType.PRIORITY
        else:
            location.progress_type = progress_type
    else:
        location.progress_type = progress_type

    reg.locations.append(location)

def create_track_checks(world: "TrackmaniaWorld", series: Region, map_index : int):
    map_name = f"{series.name} {get_map_name(map_index)}"
    reg = series

    if world.options.target_time < 100 or world.options.disable_bronze_locations <= 0:
        create_check(world, reg, map_name, MapCheckTypes.Bronze)

    if world.options.target_time >=100 and world.options.disable_silver_locations <= 0:
        create_check(world, reg, map_name, MapCheckTypes.Silver)

    if world.options.target_time >=200 and world.options.disable_gold_locations <= 0:
        create_check(world, reg, map_name, MapCheckTypes.Gold)

    if world.options.target_time >=300 and world.options.disable_author_locations <= 0:
        create_check(world, reg, map_name, MapCheckTypes.Author)

    create_check(world, reg, map_name, MapCheckTypes.Target)

def create_series_region(world: "TrackmaniaWorld", series: int) -> Region:
    series_name = get_series_name(series)
    reg = Region(series_name, world.player, world.multiworld)
    world.multiworld.regions.append(reg)

    for x in range(world.series_data[series]["MapCount"]):
        create_track_checks(world, reg, x)

    return reg

def create_victory_region(world: "TrackmaniaWorld", final_region: Region):
    victory_region = Region("Victory!", world.player, world.multiworld)
    world.multiworld.regions.append(victory_region)
    victory_event = TrackmaniaLocation(world.player,"Victory!",None,victory_region)
    victory_region.locations.append(victory_event)
    victory_event.place_locked_item(TrackmaniaItem("Victory!", ItemClassification.progression, None, world.player))
    final_region.connect(victory_region, "Victory!")

def create_regions(world: "TrackmaniaWorld"):
    menu = Region ("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    previous_region: Region = menu
    for i in range(world.options.series_number):
        series = create_series_region(world, i)
        previous_region.connect(series, f"{previous_region.name} -> {series.name}")
        previous_region = series

    create_victory_region(world, previous_region)

    # from Utils import visualize_regions
    # visualize_regions(world.multiworld.get_region("Menu", world.player), "my_world.puml")
