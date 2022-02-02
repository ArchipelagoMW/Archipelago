import typing
from Options import Choice, Option, Toggle, Range, OptionList, DeathLink, OptionSet


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


class ForcedAdvancementHorizontal(Toggle):
    """Force all horizontal line rewards to be advancement items"""
    display_name = "Horizontal Line Priority Rewards"
    default = 0


class ForcedAdvancementVertical(Toggle):
    """Force all vertical line rewards to be advancement items"""
    display_name = "vertical Line Priority Rewards"
    default = 0


class ForcedAdvancementDiagonal(Toggle):
    """Force all diagonal line rewards to be advancement items"""
    display_name = "Diagonal Line Priority Rewards"
    default = 0


class PriorityRewardItemBlacklist(OptionSet):
    """Add items to this list to blacklist them from being Bingo rewards for lines set to be forced advancement items"""
    display_name = "Priority reward item Blacklist"
    default = {"Gold Skulltula Token"}


class RewardItemBlacklist(OptionSet):
    """Add items to this list to blacklist them from being any Bingo rewards"""
    display_name = "General reward item Blacklist"
    default = {}

bingo_options: typing.Dict[str, type(Option)] = {
    "card_pairs": CardPairs,
    "reveal_rewards": RevealRewards,
    "disallow_bingo_calls": DisallowBingoCalls,
    "priority_rewards_horizontal": ForcedAdvancementHorizontal,
    "priority_rewards_vertical": ForcedAdvancementVertical,
    "priority_rewards_diagonal": ForcedAdvancementDiagonal,
    "priority_reward_item_blacklist": PriorityRewardItemBlacklist,
    "reward_item_blacklist": RewardItemBlacklist
}
