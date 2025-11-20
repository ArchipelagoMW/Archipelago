from Options import Choice
from worlds.rac3 import RAC3OPTION

class Arena(Choice):
    """
    Determines whether Annihilation Nation challenges and anything that is located in or behind them is a location.
    Disabled: Removes anything that is located in or behind an Annihilation Nation challenge from being a location.
    Enabled: Annihilation Nation challenges, and anything directly locked behind them, are added as locations.
    Any Skill Points or Titanium Bolts are added if their respective setting is enabled.
    """
    display_name = RAC3OPTION.ARENA
    option_disabled = 0
    option_enabled = 1
    default = 0