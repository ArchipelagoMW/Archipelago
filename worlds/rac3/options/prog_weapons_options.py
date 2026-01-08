from Options import Choice
from worlds.rac3 import RAC3OPTION


class EnableProgressiveWeapons(Choice):
    """
    Determines whether weapon level-ups are progressive items or not.
    **Disable**: Weapon leveling and exp functions like in the vanilla game.
    **Enable**: Weapons level-up when it's progressive item is collected, weapon exp is disabled.
    """
    display_name = RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS
    option_disable = 0
    option_enable = 1
    default = 1
