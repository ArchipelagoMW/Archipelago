import enum
from dataclasses import dataclass
from typing import Optional

from BaseClasses import Item, ItemClassification
from .item_tables import ItemData


class ItemFilterFlags(enum.IntFlag):
    """Removed > Start Inventory > Locked > Excluded > Requested > Culled"""
    Available = 0
    StartInventory = enum.auto()
    Locked = enum.auto()
    """Used to flag items that are never allowed to be culled."""
    LogicLocked = enum.auto()
    """Locked by item cull logic checks; logic-locked w/a upgrades may be removed if all parents are removed"""
    Requested = enum.auto()
    """Soft-locked items by item count checks during item culling; may be re-added"""
    Removed = enum.auto()
    """Marked for immediate removal"""
    UserExcluded = enum.auto()
    """Excluded by the user; display an error message if failing to exclude"""
    FilterExcluded = enum.auto()
    """Excluded by item filtering"""
    Culled = enum.auto()
    """Soft-removed by the item culling"""
    NonLocal = enum.auto()
    Plando = enum.auto()
    AllowedOrphan = enum.auto()
    """Used to flag items that shouldn't be filtered out with their parents"""
    ForceProgression = enum.auto()
    """Used to flag items that aren't classified as progression by default"""

    Unexcludable = StartInventory|Plando|Locked|LogicLocked
    UnexcludableUpgrade = StartInventory|Plando|Locked
    Uncullable = StartInventory|Plando|Locked|LogicLocked|Requested
    Excluded = UserExcluded|FilterExcluded
    RequestedOrBetter = StartInventory|Locked|LogicLocked|Requested
    CulledOrBetter = Removed|Excluded|Culled


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
