from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Dict, List, Union, FrozenSet

from BaseClasses import CollectionState, ItemClassification
from .items import item_table

MISSING_ITEM = "THIS ITEM IS MISSING"


class StardewRule:
    def __call__(self, state: CollectionState) -> bool:
        raise NotImplementedError

    def __or__(self, other) -> StardewRule:
        if isinstance(other, Or):
            return Or(self, *other.rules)

        return Or(self, other)

    def __and__(self, other) -> StardewRule:
        if isinstance(other, And):
            return And(other.rules.union({self}))

        return And(self, other)

    def get_difficulty(self):
        raise NotImplementedError

    def simplify(self) -> StardewRule:
        return self


class True_(StardewRule):  # noqa

    def __new__(cls, _cache=[]):  # noqa
        # Only one single instance will be ever created.
        if not _cache:
            _cache.append(super(True_, cls).__new__(cls))
        return _cache[0]

    def __call__(self, state: CollectionState) -> bool:
        return True

    def __or__(self, other) -> StardewRule:
        return self

    def __and__(self, other) -> StardewRule:
        return other

    def __repr__(self):
        return "True"

    def get_difficulty(self):
        return 0


class False_(StardewRule):  # noqa

    def __new__(cls, _cache=[]):  # noqa
        # Only one single instance will be ever created.
        if not _cache:
            _cache.append(super(False_, cls).__new__(cls))
        return _cache[0]

    def __call__(self, state: CollectionState) -> bool:
        return False

    def __or__(self, other) -> StardewRule:
        return other

    def __and__(self, other) -> StardewRule:
        return self

    def __repr__(self):
        return "False"

    def get_difficulty(self):
        return 999999999


class Or(StardewRule):
    rules: FrozenSet[StardewRule]

    def __init__(self, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list = set()
        if isinstance(rule, Iterable):
            rules_list.update(rule)
        else:
            rules_list.add(rule)

        if rules is not None:
            rules_list.update(rules)

        assert rules_list, "Can't create a Or conditions without rules"

        new_rules = set()
        for rule in rules_list:
            if isinstance(rule, Or):
                new_rules.update(rule.rules)
            else:
                new_rules.add(rule)
        rules_list = new_rules

        self.rules = frozenset(rules_list)

    def __call__(self, state: CollectionState) -> bool:
        return any(rule(state) for rule in self.rules)

    def __repr__(self):
        return f"({' | '.join(repr(rule) for rule in self.rules)})"

    def __or__(self, other):
        if isinstance(other, True_):
            return other
        if isinstance(other, False_):
            return self
        if isinstance(other, Or):
            return Or(self.rules.union(other.rules))

        return Or(self.rules.union({other}))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.rules == self.rules

    def __hash__(self):
        return hash(self.rules)

    def get_difficulty(self):
        return min(rule.get_difficulty() for rule in self.rules)

    def simplify(self) -> StardewRule:
        if any(isinstance(rule, True_) for rule in self.rules):
            return True_()

        simplified_rules = {rule.simplify() for rule in self.rules}
        simplified_rules = {rule for rule in simplified_rules if rule is not False_()}

        if not simplified_rules:
            return False_()

        if len(simplified_rules) == 1:
            return next(iter(simplified_rules))

        return Or(simplified_rules)


class And(StardewRule):
    rules: FrozenSet[StardewRule]

    def __init__(self, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list = set()
        if isinstance(rule, Iterable):
            rules_list.update(rule)
        else:
            rules_list.add(rule)

        if rules is not None:
            rules_list.update(rules)

        assert rules_list, "Can't create a And conditions without rules"

        new_rules = set()
        for rule in rules_list:
            if isinstance(rule, And):
                new_rules.update(rule.rules)
            else:
                new_rules.add(rule)
        rules_list = new_rules

        self.rules = frozenset(rules_list)

    def __call__(self, state: CollectionState) -> bool:
        return all(rule(state) for rule in self.rules)

    def __repr__(self):
        return f"({' & '.join(repr(rule) for rule in self.rules)})"

    def __and__(self, other):
        if isinstance(other, True_):
            return self
        if isinstance(other, False_):
            return other
        if isinstance(other, And):
            return And(self.rules.union(other.rules))

        return And(self.rules.union({other}))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.rules == self.rules

    def __hash__(self):
        return hash(self.rules)

    def get_difficulty(self):
        return max(rule.get_difficulty() for rule in self.rules)

    def simplify(self) -> StardewRule:
        if any(isinstance(rule, False_) for rule in self.rules):
            return False_()

        simplified_rules = {rule.simplify() for rule in self.rules}
        simplified_rules = {rule for rule in simplified_rules if rule is not True_()}

        if not simplified_rules:
            return True_()

        if len(simplified_rules) == 1:
            return next(iter(simplified_rules))

        return And(simplified_rules)


class Count(StardewRule):
    count: int
    rules: List[StardewRule]

    def __init__(self, count: int, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list = []
        if isinstance(rule, Iterable):
            rules_list.extend(rule)
        else:
            rules_list.append(rule)

        if rules is not None:
            rules_list.extend(rules)

        assert rules_list, "Can't create a Count conditions without rules"
        assert len(rules_list) >= count, "Count need at least as many rules at the count"

        self.rules = rules_list
        self.count = count

    def __call__(self, state: CollectionState) -> bool:
        c = 0
        for r in self.rules:
            if r(state):
                c += 1
            if c >= self.count:
                return True
        return False

    def __repr__(self):
        return f"Received {self.count} {repr(self.rules)}"

    def get_difficulty(self):
        rules_sorted_by_difficulty = sorted(self.rules, key=lambda x: x.get_difficulty())
        easiest_n_rules = rules_sorted_by_difficulty[0:self.count]
        return max(rule.get_difficulty() for rule in easiest_n_rules)

    def simplify(self):
        return Count(self.count, [rule.simplify() for rule in self.rules])


class TotalReceived(StardewRule):
    count: int
    items: Iterable[str]
    player: int

    def __init__(self, count: int, items: Union[str, Iterable[str]], player: int):
        items_list = []
        if isinstance(items, Iterable):
            items_list.extend(items)
        else:
            items_list.append(items)

        assert items_list, "Can't create a Total Received conditions without items"
        for item in items_list:
            assert item_table[item].classification & ItemClassification.progression, \
                "Item has to be progression to be used in logic"

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

    def __repr__(self):
        return f"Received {self.count} {self.items}"

    def get_difficulty(self):
        return self.count


@dataclass(frozen=True)
class Received(StardewRule):
    item: str
    player: int
    count: int

    def __post_init__(self):
        assert item_table[self.item].classification & ItemClassification.progression, \
            "Item has to be progression to be used in logic"

    def __call__(self, state: CollectionState) -> bool:
        return state.has(self.item, self.player, self.count)

    def __repr__(self):
        if self.count == 1:
            return f"Received {self.item}"
        return f"Received {self.count} {self.item}"

    def get_difficulty(self):
        if self.item == "Spring":
            return 0
        if self.item == "Summer":
            return 1
        if self.item == "Fall":
            return 2
        if self.item == "Winter":
            return 3
        return self.count


@dataclass(frozen=True)
class Reach(StardewRule):
    spot: str
    resolution_hint: str
    player: int

    def __call__(self, state: CollectionState) -> bool:
        return state.can_reach(self.spot, self.resolution_hint, self.player)

    def __repr__(self):
        return f"Reach {self.resolution_hint} {self.spot}"

    def get_difficulty(self):
        return 1


@dataclass(frozen=True)
class Has(StardewRule):
    item: str
    # For sure there is a better way than just passing all the rules everytime
    other_rules: Dict[str, StardewRule]

    def __call__(self, state: CollectionState) -> bool:
        if isinstance(self.item, str):
            return self.other_rules[self.item](state)

    def __repr__(self):
        if not self.item in self.other_rules:
            return f"Has {self.item} -> {MISSING_ITEM}"
        return f"Has {self.item} -> {repr(self.other_rules[self.item])}"

    def get_difficulty(self):
        return self.other_rules[self.item].get_difficulty() + 1

    def __hash__(self):
        return hash(self.item)

    def simplify(self) -> StardewRule:
        return self.other_rules[self.item].simplify()
