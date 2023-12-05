from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class PrioritizeBosses(DefaultOnToggle):
    """
    Should boss location prioritize holding progression items?
    """
    display_name = "Progression Items Prioritized to Bosses"

class Zeroes(DefaultOnToggle):
    """
    Toggle whether 0's should be included
    """
    display_name = "Zeroes"

class Cure(DefaultOnToggle):
    """
    Toggle whether Cure cards should be included
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

khrecom_options: Dict[str, type(Option)] = {
    "prioritize_bosses": PrioritizeBosses,
    "zeroes": Zeroes,
    "cure": Cure,
    "early_cure": EarlyCure,
    "enemy_cards": EnemyCards,
}
