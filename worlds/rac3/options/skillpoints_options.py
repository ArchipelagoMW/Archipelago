from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class SkillPoints(Choice):
    """
    Determines which skill points are locations in the world.
    Any Skill Points locked behind other locations such as Ranger Missions require those options to be enabled
    Simple locations are the following:
    - Aridia: Skillpoint: Go for hang time
    - Phoenix: Skillpoint: Beat Helga's best time
    - Phoenix: Skillpoint: Turn Up The Heat
    - Phoenix: Skillpoint: Monkeying around
    - Marcadia: Skillpoint: Reflect on how to score
    - Daxx: Skillpoint: Bugs to Birds
    - Annihilation Nation: Skillpoint: Lights, camera action!
    - Aquatos: Skillpoint: Search for sunken treasure
    - Tyhrranosis: Skillpoint: Be a Sharpshooter
    - Obani Gemini: Skillpoint: Get to the belt
    - Blackwater City: Skillpoint: Bash the party
    - Koros: Skillpoint: You break it, you win it
    - Metropolis: Skillpoint: 2002 was a good year in the city
    - Crash Site: Skillpoint: Suck it up!
    - Crash Site: Skillpoint: Aim High
    - Aridia: Skillpoint: Zap back at ya'
    - Hideout: Skillpoint: Break the Dan
    - Command Center: Skillpoint: Spread your germs
    """
    display_name = RAC3OPTION.SKILL_POINTS
    option_none = 0
    option_simple = 1
    option_all = 2
    default = 1
