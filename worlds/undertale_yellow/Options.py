from Options import Choice, Toggle, Range, PerGameCommonOptions
from dataclasses import dataclass

class GoalRoute(Choice):
    """Route needed to goal"""
    display_name = "Goal Route"
    option_neutral = 1
    option_pacifist = 2
    option_genocide = 3
    option_all = 4
    default = 1

class StartingArea(Choice):
    """Area you start with a key for."""
    display_name = "Starting Area"
    option_ruins = 0
    option_snowdin = 1
    option_dunes = 2
    option_steamworks = 3
    default = 0

class ProgressiveArmor(Toggle):
    """Makes the armor progressive."""
    display_name = "Progressive Armor"
    default = 0


class ProgressiveAmmo(Toggle):
    """Makes the ammo progressive."""
    display_name = "Progressive Ammo"
    default = 0

@dataclass
class UndertaleYellowOptions(PerGameCommonOptions):
    goal_route:                               Goal Route
    starting_area:                            StartingArea
    prog_armor:                               ProgressiveArmor
    prog_ammo:                                ProgressiveAmmo
