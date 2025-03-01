from BaseClasses import Region, MultiWorld
from .options import PeaksOfYoreOptions
from worlds.AutoWorld import World
from .locations import get_locations, get_location_names_by_type, PeaksOfYoreLocation
from .data import PeaksOfYoreRegion


def create_poy_regions(poy_world: "PeaksOfWorld", options: PeaksOfYoreOptions) -> None:
    world: World = poy_world
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    cabin_region = Region("Cabin", world.player, world.multiworld)
    world.multiworld.regions.append(cabin_region)
    menu_region.connect(cabin_region)

    if options.enable_fundamental:
        create_region("Fundamental Peaks", PeaksOfYoreRegion.FUNDAMENTALS, {"Fundamentals Book": 1},
                      cabin_region, poy_world)

    if options.enable_intermediate:
        create_region("Intermediate Peaks", PeaksOfYoreRegion.INTERMEDIATE, {"Intermediate Book": 1},
                      cabin_region, poy_world)

    if options.enable_advanced:
        create_region("Advanced Peaks", PeaksOfYoreRegion.ADVANCED, {"Advanced Book": 1}, cabin_region, poy_world)

    if options.enable_expert:
        create_region("Expert Peaks", PeaksOfYoreRegion.EXPERT, {"Expert Book": 1, "Progressive Crampons": 1},
                      cabin_region, poy_world)


def create_region(region_name: str, region_enum: PeaksOfYoreRegion, item_requirements: dict[str: int],
                  cabin_region: Region, poy_world: "PeaksOfWorld"):
    world: World = poy_world
    region = Region(region_name, world.player, world.multiworld)

    peaks = get_location_names_by_type(region_enum, "Peak")
    if "Solemn Tempest" in peaks and poy_world.options.disable_solemn_tempest:
        peaks.remove("Solemn Tempest")
    poy_world.peaks_in_pool.extend(peaks)

    poy_world.artefacts_in_pool.extend(get_location_names_by_type(region_enum, "Artefact"))

    locations = {k: v for k, v in get_locations(region_enum).items() if (not poy_world.options.disable_solemn_tempest)
                 or k == "Solemn Tempest"}

    region.add_locations(locations, PeaksOfYoreLocation)
    cabin_region.connect(region, region_name + " Connection", lambda state:
                                                                state.has_all_counts(item_requirements, world.player))
    world.location_count += len(region.locations)
