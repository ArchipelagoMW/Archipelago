# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
import random

from .Items import item_table, MeritousItem
from .Locations import location_table, MeritousLocation
from .Options import meritous_options
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Region, RegionType, Entrance, Item, MultiWorld
from ..AutoWorld import World

client_version = 1


class MeritousWorld(World):
    """Insert some sort of description here"""

    game: str = "Mertious"
    topology_present: False

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 1
    forced_auto_forfeit = False

    options = meritous_options

    def create_regions(self):
        create_regions(self.world, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_item(self, name: str) -> Item:
        return MeritousItem(name, True, item_table[name], self.player)

    def _make_crystals(self) -> MeritousItem:
        rand_crystals = random.randrange(0, 32)
        if rand_crystals < 24:
            return self.create_item("Crystals x500")
        elif rand_crystals < 31:
            return self.create_item("Crystals x1000")
        else:
            return self.create_item("Crystals x2000")

    def generate_basic(self):
        frequencies = [0, 25, 23, 22, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]
        item_count = 0
        location_count = len(location_table)
        item_pool = []

        for i, name in enumerate(item_table):
            if (i < len(frequencies)):
                item_pool += self.create_item(name) * frequencies[i]
                item_count += frequencies[i]

        while item_count < location_count:
            item_pool += self._make_crystals()
            item_count += 1

    def fill_slot_data(self) -> dict:
        return {
            "goal": self.world.goal[self.player],
            "death_link": self.world.death_link[self.player]
        }
