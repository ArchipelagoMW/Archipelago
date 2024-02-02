from enum import IntEnum, IntFlag
from typing import Callable, Optional

from BaseClasses import CollectionState


class ItemType(IntEnum):
    JEWEL = 0
    CD = 1
    ITEM = 2
    EVENT = 3
    ABILITY = 4


class Box(IntEnum):
    JEWEL_NE = 0
    JEWEL_SE = 1
    JEWEL_SW = 2
    JEWEL_NW = 3
    CD = 4
    FULL_HEALTH = 5


class LocationType(IntEnum):
    BOX = 0
    BOSS = 1
    KEYZER = 2


class ItemFlag(IntFlag):
    JEWEL_NE = 1 << 0
    JEWEL_SE = 1 << 1
    JEWEL_SW = 1 << 2
    JEWEL_NW = 1 << 3
    CD = 1 << 4
    KEYZER = 1 << 5
    FULL_HEALTH = 1 << 6
    FULL_HEALTH_2 = 1 << 7


class Passage(IntEnum):
    ENTRY = 0
    EMERALD = 1
    RUBY = 2
    TOPAZ = 3
    SAPPHIRE = 4
    GOLDEN = 5

    def long_name(self):
        if self == Passage.GOLDEN:
            return 'Golden Pyramid'
        else:
            return self.short_name() + ' Passage'

    def short_name(self):
        return ('Entry', 'Emerald', 'Ruby', 'Topaz', 'Sapphire', 'Golden')[self]


AccessRule = Optional[Callable[[CollectionState], bool]]
