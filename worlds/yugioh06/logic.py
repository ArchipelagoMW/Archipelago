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


back_row_removal = {
    "Anteatereatingant",
    "B.E.S. Tetran",
    "Breaker the Magical Warrior",
    "Calamity of the Wicked",
    "Chiron the Mage",
    "Dust Tornado",
    "Heavy Storm",
    "Mystical Space Typhoon",
    "Mobius the Frost Monarch",
    "Raigeki Break",
    "Stamping Destruction",
    "Swarm of Locusts"
}


monster_removal = {
    "Blast Sphere",
    "Exiled Force",
    "Fissure",
    "Hammer Shot",
    "Lightning Vortex",
    "Man-Eater Bug",
    "Michizure",
    "Newdoria",
    "Night Assailant",
    "Offerings to the Doomed",
    "Old Vindictive Magician",
    "Raigeki Break",
    "Sakuretsu Armor",
    "Smashing Ground",
    "Soul Taker",
    "Torrential Tribute",
    "Tribute to the Doomed",
    "Widespread Ruin",
    "Yomi Ship",
    "Zaborg the Thunder Monarch"
}
