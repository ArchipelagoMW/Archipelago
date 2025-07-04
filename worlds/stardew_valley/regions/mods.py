from collections.abc import Iterable

from .model import ConnectionData, RegionData, ModRegionsData
from ..mods.region_data import region_data_by_content_pack, vanilla_connections_to_remove_by_content_pack


def modify_regions_for_mods(current_regions_by_name: dict[str, RegionData], active_content_packs: Iterable[str]) -> None:
    for content_pack in active_content_packs:
        try:
            region_data = region_data_by_content_pack[content_pack]
        except KeyError:
            continue

        merge_mod_regions(current_regions_by_name, region_data)


def merge_mod_regions(current_regions_by_name: dict[str, RegionData], mod_region_data: ModRegionsData) -> None:
    for new_region in mod_region_data.regions:
        region_name = new_region.name
        try:
            current_region = current_regions_by_name[region_name]
        except KeyError:
            current_regions_by_name[region_name] = new_region
            continue

        current_regions_by_name[region_name] = current_region.merge_with(new_region)


def modify_connections_for_mods(connections: dict[str, ConnectionData], active_mods: Iterable[str]) -> None:
    for active_mod in active_mods:
        try:
            region_data = region_data_by_content_pack[active_mod]
        except KeyError:
            continue

        try:
            vanilla_connections_to_remove = vanilla_connections_to_remove_by_content_pack[active_mod]
            for connection_name in vanilla_connections_to_remove:
                connections.pop(connection_name)
        except KeyError:
            pass

        connections.update({
            connection.name: connection
            for connection in region_data.connections
        })
