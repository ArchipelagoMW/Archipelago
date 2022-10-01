import typing

from BaseClasses import MultiWorld
from Options import Choice, Range, Option, Toggle, DefaultOnToggle, DeathLink, TextChoice

class Goal(Choice):
    """
    Determines the goal of the seed
    Alpha: Defeat Alpha at the WWW base
    Serenade: Defeat Serenade in the Secret Area
    Alpha Omega: Defeat Alpha Omega after collecting Seven Stars [NOT RECOMMENDED. VERY LONG]
    """
    display_name = "Goal"
    option_alpha = 0
    option_serenade = 1
    option_alpha_omega = 2
    default = 0


MMBN3Options = {
    "Goal": Goal
}