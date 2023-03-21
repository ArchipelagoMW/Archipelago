from typing import Dict, Any, Iterable, Optional, Union
from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import DLCquestItem, item_table, ItemData, create_items
from .Locations import location_table, DLCquestLocation
from .Options import DLCquest_options, DLCQuestOptions, fetch_options
from .Rules import set_rules
from .Regions import create_regions

client_version = 0

class DLCqwebworld(WebWorld):
    tutorials = [Tutorial(
        "magic it is ",
        "a guide to not die",
        "Mandarin",
        "setup_en.md",
        "setup/en",
        ["axe_y"]
    )]


class DLCqworld(World):
    """
    DLCquest is a metroid ish game where everything is an in-game dlc.
    """
    game = "DLCquest"
    topology_present = False
    web = DLCqwebworld()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table


    data_version = 0

    option_definitions = DLCquest_options

    def generate_early(self):
        self.options = fetch_options(self.multiworld, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)






    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options)

    def create_event(self, event: str):
        return DLCquestItem(event, True, None, self.player)

    def create_items(self):
        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if not location.event])

        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]]

        created_items = create_items(self, self.options)


        self.multiworld.itempool += created_items





    def create_item(self, item: Union[str, ItemData]) -> DLCquestItem:
        if isinstance(item, str):
            item = item_table[item]

        return DLCquestItem(item.name, item.classification, item.code, self.player)

    def fill_slot_data(self):
        return {
            "death_link": self.multiworld.death_link[self.player].value,
            "ending_choice": self.multiworld.ending_choice[self.player].value,
            "campaign": self.multiworld.campaign[self.player].value,
            "coinsanity": self.multiworld.coinsanity[self.player].value,
            "coinbundlerange": self.multiworld.coinbundlequantity[self.player].value,
            "item_shuffle": self.multiworld.item_shuffle[self.player].value
        }

