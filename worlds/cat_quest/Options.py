from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, StartInventoryPool

class Goal(Choice):
    """Choose the end goal.
    Main Quest: Complete the main quest
    Questsanity: Complete the main quest and all side quests"""
    display_name = "Goal"
    option_main_quest = 0
    option_questsanity = 1
    default = 0

@dataclass
class CatQuestOptions(PerGameCommonOptions):
    goal: Goal