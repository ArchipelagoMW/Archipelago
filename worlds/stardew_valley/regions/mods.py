from collections.abc import Iterable

from .model import ConnectionData, RegionData, ModRegionsData
from ..mods.region_data import region_data_by_mod, vanilla_connections_to_remove_by_mod


def add_mods_regions(current_regions_by_name: dict[str, RegionData], active_mods: Iterable[str]) -> None:
    for active_mod in active_mods:
        try:
            region_data = region_data_by_mod[active_mod]
        except KeyError:
            continue

        add_mod_regions(current_regions_by_name, region_data)


def add_mod_regions(current_regions_by_name: dict[str, RegionData], mod_region_data: ModRegionsData) -> None:
    for new_region in mod_region_data.regions:
        region_name = new_region.name
        try:
            current_region = current_regions_by_name[region_name]
        except KeyError:
            current_regions_by_name[region_name] = new_region
            continue

        current_regions_by_name[region_name] = current_region.merge_with(new_region)


def modify_connections_for_mods(connections: dict[str, ConnectionData], active_mods: Iterable[str]) -> dict[str, ConnectionData]:
    for active_mod in active_mods:
        if active_mod not in region_data_by_mod:
            continue

        if active_mod in vanilla_connections_to_remove_by_mod:
            for connection_data in vanilla_connections_to_remove_by_mod[active_mod]:
                connections.pop(connection_data.name)

        connections.update({connection.name: connection for connection in region_data_by_mod[active_mod].connections})

    return connections
