"""
Classes and functions related to AP items for Pokemon Emerald
"""
from typing import Dict, FrozenSet, Optional

from BaseClasses import Item, ItemClassification

from .data import BASE_OFFSET, data


class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[reverse_offset_item_value(code)].tags


def offset_item_value(item_value: int) -> int:
    """
    Returns the AP item id (code) for a given item value
    """
    return item_value + BASE_OFFSET


def reverse_offset_item_value(item_id: int) -> int:
    """
    Returns the item value for a given AP item id (code)
    """
    return item_id - BASE_OFFSET


def create_item_label_to_code_map() -> Dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    label_to_code_map: Dict[str, int] = {}
    for item_value, attributes in data.items.items():
        label_to_code_map[attributes.label] = offset_item_value(item_value)

    return label_to_code_map


ITEM_GROUPS = {
    "Badges": {
        "Stone Badge", "Knuckle Badge",
        "Dynamo Badge", "Heat Badge",
        "Balance Badge", "Feather Badge",
        "Mind Badge", "Rain Badge",
    },
    "HMs": {
        "HM01 Cut", "HM02 Fly",
        "HM03 Surf", "HM04 Strength",
        "HM05 Flash", "HM06 Rock Smash",
        "HM07 Waterfall", "HM08 Dive",
    },
    "HM01": {"HM01 Cut"},
    "HM02": {"HM02 Fly"},
    "HM03": {"HM03 Surf"},
    "HM04": {"HM04 Strength"},
    "HM05": {"HM05 Flash"},
    "HM06": {"HM06 Rock Smash"},
    "HM07": {"HM07 Waterfall"},
    "HM08": {"HM08 Dive"},
}


def get_item_classification(item_code: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[reverse_offset_item_value(item_code)].classification
