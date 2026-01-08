# pylint: disable=missing-class-docstring, missing-module-docstring, fixme
from copy import deepcopy
from typing import List

from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.celeste.data import (
    BaseData,
    CelesteItem,
    CelesteItemType,
    CelesteLevel,
    CelesteLocation,
    CelesteSide,
)
from worlds.celeste.progression import BaseProgression, DefaultProgression

from .options import (
    ProgressionSystemEnum,
    VictoryConditionEnum,
    celeste_options,
    get_option_value,
)


class CelesteWebWorld(WebWorld):
    theme = "ice"
    tutorials = [
        Tutorial(
            "Multiworld Setup Tutorial",
            "A guide to setting up the Celeste randomiser connected to an Archipelago MultiWorld.",
            "English",
            "celeste_en.md",
            "celeste/en",
            ["doshyw"],
        )
    ]


class CelesteWorld(World):
    """
    Help Madeline survive her inner demons on her journey to the top of Celeste Mountain, in this super-tight,
    hand-crafted platformer from the creators of multiplayer classic TowerFall.
    """

    game = "Celeste"
    option_definitions = celeste_options
    topology_present = True
    web = CelesteWebWorld()

    item_name_to_id = BaseData.item_name_to_id()
    location_name_to_id = BaseData.location_name_to_id()

    progression_system: BaseProgression

    required_client_version = (0, 4, 3)

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.progression_system = None

    def generate_early(self) -> None:
        options = {x: get_option_value(self.multiworld, self.player, x) for x in celeste_options}

        if options["progression_system"] == ProgressionSystemEnum.DEFAULT_PROGRESSION.value:
            self.progression_system = DefaultProgression(options)

    def create_item(self, name: str) -> CelesteItem:
        uuid = self.item_name_to_id[name]

        if self.progression_system is not None:
            item_dict = self.progression_system.items_dict(self.player, self.multiworld)
            if uuid in item_dict:
                return item_dict[uuid].copy()

        raw_item = BaseData.get_item(uuid)
        return CelesteItem(
            raw_item[3], ItemClassification.filler, uuid, self.player, raw_item[0], raw_item[1], raw_item[2]
        )

    def create_regions(self):
        regions = self.progression_system.regions(self.player, self.multiworld)
        self.multiworld.regions.extend(regions)

    def create_items(self):
        item_table = self.progression_system.items(self.player, self.multiworld)

        for item in item_table:
            if item.name != self.progression_system.victory_item_name():
                self.multiworld.itempool.append(item.copy())

        self.item_name_groups = {
            "cassettes": [item.name for item in item_table if item.item_type == CelesteItemType.CASSETTE],
            "levels": [item.name for item in item_table if item.item_type == CelesteItemType.COMPLETION],
            "hearts": [item.name for item in item_table if item.item_type == CelesteItemType.GEMHEART],
        }

    def generate_basic(self) -> None:
        victory_name = self.progression_system.victory_item_name()
        self.multiworld.get_location(victory_name, self.player).place_locked_item(self.create_item(victory_name))
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            self.progression_system.victory_item_name(), self.player
        )

    def fill_slot_data(self):
        slot_data = {}
        for option_name in celeste_options:
            current_option = self.progression_system.get_option(option_name)
            initial_option = get_option_value(self.multiworld, self.player, option_name)
            if current_option != initial_option:
                print(
                    f"[WARNING] [CELESTE] Invalid options value {option_name} = {initial_option}.",
                    f"Overridden as {current_option}.",
                )
                getattr(self.options, option_name).value = current_option
            slot_data[option_name] = current_option

        return slot_data
