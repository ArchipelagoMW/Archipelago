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


class ForceNonLocal(Toggle):
    """Automatically place all Bingo calls into the non-local-items list"""
    display_name = "Force Non-Local"
    default = 1


class AdvancementItemsOnly(Toggle):
    """Restrict Bingo cards to have only advancement items"""
    display_name = "Advancement Items Only"
    default = 1


bingo_options: typing.Dict[str, type(Option)] = {
    "card_pairs": CardPairs,
    "reveal_rewards": RevealRewards,
    "force_non_local": ForceNonLocal,
    "advancement_items_only": AdvancementItemsOnly
}