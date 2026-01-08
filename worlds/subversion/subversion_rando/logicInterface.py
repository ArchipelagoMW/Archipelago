from typing import Callable

from .loadout import Loadout

AreaLogicType = dict[str, dict[tuple[str, str], Callable[[Loadout], bool]]]
LocationLogicType = dict[str, Callable[[Loadout], bool]]
