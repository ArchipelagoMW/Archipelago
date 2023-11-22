from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class PrioritizeBosses(DefaultOnToggle):
    """
    Should boss location prioritize holding progression items?
    """
    display_name = "Progression Items Prioritized to Bosses"

class PacksOrSets(Choice):
    """
    Packs contain cards that are randomized upon receipt at the lua script level
    Sets are static card sets (i.e. You received Lady Luck 4-6)
    """
    display_name = "Packs or Sets"
    option_sets   = 1
    option_packs  = 2
    default       = 1

class Zeroes(DefaultOnToggle):
    """
    Toggle whether 0's should be included.  Does nothing if you are using card packs
    """
    display_name = "Zeroes"

class Cure(DefaultOnToggle):
    """
    Toggle whether Cure cards should be included.  Does nothing if you are using card packs
    """
    display_name = "Cure"

class EarlyCure(DefaultOnToggle):
    """
    Should one of the starting checks contain Cure 4-6?
    """
    display_name = "Early Cure"

class EnemyCards(DefaultOnToggle):
    """
    Should enemy cards be shuffled into the pool?
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
