from __future__ import annotations

from dataclasses import dataclass, field
from functools import reduce, cached_property
from typing import Iterable, Dict, List, Union, FrozenSet, Optional, Sized

from BaseClasses import CollectionState, ItemClassification
from .items import item_table

MISSING_ITEM = "THIS ITEM IS MISSING"


@dataclass
class StardewRuleExplanation:
    rule: StardewRule
    state: CollectionState
    sub_rules: Iterable[StardewRule] = field(default_factory=set)

    def summary(self, depth=0):
        return "\t" * depth + f"{str(self.rule)} -> {self.result}"

    def __str__(self, depth=0):
        if not self.sub_rules:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(StardewRuleExplanation.__str__(i, depth + 1)
                                                      if i.result is False else i.summary(depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    def __repr__(self, depth=0):
        if not self.sub_rules:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(StardewRuleExplanation.__repr__(i, depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    @cached_property
    def result(self):
        return self.rule(self.state)

    @cached_property
    def explained_sub_rules(self):
        return [i.explain(self.state) for i in self.sub_rules]


class StardewRule:
    def __call__(self, state: CollectionState) -> bool:
        raise NotImplementedError

    def __or__(self, other) -> StardewRule:
        if other is true_ or other is false_ or type(other) is Or:
            return other | self

        return Or(self, other)

    def __and__(self, other) -> StardewRule:
        if other is true_ or other is false_ or type(other) is And:
            return other & self

        return And(self, other)

    def get_difficulty(self):
        raise NotImplementedError

    def simplify(self) -> StardewRule:
        return self

    def explain(self, state: CollectionState) -> StardewRuleExplanation:
        return StardewRuleExplanation(self, state)


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

_default_has_progression_percent = object()


class Or(StardewRule):
    rules: FrozenSet[StardewRule]

    _simplified: bool
    _has_progression_percent: Optional[HasProgressionPercent]
    _detailed_rules: FrozenSet[StardewRule]

    def __init__(self, *rules: StardewRule, _has_progression_percent=_default_has_progression_percent):
        self._simplified = False

        if _has_progression_percent is _default_has_progression_percent:
            assert rules, "Can't create a Or conditions without rules"
            _has_progression_percent = HasProgressionPercent.reduce_or([i for i in rules if type(i) is HasProgressionPercent])
            if rules is not None:
                rules = (i for i in rules if type(i) is not HasProgressionPercent)

        self.rules = frozenset(rules)
        self._detailed_rules = self.rules
        self._has_progression_percent = _has_progression_percent

    def __call__(self, state: CollectionState) -> bool:
        self.simplify()
        return any(rule(state) for rule in self.rules)

    def __str__(self):
        prefix = str(self._has_progression_percent) + " | " if self._has_progression_percent else ""
        return f"({prefix}{' | '.join(str(rule) for rule in self._detailed_rules)})"

    def __repr__(self):
        prefix = repr(self._has_progression_percent) + " | " if self._has_progression_percent else ""
        return f"({prefix}{' | '.join(repr(rule) for rule in self._detailed_rules)})"

    def __or__(self, other):
        if other is true_ or other is false_:
            return other | self

        if type(other) is HasProgressionPercent:
            if self._has_progression_percent:
                return Or(*self.rules, _has_progression_percent=self._has_progression_percent | other)
            return Or(*self.rules, _has_progression_percent=other)

        if type(other) is Or:
            return Or(*self.rules.union(other.rules), _has_progression_percent=self._has_progression_percent)

        return Or(*self.rules.union({other}), _has_progression_percent=self._has_progression_percent)

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

        rules = self.rules.union({self._has_progression_percent}) if self._has_progression_percent else self.rules
        simplified_rules = [simplified
                            for simplified in {rule.simplify() for rule in rules}
                            if simplified is not false_]

        if not simplified_rules:
            return false_

        if len(simplified_rules) == 1:
            return simplified_rules[0]

        self.rules = frozenset(simplified_rules)
        self._simplified = True
        return self

    def explain(self, state: CollectionState) -> StardewRuleExplanation:
        return StardewRuleExplanation(self, state, self._detailed_rules)


class And(StardewRule):
    rules: FrozenSet[StardewRule]

    _simplified: bool
    _has_progression_percent: Optional[HasProgressionPercent]
    _detailed_rules: FrozenSet[StardewRule]

    def __init__(self, *rules: StardewRule, _has_progression_percent=_default_has_progression_percent):
        self._simplified = False

        if _has_progression_percent is _default_has_progression_percent:
            assert rules, "Can't create a And conditions without rules"
            _has_progression_percent = HasProgressionPercent.reduce_and([i for i in rules if type(i) is HasProgressionPercent])
            if rules is not None:
                rules = (i for i in rules if type(i) is not HasProgressionPercent)

        self.rules = frozenset(rules)
        self._detailed_rules = self.rules
        self._has_progression_percent = _has_progression_percent

    def __call__(self, state: CollectionState) -> bool:
        self.simplify()
        result = all(rule(state) for rule in self.rules)
        return result

    def __str__(self):
        prefix = str(self._has_progression_percent) + " & " if self._has_progression_percent else ""
        return f"({prefix}{' & '.join(str(rule) for rule in self._detailed_rules)})"

    def __repr__(self):
        prefix = repr(self._has_progression_percent) + " & " if self._has_progression_percent else ""
        return f"({prefix}{' & '.join(repr(rule) for rule in self._detailed_rules)})"

    def __and__(self, other):
        if other is true_ or other is false_:
            return other & self

        if type(other) is HasProgressionPercent:
            if self._has_progression_percent:
                return And(*self.rules, _has_progression_percent=self._has_progression_percent & other)
            return And(*self.rules, _has_progression_percent=other)

        if type(other) is And:
            return And(*self.rules.union(other.rules), _has_progression_percent=self._has_progression_percent)

        return And(*self.rules.union({other}), _has_progression_percent=self._has_progression_percent)

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

        rules = self.rules.union({self._has_progression_percent}) if self._has_progression_percent else self.rules
        simplified_rules = [simplified
                            for simplified in {rule.simplify() for rule in rules}
                            if simplified is not true_]

        if not simplified_rules:
            return true_

        if len(simplified_rules) == 1:
            return simplified_rules[0]

        self.rules = frozenset(simplified_rules)
        self._simplified = True
        return self

    def explain(self, state: CollectionState) -> StardewRuleExplanation:
        return StardewRuleExplanation(self, state, self._detailed_rules)


class Count(StardewRule):
    count: int
    rules: List[StardewRule]
    _simplified: bool

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
        self._simplified = False

    def __call__(self, state: CollectionState) -> bool:
        self.simplify()
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
        if self._simplified:
            return self

        simplified_rules = [rule.simplify() for rule in self.rules]
        self.rules = simplified_rules
        self._simplified = True
        return self

    def explain(self, state: CollectionState) -> StardewRuleExplanation:
        return StardewRuleExplanation(self, state, self.rules)


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

    def __repr__(self):
        return f"Received {self.count} {self.items}"

    def get_difficulty(self):
        return self.count

    def explain(self, state: CollectionState) -> StardewRuleExplanation:
        return StardewRuleExplanation(self, state, [Received(i, self.player, 1) for i in self.items])


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

    def explain(self, state: CollectionState) -> StardewRuleExplanation:
        # FIXME this should be in core
        if self.resolution_hint == 'Location':
            spot = state.multiworld.get_location(self.spot, self.player)
            # TODO explain virtual reach for room
            access_rule = spot.access_rule
        elif self.resolution_hint == 'Entrance':
            spot = state.multiworld.get_entrance(self.spot, self.player)
            access_rule = spot.access_rule
        else:
            # default to Region
            spot = state.multiworld.get_region(self.spot, self.player)
            # TODO check entrances rules
            access_rule = None

        if not isinstance(access_rule, StardewRule):
            return StardewRuleExplanation(self, state)

        return StardewRuleExplanation(self, state, [access_rule])


class Has(StardewRule):
    item: str
    # For sure there is a better way than just passing all the rules everytime
    other_rules: Dict[str, StardewRule]

    def __init__(self, item: str, other_rules: Dict[str, StardewRule]):
        self.item = item
        self.other_rules = other_rules

    def __call__(self, state: CollectionState) -> bool:
        self.simplify()
        return self.other_rules[self.item](state)

    def __str__(self):
        if self.item not in self.other_rules:
            return f"Has {self.item} -> {MISSING_ITEM}"
        return f"Has {self.item}"

    def __repr__(self):
        if self.item not in self.other_rules:
            return f"Has {self.item} -> {MISSING_ITEM}"
        return f"Has {self.item} -> {repr(self.other_rules[self.item])}"

    def get_difficulty(self):
        return self.other_rules[self.item].get_difficulty() + 1

    def __hash__(self):
        return hash(self.item)

    def simplify(self) -> StardewRule:
        return self.other_rules[self.item].simplify()

    def explain(self, state: CollectionState) -> StardewRuleExplanation:
        return StardewRuleExplanation(self, state, [self.other_rules[self.item]])


@dataclass(frozen=True)
class HasProgressionPercent(StardewRule):
    player: int
    percent: int

    # Cache in __new__

    @staticmethod
    def reduce_and(rules: Union[Iterable[HasProgressionPercent], Sized]) -> Optional[HasProgressionPercent]:
        if not rules:
            return None
        if len(rules) == 1:
            return next(iter(rules))
        return reduce(HasProgressionPercent.__and__, rules)  # noqa

    @staticmethod
    def reduce_or(rules: Union[Iterable[HasProgressionPercent], Sized]) -> Optional[HasProgressionPercent]:
        if not rules:
            return None
        if len(rules) == 1:
            return next(iter(rules))
        return reduce(HasProgressionPercent.__or__, rules)  # noqa

    def __post_init__(self):
        assert self.percent > 0, "HasProgressionPercent rule must be above 0%"
        assert self.percent <= 100, "HasProgressionPercent rule can't require more than 100% of items"

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

    def __repr__(self):
        return f"HasProgressionPercent {self.percent}"

    def __and__(self, other):
        if type(other) is HasProgressionPercent:
            return max(self, other, key=lambda x: x.percent)
        return super().__and__(other)

    def __or__(self, other):
        if type(other) is HasProgressionPercent:
            return min(self, other, key=lambda x: x.percent)
        return super().__or__(other)

    def get_difficulty(self):
        return self.percent
