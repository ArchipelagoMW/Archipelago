import typing
from Options import Choice, Option, Toggle, Range, OptionList, DeathLink, OptionSet


class CardPairs(Range):
    """How many pairs of Bingo cards."""
    display_name = "Card Pairs"
    range_start = 1
    range_end = 40
    default = 2


class MinimumOccurrences(Range):
    """Minimum occurrences of each Bingo Call. If 2, there will be exactly 2 of each Bingo Call.
    If 0, there may be Bingo Calls which do not appear on any cards, rendering them useless"""
    display_name = "Minimum Occurrences"
    range_start = 0
    range_end = 2
    default = 2

class RevealRewards(Toggle):
    """Start with all Bingo rewards hinted."""
    display_name = "Reveal Rewards"
    default = 0


class DisallowBingoCalls(Toggle):
    """Disallow Bingo calls, including from other Bingo games, as this game's Bingo rewards"""
    display_name = "Disallow Bingo calls on Bingo cards"
    default = 1


class ForcedAdvancementHorizontal(Toggle):
    """Prioritize all horizontal line rewards for advancement items"""
    display_name = "Horizontal Line Priority Rewards"
    default = 0


class ForcedAdvancementVertical(Toggle):
    """Prioritize all vertical line rewards for advancement items"""
    display_name = "vertical Line Priority Rewards"
    default = 0


class ForcedAdvancementDiagonal(Toggle):
    """Prioritize all diagonal line rewards for advancement items"""
    display_name = "Diagonal Line Priority Rewards"
    default = 0


class PriorityRewardItemBlacklist(OptionSet):
    """Add items to this list to blacklist them from being rewards for lines prioritized for forced advancement items"""
    display_name = "Priority reward item Blacklist"
    default = {"Gold Skulltula Token"}


bingo_options: typing.Dict[str, type(Option)] = {
    "card_pairs": CardPairs,
    "bingo_call_minimum_occurrences": MinimumOccurrences,
    "reveal_rewards": RevealRewards,
    "disallow_bingo_calls": DisallowBingoCalls,
    "priority_rewards_horizontal": ForcedAdvancementHorizontal,
    "priority_rewards_vertical": ForcedAdvancementVertical,
    "priority_rewards_diagonal": ForcedAdvancementDiagonal,
    "priority_reward_item_blacklist": PriorityRewardItemBlacklist,
}
