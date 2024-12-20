from enum import Enum
from typing import NamedTuple, Callable

from BaseClasses import Location, MultiWorld

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
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


