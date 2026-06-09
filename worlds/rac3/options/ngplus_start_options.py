"""This module contains options for New Game Plus purchase locations"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class NGPlusStart(Choice):
    """
    Determines if the game should start in New Game Plus mode.
    **Disable**: Game starts in normal mode.
    **Enable**: Game starts in Challenge Mode.
    **Enable with Multiplier**: Game starts in Challenge Mode, and the NG+ multiplier is enabled.

    WARNING: The NG+ multiplier stacks with the bolt and XP multiplier, which can lead to very high multipliers that can break the game.
    Use with caution.
    """
    display_name = RAC3OPTION.NGPLUS_START
    option_disable = 0
    option_enable = 1
    option_enable_with_multiplier = 2
    default = 0
