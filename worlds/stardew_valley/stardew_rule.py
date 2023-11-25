from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Dict, List, Union, FrozenSet, Set

from BaseClasses import CollectionState, ItemClassification
from .items import item_table

MISSING_ITEM = "THIS ITEM IS MISSING"


class StardewRule:
    def __call__(self, state: CollectionState) -> bool:
        raise NotImplementedError

    def __or__(self, other) -> StardewRule:
        if type(other) is Or:
            return Or(self, *other.rules)

        return Or(self, other)

    def __and__(self, other) -> StardewRule:
        if type(other) is And:
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


false_ = False_()
true_ = True_()
assert false_ is False_()
assert true_ is True_()


class Or(StardewRule):
    rules: FrozenSet[StardewRule]
    _simplified: bool

    def __init__(self, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list: Set[StardewRule]

        if isinstance(rule, Iterable):
            rules_list = {*rule}
        else:
            rules_list = {rule}

        if rules is not None:
            rules_list.update(rules)

        assert rules_list, "Can't create a Or conditions without rules"

        if any(type(rule) is Or for rule in rules_list):
            new_rules: Set[StardewRule] = set()
            for rule in rules_list:
                if type(rule) is Or:
                    new_rules.update(rule.rules)
                else:
                    new_rules.add(rule)
            rules_list = new_rules

        self.rules = frozenset(rules_list)
        self._simplified = False

    def __call__(self, state: CollectionState) -> bool:
        return any(rule(state) for rule in self.rules)

    def __repr__(self):
        return f"({' | '.join(repr(rule) for rule in self.rules)})"

    def __or__(self, other):
        if other is true_:
            return other
        if other is false_:
            return self
        if type(other) is Or:
            return Or(self.rules.union(other.rules))

        return Or(self.rules.union({other}))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.rules == self.rules

    def __hash__(self):
        return hash(self.rules)

    def get_difficulty(self):
        return min(rule.get_difficulty() for rule in self.rules)

    def simplify(self) -> StardewRule:
        if self._simplified:
            return self
        if true_ in self.rules:
            return true_

        simplified_rules = [simplified for simplified in {rule.simplify() for rule in self.rules}
                            if simplified is not false_]

        if not simplified_rules:
            return false_

        if len(simplified_rules) == 1:
            return simplified_rules[0]

        self.rules = frozenset(simplified_rules)
        self._simplified = True
        return self


class And(StardewRule):
    rules: FrozenSet[StardewRule]
    _simplified: bool

    def __init__(self, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list: Set[StardewRule]

        if isinstance(rule, Iterable):
            rules_list = {*rule}
        else:
            rules_list = {rule}

        if rules is not None:
            rules_list.update(rules)

        if not rules_list:
            rules_list.add(true_)
        elif any(type(rule) is And for rule in rules_list):
            new_rules: Set[StardewRule] = set()
            for rule in rules_list:
                if type(rule) is And:
                    new_rules.update(rule.rules)
                else:
                    new_rules.add(rule)
            rules_list = new_rules

        self.rules = frozenset(rules_list)
        self._simplified = False

    def __call__(self, state: CollectionState) -> bool:
        return all(rule(state) for rule in self.rules)

    def __repr__(self):
        return f"({' & '.join(repr(rule) for rule in self.rules)})"

    def __and__(self, other):
        if other is true_:
            return self
        if other is false_:
            return other
        if type(other) is And:
            return And(self.rules.union(other.rules))

        return And(self.rules.union({other}))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.rules == self.rules

    def __hash__(self):
        return hash(self.rules)

    def get_difficulty(self):
        return max(rule.get_difficulty() for rule in self.rules)

    def simplify(self) -> StardewRule:
        if self._simplified:
            return self
        if false_ in self.rules:
            return false_

        simplified_rules = [simplified for simplified in {rule.simplify() for rule in self.rules}
                            if simplified is not true_]

        if not simplified_rules:
            return true_

        if len(simplified_rules) == 1:
            return simplified_rules[0]

        self.rules = frozenset(simplified_rules)
        self._simplified = True
        return self


class Count(StardewRule):
    count: int
    rules: List[StardewRule]

    def __init__(self, count: int, rule: Union[StardewRule, Iterable[StardewRule]], *rules: StardewRule):
        rules_list: List[StardewRule]

        if isinstance(rule, Iterable):
            rules_list = [*rule]
        else:
            rules_list = [rule]

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
        items_list: List[str]

        if isinstance(items, Iterable):
            items_list = [*items]
        else:
            items_list = [items]

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
            f"Item [{item_table[self.item].name}] has to be progression to be used in logic"

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
