from dataclasses import dataclass
from Options import Choice, Range, Toggle, ItemDict, PerGameCommonOptions, StartInventoryPool

class StartingPartyMember(Choice):
    """
    This selects which party member you are given at the very beginning of the game.
    """
    display_name = "Starting Party Member"
    option_random = 0
    option_pinn = 1
    option_geo = 1
    option_kani = 1
    default = 0


@dataclass
class SilverDazeOptions(PerGameCommonOptions):
    StartingPartyMember = StartingPartyMember