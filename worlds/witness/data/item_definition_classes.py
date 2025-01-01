from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from BaseClasses import ItemClassification


class ItemCategory(Enum):
    SYMBOL = 0
    DOOR = 1
    LASER = 2
    USEFUL = 3
    FILLER = 4
    TRAP = 5
    JOKE = 6
    EVENT = 7


CATEGORY_NAME_MAPPINGS: Dict[str, ItemCategory] = {
    "Symbols:": ItemCategory.SYMBOL,
    "Doors:": ItemCategory.DOOR,
    "Lasers:": ItemCategory.LASER,
    "Useful:": ItemCategory.USEFUL,
    "Filler:": ItemCategory.FILLER,
    "Traps:": ItemCategory.TRAP,
    "Jokes:": ItemCategory.JOKE
}


@dataclass(frozen=True)
class ItemDefinition:
    local_code: int
    category: ItemCategory


@dataclass(frozen=True)
class ProgressiveItemDefinition(ItemDefinition):
    child_item_names: List[str]


@dataclass(frozen=True)
class DoorItemDefinition(ItemDefinition):
    panel_id_hexes: List[str]


@dataclass(frozen=True)
class WeightedItemDefinition(ItemDefinition):
    weight: int


@dataclass()
class ItemData:
    """
    ItemData for an item in The Witness
    """
    ap_code: Optional[int]
    definition: ItemDefinition
    classification: ItemClassification
    local_only: bool = False
