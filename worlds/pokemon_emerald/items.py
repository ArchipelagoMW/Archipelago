"""
Classes and functions related to AP items for Pokemon Emerald
"""
from typing import Dict, FrozenSet, Set, Optional, Union

from BaseClasses import Item, ItemClassification

from .data import config, data


class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[reverse_offset_item_value(code)].tags


def offset_item_value(item_value: Union[int, None]) -> Union[int, None]:
    """
    Returns the AP item id (code) for a given item value
    """
    if item_value is None:
        return None
    return item_value + config["ap_offset"]


def reverse_offset_item_value(item_id: Union[int, None]) -> Union[int, None]:
    """
    Returns the item value for a given AP item id (code)
    """
    if item_id is None:
        return None
    return item_id - config["ap_offset"]


def create_item_label_to_code_map() -> Dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    label_to_code_map: Dict[str, int] = {}
    for item_value, attributes in data.items.items():
        label_to_code_map[attributes.label] = offset_item_value(item_value)

    return label_to_code_map


def create_item_groups() -> Dict[str, Set[str]]:
    return {
        "Badge": {
            "Stone Badge", "Knuckle Badge",
            "Dynamo Badge", "Heat Badge",
            "Balance Badge", "Feather Badge",
            "Mind Badge", "Rain Badge"
        },
        "HM": {
            "HM01 Cut", "HM02 Fly",
            "HM03 Surf", "HM04 Strength",
            "HM05 Flash", "HM06 Rock Smash",
            "HM07 Waterfall", "HM08 Dive"
        }
    }


def get_item_classification(item_code: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[reverse_offset_item_value(item_code)].classification
