import typing, os, json
from BaseClasses import Item, ItemClassification, Region, Entrance, Location
from .Locations import JakAndDaxterLocation, location_table
from .Options import JakAndDaxterOptions
from .Regions import JakAndDaxterLevel, JakAndDaxterSubLevel, JakAndDaxterRegion, level_table, subLevel_table, create_regions
from .Rules import set_rules
from .Items import JakAndDaxterItem, item_table, generic_item_table, special_item_table
from .GameID import game_id
from ..AutoWorld import World

from Utils import visualize_regions

class JakAndDaxterWorld(World):
    game: str = "Jak and Daxter: The Precursor Legacy"

    # Stored as {ID: Name} pairs, these must now be swapped to {Name: ID} pairs.
    item_name_to_id = {item_table[k]: game_id + k for k in item_table}
    location_name_to_id = {location_table[k]: game_id + k for k in location_table}

    options_dataclass = JakAndDaxterOptions
    options: JakAndDaxterOptions

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player)

    def create_item(self, name: str, item_id: int) -> Item:
        if "Power Cell" in name:
            classification = ItemClassification.progression_skip_balancing
        elif "Scout Fly" in name:
            classification = ItemClassification.progression_skip_balancing
        elif "Precursor Orb" in name:
            classification = ItemClassification.filler # TODO
        else:
            classification = ItemClassification.progression

        item = JakAndDaxterItem(name, classification, item_id, self.player)
        return item

    def create_items(self):
        self.multiworld.itempool += [self.create_item("Power Cell", game_id + k) for k in range(0, 101)]
        # self.multiworld.itempool += [self.create_item(item_table[101]) for k in range(101, 212)]
        self.multiworld.itempool += [self.create_item(item_table[k], game_id + k) for k in special_item_table]
