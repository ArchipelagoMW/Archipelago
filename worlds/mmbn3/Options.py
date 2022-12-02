import typing

from BaseClasses import MultiWorld
from Options import Choice, Range, Option, Toggle, DefaultOnToggle, DeathLink, TextChoice


class Goal(Choice):
    """
    Determines the goal of the seed
    Alpha: Defeat Alpha at the WWW base
    Serenade: Defeat Serenade in the Secret Area
    Alpha Omega: Defeat Alpha Omega after collecting Seven Stars [NOT RECOMMENDED. VERY LONG]
    """
    display_name = "Goal"
    option_alpha = 0
    option_serenade = 1
    option_alpha_omega = 2
    default = 0


class ExtraRanks(Range):
    """
    How many extra Undernet Ranks to add to the pool in place of filler items.
    The more ranks there are, the faster the game will go.
    Depending on your other options, you might not have enough filler items to replace.
    If generation errors occur, consider reducing this value.
    """
    display_name = "Extra Undernet Ranks"
    range_start = 0
    range_end = 16
    default = 0

class IncludeJobs(DefaultOnToggle):
    """
    Whether Jobs can be included in logic.
    """
    display_name = "Include Jobs"

# Possible logic options:
# - Include Number Trader
# - Include Secret Area
# - Overworld Item Restrictions
# - Cybermetro Locked Shortcuts


MMBN3Options = {
    "Goal": Goal,
    "ExtraRanks": ExtraRanks,
    # "JobProgression": JobProgression
    "IncludeJobs": IncludeJobs
}