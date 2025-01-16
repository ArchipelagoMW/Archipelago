from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, StartInventoryPool

class Goal(Choice):
    """Choose the end goal.
    Main Quest: Complete the main quest"""
    display_name = "Goal"
    option_main_quest = 0
    default = 0

# """Purchaseable skills Toggle
# Yes: Skills will appear in the item pool once, and will be purchaseable in the Arcane Temples hereafter
# No: Skills and all upgrades will appear in the item pool, and you cannot upgrade skills by purchasing them in the Arcane Temples"""

@dataclass
class CatQuestOptions(PerGameCommonOptions):
    goal: Goal