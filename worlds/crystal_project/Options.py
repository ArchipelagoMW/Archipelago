from dataclasses import dataclass
from typing import Type, Any
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility, Option
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions

class Goal(Choice):
    """
    Choose what is required to complete the game.
    
    Talking to Nan in <insert correct place name here!> will tell you the selected goal.
    
    Astley: Defeat Astley (add more here).
    
    True Astley: Defeat Astley but more somehow

    Clamshells: Collect enough clamshells for the clam lover
    """
    display_name = "Goal"
    option_astley = 0
    option_true_astley = 1
    option_clamshells = 2
    default = 0
    
class ClamshellsQuantity(Range):
    """If your goal is Clamshells, this is where you select how many you need to win."""
    display_name = "Clamshells needed to win"
    range_start = 1
    range_end = 19
    default = 13

class RandomizeJobs(DefaultOnToggle):
    """
    When enabled, Jobs can be found anywhere, when disabled they are always on crystals.
    """
    display_name = "Randomize Jobs"

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    goal: Goal
    clamshellsQuantity: ClamshellsQuantity
    randomizeJobs: RandomizeJobs