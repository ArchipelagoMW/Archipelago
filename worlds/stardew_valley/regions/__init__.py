from collections.abc import Iterable
from random import Random
from typing import Protocol

from BaseClasses import Region, Entrance
from .entrance_rando import randomize_connections
from .regions import create_connections_and_regions
from ..content import StardewContent
from ..options import StardewValleyOptions

__exports__ = ['create_regions', 'RegionFactory']


class RegionFactory(Protocol):
    def __call__(self, name: str, exits: Iterable[str]) -> Region:
        raise NotImplementedError


def create_regions(region_factory: RegionFactory, random: Random, world_options: StardewValleyOptions, content: StardewContent) \
        -> tuple[dict[str, Region], dict[str, Entrance], dict[str, str]]:
    entrances_data, regions_data = create_connections_and_regions(world_options)

    regions_by_name: dict[str: Region] = {
        region_name: region_factory(region_name, region.exits)
        for region_name, region in regions_data.items()
    }

    entrances_by_name: dict[str: Entrance] = {
        entrance.name: entrance
        for region in regions_by_name.values()
        for entrance in region.exits
        if entrance.name in entrances_data
    }

    connections, randomized_data = randomize_connections(random, world_options, content, regions_data, entrances_data)

    for connection in connections:
        if connection.name in entrances_by_name:
            entrances_by_name[connection.name].connect(regions_by_name[connection.destination])
    return regions_by_name, entrances_by_name, randomized_data
