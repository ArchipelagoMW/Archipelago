from BaseClasses import Item, ItemClassification
from .Util import get_data_json

class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"

    def __init__(self, name: str, classification: ItemClassification, code: int, player: int):
        super().__init__(name, classification, code, player)

def create_ball_items(self):
    data = get_data_json()
    items = []

    for item in data["ball_items"]:
        new_item = PokemonEmeraldItem(item["name"], ItemClassification.filler, item["default_item"], self.player)
        items.append(new_item)

    return items

def create_item_name_to_id_map():
    data = get_data_json()

    map = {}
    for item in data["ball_items"]:
        map[item["name"]] = item["default_item"]

    return map
