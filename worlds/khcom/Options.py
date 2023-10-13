from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class BattleCards(Toggle):
    """
    Determines if collecting specific battle cards should yield any progression items
    """
    display_name = "Battle Cards Yield Progression Items"

khcom_options: Dict[str, type(Option)] = {
    "battle_cards": BattleCards
}
