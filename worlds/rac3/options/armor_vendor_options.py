from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class ArmorVendors(Choice):
    """
    Determines whether armor vendor items are locations in the world.
    Disabled: No armor vendor items are locations.
    Enabled: Armor vendor items are added as locations.

    Note: Each planet you have will put the next 3 items in the armor vendor in order of how they would appear in the vanilla game.
    """
    display_name = RAC3OPTION.ARMOR_VENDOR
    option_disabled = 0
    option_enabled = 1
    default = 1
