from Options import Choice
from worlds.rac3 import RAC3OPTION


class TitaniumBolts(Choice):
    """
    Determines whether Titanium Bolts are locations in the world.
    Disabled: No Titanium Bolts are locations.
    Enabled: Titanium Bolts are added as locations. Any Titanium bolts locked behind other locations such as
    Ranger Missions require those options to be enabled
    """
    display_name = RAC3OPTION.TITANIUM_BOLTS
    option_disabled = 0
    option_enabled = 1
    default = 1
