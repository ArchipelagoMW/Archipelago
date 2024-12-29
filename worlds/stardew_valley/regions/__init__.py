from typing import Protocol

from BaseClasses import Region, Entrance
from entrance_rando import disconnect_entrance_for_randomization
from .entrance_rando import randomize_connections, create_randomization_flag_mask
from .regions import create_connections_and_regions
from ..content import StardewContent
from ..options import StardewValleyOptions

__exports__ = ['create_regions', 'RegionFactory']


class RegionFactory(Protocol):
    def __call__(self, name: str) -> Region:
        raise NotImplementedError


def create_regions(region_factory: RegionFactory, world_options: StardewValleyOptions, content: StardewContent) \
        -> tuple[dict[str, Region], dict[str, Entrance]]:
    entrance_data_by_name, region_data_by_name = create_connections_and_regions(content.registered_packs)

    regions_by_name: dict[str: Region] = {
        region_name: region_factory(region_name)
        for region_name in region_data_by_name
    }

    entrances_by_name: dict[str: Entrance] = {}

    # Not really a mask... :thinking:
    randomization_flag = create_randomization_flag_mask(world_options.entrance_randomization, content)

    for region_name, region_data in region_data_by_name.items():
        origin_region = regions_by_name[region_name]

        for entrance_name in region_data.exits:
            entrance_data = entrance_data_by_name[entrance_name]
            destination_region = regions_by_name[entrance_data.destination]
            entrance = origin_region.connect(destination_region, entrance_name)

            if randomization_flag and randomization_flag in entrance_data.flag:
                disconnect_entrance_for_randomization(entrance)

    return regions_by_name, entrances_by_name
