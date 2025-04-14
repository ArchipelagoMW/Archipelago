from dataclasses import dataclass
from typing import Type, Any
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility, Option
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions
from schema import Schema, And, Optional, Or

class RandomizeWhatever(DefaultOnToggle):
    """
    When enabled, the Walkie Talkie item will be placed into the item pool. Otherwise, it will be placed in its vanilla location.
    This item usually allows the player to locate Avery around the map or restart a race.
    """
    display_name = "Randomize Whatever"

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    whatever: RandomizeWhatever