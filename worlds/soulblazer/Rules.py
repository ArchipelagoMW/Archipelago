from typing import Callable

from enum import IntEnum, auto
from BaseClasses import CollectionState
from .Names import ItemName, ItemID, LairName, LairID, ChestName, ChestID
from .Locations import SoulBlazerLocationData

class LocationFlag(IntEnum):
    NONE = 0
    CAN_CUT_METAL = auto()
    CAN_CUT_SPIRIT = auto()
    HAS_THUNDER = auto()
    HAS_MAGIC = auto()

metal_items = [ItemName.ZANTETSUSWORD, ItemName.SOULBLADE]
spirit_items = [ItemName.SPIRITSWORD, ItemName.SOULBLADE]
thunder_items = [ItemName.THUNDERRING, *metal_items]
magic_items = [ItemName.FLAMEBALL, ItemName.LIGHTARROW, ItemName.MAGICFLARE, ItemName.ROTATOR, ItemName.SPARKBOMB, ItemName.FLAMEPILLAR, ItemName.TORNADO]

def no_requirement(state: CollectionState, player: int) -> bool:
    return True

def can_cut_metal(state: CollectionState, player: int) -> bool:
    return state.has_any(metal_items, player)

def can_cut_spirit(state: CollectionState, player: int) -> bool:
    return state.has_any(spirit_items, player)

def has_thunder(state: CollectionState, player: int) -> bool:
    return state.has_any(thunder_items, player)

def has_magic(state: CollectionState, player: int) -> bool:
    return state.has_any(magic_items, player)

rule_for_flag = {
    LocationFlag.NONE : no_requirement,
    LocationFlag.CAN_CUT_METAL : can_cut_metal,
    LocationFlag.CAN_CUT_SPIRIT : can_cut_spirit,
    LocationFlag.HAS_THUNDER : has_thunder,
    LocationFlag.HAS_MAGIC : has_magic,
    LocationFlag.NEEDS_NPC : no_requirement, # TODO: implement?
}

# Many locations depend on one or two NPC releases so rather than create regions to hold one location,
# we put these location-specific dependencies here.
# TODO: fill
location_dependencies = {

}

def get_rule_for_location(name: str, player: int, flag: LocationFlag) -> Callable[[CollectionState], bool]:
    """Returns the access rule for the given location."""

    def rule(state: CollectionState) -> bool:
        return (
            rule_for_flag[flag](state, player)
            and state.has_all(location_dependencies.get(name, []), player)
        )
    
    return rule

#TODO: access rule for region/entrance