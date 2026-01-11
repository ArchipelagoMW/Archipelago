import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions



class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

class ExpMultiplierOption(Range):
    """Multiplies stat gain by specified amount"""
    display_name = "Exp Multiplier"
    min_value = 1
    range_start = 1
    range_end = 10
    default = 1

class EnsureEarlyStatCapOption(DefaultOnToggle):
    """Places a Stat Cap in the first properity point location"""
    display_name = "Ensure Early Stat Cap"    

class GoalOption(Choice):
    """Sets the goal for the game"""
    display_name = "Goal"
    default = 0
    option_prosperity = 0
    option_digitamamon = 1   

class RequiredProsperityOption(Range):
    """Sets the required prosperity points to complete the game"""
    display_name = "Required Prosperity Points"
    min_value = 1
    range_start = 1
    range_end = 100
    default = 100

class ProgressiveStatOption(DefaultOnToggle):
    """Enables Progressive Stat gain caps"""
    display_name = "Progressive Stat Caps"

class EasyMonochromonOption(DefaultOnToggle):
    """Always win the Monochromon Minigame"""
    display_name = "Easy Monochromon"
    
class FastDrimogemonOption(DefaultOnToggle):
    """Makes Drimogen dig in 1 day instead of 10"""
    display_name = "Fast Drimogemon"
    
class RandomStarterOption(Choice):
    """Randomise the 2 starter digimon options
    Vanilla = Agumon and Gabumon are the starters
    All = Any digimon can be a starter
    Rookie = Only rookie digimon can be a starter"""
    display_name = "Random starter digimon"
    option_vanilla = 0
    option_all = 1
    option_rookie = 2
    default = 2

class RandomTechniqueOption(Choice):
    """Randomise the techniques that digimon learn
    Vanilla = Digimon techniques are unchanged
    Enabled = Techniques are randomised"""
    display_name = "Random techniques"
    option_vanilla = 0
    option_enabled = 1
    default = 1

@dataclass
class DigimonWorldOption(PerGameCommonOptions):
    goal: GoalOption
    early_statcap: EnsureEarlyStatCapOption
    required_prosperity: RequiredProsperityOption
    guaranteed_items: GuaranteedItemsOption
    exp_multiplier: ExpMultiplierOption
    progressive_stats: ProgressiveStatOption
    random_starter: RandomStarterOption
    random_techniques: RandomTechniqueOption
    fast_drimogemon: FastDrimogemonOption
    easy_monochromon: EasyMonochromonOption