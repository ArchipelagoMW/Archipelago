import settings
import os
import typing
import threading
import pkgutil

from .Items import item_table, filler_items, get_item_names_per_category
from .Locations import get_locations
from .Regions import init_areas
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
    location_name_to_id = {location.name: location.code for location in get_locations()}
    item_name_groups = get_item_names_per_category()

    def generate_early(self):
        self.multiworld.push_precollected(self.create_item("Item - Home Point Stone"))

    def create_regions(self) -> None:
        init_areas(self, get_locations())

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())

        self.multiworld.itempool += pool

    def get_filler_item_name(self) -> str:
        #traps go here if we have any
        # trap_chance: int = self.options.trap_chance.value
        # enabled_traps: List[str] = self.options.traps.value

        # if self.random.random() < (trap_chance / 100) and enabled_traps:
        #     return self.random.choice(enabled_traps)
        # else:
        #     return self.random.choice(filler_items) 
        return self.random.choice(filler_items)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add("Job - Warrior")
        excluded_items.add("Job - Monk")
        excluded_items.add("Job - Rogue")
        excluded_items.add("Job - Cleric")
        excluded_items.add("Job - Wizard")
        excluded_items.add("Job - Warlock")

        if self.options.randomizeJobs != 1:
            excluded_items.add("Job - Fencer")
            excluded_items.add("Job - Shaman")
            excluded_items.add("Job - Scholar")
            excluded_items.add("Job - Aegis")
            excluded_items.add("Job - Hunter")
            excluded_items.add("Job - Chemist")
            excluded_items.add("Job - Reaper")
            excluded_items.add("Job - Ninja")
            excluded_items.add("Job - Nomad")
            excluded_items.add("Job - Dervish")
            excluded_items.add("Job - Beatsmith")
            excluded_items.add("Job - Samurai")
            excluded_items.add("Job - Assassin")
            excluded_items.add("Job - Valkyrie")
            excluded_items.add("Job - Summoner")
            excluded_items.add("Job - Beastmaster")
            excluded_items.add("Job - Weaver")
            excluded_items.add("Job - Mimic")

        return excluded_items

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
            item = self.create_item(self.get_filler_item_name())
            pool.append(item)

        return pool

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)

        return item