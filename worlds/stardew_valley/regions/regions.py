from typing import Protocol, Dict

from BaseClasses import Region
from . import vanilla_data, mods
from .entrance_rando import create_player_randomization_flag, connect_regions
from .model import ConnectionData, RegionData
from ..content import StardewContent
from ..mods.mod_data import ModNames
from ..options import StardewValleyOptions, IncludeEndgameLocations
from ..strings.ap_names.ap_option_names import StartWithoutOptionName
from ..strings.entrance_names import Entrance
from ..strings.region_names import Region as RegionName


class RegionFactory(Protocol):
    def __call__(self, name: str) -> Region:
        raise NotImplementedError


def create_regions(region_factory: RegionFactory, world_options: StardewValleyOptions, content: StardewContent) -> tuple[dict[str, Region], dict[str, str]]:
    # the ginger island regions are now a content pack instead of a special case, but this does mean the pack needs to be registerd
    if not world_options.exclude_ginger_island.value:
        content.registered_packs.add(ModNames.ginger_island)

    connection_data_by_name, region_data_by_name = create_connections_and_regions(content.registered_packs)

    regions_by_name: dict[str: Region] = {
        region_name: region_factory(region_name)
        for region_name in region_data_by_name
    }

    connect_starting_region(regions_by_name, world_options)

    randomization_flag = create_player_randomization_flag(world_options.entrance_randomization, world_options.entrance_randomization_behavior.value,
                                                          world_options.include_endgame_locations == IncludeEndgameLocations.option_true, content)

    is_chaos = world_options.entrance_randomization_behavior.is_chaos()
    randomized_entrances = connect_regions(region_data_by_name, connection_data_by_name, regions_by_name, randomization_flag,
                                           world_options.entrance_plando.value, is_chaos)

    return regions_by_name, randomized_entrances


def connect_starting_region(regions_by_name: Dict[str, Region], world_options: StardewValleyOptions):
    menu_region = regions_by_name[RegionName.stardew_valley]
    if StartWithoutOptionName.house in world_options.start_without:
        menu_region.connect(regions_by_name[RegionName.farm], Entrance.to_farm)
    else:
        menu_region.connect(regions_by_name[RegionName.farm_house], Entrance.to_farmhouse)


def create_connections_and_regions(active_content_packs: set[str]) -> tuple[dict[str, ConnectionData], dict[str, RegionData]]:
    regions_by_name = create_all_regions(active_content_packs)
    connections_by_name = create_all_connections(active_content_packs)

    return connections_by_name, regions_by_name


def create_all_regions(active_content_packs: set[str]) -> dict[str, RegionData]:
    current_regions_by_name = create_vanilla_regions()
    mods.modify_regions_for_mods(current_regions_by_name, sorted(active_content_packs))
    return current_regions_by_name


def create_vanilla_regions() -> dict[str, RegionData]:
    return {**vanilla_data.regions_without_ginger_island_by_name}


def create_all_connections(active_content_packs: set[str]) -> dict[str, ConnectionData]:
    connections = create_vanilla_connections()
    mods.modify_connections_for_mods(connections, sorted(active_content_packs))
    return connections


def create_vanilla_connections() -> dict[str, ConnectionData]:
    return {**vanilla_data.connections_without_ginger_island_by_name}
