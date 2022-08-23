import typing
from Options import Option, DefaultOnToggle, Range, Toggle, Choice


class AlwaysServerOldestOrder(DefaultOnToggle):
    """Modifies the game so that serving an expired order doesn't target the ticket with the highest tip. This helps players dig out of a broken tip combo fater."""
    display_name = "Always Serve Oldest Order"


class AlwaysPreserveCookingProgress(DefaultOnToggle):
    """Modifies the game to behave more like AYCE, where adding an item to an in-progress container doesn't reset the entire progress bar."""
    display_name = "Preserve Cooking/Mixing Progress"


class AlwaysStartLevelTimer(DefaultOnToggle):
    """Modifies the game to behave more like AYCE, where levels that introduce new recipes do not start with a paused timer."""
    display_name = "Level Timer Always Starts"


class DisplayLeaderboardScores(DefaultOnToggle):
    """Mods the Overworld map to fetch and display the current world records for each level. Press number keys 1-4 to view leaderboard scores for that number of players."""
    display_name = "Display Leaderboard Scores"


class ShuffleLevelOrder(DefaultOnToggle):
    """Shuffles the order of kitchens on the overworld map. Also draws from DLC maps."""
    display_name = "Shuffle Level Order"


class FixBugs(DefaultOnToggle):
    """Fixes Bugs Present in the base game: Double Serving Exploit, Sink Bug, Control Stick Cancel/Throw Bug, Can't Throw Near Empty Burner Bug"""
    display_name = "Bug Fixes"


class StarsToWin(Range):
    """Number of stars required to unlock 6-6. All levels between 1-1 and 6-6 will be spread between these two numbers"""
    range_start = 0
    range_end = 105
    default = 50


class StarThresholdScale(Range):
    """How difficult should the final star for each level be on a scale of 1-100, where 100 is the world record score (Vanilla 4-Star is 45 on average)"""
    range_start = 1
    range_end = 100
    default = 30


overcooked_options = {
    "AlwaysServerOldestOrder": AlwaysServerOldestOrder,
    "AlwaysPreserveCookingProgress": AlwaysPreserveCookingProgress,
    "AlwaysStartLevelTimer": AlwaysStartLevelTimer,
    "DisplayLeaderboardScores": DisplayLeaderboardScores,
    "ShuffleLevelOrder": ShuffleLevelOrder,
    "FixBugs": FixBugs,
    "StarsToWin": StarsToWin,
    "StarThresholdScale": StarThresholdScale,
}
