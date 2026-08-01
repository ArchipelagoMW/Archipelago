from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventoryPool


class Goal(Choice):
    """Victory condition.

    sigma: reach and defeat Sigma after defeating all 8 Mavericks.
    launch: collect all 8 Enigma/Shuttle Parts and complete a successful
    launch (the client only powers a launch once every part is in hand -
    partial part sets always fail the launch, vanilla-style).
    """
    display_name = "Goal"
    option_sigma = 0
    option_launch = 1
    default = 0


@dataclass
class MMX5Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
