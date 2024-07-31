import math
import os
import random
from typing import Dict
import typing

from .Data import get_boosts_data

from .Rules import create_boost_rules
import Utils
from .Container import CivVIContainer, generate_goody_hut_sql, generate_new_items, generate_setup_file, generate_update_boosts_sql
from .Enum import CivVICheckType
from .Items import BOOSTSANITY_PROGRESSION_ITEMS, FILLER_DISTRIBUTION, CivVIItemData, FillerItemRarity, generate_item_table, CivVIItem, get_random_filler_by_rarity
from .Locations import CivVILocation, CivVILocationData, EraType, generate_era_location_table, generate_flat_location_table
from .Options import CivVIOptions
from .Regions import create_regions
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess


def run_client():
    print("Running Civ6 Client")
    from .Civ6Client import main  # lazy import
    launch_subprocess(main, name="Civ6Client")


components.append(
    Component("Civ6 Client", func=run_client, component_type=Type.CLIENT,
              file_identifier=SuffixIdentifier(".apcivvi"))
)


class CivVIWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Civlization VI for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["hesto2"]
    )]


class CivVIWorld(World):
    """
    Civilization VI is a turn-based strategy video game in which one or more players compete alongside computer-controlled AI opponents to grow their individual civilization from a small tribe to control the entire planet across several periods of development.
    """

    game: str = "Civilization VI"
    topology_present = False
    options_dataclass = CivVIOptions
    options: CivVIOptions

    web = CivVIWeb()

    item_name_to_id = {
        item.name: item.code for item in generate_item_table().values()}
    location_name_to_id = {
        location.name: location.code for location in generate_flat_location_table().values()}

    item_table: Dict[str, CivVIItemData] = {}
    location_by_era: Dict[EraType, Dict[str, CivVILocationData]]

    data_version = 1
    required_client_version = (0, 4, 5)

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.location_by_era = generate_era_location_table()

        self.location_table: Dict[str, CivVILocationData] = {}
        self.item_table = generate_item_table()

        for _era, locations in self.location_by_era.items():
            for _item_name, location in locations.items():
                self.location_table[location.name] = location

    def get_filler_item_name(self):
        return get_random_filler_by_rarity(FillerItemRarity.COMMON, self.item_table).name

    def create_regions(self):
        create_regions(self, self.options, self.player)

    def set_rules(self) -> None:
        if self.options.boostsanity.value:
            create_boost_rules(self)

    def create_item(self, name: str) -> Item:
        item: CivVIItemData = self.item_table[name]
        classification = item.classification
        if self.options.boostsanity.value:
            if item.civ_name in BOOSTSANITY_PROGRESSION_ITEMS:
                classification = ItemClassification.progression

        return CivVIItem(item, self.player, classification)

    def create_items(self):
        progressive_era_item = None
        for item_name, data in self.item_table.items():
            # Don't add progressive items to the itempool here
            if data.item_type == CivVICheckType.PROGRESSIVE_DISTRICT:
                continue
            if data.item_type == CivVICheckType.ERA:
                # Don't add era items in this way
                progressive_era_item = data
                continue
            if data.item_type == CivVICheckType.GOODY:
                continue

                # If we're using progressive districts, we need to check if we need to create a different item instead
            item_to_create = item_name
            if self.options.progression_style.current_key != "none":
                item: CivVIItemData = self.item_table[item_name]
                if item.progression_name != None:
                    item_to_create = self.item_table[item.progression_name].name

            self.multiworld.itempool += [self.create_item(
                item_to_create)]

        # Era items
        if self.options.progression_style.current_key == "eras_and_districts":
            # Add one less than the total number of eras (start in ancient, don't need to find it)
            for era in EraType:
                if era.value == "ERA_ANCIENT":
                    continue
                self.multiworld.itempool += [self.create_item(
                    progressive_era_item.name)]

        num_filler_items = 0
        # Goody items, create 10 by default if options are enabled
        if self.options.shuffle_goody_hut_rewards.value:
            num_filler_items += 10

        if self.options.boostsanity.value:
            boost_data = get_boosts_data()
            num_filler_items += len(boost_data)

        filler_count = {rarity: FILLER_DISTRIBUTION[rarity] * num_filler_items for rarity in FillerItemRarity.__reversed__()}
        min_count = 1
        # Add filler items by rarity
        total_created = 0
        for rarity, count in filler_count.items():
            for _ in range(max(min_count, math.ceil(count))):
                if total_created >= num_filler_items:
                    break
                self.multiworld.itempool += [self.create_item(
                    get_random_filler_by_rarity(rarity, self.item_table).name)]
                total_created += 1

    def post_fill(self):
        if self.options.pre_hint_items.current_key == "none":
            return

        show_flags = {
            ItemClassification.progression: self.options.pre_hint_items.current_key != "none",
            ItemClassification.useful: self.options.pre_hint_items.current_key == "no_junk" or self.options.pre_hint_items.current_key == "all",
            ItemClassification.filler: self.options.pre_hint_items.current_key == "all",
        }

        start_location_hints: typing.Set[str] = self.options.start_location_hints.value
        for location_name, location_data in self.location_table.items():
            if location_data.location_type != CivVICheckType.CIVIC and location_data.location_type != CivVICheckType.TECH:
                continue

            location: CivVILocation = self.multiworld.get_location(location_name, self.player)

            if not location.item or not show_flags.get(location.item.classification, False):
                continue

            start_location_hints.add(location_name)

    def fill_slot_data(self):
        return {
            "progression_style": self.options.progression_style.current_key,
            "death_link": self.options.death_link.value,
            "research_cost_multiplier": self.options.research_cost_multiplier.value,
            "death_link_effect": self.options.death_link_effect.value,
            "death_link_effect_percent": self.options.death_link_effect_percent.value,

        }

    def generate_output(self, output_directory: str):
        mod_name = f"AP-{self.multiworld.get_file_safe_player_name(self.player)}"
        mod_dir = os.path.join(
            output_directory, mod_name + "_" + Utils.__version__)
        mod_files = {
            f"NewItems.xml": generate_new_items(self),
            f"InitOptions.lua": generate_setup_file(self),
            f"GoodyHutOverride.sql": generate_goody_hut_sql(self),
            f"UpdateExistingBoosts.sql": generate_update_boosts_sql(self),
        }
        mod = CivVIContainer(mod_files, mod_dir, output_directory, self.player,
                             self.multiworld.get_file_safe_player_name(self.player))
        mod.write()
