from dataclasses import dataclass
from typing import Type, Any
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility, Option
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions

class RandomizeJobs(Toggle):
    """
    When enabled, Jobs can be found anywhere, when disabled they are always on crystals.
    """
    display_name = "Randomize Whatever"

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    randomizeJobs: RandomizeJobs