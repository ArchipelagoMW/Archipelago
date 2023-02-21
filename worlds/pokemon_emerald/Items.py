from BaseClasses import Item, ItemClassification
from .Data import get_item_attributes


class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"

    def __init__(self, name: str, classification: ItemClassification, code: int, player: int):
        super().__init__(name, classification, code, player)


def create_item_name_to_id_map():
    items = get_item_attributes()

    map = {}
    for id, attributes in items.items():
        map[attributes.label] = id

    return map


def get_item_classification(item_id):
    return get_item_attributes()[item_id].classification
