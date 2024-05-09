# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass

import typing
from Options import Option, Range, PerGameCommonOptions


class TaskAdvances(Range):
    """Task Advances allow you to skip one step of a level task. They do not restock, so use them sparingly."""
    display_name = "Task Advances"
    range_start = 0
    range_end = 5
    default = 4


class Turners(Range):
    """Turners allow you to change the direction of a Bumper. These restock when the board resets."""
    display_name = "Turners"
    range_start = 0
    range_end = 5
    default = 3


class PaintCans(Range):
    """
        Paint Cans allow you to change the color of a Bumper.
        The ones you get from the multiworld restock when the board resets; you also get one-time ones from score.
    """
    display_name = "Paint Cans"
    range_start = 0
    range_end = 5
    default = 3


class Traps(Range):
    """
        Traps affect the board in various ways.
        This number indicates how many total traps will be added to the item pool.
    """
    display_name = "Trap Count"
    range_start = 0
    range_end = 15
    default = 5


class RainbowTrapWeight(Range):
    """Rainbow Traps change the color of every bumper on the field."""
    display_name = "Rainbow Trap weight"
    range_start = 0
    range_end = 100
    default = 50


class SpinnerTrapWeight(Range):
    """Spinner Traps change the direction of every bumper on the field."""
    display_name = "Spinner Trap weight"
    range_start = 0
    range_end = 100
    default = 50


class KillerTrapWeight(Range):
    """Killer Traps end the current board immediately."""
    display_name = "Killer Trap weight"
    range_start = 0
    range_end = 100
    default = 0


@dataclass
class BumpstikOptions(PerGameCommonOptions):
    task_advances: TaskAdvances
    turners: Turners
    paint_cans: PaintCans
    trap_count: Traps
    rainbow_trap_weight: RainbowTrapWeight
    spinner_trap_weight: SpinnerTrapWeight
    killer_trap_weight: KillerTrapWeight
