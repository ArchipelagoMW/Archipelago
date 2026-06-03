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
    "Cherrygrove City",
    "Route 30",
    "Violet City",
    "Route 32",
    "Union Cave",
    "Azalea Town",
    "Ilex Forest",
    "Goldenrod City",
    "Goldenrod Radio Tower",
    "Route 35",
    "National Park",
    "Ecruteak City",
    "Olivine City",
    "Olivine Lighthouse",
    "Cianwood City",
    "Mahogany Town",
    "Lake of Rage",
    "Goldenrod Underground",
    "Blackthorn City",
    "Victory Road",
    "Pokemon League",
)


REGION_CONNECTIONS = (
    RegionConnection("Menu", "New Bark Town", "Menu to New Bark Town"),
    RegionConnection("New Bark Town", "Cherrygrove City", "New Bark Town to Cherrygrove City"),
    RegionConnection("Cherrygrove City", "Route 30", "Cherrygrove City to Route 30"),
    RegionConnection("Route 30", "Violet City", "Route 30 to Violet City"),

    RegionConnection("Violet City", "Route 32", "Violet City to Route 32"),
    RegionConnection("Route 32", "Union Cave", "Route 32 to Union Cave"),
    RegionConnection("Union Cave", "Azalea Town", "Union Cave to Azalea Town"),

    RegionConnection("Azalea Town", "Ilex Forest", "Azalea Town to Ilex Forest"),
    RegionConnection("Ilex Forest", "Goldenrod City", "Ilex Forest to Goldenrod City"),

    RegionConnection("Goldenrod City", "Goldenrod Radio Tower", "Goldenrod City to Goldenrod Radio Tower"),
    RegionConnection("Goldenrod City", "Route 35", "Goldenrod City to Route 35"),
    RegionConnection("Route 35", "National Park", "Route 35 to National Park"),
    RegionConnection("National Park", "Ecruteak City", "National Park to Ecruteak City"),

    RegionConnection("Ecruteak City", "Olivine City", "Ecruteak City to Olivine City"),
    RegionConnection("Olivine City", "Olivine Lighthouse", "Olivine City to Olivine Lighthouse"),
    RegionConnection("Olivine City", "Cianwood City", "Olivine City to Cianwood City"),

    RegionConnection("Ecruteak City", "Mahogany Town", "Ecruteak City to Mahogany Town"),
    RegionConnection("Mahogany Town", "Lake of Rage", "Mahogany Town to Lake of Rage"),

    RegionConnection("Goldenrod City", "Goldenrod Underground", "Goldenrod City to Goldenrod Underground"),

    RegionConnection("Mahogany Town", "Blackthorn City", "Mahogany Town to Blackthorn City"),
    RegionConnection("Blackthorn City", "Victory Road", "Blackthorn City to Victory Road"),
    RegionConnection("Victory Road", "Pokemon League", "Victory Road to Pokemon League"),
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