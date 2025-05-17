from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import SohWorld


def get_soh_rule(world: "SohWorld") -> Callable[[CollectionState], bool]:

    return lambda state: True
