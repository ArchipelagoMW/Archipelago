"""
Options for the Castlevania: Aria of Sorrow randomizer.
"""

from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle

class RandomizePickups(Toggle):
    """
    Adds on-ground, single-obtainance pickups to the pool.
    """
    display_name = "Randomize Pickups"
    default = 1


@dataclass
class CVAOSOptions(PerGameCommonOptions):
    """Options for the Castlevania: Aria of Sorrow randomizer."""
    randomize_pickups: RandomizePickups
