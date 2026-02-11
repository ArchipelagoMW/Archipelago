from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class IntroSkip(Choice):
    """
    Determines whether the player should start on Veldin or Starship Phoenix.
    Disabled: The player starts on Veldin, then must complete Florana to reach the Starship Phoenix.
    Enabled: The player begins on the Starship Phoenix, Veldin is skipped and the player starts with the items that
    would have been placed on Veldin.
    """
    display_name = RAC3OPTION.INTRO_SKIP
    option_disabled = 0
    option_enabled = 1
    default = 0
