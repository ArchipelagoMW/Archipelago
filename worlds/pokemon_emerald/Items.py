from typing import FrozenSet, Optional, Union
from BaseClasses import Item, ItemClassification
from .Data import get_item_attributes


class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)

        if (code == None):
            self.tags = set(["Event"])
        else:
            self.tags = get_item_attributes()[reverse_offset_item_value(code)].tags


def offset_item_value(item_value: Union[int, None]) -> Union[int, None]:
    if (item_value == None): return None
    return item_value + 3860000


def reverse_offset_item_value(id: Union[int, None]) -> Union[int, None]:
    if (id == None): return None
    return id - 3860000


def create_item_label_to_id_map():
    items = get_item_attributes()

    map = {}
    for item_value, attributes in items.items():
        map[attributes.label] = offset_item_value(item_value)

    return map


def get_item_classification(item_code: int):
    return get_item_attributes()[reverse_offset_item_value(item_code)].classification
