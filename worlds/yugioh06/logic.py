from typing import List

from BaseClasses import CollectionState

core_booster: List[str] = [
    "LEGEND OF B.E.W.D.",
    "METAL RAIDERS",
    "PHARAOH'S SERVANT",
    "PHARAONIC GUARDIAN",
    "SPELL RULER",
    "LABYRINTH OF NIGHTMARE",
    "LEGACY OF DARKNESS",
    "MAGICIAN'S FORCE",
    "DARK CRISIS",
    "INVASION OF CHAOS",
    "ANCIENT SANCTUARY",
    "SOUL OF THE DUELIST",
    "RISE OF DESTINY",
    "FLAMING ETERNITY",
    "THE LOST MILLENIUM",
    "CYBERNETIC REVOLUTION",
    "ELEMENTAL ENERGY",
    "SHADOW OF INFINITY",
]


def yugioh06_difficulty(state: CollectionState, player: int, amount: int):
    return state.has_from_list(core_booster, player, amount)
