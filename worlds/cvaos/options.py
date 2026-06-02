"""
Options for the Castlevania: Aria of Sorrow randomizer.
"""

from dataclasses import dataclass
from Options import Choice, ItemsAccessibility, PerGameCommonOptions, Toggle

class RandomizePickups(Toggle):
    """
    Adds on-ground, single-obtainance pickups to the pool.
    """
    display_name = "Randomize Pickups"
    default = 1


class Goal(Choice):
    """
    The win condition.

    - chaos: defeat Chaos. Requires reaching the Flame Demon
      and Succubus enemies (whose souls are needed) plus the Giant Bat soul, then reaching
      Graham.
    - graham: defeat Graham (the bad-ending final boss). Requires reaching Graham
    """
    display_name = "Goal"
    option_chaos = 0
    option_graham = 1
    default = option_chaos


@dataclass
class CVAOSOptions(PerGameCommonOptions):
    """Options for the Castlevania: Aria of Sorrow randomizer."""
    accessibility: ItemsAccessibility
    randomize_pickups: RandomizePickups
    goal: Goal
