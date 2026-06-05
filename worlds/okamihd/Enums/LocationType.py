from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import OkamiWorld


class LocationType(Enum):
    FREESTANDING_ITEM = 0,
    NORMAL_CHEST = 1,
    UNDERWATER_CHEST = 2,
    TREASURE_BUD = 3,
    BURNING_CHEST = 4,
    BURIED_CHEST = 5,
    STONE_BURIED_CHEST = 6,
    CONSTELLATION = 7,
    BURIED_UNDER_LEAF_PILE = 8,
    EVENT = 9
    BURNING_CHEST_NO_WATER = 10,
    DARUMA = 11,
    # Like underwater chest, but can also be obtained with cherry bomb.
    UNDERWATER_CHEST_SHALLOW = 12,
    # Slash, Bomb, Bloom
    DIGGING_MINIGAME_EARLY = 13,
    # + Watersprout + Galestrom
    DIGGING_MINIGAME_LATER = 14,
    # Frozen chest
    FROZEN_CHEST = 15,
    # Shop item slot
    SHOP = 16,
    FISHING_MINIGAME = 17
    # Chest that can only be opened by Issun in Tiny size
    LOCKED_CHEST = 18
    THUNDER_CHEST = 19
    # Chest with element Sources that depend on special rules; Don't apply any requirments except the special rule one
    THUNDER_CHEST_SPECIAL_SOURCE = 20
    FROZEN_CHEST_SPECIAL_SOURCE = 21
    # + Holy Eagle + Golden Ink Pot
    DIGGING_MINIGAME_HARD = 22
