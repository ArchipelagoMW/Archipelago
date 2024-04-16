from BaseClasses import Item, ItemClassification
from .Locations import JakAndDaxterLocation, location_table
from .Options import JakAndDaxterOptions
from .Regions import JakAndDaxterLevel, JakAndDaxterSubLevel, JakAndDaxterRegion, level_table, subLevel_table, \
    create_regions
from .Rules import set_rules
from .Items import JakAndDaxterItem, item_table, generic_item_table, special_item_table
from .GameID import game_id
from ..AutoWorld import World


class JakAndDaxterWorld(World):
    game: str = "Jak and Daxter: The Precursor Legacy"
    data_version = 1
    required_client_version = (0, 4, 5)

    # Stored as {ID: Name} pairs, these must now be swapped to {Name: ID} pairs.
    item_name_to_id = {item_table[k]: game_id + k for k in item_table}
    location_name_to_id = {location_table[k]: game_id + k for k in location_table}

    options_dataclass = JakAndDaxterOptions
    options: JakAndDaxterOptions

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player)

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        if "Power Cell" in name:
            classification = ItemClassification.progression_skip_balancing
        elif "Scout Fly" in name:
            classification = ItemClassification.progression_skip_balancing
        elif "Precursor Orb" in name:
            classification = ItemClassification.filler  # TODO
        else:
            classification = ItemClassification.progression

        item = JakAndDaxterItem(name, classification, item_id, self.player)
        return item

    def create_items(self):
        self.multiworld.itempool += [self.create_item("Power Cell") for _ in range(0, 101)]
        self.multiworld.itempool += [self.create_item("Scout Fly") for _ in range(101, 213)]
        self.multiworld.itempool += [self.create_item(item_table[k]) for k in special_item_table]
