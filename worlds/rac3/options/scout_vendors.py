from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class ScoutVendors(Choice):
    """
    Determines whether weapon and armor vendors should send out hints about items inside them.
    Due to the amount of checks in the ship vendors, those are not supported.
    """
    display_name = RAC3OPTION.SCOUT_VENDORS
    option_disabled = 0
    option_enabled = 1
    default = 0
