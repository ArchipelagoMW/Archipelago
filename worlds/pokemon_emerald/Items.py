from BaseClasses import Item, ItemClassification
from .Util import get_data_json

class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"

    def __init__(self, name: str, classification: ItemClassification, code: int, player: int):
        super().__init__(name, classification, code, player)

def create_item_name_to_id_map():
    data = get_data_json()

    map = {}
    for item in data["ball_items"]:
        map[item["name"]] = item["default_item"]
    for item in data["hidden_items"]:
        map[item["name"]] = item["default_item"]

    map["ITEM_BADGE_1"] = data["constants"]["items"]["ITEM_BADGE_1"]
    map["ITEM_BADGE_2"] = data["constants"]["items"]["ITEM_BADGE_2"]
    map["ITEM_BADGE_3"] = data["constants"]["items"]["ITEM_BADGE_3"]
    map["ITEM_BADGE_4"] = data["constants"]["items"]["ITEM_BADGE_4"]
    map["ITEM_BADGE_5"] = data["constants"]["items"]["ITEM_BADGE_5"]
    map["ITEM_BADGE_6"] = data["constants"]["items"]["ITEM_BADGE_6"]
    map["ITEM_BADGE_7"] = data["constants"]["items"]["ITEM_BADGE_7"]
    map["ITEM_BADGE_8"] = data["constants"]["items"]["ITEM_BADGE_8"]

    return map

def create_badge_items(self):
    data = get_data_json()
    return [
        PokemonEmeraldItem("ITEM_BADGE_1", ItemClassification.progression, data["constants"]["items"]["ITEM_BADGE_1"], self.player),
        PokemonEmeraldItem("ITEM_BADGE_2", ItemClassification.progression, data["constants"]["items"]["ITEM_BADGE_2"], self.player),
        PokemonEmeraldItem("ITEM_BADGE_3", ItemClassification.progression, data["constants"]["items"]["ITEM_BADGE_3"], self.player),
        PokemonEmeraldItem("ITEM_BADGE_4", ItemClassification.progression, data["constants"]["items"]["ITEM_BADGE_4"], self.player),
        PokemonEmeraldItem("ITEM_BADGE_5", ItemClassification.progression, data["constants"]["items"]["ITEM_BADGE_5"], self.player),
        PokemonEmeraldItem("ITEM_BADGE_6", ItemClassification.progression, data["constants"]["items"]["ITEM_BADGE_6"], self.player),
        PokemonEmeraldItem("ITEM_BADGE_7", ItemClassification.progression, data["constants"]["items"]["ITEM_BADGE_7"], self.player),
        PokemonEmeraldItem("ITEM_BADGE_8", ItemClassification.progression, data["constants"]["items"]["ITEM_BADGE_8"], self.player),
    ]

def create_ball_items(self):
    data = get_data_json()
    items = []

    for item in data["ball_items"]:
        new_item = PokemonEmeraldItem(item["name"], ItemClassification.filler, item["default_item"], self.player)
        items.append(new_item)

    return items

def create_hidden_items(self):
    data = get_data_json()
    items = []

    for item in data["hidden_items"]:
        new_item = PokemonEmeraldItem(item["name"], ItemClassification.filler, item["default_item"], self.player)
        items.append(new_item)

    return items
