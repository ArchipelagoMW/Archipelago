from typing import Dict, FrozenSet, Optional, Union
from BaseClasses import Item, ItemClassification
from .Data import data, config


class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[reverse_offset_item_value(code)].tags


def offset_item_value(item_value: Union[int, None]) -> Union[int, None]:
    if item_value is None:
        return None
    return item_value + config["ap_offset"]


def reverse_offset_item_value(item_id: Union[int, None]) -> Union[int, None]:
    if item_id is None:
        return None
    return item_id - config["ap_offset"]


def create_item_label_to_code_map() -> Dict[str, int]:
    label_to_code_map: Dict[str, int] = {}
    for item_value, attributes in data.items.items():
        label_to_code_map[attributes.label] = offset_item_value(item_value)

    return label_to_code_map


def get_item_classification(item_code: int):
    return data.items[reverse_offset_item_value(item_code)].classification
