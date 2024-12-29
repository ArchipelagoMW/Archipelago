from typing import Dict

from . import vanilla_data, mods
from .model import RegionData, ConnectionData, RandomizationFlag


def create_connections_and_regions(world_options) -> tuple[dict[str, ConnectionData], dict[str, RegionData]]:
    active_mods = world_options.mods.value

    regions_by_name = create_all_regions(active_mods)
    connections_by_name = create_all_connections(active_mods)

    if world_options.exclude_ginger_island.value:
        remove_ginger_island_regions_and_connections(connections_by_name, regions_by_name)

    return connections_by_name, regions_by_name


def create_vanilla_regions() -> dict[str, RegionData]:
    return {region.name: region for region in vanilla_data.vanilla_regions}


def create_all_regions(active_mods: set[str]) -> dict[str, RegionData]:
    current_regions_by_name = create_vanilla_regions()
    mods.add_mods_regions(current_regions_by_name, active_mods)
    return current_regions_by_name


def create_vanilla_connections() -> dict[str, ConnectionData]:
    return {connection.name: connection for connection in vanilla_data.vanilla_connections}


def create_all_connections(active_mods: set[str]) -> dict[str, ConnectionData]:
    connections = create_vanilla_connections()
    connections = mods.modify_connections_for_mods(connections, active_mods)
    return connections


def remove_ginger_island_regions_and_connections(connections_by_name: dict[str, ConnectionData], regions_by_name: Dict[str, RegionData]):
    connections_to_remove = set()

    for connection_name, connection in connections_by_name.items():
        if connection.flag & RandomizationFlag.GINGER_ISLAND:
            connections_to_remove.add(connection_name)

    regions_to_remove = set()
    for region_name, region in regions_by_name.items():
        if region.is_ginger_island:
            regions_to_remove.add(region_name)
            continue

        regions_by_name[region_name] = region.get_without_exits(connections_to_remove)

    for connection_name in connections_to_remove:
        del connections_by_name[connection_name]
    for region_name in regions_to_remove:
        del regions_by_name[region_name]

    return connections_by_name, regions_by_name
