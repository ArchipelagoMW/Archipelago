from typing import NamedTuple

from BaseClasses import Region, Location
from options import *
from worlds.AutoWorld import World
from .data import *


class PeaksOfYoreLocation(Location):
    game = "Peaks of Yore"


class RegionLocationInfo(NamedTuple):
    artefacts_in_pool: list[str]
    peaks_in_pool: list[str]
    time_attack_in_pool: list[str]


# IDE was yelling at me and not happy that I called a parameter "options", so have "opts"
def create_poy_regions(world: World, opts: PeaksOfYoreOptions) -> RegionLocationInfo:
    result = RegionLocationInfo([], [], [])

    cabin_region = Region("Cabin", world.player, world.multiworld)
    world.multiworld.regions.append(cabin_region)

    for r in poy_regions.subregions:
        tempres = recursive_create_region(r, cabin_region, world, opts)
        result.peaks_in_pool.extend(tempres.peaks_in_pool)
        result.artefacts_in_pool.extend(tempres.artefacts_in_pool)
        result.time_attack_in_pool.extend(tempres.time_attack_in_pool)
    return result


def recursive_create_region(region_data: POYRegion, parent_region: Region, world: World, opts: PeaksOfYoreOptions) -> \
        RegionLocationInfo:
    """
    Takes a POYRegion, and creates it and its subregions as a subregion of parent_region
    """
    result = RegionLocationInfo([], [], [])
    if not region_data.enable_requirements(opts):
        return result
    region = Region(region_data.name, world.player, world.multiworld)
    world.multiworld.regions.append(region)

    locations = region_data.get_locations_dict()
    region.add_locations(locations, PeaksOfYoreLocation)

    for location, address in locations.items():
        if address < rope_offset:
            result.peaks_in_pool.append(location)
        elif artefact_offset < address < book_offset:
            result.artefacts_in_pool.append(location)
        elif time_attack_time_offset < address:
            result.time_attack_in_pool.append(location)

    if parent_region is not None:
        entry_requirements = dict(region_data.entry_requirements)
        if (((region_data.is_peak and opts.game_mode == GameMode.option_book_unlock) or
            (region_data.is_book and opts.game_mode == GameMode.option_peak_unlock)) and
            len(entry_requirements) != 0):
            # if region is peak and unlock is book or region is book and unlock is peak,
            # remove the last entry requirement, which is only useful in the other gamemode
            # i.e. the requirement to unlock a peak before being able to enter it's region should be removed if playing
            # book unlock mode
            # WARNING: I'll probably want to change this as this assumes that any other "normal" requirements are placed before, which can easily lead to problems
            entry_requirements.popitem()

        parent_region.connect(region, region_data.name + " Connection", lambda state: state.has_all_counts(
            entry_requirements, world.player))

    for r in region_data.subregions:
        tempres = recursive_create_region(r, region, world, opts)
        result.peaks_in_pool.extend(tempres.peaks_in_pool)
        result.artefacts_in_pool.extend(tempres.artefacts_in_pool)
        result.time_attack_in_pool.extend(tempres.time_attack_in_pool)
    return result
