import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions

class GoalOptions():
    DEFEAT_ZAROK = 0
    CHALICE = 1
    
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
    Chalices - Collect all chalices"""
    display_name = "Completion Goal"
    default = GoalOptions.DEFEAT_ZAROK
    option_zarok = GoalOptions.DEFEAT_ZAROK
    option_chalice = GoalOptions.CHALICE

@dataclass
class MedievilOption(PerGameCommonOptions):
    goal: GoalOption
    exclude_ant_caves: ExcludeAntCaves
    exclude_dynamic_items: ExcludeDynamicItems
    guaranteed_items: GuaranteedItemsOption