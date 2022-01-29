import typing
from Options import Choice, Option, Toggle, Range, OptionList, DeathLink


class CardPairs(Range):
    """How many pairs of Bingo cards."""
    display_name = "Card Pairs"
    range_start = 1
    range_end = 4
    default = 4


class RevealRewards(Toggle):
    """Start with all Bingo rewards hinted."""
    display_name = "Reveal Rewards"
    default = 0


class DisallowBingoCalls(Toggle):
    """Disallow Bingo calls, including from other Bingo games, as this game's Bingo rewards"""
    display_name = "Disallow Bingo calls on Bingo cards"
    default = 1


class ForcedAdvancement(Range):
    """Percentage of Bingo rewards to be prioritized for advancement items."""
    display_name = "Advancement Items Prioritization"
    range_start = 0
    range_end = 100
    default = 0


bingo_options: typing.Dict[str, type(Option)] = {
    "card_pairs": CardPairs,
    "reveal_rewards": RevealRewards,
    "disallow_bingo_calls": DisallowBingoCalls,
    "priority_rewards": ForcedAdvancement
}