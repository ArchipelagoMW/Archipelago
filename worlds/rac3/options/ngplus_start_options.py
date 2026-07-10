"""This module contains options for New Game Plus purchase locations"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class NGPlusStart(Choice):
    """
    Determines if the game should start in New Game Plus mode.
    ------------------------------------------------------------------------------------
    Disabled:                Game starts in normal mode.
    Enabled:                 Game starts in Challenge Mode.
    Enabled with Multiplier: Game starts in Challenge Mode, and the NG+ multiplier is enabled.
    ------------------------------------------------------------------------------------
    WARNING:    The NG+ bolt multiplier stacks with the bolt and XP multiplier, which can lead to very high multipliers
                that can break the game. Use with caution.
    """
    display_name = RAC3OPTION.NGPLUS_START
    option_disabled = 0
    option_enabled = 1
    option_enabled_with_multiplier = 2
    default = 0
