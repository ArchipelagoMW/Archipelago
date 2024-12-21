from enum import Enum
from typing import Callable, NamedTuple

from BaseClasses import Item, ItemClassification, MultiWorld


class LoonylandItem(Item):
    """
    Item from the game Loonyland
    """

    game: str = "Loonyland"
    cheat: bool = False


class LLItemCat(Enum):
    ITEM = 0
    CHEAT = 1
    FILLER = 2
    TRAP = 3
    EVENT = 4


class LLItem(NamedTuple):
    id: int
    category: LLItemCat
    classification: ItemClassification
    frequency: int = 1
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
