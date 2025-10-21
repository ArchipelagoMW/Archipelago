from typing import TYPE_CHECKING

from BaseClasses import Region
from .Locations import A1800Location, location_list

if TYPE_CHECKING:
    from . import A1800World


def create_regions(world: "A1800World") -> None:
    _create_region(world, "Old World")


def _create_region(world: "A1800World", name: str) -> Region:
    region = Region(name, world.player, world.multiworld)

    for data in location_list:
        if data.region == name:
            location = A1800Location(world.player, data, region)
            region.locations.append(location)

    world.multiworld.regions.append(region)
    return region
