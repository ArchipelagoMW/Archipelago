from typing import TypedDict
from Options import DefaultOnToggle, Range, Choice


class OC2OnToggle(DefaultOnToggle):
    @property
    def result(self) -> bool:
        return bool(self.value)


class AlwaysServeOldestOrder(OC2OnToggle):
    """Modifies the game so that serving an expired order doesn't target the ticket with the highest tip. This helps
    players dig out of a broken tip combo faster."""
    display_name = "Always Serve Oldest Order"


class AlwaysPreserveCookingProgress(OC2OnToggle):
    """Modifies the game to behave more like AYCE, where adding an item to an in-progress container doesn't reset the
    entire progress bar."""
    display_name = "Preserve Cooking/Mixing Progress"


class DisplayLeaderboardScores(OC2OnToggle):
    """Modifies the Overworld map to fetch and display the current world records for each level. Press number keys 1-4
    to view leaderboard scores for that number of players."""
    display_name = "Display Leaderboard Scores"


class ShuffleLevelOrder(OC2OnToggle):
    """Shuffles the order of kitchens on the overworld map. Also draws from DLC maps."""
    display_name = "Shuffle Level Order"


class IncludeHordeLevels(OC2OnToggle):
    """Includes "Horde Defence" levels in the pool of possible kitchens when Shuffle Level Order is enabled. Also adds
    two horde-specific items into the item pool."""
    display_name = "Include Horde Levels"


class KevinLevels(OC2OnToggle):
    """Includes the 8 Kevin level locations on the map as unlockables. Turn off to make games shorter."""
    display_name = "Kevin Level Checks"


class FixBugs(OC2OnToggle):
    """Fixes Bugs Present in the base game:
    - Double Serving Exploit
    - Sink Bug
    - Control Stick Cancel/Throw Bug
    - Can't Throw Near Empty Burner Bug"""
    display_name = "Fix Bugs"


class ShorterLevelDuration(OC2OnToggle):
    """Modifies level duration to be about 1/3rd shorter than in the original game, thus bringing the item discovery
    pace in line with other popular Archipelago games.
    
    Points required to earn stars are scaled accordingly. ("Boss Levels" which change scenery mid-game are not
    affected.)"""
    display_name = "Shorter Level Duration"


class PrepLevels(Choice):
    """Choose How "Prep Levels" are handled (levels where the timer does not start until the first order is served):

    - Original: Prep Levels may appear

    - Excluded: Prep Levels are excluded from the pool during level shuffling

    - All You Can Eat: Prep Levels may appear, but the timer automatically starts. The star score requirements are also
    adjusted to use the All You Can Eat World Record (if it exists)"""
    auto_display_name = True
    display_name = "Prep Level Behavior"
    option_original = 0
    option_excluded = 1
    option_all_you_can_eat = 2
    default = 1


class StarsToWin(Range):
    """Number of stars required to unlock 6-6.

    Level purchase requirements between 1-1 and 6-6 will be spread between these two numbers. Using too high of a number
    may result in more frequent generation failures, especially when horde levels are enabled."""
    display_name = "Stars to Win"
    range_start = 0
    range_end = 100
    default = 66


class StarThresholdScale(Range):
    """How difficult should the third star for each level be on a scale of 1-100%, where 100% is the current world
    record score and 45% is the average vanilla 4-star score."""
    display_name = "Star Difficulty %"
    range_start = 1
    range_end = 100
    default = 45


overcooked_options = {
    # randomization options
    "shuffle_level_order": ShuffleLevelOrder,
    "include_horde_levels": IncludeHordeLevels,
    "prep_levels": PrepLevels,
    "kevin_levels": KevinLevels,

    # quality of life options
    "fix_bugs": FixBugs,
    "shorter_level_duration": ShorterLevelDuration,
    "always_preserve_cooking_progress": AlwaysPreserveCookingProgress,
    "always_serve_oldest_order": AlwaysServeOldestOrder,
    "display_leaderboard_scores": DisplayLeaderboardScores,

    # difficulty settings
    "stars_to_win": StarsToWin,
    "star_threshold_scale": StarThresholdScale,
}

OC2Options = TypedDict("OC2Options", {option.__name__: option for option in overcooked_options.values()})
