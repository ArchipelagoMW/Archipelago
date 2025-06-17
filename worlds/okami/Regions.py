from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType, CollectionState
from .Locations import create_region_locations, create_region_events
from typing import TYPE_CHECKING, List, Dict, Optional
from .RegionsData import menu,r100,r122,r101,r102,r103,rf01,rf02,rf03,rf04
from .Rules import apply_exit_rules
from .Types import RegionNames

if TYPE_CHECKING:
    from . import OkamiWorld


okami_exits={
    **menu.exits,
    **r100.exits,
    **r122.exits,
    **r101.exits,
    **r102.exits,
    **r103.exits,
    **rf01.exits,
    **rf02.exits,
    **rf03.exits,
    **rf04.exits,
}

def get_region_name(key:str):
    if key in RegionNames:
        return RegionNames[key]

def create_regions(world: "OkamiWorld"):
    for name in RegionNames:
        reg=create_region(world,name)
        world.multiworld.regions.append(reg)
    #Second loop to create exits
    for name in RegionNames:
        reg = world.multiworld.get_region(name,world.player)
        create_region_exits(reg, world)

def create_region(world:"OkamiWorld",region_name:str):
    reg = Region(region_name,world.player, world.multiworld)
    create_region_locations(reg,world)
    create_region_events(reg,world)
    return reg


def create_region_exits(reg:Region,world:"OkamiWorld"):
    if reg.name in okami_exits:
        for exit_data in okami_exits[reg.name]:
            exiting_region=world.multiworld.get_region(exit_data.destination,world.player)
            ext = reg.connect(exiting_region,exit_data.name)
            apply_exit_rules(ext,ext.name,exit_data,world)

def get_region_location_count(world: "OkamiWorld", region_name: str, included_only: bool = True) -> int:
    count = 0
    region = world.multiworld.get_region(region_name, world.player)
    for loc in region.locations:
        if loc.address is not None and (not included_only or loc.progress_type is not LocationProgressType.EXCLUDED):
            count += 1

    return count

