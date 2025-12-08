from __future__ import annotations
from BaseClasses import Region
from .locations import location_table, BKSim_Location
from .common import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import BKSimWorld


def create_regions(world: BKSimWorld) -> None:
    multiworld = world.multiworld
    player = world.player

    for rid in RID:
        multiworld.regions.append(Region(rid, player, multiworld))

    locs_per_weather = world.options.locs_per_weather.value
    for locid, locinfo in enumerate(location_table, 1):
        if locinfo.index >= locs_per_weather:
            continue
        region = world.get_region(locinfo.region_id)
        if region:
            region.locations.append(BKSim_Location(player, locinfo.name, locid, region, locinfo))
