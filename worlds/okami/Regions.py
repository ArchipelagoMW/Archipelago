from collections.abc import Callable
from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType, CollectionState
from .Locations import create_region_locations, create_region_events
from typing import TYPE_CHECKING, List, Dict, Optional
from .RegionsData import menu,r100,r122
from .Types import OkamiLocation, LocData, ExitData


if TYPE_CHECKING:
    from . import OkamiWorld


okami_regions={
    **(menu.regions),
    **(r100.regions),
    **(r122.regions)
}

okami_exits={
    **menu.exits,
    **r100.exits,
    **r122.exits,
}

def get_region_name(key:str):
    if key in okami_regions:
        return okami_regions[key]

def create_regions2(world: "OkamiWorld"):
    for (key,name) in okami_regions.items():
        reg=create_region2(world,name)
        world.multiworld.regions.append(reg)
    #Second loop to create exits
    for (key,name) in okami_regions.items():
        reg = world.multiworld.get_region(name,world.player)
        create_region_exits(reg,world)

def create_region2(world:"OkamiWorld",region_name:str):
    reg = Region(region_name,world.player, world.multiworld)
    create_region_locations(reg,world)
    create_region_events(reg,world)
    return reg


def create_region_exits(reg:Region,world:"OkamiWorld"):

    if reg.name in okami_exits:
        for (exit_name, exit_data) in okami_exits[reg.name].items():
            exiting_region=world.multiworld.get_region(get_region_name(exit_data.destination),world.player)
            reg.connect(exiting_region,exit_name,rule=exit_data.rule)


# Takes an entrance, removes its old connections, and reconnects it between the two regions specified.
def reconnect_regions(entrance: Entrance, start_region: Region, exit_region: Region):
    if entrance in entrance.connected_region.entrances:
        entrance.connected_region.entrances.remove(entrance)

    if entrance in entrance.parent_region.exits:
        entrance.parent_region.exits.remove(entrance)

    if entrance in start_region.exits:
        start_region.exits.remove(entrance)

    if entrance in exit_region.entrances:
        exit_region.entrances.remove(entrance)

    entrance.parent_region = start_region
    start_region.exits.append(entrance)
    entrance.connect(exit_region)

def get_region_location_count(world: "OkamiWorld", region_name: str, included_only: bool = True) -> int:
    count = 0
    region = world.multiworld.get_region(region_name, world.player)
    for loc in region.locations:
        if loc.address is not None and (not included_only or loc.progress_type is not LocationProgressType.EXCLUDED):
            count += 1

    return count

