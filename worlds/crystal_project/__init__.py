import settings
import os
import typing
import threading
import pkgutil

from .Items import item_table, get_item_names_per_category
from .Locations import get_locations
from .Regions import init_areas
from .game_data.static_location_data import location_ids, location_groups
from .Options import CrystalProjectOptions, Toggle

from typing import List, Set, Dict, TextIO
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, ItemClassification

#class CrystalProjectSettings(settings.Group):
    # class RomFile(settings.SNESRomPath):
    #     """Insert help text for host.yaml here."""

    # rom_file: RomFile = RomFile("MyGame.sfc")

class CrystalProjectWorld(World):
    """Insert description of the world/game here."""
    game = "Crystal Project"  # name of the game/world
    options_dataclass = CrystalProjectOptions
    options: CrystalProjectOptions
    #settings: typing.ClassVar[CrystalProjectSettings]  # will be automatically assigned from type hint
    topology_present = False  # show path to required location checks in spoiler

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    location_name_groups = location_groups
    item_name_groups = get_item_names_per_category()
    self.multiworld.push_precollected(self.create_item("Home Point Stone"))

    def create_regions(self) -> None:
        init_areas(self, get_locations("CrystalProjectWorld"))

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())

        self.multiworld.itempool += pool

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add("Warrior Job")
        excluded_items.add("Monk Job")
        excluded_items.add("Rogue Job")
        excluded_items.add("Cleric Job")
        excluded_items.add("Wizard Job")

        if(!self.options.randomizeJobs) {
            excluded_items.add("Warlock Job")
            excluded_items.add("Fencer Job")
            excluded_items.add("Shaman Job")
            excluded_items.add("Scholar Job")
            excluded_items.add("Aegis Job")
            excluded_items.add("Hunter Job")
            excluded_items.add("Chemist Job")
            excluded_items.add("Reaper Job")
            excluded_items.add("Ninja Job")
            excluded_items.add("Nomad Job")
            excluded_items.add("Dervish Job")
            excluded_items.add("Beatsmith Job")
            excluded_items.add("Samurai Job")
            excluded_items.add("Assassin Job")
            excluded_items.add("Valkyrie Job")
            excluded_items.add("Summoner Job")
            excluded_items.add("Beastmaster Job")
            excluded_items.add("Weaver Job")
            excluded_items.add("Mimic Job")
        }

        return excluded_items

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        return pool

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)

        return item