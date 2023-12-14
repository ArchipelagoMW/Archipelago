from dataclasses import dataclass
from Options import Toggle, Range, Choice, DeathLink, PerGameCommonOptions

class WinGoal(Choice):
    """What boss(es) need to be killed for victory? None will result in there being no goal."""
    display_name = "Goal"
    option_none = 0
    option_fuel_weaver = 1
    option_alter_guardian = 2
    option_either = 3
    option_both = 4
    default = 3
    
# class KillCount(Range):
#     """How many unique kills should be a requirement for winning in addition to the Goal
#     0 = Disabled"""
#     display_name = ""
#     range_start = 0
#     range_end = 100
#     default = 50

# By convention, we call the options dataclass `<world>Options`.
# It has to be derived from 'PerGameCommonOptions'.
@dataclass
class DSTOptions(PerGameCommonOptions):
    bosses: WinGoal
    # killcount: KillCount
    death_link: DeathLink