"""This module contains options for the Progressive OmniWrench in the item pool"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class ProgressiveWrench(Choice):
    """
    Determines if Progresive OmniWrench items are included in the item pool.
    ------------------------------------------------------------------------------------
    Disable for the vanilla OmniWrench behaviour.
    Enable for OmniWrench upgrades to be included in the item pool.
    ------------------------------------------------------------------------------------
    Note: Experimental feature.
    """
    display_name = RAC3OPTION.PROGRESSIVE_WRENCH
    option_disabled = 0
    option_enabled = 1
    default = 0

