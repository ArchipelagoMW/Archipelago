"""
Initialization module for The Legend of Zelda - The Minish Cap.
Handles the Web page for yaml generation, saving rom file and high-level generation.
"""

import logging
import os
import pkgutil
from typing import ClassVar, TextIO

import settings
from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from Fill import FillError
from Options import OptionError
from .client import MinishCapClient
from .constants import MinishCapEvent, MinishCapItem, MinishCapLocation, TMCEvent, TMCItem, TMCLocation, TMCRegion
from .dungeons import fill_dungeons
from .items import (get_filler_item_selection, get_item_pool, get_pre_fill_pool, item_frequencies, item_groups,
                    item_table, ItemData)
from .locations import (all_locations, DEFAULT_SET, GOAL_PED, GOAL_VAATI, location_groups, OBSCURE_SET, POOL_DIG,
                        POOL_ENEMY, POOL_POT, POOL_RUPEE, POOL_WATER)
from .options import (DHCAccess, DungeonItem, get_option_data, Goal, MinishCapOptions, NonElementDungeons,
                      OPTION_GROUPS, ShuffleElements, SLOT_DATA_OPTIONS)
from .regions import create_regions
from .rom import MinishCapProcedurePatch, write_tokens
from .rules import MinishCapRules

tmc_logger = logging.getLogger("The Minish Cap")


class MinishCapWebWorld(WebWorld):
    """ Minish Cap Webpage configuration """

    theme = "grassFlowers"
    bug_report_page = "https://github.com/eternalcode0/Archipelago/issues"
    option_groups = OPTION_GROUPS
    tutorials = [
        Tutorial(tutorial_name="Setup Guide",
                 description="A guide to setting up The Legend of Zelda: The Minish Cap for Archipelago.",
                 language="English",
                 file_name="setup_en.md",
                 link="setup/en",
                 authors=["eternalcode"]),
        Tutorial(tutorial_name="Setup Guide",
                 description="A guide to setting up The Legend of Zelda: The Minish Cap for Archipelago.",
                 language="Français",
                 file_name="setup_fr.md",
                 link="setup/fr",
                 authors=["Deoxis9001"])
    ]


class MinishCapSettings(settings.Group):
    """ Settings for the launcher """

    class RomFile(settings.UserFilePath):
        """File name of the Minish Cap EU rom"""

        copy_to = "Legend of Zelda, The - The Minish Cap (Europe).gba"
        description = "Minish Cap ROM File"
        md5s = ["2af78edbe244b5de44471368ae2b6f0b"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class MinishCapWorld(World):
    """ Randomizer methods/data for generation """

    game = "The Minish Cap"
    web = MinishCapWebWorld()
    options_dataclass = MinishCapOptions
    options: MinishCapOptions
    settings: ClassVar[MinishCapSettings]
    item_name_to_id = {name: data.item_id for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    item_name_groups = item_groups
    item_pool = []
    pre_fill_pool = []
    location_name_groups = location_groups
    filler_items = []
    disabled_locations: set[str]
    disabled_dungeons: set[str]

    # region APWorld Generation
    # sorted in execution order

    def generate_early(self) -> None:
        enabled_pools = set(DEFAULT_SET)
        if self.options.rupeesanity.value:
            enabled_pools.add(POOL_RUPEE)
        if self.options.shuffle_pots.value:
            enabled_pools.add(POOL_POT)
        if self.options.shuffle_digging.value:
            enabled_pools.add(POOL_DIG)
        if self.options.shuffle_underwater.value:
            enabled_pools.add(POOL_WATER)
        if self.options.shuffle_gold_enemies.value:
            enabled_pools.add(POOL_ENEMY)

        enabled_pools.update([f"cucco:{round_num}" for round_num in range(
            10, 10 - self.options.cucco_rounds.value, -1)])
        enabled_pools.update([f"goron:{round_num}" for round_num in range(1, self.options.goron_sets.value + 1)])

        # Default dhc_access to closed when it's been set to ped with goal vaati disabled.
        # There's too many flags to manage to allow DHC to open after ped completes and vaati is slain.
        if self.options.goal.value == Goal.option_pedestal and self.options.dhc_access.value == DHCAccess.option_pedestal:
            self.options.dhc_access.value = DHCAccess.option_closed

        self.filler_items = get_filler_item_selection(self)

        if self.options.shuffle_elements.value == ShuffleElements.option_dungeon_prize:
            self.options.start_hints.value.add(TMCItem.EARTH_ELEMENT)
            self.options.start_hints.value.add(TMCItem.FIRE_ELEMENT)
            self.options.start_hints.value.add(TMCItem.WATER_ELEMENT)
            self.options.start_hints.value.add(TMCItem.WIND_ELEMENT)

        self.disabled_locations = set(loc.name for loc in all_locations if not loc.pools.issubset(enabled_pools))

        if self.options.dhc_access.value == DHCAccess.option_closed:
            self.disabled_locations.update(loc for loc in location_groups["DHC"])

        # Check if the settings require more dungeons than are included
        self.disabled_dungeons = set(dungeon for dungeon in ["DWS", "CoF", "FoW", "ToD", "RC", "PoW"]
                                     if location_groups[dungeon].issubset(self.options.exclude_locations.value))

        if self.options.ped_dungeons > 6 - len(self.disabled_dungeons):
            error_message = "Slot '%s' has required %d/6 dungeons to goal but found %d excluded. "
            raise OptionError(error_message % (
                self.player_name,
                self.options.ped_dungeons,
                len(self.disabled_dungeons)))

    # push start_inventory and start_inventory_from_pool into precollected_items

    def create_regions(self) -> None:
        create_regions(self, self.disabled_locations, self.disabled_dungeons)

        loc = GOAL_VAATI if self.options.goal.value == Goal.option_vaati else GOAL_PED
        goal_region = self.get_region(loc.region)
        goal_item = MinishCapItem("Victory", ItemClassification.progression, None, self.player)
        goal_location = MinishCapLocation(self.player, loc.name, None, goal_region)
        goal_location.place_locked_item(goal_item)
        goal_region.locations.append(goal_location)
        if self.options.goal.value == Goal.option_vaati:
            reg = self.get_region(TMCRegion.STAINED_GLASS)
            ped = MinishCapLocation(self.player, TMCEvent.CLEAR_PED, None, reg)
            ped.place_locked_item(self.create_event(TMCEvent.CLEAR_PED))
            reg.locations.append(ped)

    # All non-event locations finalized

    def create_items(self):
        # Force vanilla elements into their pre-determined locations (must happen before pre_fill for plando)
        if self.options.shuffle_elements.value is ShuffleElements.option_vanilla:
            # Place elements into ordered locations, don't shuffle
            location_names = [TMCLocation.DEEPWOOD_PRIZE, TMCLocation.COF_PRIZE, TMCLocation.DROPLETS_PRIZE,
                              TMCLocation.PALACE_PRIZE]
            item_names = [TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT]
            for location_name, item_name in zip(location_names, item_names):
                loc = self.get_location(location_name)
                if loc.item is not None:
                    raise FillError(f"Slot '{self.player_name}' used 'shuffle_elements: vanilla' but location "
                                    f"'{location_name}' was already filled with '{loc.item.name}'")
                loc.place_locked_item(self.create_item(item_name))
        elif self.options.shuffle_elements.value is ShuffleElements.option_dungeon_prize:
            # Get unfilled prize locations, shuffle, and place each element
            location_names = [TMCLocation.DEEPWOOD_PRIZE, TMCLocation.COF_PRIZE, TMCLocation.FORTRESS_PRIZE,
                              TMCLocation.DROPLETS_PRIZE, TMCLocation.PALACE_PRIZE, TMCLocation.CRYPT_PRIZE]
            locations = list(self.multiworld.get_unfilled_locations_for_players(location_names, [self.player]))
            if len(locations) < 4:
                raise FillError(f"Slot '{self.player_name}' used 'shuffle_elements: dungeon_prize' but only "
                                f"{len(locations)}/6 prize locations are available to fill the 4 elements")
            element_locations = self.random.sample(locations, k=4)
            item_names = [TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT]
            for location, item_name in zip(element_locations, item_names):
                location.place_locked_item(self.create_item(item_name))
        if self.options.non_element_dungeons.value == NonElementDungeons.option_excluded and \
                self.options.shuffle_elements.on_prize and \
                self.options.ped_dungeons.value <= 4:
            locations = list(loc.name for loc in self.multiworld.get_unfilled_locations_for_players(
                location_names, [self.player]))
            prize_name_to_region = {
                TMCLocation.DEEPWOOD_PRIZE: "DWS",
                TMCLocation.COF_PRIZE: "CoF",
                TMCLocation.FORTRESS_PRIZE: "FoW",
                TMCLocation.DROPLETS_PRIZE: "ToD",
                TMCLocation.PALACE_PRIZE: "PoW",
                TMCLocation.CRYPT_PRIZE: "RC"}
            self.options.exclude_locations.value.update(
                region_locations
                for prize_name in locations
                for region_locations in location_groups[prize_name_to_region[prize_name]])

        # Add in all progression and useful items
        self.item_pool = get_item_pool(self)
        self.pre_fill_pool = get_pre_fill_pool(self)
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        self.multiworld.itempool.extend(self.item_pool)
        filler = [self.create_filler() for _ in range(total_locations - len(self.item_pool) - len(self.pre_fill_pool))]
        self.multiworld.itempool.extend(filler)

    # local_items overrides non_local_items

    def set_rules(self) -> None:
        MinishCapRules(self).set_rules(self.disabled_locations, self.location_name_to_id)

    def connect_entrances(self) -> None:
        pass
        # if options.randomize_entrances.value:
        #     self.rule_builder.randomize_entrances()

        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_world.puml",
        #                   regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
        #                  self.player])

    # All rules finalized
    # location progress type assigned, excluded overrides priority
    # locality for local_items and non_local_item set

    def generate_basic(self) -> None:
        pass

    # remove start_inventory_from_pool from the pool
    # process item_links
    # item plando is processed

    def pre_fill(self) -> None:
        fill_dungeons(self)

    # finalize item pool
    # perform standard fill

    def post_fill(self):
        pass

    # finalize randomization, no more calls to self.random
    # process progression balancing
    # perform accessibility check

    def generate_output(self, output_directory: str) -> None:
        patch = MinishCapProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff"))
        write_tokens(self, patch)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}" f"{patch.patch_file_ending}"))

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        pass

    def fill_slot_data(self) -> dict[str, any]:
        data = {"DeathLink": self.options.death_link.value, "DeathLinkGameover": self.options.death_link_gameover.value,
                "RupeeSpot": self.options.rupeesanity.value,
                "GoalVaati": int(self.options.goal.value == Goal.option_vaati)}

        data |= self.options.as_dict(*SLOT_DATA_OPTIONS, casing="snake")
        data |= get_option_data(self.options)

        # Setup prize location data for tracker to show element hints
        prizes = {TMCLocation.COF_PRIZE: "prize_cof", TMCLocation.CRYPT_PRIZE: "prize_rc",
                  TMCLocation.PALACE_PRIZE: "prize_pow", TMCLocation.DEEPWOOD_PRIZE: "prize_dws",
                  TMCLocation.DROPLETS_PRIZE: "prize_tod", TMCLocation.FORTRESS_PRIZE: "prize_fow"}
        if self.options.shuffle_elements.value in {ShuffleElements.option_dungeon_prize,
                                                   ShuffleElements.option_vanilla}:
            for loc_name, data_name in prizes.items():
                placed_item = self.get_location(loc_name).item.name
                if placed_item in self.item_name_groups["Elements"]:
                    data[data_name] = item_table[placed_item].byte_ids[0]
                else:
                    data[data_name] = 0
        else:
            for slot_key in prizes.values():
                data[slot_key] = 0

        return data

    # playthrough is calculated

    def write_spoiler_header(self, spoiler_handle: TextIO):
        pass

    def write_spoiler(self, spoiler_handle: TextIO):
        pass

    def write_spoiler_end(self, spoiler_handle: TextIO):
        pass

    # output zip
    # endregion

    def create_item(self, name: str) -> MinishCapItem:
        item = item_table[name]
        return MinishCapItem(name, item.classification, self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> MinishCapEvent:
        return MinishCapEvent(name, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        if len(self.filler_items) == 0:
            self.filler_items = get_filler_item_selection(self)
        return self.random.choice(self.filler_items)

    def get_pre_fill_items(self) -> list[Item]:
        return self.pre_fill_pool
