from . import vanilla_data, mods
from .model import RegionData, ConnectionData
from ..content.vanilla.ginger_island import ginger_island_content_pack


def create_connections_and_regions(active_content_packs: set[str]) -> tuple[dict[str, ConnectionData], dict[str, RegionData]]:
    regions_by_name = create_all_regions(active_content_packs)
    connections_by_name = create_all_connections(active_content_packs)

    return connections_by_name, regions_by_name


def create_vanilla_regions(active_content_packs: set[str]) -> dict[str, RegionData]:
    if ginger_island_content_pack.name in active_content_packs:
        return {**vanilla_data.regions_with_ginger_island_by_name}
    else:
        return {**vanilla_data.regions_without_ginger_island_by_name}


def create_all_regions(active_content_packs: set[str]) -> dict[str, RegionData]:
    current_regions_by_name = create_vanilla_regions(active_content_packs)
    mods.modify_regions_for_mods(current_regions_by_name, active_content_packs)
    return current_regions_by_name


def create_vanilla_connections(active_content_packs: set[str]) -> dict[str, ConnectionData]:
    if ginger_island_content_pack.name in active_content_packs:
        return {**vanilla_data.connections_with_ginger_island_by_name}
    else:
        return {**vanilla_data.connections_without_ginger_island_by_name}


def create_all_connections(active_content_packs: set[str]) -> dict[str, ConnectionData]:
    connections = create_vanilla_connections(active_content_packs)
    mods.modify_connections_for_mods(connections, active_content_packs)
    return connections
