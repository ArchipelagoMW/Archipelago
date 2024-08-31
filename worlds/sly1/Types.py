from enum import IntEnum, IntFlag
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification

class Sly1Location(Location):
    game = "Sly Cooper and the Thievius Raccoonus"

class Sly1Item(Item):
    game = "Sly Cooper and the Thievius Raccoonus"

class EpisodeType(IntEnum):
    ToT = 1
    SSE = 2
    VV = 3
    FitS = 4

class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1


class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
    key_requirement: int = 0

episode_type_to_name = {
    EpisodeType.ToT:      "Tides of Terror",
    EpisodeType.SSE:      "Sunset Snake Eyes",
    EpisodeType.VV:       "Vicious Voodoo",
    EpisodeType.FitS:     "Fire in the Sky"
}