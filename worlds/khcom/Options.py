from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class PrioritizeBosses(DefaultOnToggle):
    """
    Toggles whether boss locations should prioritize holding progression items.
    """
    display_name = "Progression Items Prioritized to Bosses"

class PacksOrSets(Choice):
    """
    Packs contain cards that are randomized upon receipt at the lua script level
    Sets are static card sets (i.e. You received Card Set Lady Luck 4-6)
    """
    display_name = "Packs or Sets"
    option_sets   = 1
    option_packs  = 2
    default       = 1

class Zeroes(DefaultOnToggle):
    """
    Toggle whether 0 value card's should be included in the item pool.  Innefective if you are using card packs
    """
    display_name = "Zeroes"

class Cure(DefaultOnToggle):
    """
    Toggle whether Cure cards should be included in the item pool.  Innefective if you are using card packs
    """
    display_name = "Cure"

class EarlyCure(DefaultOnToggle):
    """
    Toggles whether one of the starting locations should contain Cure 4-6?
    """
    display_name = "Early Cure"

class EnemyCards(DefaultOnToggle):
    """
    Toggles whether enemy cards should be shuffled into the item pool.
    """
    display_name = "Enemy Cards"

khcom_options: Dict[str, type(Option)] = {
    "prioritize_bosses": PrioritizeBosses,
    "packs_or_sets": PacksOrSets,
    "zeroes": Zeroes,
    "cure": Cure,
    "early_cure": EarlyCure,
    "enemy_cards": EnemyCards,
}
