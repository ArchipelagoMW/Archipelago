from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Toggle

class Goal(Choice):
    """Choose the end goal.
    Main Quest: Complete the main quest
    Questsanity: Complete all quests in the game
    Max Level: Reach level 99
    Max Level and Main Quest: Complete the main quest and reach level 99
    Spellmastery: Get all spells to max level
    """
    display_name = "Goal"
    option_main_quest = 0
    option_questsanity = 1
    option_max_level = 2
    option_max_level_and_main_quest = 3
    option_spellmastery = 4
    default = 0

class SkillUpgrade(Choice):
    """Choose how skills will be upgraded.
    Coins: You upgrade skills in-game using coins. (The vanilla way)
    Progressive Skills: Each spell is added to the itempool 10 times.
    Upgrades: Each spell is added to the itempool once, allowing usage of that spell. Additionally, 9 upgrades for each spell are added to the itempool, that will be applied once the skill is aquired.
    Magic Levels: Each spell is added to the itempool once, allowing usage of that spell. Additionally, 9 magic levels are added to the itempool, that will upgrade all acquired spells.
    """
    display_name = "Skills Upgrades"
    option_coins = 0
    option_progressive_skills = 1
    option_upgrades = 2
    option_magic_levels = 3
    default = 3

class IncludeTemples(Toggle):
    """Choose if visiting temples will be included"""
    display_name = "Include Temples"
    default = True

class IncludeMonuments(Toggle):
    """Choose if visiting monuments will be included"""
    display_name = "Include Monuments"
    default = True

class IncludeEXPQuestRewards(Toggle):
    """Choose if you want to receive EXP as quest rewards. (Beware, not including this option can cause heavy grind with some options)"""
    display_name = "Include EXP Quest Rewards"
    default = True

class IncludeCoinQuestRewards(Toggle):
    """Choose if you want to receive coins as quest rewards"""
    display_name = "Include Coin Quest Rewards"
    default = True

@dataclass
class CatQuestOptions(PerGameCommonOptions):
    goal: Goal
    skill_upgrade: SkillUpgrade
    include_temples: IncludeTemples
    include_monuments: IncludeMonuments
    include_quest_reward_exp: IncludeEXPQuestRewards
    include_quest_reward_coins: IncludeCoinQuestRewards
    
