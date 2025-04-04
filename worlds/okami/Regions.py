from collections.abc import Callable
from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType, CollectionState
from .Locations import create_region_locations, create_region_events
from typing import TYPE_CHECKING, List, Dict, Optional
from .RegionsData import menu,r100,r122,r101,r102
from .Rules import apply_exit_rules


if TYPE_CHECKING:
    from . import OkamiWorld


okami_regions={
    **menu.regions,
    **r100.regions,
    **r122.regions,
    **r101.regions,
    **r102.regions
}

okami_exits={
    **menu.exits,
    **r100.exits,
    **r122.exits,
    **r101.exits,
    **r102.exits
}

def get_region_name(key:str):
    if key in okami_regions:
        return okami_regions[key]

def create_regions(world: "OkamiWorld"):
    for (key,name) in okami_regions.items():
        reg=create_region(key,world,name)
        print("Created Region "+name)
        world.multiworld.regions.append(reg)
    #Second loop to create exits
    for (key,name) in okami_regions.items():
        reg = world.multiworld.get_region(name,world.player)
        create_region_exits(key, reg, world)

    for r in world.get_regions():
        print (r.name)
        print(r.entrances)

def create_region(region_key:str ,world:"OkamiWorld",region_name:str):
    reg = Region(region_name,world.player, world.multiworld)
    create_region_locations(region_key,reg,world)
    create_region_events(region_key,reg,world)
    return reg


def create_region_exits(region_key:str,reg:Region,world:"OkamiWorld"):
    print ("Creating Exits for "+reg.name)
    if region_key in okami_exits:
        for exit_data in okami_exits[region_key]:
            destination_name =get_region_name(exit_data.destination)
            if destination_name is None:
                print('\033[93m' + "Region "+exit_data.destination +" does not exit"+'\033[0m')
                continue
            exiting_region=world.multiworld.get_region(destination_name,world.player)
            ext = reg.connect(exiting_region,exit_data.name)
            apply_exit_rules(ext,ext.name,exit_data,world)
            print("Created Exit "+ext.name + " to " + exiting_region.name)


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

