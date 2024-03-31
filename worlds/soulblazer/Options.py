from dataclasses import dataclass
from Options import Toggle, Range, Choice, PerGameCommonOptions

class StartingSword(Choice):
    """
    Determines the sword you will get in the first chest.
    Vanilla: You will get the Sword of Life.
    Randomized: You will get a random sword.
    """
    display_name = "Starting Sword"
    option_vanilla = 0
    option_randomized = 1
    default = 0
    pass

# TODO: Create/implement option for modifying Gem/Exp values

# TODO: Delete these
class Difficulty(Choice):
    """Sets overall game difficulty."""
    display_name = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    alias_beginner = 0  # same as easy
    alias_expert = 2  # same as hard
    default = 1  # default to normal


class FinalBossHP(Range):
    """Sets the HP of the final boss"""
    display_name = "Final Boss HP"
    range_start = 100
    range_end = 10000
    default = 2000


class FixXYZGlitch(Toggle):
    """Fixes ABC when you do XYZ"""
    display_name = "Fix XYZ Glitch"


# By convention, we call the options dataclass `<world>Options`.
# It has to be derived from 'PerGameCommonOptions'.
@dataclass
class SoulBlazerOptions(PerGameCommonOptions):
    starting_sword: StartingSword
    #difficulty: Difficulty
    #final_boss_hp: FinalBossHP
    #fix_xyz_glitch: FixXYZGlitch
