from typing import NamedTuple

from BaseClasses import Region, Location
from .options import PeaksOfYoreOptions
from worlds.AutoWorld import World
from .data import *


class PeaksOfYoreLocation(Location):
    game = "Peaks of Yore"


class RegionLocationInfo(NamedTuple):
    artefacts_in_pool: list[str]
    peaks_in_pool: list[str]
    time_attack_in_pool: list[str]


def create_poy_regions(world: World, options: PeaksOfYoreOptions) -> RegionLocationInfo:
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    cabin_region = Region("Cabin", world.player, world.multiworld)
    world.multiworld.regions.append(cabin_region)
    menu_region.connect(cabin_region)

    result = RegionLocationInfo([], [], [])

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


def create_region(name: str, region_enum: PeaksOfYoreRegion, item_requirements: dict[str, int],
                  cabin_region: Region, world: World, options: PeaksOfYoreOptions) -> RegionLocationInfo:
    peaks_region = Region(name, world.player, world.multiworld)

    ropes: dict[str: int] = locations_to_dict(ropes_list[region_enum])
    artefacts: dict[str: int] = locations_to_dict(artefacts_list[region_enum])
    bird_seeds: dict[str: int] = locations_to_dict(bird_seeds_list[region_enum])
    # simple things above
    # shenanigans below

    regional_peaks_list: list[ItemOrLocation] = peaks_list[region_enum]
    removeST: bool = False
    if region_enum == PeaksOfYoreRegion.EXPERT and options.disable_solemn_tempest:
        removeST = True
        for peak in regional_peaks_list:
            if peak.id == 37:
                regional_peaks_list.remove(peak)

    peaks: dict[str: int] = locations_to_dict(regional_peaks_list)

    free_solo_peaks: dict[str: int] = {}
    if options.include_free_solo and region_enum not in (PeaksOfYoreRegion.FUNDAMENTALS,
                                                         PeaksOfYoreRegion.INTERMEDIATE):
        free_solo_peaks = locations_to_dict(free_solo_peak_list[region_enum])
        if removeST:
            free_solo_peaks.pop("Solemn Tempest (Free Solo)")

    all_locations: dict[str: int] = {**ropes, **artefacts, **bird_seeds, **peaks, **free_solo_peaks}

    peaks_region.add_locations(all_locations, PeaksOfYoreLocation)
    cabin_region.connect(peaks_region, name + " Connection", lambda state: state.has_all_counts(item_requirements,
                                                                                                world.player))

    time_attack_checks: list[str] = []

    if options.include_time_attack:
        time_attack_time: dict[str: int] = locations_to_dict(time_attack_time_list[region_enum])
        time_attack_ropes: dict[str: int] = locations_to_dict(time_attack_ropes_list[region_enum])
        time_attack_holds: dict[str: int] = locations_to_dict(time_attack_holds_list[region_enum])

        time_attack_checks = [*time_attack_time.keys(), *time_attack_ropes.keys(), *time_attack_holds.keys()]

        time_attack_region = Region(name + " (Time Attack)", world.player, world.multiworld)
        time_attack_region.add_locations({**time_attack_time, **time_attack_ropes, **time_attack_holds},
                                         PeaksOfYoreLocation)
        peaks_region.connect(time_attack_region, name + " Time Attack Connection",
                             lambda state: state.has("Pocketwatch", world.player))

    return RegionLocationInfo([*artefacts.keys()], [*peaks.keys()], time_attack_checks)


def locations_to_dict(locations: list[ItemOrLocation]) -> dict[str: int]:
    return {loc.name: loc.id for loc in locations}
