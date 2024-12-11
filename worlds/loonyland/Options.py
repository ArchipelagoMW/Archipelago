from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions


class WinCondition(Choice):
    """Sets Win Condition."""
    display_name = "Win Condition"
    option_evilizer = 0
    option_40badges = 1
    default = 0


@dataclass
class LoonylandOptions(PerGameCommonOptions):
    win_condition: WinCondition
