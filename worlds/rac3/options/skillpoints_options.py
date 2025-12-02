from Options import Choice
from worlds.rac3 import RAC3OPTION


class SkillPoints(Choice):
    # Todo: Update skill points
    """
    Determines which skill points are locations in the world.
    None: No skill points are locations.
    Simple: 15 simple skill points are locations. Still taking feedback on the selection:
    - Stay Squeaky Clean
    - Reflect on how to score
    - Lights, camera action!
    - Flee Flawlessly
    - Search for sunken treasure
    - Be a sharpshooter
    - Beat Helga's Best Time
    - Bugs to Birdie
    - Get to the belt
    - Feeling Lucky?
    - 2002 was a good year in the city
    - Aim High
    - Go for hang time
    - Break the Dan
    - You break it, you win it
    Every Skill Point: All 30 skill points are locations.
    """
    display_name = RAC3OPTION.SKILL_POINTS
    option_none = 0
    option_simple = 1
    option_every_skill_point = 2
    default = 1
