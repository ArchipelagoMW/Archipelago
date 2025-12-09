from Options import Choice
from worlds.rac3 import RAC3OPTION


class VRChallenges(Choice):
    """
    Determines whether VR Challenges and anything that is located in or behind them is a location.
    Disabled: Removes anything that is located in or behind a VR Challenge from being a location.
    Enabled: VR Challenges, and anything directly locked behind them, are added as locations.
    Any Skill Points or Titanium Bolts are added if their respective setting is enabled.
    This option also includes the VR Training Challenge before Daxx and all of it's checks
    """
    display_name = RAC3OPTION.VR_CHALLENGES
    option_disabled = 0
    option_enabled = 1
    default = 1
