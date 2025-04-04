from enum import IntEnum
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification


class OkamiLocation(Location):
    game = "Okami"

class OkamiItem(Item):
    game = "Okami"

class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification

class BrushTechniques(IntEnum):
    # MAIN
    SUNRISE = 0x100
    REJUVENATION = 0x101
    POWER_SLASH=0x102
    CHERRY_BOMB=0x103
    GREENSPROUT_BLOOM= 0x104
    GREENSPROUT_WATERLILY = 0x105
    GREENSPROUT_VINE= 0x106
    WATERSPROUT= 0x107
    CRESCENT= 0x108
    GALESTROM= 0x109
    INFERNO= 0x110
    VEIL_OF_MIST= 0x111
    CATWALK= 0x112
    THUNDERSTROM= 0x113
    BLIZZARD= 0x114
    # UPGRADES/SECRET
    MIST_WARP= 0x115
    FIREBURST= 0x116
    WHIRLWIND= 0x117
    DELUGE= 0x118
    FOUNTAIN = 0x119
    THUNDERBOLT= 0x120
    # VERY SECRET ONE
    ICESTROM = 0x121

class LocData(NamedTuple):
    id: int = 0
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    # 0 => No, 1=> Yes, 2=> Iron Claws
    buried_chest:int =0

class ExitData(NamedTuple):
    name: str
    destination: str
    has_events: [str] = []
    doesnt_have_events:[str] =[]
    needs_swim:bool = False