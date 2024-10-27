import enum
from dataclasses import dataclass
from typing import Optional

from BaseClasses import Item, ItemClassification
from worlds.sc2.item.item_tables import ItemData


class ItemFilterFlags(enum.IntFlag):
    Available = 0
    Locked = enum.auto()
    StartInventory = enum.auto()
    NonLocal = enum.auto()
    Removed = enum.auto()
    Plando = enum.auto()
    Excluded = enum.auto()
    AllowedOrphan = enum.auto()
    """Used to flag items that shouldn't be filtered out with their parents"""
    ForceProgression = enum.auto()
    """Used to flag items that aren't classified as progression by default"""
    Necessary = enum.auto()
    """Used to flag items that are never allowed to be culled.
    This differs from `Locked` in that locked items may still be culled if there's space issues or in some circumstances when a parent item is culled."""

    Unremovable = Locked|StartInventory|Plando|Necessary


@dataclass
class FilterItem:
    name: str
    data: ItemData
    index: int = 0
    flags: ItemFilterFlags = ItemFilterFlags.Available


class StarcraftItem(Item):
    game: str = "Starcraft 2"
    filter_flags: ItemFilterFlags = ItemFilterFlags.Available

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int, filter_flags: ItemFilterFlags = ItemFilterFlags.Available):
        super().__init__(name, classification, code, player)
        self.filter_flags = filter_flags
