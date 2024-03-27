from enum import IntEnum, IntFlag
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification


class HatInTimeLocation(Location):
    game = "A Hat in Time"


class HatInTimeItem(Item):
    game = "A Hat in Time"


class HatType(IntEnum):
    NONE = -1
    SPRINT = 0
    BREWING = 1
    ICE = 2
    DWELLER = 3
    TIME_STOP = 4


class HitType(IntEnum):
    none = 0
    umbrella = 1
    umbrella_or_brewing = 2
    dweller_bell = 3


class HatDLC(IntFlag):
    none = 0b000
    dlc1 = 0b001
    dlc2 = 0b010
    death_wish = 0b100
    dlc1_dw = 0b101
    dlc2_dw = 0b110


class ChapterIndex(IntEnum):
    SPACESHIP = 0
    MAFIA = 1
    BIRDS = 2
    SUBCON = 3
    ALPINE = 4
    FINALE = 5
    CRUISE = 6
    METRO = 7


class Difficulty(IntEnum):
    NORMAL = -1
    MODERATE = 0
    HARD = 1
    EXPERT = 2


class LocData(NamedTuple):
    id: Optional[int] = 0
    region: Optional[str] = ""
    required_hats: Optional[List[HatType]] = [HatType.NONE]
    hookshot: Optional[bool] = False
    dlc_flags: Optional[HatDLC] = HatDLC.none
    paintings: Optional[int] = 0  # Paintings required for Subcon painting shuffle
    misc_required: Optional[List[str]] = []

    # For UmbrellaLogic setting only.
    hit_type: Optional[HitType] = HitType.none

    # Other
    act_event: Optional[bool] = False  # Only used for event locations. Copy access rule from act completion
    nyakuza_thug: Optional[str] = ""  # Name of Nyakuza thug NPC (for metro shops)
    snatcher_coin: Optional[str] = ""  # Only for Snatcher Coin event locations, name of the Snatcher Coin item


class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification
    dlc_flags: Optional[HatDLC] = HatDLC.none


hat_type_to_item = {
    HatType.SPRINT:     "Sprint Hat",
    HatType.BREWING:    "Brewing Hat",
    HatType.ICE:        "Ice Hat",
    HatType.DWELLER:    "Dweller Mask",
    HatType.TIME_STOP:  "Time Stop Hat",
}
