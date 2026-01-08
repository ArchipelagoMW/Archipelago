from Options import Choice
from worlds.rac3 import RAC3OPTION


class Arena(Choice):
    """
    Determines whether Annihilation Nation challenges and anything that is located in or behind them is a location.
    None: Removes anything that is located in or behind an Annihilation Nation challenge from being a location.
    First Only: Annihilation Nation 1 challenges, and anything directly locked behind them, are added as locations.
    Second Only: Annihilation Nation 2 challenges, and anything directly locked behind them, are added as locations.
    All: All Annihilation Nation challenges, and anything directly locked behind them, are added as locations.
    Any Skill Points or Titanium Bolts are added if their respective setting is enabled.
    """
    display_name = RAC3OPTION.ARENA
    option_none = 0
    option_first_only = 1
    option_second_only = 2
    option_all = 3
    default = 3
