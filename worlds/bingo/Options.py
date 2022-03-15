import typing
from Options import Choice, Option, Toggle, Range, OptionList, DeathLink, OptionSet


class BingoMode(Choice):
    """any_line: each card has only one reward, granted when the first full line is completed.
    every_line: each card has 12 rewards, one for each line completed."""
    display_name = "Bingo Mode"
    option_any_line = 0
    option_every_line = 1
    default = 1


class NumberOfRewards(Range):
    """Number of Bingo rewards. If using Every Line mode, this will be rounded to the nearest 12"""
    display_name = "Number of Rewards"
    range_start = 24
    range_end = 960
    default = 24


class AllowUnusedCalls(Toggle):
    """Allows some calls to not appear on any cards and will be flagged as junk items"""
    display_name = "Allow Unused Calls"
    default = 1


class DisallowBingoCalls(Toggle):
    """Disallow Bingo calls, including from other Bingo games, as this game's Bingo rewards"""
    display_name = "Disallow Bingo calls on Bingo cards"
    default = 1


class ForcedAdvancement(Toggle):
    """Prioritize all bingo rewards for advancement items"""
    display_name = "Priority Rewards"
    default = 0


class ItemBlacklist(OptionSet):
    """Add items to this list to blacklist them from being rewards"""
    display_name = "Priority reward item Blacklist"
    default = {}


class AutoHint(Toggle):
    """Automatically add hints for Bingo Calls on lines when the reward on that line is hinted for.
    Does not work if any_line mode is used. Disables hint points for this game so you cannot manually hint."""
    default = 1

bingo_options: typing.Dict[str, type(Option)] = {
    "bingo_mode": BingoMode,
    "number_of_rewards": NumberOfRewards,
    "allow_unused_calls": AllowUnusedCalls,
    "disallow_bingo_calls": DisallowBingoCalls,
    "priority_rewards": ForcedAdvancement,
    "item_blacklist": ItemBlacklist,
    "auto_hint": AutoHint
}
