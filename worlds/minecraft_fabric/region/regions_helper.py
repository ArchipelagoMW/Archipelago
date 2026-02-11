from __future__ import annotations


from typing import TYPE_CHECKING, Optional


from worlds.minecraft_fabric.logic.vanilla_logic import *


if TYPE_CHECKING:
   from worlds.minecraft_fabric import FabricMinecraftWorld


from BaseClasses import Region, Location, CollectionState, Entrance
from worlds.minecraft_fabric.location.minecraft_locations import location_table

# HELPER METHODS #######################################################################################################

# Determines whether a location is included
def blacklisted_location(world: FabricMinecraftWorld, location_type: int):
    exclusions = {
        0: False,                                                                       # Default Advancement
        1: "Hard" in world.options.excluded_locations.value,                            # Hard Advancement
        2: "Exploration" in world.options.excluded_locations.value,                     # Exploration Advancement
        3: "Unreasonable" in world.options.excluded_locations.value,                    # Unreasonable Advancement

        5: False,                                                                       # Default Itemsanity
        6: "Hard" in world.options.excluded_locations.value,                            # Hard Itemsanity
        7: "Exploration" in world.options.excluded_locations.value,                     # Exploration Itemsanity
        8: "Unreasonable" in world.options.excluded_locations.value,                    # Unreasonable Itemsanity

        9: "Discs" in world.options.excluded_from_itemsanity.value,                     # Music Disc Checks
        10: "Rare Ores" in world.options.excluded_from_itemsanity.value,                # Rare Ore Checks
        11: "Mob Heads" in world.options.excluded_from_itemsanity.value,                # Mob Head Checks
        12: "Netherite Gear" in world.options.excluded_from_itemsanity.value,           # Netherite Gear Checks
        13: "Trims" in world.options.excluded_from_itemsanity.value,                    # Armor Trim Checks
        14: "Sherds" in world.options.excluded_from_itemsanity.value                    # Pottery Sherd Checks
    }

    if location_type in exclusions:
        if exclusions[location_type]:
            return True

    if location_type in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14] and not world.options.itemsanity:
        return True

    return False

# Creates a Region with Locations, and Excludes Unused Locations based on settings
def create_locations_advanced(world: FabricMinecraftWorld, region_name: str, locations: dict[str, int]):
   location_list = []

   for location, location_type in locations.items():
       if blacklisted_location(world, location_type):
           continue

       location_list.append(location)

   return create_locations(world, region_name, location_list)

# Creates a Region and Locations, also adds Itemsanity Locations to a list for excluding based on Localfill
def create_locations(world: FabricMinecraftWorld, region_name: str, locations: list[str]):
   region = Region(region_name, world.player, world.multiworld, region_name)

   for name in locations:
       location = Location(world.player, name, location_table[name], region)
       if name.endswith("(Itemsanity)"):
          world.itemsanity_locations.append(name)
       region.locations.append(location)

   world.multiworld.regions.append(region)


# Connects 2 Regions together!
def connect(world, source: str, target: str, rule=None) -> Optional[Entrance]:
   source_region = world.multiworld.get_region(source, world.player)
   target_region = world.multiworld.get_region(target, world.player)


   connection = Entrance(world.player, source + " ==> " + target, source_region)

   if rule:
       connection.access_rule = rule


   source_region.exits.append(connection)
   connection.connect(target_region)


   return connection

# Creates a Region with Locations, and Connects it to a parent Region
def create_locations_and_connect(world: FabricMinecraftWorld, region_name: str, new_region_name: str, locations: dict[str, int], rule=None):
   create_locations_advanced(world, new_region_name, locations)
   connect(world, region_name, new_region_name, rule)