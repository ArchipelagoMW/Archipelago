import typing
from itertools import chain
from typing import Callable, Set

from . import pyevermizer
from .options import EnergyCore, OutOfBounds, SequenceBreaks, SoEOptions

if typing.TYPE_CHECKING:
    from BaseClasses import CollectionState

# TODO: Options may preset certain progress steps (i.e. P_ROCK_SKIP), set in generate_early?

# TODO: resolve/flatten/expand rules to get rid of recursion below where possible
# Logic.rules are all rules including locations, excluding those with no progress (i.e. locations that only drop items)
rules = pyevermizer.get_logic()
# Logic.items are all items and extra items excluding non-progression items and duplicates
# NOTE: we are skipping sniff items here because none of them is supposed to provide progression
item_names: Set[str] = set()
items = [
    item
    for item in filter(
        lambda item: item.progression,
        chain(pyevermizer.get_items(), pyevermizer.get_extra_items()),
    )
    if item.name not in item_names and not item_names.add(item.name)  # type: ignore[func-returns-value]
]


class SoEPlayerLogic:
    __slots__ = "player", "out_of_bounds", "sequence_breaks", "has"
    player: int
    out_of_bounds: bool
    sequence_breaks: bool

    has: Callable[..., bool]
    """
    Returns True if count of one of evermizer's progress steps is reached based on collected items. i.e. 2 * P_DE
    """

    def __init__(self, player: int, options: "SoEOptions"):
        self.player = player
        self.out_of_bounds = options.out_of_bounds == OutOfBounds.option_logic
        self.sequence_breaks = options.sequence_breaks == SequenceBreaks.option_logic

        if options.energy_core == EnergyCore.option_fragments:
            # override logic for energy core fragments
            required_fragments = options.required_fragments.value

            def fragmented_has(state: "CollectionState", progress: int, count: int = 1) -> bool:
                if progress == pyevermizer.P_ENERGY_CORE:
                    progress = pyevermizer.P_CORE_FRAGMENT
                    count = required_fragments
                return self._has(state, progress, count)

            self.has = fragmented_has
        else:
            # default (energy core) logic
            self.has = self._has

    def _count(self, state: "CollectionState", progress: int, max_count: int = 0) -> int:
        """
        Returns reached count of one of evermizer's progress steps based on collected items.
        i.e. returns 0-3 for P_DE based on items providing CHECK_BOSS,DIAMOND_EYE_DROP
        """
        n = 0
        for item in items:
            for pvd in item.provides:
                if pvd[1] == progress:
                    if state.has(item.name, self.player):
                        n += state.count(item.name, self.player) * pvd[0]
                        if n >= max_count > 0:
                            return n
        for rule in rules:
            for pvd in rule.provides:
                if pvd[1] == progress and pvd[0] > 0:
                    has = True
                    for req in rule.requires:
                        if not self.has(state, req[1], req[0]):
                            has = False
                            break
                    if has:
                        n += pvd[0]
                        if n >= max_count > 0:
                            return n
        return n

    def _has(self, state: "CollectionState", progress: int, count: int = 1) -> bool:
        """Default implementation of has"""
        if self.out_of_bounds is True and progress == pyevermizer.P_ALLOW_OOB:
            return True
        if self.sequence_breaks is True and progress == pyevermizer.P_ALLOW_SEQUENCE_BREAKS:
            return True
        return self._count(state, progress, count) >= count
