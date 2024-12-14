from typing import NamedTuple

from BaseClasses import Item, ItemClassification
from enum import Enum

class LoonylandItem(Item):
    """
    Item from the game Loonyland
    """
    game: str = "Loonyland"

class LL_ItemCat(Enum):
    ITEM = 0
    CHEAT = 1
    FILLER = 2
    TRAP = 3
    EVENT = 4


class LL_Item(NamedTuple):
    id: int
    category: LL_ItemCat
    classification: ItemClassification
    frequency: int = 1
