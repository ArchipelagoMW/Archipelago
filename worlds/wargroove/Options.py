import typing
from Options import Choice, Option, Range, Toggle


class IncomeBoost(Range):
    """How much extra income the player gets per turn per boost received (There are 7 total boosts)."""
    display_name = "Income Boost"
    range_start = 0
    range_end = 100
    default = 25


class CODefenseBoost(Range):
    """How much extra defense the player's commander gets per boost received (There are 7 total boosts)."""
    display_name = "CO Defense Boost"
    range_start = 0
    range_end = 15
    default = 2


wargroove_options: typing.Dict[str, type(Option)] = {
    "income_boost": IncomeBoost,
    "co_defense_boost": CODefenseBoost
}
