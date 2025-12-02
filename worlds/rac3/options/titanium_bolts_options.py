from Options import Choice
from worlds.rac3 import RAC3OPTION


class TitaniumBolts(Choice):
    """
    Determines whether titanium bolts are locations in the world.
    Disabled: No titanium bolts are locations.
    Enabled: All titanium bolts are locations.
    """
    display_name = RAC3OPTION.TITANIUM_BOLTS
    option_disabled = 0
    option_enabled = 1
    default = 1
