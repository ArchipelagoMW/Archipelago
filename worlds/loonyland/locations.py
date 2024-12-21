from enum import Enum
from typing import Callable, NamedTuple

from BaseClasses import Location, MultiWorld


class LoonylandLocation(Location):
    game = "Loonyland"


class LLLocCat(Enum):
    PICKUP = 0
    QUEST = 1
    BADGE = 2
    EVENT = 4


class LLLocation(NamedTuple):
    id: int
    category: LLLocCat
    region: str
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


