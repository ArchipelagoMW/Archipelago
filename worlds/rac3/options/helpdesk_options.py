"""This module contains options for New Game Plus purchase locations"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class HelpDesk(Choice):
    """
    Determines if the in-game help desk should be enabled/disabled from the start.
    **Disable**: Helpdesk is disabled when creating a new save.
    **Enable**: Helpdesk is enabled when creating a new save.
    """
    display_name = RAC3OPTION.HELP_DESK
    option_disable = 0
    option_enable = 1
    default = 1
