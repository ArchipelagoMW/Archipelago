# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
from Options import Option, Range


class RainbowTrap(Range):
    """Rainbow Traps change the color of every bumper on the field."""
    display_name = "Rainbow Traps"
    range_start = 0
    range_end = 5
    default = 2


class SpinnerTrap(Range):
    """Spinner Traps change the direction of every bumper on the field."""
    display_name = "Spinner Traps"
    range_start = 0
    range_end = 5
    default = 2


class KillerTrap(Range):
    """Killer Traps end the current board immediately."""
    display_name = "Killer Traps"
    range_start = 0
    range_end = 3
    default = 0


bumpstik_options: typing.Dict[str, type(Option)] = {
    "rainbow_traps": RainbowTrap,
    "spinner_traps": SpinnerTrap,
    "killer_traps": KillerTrap
}
