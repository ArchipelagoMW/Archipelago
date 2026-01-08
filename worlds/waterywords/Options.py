from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

class ScoreForLastCheck(Range):
    """
    Score you need to reach to get the final check.
    THIS DETERMINES THE DIFFICULTY! 1000 is probably way to hard, 300 too easy. We will need to figure this out :)
    """

    display_name = "Score for last check"
    range_start = 160
    range_end = 777
    default = 250


class ScoreForGoal(Range):
    """
    This option determines what score you need to reach to finish the game.
    It cannot be higher than the score for the last check (if it is, this option is changed automatically).
    """

    display_name = "Score for goal"
    range_start = 160
    range_end = 777
    default = 200


class MergeItems(Toggle):
    """
    This option merges the 95 letters into 19 packs of "5 Letters"
    and merges the 45 bonus tiles into 9 packs of "5 Bonus Tiles"
    """
    display_name = "Merge items"
    default = True

@dataclass
class YachtDiceOptions(PerGameCommonOptions):
    score_for_last_check: ScoreForLastCheck
    score_for_goal: ScoreForGoal
    merge_items: MergeItems