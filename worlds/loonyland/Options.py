from dataclasses import dataclass

from Options import Toggle, Range, Choice, PerGameCommonOptions

class WinCondition(Choice)
    display_name = "Win Condition"
    option_evilizer = 0
    option_40badges = 1
    default = 0
    
@dataclass
class LoonylandOptions(PerGameCommonOptions):
    win_condition: WinCondition