from enum import IntEnum, IntFlag
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification


class OkamiLocation(Location):
    game = "Okami"


class OkamiItem(Item):
    game = "Okami"

class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification