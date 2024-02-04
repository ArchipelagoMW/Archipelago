from typing import List

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import Celeste64Item, item_data_table, item_table
from .Locations import Celeste64Location, location_data_table, location_table
from .Names import ItemName, LocationName
from .Options import Celeste64Options
from .Regions import region_data_table
from .Rules import set_rules


class Celeste64WebWorld(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Celeste 64 in Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["PoryGone"]
    )

    tutorials = [setup_en]


class Celeste64World(World):
    """Relive the magic of Celeste Mountain alongside Madeline in this small, heartfelt 3D platformer.
    Created in a week(ish) by the Celeste team to celebrate the game’s sixth anniversary 🍓✨"""

    game = "Celeste 64"
    data_version = 0
    web = Celeste64WebWorld()
    options_dataclass = Celeste64Options
    options: Celeste64Options
    location_name_to_id = location_table
    item_name_to_id = item_table


    def create_item(self, name: str) -> Celeste64Item:
        # Potentially don't make all strawberries Progression
        return Celeste64Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[Celeste64Item] = []
        for name, item in item_data_table.items():
            item_pool.append(self.create_item(name))

        for _ in range(21):
            item_pool.append(self.create_item(ItemName.strawberry))

        self.multiworld.itempool += item_pool


    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name
            }, Celeste64Location)
            region.add_exits(region_data_table[region_name].connecting_regions)


    def get_filler_item_name(self) -> str:
        return ItemName.strawberry


    def set_rules(self) -> None:
        set_rules(self)


    def fill_slot_data(self):
        return {
            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
            "strawberries_required": self.options.strawberries_required.value
        }
