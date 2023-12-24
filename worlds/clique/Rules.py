from typing import Callable

from BaseClasses import CollectionState
from Options import PerGameCommonOptions


def get_button_rule(options: PerGameCommonOptions, player: int) -> Callable[[CollectionState], bool]:
    if getattr(options, "hard_mode"):
        return lambda state: state.has("Button Activation", player)

    return lambda state: True
