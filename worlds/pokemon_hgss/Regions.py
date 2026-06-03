from dataclasses import dataclass

from BaseClasses import Region

from .Locations import (
    PokemonHGSSLocation,
    get_locations_for_region,
)


@dataclass(frozen=True)
class RegionConnection:
    source: str
    target: str
    entrance_name: str


REGION_ORDER = (
    "Menu",
    "New Bark Town",
    "Route 30",
    "Violet City",
    "Azalea Town",
    "Ilex Forest",
    "Goldenrod City",
    "Goldenrod Radio Tower",
    "Ecruteak City",
    "Olivine City",
    "Olivine Lighthouse",
    "Cianwood City",
    "Mahogany Town",
    "Goldenrod Underground",
    "Blackthorn City",
    "Pokemon League",
)


REGION_CONNECTIONS = (
    RegionConnection("Menu", "New Bark Town", "Menu to New Bark Town"),
    RegionConnection("New Bark Town", "Route 30", "New Bark Town to Route 30"),
    RegionConnection("Route 30", "Violet City", "Route 30 to Violet City"),
    RegionConnection("Violet City", "Azalea Town", "Violet City to Azalea Town"),
    RegionConnection("Azalea Town", "Ilex Forest", "Azalea Town to Ilex Forest"),
    RegionConnection("Ilex Forest", "Goldenrod City", "Ilex Forest to Goldenrod City"),
    RegionConnection("Goldenrod City", "Goldenrod Radio Tower", "Goldenrod City to Goldenrod Radio Tower"),
    RegionConnection("Goldenrod City", "Ecruteak City", "Goldenrod City to Ecruteak City"),
    RegionConnection("Ecruteak City", "Olivine City", "Ecruteak City to Olivine City"),
    RegionConnection("Olivine City", "Olivine Lighthouse", "Olivine City to Olivine Lighthouse"),
    RegionConnection("Olivine City", "Cianwood City", "Olivine City to Cianwood City"),
    RegionConnection("Ecruteak City", "Mahogany Town", "Ecruteak City to Mahogany Town"),
    RegionConnection("Goldenrod City", "Goldenrod Underground", "Goldenrod City to Goldenrod Underground"),
    RegionConnection("Mahogany Town", "Blackthorn City", "Mahogany Town to Blackthorn City"),
    RegionConnection("Blackthorn City", "Pokemon League", "Blackthorn City to Pokemon League"),
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

    for connection in REGION_CONNECTIONS:
        source_region = world.multiworld.get_region(
            connection.source,
            world.player,
        )

        target_region = world.multiworld.get_region(
            connection.target,
            world.player,
        )

        source_region.connect(
            target_region,
            connection.entrance_name,
        )