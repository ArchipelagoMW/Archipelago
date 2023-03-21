from typing import FrozenSet, Optional, Union
from BaseClasses import Item, ItemClassification
from .Data import get_item_attributes, get_config


class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = get_item_attributes()[reverse_offset_item_value(code)].tags


def offset_item_value(item_value: Union[int, None]) -> Union[int, None]:
    if item_value is None:
        return None
    return item_value + get_config()["ap_offset"]


def reverse_offset_item_value(id: Union[int, None]) -> Union[int, None]:
    if id is None:
        return None
    return id - get_config()["ap_offset"]


def create_item_label_to_id_map():
    items = get_item_attributes()

    label_to_id_map = {}
    for item_value, attributes in items.items():
        label_to_id_map[attributes.label] = offset_item_value(item_value)

    return label_to_id_map


def get_item_classification(item_code: int):
    return get_item_attributes()[reverse_offset_item_value(item_code)].classification
