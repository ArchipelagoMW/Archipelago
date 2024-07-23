from typing import Dict, Any, ClassVar
import settings

from Utils import local_path, visualize_regions
from BaseClasses import Item, ItemClassification, Tutorial
from .GameID import jak1_id, jak1_name, jak1_max
from .JakAndDaxterOptions import JakAndDaxterOptions, EnableOrbsanity
from .Locations import JakAndDaxterLocation, location_table
from .Items import JakAndDaxterItem, item_table
from .locs import (CellLocations as Cells,
                   ScoutLocations as Scouts,
                   SpecialLocations as Specials,
                   OrbCacheLocations as Caches,
                   OrbLocations as Orbs)
from .Regions import create_regions
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="JakAndDaxterClient")


components.append(Component("Jak and Daxter Client",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="egg"))

icon_paths["egg"] = local_path("worlds", "jakanddaxter", "icons", "egg.png")


class JakAndDaxterSettings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """Path to folder containing the ArchipelaGOAL mod executables (gk.exe and goalc.exe)."""
        description = "ArchipelaGOAL Root Directory"

    root_directory: RootDirectory = RootDirectory("D:/Files/Repositories/ArchipelaGOAL/out/build/Release/bin")


class JakAndDaxterWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ArchipelaGOAL (Archipelago on OpenGOAL).",
        "English",
        "setup_en.md",
        "setup/en",
        ["markustulliuscicero"]
    )

    tutorials = [setup_en]


class JakAndDaxterWorld(World):
    """
    Jak and Daxter: The Precursor Legacy is a 2001 action platformer developed by Naughty Dog
    for the PlayStation 2. The game follows the eponymous protagonists, a young boy named Jak
    and his friend Daxter, who has been transformed into an ottsel. With the help of Samos
    the Sage of Green Eco and his daughter Keira, the pair travel north in search of a cure for Daxter,
    discovering artifacts created by an ancient race known as the Precursors along the way. When the
    rogue sages Gol and Maia Acheron plan to flood the world with Dark Eco, they must stop their evil plan
    and save the world.
    """
    # ID, name, version
    game = jak1_name
    required_client_version = (0, 4, 6)

    # Options
    settings: ClassVar[JakAndDaxterSettings]
    options_dataclass = JakAndDaxterOptions
    options: JakAndDaxterOptions

    # Web world
    web = JakAndDaxterWebWorld()

    # Stored as {ID: Name} pairs, these must now be swapped to {Name: ID} pairs.
    # Remember, the game ID and various offsets for each item type have already been calculated.
    item_name_to_id = {item_table[k]: k for k in item_table}
    location_name_to_id = {location_table[k]: k for k in location_table}
    item_name_groups = {
        "Power Cells": {item_table[k]: k for k in item_table
                        if k in range(jak1_id, jak1_id + Scouts.fly_offset)},
        "Scout Flies": {item_table[k]: k for k in item_table
                        if k in range(jak1_id + Scouts.fly_offset, jak1_id + Specials.special_offset)},
        "Specials": {item_table[k]: k for k in item_table
                     if k in range(jak1_id + Specials.special_offset, jak1_id + Caches.orb_cache_offset)},
        "Moves": {item_table[k]: k for k in item_table
                  if k in range(jak1_id + Caches.orb_cache_offset, jak1_id + Orbs.orb_offset)},
        "Precursor Orbs": {item_table[k]: k for k in item_table
                           if k in range(jak1_id + Orbs.orb_offset, jak1_max)},
    }

    # This will also set Locations, Location access rules, Region access rules, etc.
    def create_regions(self) -> None:
        create_regions(self.multiworld, self.options, self.player)
        visualize_regions(self.multiworld.get_region("Menu", self.player), "jakanddaxter.puml")

    # Helper function to get the correct orb bundle size.
    def get_orb_bundle_size(self) -> int:
        if self.options.enable_orbsanity == EnableOrbsanity.option_per_level:
            return self.options.level_orbsanity_bundle_size.value
        elif self.options.enable_orbsanity == EnableOrbsanity.option_global:
            return self.options.global_orbsanity_bundle_size.value
        else:
            return 0

    # Helper function to reuse some nasty if/else trees.
    def item_type_helper(self, item) -> (int, ItemClassification):
        # Make 101 Power Cells.
        if item in range(jak1_id, jak1_id + Scouts.fly_offset):
            classification = ItemClassification.progression_skip_balancing
            count = 101

        # Make 7 Scout Flies per level.
        elif item in range(jak1_id + Scouts.fly_offset, jak1_id + Specials.special_offset):
            classification = ItemClassification.progression_skip_balancing
            count = 7

        # Make only 1 of each Special Item.
        elif item in range(jak1_id + Specials.special_offset, jak1_id + Caches.orb_cache_offset):
            classification = ItemClassification.progression
            count = 1

        # Make only 1 of each Move Item.
        elif item in range(jak1_id + Caches.orb_cache_offset, jak1_id + Orbs.orb_offset):
            classification = ItemClassification.progression
            count = 1

        # Make N Precursor Orb bundles, where N is 2000 / bundle size.
        elif item in range(jak1_id + Orbs.orb_offset, jak1_max):
            classification = ItemClassification.progression_skip_balancing
            size = self.get_orb_bundle_size()
            count = int(2000 / size) if size > 0 else 0  # Don't divide by zero!

        # Under normal circumstances, we will create 0 filler items.
        # We will manually create filler items as needed.
        elif item == jak1_max:
            classification = ItemClassification.filler
            count = 0

        # If we try to make items with ID's higher than we've defined, something has gone wrong.
        else:
            raise KeyError(f"Tried to fill item pool with unknown ID {item}.")

        return count, classification

    def create_items(self) -> None:
        for item_name in self.item_name_to_id:
            item_id = self.item_name_to_id[item_name]

            # Handle Move Randomizer option.
            # If it is OFF, put all moves in your starting inventory instead of the item pool,
            # then fill the item pool with a corresponding amount of filler items.
            if item_name in self.item_name_groups["Moves"] and not self.options.enable_move_randomizer:
                self.multiworld.push_precollected(self.create_item(item_name))
                self.multiworld.itempool += [self.create_item(self.get_filler_item_name())]
                continue

            # Handle Orbsanity option.
            # If it is OFF, don't add any orbs to the item pool.
            # If it is ON, don't add any orb bundles that don't match the chosen option.
            if (item_name in self.item_name_groups["Precursor Orbs"]
                and ((self.options.enable_orbsanity == EnableOrbsanity.option_off
                      or Orbs.to_game_id(item_id) != self.get_orb_bundle_size()))):
                continue

            # In every other scenario, do this.
            count, classification = self.item_type_helper(item_id)
            self.multiworld.itempool += [JakAndDaxterItem(item_name, classification, item_id, self.player)
                                         for _ in range(count)]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        _, classification = self.item_type_helper(item_id)
        return JakAndDaxterItem(name, classification, item_id, self.player)

    def get_filler_item_name(self) -> str:
        return "Green Eco Pill"

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict("enable_move_randomizer",
                                    "enable_orbsanity",
                                    "global_orbsanity_bundle_size",
                                    "level_orbsanity_bundle_size",
                                    "fire_canyon_cell_count",
                                    "mountain_pass_cell_count",
                                    "lava_tube_cell_count",
                                    "completion_condition")
