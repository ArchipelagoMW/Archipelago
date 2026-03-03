from typing import NamedTuple
import logging

from BaseClasses import Region, Location
from .options import *
from worlds.AutoWorld import World
from .data import *

class RegionLocationInfo(NamedTuple):
    artefacts_in_pool: list[str]
    peaks_in_pool: list[str]
    time_attack_in_pool: list[str]
    other_in_pool: list[str]
    total_requirements: dict[str, int]
    entry_requirements: dict[str, int]
    is_entry: bool

    def get_total_location_count(self):
        return (len(self.artefacts_in_pool) + len(self.peaks_in_pool)
                + len(self.time_attack_in_pool) + len(self.other_in_pool))

    def __iadd__(self, other):
        self.artefacts_in_pool.extend(other.artefacts_in_pool)
        self.peaks_in_pool.extend(other.peaks_in_pool)
        self.time_attack_in_pool.extend(other.time_attack_in_pool)
        self.other_in_pool.extend(other.other_in_pool)

        for k,v in other.total_requirements.items():
            if k not in self.total_requirements.keys():
                self.total_requirements[k] = v
            else:
                self.total_requirements[k] = max(v, self.total_requirements[k])

        for k,v in other.entry_requirements.items():
            if k not in self.entry_requirements.keys():
                self.entry_requirements[k] = v
            else:
                self.entry_requirements[k] = max(v, self.entry_requirements[k])

        return self.set_entry(other.is_entry or self.is_entry)

    def set_entry(self, is_entry: bool):
        return RegionLocationInfo(self.artefacts_in_pool, self.peaks_in_pool, self.time_attack_in_pool,
                                  self.other_in_pool, self.total_requirements,
                                  self.entry_requirements, is_entry)

# IDE was yelling at me and not happy that I called a parameter "options", so have "opts"
def create_poy_regions(world: World, opts: PeaksOfYoreOptions) -> RegionLocationInfo:
    result = RegionLocationInfo([], [], [], [], {}, {}, False)

    cabin_region = Region("Cabin", world.player, world.multiworld)
    world.multiworld.regions.append(cabin_region)

    for r in poy_regions.subregions:
        result += recursive_create_region(r, cabin_region, world, opts)

    return result


def recursive_create_region(region_data: POYRegion, parent_region: Region, world: World, opts: PeaksOfYoreOptions) -> \
        RegionLocationInfo:
    """
    Takes a POYRegion, and creates it and its subregions as a subregion of parent_region
    """
    result = RegionLocationInfo([], [], [], [], {}, {}, False)
    if not region_data.enable_requirements(opts):
        return result

    region = Region(region_data.name, world.player, world.multiworld)
    world.multiworld.regions.append(region)

    locations = region_data.get_locations_dict()
    events: list[str] = []

    for name, id in locations.copy().items():
        if id is None:
            locations.pop(name)
            events.append(name)

    for name in events:
        region.add_event(name, location_type=PeaksOfYoreLocation, item_type=PeaksOfYoreItem)
    region.add_locations(locations, PeaksOfYoreLocation)

    for location, address in locations.items():
        if address < rope_offset:
            result.peaks_in_pool.append(location)
        elif artefact_offset < address < book_offset:
            result.artefacts_in_pool.append(location)
        elif time_attack_time_offset < address:
            result.time_attack_in_pool.append(location)
        else:
            result.other_in_pool.append(location)

    entry_requirements = dict(region_data.entry_requirements)

    if parent_region is not None:
        if (((region_data.is_peak and opts.game_mode == GameMode.option_book_unlock) or
            (region_data.is_book and opts.game_mode == GameMode.option_peak_unlock)) and
            len(entry_requirements) != 0):
            # if region is peak and unlock is book or region is book and unlock is peak,
            # remove the last entry requirement, which is only useful in the other gamemode
            # i.e. the requirement to unlock a peak before being able to enter it's region should be removed if playing
            # book unlock mode
            # WARNING: I'll probably want to change this as this assumes that any other "normal" requirements are placed
            #   before, which can easily lead to problems
            entry_requirements.popitem()

        parent_region.connect(region, region_data.name + " Connection", lambda state: state.has_all_counts(
            entry_requirements, world.player))

    for r in region_data.subregions:
        result += recursive_create_region(r, region, world, opts)

    for k, v in entry_requirements.items():
        if k not in result.total_requirements.keys():
            result.total_requirements[k] = v
        else:
            result.total_requirements[k] = max(result.total_requirements[k], v)

    # if one of the subregions gives entry requirements or this one is start
    if result.is_entry or region_data.is_start(opts):
        logging.debug(f"adding {entry_requirements} to entry reqs for {region_data.name}")
        result = result.set_entry(True)
        for k, v in entry_requirements.items():
            if k not in result.entry_requirements.keys():
                result.entry_requirements[k] = v
            else:
                result.entry_requirements[k] = max(v,result.entry_requirements[k])

    return result
