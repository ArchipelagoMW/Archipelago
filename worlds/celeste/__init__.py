from copy import deepcopy
from typing import Dict, List

from BaseClasses import ItemClassification, Location, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import CelesteItem, item_table, item_data_table
from .Locations import CelesteLocation, location_table, strawberry_location_data_table
from .Names import ItemName, LocationName
from .Options import CelesteOptions, celeste_option_groups, resolve_options


class CelesteWebWorld(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Celeste in Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["PoryGone"]
    )

    tutorials = [setup_en]

    option_groups = celeste_option_groups


class CelesteWorld(World):
    """TBD"""

    # Class Data
    game = "Celeste"
    web = CelesteWebWorld()
    options_dataclass = CelesteOptions
    options: CelesteOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    # Instance Data
    madeline_one_dash_hair_color: int
    madeline_two_dash_hair_color: int
    madeline_no_dash_hair_color: int
    madeline_feather_hair_color: int

    def generate_early(self) -> None:
        resolve_options(self)

    def create_item(self, name: str) -> CelesteItem:
        return CelesteItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[CelesteItem] = []

        location_count: int = 1

        real_total_strawberries: int = min(self.options.total_strawberries.value, location_count - len(item_pool))
        self.strawberries_required = int(real_total_strawberries * (self.options.strawberries_required_percentage / 100))

        item_pool += [self.create_item(ItemName.strawberry) for _ in range(real_total_strawberries)]

        filler_item_count: int = location_count - len(item_pool)
        item_pool += [self.create_item(ItemName.raspberry) for _ in range(filler_item_count)]

        self.multiworld.itempool += item_pool


    def create_regions(self) -> None:
        from .Regions import region_data_table
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in strawberry_location_data_table.items()
                if location_data.region == region_name
            }, CelesteLocation)

            region.add_exits(region_data_table[region_name].connecting_regions)


    def get_filler_item_name(self) -> str:
        return ItemName.raspberry


    def set_rules(self) -> None:
        from .Rules import set_rules
        set_rules(self)


    def fill_slot_data(self):
        return {
            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
            "strawberries_required": self.strawberries_required,
            "madeline_one_dash_hair_color": self.madeline_one_dash_hair_color,
            "madeline_two_dash_hair_color": self.madeline_two_dash_hair_color,
            "madeline_no_dash_hair_color": self.madeline_no_dash_hair_color,
            "madeline_feather_hair_color": self.madeline_feather_hair_color,
        }
