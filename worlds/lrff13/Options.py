from typing import Dict
from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions

class UltimateLair(Toggle):
    """Include the Ultimate Lair dungeon checks for progression."""
    display_name = "Ultimate Lair"
    default = False

class Superbosses(Toggle):
    """Allow superboss related checks to be included in progression."""
    display_name = "Super Bosses"
    default = False

class CanvasOfPrayers(Toggle):
    """Allow Canvas of Prayers related checks to be included in progression."""
    display_name = "Canvas of Prayers"
    default = False

class Grindy(Toggle):
    """Allow 20+ Soul Seeds and 10+ Unappraised items checks to be included in progression."""
    display_name = "Grindy Soul Seeds/Unappraised"
    default = False

class ShuffleTeleport(Toggle):
    """Allow Teleport to be shuffled into the item pool."""
    display_name = "Shuffle Teleport"
    default = False

class ShuffleEscape(Toggle):
    """Allow Escape to be shuffled into the item pool."""
    display_name = "Shuffle Escape"
    default = False

class ShuffleChronostasis(Toggle):
    """Allow Chronostasis to be shuffled into the item pool."""
    display_name = "Shuffle Chronostasis"
    default = False

class ShuffleCuraga(Toggle):
    """Allow Curaga to be shuffled into the item pool."""
    display_name = "Shuffle Curaga"
    default = False

class ShuffleArise(Toggle):
    """Allow Arise to be shuffled into the item pool."""
    display_name = "Shuffle Arise"
    default = True

class ShuffleEsunada(Toggle):
    """Allow Esunada to be shuffled into the item pool."""
    display_name = "Shuffle Esunada"
    default = True

class ShuffleQuake(Toggle):
    """Allow Quake to be shuffled into the item pool."""
    display_name = "Shuffle Quake"
    default = True

class ShuffleDecoy(Toggle):
    """Allow Decoy to be shuffled into the item pool."""
    display_name = "Shuffle Decoy"
    default = True

class ShuffleArmyOfOne(Toggle):
    """Allow Army of One to be shuffled into the item pool."""
    display_name = "Shuffle Army of One"
    default = True

class AllowDLCItems(Toggle):
    """Allow DLC items to be shuffled into the item pool."""
    display_name = "Allow DLC Items"
    default = False

@dataclass
class LRFF13GameOptions(PerGameCommonOptions):
    ultimate_lair: UltimateLair
    superbosses: Superbosses
    canvas_of_prayers: CanvasOfPrayers
    grindy: Grindy
    shuffle_teleport: ShuffleTeleport
    shuffle_escape: ShuffleEscape
    shuffle_chronostasis: ShuffleChronostasis
    shuffle_curaga: ShuffleCuraga
    shuffle_arise: ShuffleArise
    shuffle_esunada: ShuffleEsunada
    shuffle_quake: ShuffleQuake
    shuffle_decoy: ShuffleDecoy
    shuffle_army_of_one: ShuffleArmyOfOne
    allow_dlc_items: AllowDLCItems