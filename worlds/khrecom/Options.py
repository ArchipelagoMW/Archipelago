from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class Zeroes(DefaultOnToggle):
    """
    Toggle whether 0 value cards should be included in the item pool.
    """
    display_name = "Zeroes"

class Cure(DefaultOnToggle):
    """
    Toggle whether Cure cards should be included in the item pool.
    """
    display_name = "Cure"

class EarlyCure(DefaultOnToggle):
    """
    Toggle whether one of the starting checks should include Cure 4-6
    """
    display_name = "Early Cure"

class EnemyCards(DefaultOnToggle):
    """
    Toggle whether Enemy Cards should be included in the item pool.
    """
    display_name = "Enemy Cards"

class DaysItems(Toggle):
    """
    Toggle whether items not available to the player until they watch 358/2 Days are included in the item pool.
    """
    display_name = "Days Items"

class DaysLocations(Toggle):
    """
    Toggle whether locations not available to the player until they watch 358/2 Days are included in the locations list.
    """
    display_name = "Days Locations"

khrecom_options: Dict[str, type(Option)] = {
    "zeroes": Zeroes,
    "cure": Cure,
    "early_cure": EarlyCure,
    "enemy_cards": EnemyCards,
    "days_items": DaysItems,
    "days_locations": DaysLocations,
}
