import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import Toggle


class TrapPercentage(Range):
    """Percentage of filler that are traps"""

    display_name = "Trap Percentage"
    default = 1
    range_start = 0
    range_end = 100
