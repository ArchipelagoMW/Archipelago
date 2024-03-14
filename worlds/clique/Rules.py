from typing import Callable

from BaseClasses import CollectionState, MultiWorld


def get_button_rule(multiworld: MultiWorld, player: int) -> Callable[[CollectionState], bool]:
    if getattr(multiworld, "hard_mode")[player]:
        return lambda state: state.has("Button Activation", player)

    return lambda state: True
