from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range, Toggle
  
class SizeOfCube(Choice):
    """
    Which size of cube you want to play.
    Note! This game is harder than just solving the cube!
    """

    display_name = "Size of Cube"
    option_2x2x2 = 2
    option_3x3x3 = 3
    option_4x4x4 = 4
    option_5x5x5 = 5
    default = 2
    
class StartingStickers(Range):
    """
    How many stickers you start with.
    """

    display_name = "Starting Stickers"
    range_start = 1
    range_end = 15
    default = 5

class RandomizeColorLayout(Toggle):
    """
    Whether you want to use the default color layout (off) or randomize it (on).
    """

    display_name = "Randomize color layout"
    default = 0

class MinimumStickersUnlockedPercentToGoalWhenSolved(Range):
    """
    What percentage of stickers are required to goal when the cube is solved.
    A cube is considered "solved" if all the stickers, including the locked ones, are in the correct position
    """

    display_name = "Percentage of stickers required to goal when the cube is solved"
    range_start = 0
    range_end = 100
    default = 0

@dataclass
class TwistyCubeOptions(PerGameCommonOptions):
    size_of_cube: SizeOfCube
    starting_stickers: StartingStickers
    randomize_color_layout: RandomizeColorLayout
    minimum_stickers_unlocked_percent_to_goal_when_solved: MinimumStickersUnlockedPercentToGoalWhenSolved