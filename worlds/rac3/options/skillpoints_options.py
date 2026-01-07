from Options import OptionDict
from worlds.rac3 import RAC3OPTION
from worlds.rac3.constants.locations.skillpoints import SKILLPOINT_LOCATION_TO_NAME


class SkillPoints(OptionDict):
    """
    Determines which skill points are locations in the world.
    For skill points you wish to include put true next to them.
    For skill points you wish to exclude put false next to them.
    Any Skill Points locked behind other locations such as Ranger Missions require those options to be enabled
    """
    display_name = RAC3OPTION.SKILL_POINTS
    default = {name: True for name in SKILLPOINT_LOCATION_TO_NAME.values()}
    valid_keys = SKILLPOINT_LOCATION_TO_NAME.values()
