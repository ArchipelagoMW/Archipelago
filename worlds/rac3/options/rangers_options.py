from Options import Choice
from worlds.rac3 import RAC3OPTION


class Rangers(Choice):
    """
    Determines whether Ranger Missions and anything that is located in or behind them is a location.
    None: Removes anything that is located in or behind a Ranger Mission from being a location.
    Story Missions: Story related Ranger Missions, and anything directly locked behind them, are added as locations.
    Story missions include: Marcadia, Blackwater City, and Aridia missions.
    Optional Missions: Ranger Missions that are optional in the main game, and anything directly locked behind them,
    are added as locations.
    Optional missions include: Tyhrranosis: Operation ISLAND STRIKE and Metropolis: Operation URBAN STORM missions
    All: Ranger Missions, and anything directly locked behind them, are added as locations.
    Any Skill Points or Titanium Bolts are added if their respective setting is enabled.
    """
    display_name = RAC3OPTION.RANGERS
    option_none = 0
    option_story_missions = 1
    option_optional_missions = 2
    option_all = 3
    default = 3
