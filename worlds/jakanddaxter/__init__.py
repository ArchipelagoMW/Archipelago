from typing import Dict, Any, ClassVar, Tuple, Callable, Optional
import settings

from Utils import local_path
from BaseClasses import Item, ItemClassification, Tutorial, CollectionState
from .GameID import jak1_id, jak1_name, jak1_max
from .JakAndDaxterOptions import JakAndDaxterOptions, EnableOrbsanity
from .Locations import (JakAndDaxterLocation,
                        location_table,
                        cell_location_table,
                        scout_location_table,
                        special_location_table,
                        cache_location_table,
                        orb_location_table)
from .Items import (JakAndDaxterItem,
                    item_table,
                    cell_item_table,
                    scout_item_table,
                    special_item_table,
                    move_item_table,
                    orb_item_table)
from .Levels import level_table, level_table_with_global
from .locs import (CellLocations as Cells,
                   ScoutLocations as Scouts,
                   SpecialLocations as Specials,
                   OrbCacheLocations as Caches,
                   OrbLocations as Orbs)
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
        """Path to folder containing the ArchipelaGOAL mod executables (gk.exe and goalc.exe).
        Ensure this path contains forward slashes (/) only."""
        description = "ArchipelaGOAL Root Directory"

    root_directory: RootDirectory = RootDirectory("%appdata%/OpenGOAL-Mods/archipelagoal")


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
        "Power Cells": set(cell_item_table.values()),
        "Scout Flies": set(scout_item_table.values()),
        "Specials": set(special_item_table.values()),
        "Moves": set(move_item_table.values()),
        "Precursor Orbs": set(orb_item_table.values()),
    }
    location_name_groups = {
        "Power Cells": set(cell_location_table.values()),
        "Scout Flies": set(scout_location_table.values()),
        "Specials": set(special_location_table.values()),
        "Orb Caches": set(cache_location_table.values()),
        "Precursor Orbs": set(orb_location_table.values()),
        "Trades": {location_table[Cells.to_ap_id(k)] for k in
                   {11, 12, 31, 32, 33, 96, 97, 98, 99, 13, 14, 34, 35, 100, 101}},
    }

    # Functions and Variables that are Options-driven, keep them as instance variables here so that we don't clog up
    # the seed generation routines with options checking. So we set these once, and then just use them as needed.
    can_trade: Callable[[CollectionState, int, Optional[int]], bool]
    orb_bundle_size: int = 0
    orb_bundle_item_name: str = ""

    def generate_early(self) -> None:
        # For the fairness of other players in a multiworld game, enforce some friendly limitations on our options,
        # so we don't cause chaos during seed generation. These friendly limits should **guarantee** a successful gen.
        if self.multiworld.players > 1:
            from .Rules import enforce_multiplayer_limits
            enforce_multiplayer_limits(self.options)

        # Verify that we didn't overload the trade amounts with more orbs than exist in the world.
        # This is easy to do by accident even in a single-player world.
        from .Rules import verify_orb_trade_amounts
        verify_orb_trade_amounts(self.options)

        # Cache the orb bundle size and item name for quicker reference.
        if self.options.enable_orbsanity == EnableOrbsanity.option_per_level:
            self.orb_bundle_size = self.options.level_orbsanity_bundle_size.value
            self.orb_bundle_item_name = orb_item_table[self.orb_bundle_size]
        elif self.options.enable_orbsanity == EnableOrbsanity.option_global:
            self.orb_bundle_size = self.options.global_orbsanity_bundle_size.value
            self.orb_bundle_item_name = orb_item_table[self.orb_bundle_size]

        # Options drive which trade rules to use, so they need to be setup before we create_regions.
        from .Rules import set_orb_trade_rule
        set_orb_trade_rule(self)

    # This will also set Locations, Location access rules, Region access rules, etc.
    def create_regions(self) -> None:
        from .Regions import create_regions
        create_regions(self)

        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "jakanddaxter.puml")

    # Helper function to reuse some nasty if/else trees.
    def item_type_helper(self, item) -> Tuple[int, ItemClassification]:
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
            count = 2000 // self.orb_bundle_size if self.orb_bundle_size > 0 else 0  # Don't divide by zero!

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
                self.multiworld.itempool += [self.create_filler()]
                continue

            # Handle Orbsanity option.
            # If it is OFF, don't add any orb bundles to the item pool, period.
            # If it is ON, don't add any orb bundles that don't match the chosen option.
            if (item_name in self.item_name_groups["Precursor Orbs"]
                and (self.options.enable_orbsanity == EnableOrbsanity.option_off
                     or item_name != self.orb_bundle_item_name)):
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

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change:
            # No matter the option, no matter the item, set the caches to stale.
            state.prog_items[self.player]["Reachable Orbs Fresh"] = False

            # Matching the item name implies Orbsanity is ON, so we don't need to check the option.
            # When Orbsanity is OFF, there won't even be any orb bundle items to collect.
            # Give the player the appropriate number of Tradeable Orbs based on bundle size.
            if item.name == self.orb_bundle_item_name:
                state.prog_items[self.player]["Tradeable Orbs"] += self.orb_bundle_size
        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change:
            # No matter the option, no matter the item, set the caches to stale.
            state.prog_items[self.player]["Reachable Orbs Fresh"] = False

            # The opposite of what we did in collect: Take away from the player
            # the appropriate number of Tradeable Orbs based on bundle size.
            if item.name == self.orb_bundle_item_name:
                state.prog_items[self.player]["Tradeable Orbs"] -= self.orb_bundle_size

            # TODO - 3.8 compatibility, remove this block when no longer required.
            if state.prog_items[self.player]["Tradeable Orbs"] < 1:
                del state.prog_items[self.player]["Tradeable Orbs"]
            if state.prog_items[self.player]["Reachable Orbs"] < 1:
                del state.prog_items[self.player]["Reachable Orbs"]
            for level in level_table:
                if state.prog_items[self.player][f"{level} Reachable Orbs".strip()] < 1:
                    del state.prog_items[self.player][f"{level} Reachable Orbs".strip()]

        return change

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict("enable_move_randomizer",
                                    "enable_orbsanity",
                                    "global_orbsanity_bundle_size",
                                    "level_orbsanity_bundle_size",
                                    "fire_canyon_cell_count",
                                    "mountain_pass_cell_count",
                                    "lava_tube_cell_count",
                                    "citizen_orb_trade_amount",
                                    "oracle_orb_trade_amount",
                                    "jak_completion_condition")
