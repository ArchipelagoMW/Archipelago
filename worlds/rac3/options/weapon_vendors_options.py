from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class WeaponVendors(Choice):
    """
    Warning: Receiving weapons send out their associated vendor checks as well, it is recommended to keep
    this option disabled until it is fixed. Weapons are still randomized even with this option disabled.

    Determines whether weapon vendors are locations in the world.
    Disabled: No weapon vendors are locations.
    Enabled: Weapon vendors are added as locations.
    """
    display_name = RAC3OPTION.WEAPON_VENDORS
    option_disabled = 0
    option_enabled = 1
    default = 0
