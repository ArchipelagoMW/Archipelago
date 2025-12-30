from Options import Choice
from worlds.rac3 import RAC3OPTION


class SkillPoints(Choice):
    """
    Determines which skill points are locations in the world.
    None: No skill points are locations.
    Simple: 20 simple skill points are locations, 10 of the more challenging or time-consuming skill points are
    removed. Any Skill Points locked behind other locations such as Ranger Missions require those options to be enabled.
    These are the skill points enabled:
    - Stay Squeaky Clean
    - Monkeying around
    - Beat Helga's best time
    - Turn Up The Heat
    - Reflect on how to score
    - Flee Flawlessly
    - Lights, camera action!
    - Search for sunken treasure
    - Be a sharpshooter
    - Bugs to Birdie
    - Get to the belt
    - Feeling Lucky?
    - Bash the party
    - 2002 was a good year in the city
    - Aim High
    - Zap back at ya'
    - Go for hang time
    - Break the Dan
    - You break it, you win it
    - Spread your germs
    Every Skill Point: All 30 Skill Points are added as locations. Any Skill Points locked behind other locations
    such as Ranger Missions require those options to be enabled
    """
    display_name = RAC3OPTION.SKILL_POINTS
    option_none = 0
    option_simple = 1
    option_every_skill_point = 2
    default = 1
