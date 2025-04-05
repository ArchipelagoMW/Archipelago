from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property, singledispatch
from typing import Iterable, Set, Tuple, List, Optional

from BaseClasses import CollectionState, Location, Entrance
from worlds.generic.Rules import CollectionRule
from . import StardewRule, AggregatingStardewRule, Count, Has, TotalReceived, Received, Reach, true_


@dataclass
class RuleExplanation:
    rule: StardewRule
    state: CollectionState = field(repr=False, hash=False)
    expected: bool
    sub_rules: Iterable[StardewRule] = field(default_factory=list)
    explored_rules_key: Set[Tuple[str, str]] = field(default_factory=set, repr=False, hash=False)
    current_rule_explored: bool = False

    def __post_init__(self):
        checkpoint = _rule_key(self.rule)
        if checkpoint is not None and checkpoint in self.explored_rules_key:
            self.current_rule_explored = True
            self.sub_rules = []

    def summary(self, depth=0) -> str:
        summary = "  " * depth + f"{str(self.rule)} -> {self.result}"
        if self.current_rule_explored:
            summary += " [Already explained]"
        return summary

    def __str__(self, depth=0):
        if not self.sub_rules:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(i.__str__(depth + 1)
                                                      if i.result is not self.expected else i.summary(depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    @cached_property
    def result(self) -> bool:
        try:
            return self.rule(self.state)
        except KeyError:
            return False

    @cached_property
    def explained_sub_rules(self) -> List[RuleExplanation]:
        rule_key = _rule_key(self.rule)
        if rule_key is not None:
            self.explored_rules_key.add(rule_key)

        return [_explain(i, self.state, self.expected, self.explored_rules_key) for i in self.sub_rules]


@dataclass
class CountSubRuleExplanation(RuleExplanation):
    count: int = 1

    @staticmethod
    def from_explanation(expl: RuleExplanation, count: int) -> CountSubRuleExplanation:
        return CountSubRuleExplanation(expl.rule, expl.state, expl.expected, expl.sub_rules, expl.explored_rules_key, expl.current_rule_explored, count)

    def summary(self, depth=0) -> str:
        summary = "  " * depth + f"{self.count}x {str(self.rule)} -> {self.result}"
        if self.current_rule_explored:
            summary += " [Already explained]"
        return summary


@dataclass
class CountExplanation(RuleExplanation):
    rule: Count

    @cached_property
    def explained_sub_rules(self) -> List[RuleExplanation]:
        return [
            CountSubRuleExplanation.from_explanation(_explain(rule, self.state, self.expected, self.explored_rules_key), count)
            for rule, count in self.rule.counter.items()
        ]


def explain(rule: CollectionRule, state: CollectionState, expected: bool = True) -> RuleExplanation:
    if isinstance(rule, StardewRule):
        return _explain(rule, state, expected, explored_spots=set())
    else:
        return f"Value of rule {str(rule)} was not {str(expected)} in {str(state)}"  # noqa


@singledispatch
def _explain(rule: StardewRule, state: CollectionState, expected: bool, explored_spots: Set[Tuple[str, str]]) -> RuleExplanation:
    return RuleExplanation(rule, state, expected, explored_rules_key=explored_spots)


@_explain.register
def _(rule: AggregatingStardewRule, state: CollectionState, expected: bool, explored_spots: Set[Tuple[str, str]]) -> RuleExplanation:
    return RuleExplanation(rule, state, expected, rule.original_rules, explored_rules_key=explored_spots)


@_explain.register
def _(rule: Count, state: CollectionState, expected: bool, explored_spots: Set[Tuple[str, str]]) -> RuleExplanation:
    return CountExplanation(rule, state, expected, rule.rules, explored_rules_key=explored_spots)


@_explain.register
def _(rule: Has, state: CollectionState, expected: bool, explored_spots: Set[Tuple[str, str]]) -> RuleExplanation:
    try:
        return RuleExplanation(rule, state, expected, [rule.other_rules[rule.item]], explored_rules_key=explored_spots)
    except KeyError:
        return RuleExplanation(rule, state, expected, explored_rules_key=explored_spots)


@_explain.register
def _(rule: TotalReceived, state: CollectionState, expected: bool, explored_spots: Set[Tuple[str, str]]) -> RuleExplanation:
    return RuleExplanation(rule, state, expected, [Received(i, rule.player, 1) for i in rule.items], explored_rules_key=explored_spots)


@_explain.register
def _(rule: Reach, state: CollectionState, expected: bool, explored_spots: Set[Tuple[str, str]]) -> RuleExplanation:
    access_rules = None
    if rule.resolution_hint == 'Location':
        spot = state.multiworld.get_location(rule.spot, rule.player)

        if isinstance(spot.access_rule, StardewRule):
            if spot.access_rule is true_:
                access_rules = [Reach(spot.parent_region.name, "Region", rule.player)]
            else:
                access_rules = [spot.access_rule, Reach(spot.parent_region.name, "Region", rule.player)]
        elif spot.access_rule == Location.access_rule:
            # Sometime locations just don't have an access rule and all the relevant logic is in the parent region.
            access_rules = [Reach(spot.parent_region.name, "Region", rule.player)]


    elif rule.resolution_hint == 'Entrance':
        spot = state.multiworld.get_entrance(rule.spot, rule.player)

        if isinstance(spot.access_rule, StardewRule):
            if spot.access_rule is true_:
                access_rules = [Reach(spot.parent_region.name, "Region", rule.player)]
            else:
                access_rules = [spot.access_rule, Reach(spot.parent_region.name, "Region", rule.player)]
        elif spot.access_rule == Entrance.access_rule:
            # Sometime entrances just don't have an access rule and all the relevant logic is in the parent region.
            access_rules = [Reach(spot.parent_region.name, "Region", rule.player)]

    else:
        spot = state.multiworld.get_region(rule.spot, rule.player)
        access_rules = [*(Reach(e.name, "Entrance", rule.player) for e in spot.entrances)]

    if not access_rules:
        return RuleExplanation(rule, state, expected, explored_rules_key=explored_spots)

    return RuleExplanation(rule, state, expected, access_rules, explored_rules_key=explored_spots)


@_explain.register
def _(rule: Received, state: CollectionState, expected: bool, explored_spots: Set[Tuple[str, str]]) -> RuleExplanation:
    access_rules = None
    if rule.event:
        try:
            spot = state.multiworld.get_location(rule.item, rule.player)
            if spot.access_rule is true_:
                access_rules = [Reach(spot.parent_region.name, "Region", rule.player)]
            else:
                access_rules = [spot.access_rule, Reach(spot.parent_region.name, "Region", rule.player)]
        except KeyError:
            pass

    if not access_rules:
        return RuleExplanation(rule, state, expected, explored_rules_key=explored_spots)

    return RuleExplanation(rule, state, expected, access_rules, explored_rules_key=explored_spots)


@singledispatch
def _rule_key(_: StardewRule) -> Optional[Tuple[str, str]]:
    return None


@_rule_key.register
def _(rule: Reach) -> Tuple[str, str]:
    return rule.spot, rule.resolution_hint


@_rule_key.register
def _(rule: Received) -> Optional[Tuple[str, str]]:
    if not rule.event:
        return None

    return rule.item, "Logic Event"
