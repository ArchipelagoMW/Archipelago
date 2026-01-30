from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class WeaponVendors(Choice):
    """
    Determines whether weapon vendors are locations in the world.
    Disabled: No weapon vendors are locations.
    Enabled: Weapon vendors are added as locations.

    Weapons are still randomized regardless of this setting.
    """
    display_name = RAC3OPTION.WEAPON_VENDORS
    option_disabled = 0
    option_enabled = 1
    default = 1
