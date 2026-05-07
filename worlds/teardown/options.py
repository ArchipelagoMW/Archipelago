from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Toggle, DefaultOnToggle

class MissionAmount(Range):
    """
    Amount of levels required to complete goal
    """
    display_name = "Mission Amount"

    range_start = 1
    range_end = 40
    default = 30


class StartingTool(Toggle):
    """
    If enabled, the starting tools will be randomized.
    """
    display_name = "Randomize Starting Tools"


class StartingLevel(DefaultOnToggle):
    """
    If enabled, the starting level is randomized, if not it is Old Building Problem.
    """
    display_name = "Randomize Starting Level"


# class ValuableSanity(Toggle):
#    """
#    Enables Valuable Sanity
#    """
#    display_name = "Valuable Sanity"



@dataclass
class TeardownOptions(PerGameCommonOptions):
    MissionAmount: MissionAmount
    StartingTool: StartingTool
    StartingLevel: StartingLevel
    #ValuableSanity: ValuableSanity

