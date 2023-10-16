from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class EnemyCards(Toggle):
    """
    Should progression checks be included for enemy cards?
    """
    display_name = "Enemy Cards Checks Hold Progression"

khcom_options: Dict[str, type(Option)] = {
    "enemy_cards": EnemyCards
}
