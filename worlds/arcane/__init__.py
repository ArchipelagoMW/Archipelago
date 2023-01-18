import os
import typing
# import math
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import ArcaneItem, ItemData, item_table, junk_table
from .Locations import ArcaneLocation, all_locations, setup_locations
from .Options import arcane_options
from .Regions import create_regions, connect_regions
from .Rules import set_rules
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World
# import math


class ArcaneWeb(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Arcane: Online Mystery Serial randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Liquid Cat"]
    )

    tutorials = "Insert setup webpage here"


class ArcaneWorld(World):
    """
    Arcane is an episodic Flash-based point-and-click series of web games. Guide
    detectives Prescott, Ophelia, and Gregor on their expeditions around the Miller villa and
    England as they attempt to thwart the plans of the sinister Elder Star to return the
    Great Old Ones to Earth. But be careful not to click too needlessly, or bad things may happen...
    """
    game: str = "Arcane Online Mystery Serial"
    option_definitions = arcane_options
    topology_present = False
    data_version = 0
    # hint_blacklist = {}
    web = ArcaneWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    episode_ending_list = []
    total_required_episodes = 1

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def _get_slot_data(self):
        return {
            "death_link": self.multiworld.death_link[self.player].value,
        }

    def generate_early(self):
        if self.multiworld.episodes_to_clear[self.player].value == 0:
            self.episode_ending_list = [LocationName.s1e4_end]
        elif self.multiworld.episodes_to_clear[self.player].value == 1:
            self.episode_ending_list = [LocationName.s2e8_end]
        elif self.multiworld.episodes_to_clear[self.player].value == 2:
            self.episode_ending_list = [LocationName.s1e4_end, LocationName.s2e8_end]
            self.total_required_episodes = 2
        elif self.multiworld.episodes_to_clear[self.player].value == 3:
            self.episode_ending_list = [LocationName.s1e1_end, LocationName.s1e2_end, LocationName.s1e3_end, LocationName.s1e4_end]
            self.total_required_episodes = 4
        elif self.multiworld.episodes_to_clear[self.player].value == 4:
            self.episode_ending_list = [LocationName.s2e1_end, LocationName.s2e2_end, LocationName.s2e3_end, LocationName.s2e4_end,
                                        LocationName.s2e5_end, LocationName.s2e6_end, LocationName.s2e7_end, LocationName.s2e8_end]
            self.total_required_episodes = 8
        else:
            self.episode_ending_list = [LocationName.s1e1_end, LocationName.s1e2_end, LocationName.s1e3_end, LocationName.s1e4_end,
                                        LocationName.s2e1_end, LocationName.s2e2_end, LocationName.s2e3_end, LocationName.s2e4_end,
                                        LocationName.s2e5_end, LocationName.s2e6_end, LocationName.s2e7_end, LocationName.s2e8_end]
            self.total_required_episodes = self.multiworld.number_to_clear[self.player].value

    def create_regions(self):
        location_table = setup_locations()
        create_regions(self.multiworld, self.player, location_table, self.episode_ending_list)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        created_item = []

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = ArcaneItem(name, classification, data.code, self.player)

        return created_item

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.total_required_episodes)

    def generate_basic(self):
        itempool: typing.List[ArcaneItem] = []

        total_required_locations = 86

        for i in range(len(self.episode_ending_list)):
            self.multiworld.get_location(self.episode_ending_list[i], self.player).place_locked_item(self.create_item(ItemName.clear))

        for item in item_table:
            if item_table[item].code is not None:
                itempool += [self.create_item(item) for _ in range(item_table[item].quantity)]

        total_junk_count = total_required_locations - len(itempool)

        junk_pool = []
        for item_name in self.multiworld.random.choices(list(junk_table.keys()), k=total_junk_count):
            junk_pool.append(self.create_item(item_name))

        itempool += junk_pool

        connect_regions(self.multiworld, self.player)

        self.multiworld.itempool += itempool

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in arcane_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data
