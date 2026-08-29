from collections import defaultdict
import math
import os
from typing import Any, Dict, List, Set

from .ProgressiveDistricts import get_flat_progressive_districts
from worlds.generic.Rules import forbid_item


from .Data import (
    get_boosts_data,
    get_era_required_items_data,
)

from .Rules import create_boost_rules
from .Container import (
    CivVIContainer,
    generate_goody_hut_sql,
    generate_new_items,
    generate_setup_file,
    generate_update_boosts_sql,
)
from .Enum import CivVICheckType, CivVIHintClassification
from .Items import (
    BOOSTSANITY_PROGRESSION_ITEMS,
    FILLER_DISTRIBUTION,
    CivVIEvent,
    CivVIItemData,
    FillerItemRarity,
    format_item_name,
    generate_item_table,
    CivVIItem,
    get_item_by_civ_name,
    get_random_filler_by_rarity,
)
from .Locations import (
    CivVILocation,
    CivVILocationData,
    EraType,
    generate_era_location_table,
    generate_flat_location_table,
)
from .Options import CivVIOptions
from .Regions import create_regions
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess  # type: ignore


def run_client(*args: Any):
    print("Running Civ6 Client")
    from .Civ6Client import main  # lazy import

    launch_subprocess(main, name="Civ6Client")


components.append(
    Component(
        "Civ6 Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apcivvi"),
    )
)


class CivVIWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Civilization VI for MultiWorld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["hesto2"],
        )
    ]
    theme = "ocean"


class CivVIWorld(World):
    """
    Civilization VI is a turn-based strategy video game in which one or more players compete alongside computer-controlled opponents to grow their individual civilization from a small tribe to control the entire planet across several periods of development.
    """

    game = "Civilization VI"
    topology_present = False
    options_dataclass = CivVIOptions
    options: CivVIOptions  # type: ignore

    web = CivVIWeb()

    item_name_to_id = {item.name: item.code for item in generate_item_table().values()}
    location_name_to_id = {
        location.name: location.code
        for location in generate_flat_location_table().values()
    }

    item_table: Dict[str, CivVIItemData] = {}
    location_by_era: Dict[str, Dict[str, CivVILocationData]]
    required_client_version = (0, 4, 5)
    location_table: Dict[str, CivVILocationData]
    era_required_non_progressive_items: Dict[EraType, List[str]]
    era_required_progressive_items_counts: Dict[EraType, Dict[str, int]]
    era_required_progressive_era_counts: Dict[EraType, int]
    item_by_civ_name: Dict[str, str]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.location_by_era = generate_era_location_table()

        self.location_table: Dict[str, CivVILocationData] = {}
        self.item_table = generate_item_table()

        self.era_required_non_progressive_items = {}
        self.era_required_progressive_items_counts = {}
        self.era_required_progressive_era_counts = {}

        for locations in self.location_by_era.values():
            for location in locations.values():
                self.location_table[location.name] = location

    def generate_early(self) -> None:
        flat_progressive_items = get_flat_progressive_districts()

        self.item_by_civ_name = {
            item.civ_name: get_item_by_civ_name(item.civ_name, self.item_table).name
            for item in self.item_table.values()
            if item.civ_name
        }

        previous_era_counts = None
        eras_list = [e.value for e in EraType]
        for era in EraType:
            # Initialize era_required_progressive_era_counts
            era_index = eras_list.index(era.value)
            self.era_required_progressive_era_counts[era] = (
                0
                if era in {EraType.ERA_FUTURE, EraType.ERA_INFORMATION}
                else era_index + 1
            )

            # Initialize era_required_progressive_items_counts
            self.era_required_progressive_items_counts[era] = defaultdict(int)

            if previous_era_counts:
                self.era_required_progressive_items_counts[era].update(
                    previous_era_counts
                )

            # Initialize era_required_non_progressive_items and add to item counts
            self.era_required_non_progressive_items[era] = []

            for item in get_era_required_items_data()[era.value]:
                if (
                    item in flat_progressive_items
                    and self.options.progression_style != "none"
                ):
                    progressive_name = format_item_name(flat_progressive_items[item])
                    self.era_required_progressive_items_counts[era][
                        progressive_name
                    ] += 1
                else:
                    self.era_required_non_progressive_items[era].append(
                        self.item_by_civ_name[item]
                    )

            previous_era_counts = self.era_required_progressive_items_counts[era].copy()

    def get_filler_item_name(self) -> str:
        return get_random_filler_by_rarity(self, FillerItemRarity.COMMON).name

    def create_regions(self) -> None:
        create_regions(self)

    def set_rules(self) -> None:
        if self.options.boostsanity:
            create_boost_rules(self)

    def create_event(self, event: str):
        return CivVIEvent(event, ItemClassification.progression, None, self.player)

    def create_item(self, name: str) -> Item:
        item: CivVIItemData = self.item_table[name]
        classification = item.classification
        if self.options.boostsanity:
            if item.civ_name in BOOSTSANITY_PROGRESSION_ITEMS:
                classification = ItemClassification.progression

        return CivVIItem(item, self.player, classification)

    def create_items(self) -> None:
        data = get_era_required_items_data()
        early_items = data[EraType.ERA_ANCIENT.value]
        early_locations = [
            location
            for location in self.location_table.values()
            if location.era_type == EraType.ERA_ANCIENT.value
        ]
        for item_name, item_data in self.item_table.items():
            # These item types are handled individually
            if item_data.item_type in [
                CivVICheckType.PROGRESSIVE_DISTRICT,
                CivVICheckType.ERA,
                CivVICheckType.GOODY,
            ]:
                continue

            # If we're using progressive districts, we need to check if we need to create a different item instead
            item_to_create = item_name
            item: CivVIItemData = self.item_table[item_name]
            if self.options.progression_style != "none":
                if item.progressive_name:
                    item_to_create = self.item_table[item.progressive_name].name

            self.multiworld.itempool += [self.create_item(item_to_create)]
            if item.civ_name in early_items:
                self.multiworld.early_items[self.player][item_to_create] = 1
            elif self.item_table[item_name].era in [
                EraType.ERA_ATOMIC,
                EraType.ERA_INFORMATION,
                EraType.ERA_FUTURE,
            ]:
                for location in early_locations:
                    found_location = None
                    try:
                        found_location = self.get_location(location.name)
                        forbid_item(found_location, item_to_create, self.player)
                    except KeyError:
                        pass

        # Era items
        if self.options.progression_style == "eras_and_districts":
            # Add one less than the total number of eras (start in ancient, don't need to find it)
            for era in EraType:
                if era.value == "ERA_ANCIENT":
                    continue
                progressive_era_item = self.item_table.get("Progressive Era")
                assert progressive_era_item is not None
                self.multiworld.itempool += [
                    self.create_item(progressive_era_item.name)
                ]

            self.multiworld.early_items[self.player]["Progressive Era"] = 2

        num_filler_items = 0
        # Goody items, create 10 by default if options are enabled
        if self.options.shuffle_goody_hut_rewards:
            num_filler_items += 10

        if self.options.boostsanity:
            num_filler_items += len(get_boosts_data())

        filler_count = {
            rarity: math.ceil(FILLER_DISTRIBUTION[rarity] * num_filler_items)
            for rarity in FillerItemRarity.__reversed__()
        }
        filler_count[FillerItemRarity.COMMON] -= (
            sum(filler_count.values()) - num_filler_items
        )
        self.multiworld.itempool += [
            self.create_item(get_random_filler_by_rarity(self, rarity).name)
            for rarity, count in filler_count.items()
            for _ in range(count)
        ]

    def post_fill(self) -> None:
        if not self.options.pre_hint_items.value:
            return

        def is_hintable_filler_item(item: Item) -> bool:
            return (
                item.classification == 0
                and CivVIHintClassification.FILLER.value
                in self.options.pre_hint_items.value
            )

        start_location_hints: Set[str] = self.options.start_location_hints.value
        non_filler_flags = [
            CivVIHintClassification(flag).to_item_classification()
            for flag in self.options.pre_hint_items.value
            if flag != CivVIHintClassification.FILLER.value
        ]
        for location_name, location_data in self.location_table.items():
            if (
                location_data.location_type != CivVICheckType.CIVIC
                and location_data.location_type != CivVICheckType.TECH
            ):
                continue

            location: CivVILocation = self.get_location(location_name)  # type: ignore

            if location.item and (
                is_hintable_filler_item(location.item)
                or any(
                    flag in location.item.classification for flag in non_filler_flags
                )
            ):
                start_location_hints.add(location_name)

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict(
            "progression_style",
            "death_link",
            "research_cost_multiplier",
            "death_link_effect",
            "death_link_effect_percent",
        )

    def generate_output(self, output_directory: str):
        mod_name = self.multiworld.get_out_file_name_base(self.player)
        mod_dir = os.path.join(output_directory, mod_name)
        mod_files = {
            f"NewItems.xml": generate_new_items(self),
            f"InitOptions.lua": generate_setup_file(self),
            f"GoodyHutOverride.sql": generate_goody_hut_sql(self),
            f"UpdateExistingBoosts.sql": generate_update_boosts_sql(self),
        }
        mod = CivVIContainer(
            mod_files,
            mod_dir,
            output_directory,
            self.player,
            self.multiworld.get_file_safe_player_name(self.player),
        )
        mod.write()
