# Python standard libraries
from collections import defaultdict
from math import ceil
from typing import Any, ClassVar, Callable, Union, cast

# Archipelago imports
import settings
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths
from BaseClasses import (Item,
                         ItemClassification as ItemClass,
                         Tutorial,
                         CollectionState)
from Options import OptionGroup

# Jak imports
from . import options
from .game_id import jak1_id, jak1_name, jak1_max
from .items import (JakAndDaxterItem,
                    OrbAssoc,
                    item_table,
                    cell_item_table,
                    scout_item_table,
                    special_item_table,
                    move_item_table,
                    orb_item_table,
                    trap_item_table)
from .levels import level_table, level_table_with_global
from .locations import (JakAndDaxterLocation,
                        location_table,
                        cell_location_table,
                        scout_location_table,
                        special_location_table,
                        cache_location_table,
                        orb_location_table)
from .regions import create_regions
from .rules import (enforce_mp_absolute_limits,
                    enforce_mp_friendly_limits,
                    enforce_sp_limits,
                    set_orb_trade_rule)
from .locs import (cell_locations as cells,
                   scout_locations as scouts,
                   special_locations as specials,
                   orb_cache_locations as caches,
                   orb_locations as orbs)
from .regs.region_base import JakAndDaxterRegion


def launch_client():
    from . import client
    launch_subprocess(client.launch, name="JakAndDaxterClient")


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
    auto_detect_root_directory: Union[AutoDetectRootDirectory, bool] = True
    enforce_friendly_options: Union[EnforceFriendlyOptions, bool] = True


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
            options.EnableOrbsanity,
            options.GlobalOrbsanityBundleSize,
            options.PerLevelOrbsanityBundleSize,
        ]),
        OptionGroup("Power Cell Counts", [
            options.EnableOrderedCellCounts,
            options.FireCanyonCellCount,
            options.MountainPassCellCount,
            options.LavaTubeCellCount,
        ]),
        OptionGroup("Orb Trade Counts", [
            options.CitizenOrbTradeAmount,
            options.OracleOrbTradeAmount,
        ]),
        OptionGroup("Traps", [
            options.FillerPowerCellsReplacedWithTraps,
            options.FillerOrbBundlesReplacedWithTraps,
            options.TrapEffectDuration,
            options.TrapWeights,
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
    options_dataclass = options.JakAndDaxterOptions
    options: options.JakAndDaxterOptions

    # Web world
    web = JakAndDaxterWebWorld()

    # Stored as {ID: Name} pairs, these must now be swapped to {Name: ID} pairs.
    # Remember, the game ID and various offsets for each item type have already been calculated.
    item_name_to_id = {name: k for k, name in item_table.items()}
    location_name_to_id = {name: k for k, name in location_table.items()}
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
        "Power Cells - GR": set(cells.locGR_cellTable.values()),
        "Power Cells - SV": set(cells.locSV_cellTable.values()),
        "Power Cells - FJ": set(cells.locFJ_cellTable.values()),
        "Power Cells - SB": set(cells.locSB_cellTable.values()),
        "Power Cells - MI": set(cells.locMI_cellTable.values()),
        "Power Cells - FC": set(cells.locFC_cellTable.values()),
        "Power Cells - RV": set(cells.locRV_cellTable.values()),
        "Power Cells - PB": set(cells.locPB_cellTable.values()),
        "Power Cells - LPC": set(cells.locLPC_cellTable.values()),
        "Power Cells - BS": set(cells.locBS_cellTable.values()),
        "Power Cells - MP": set(cells.locMP_cellTable.values()),
        "Power Cells - VC": set(cells.locVC_cellTable.values()),
        "Power Cells - SC": set(cells.locSC_cellTable.values()),
        "Power Cells - SM": set(cells.locSM_cellTable.values()),
        "Power Cells - LT": set(cells.locLT_cellTable.values()),
        "Power Cells - GMC": set(cells.locGMC_cellTable.values()),
        "Scout Flies": set(scout_location_table.values()),
        "Scout Flies - GR": set(scouts.locGR_scoutTable.values()),
        "Scout Flies - SV": set(scouts.locSV_scoutTable.values()),
        "Scout Flies - FJ": set(scouts.locFJ_scoutTable.values()),
        "Scout Flies - SB": set(scouts.locSB_scoutTable.values()),
        "Scout Flies - MI": set(scouts.locMI_scoutTable.values()),
        "Scout Flies - FC": set(scouts.locFC_scoutTable.values()),
        "Scout Flies - RV": set(scouts.locRV_scoutTable.values()),
        "Scout Flies - PB": set(scouts.locPB_scoutTable.values()),
        "Scout Flies - LPC": set(scouts.locLPC_scoutTable.values()),
        "Scout Flies - BS": set(scouts.locBS_scoutTable.values()),
        "Scout Flies - MP": set(scouts.locMP_scoutTable.values()),
        "Scout Flies - VC": set(scouts.locVC_scoutTable.values()),
        "Scout Flies - SC": set(scouts.locSC_scoutTable.values()),
        "Scout Flies - SM": set(scouts.locSM_scoutTable.values()),
        "Scout Flies - LT": set(scouts.locLT_scoutTable.values()),
        "Scout Flies - GMC": set(scouts.locGMC_scoutTable.values()),
        "Specials": set(special_location_table.values()),
        "Orb Caches": set(cache_location_table.values()),
        "Precursor Orbs": set(orb_location_table.values()),
        "Precursor Orbs - GR": set(orbs.locGR_orbBundleTable.values()),
        "Precursor Orbs - SV": set(orbs.locSV_orbBundleTable.values()),
        "Precursor Orbs - FJ": set(orbs.locFJ_orbBundleTable.values()),
        "Precursor Orbs - SB": set(orbs.locSB_orbBundleTable.values()),
        "Precursor Orbs - MI": set(orbs.locMI_orbBundleTable.values()),
        "Precursor Orbs - FC": set(orbs.locFC_orbBundleTable.values()),
        "Precursor Orbs - RV": set(orbs.locRV_orbBundleTable.values()),
        "Precursor Orbs - PB": set(orbs.locPB_orbBundleTable.values()),
        "Precursor Orbs - LPC": set(orbs.locLPC_orbBundleTable.values()),
        "Precursor Orbs - BS": set(orbs.locBS_orbBundleTable.values()),
        "Precursor Orbs - MP": set(orbs.locMP_orbBundleTable.values()),
        "Precursor Orbs - VC": set(orbs.locVC_orbBundleTable.values()),
        "Precursor Orbs - SC": set(orbs.locSC_orbBundleTable.values()),
        "Precursor Orbs - SM": set(orbs.locSM_orbBundleTable.values()),
        "Precursor Orbs - LT": set(orbs.locLT_orbBundleTable.values()),
        "Precursor Orbs - GMC": set(orbs.locGMC_orbBundleTable.values()),
        "Trades": {location_table[cells.to_ap_id(k)] for k in
                   {11, 12, 31, 32, 33, 96, 97, 98, 99, 13, 14, 34, 35, 100, 101}},
        "'Free 7 Scout Flies' Power Cells": set(cells.loc7SF_cellTable.values()),
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
    power_cell_thresholds: list[int]
    power_cell_thresholds_minus_one: list[int]
    trap_weights: tuple[list[str], list[int]]

    # Store these dictionaries for speed improvements.
    level_to_regions: dict[str, list[JakAndDaxterRegion]]  # Contains all levels and regions.
    level_to_orb_regions: dict[str, list[JakAndDaxterRegion]]  # Contains only regions which contain orbs.

    # Handles various options validation, rules enforcement, and caching of important information.
    def generate_early(self) -> None:

        # Initialize the level-region dictionary.
        self.level_to_regions = defaultdict(list)
        self.level_to_orb_regions = defaultdict(list)

        # Cache the power cell threshold values for quicker reference.
        self.power_cell_thresholds = [
            self.options.fire_canyon_cell_count.value,
            self.options.mountain_pass_cell_count.value,
            self.options.lava_tube_cell_count.value,
            100,  # The 100 Power Cell Door.
        ]

        # Order the thresholds ascending and set the options values to the new order.
        if self.options.enable_ordered_cell_counts:
            self.power_cell_thresholds.sort()
            self.options.fire_canyon_cell_count.value = self.power_cell_thresholds[0]
            self.options.mountain_pass_cell_count.value = self.power_cell_thresholds[1]
            self.options.lava_tube_cell_count.value = self.power_cell_thresholds[2]

        # We would have done this earlier, but we needed to sort the power cell thresholds first. Don't worry, we'll
        # come back to them.
        enforce_friendly_options = self.settings.enforce_friendly_options
        if self.multiworld.players == 1:
            # For singleplayer games, always enforce/clamp the cell counts to valid values.
            enforce_sp_limits(self)
        else:
            if enforce_friendly_options:
                # For multiplayer games, we have a host setting to make options fair/sane for other players.
                # If this setting is enabled, enforce/clamp some friendly limitations on our options.
                enforce_mp_friendly_limits(self)
            else:
                # Even if the setting is disabled, some values must be clamped to avoid generation errors.
                enforce_mp_absolute_limits(self)

        # That's right, set the collection of thresholds again. Don't just clamp the values without updating this list!
        self.power_cell_thresholds = [
            self.options.fire_canyon_cell_count.value,
            self.options.mountain_pass_cell_count.value,
            self.options.lava_tube_cell_count.value,
            100,  # The 100 Power Cell Door.
        ]

        # Now that the threshold list is finalized, store this for the remove function.
        self.power_cell_thresholds_minus_one = [x - 1 for x in self.power_cell_thresholds]

        # Calculate the number of power cells needed for full region access, the number being replaced by traps,
        # and the number of remaining filler.
        if self.options.jak_completion_condition == options.CompletionCondition.option_open_100_cell_door:
            self.total_prog_cells = 100
        else:
            self.total_prog_cells = max(self.power_cell_thresholds[:3])
        non_prog_cells = self.total_power_cells - self.total_prog_cells
        self.total_trap_cells = min(self.options.filler_power_cells_replaced_with_traps.value, non_prog_cells)
        self.options.filler_power_cells_replaced_with_traps.value = self.total_trap_cells
        self.total_filler_cells = non_prog_cells - self.total_trap_cells

        # Cache the orb bundle size and item name for quicker reference.
        if self.options.enable_orbsanity == options.EnableOrbsanity.option_per_level:
            self.orb_bundle_size = self.options.level_orbsanity_bundle_size.value
            self.orb_bundle_item_name = orb_item_table[self.orb_bundle_size]
        elif self.options.enable_orbsanity == options.EnableOrbsanity.option_global:
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
            self.options.filler_orb_bundles_replaced_with_traps.value = self.total_trap_orb_bundles
            self.total_filler_orb_bundles = non_prog_orb_bundles - self.total_trap_orb_bundles
        else:
            self.options.filler_orb_bundles_replaced_with_traps.value = 0

        self.trap_weights = self.options.trap_weights.weights_pair

        # Options drive which trade rules to use, so they need to be setup before we create_regions.
        set_orb_trade_rule(self)

    # This will also set Locations, Location access rules, Region access rules, etc.
    def create_regions(self) -> None:
        create_regions(self)

        # Don't forget to add the created regions to the multiworld!
        for level in self.level_to_regions:
            self.multiworld.regions.extend(self.level_to_regions[level])

            # As a lazy measure, let's also fill level_to_orb_regions here.
            # This should help speed up orbsanity calculations.
            self.level_to_orb_regions[level] = [reg for reg in self.level_to_regions[level] if reg.orb_count > 0]

        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "jakanddaxter.puml")

    def item_data_helper(self, item: int) -> list[tuple[int, ItemClass, OrbAssoc, int]]:
        """
        Helper function to reuse some nasty if/else trees. This outputs a list of pairs of item count and class.
        For instance, not all 101 power cells need to be marked progression if you only need 72 to beat the game.
        So we will have 72 Progression Power Cells, and 29 Filler Power Cells.
        """
        data: list[tuple[int, ItemClass, OrbAssoc, int]] = []

        # Make N Power Cells. We only want AP's Progression Fill routine to handle the amount of cells we need
        # to reach the furthest possible region. Even for early completion goals, all areas in the game must be
        # reachable or generation will fail. TODO - Option-driven region creation would be an enormous refactor.
        if item in range(jak1_id, jak1_id + scouts.fly_offset):
            data.append((self.total_prog_cells, ItemClass.progression_skip_balancing, OrbAssoc.IS_POWER_CELL, 0))
            data.append((self.total_filler_cells, ItemClass.filler, OrbAssoc.IS_POWER_CELL, 0))

        # Make 7 Scout Flies per level.
        elif item in range(jak1_id + scouts.fly_offset, jak1_id + specials.special_offset):
            data.append((7, ItemClass.progression_skip_balancing, OrbAssoc.NEVER_UNLOCKS_ORBS, 0))

        # Make only 1 of each Special Item.
        elif item in range(jak1_id + specials.special_offset, jak1_id + caches.orb_cache_offset):
            data.append((1, ItemClass.progression | ItemClass.useful, OrbAssoc.ALWAYS_UNLOCKS_ORBS, 0))

        # Make only 1 of each Move Item.
        elif item in range(jak1_id + caches.orb_cache_offset, jak1_id + orbs.orb_offset):
            data.append((1, ItemClass.progression | ItemClass.useful, OrbAssoc.ALWAYS_UNLOCKS_ORBS, 0))

        # Make N Precursor Orb bundles. Like Power Cells, only a fraction of these will be marked as Progression
        # with the remainder as Filler, but they are still entirely fungible. See collect function for why these
        # are OrbAssoc.NEVER_UNLOCKS_ORBS.
        elif item in range(jak1_id + orbs.orb_offset, jak1_max - max(trap_item_table)):
            data.append((self.total_prog_orb_bundles, ItemClass.progression_skip_balancing,
                         OrbAssoc.NEVER_UNLOCKS_ORBS, self.orb_bundle_size))
            data.append((self.total_filler_orb_bundles, ItemClass.filler,
                         OrbAssoc.NEVER_UNLOCKS_ORBS, self.orb_bundle_size))

        # We will manually create trap items as needed.
        elif item in range(jak1_max - max(trap_item_table), jak1_max):
            data.append((0, ItemClass.trap, OrbAssoc.NEVER_UNLOCKS_ORBS, 0))

        # We will manually create filler items as needed.
        elif item == jak1_max:
            data.append((0, ItemClass.filler, OrbAssoc.NEVER_UNLOCKS_ORBS, 0))

        # If we try to make items with ID's higher than we've defined, something has gone wrong.
        else:
            raise KeyError(f"Tried to fill item pool with unknown ID {item}.")

        return data

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
                    and (self.options.enable_orbsanity == options.EnableOrbsanity.option_off
                         or item_name != self.orb_bundle_item_name)):
                continue

            # Skip Traps for now.
            if item_name in self.item_name_groups["Traps"]:
                continue

            # In almost every other scenario, do this. Not all items with the same name will have the same item class.
            data = self.item_data_helper(item_id)
            for (count, classification, orb_assoc, orb_amount) in data:
                self.multiworld.itempool += [JakAndDaxterItem(item_name, classification, item_id,
                                                              self.player, orb_assoc, orb_amount)
                                             for _ in range(count)]
                items_made += count

        # Handle Traps (for real).
        # Manually fill the item pool with a weighted assortment of trap items, equal to the sum of
        # total_trap_cells + total_trap_orb_bundles. Only do this if one or more traps have weights > 0.
        names, weights = self.trap_weights
        if sum(weights):
            total_traps = self.total_trap_cells + self.total_trap_orb_bundles
            trap_list = self.random.choices(names, weights=weights, k=total_traps)
            self.multiworld.itempool += [self.create_item(trap_name) for trap_name in trap_list]
            items_made += total_traps

        # Handle Unfilled Locations.
        # Add an amount of filler items equal to the number of locations yet to be filled.
        # This is the final set of items we will add to the pool.
        all_regions = self.multiworld.get_regions(self.player)
        total_locations = sum(reg.location_count for reg in cast(list[JakAndDaxterRegion], all_regions))
        total_filler = total_locations - items_made
        self.multiworld.itempool += [self.create_filler() for _ in range(total_filler)]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]

        # Use first tuple (will likely be the most important).
        _, classification, orb_assoc, orb_amount = self.item_data_helper(item_id)[0]
        return JakAndDaxterItem(name, classification, item_id, self.player, orb_assoc, orb_amount)

    def get_filler_item_name(self) -> str:
        return "Green Eco Pill"

    def collect(self, state: CollectionState, item: JakAndDaxterItem) -> bool:
        change = super().collect(state, item)
        if change:
            # Orbsanity as an option is no-factor to these conditions. Matching the item name implies Orbsanity is ON,
            # so we don't need to check the option. When Orbsanity is OFF, there won't even be any orb bundle items
            # to collect.

            # Orb items do not intrinsically unlock anything that contains more Reachable Orbs, so they do not need to
            # set the cache to stale. They just change how many orbs you have to trade with.
            if item.orb_amount > 0:
                state.prog_items[self.player]["Tradeable Orbs"] += self.orb_bundle_size  # Give a bundle of Trade Orbs

            # Power Cells DO unlock new regions that contain more Reachable Orbs - the connector levels and new
            # hub levels - BUT they only do that when you have a number of them equal to one of the threshold values.
            elif (item.orb_assoc == OrbAssoc.ALWAYS_UNLOCKS_ORBS
                  or (item.orb_assoc == OrbAssoc.IS_POWER_CELL
                      and state.count("Power Cell", self.player) in self.power_cell_thresholds)):
                state.prog_items[self.player]["Reachable Orbs Fresh"] = False

            # However, every other item that does not have an appropriate OrbAssoc that changes the CollectionState
            # should NOT set the cache to stale, because they did not make it possible to reach more orb locations
            # (level unlocks, region unlocks, etc.).
        return change

    def remove(self, state: CollectionState, item: JakAndDaxterItem) -> bool:
        change = super().remove(state, item)
        if change:

            # Do the same thing we did in collect, except subtract trade orbs instead of add.
            if item.orb_amount > 0:
                state.prog_items[self.player]["Tradeable Orbs"] -= self.orb_bundle_size  # Take a bundle of Trade Orbs

            # Ditto Power Cells, but check thresholds - 1, because we potentially crossed the threshold in the opposite
            # direction. E.g. we've removed the 20th power cell, our count is now 19, so we should stale the cache.
            elif (item.orb_assoc == OrbAssoc.ALWAYS_UNLOCKS_ORBS
                  or (item.orb_assoc == OrbAssoc.IS_POWER_CELL
                      and state.count("Power Cell", self.player) in self.power_cell_thresholds_minus_one)):
                state.prog_items[self.player]["Reachable Orbs Fresh"] = False

        return change

    def fill_slot_data(self) -> dict[str, Any]:
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
                                            "trap_weights",
                                            "jak_completion_condition",
                                            "require_punch_for_klaww",
                                            )
        return options_dict
