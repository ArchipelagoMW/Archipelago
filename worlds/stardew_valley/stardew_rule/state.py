from dataclasses import dataclass
from typing import Iterable, Union, List, Tuple, Hashable

from BaseClasses import ItemClassification, CollectionState
from .base import BaseStardewRule, CombinableStardewRule
from .explanation import RuleExplanation, ExplainableRule
from .protocol import StardewRule
from ..items import item_table


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

        assert items_list, "Can't create a Total Received conditions without items"
        for item in items_list:
            assert item_table[item].classification & ItemClassification.progression, \
                f"Item [{item_table[item].name}] has to be progression to be used in logic"

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

    def get_difficulty(self):
        return self.count

    def __repr__(self):
        return f"Received {self.count} {self.items}"

    def explain(self, state: CollectionState, expected=True) -> RuleExplanation:
        return RuleExplanation(self, state, expected, [Received(i, self.player, 1) for i in self.items])


@dataclass(frozen=True)
class Received(CombinableStardewRule):
    item: str
    player: int
    count: int

    def __post_init__(self):
        assert item_table[self.item].classification & ItemClassification.progression, \
            f"Item [{item_table[self.item].name}] has to be progression to be used in logic"

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
            return f"Received {self.item}"
        return f"Received {self.count} {self.item}"

    def get_difficulty(self):
        return self.count


@dataclass(frozen=True)
class Reach(BaseStardewRule):
    spot: str
    resolution_hint: str
    player: int

    def __call__(self, state: CollectionState) -> bool:
        return state.can_reach(self.spot, self.resolution_hint, self.player)

    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        return self, self(state)

    def __repr__(self):
        return f"Reach {self.resolution_hint} {self.spot}"

    def get_difficulty(self):
        return 1

    def explain(self, state: CollectionState, expected=True) -> RuleExplanation:
        access_rules = None
        if self.resolution_hint == 'Location':
            spot = state.multiworld.get_location(self.spot, self.player)

            if isinstance(spot.access_rule, ExplainableRule):
                access_rules = [spot.access_rule, Reach(spot.parent_region.name, "Region", self.player)]

        elif self.resolution_hint == 'Entrance':
            spot = state.multiworld.get_entrance(self.spot, self.player)

            if isinstance(spot.access_rule, ExplainableRule):
                access_rules = [spot.access_rule, Reach(spot.parent_region.name, "Region", self.player)]

        else:
            spot = state.multiworld.get_region(self.spot, self.player)
            access_rules = [*(Reach(e.name, "Entrance", self.player) for e in spot.entrances)]

        if not access_rules:
            return RuleExplanation(self, state, expected)

        return RuleExplanation(self, state, expected, access_rules)


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
        stardew_world = state.multiworld.worlds[self.player]
        total_count = stardew_world.total_progression_items
        needed_count = (total_count * self.percent) // 100
        total_count = 0
        for item in state.prog_items[self.player]:
            item_count = state.prog_items[self.player][item]
            total_count += item_count
            if total_count >= needed_count:
                return True
        return False

    def evaluate_while_simplifying(self, state: CollectionState) -> Tuple[StardewRule, bool]:
        return self, self(state)

    def __repr__(self):
        return f"HasProgressionPercent {self.percent}"

    def get_difficulty(self):
        return self.percent
