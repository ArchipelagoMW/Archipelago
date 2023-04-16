from typing import Dict, Any, Iterable, Optional, Union
from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import DLCQuestItem, item_table, ItemData, create_items
from .Locations import location_table, DLCQuestLocation
from .Options import DLCQuest_options, DLCQuestOptions, fetch_options
from .Rules import set_rules
from .Regions import create_regions

client_version = 0


class DLCqwebworld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago DLCQuest game on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["axe_y"]
    )]


class DLCqworld(World):
    """
    DLCQuest is a metroid ish game where everything is an in-game dlc.
    """
    game = "DLCQuest"
    topology_present = False
    web = DLCqwebworld()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    data_version = 1

    option_definitions = DLCQuest_options

    def generate_early(self):
        self.options = fetch_options(self.multiworld, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options)

    def create_event(self, event: str):
        return DLCQuestItem(event, True, None, self.player)

    def create_items(self):
        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if not location.event])

        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]]

        created_items = create_items(self, self.options, locations_count + len(items_to_exclude), self.multiworld.random)

        self.multiworld.itempool += created_items

        for item in items_to_exclude:
            if item in self.multiworld.itempool:
                self.multiworld.itempool.remove(item)

    def create_item(self, item: Union[str, ItemData]) -> DLCQuestItem:
        if isinstance(item, str):
            item = item_table[item]

        return DLCQuestItem(item.name, item.classification, item.code, self.player)

    def fill_slot_data(self):
        return {
            "death_link": self.multiworld.death_link[self.player].value,
            "ending_choice": self.multiworld.ending_choice[self.player].value,
            "campaign": self.multiworld.campaign[self.player].value,
            "coinsanity": self.multiworld.coinsanity[self.player].value,
            "coinbundlerange": self.multiworld.coinbundlequantity[self.player].value,
            "item_shuffle": self.multiworld.item_shuffle[self.player].value,
            "seed": self.multiworld.per_slot_randoms[self.player].randrange(99999999)
        }
