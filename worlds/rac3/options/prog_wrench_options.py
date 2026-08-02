"""This module contains options for the Progressive OmniWrench in the item pool"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class ProgressiveWrench(Choice):
    """
    Determines whether the OmniWrench is a Progressive item or not.
    ------------------------------------------------------------------------------------
    Disable:           OmniWrench functions like in the vanilla game.
    Manual Upgrade:    OmniWrench is allowed to upgrade if the Nanotech level required is reached and its progressive item is collected.
    Automatic Upgrade: The OmniWrench will upgrade when its progressive item is collected, ignoring your Nanotech level.
    Lost Wrench:       Ratchet will start without its OmniWrench and will need to be collected first. DO NOT USE YET.
    ------------------------------------------------------------------------------------
    Note: If Weapon Level Locations are enabled, Automatic Upgrade will be forced to Manual Upgrade instead.
    """
    display_name = RAC3OPTION.PROGRESSIVE_WRENCH
    option_disable = 0
    option_manual_upgrade = 1
    option_automatic_upgrade = 2
    option_lost_wrench = 3
    default = 0
