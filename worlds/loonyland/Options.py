from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions


class WinCondition(Choice):
    """Evilizer: Beat the final boss
    NOT IMPLEMENTED: 40 badges: get all 40 badge locs
    NOT IMPLEMENTED: normal_remix: Beat the final boss in normal and remix"""

    display_name = "Win Condition"
    option_evilizer = 0
    option_40badges = 1
    option_normal_remix = 2
    default = 0

class Difficulty(Choice):
    """Difficulty Setting"""
    display_name = "Difficulty"
    option_beginner = 0
    option_normal = 1
    option_hard = 2
    option_challenge = 3
    option_mad = 4
    option_loony = 5
    default = 2


@dataclass
class LoonylandOptions(PerGameCommonOptions):
    win_condition: WinCondition
    difficulty: Difficulty

