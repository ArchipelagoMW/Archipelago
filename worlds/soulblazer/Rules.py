from enum import IntEnum, auto
from BaseClasses import CollectionState
from Names import ItemName, ItemID, LairName, LairID, ChestName, ChestID

class LocationFlag(IntEnum):
    NONE = 0
    CAN_CUT_METAL = auto()
    CAN_CUT_SPIRIT = auto()
    HAS_THUNDER = auto()
    HAS_MAGIC = auto()
    NEEDS_NPC = auto()

metal_items = [ItemName.ZANTETSUSWORD, ItemName.SOULBLADE]
spirit_items = [ItemName.SPIRITSWORD, ItemName.SOULBLADE]
thunder_items = [ItemName.THUNDERRING, *metal_items]
magic_items = [ItemName.FLAMEBALL, ItemName.LIGHTARROW, ItemName.MAGICFLARE, ItemName.ROTATOR, ItemName.SPARKBOMB, ItemName.FLAMEPILLAR, ItemName.TORNADO]

def can_cut_metal(state: CollectionState, player: int) -> bool:
    return state.has_any(metal_items, player)

def can_cut_spirit(state: CollectionState, player: int) -> bool:
    return state.has_any(spirit_items, player)

def has_thunder(state: CollectionState, player: int) -> bool:
    return state.has_any(thunder_items, player)

