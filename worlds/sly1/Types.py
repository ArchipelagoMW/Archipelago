from enum import IntEnum, IntFlag
from typing import NamedTuple, Optional, List
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

class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1


class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
    key_type: Optional[EpisodeType]
    key_requirement: Optional[int] = 0

episode_type_to_name = {
    EpisodeType.TOT:      "Tides of Terror",
    EpisodeType.SSE:      "Sunset Snake Eyes",
    EpisodeType.VV:       "Vicious Voodoo",
    EpisodeType.FITS:     "Fire in the Sky",
    EpisodeType.CHOH:     "Cold Heart of Hate"
}

episode_type_to_shortened_name = {
    EpisodeType.TOT:    "ToT",
    EpisodeType.SSE:    "SSE",
    EpisodeType.VV:     "VV",
    EpisodeType.FITS:   "FitS",
    EpisodeType.CHOH:   "CHoH"
}