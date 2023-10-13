# world/khcom/__init__.py

import settings
import typing
from .Options import khcom_options  # the options we defined earlier
from .Items import KHCOMItem, item_table  # data used below to add items to the World
from .Locations import KHCOMAchievement, achievement_table  # same as above
from .Rules import set_rules
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification


class KHCOMWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Kingdom Hearts Chain of Memories Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "khcom_en.md",
        "khcom/en",
        ["Phar"]
    )]
    bug_report_page = "https://github.com/ThePhar/RogueLegacyRandomizer/issues/new?assignees=&labels=bug&template=" \
                      "report-an-issue---.md&title=%5BIssue%5D"

class KHCOMWorld(World):
    game = "Kingdom Hearts Chain of Memories"
    options_dataclass = khcom_options
    options: khcom_options
    topology_present = True
    base_id = 7474

    item_name_to_id = {name: id for
                       id, name in enumerate(item_table, base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(mygame_locations, base_id)}
    
    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        return {option_name: self.get_setting(option_name).value for option_name in khcom_options}
        
    def create_items(self):
        item_pool: List[KHCOMItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        for name, data in item_table.items():
            quantity = data.khcomamount
    
    def create_item(self, name: str) -> KHCOMItem:
        data = item_table[name]
        return KHCOMItem(name, data.classification, data.code, self.player)
    
    def set_rules(self):
        set_rules(self.multiworld, self.player)
    
    def create_regions(self):
        create_regions(self.multiworld, self.player)
        self._place_events()