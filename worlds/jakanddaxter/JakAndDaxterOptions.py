import os
from dataclasses import dataclass
from Options import Toggle, PerGameCommonOptions


class EnableMoveRandomizer(Toggle):
    """Enable to include movement options as items in the randomizer.
    Jak is only able to run, swim, and single jump, until you find his other moves.
    Adds 11 items to the pool."""
    display_name = "Enable Move Randomizer"


# class EnableOrbsanity(Toggle):
#     """Enable to include Precursor Orbs as an ordered list of progressive checks.
#     Each orb you collect triggers the next release in the list.
#     Adds 2000 items to the pool."""
#     display_name = "Enable Orbsanity"


@dataclass
class JakAndDaxterOptions(PerGameCommonOptions):
    enable_move_randomizer: EnableMoveRandomizer
    # enable_orbsanity: EnableOrbsanity
