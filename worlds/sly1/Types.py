from enum import IntEnum
from typing import Any, NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

class Sly1Location(Location):
    game = "Sly Cooper and the Thievius Raccoonus"

class Sly1Item(Item):
    game = "Sly Cooper and the Thievius Raccoonus"

class EpisodeType(IntEnum):
    TOT = 1
    SSE = 2
    VV = 3
    FITS = 4
    CHOH = 5
    ALL = 6

class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1

class EventData(NamedTuple):
    name:       str
    ap_code:    Optional[int] = None

class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
    key_type: Optional[EpisodeType] = None
    key_requirement: Optional[int] = 0
    level_type: Optional[str] = None

class LevelData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
    bottle_amount: Optional[int]

episode_type_to_name = {
    EpisodeType.TOT:      "Tide of Terror",
    EpisodeType.SSE:      "Sunset Snake Eyes",
    EpisodeType.VV:       "Vicious Voodoo",
    EpisodeType.FITS:     "Fire in the Sky",
    EpisodeType.CHOH:     "Cold Heart of Hate",
    EpisodeType.ALL:      "All"
}

episode_type_to_shortened_name = {
    EpisodeType.TOT:    "ToT",
    EpisodeType.SSE:    "SSE",
    EpisodeType.VV:     "VV",
    EpisodeType.FITS:   "FitS",
    EpisodeType.CHOH:   "CHoH",
    EpisodeType.ALL:    "All"
}