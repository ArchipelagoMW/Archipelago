from typing import Dict, Optional, List, Set

from BaseClasses import Item, ItemClassification
from .Const import BASE_OFFSET
from .Data import data, ClairObscurItemData


class ClairObscurItem(Item):
    game = "Clair Obscur Expedition 33"

    def __init__(self, name: str, classification: ItemClassification, ap_id: Optional[int], player: int) -> None:
        super().__init__(name, classification, ap_id, player)

def offset_item_value(item_id: int) -> int:
    """
    Returns the AP item id for a given item value
    """
    return BASE_OFFSET + item_id

def reverse_offset_item_value(item_id: int) -> int:
    """
    Returns the item value for a given AP item id
    """
    return item_id - BASE_OFFSET


def create_item_name_to_ap_id() -> Dict[str, int]:
    """
    Creates a map from item name to their AP item id
    """
    name_to_ap_id = {}
    for item_id, attributes in data.items.items():
        name_to_ap_id[attributes.name] = offset_item_value(item_id)

    return name_to_ap_id

def get_classification(item_id: int) -> ItemClassification:
    return data.items[reverse_offset_item_value(item_id)].classification

def create_item_groups(items: Dict[int, ClairObscurItemData]) -> Dict[str, Set[str]]:
    item_groups: Dict[str, Set[str]] = {
        "Upgrade material": set(),
        "Exploration capacities": set(),
        "Quest item": set(),
        "Journal": set(),
        "Picto": set(),
        "Weapon": set(),
        "Character": set(),
        "Area": set()
    }

    for item in items.keys():
        item_groups[items[item].type].add(items[item].name)

    return item_groups
