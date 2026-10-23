from ...mods.region_data import region_data_by_content_pack
from .ginger_island_data import ginger_island_connections, ginger_island_regions
from .model import (
    ConnectionData,
    GroupFlag,
    MergeFlag,
    ModRegionsData,
    RandomizationFlag,
    RegionData,
    reverse_connection_name,
)
from .vanilla_data import (
    connections_without_ginger_island_by_name,
    regions_without_ginger_island_by_name,
    vanilla_connections,
    vanilla_regions,
)

__all__ = [
    "ConnectionData",
    "GroupFlag",
    "MergeFlag",
    "ModRegionsData",
    "RandomizationFlag",
    "RegionData",
    "connections_without_ginger_island_by_name",
    "ginger_island_connections",
    "ginger_island_regions",
    "randomizable_entrances",
    "randomizable_exits",
    "regions_without_ginger_island_by_name",
    "reverse_connection_name",
    "vanilla_connections",
    "vanilla_regions",
]


randomizable_entrances = frozenset(
    connection.destination_entrance_name
    for connection_group in [vanilla_connections, ginger_island_connections]
    + [region_data.connections for region_data in region_data_by_content_pack.values()]
    for connection in connection_group
)

randomizable_exits = frozenset(
    connection.name
    for connection_group in [vanilla_connections, ginger_island_connections]
    + [region_data.connections for region_data in region_data_by_content_pack.values()]
    for connection in connection_group
)
