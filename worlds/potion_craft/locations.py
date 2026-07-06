from typing import NamedTuple, Optional, Dict

from BaseClasses import Location, Region
from . import POTION_CRAFT, PotionCraftBase
from .data import LocationTypeEnum
from .data.locations import all_locations
from .data.regions import all_regions, ChapterRegions, all_connections


class PotionCraftLocation(Location):
    game: str = POTION_CRAFT


def create_location(world: PotionCraftBase, location_type: LocationTypeEnum):
    region = world.get_region(location_type.region.value)
    location = Location(world.player, location_type.value, location_type.location_id, region)
    location.progress_type = location_type.progress_type
    region.locations.append(location)
    world.set_rule(location, location_type.rule)

def create_locations(world: PotionCraftBase):
    for location_type in all_locations:
        create_location(world, location_type)


def create_region(world: PotionCraftBase, region_name: str):
    region = Region(region_name, world.player, world.multiworld)
    world.multiworld.regions.append(region)

def create_regions(world: PotionCraftBase):
    create_region(world, "Menu")
    for region_type in all_regions:
        create_region(world,region_type.value)



def create_entrances(world: PotionCraftBase):
    menu = world.get_region("Menu")
    world.create_entrance(menu, world.get_region(ChapterRegions.CHAPTER_1.value), name="Menu To Chapter 1")
    for entrance_type in all_connections:
        world.create_entrance(world.get_region(entrance_type.exiting_region.value), world.get_region(entrance_type.entering_region.value), name=entrance_type.value, rule=entrance_type.rule)

