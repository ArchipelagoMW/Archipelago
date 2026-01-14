from Options import Choice
from worlds.rac3 import RAC3OPTION


class SkillPoints(Choice):
    """
    Determines which skill points are locations in the world.
    Any Skill Points locked behind other locations such as Ranger Missions require those options to be enabled
    """
    display_name = RAC3OPTION.SKILL_POINTS
    option_none = 0
    option_simple = 1
    option_all = 2
    default = 1
