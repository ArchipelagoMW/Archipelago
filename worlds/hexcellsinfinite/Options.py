from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in hexcells_infinite_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list


class RequirePerfectClears(Toggle):
    """
    This determines if levels need to be cleared with no mistakes to send out an item. 
    """
    display_name = "Require Perfect Clears"

class PuzzleOptions(Choice):
    """
    This determines how puzzles will be randomized.
    Vanilla: No puzzle randomization, all puzzles are as they are in the base game.
    Randomized: Every level has a randomly generated puzzle.
    True Randomized: Every level has a randomly generated puzzle, that is re-randomized if you leave the level.
    """
    display_name = "Puzzle Options"
    option_vanilla = 1
    option_randomized = 2
    option_true_randomized = 3
    default = 1


class EnableShields(Toggle):
    """
    When enabled, puzzle solves that involve mistakes will give 1 shield (max of 1 shield). Shields are used to block mistakes on future levels. This pairs well with True Randomization. 
    """
    display_name = "Enable Shields"

    
class LevelUnlockType(Choice):
    """
    This determines how levels will be unlocked.
    Vanilla: Levels are unlocked in groups of 6, with 6 groups total.
    Individual: Levels are unlocked individually, with individual gem amount requirements.
    NOT CURRENTLY IMPLEMENTED 
    """
    display_name = "Level Unlock Type"
    option_vanilla = 1
    option_individual = 2
    default = 1

class HardGeneration(Toggle):
    """
    When enabled, puzzle will be generated with harder sets. Does not affect "Vanilla" under "Puzzle Options".
    """
    display_name = "Hard Generation"

@dataclass
class HexcellsInfiniteOptions(PerGameCommonOptions):

    RequirePerfectClears:         RequirePerfectClears
    PuzzleOptions:                PuzzleOptions
    EnableShields:                EnableShields
    LevelUnlockType:              LevelUnlockType
    HardGeneration:               HardGeneration


# # This is where you organize your options
# # Its entirely up to you how you want to organize it
hexcells_infinite_option_groups: Dict[str, List[Any]] = {
    "General Options": [RequirePerfectClears, PuzzleOptions, EnableShields, LevelUnlockType, HardGeneration],

}