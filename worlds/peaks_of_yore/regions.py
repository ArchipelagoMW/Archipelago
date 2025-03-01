from typing import NamedTuple

from BaseClasses import Region, MultiWorld
from .options import PeaksOfYoreOptions
from worlds.AutoWorld import World
from .locations import get_locations, get_location_names_by_type, PeaksOfYoreLocation
from .data import PeaksOfYoreRegion


class RegionLocationInfo(NamedTuple):
    artefacts_in_pool: list[str]
    peaks_in_pool: list[str]


def create_poy_regions(world: World, options: PeaksOfYoreOptions) -> RegionLocationInfo:
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    cabin_region = Region("Cabin", world.player, world.multiworld)
    world.multiworld.regions.append(cabin_region)
    menu_region.connect(cabin_region)

    result = RegionLocationInfo([], [])

    if options.enable_fundamental:
        r = create_region("Fundamental Peaks", PeaksOfYoreRegion.FUNDAMENTALS, {"Fundamentals Book": 1},
                          cabin_region, world, options)
        result.peaks_in_pool.extend(r.peaks_in_pool)
        result.artefacts_in_pool.extend(r.artefacts_in_pool)

    if options.enable_intermediate:
        r = create_region("Intermediate Peaks", PeaksOfYoreRegion.INTERMEDIATE, {"Intermediate Book": 1},
                          cabin_region, world, options)
        result.peaks_in_pool.extend(r.peaks_in_pool)
        result.artefacts_in_pool.extend(r.artefacts_in_pool)

    if options.enable_advanced:
        r = create_region("Advanced Peaks", PeaksOfYoreRegion.ADVANCED, {"Advanced Book": 1},
                          cabin_region, world, options)
        result.peaks_in_pool.extend(r.peaks_in_pool)
        result.artefacts_in_pool.extend(r.artefacts_in_pool)

    if options.enable_expert:
        r = create_region("Expert Peaks", PeaksOfYoreRegion.EXPERT, {"Expert Book": 1, "Progressive Crampons": 1},
                          cabin_region, world, options)
        result.peaks_in_pool.extend(r.peaks_in_pool)
        result.artefacts_in_pool.extend(r.artefacts_in_pool)
    return result


def create_region(region_name: str, region_enum: PeaksOfYoreRegion, item_requirements: dict[str: int],
                  cabin_region: Region, world: World, options: PeaksOfYoreOptions) -> RegionLocationInfo:
    region = Region(region_name, world.player, world.multiworld)

    peaks = get_location_names_by_type(region_enum, "Peak")
    if "Solemn Tempest" in peaks and options.disable_solemn_tempest:
        peaks.remove("Solemn Tempest")

    peaks_in_pool = peaks
    artefacts_in_pool = get_location_names_by_type(region_enum, "Artefact")

    locations = {k: v for k, v in get_locations(region_enum).items() if (not options.disable_solemn_tempest)
                 or k != "Solemn Tempest"}

    region.add_locations(locations, PeaksOfYoreLocation)
    cabin_region.connect(region, region_name + " Connection", lambda state: state.has_all_counts(item_requirements,
                                                                                                 world.player))
    world.location_count += len(region.locations)
    return RegionLocationInfo(artefacts_in_pool, peaks_in_pool)
