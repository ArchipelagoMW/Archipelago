from Options import Choice
from worlds.rac3 import RAC3OPTION


class VidComics(Choice):
    """
    Determines whether VidComics and anything that is located in or behind them is a location.
    Disabled: Removes anything that is located in or behind a VidComic from being a location.
    Enabled: VidComics, and anything directly locked behind them, are added as locations.
    Any Skill Points or Titanium Bolts are added if their respective setting is enabled.
    """
    display_name = RAC3OPTION.VIDCOMICS
    option_disabled = 0
    option_enabled = 1
    default = 1
