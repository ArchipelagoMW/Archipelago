from worlds.AutoWorld import WebWorld, World
from .Options import GSTLAOptions

from .Items import GSTLAItem, item_table, all_items
from .Locations import GSTLALocation, all_locations

class GSTLAWeb(WebWorld):
    theme = "jungle"

class GSTLAWorld(World):
    game = "Golden Sun The Lost Age"
    option_definitions = GSTLAOptions
    data_version = 1

    item_name_to_id = {item.itemName: item.id for item in all_items }
    location_name_to_id = {location.name: location.id for location in all_locations}

    web = GSTLAWeb()

def generate_early(self) -> None:
    pass

def create_regions(self) -> None:
    pass

def create_items(self) -> None:
    pass

def set_rules(self) -> None:
    pass

def generate_output(self, output_directory: str):
    pass

def create_item(self, name: str) -> "Item":
    item = item_table[name]
    return GSTLAItem(item.itemName, item.progression, item.id, self.player)

def create_event(self, event: str):
    pass