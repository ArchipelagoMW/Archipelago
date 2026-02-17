"""
Classes and functions related to AP items for Kirby & The Amazing Mirror
"""
from typing import Dict, FrozenSet, Optional, Set

from BaseClasses import Item, ItemClassification

from .data import data


class KirbyAmItem(Item):
    game: str = "Kirby & The Amazing Mirror"
    tags: frozenset[str]

    def __init__(self, name: str, classification: ItemClassification, code: int | None, player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            # data.items is keyed by the final AP item id (code).
            self.tags = data.items[code].tags


def create_item_label_to_code_map() -> dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    label_to_code_map: dict[str, int] = {}
    for item_id, attributes in data.items.items():
        label_to_code_map[attributes.label] = item_id

    return label_to_code_map


def get_item_classification(item_code: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[item_code].classification
