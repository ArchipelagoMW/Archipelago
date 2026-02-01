from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

class HexcellsInfiniteLocation(Location):
    game = "HexcellsInfinite"

class HexcellsInfiniteItem(Item):
    game = "HexcellsInfinite"

class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    amount: int | None = 1

class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
