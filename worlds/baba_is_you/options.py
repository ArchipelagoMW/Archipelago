from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class Goal(Choice):
    """
    Determines the requirements to beat the game.
    end: Reach the normal ending in "A Way Out?".
    flower: Reach the area "???".
    depths: Reach the area "Depths".
    meta: Reach the area "Meta".
    done: Reach the secret ending in "The End".
    levels: Win a specified amount of levels.
    blossoms: Collect a specified amount of blossoms.

    NOTICE: Only "end", "flower", "levels", and "blossoms" are implemented at this time. Do not select the other options.
    """

    display_name = "Goal"
    option_end = 0
    option_flower = 1
    option_depths = 2
    option_meta = 3
    option_done = 4
    option_levels = 5
    option_blossoms = 6
    default = 0

class GoalLevels(Range):
    """
    Determines how many levels need to be won when the goal is set to "levels".
    160 requires every level in the early game. 231 requires all levels.
    """

    display_name = "Goal Levels"
    range_start = 0
    range_end = 231
    default = 80 # 160 total before top gate

class GoalBlossoms(Range):
    """
    Determines how many blossoms need to be obtained when the goal is set to "blossoms".
    """

    display_name = "Goal Blossoms"
    range_start = 0
    range_end = 12
    default = 7

class LogicDifficulty(Choice):
    """
    Determines the logic difficulty for levels.
    easy: All interactable words are expected to complete a level.
    normal: Only the necessary words will be expected to complete a level. You may have to use alternative solutions.
    hard: Like normal, but also includes very difficult solutions, some of which require advanced techniques like parsing bugs and object priority.
    """

    display_name = "Logic Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1

class StartWithDefaultWords(DefaultOnToggle):
    """
    Start with the 9 words that appear in the level "Baba Is You".
    Disabling this will lead to an extremely restrictive start, especially if Shuffle Levels (unimplemented) is disabled.
    This will also fail to generate if Shuffle Levels is off and this is a solo game.
    As such, it is recommended to add a few starting items if this is disabled.
    """

    display_name = "Start With Default Words"

class OpenMap(DefaultOnToggle):
    """
    All levels and worlds on the Map will be open immediately, with the exception of areas behind gates.
    """
    
    display_name = "Open Map"

class WorldKeys(DefaultOnToggle):
    """
    All subworlds (worlds on the Map, and "ABC" in ???) will require their respective Key item to access.
    """

    display_name = "World Keys"

class AreaAccess(Choice):
    """
    Determines which areas of the game will be accessible when the goal is set to "end", "levels", or "blossoms".
    All other goal options will override this option.
    early: The Map and its subworlds will be accessible, but the top gate will be blocked off, preventing access to Slideshow and beyond.
    map: The Map and its subworlds will be fully accessible. ??? will be accessible, but not the levels within.
    flower: Map, ???, and their subworlds will be accessible. Depths will be accessible, but not the levels within.
    depths: Map, ???, Depths, and their subworlds will be accessible. Meta will be accessible, but not the levels within.
    meta: All areas other than "Center" and its two levels will be accessible.
    full: All areas will be accessible.

    NOTICE: Only "early" is implemented at this time. Do not select the other options.
    """

    display_name = "Accessible Areas"
    option_early = 0
    option_map = 1
    option_flower = 2
    option_depths = 3
    option_meta = 4
    option_full = 5
    default = 0

class ExcludeWhoa(DefaultOnToggle):
    """
    Excludes the level "Whoa" from logic and level shuffle.
    Only applies if Meta and its levels are accessible.
    """

    display_name = "Exclude Whoa"

class ExcludeGallery(DefaultOnToggle):
    """
    Excludes the level "Gallery" from logic.
    When disabled, the 3 Bonus items will become progression items.
    Only applies if Center and its levels are accessible.
    """

    display_name = "Exclude Gallery"

class ExcludeMazeTransform(DefaultOnToggle):
    """
    Excludes transformations for "Ultimate Maze" from logic.
    This removes some locations if Transformsanity is enabled.
    This does NOT remove the 4 "Write" levels from logic, as those can be accessed regardless.
    Only applies if ??? and its levels are accessible.
    """

    display_name = "Exclude Ultimate Maze Transform"

class BlossomPetals(Range):
    """
    Determines how many Blossom Petals are in the item pool.
    Each Blossom Petal is worth 1/8 of a Blossom.
    """

    display_name = "Blossom Petals"
    range_start = 0
    range_end = 96
    default = 0

class Blossoms(Range):
    """
    Determines how many Blossoms are in the item pool.
    """

    display_name = "Blossoms"
    range_start = 0
    range_end = 12
    default = 12

class FirstGateBlossoms(Range):
    """
    Determines how many Blossoms are needed to open the first gate on the map.
    This gate blocks access to "A Way Out?".
    """

    display_name = "First Gate Blossoms"
    range_start = 0
    range_end = 12
    default = 3

class SecondGateBlossoms(Range):
    """
    Determines how many Blossoms are needed to open the second gate on the map.
    This gate blocks access to "Volcanic Cavern" and "Mountain".
    """

    display_name = "Second Gate Blossoms"
    range_start = 0
    range_end = 12
    default = 5

class ThirdGateBlossoms(Range):
    """
    Determines how many Blossoms are needed to open the third gate on the map.
    This gate blocks access to levels 8, 9, and 10 on the map, as well as "???" and beyond.
    Not applicable if area access is set to "early".
    """

    display_name = "Third Gate Blossoms"
    range_start = 0
    range_end = 12
    default = 7

class CompleteChecks(Toggle):
    """
    Adds checks for completing a world (completing all levels within that world)
    """

    display_name = "Complete Checks"

class Transformsanity(Toggle):
    """
    Adds checks for every possible individual transformation for a level.
    For example, "Fragile Existence" would have 4 additional checks, for transforming into "Baba", "Key", "Door", or "Wall".
    Not applicable if area access is set to "early".
    """

    display_name = "Transformsanity"

class LevelShuffle(Choice):
    """
    Swaps normal levels with other normal levels.
    Levels with transformations, as well as "A Way Out?", "The Box", "The End", and "Gallery", will never be shuffled.
    disabled: Levels will not be shuffled (default).
    limited: Only levels within accessible areas will be shuffled.
    full: All levels will be shuffled, minus the exceptions listed above.

    NOTICE: Since only the early game has been implemented, both "limited" and "full" act the same.
    """

    display_name = "Shuffle Levels"
    option_disabled = 0
    option_limited = 1
    option_full = 2
    default = 0


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class BabaIsYouOptions(PerGameCommonOptions):
    goal: Goal
    goal_levels: GoalLevels
    goal_blossoms: GoalBlossoms
    logic_difficulty: LogicDifficulty
    start_with_default_words: StartWithDefaultWords
    open_map: OpenMap
    world_keys: WorldKeys
    area_access: AreaAccess
    exclude_whoa: ExcludeWhoa
    exclude_gallery: ExcludeGallery
    exclude_maze_transform: ExcludeMazeTransform
    blossom_petals: BlossomPetals
    blossoms: Blossoms
    first_gate_blossoms: FirstGateBlossoms
    second_gate_blossoms: SecondGateBlossoms
    third_gate_blossoms: ThirdGateBlossoms
    complete_checks: CompleteChecks
    transformsanity: Transformsanity
    level_shuffle: LevelShuffle