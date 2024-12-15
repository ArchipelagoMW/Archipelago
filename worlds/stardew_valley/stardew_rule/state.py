from dataclasses import dataclass
from typing import Iterable, Union, List, Tuple, Hashable, TYPE_CHECKING

from BaseClasses import CollectionState
from .base import BaseStardewRule, CombinableStardewRule
from .protocol import StardewRule

if TYPE_CHECKING:
    from .. import StardewValleyWorld


class TotalReceived(BaseStardewRule):
    count: int
    items: Iterable[str]
    player: int

    def __init__(self, count: int, items: Union[str, Iterable[str]], player: int):
        items_list: List[str]

        if isinstance(items, Iterable):
            items_list = [*items]
        else:
            items_list = [items]

        self.player = player
        self.items = items_list
        self.count = count

    def __call__(self, state: CollectionState) -> bool:
        c = 0
        for item in self.items:
            c += state.count(item, self.player)
            if c >= self.count:
                return True
        return False

    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        return self, self(state)

    def __repr__(self):
        return f"Received {self.count} {self.items}"


@dataclass(frozen=True)
class Received(CombinableStardewRule):
    item: str
    player: int
    count: int
    event: bool = False
    """Helps `explain` to know it can dig into a location with the same name."""

    @property
    def combination_key(self) -> Hashable:
        return self.item

    @property
    def value(self):
        return self.count

    def __call__(self, state: CollectionState) -> bool:
        return state.has(self.item, self.player, self.count)

    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        return self, self(state)

    def __repr__(self):
        if self.count == 1:
            return f"Received {'event ' if self.event else ''}{self.item}"
        return f"Received {'event ' if self.event else ''}{self.count} {self.item}"


@dataclass(frozen=True)
class Reach(BaseStardewRule):
    spot: str
    resolution_hint: str
    player: int

    def __call__(self, state: CollectionState) -> bool:
        if self.resolution_hint == 'Region' and self.spot not in state.multiworld.regions.region_cache[self.player]:
            return False
        return state.can_reach(self.spot, self.resolution_hint, self.player)

    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        return self, self(state)

    def __repr__(self):
        return f"Reach {self.resolution_hint} {self.spot}"


@dataclass(frozen=True)
class HasProgressionPercent(CombinableStardewRule):
    player: int
    percent: int

    def __post_init__(self):
        assert self.percent > 0, "HasProgressionPercent rule must be above 0%"
        assert self.percent <= 100, "HasProgressionPercent rule can't require more than 100% of items"

    @property
    def combination_key(self) -> Hashable:
        return HasProgressionPercent.__name__

    @property
    def value(self):
        return self.percent

    def __call__(self, state: CollectionState) -> bool:
        stardew_world: "StardewValleyWorld" = state.multiworld.worlds[self.player]
        total_count = stardew_world.total_progression_items
        needed_count = (total_count * self.percent) // 100
        player_state = state.prog_items[self.player]

        if needed_count <= len(player_state) - len(stardew_world.excluded_from_total_progression_items):
            return True

        total_count = 0
        for item, item_count in player_state.items():
            if item in stardew_world.excluded_from_total_progression_items:
                continue

            total_count += item_count
            if total_count >= needed_count:
                return True

        return False

    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        return self, self(state)

    def __repr__(self):
        return f"Received {self.percent}% progression items"
