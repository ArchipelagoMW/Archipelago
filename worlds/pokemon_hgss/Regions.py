from BaseClasses import Region

from .Locations import (
    PokemonHGSSLocation,
    get_locations_for_region,
)


REGION_ORDER = (
    "Menu",
    "Violet City",
    "Azalea Town",
    "Goldenrod City",
    "Ecruteak City",
    "Cianwood City",
    "Olivine City",
    "Mahogany Town",
    "Blackthorn City",
    "Pokemon League",
)


REGION_CONNECTIONS = (
    ("Menu", "Violet City"),
    ("Violet City", "Azalea Town"),
    ("Azalea Town", "Goldenrod City"),
    ("Goldenrod City", "Ecruteak City"),
    ("Ecruteak City", "Cianwood City"),
    ("Cianwood City", "Olivine City"),
    ("Olivine City", "Mahogany Town"),
    ("Mahogany Town", "Blackthorn City"),
    ("Blackthorn City", "Pokemon League"),
)


def create_region(world, region_name: str) -> Region:
    region = Region(region_name, world.player, world.multiworld)

    for location_data in get_locations_for_region(region_name):
        location = PokemonHGSSLocation(
            world.player,
            location_data.name,
            location_data.code,
            region,
        )

        region.locations.append(location)

    return region


def create_hgss_regions(world) -> None:
    regions = [
        create_region(world, region_name)
        for region_name in REGION_ORDER
    ]

    world.multiworld.regions += regions

    for source_region_name, target_region_name in REGION_CONNECTIONS:
        source_region = world.multiworld.get_region(
            source_region_name,
            world.player,
        )

        target_region = world.multiworld.get_region(
            target_region_name,
            world.player,
        )

        source_region.connect(target_region)