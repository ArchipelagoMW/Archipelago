from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventoryPool


class Goal(Choice):
    """Victory condition.

    sigma: reach and defeat Sigma after defeating all 8 Mavericks.
    (More goals - e.g. Zero Virus stages, low-hour clears - may come later.)
    """
    display_name = "Goal"
    option_sigma = 0
    default = 0


@dataclass
class MMX5Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
