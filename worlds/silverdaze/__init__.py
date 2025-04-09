#Sawyer: I'll get to this sooner or later!

from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import SDItem, SDItemData, event_item_table, get_items_by_category, item_table
from .Locations import SDLocation, location_table
#from .Options import SDOptions
#from .Presets import sd_options_presets
from .Rules import set_rules

class SDWorld(World):
    """
    This is where I'll describe Silver Daze once we get that far.
    """
    game = "Silver Daze"
    #options_dataclass = SDOptions
    #options: SDOptions
    required_client_version = (0, 5, 4)

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}
    
def create_items(self):
    item_pool: List[SDItem] = []
     #Characters, I think?
    starting_character = "Pinn"
    #Later, let's make this an option
    itempool.remove(starting_character)
    self.multiworld.push_precollected(self.create_item(starting_character))
    
    #Start adding the actual items
    total_locations = len(self.multiworld.get_unfilled_locations(self.player))
    for name, data in item_table.items():
        quantity = data.max_quantity
        item_pool += [self.create_item(name) for _ in range(0, quantity)]


# Fill any empty locations with filler items.
while len(item_pool) < total_locations:
    item_pool.append(self.create_item(self.get_filler_item_name()))
    self.multiworld.itempool += item_pool


def get_filler_item_name(self) -> str:
    fillers = get_items_by_category("Filler")
    weights = [data.weight for data in fillers.values()]
    return self.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
    
def create_item(self, name: str) -> SDItem:
    data = item_table[name]
    return SDItem(name, data.classification, data.code, self.player)

def create_event(self, name: str) -> SDItem:
    data = event_item_table[name]
    return SDItem(name, data.classification, data.code, self.player)

def set_rules(self):
    set_rules(self, self.player)

def create_regions(self):
    create_regions(self)
    self._place_events()