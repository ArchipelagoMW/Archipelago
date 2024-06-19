from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property, singledispatch
from typing import Iterable

from BaseClasses import CollectionState
from worlds.generic.Rules import CollectionRule
from ...stardew_rule import StardewRule, AggregatingStardewRule, Count, Has, TotalReceived, Received, Reach

max_explanation_depth = 10


@dataclass
class RuleExplanation:
    rule: StardewRule
    state: CollectionState
    expected: bool
    sub_rules: Iterable[StardewRule] = field(default_factory=list)

    def summary(self, depth=0):
        return "  " * depth + f"{str(self.rule)} -> {self.result}"

    def __str__(self, depth=0):
        if not self.sub_rules or depth >= max_explanation_depth:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(RuleExplanation.__str__(i, depth + 1)
                                                      if i.result is not self.expected else i.summary(depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    def __repr__(self, depth=0):
        if not self.sub_rules or depth >= max_explanation_depth:
            return self.summary(depth)

        return self.summary(depth) + "\n" + "\n".join(RuleExplanation.__repr__(i, depth + 1)
                                                      for i in sorted(self.explained_sub_rules, key=lambda x: x.result))

    @cached_property
    def result(self):
        return self.rule(self.state)

    @cached_property
    def explained_sub_rules(self):
        return [_explain(i, self.state, self.expected) for i in self.sub_rules]


def explain(rule: CollectionRule, state: CollectionState, expected: bool = True) -> RuleExplanation:
    if isinstance(rule, StardewRule):
        return _explain(rule, state, expected)
    else:
        return f"Value of rule {str(rule)} was not {str(expected)} in {str(state)}"  # noqa


@singledispatch
def _explain(rule: StardewRule, state: CollectionState, expected: bool) -> RuleExplanation:
    return RuleExplanation(rule, state, expected)


@_explain.register
def _(rule: AggregatingStardewRule, state: CollectionState, expected: bool) -> RuleExplanation:
    return RuleExplanation(rule, state, expected, rule.original_rules)


@_explain.register
def _(rule: Count, state: CollectionState, expected: bool) -> RuleExplanation:
    return RuleExplanation(rule, state, expected, rule.rules)


@_explain.register
def _(rule: Has, state: CollectionState, expected: bool) -> RuleExplanation:
    return RuleExplanation(rule, state, expected, [rule.other_rules[rule.item]])


@_explain.register
def _(rule: TotalReceived, state: CollectionState, expected=True) -> RuleExplanation:
    return RuleExplanation(rule, state, expected, [Received(i, rule.player, 1) for i in rule.items])


@_explain.register
def _(rule: Reach, state: CollectionState, expected=True) -> RuleExplanation:
    access_rules = None
    if rule.resolution_hint == 'Location':
        spot = state.multiworld.get_location(rule.spot, rule.player)

        if isinstance(spot.access_rule, StardewRule):
            access_rules = [spot.access_rule, Reach(spot.parent_region.name, "Region", rule.player)]

    elif rule.resolution_hint == 'Entrance':
        spot = state.multiworld.get_entrance(rule.spot, rule.player)

        if isinstance(spot.access_rule, StardewRule):
            access_rules = [spot.access_rule, Reach(spot.parent_region.name, "Region", rule.player)]

    else:
        spot = state.multiworld.get_region(rule.spot, rule.player)
        access_rules = [*(Reach(e.name, "Entrance", rule.player) for e in spot.entrances)]

    if not access_rules:
        return RuleExplanation(rule, state, expected)

    return RuleExplanation(rule, state, expected, access_rules)
