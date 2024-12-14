from enum import Enum
from typing import NamedTuple, Dict

from BaseClasses import Location

loonyland_base_id: int = 2876900


class LoonylandLocation(Location):
    game = "Loonyland"


class LL_LocCat(Enum):
    PICKUP = 0
    QUEST = 1
    BADGE = 2
    EVENT = 4


class LL_Location(NamedTuple):
    id: int
    category: LL_LocCat
    region: str


