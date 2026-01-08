"""Includes utility functions for plandomizer support."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Plandomizer import PlandoItems, PlandoItemToItemMap
from randomizer.Enums.Transitions import Transitions
from randomizer.Lists.Item import ItemList

# This dict only contains names for plando items that don't map 1:1 to Item.
plandoItemNameDict = {
    PlandoItems.ProgressiveSlam: "Progressive Slam",
    PlandoItems.ProgressiveAmmoBelt: "Progressive Ammo Belt",
    PlandoItems.ProgressiveInstrumentUpgrade: "Progressive Instrument Upgrade",
    PlandoItems.DonkeyBlueprint: "Blueprint (Donkey)",
    PlandoItems.DiddyBlueprint: "Blueprint (Diddy)",
    PlandoItems.LankyBlueprint: "Blueprint (Lanky)",
    PlandoItems.TinyBlueprint: "Blueprint (Tiny)",
    PlandoItems.ChunkyBlueprint: "Blueprint (Chunky)",
    PlandoItems.JunkItem: "Junk Item",
}


def GetNameFromPlandoItem(plandoItem: PlandoItems) -> str:
    """Obtain a display name for a given PlandoItem enum."""
    if plandoItem in plandoItemNameDict:
        return plandoItemNameDict[plandoItem]
    mappedItem = PlandoItemToItemMap[plandoItem]
    return ItemList[mappedItem].name


# A dictionary that maps plando options to enum classes. The key for each enum
# must exactly match that of the associated HTML input.
PlandoEnumMap = {
    "plando_starting_exit": Transitions,
    "plando_starting_kongs_selected": Kongs,
    "plando_kong_rescue_donkey": Kongs,
    "plando_kong_rescue_diddy": Kongs,
    "plando_kong_rescue_lanky": Kongs,
    "plando_kong_rescue_tiny": Kongs,
    "plando_kong_rescue_chunky": Kongs,
    "plando_starting_moves_selected": PlandoItems,
    "plando_level_order_0": Levels,
    "plando_level_order_1": Levels,
    "plando_level_order_2": Levels,
    "plando_level_order_3": Levels,
    "plando_level_order_4": Levels,
    "plando_level_order_5": Levels,
    "plando_level_order_6": Levels,
    "plando_level_order_7": Levels,
    "plando_krool_order_0": Maps,
    "plando_krool_order_1": Maps,
    "plando_krool_order_2": Maps,
    "plando_krool_order_3": Maps,
    "plando_krool_order_4": Maps,
    "plando_boss_order_0": Maps,
    "plando_boss_order_1": Maps,
    "plando_boss_order_2": Maps,
    "plando_boss_order_3": Maps,
    "plando_boss_order_4": Maps,
    "plando_boss_order_5": Maps,
    "plando_boss_order_6": Maps,
    "plando_boss_kong_0": Kongs,
    "plando_boss_kong_1": Kongs,
    "plando_boss_kong_2": Kongs,
    "plando_boss_kong_3": Kongs,
    "plando_boss_kong_4": Kongs,
    "plando_boss_kong_5": Kongs,
    "plando_boss_kong_6": Kongs,
    "plando_helm_order_0": Kongs,
    "plando_helm_order_1": Kongs,
    "plando_helm_order_2": Kongs,
    "plando_helm_order_3": Kongs,
    "plando_helm_order_4": Kongs,
}
