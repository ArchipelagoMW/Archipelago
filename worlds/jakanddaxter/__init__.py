import typing
from typing import Any, ClassVar, Callable
from math import ceil
import Utils
import settings
from Options import OptionGroup

from BaseClasses import (Item,
                         ItemClassification as ItemClass,
                         Tutorial,
                         CollectionState)
from .GameID import jak1_id, jak1_name, jak1_max
from . import Options
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
                    orb_item_table,
                    trap_item_table)
from .Levels import level_table, level_table_with_global
from .regs.RegionBase import JakAndDaxterRegion
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
                            icon="precursor_orb"))

icon_paths["precursor_orb"] = f"ap:{__name__}/icons/precursor_orb.png"


class JakAndDaxterSettings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """Path to folder containing the ArchipelaGOAL mod executables (gk.exe and goalc.exe).
        Ensure this path contains forward slashes (/) only. This setting only applies if
        Auto Detect Root Directory is set to false."""
        description = "ArchipelaGOAL Root Directory"

    class AutoDetectRootDirectory(settings.Bool):
        """Attempt to find the OpenGOAL installation and the mod executables (gk.exe and goalc.exe)
        automatically. If set to true, the ArchipelaGOAL Root Directory setting is ignored."""
        description = "ArchipelaGOAL Auto Detect Root Directory"

    class EnforceFriendlyOptions(settings.Bool):
        """Enforce friendly player options in both single and multiplayer seeds. Disabling this allows for
        more disruptive and challenging options, but may impact seed generation. Use at your own risk!"""
        description = "ArchipelaGOAL Enforce Friendly Options"

    root_directory: RootDirectory = RootDirectory(
        "%programfiles%/OpenGOAL-Launcher/features/jak1/mods/JakMods/archipelagoal")
    # Don't ever change these type hints again.
    auto_detect_root_directory: typing.Union[AutoDetectRootDirectory, bool] = True
    enforce_friendly_options: typing.Union[EnforceFriendlyOptions, bool] = True


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
    bug_report_page = "https://github.com/ArchipelaGOAL/Archipelago/issues"

    option_groups = [
        OptionGroup("Orbsanity", [
            Options.EnableOrbsanity,
            Options.GlobalOrbsanityBundleSize,
            Options.PerLevelOrbsanityBundleSize,
        ]),
        OptionGroup("Power Cell Counts", [
            Options.EnableOrderedCellCounts,
            Options.FireCanyonCellCount,
            Options.MountainPassCellCount,
            Options.LavaTubeCellCount,
        ]),
        OptionGroup("Orb Trade Counts", [
            Options.CitizenOrbTradeAmount,
            Options.OracleOrbTradeAmount,
        ]),
        OptionGroup("Traps", [
            Options.FillerPowerCellsReplacedWithTraps,
            Options.FillerOrbBundlesReplacedWithTraps,
            Options.TrapEffectDuration,
            Options.ChosenTraps,
        ]),
    ]


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
    required_client_version = (0, 5, 0)

    # Options
    settings: ClassVar[JakAndDaxterSettings]
    options_dataclass = Options.JakAndDaxterOptions
    options: Options.JakAndDaxterOptions

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
        "Traps": set(trap_item_table.values()),
    }
    location_name_groups = {
        "Power Cells": set(cell_location_table.values()),
        "Power Cells - GR": set(Cells.locGR_cellTable.values()),
        "Power Cells - SV": set(Cells.locSV_cellTable.values()),
        "Power Cells - FJ": set(Cells.locFJ_cellTable.values()),
        "Power Cells - SB": set(Cells.locSB_cellTable.values()),
        "Power Cells - MI": set(Cells.locMI_cellTable.values()),
        "Power Cells - FC": set(Cells.locFC_cellTable.values()),
        "Power Cells - RV": set(Cells.locRV_cellTable.values()),
        "Power Cells - PB": set(Cells.locPB_cellTable.values()),
        "Power Cells - LPC": set(Cells.locLPC_cellTable.values()),
        "Power Cells - BS": set(Cells.locBS_cellTable.values()),
        "Power Cells - MP": set(Cells.locMP_cellTable.values()),
        "Power Cells - VC": set(Cells.locVC_cellTable.values()),
        "Power Cells - SC": set(Cells.locSC_cellTable.values()),
        "Power Cells - SM": set(Cells.locSM_cellTable.values()),
        "Power Cells - LT": set(Cells.locLT_cellTable.values()),
        "Power Cells - GMC": set(Cells.locGMC_cellTable.values()),
        "Scout Flies": set(scout_location_table.values()),
        "Scout Flies - GR": set(Scouts.locGR_scoutTable.values()),
        "Scout Flies - SV": set(Scouts.locSV_scoutTable.values()),
        "Scout Flies - FJ": set(Scouts.locFJ_scoutTable.values()),
        "Scout Flies - SB": set(Scouts.locSB_scoutTable.values()),
        "Scout Flies - MI": set(Scouts.locMI_scoutTable.values()),
        "Scout Flies - FC": set(Scouts.locFC_scoutTable.values()),
        "Scout Flies - RV": set(Scouts.locRV_scoutTable.values()),
        "Scout Flies - PB": set(Scouts.locPB_scoutTable.values()),
        "Scout Flies - LPC": set(Scouts.locLPC_scoutTable.values()),
        "Scout Flies - BS": set(Scouts.locBS_scoutTable.values()),
        "Scout Flies - MP": set(Scouts.locMP_scoutTable.values()),
        "Scout Flies - VC": set(Scouts.locVC_scoutTable.values()),
        "Scout Flies - SC": set(Scouts.locSC_scoutTable.values()),
        "Scout Flies - SM": set(Scouts.locSM_scoutTable.values()),
        "Scout Flies - LT": set(Scouts.locLT_scoutTable.values()),
        "Scout Flies - GMC": set(Scouts.locGMC_scoutTable.values()),
        "Specials": set(special_location_table.values()),
        "Orb Caches": set(cache_location_table.values()),
        "Precursor Orbs": set(orb_location_table.values()),
        "Precursor Orbs - GR": set(Orbs.locGR_orbBundleTable.values()),
        "Precursor Orbs - SV": set(Orbs.locSV_orbBundleTable.values()),
        "Precursor Orbs - FJ": set(Orbs.locFJ_orbBundleTable.values()),
        "Precursor Orbs - SB": set(Orbs.locSB_orbBundleTable.values()),
        "Precursor Orbs - MI": set(Orbs.locMI_orbBundleTable.values()),
        "Precursor Orbs - FC": set(Orbs.locFC_orbBundleTable.values()),
        "Precursor Orbs - RV": set(Orbs.locRV_orbBundleTable.values()),
        "Precursor Orbs - PB": set(Orbs.locPB_orbBundleTable.values()),
        "Precursor Orbs - LPC": set(Orbs.locLPC_orbBundleTable.values()),
        "Precursor Orbs - BS": set(Orbs.locBS_orbBundleTable.values()),
        "Precursor Orbs - MP": set(Orbs.locMP_orbBundleTable.values()),
        "Precursor Orbs - VC": set(Orbs.locVC_orbBundleTable.values()),
        "Precursor Orbs - SC": set(Orbs.locSC_orbBundleTable.values()),
        "Precursor Orbs - SM": set(Orbs.locSM_orbBundleTable.values()),
        "Precursor Orbs - LT": set(Orbs.locLT_orbBundleTable.values()),
        "Precursor Orbs - GMC": set(Orbs.locGMC_orbBundleTable.values()),
        "Trades": {location_table[Cells.to_ap_id(k)] for k in
                   {11, 12, 31, 32, 33, 96, 97, 98, 99, 13, 14, 34, 35, 100, 101}},
        "'Free 7 Scout Flies' Power Cells": set(Cells.loc7SF_cellTable.values()),
    }

    # These functions and variables are Options-driven, keep them as instance variables here so that we don't clog up
    # the seed generation routines with options checking. So we set these once, and then just use them as needed.
    can_trade: Callable[[CollectionState, int, int | None], bool]
    total_orbs: int = 2000
    orb_bundle_item_name: str = ""
    orb_bundle_size: int = 0
    total_trade_orbs: int = 0
    total_prog_orb_bundles: int = 0
    total_trap_orb_bundles: int = 0
    total_filler_orb_bundles: int = 0
    total_power_cells: int = 101
    total_prog_cells: int = 0
    total_trap_cells: int = 0
    total_filler_cells: int = 0
    power_cell_thresholds: list[int] = []
    chosen_traps: list[str] = []

    # Handles various options validation, rules enforcement, and caching of important information.
    def generate_early(self) -> None:

        # Cache the power cell threshold values for quicker reference.
        self.power_cell_thresholds = []
        self.power_cell_thresholds.append(self.options.fire_canyon_cell_count.value)
        self.power_cell_thresholds.append(self.options.mountain_pass_cell_count.value)
        self.power_cell_thresholds.append(self.options.lava_tube_cell_count.value)
        self.power_cell_thresholds.append(100)  # The 100 Power Cell Door.

        # Order the thresholds ascending and set the options values to the new order.
        try:
            if self.options.enable_ordered_cell_counts:
                self.power_cell_thresholds.sort()
                self.options.fire_canyon_cell_count.value = self.power_cell_thresholds[0]
                self.options.mountain_pass_cell_count.value = self.power_cell_thresholds[1]
                self.options.lava_tube_cell_count.value = self.power_cell_thresholds[2]
        except IndexError:
            pass  # Skip if not possible.

        # For the fairness of other players in a multiworld game, enforce some friendly limitations on our options,
        # so we don't cause chaos during seed generation. These friendly limits should **guarantee** a successful gen.
        # We would have done this earlier, but we needed to sort the power cell thresholds first.
        enforce_friendly_options = Utils.get_settings()["jakanddaxter_options"]["enforce_friendly_options"]
        if enforce_friendly_options:
            if self.multiworld.players > 1:
                from .Rules import enforce_multiplayer_limits
                enforce_multiplayer_limits(self)
            else:
                from .Rules import enforce_singleplayer_limits
                enforce_singleplayer_limits(self)

        # Calculate the number of power cells needed for full region access, the number being replaced by traps,
        # and the number of remaining filler.
        if self.options.jak_completion_condition == Options.CompletionCondition.option_open_100_cell_door:
            self.total_prog_cells = 100
        else:
            self.total_prog_cells = max(self.power_cell_thresholds[:3])
        non_prog_cells = self.total_power_cells - self.total_prog_cells
        self.total_trap_cells = min(self.options.filler_power_cells_replaced_with_traps.value, non_prog_cells)
        self.total_filler_cells = non_prog_cells - self.total_trap_cells

        # Verify that we didn't overload the trade amounts with more orbs than exist in the world.
        # This is easy to do by accident even in a singleplayer world.
        self.total_trade_orbs = (9 * self.options.citizen_orb_trade_amount) + (6 * self.options.oracle_orb_trade_amount)
        from .Rules import verify_orb_trade_amounts
        verify_orb_trade_amounts(self)

        # Cache the orb bundle size and item name for quicker reference.
        if self.options.enable_orbsanity == Options.EnableOrbsanity.option_per_level:
            self.orb_bundle_size = self.options.level_orbsanity_bundle_size.value
            self.orb_bundle_item_name = orb_item_table[self.orb_bundle_size]
        elif self.options.enable_orbsanity == Options.EnableOrbsanity.option_global:
            self.orb_bundle_size = self.options.global_orbsanity_bundle_size.value
            self.orb_bundle_item_name = orb_item_table[self.orb_bundle_size]
        else:
            self.orb_bundle_size = 0
            self.orb_bundle_item_name = ""

        # Calculate the number of orb bundles needed for trades, the number being replaced by traps,
        # and the number of remaining filler. If Orbsanity is off, default values of 0 will prevail for all.
        if self.orb_bundle_size > 0:
            total_orb_bundles = self.total_orbs // self.orb_bundle_size
            self.total_prog_orb_bundles = ceil(self.total_trade_orbs / self.orb_bundle_size)
            non_prog_orb_bundles = total_orb_bundles - self.total_prog_orb_bundles
            self.total_trap_orb_bundles = min(self.options.filler_orb_bundles_replaced_with_traps.value,
                                              non_prog_orb_bundles)
            self.total_filler_orb_bundles = non_prog_orb_bundles - self.total_trap_orb_bundles

        self.chosen_traps = list(self.options.chosen_traps.value)

        # Options drive which trade rules to use, so they need to be setup before we create_regions.
        from .Rules import set_orb_trade_rule
        set_orb_trade_rule(self)

    # This will also set Locations, Location access rules, Region access rules, etc.
    def create_regions(self) -> None:
        from .Regions import create_regions
        create_regions(self)

        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "jakanddaxter.puml")

    # Helper function to reuse some nasty if/else trees. This outputs a list of pairs of item count and classification.
    # For instance, not all 101 power cells need to be marked progression if you only need 72 to beat the game. So we
    # will have 72 Progression Power Cells, and 29 Filler Power Cells.
    def item_type_helper(self, item: int) -> list[tuple[int, ItemClass]]:
        counts_and_classes: list[tuple[int, ItemClass]] = []

        # Make N Power Cells. We only want AP's Progression Fill routine to handle the amount of cells we need
        # to reach the furthest possible region. Even for early completion goals, all areas in the game must be
        # reachable or generation will fail. TODO - Option-driven region creation would be an enormous refactor.
        if item in range(jak1_id, jak1_id + Scouts.fly_offset):
            counts_and_classes.append((self.total_prog_cells, ItemClass.progression_skip_balancing))
            counts_and_classes.append((self.total_filler_cells, ItemClass.filler))

        # Make 7 Scout Flies per level.
        elif item in range(jak1_id + Scouts.fly_offset, jak1_id + Specials.special_offset):
            counts_and_classes.append((7, ItemClass.progression_skip_balancing))

        # Make only 1 of each Special Item.
        elif item in range(jak1_id + Specials.special_offset, jak1_id + Caches.orb_cache_offset):
            counts_and_classes.append((1, ItemClass.progression | ItemClass.useful))

        # Make only 1 of each Move Item.
        elif item in range(jak1_id + Caches.orb_cache_offset, jak1_id + Orbs.orb_offset):
            counts_and_classes.append((1, ItemClass.progression | ItemClass.useful))

        # Make N Precursor Orb bundles. Like Power Cells, only a fraction of these will be marked as Progression
        # with the remainder as Filler, but they are still entirely fungible.
        elif item in range(jak1_id + Orbs.orb_offset, jak1_max - max(trap_item_table)):
            counts_and_classes.append((self.total_prog_orb_bundles, ItemClass.progression_skip_balancing))
            counts_and_classes.append((self.total_filler_orb_bundles, ItemClass.filler))

        # We will manually create trap items as needed.
        elif item in range(jak1_max - max(trap_item_table), jak1_max):
            counts_and_classes.append((0, ItemClass.trap))

        # We will manually create filler items as needed.
        elif item == jak1_max:
            counts_and_classes.append((0, ItemClass.filler))

        # If we try to make items with ID's higher than we've defined, something has gone wrong.
        else:
            raise KeyError(f"Tried to fill item pool with unknown ID {item}.")

        return counts_and_classes

    def create_items(self) -> None:
        items_made: int = 0
        for item_name in self.item_name_to_id:
            item_id = self.item_name_to_id[item_name]

            # Handle Move Randomizer option.
            # If it is OFF, put all moves in your starting inventory instead of the item pool,
            # then fill the item pool with a corresponding amount of filler items.
            if item_name in self.item_name_groups["Moves"] and not self.options.enable_move_randomizer:
                self.multiworld.push_precollected(self.create_item(item_name))
                self.multiworld.itempool.append(self.create_filler())
                items_made += 1
                continue

            # Handle Orbsanity option.
            # If it is OFF, don't add any orb bundles to the item pool, period.
            # If it is ON, don't add any orb bundles that don't match the chosen option.
            if (item_name in self.item_name_groups["Precursor Orbs"]
                    and (self.options.enable_orbsanity == Options.EnableOrbsanity.option_off
                         or item_name != self.orb_bundle_item_name)):
                continue

            # Skip Traps for now.
            if item_name in self.item_name_groups["Traps"]:
                continue

            # In almost every other scenario, do this. Not all items with the same name will have the same item class.
            counts_and_classes = self.item_type_helper(item_id)
            for (count, classification) in counts_and_classes:
                self.multiworld.itempool += [JakAndDaxterItem(item_name, classification, item_id, self.player)
                                             for _ in range(count)]
                items_made += count

        # Handle Traps (for real).
        # Manually fill the item pool with a random assortment of trap items, equal to the sum of
        # total_trap_cells + total_trap_orb_bundles. Only do this if one or more traps have been selected.
        if len(self.chosen_traps) > 0:
            total_traps = self.total_trap_cells + self.total_trap_orb_bundles
            for _ in range(total_traps):
                trap_name = self.random.choice(self.chosen_traps)
                self.multiworld.itempool.append(self.create_item(trap_name))
            items_made += total_traps

        # Handle Unfilled Locations.
        # Add an amount of filler items equal to the number of locations yet to be filled.
        # This is the final set of items we will add to the pool.
        all_regions = self.multiworld.get_regions(self.player)
        total_locations = sum(reg.location_count for reg in typing.cast(list[JakAndDaxterRegion], all_regions))
        total_filler = total_locations - items_made
        self.multiworld.itempool += [self.create_filler() for _ in range(total_filler)]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        _, classification = self.item_type_helper(item_id)[0]  # Use first tuple (will likely be the most important).
        return JakAndDaxterItem(name, classification, item_id, self.player)

    def get_filler_item_name(self) -> str:
        return "Green Eco Pill"

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change:
            # Orbsanity as an option is no-factor to these conditions. Matching the item name implies Orbsanity is ON,
            # so we don't need to check the option. When Orbsanity is OFF, there won't even be any orb bundle items
            # to collect.

            # Orb items do not intrinsically unlock anything that contains more Reachable Orbs, so they do not need to
            # set the cache to stale. They just change how many orbs you have to trade with.
            if item.name == self.orb_bundle_item_name:
                state.prog_items[self.player]["Tradeable Orbs"] += self.orb_bundle_size  # Give a bundle of Trade Orbs

            # Scout Flies ALSO do not unlock anything that contains more Reachable Orbs, NOR do they give you more
            # tradeable orbs. So let's just pass on them.
            elif item.name in self.item_name_groups["Scout Flies"]:
                pass

            # Power Cells DO unlock new regions that contain more Reachable Orbs - the connector levels and new
            # hub levels - BUT they only do that when you have a number of them equal to one of the threshold values.
            elif (item.name == "Power Cell"
                  and state.count("Power Cell", self.player) not in self.power_cell_thresholds):
                pass

            # However, every other item that changes the CollectionState should set the cache to stale, because they
            # likely made it possible to reach more orb locations (level unlocks, region unlocks, etc.).
            else:
                state.prog_items[self.player]["Reachable Orbs Fresh"] = False
        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change:

            # Do the same thing we did in collect, except subtract trade orbs instead of add.
            if item.name == self.orb_bundle_item_name:
                state.prog_items[self.player]["Tradeable Orbs"] -= self.orb_bundle_size  # Take a bundle of Trade Orbs

            # Ditto Scout Flies.
            elif item.name in self.item_name_groups["Scout Flies"]:
                pass

            # Ditto Power Cells, but check count + 1, because we potentially crossed the threshold in the opposite
            # direction. E.g. we've removed the 20th power cell, our count is now 19, so we should stale the cache.
            elif (item.name == "Power Cell"
                  and state.count("Power Cell", self.player) + 1 not in self.power_cell_thresholds):
                pass

            # Ditto everything else.
            else:
                state.prog_items[self.player]["Reachable Orbs Fresh"] = False
        return change

    def fill_slot_data(self) -> dict[str, Any]:
        slot_dict = {
            "slot_name": self.player_name,
            "slot_seed": self.multiworld.seed_name,
        }
        options_dict = self.options.as_dict("enable_move_randomizer",
                                            "enable_orbsanity",
                                            "global_orbsanity_bundle_size",
                                            "level_orbsanity_bundle_size",
                                            "fire_canyon_cell_count",
                                            "mountain_pass_cell_count",
                                            "lava_tube_cell_count",
                                            "citizen_orb_trade_amount",
                                            "oracle_orb_trade_amount",
                                            "filler_power_cells_replaced_with_traps",
                                            "filler_orb_bundles_replaced_with_traps",
                                            "trap_effect_duration",
                                            "chosen_traps",
                                            "jak_completion_condition",
                                            "require_punch_for_klaww",
                                            )
        return {**slot_dict, **options_dict}
