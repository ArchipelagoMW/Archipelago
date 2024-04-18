from BaseClasses import Item, ItemClassification
from .Locations import JakAndDaxterLocation, location_table as item_table
from .Options import JakAndDaxterOptions
from .Regions import JakAndDaxterLevel, JakAndDaxterSubLevel, JakAndDaxterRegion, level_table, subLevel_table, \
    create_regions
from .Rules import set_rules
from .Items import JakAndDaxterItem
from .GameID import game_id, game_name, cell_offset, fly_offset, orb_offset
from ..AutoWorld import World


class JakAndDaxterWorld(World):
    game: str = game_name
    data_version = 1
    required_client_version = (0, 4, 5)

    options_dataclass = JakAndDaxterOptions
    options: JakAndDaxterOptions

    # Stored as {ID: Name} pairs, these must now be swapped to {Name: ID} pairs.
    item_name_to_id = {item_table[k]: k for k in item_table}
    location_name_to_id = {item_table[k]: k for k in item_table}
    item_name_groups = {
        "Power Cell": {item_table[k]: k
                       for k in item_table if k in range(game_id + cell_offset, game_id + fly_offset)},
        "Scout Fly": {item_table[k]: k
                      for k in item_table if k in range(game_id + fly_offset, game_id + orb_offset)},
        "Precursor Orb": {}  # TODO
    }

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player)

    def create_items(self):
        self.multiworld.itempool += [self.create_item(item_table[k]) for k in item_table]

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        if item_id in range(game_id + cell_offset, game_id + fly_offset):
            # Power Cell
            classification = ItemClassification.progression_skip_balancing
        elif item_id in range(game_id + fly_offset, game_id + orb_offset):
            # Scout Fly
            classification = ItemClassification.progression_skip_balancing
        elif item_id > game_id + orb_offset:
            # Precursor Orb
            classification = ItemClassification.filler  # TODO
        else:
            classification = ItemClassification.filler

        item = JakAndDaxterItem(name, classification, item_id, self.player)
        return item
