from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class ArmorVendors(Choice):
    """
    Determines whether armor vendor items are locations in the world.
    Disabled: No armor vendor items are locations.
    Enabled: Armor vendor items are added as locations.

    Visiting the planet associated with the armor will put it in the armor vendor.
    Magnaplate: Starship Phoenix
    Adamantite: Aquatos
    Aegis Mark V: Zeldrin Starport
    Infernox: Koros

    Disabling this option will not make armor work like in the vanilla game.
    Armor is determined by the number of progressive armor items you have.
    """
    display_name = RAC3OPTION.ARMOR_VENDOR
    option_disabled = 0
    option_enabled = 1
    default = 1
