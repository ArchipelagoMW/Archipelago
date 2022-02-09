# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing

from BaseClasses import Region, RegionType, Entrance, Item, MultiWorld
from Fill import fill_restrictive
from ..AutoWorld import World

from .Items import item_table, MeritousItem
from .Locations import location_table, MeritousLocation
from .Options import meritous_options
from .Rules import set_rules
from .Regions import create_regions

client_version = 1


class MeritousWorld(World):
    """Insert some sort of description here"""

    game: str = "Meritous"
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

    def _create_item_in_quantities(self, name: str, qty: int) -> [Item]:
        return [self.create_item(name) for _ in range(0, qty)]        

    def _make_crystals(self, qty: int) -> MeritousItem:
        crystal_pool = []

        for _ in range(0, qty):
            rand_crystals = self.world.random.randrange(0, 32)
            if rand_crystals < 24:
                crystal_pool += [self.create_item("Crystals x500")]
            elif rand_crystals < 31:
                crystal_pool += [self.create_item("Crystals x1000")]
            else:
                crystal_pool += [self.create_item("Crystals x2000")]
        
        return crystal_pool

    def generate_basic(self):
        frequencies = [0, 25, 23, 22, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 3]
        item_count = 0
        location_count = len(location_table)
        item_pool = []

        self.world.get_location("Place of Power", self.player).place_locked_item(
            self.create_item("Cursed Seal"))
        self.world.get_location("The Last Place You'll Look", self.player).place_locked_item(
            self.create_item("Agate Knife"))

        if not self.world.include_psi_keys[self.player]:
            location_count -= 3
            psi_keys = []
            psi_key_storage = []
            for i in range(0, 3):
                frequencies[i + 12] = 0
                psi_keys += self.create_item(f"PSI Key {i + 1}")
                psi_key_storage += self.world.get_location(
                    f"PSI Key Storage {i + 1}", self.player)

            fill_restrictive(self.world, self.world.get_all_state(
                False), psi_key_storage, psi_keys)

        if not self.world.include_evo_traps[self.player]:
            frequencies[17] = 0
            location_count -= 3
            for boss in ["Meridian", "Ataraxia", "Merodach"]:
                self.world.get_location(boss, self.player).place_locked_item(
                    self.create_item("Evolution Trap"))

        for i, name in enumerate(item_table):
            if (i < len(frequencies)):
                item_pool += self._create_item_in_quantities(name, frequencies[i])
                item_count += frequencies[i]

        if item_count < location_count:
            item_pool += self._make_crystals(location_count - item_count)

    def fill_slot_data(self) -> dict:
        return {
            "goal": self.world.goal[self.player],
            "death_link": self.world.death_link[self.player]
        }
