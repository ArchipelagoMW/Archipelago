from worlds.AutoWorld import World
from .Items import TemplateItem, item_data
from .Locations import location_data
from .Regions import create_regions
from .Options import TemplateGameOptions

class TemplateWorld(World):
    """
    Scratch Shop is a progressive shopping simulator where players collect various 
    types of currency to unlock shop items.
    """
    game = "Scratch Shop"
    topology_present = True 
    options_dataclass = TemplateGameOptions # Uses the new dataclass structure

    item_name_to_id = {name: data[0] for name, data in item_data.items()}
    location_name_to_id = location_data

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def create_items(self):
        pool = []
        for name, data in item_data.items():
            item_id = data[0]
            classification = data[1]
            item = TemplateItem(name, classification, item_id, self.player)
            pool.append(item)
        
        self.multiworld.itempool += pool

    def set_rules(self):
        self.multiworld.get_location("Shop 2", self.player).access_rule = \
            lambda state: state.has("Red Coin", self.player)
        self.multiworld.get_location("Shop 3", self.player).access_rule = \
            lambda state: state.has("Blue Coin", self.player)
        self.multiworld.get_location("Shop 4", self.player).access_rule = \
            lambda state: state.has("Orange Coin", self.player)
        self.multiworld.get_location("Shop 5", self.player).access_rule = \
            lambda state: state.has("Yellow Coin", self.player)
        self.multiworld.get_location("Shop 6", self.player).access_rule = \
            lambda state: state.has("Maroon Coin", self.player)
        self.multiworld.get_location("Shop 7", self.player).access_rule = \
            lambda state: state.has("Purple Coin", self.player)
        self.multiworld.get_location("Shop 8", self.player).access_rule = \
            lambda state: state.has("Green Coin", self.player)
        self.multiworld.get_location("Shop 9", self.player).access_rule = \
            lambda state: state.has("Lime Coin", self.player)
        self.multiworld.get_location("Shop 10", self.player).access_rule = \
            lambda state: state.has("Teal Coin", self.player)
        self.multiworld.get_location("Shop 11", self.player).access_rule = \
            lambda state: state.has("Gold Coin", self.player)
        self.multiworld.get_location("Shop 12", self.player).access_rule = \
            lambda state: state.has("Silver Coin", self.player)
        self.multiworld.get_location("Shop 13", self.player).access_rule = \
            lambda state: state.has("Bronze Coin", self.player)
        self.multiworld.get_location("Shop 14", self.player).access_rule = \
            lambda state: state.has("Iron Coin", self.player)
        self.multiworld.get_location("Shop 15", self.player).access_rule = \
            lambda state: state.has("Copper Coin", self.player)
        self.multiworld.get_location("Shop 16", self.player).access_rule = \
            lambda state: state.has("Indigo Coin", self.player)
        self.multiworld.get_location("Shop 17", self.player).access_rule = \
            lambda state: state.has("Regular Coin", self.player)
        self.multiworld.get_location("Shop 18", self.player).access_rule = \
            lambda state: state.has("Cat Coin", self.player)
        self.multiworld.get_location("Shop 19", self.player).access_rule = \
            lambda state: state.has("Dog Coin", self.player)
        self.multiworld.get_location("Shop 20", self.player).access_rule = \
            lambda state: state.has("Invisible Coin", self.player)

        # Define how the player wins the game
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Invisible Coin", self.player) and state.has("Dog Coin", self.player) and state.has("Cat Coin", self.player) and state.has("Regular Coin", self.player) and state.has("Indigo Coin", self.player) and state.has("Copper Coin", self.player) and state.has("Iron Coin", self.player) and state.has("Bronze Coin", self.player) and state.has("Silver Coin", self.player) and state.has("Gold Coin", self.player) and state.has("Teal Coin", self.player) and state.has("Lime Coin", self.player) and state.has("Green Coin", self.player) and state.has("Purple Coin", self.player) and state.has("Maroon Coin", self.player) and state.has("Yellow Coin", self.player) and state.has("Orange Coin", self.player) and state.has("Blue Coin", self.player) and state.has("Red Coin", self.player)