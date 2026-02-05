from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions

class Goal(Choice):
    """Choose the end goal.
    Main Quest: Complete the main quest"""
    display_name = "Goal"
    option_main_quest = 0
    default = 0

#class SkillUpgrade(Choice):
#    """Choose how skills will be upgraded.
#    Coins: You upgrade skills in-game using coins.
#    Progressive Skills: Each spell is added to the itempool 10 times.
#    Upgrades: Each spell is added to the itempool once, allowing usage of that spell. Additionally, 9 upgrades for each spell are added to the itempool, that will be applied once the skill is aquired.
#    Magic Levels: Each spell is added to the itempool once, allowing usage of that spell. Additionally, 9 magic levels are added to the itempool, that will upgrade all acquired spells.
#    """
#    display_name = "Skills Upgrades"
#    option_coins = 0
#    option_progressive_skills = 1
#    option_upgrades = 2
#    option_magic_levels = 3
#    default = 2

@dataclass
class CatQuestOptions(PerGameCommonOptions):
    goal: Goal
    #skill_upgrade: SkillUpgrade
    
