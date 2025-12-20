from dataclasses import dataclass
from Options import PerGameCommonOptions, StartInventoryPool, Choice, AssembleOptions, OptionGroup

class EnableAdditionRandomizer(Choice):
    """
    Include Addition levels as checks. Every time you reach an addition threshold (level, uses), you will trigger another check.

    Shuffled (Character): Additions are randomized per character but only on that character.
    Shuffled (Party): Addition unlocks are shuffled between all characters in the party.

    Progressive (Character): Additions are considered items to be added to the randomized pool and can be placed in other games.
    """
    display_name = "Enable Addition Randomization"
    option_off = 0
    option_shuffled_character = 1
    option_shuffled_party = 2
    option_progressive_character = 3
    default = 0

class CompletionCondition(Choice):
    """
    Set the goal for completing the game.

    """
    display_name = "Completion Condition"
    option_stardust_count_25 = 0
    option_stardust_count_50 = 1 # collect all stardust in the game
    option_lavitz =  2# goal after lavitz death
    option_doel = 3 # goal after defeating dragoon doel
    option_lenus2 = 4# goal after defeating lenus w/ regole
    option_faust =  5 # goal after defeating Magician Faust
    option_melbu =  6 # goal after defeating Melbu Frahma
    default = 0


@dataclass
class LegendOfDragoonOptions(PerGameCommonOptions):
    enable_addition_randomizer: EnableAdditionRandomizer
    lod_completion_condition: CompletionCondition

lod_option_groups = [
    OptionGroup("General", [
        EnableAdditionRandomizer,
        CompletionCondition,
    ], False)
]