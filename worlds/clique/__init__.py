from typing import List, Dict, Any

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import CliqueItem, item_data_table, item_table
from .Locations import CliqueLocation, location_data_table, location_table, locked_locations
from .Options import CliqueOptions
from .Regions import region_data_table
from .Rules import get_button_rule


class CliqueWebWorld(WebWorld):
    theme = "partyTime"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Clique.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Phar"]
    )

    setup_de = Tutorial(
        tutorial_name="Anleitung zum Anfangen",
        description="Eine Anleitung um Clique zu spielen.",
        language="Deutsch",
        file_name="guide_de.md",
        link="guide/de",
        authors=["Held_der_Zeit"]
    )
    
    tutorials = [setup_en, setup_de]


class CliqueWorld(World):
    """The greatest game of all time."""

    game = "Clique"
    web = CliqueWebWorld()
    options: CliqueOptions
    options_dataclass = CliqueOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> CliqueItem:
        return CliqueItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[CliqueItem] = []
        for name, item in item_data_table.items():
            if item.code and item.can_create(self):
                item_pool.append(self.create_item(name))

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
            }, CliqueLocation)
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)

        # Set priority location for the Big Red Button!
        self.options.priority_locations.value.add("The Big Red Button")

    def get_filler_item_name(self) -> str:
        return "A Cool Filler Item (No Satisfaction Guaranteed)"

    def set_rules(self) -> None:
        button_rule = get_button_rule(self)
        self.get_location("The Big Red Button").access_rule = button_rule
        self.get_location("In the Player's Mind").access_rule = button_rule

        # Do not allow button activations on buttons.
        self.get_location("The Big Red Button").item_rule = lambda item: item.name != "Button Activation"

        # Completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: state.has("The Urge to Push", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "color": self.options.color.current_key
        }
