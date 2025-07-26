import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions

class GoalOptions():
    DEFEAT_ZAROK = 0
    CHALICE = 1

class ProgressionOptions():
    VANILLA = 0
    RANDOM = 1
    
class ExcludeAntCaves(Toggle):
    """Remove the need to go into the Ant Hill from logic"""
    display_name = "Remove Ant Hill Logic"
    
class ExcludeDynamicItems(Toggle):
    """Excludes Dynamic drops from the check list. They require a different kind of logic. Keep this as its default value unless testing"""
    display_name = "Exclude Dynamic Items from the Pool"
    default = 1
    option_true = 1
    option_false = 0

class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"
    

class GoalOption(Choice):
    """Lets the user choose the completion goal
    Defeat Zarok - Beat the boss at the end
    Chalices - Collect all chalices (Collect all chalices doesn't work right now)"""
    display_name = "Completion Goal"
    default = GoalOptions.DEFEAT_ZAROK
    option_zarok = GoalOptions.DEFEAT_ZAROK
    option_chalice = GoalOptions.CHALICE
    
class ProgressionOption(Choice):
    """Lets users choose how they wish to progress
    Vanilla - Plays the game like normal
    (Will only do Vanilla for now)"""
    display_name = "Game Progression Options"
    default = ProgressionOptions.VANILLA
    option_vanilla = ProgressionOptions.VANILLA
    
    
class MonsterSanityToggle(Toggle):
    """Sets whether to do checks for individual monsters (Doesn't work)"""
    display_name = "MonsterSanity"
    default = 0
    option_true = 1
    option_false = 0
    
class RuneSanityToggle(Toggle):
    """Sets whether to mix runes into the pool (Is this by default, but doesn't work. Vanilla progression)"""
    display_name = "RuneSanity"
    default = 1
    option_true = 1
    option_false = 0    
    
class BookSanityToggle(Toggle):
    """Sets whether reading books counts as checks (Doesn't work)"""
    display_name = "BookSanity"
    default = 0
    option_true = 1
    option_false = 0

@dataclass
class MedievilOption(PerGameCommonOptions):
    goal: GoalOption
    progression_option: ProgressionOption
    exclude_ant_caves: ExcludeAntCaves
    exclude_dynamic_items: ExcludeDynamicItems
    monstersanity: MonsterSanityToggle
    booksanity: BookSanityToggle
    runesanity: RuneSanityToggle
    guaranteed_items: GuaranteedItemsOption