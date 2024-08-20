from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import CliqueWorld


def get_button_rule(world: "CliqueWorld") -> Callable[[CollectionState], bool]:
    if world.options.hard_mode:
        return lambda state: state.has("Button Activation", world.player)

    return lambda state: True
