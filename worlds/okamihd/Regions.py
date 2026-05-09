from BaseClasses import Region, LocationProgressType
from .Locations import create_region_locations, create_region_events
from typing import TYPE_CHECKING
from .Rules import apply_exit_rules
from .Enums.RegionNames import RegionNames
from .RegionsData import okami_exits

if TYPE_CHECKING:
    from . import OkamiWorld


def get_region_name(key: str):
    if key in RegionNames:
        return RegionNames[key]


def create_regions(world: "OkamiWorld"):
    for r in RegionNames:
        reg = create_region(world, r.value)
        world.multiworld.regions.append(reg)
    # Second loop to create exits
    for r in RegionNames:
        reg = world.multiworld.get_region(r.value, world.player)
        create_region_exits(reg, world)


def create_region(world: "OkamiWorld", region_name: str):
    reg = Region(region_name, world.player, world.multiworld)
    create_region_locations(reg, world)
    create_region_events(reg, world)
    return reg


def create_region_exits(reg: Region, world: "OkamiWorld"):
    if reg.name in okami_exits:
        for exit_data in okami_exits[reg.name]:
            exiting_region = world.multiworld.get_region(exit_data.destination, world.player)
            exit_name = reg.name + ' -> ' + exiting_region.name
            ext = reg.connect(exiting_region, exit_name)
            apply_exit_rules(ext, ext.name, exit_data, world)
            if not exit_data.one_way:
                reverse_exit_name = exiting_region.name + ' -> ' + reg.name
                rev_ext = exiting_region.connect(reg,reverse_exit_name)
                apply_exit_rules(rev_ext,rev_ext.name,exit_data,world)


def get_region_location_count(world: "OkamiWorld", region_name: str, included_only: bool = True) -> int:
    count = 0
    region = world.multiworld.get_region(region_name, world.player)
    for loc in region.locations:
        if loc.address is not None and (not included_only or loc.progress_type is not LocationProgressType.EXCLUDED):
            count += 1

    return count
