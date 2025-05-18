from typing import List, Dict, Any
import random

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import SohItem, item_data_table, item_table
from .Locations import SohLocation, location_data_table, location_table, locked_locations
from .Options import SohOptions
from .Regions import region_data_table
from .Rules import get_soh_rule


class SohWebWorld(WebWorld):
    theme = "ice"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Ship of Harkinian.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["aMannus"]
    )
    
    tutorials = [setup_en]
    game_info_languages = ["en"]


class SohWorld(World):
    """A PC Port of Ocarina of Time"""

    game = "Ship of Harkinian"
    web = SohWebWorld()
    options: SohOptions
    options_dataclass = SohOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> SohItem:
        return SohItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[SohItem] = []

        location_count: int = 0

        # Count Total Locations.
        for location_name, location_data in location_data_table.items():
            # Ignore locations excluded due to options selected
            if not location_data.can_create(self):
                continue
            location_count += 1

        # Filler item list
        filler_items = ["Recovery Heart", "Blue Rupee", "Red Rupee", "Purple Rupee", "Huge Rupee", "Bombs 5", "Bombs 10", "Arrows 5", "Arrows 10", "Deku Nuts 5", "Deku Nuts 10", "Deku Stick 1"]

        # Add Base Progression Items
        item_pool.append(self.create_item("Progressive Bomb Bag"))
        item_pool.append(self.create_item("Progressive Bomb Bag"))

        filler_item_count: int = location_count - len(item_pool)
        item_pool += [self.create_item(filler_items[random.randint(0, 11)]) for _ in range(filler_item_count)]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self)
            }, SohLocation)
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)

    def get_filler_item_name(self) -> str:
        return "Blue Rupee"

    def set_rules(self) -> None:
        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: True

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "death_link": self.options.death_link.value,
        }
