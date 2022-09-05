from typing import TypedDict
from Options import DefaultOnToggle, Range, Choice


class OC2OnToggle(DefaultOnToggle):
    @property
    def result(self) -> bool:
        return bool(self.value)


class AlwaysServeOldestOrder(OC2OnToggle):
    """Modifies the game so that serving an expired order doesn't target the ticket with the highest tip. This helps players dig out of a broken tip combo fater."""
    display_name = "Always Serve Oldest Order"


class AlwaysPreserveCookingProgress(OC2OnToggle):
    """Modifies the game to behave more like AYCE, where adding an item to an in-progress container doesn't reset the entire progress bar."""
    display_name = "Preserve Cooking/Mixing Progress"


class DisplayLeaderboardScores(OC2OnToggle):
    """Mods the Overworld map to fetch and display the current world records for each level. Press number keys 1-4 to view leaderboard scores for that number of players."""
    display_name = "Display Leaderboard Scores"


class ShuffleLevelOrder(OC2OnToggle):
    """Shuffles the order of kitchens on the overworld map. Also draws from DLC maps."""
    display_name = "Shuffle Level Order"


class FixBugs(OC2OnToggle):
    """Fixes Bugs Present in the base game: Double Serving Exploit, Sink Bug, Control Stick Cancel/Throw Bug, Can't Throw Near Empty Burner Bug"""
    display_name = "Bug Fixes"


class ShorterLevelDuration(OC2OnToggle):
    """In the interest of making seeds take less time to complete, this option shortens levels by about 1/3rd of their original duration. Points required to earn stars are scaled accordingly."""
    display_name = "ShorterLevelDuration"


class PrepLevels(Choice):
    """Choose How "Prep Levels" are landled (levels where the timer does not start until the first order is served)
    Original: Prep Levels may appear
    Excluded: Prep Levels are excluded from the pool during level shuffling
    All You Can Eat: Prep Levels may appear, but the timer automatically starts. The star score requirements are also adjusted to use the All You Can Eat World Record if it exists."""
    auto_display_name = True
    display_name = "PrepLevels"
    option_original = 0
    option_excluded = 1
    option_ayce = 2
    default = 2


class StarsToWin(Range):
    """Number of stars required to unlock 6-6. All levels between 1-1 and 6-6 will be spread between these two numbers"""
    range_start = 0
    range_end = 129
    default = 84


class StarThresholdScale(Range):
    """How difficult should the final star for each level be on a scale of 1-100%, where 100% is the world record score (Vanilla 4-Star is 45% on average)"""
    range_start = 1
    range_end = 100
    default = 55


overcooked_options = {
    "always_serve_oldest_order": AlwaysServeOldestOrder,
    "always_preserve_cooking_progress": AlwaysPreserveCookingProgress,
    "display_leaderboard_scores": DisplayLeaderboardScores,
    "shuffle_level_order": ShuffleLevelOrder,
    "fix_bugs": FixBugs,
    "stars_to_win": StarsToWin,
    "star_threshold_scale": StarThresholdScale,
    "shorter_level_duration": ShorterLevelDuration,
    "prep_levels": PrepLevels,
}

OC2Options = TypedDict("OC2Options", {option.__name__: option for option in overcooked_options.values()})
