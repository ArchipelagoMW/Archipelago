from __future__ import annotations

import collections
import enum
from dataclasses import dataclass, field
from functools import cached_property, singledispatch
from typing import Iterable, List, Optional, Set, Tuple

from BaseClasses import CollectionState, MultiWorld, Region
from worlds.generic.Rules import CollectionRule
from . import (AggregatingStardewRule, Count, Has, Reach, Received,
               StardewRule, TotalReceived, true_, false_)


class ExplainMode(enum.Enum):
    VERBOSE = enum.auto()
    CLIENT = enum.auto()


def access_graph(multiworld: MultiWorld, player: int):
    stardew = multiworld.get_region("Stardew Valley", player)

    source_graph: dict[str, set[str]] = {}
    dest_graph: dict[str, set[str]] = {}

    for region in multiworld.get_regions(player):
        source_graph[region.name] = set()  # incoming
        dest_graph[region.name] = set()  # outgoing

    to_check = collections.deque([stardew])
    seen = {stardew.name}

    while to_check:
        checking_region = to_check.popleft()

        for exit in checking_region.exits:
            if exit.connected_region is None:
                continue
            neighbor = exit.connected_region

            # Always record the directed edge
            dest_graph[checking_region.name].add(neighbor.name)
            source_graph[neighbor.name].add(checking_region.name)

            # Traverse each region once to collect its exits
            if neighbor.name not in seen:
                seen.add(neighbor.name)
                to_check.append(neighbor)

    for region in multiworld.get_regions(player):
        assert (
                source_graph.get(region.name) is not None
        ), f"#{region.name} is missing\nsg = {source_graph}\ndg = {dest_graph}"
    return source_graph


region_graph: dict[str, set[str]] | None = None
valid_parent_cache: dict[str, set[str]] = {}

SubRule = StardewRule | tuple[StardewRule, frozenset[str]]


def _is_origin(region_name: str) -> bool:
    return region_name in {"Stardew Valley", "Farmhouse"}


def _has_path_to_origin(start: str, visited: set[str]) -> bool:
    assert region_graph is not None

    if _is_origin(start):
        return True

    for parent in region_graph.get(start, ()):
        if parent in visited:
            continue

        visited.add(parent)
        if _has_path_to_origin(parent, visited):
            visited.remove(parent)
            return True
        visited.remove(parent)

    return False


def valid_parents_to_origin(region: str) -> set[str]:
    cached = valid_parent_cache.get(region)
    if cached is not None:
        return cached

    assert region_graph is not None
    result: set[str] = set()

    for parent in region_graph.get(region, ()):
        if parent == region:
            continue
        if _is_origin(parent):
            result.add(parent)
            continue
        if _has_path_to_origin(parent, {region, parent}):
            result.add(parent)

    valid_parent_cache[region] = result
    return result


@dataclass
class MoreExplanation:
    rule: StardewRule
    state: CollectionState
    more_index: int
    mode: ExplainMode

    @cached_property
    def result(self) -> bool:
        try:
            return self.rule(self.state)
        except KeyError:
            return False

    def summary(self, depth=0) -> str:
        if self.mode is ExplainMode.CLIENT:
            depth *= 2

        line = "  " * depth + f"{str(self.rule)} -> {self.result}"
        line += f" [use `/explain_more {self.more_index}` to explain]"

        return line

    def __str__(self, depth=0):
        return self.summary(depth)


@dataclass
class RuleExplanation:
    rule: StardewRule
    state: CollectionState = field(repr=False, hash=False)
    expected: bool | None
    mode: ExplainMode
    sub_rules: Iterable[SubRule] = field(default_factory=list)
    more_explanations: list[StardewRule] = field(default_factory=list, repr=False, hash=False)
    explored_rules_key: set[tuple[str, str]] = field(default_factory=set, repr=False, hash=False)
    current_rule_explored: bool = False
    blocked_regions: frozenset[str] = field(default_factory=frozenset, repr=False, hash=False)

    def __post_init__(self):
        checkpoint = _rule_key(self.rule)
        if checkpoint is not None and checkpoint in self.explored_rules_key:
            self.current_rule_explored = True
            self.sub_rules = []

    def summary(self, depth=0) -> str:
        if self.mode is ExplainMode.CLIENT:
            depth *= 2

        line = "  " * depth + f"{str(self.rule)} -> {self.result}"
        if self.current_rule_explored:
            line += " [Already explained]"

        return line

    def __str__(self, depth=0):
        if not self.sub_rules:
            return self.summary(depth)

        return (
                self.summary(depth)
                + "\n"
                + "\n".join(
            i.__str__(depth + 1) if self.expected is None or i.result is not self.expected else i.summary(depth + 1)
            for i in sorted(self.explained_sub_rules, key=lambda x: x.result)
        )
        )

    def more(self, more_index: int) -> RuleExplanation:
        return explain(self.more_explanations[more_index], self.state, self.expected, self.mode)

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

        def unpack(sub_rule: SubRule) -> tuple[StardewRule, frozenset[str]]:
            if isinstance(sub_rule, tuple):
                return sub_rule
            return sub_rule, frozenset()

        if self.mode == ExplainMode.CLIENT:
            sub_explanations = []
            for sub_rule_like in self.sub_rules:
                sub_rule, extra_blocked_regions = unpack(sub_rule_like)
                merged_blocked_regions = (
                    self.blocked_regions | extra_blocked_regions if isinstance(sub_rule, Reach) else frozenset()
                )

                if isinstance(sub_rule, Reach) and sub_rule.resolution_hint == "Entrance":
                    sub_explanations.append(
                        MoreExplanation(sub_rule, self.state, len(self.more_explanations), self.mode)
                    )
                    self.more_explanations.append(sub_rule)
                elif isinstance(sub_rule, Reach) and sub_rule.resolution_hint == "Location":
                    sub_explanations.append(
                        MoreExplanation(sub_rule, self.state, len(self.more_explanations), self.mode)
                    )
                    self.more_explanations.append(sub_rule)
                else:
                    sub_explanations.append(
                        _explain(
                            sub_rule,
                            self.state,
                            self.expected,
                            self.mode,
                            self.more_explanations,
                            self.explored_rules_key,
                            merged_blocked_regions,
                        )
                    )

            return sub_explanations

        return [
            _explain(
                sub_rule,
                self.state,
                self.expected,
                self.mode,
                self.more_explanations,
                self.explored_rules_key,
                (self.blocked_regions | extra_blocked_regions) if isinstance(sub_rule, Reach) else frozenset(),
            )
            for sub_rule, extra_blocked_regions in (
                sr if isinstance(sr, tuple) else (sr, frozenset()) for sr in self.sub_rules
            )
        ]


@dataclass
class CountSubRuleExplanation(RuleExplanation):
    count: int = 1

    @staticmethod
    def from_explanation(expl: RuleExplanation, count: int) -> CountSubRuleExplanation:
        return CountSubRuleExplanation(
            expl.rule,
            expl.state,
            expl.expected,
            expl.mode,
            expl.sub_rules,
            more_explanations=expl.more_explanations,
            explored_rules_key=expl.explored_rules_key,
            current_rule_explored=expl.current_rule_explored,
            count=count,
            blocked_regions=expl.blocked_regions,
        )

    def summary(self, depth=0) -> str:
        if self.mode is ExplainMode.CLIENT:
            depth *= 2

        summary = "  " * depth + f"{self.count}x {str(self.rule)} -> {self.result}"
        if self.current_rule_explored:
            summary += " [Already explained]"
        return summary


@dataclass
class CountExplanation(RuleExplanation):
    rule: Count

    @cached_property
    def explained_sub_rules(self) -> List[RuleExplanation]:
        if all(value == 1 for value in self.rule.counter.values()):
            return super().explained_sub_rules

        return [
            CountSubRuleExplanation.from_explanation(
                _explain(
                    rule,
                    self.state,
                    self.expected,
                    self.mode,
                    self.more_explanations,
                    self.explored_rules_key,
                    self.blocked_regions if isinstance(rule, Reach) else frozenset(),
                ),
                count,
            )
            for rule, count in self.rule.counter.items()
        ]


def explain(
        rule: CollectionRule, state: CollectionState, expected: bool | None = True, mode: ExplainMode = ExplainMode.VERBOSE
) -> RuleExplanation:
    if isinstance(rule, StardewRule):
        explanation = _explain(
            rule, state, expected, mode, more_explanations=list(), explored_spots=set(), blocked_regions=frozenset()
        )
        # print(explanation)
        return explanation
    else:
        return f"Value of rule {str(rule)} was not {str(expected)} in {str(state)}"  # noqa


@singledispatch
def _explain(
        rule: StardewRule,
        state: CollectionState,
        expected: bool | None,
        mode: ExplainMode,
        more_explanations: list[StardewRule],
        explored_spots: Set[Tuple[str, str]],
        blocked_regions: frozenset[str],
) -> RuleExplanation:
    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
        blocked_regions=blocked_regions,
    )


@_explain.register
def _(
        rule: AggregatingStardewRule,
        state: CollectionState,
        expected: bool | None,
        mode: ExplainMode,
        more_explanations: list[StardewRule],
        explored_spots: Set[Tuple[str, str]],
        blocked_regions: frozenset[str],
) -> RuleExplanation:
    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        rule.simple_rules,
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
        blocked_regions=blocked_regions,
    )


@_explain.register
def _(
        rule: Count,
        state: CollectionState,
        expected: bool | None,
        mode: ExplainMode,
        more_explanations: list[StardewRule],
        explored_spots: Set[Tuple[str, str]],
        blocked_regions: frozenset[str],
) -> RuleExplanation:
    return CountExplanation(
        rule,
        state,
        expected,
        mode,
        rule.rules,
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
        blocked_regions=blocked_regions,
    )


@_explain.register
def _(
        rule: Has,
        state: CollectionState,
        expected: bool | None,
        mode: ExplainMode,
        more_explanations: list[StardewRule],
        explored_spots: Set[Tuple[str, str]],
        blocked_regions: frozenset[str],
) -> RuleExplanation:
    try:
        return RuleExplanation(
            rule,
            state,
            expected,
            mode,
            [rule.other_rules[rule.item]],
            more_explanations=more_explanations,
            explored_rules_key=explored_spots,
            blocked_regions=blocked_regions,
        )
    except KeyError:
        return RuleExplanation(
            rule,
            state,
            expected,
            mode,
            more_explanations=more_explanations,
            explored_rules_key=explored_spots,
            blocked_regions=blocked_regions,
        )


@_explain.register
def _(
        rule: TotalReceived,
        state: CollectionState,
        expected: bool | None,
        mode: ExplainMode,
        more_explanations: list[StardewRule],
        explored_spots: Set[Tuple[str, str]],
        blocked_regions: frozenset[str],
) -> RuleExplanation:
    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        [Received(i, rule.player, 1) for i in rule.items],
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
        blocked_regions=blocked_regions,
    )


@_explain.register
def _(
        rule: Reach,
        state: CollectionState,
        expected: bool | None,
        mode: ExplainMode,
        more_explanations: list[StardewRule],
        explored_spots: set[Tuple[str, str]],
        blocked_regions: frozenset[str],
) -> RuleExplanation:
    access_rules: list[SubRule] = []
    if rule.resolution_hint == "Location":
        spot = state.multiworld.get_location(rule.spot, rule.player)
        assert isinstance(
            spot.parent_region, Region
        ), f"Spot of location should have a parent region, problem in {spot.name}"

        if isinstance(spot.access_rule, StardewRule) and spot.access_rule is not true_:
            access_rules.append(spot.access_rule)
        access_rules.append(Reach(spot.parent_region.name, "Region", rule.player))

    elif rule.resolution_hint == "Entrance":
        spot = state.multiworld.get_entrance(rule.spot, rule.player)
        assert isinstance(
            spot.parent_region, Region
        ), f"Spot of entrance should have a parent region, problem in {spot.name}"

        if isinstance(spot.access_rule, StardewRule) and spot.access_rule is not true_:
            access_rules.append(spot.access_rule)

        newly_blocked = frozenset()
        if spot.connected_region is not None:
            newly_blocked = frozenset({spot.connected_region.name})

        access_rules.append((Reach(spot.parent_region.name, "Region", rule.player), newly_blocked))

    else:
        spot = state.multiworld.get_region(rule.spot, rule.player)

        global region_graph
        if region_graph is None or state.multiworld.worlds[rule.player].entrance_cache_invalid:
            valid_parent_cache.clear()
            region_graph = access_graph(state.multiworld, rule.player)
            state.multiworld.worlds[rule.player].entrance_cache_invalid = False

        valid_parent_regions = set(valid_parents_to_origin(spot.name))
        valid_parent_regions -= blocked_regions

        for entrance in spot.entrances:
            if entrance.parent_region is None:
                access_rules.append(false_)
                continue
            assert isinstance(
                entrance.parent_region, Region
            ), f"Entrance to region should have a parent region, problem is {entrance.name}"

            if entrance.parent_region.name in valid_parent_regions:
                access_rules.append(Reach(entrance.name, "Entrance", rule.player))
    if len(access_rules) == 0:
        return RuleExplanation(
            rule,
            state,
            expected,
            mode,
            more_explanations=more_explanations,
            explored_rules_key=explored_spots,
            blocked_regions=blocked_regions,
        )

    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        access_rules,
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
        blocked_regions=blocked_regions,
    )


@_explain.register
def _(
        rule: Received,
        state: CollectionState,
        expected: bool | None,
        mode: ExplainMode,
        more_explanations: list[StardewRule],
        explored_spots: Set[Tuple[str, str]],
        blocked_regions: frozenset[str],
) -> RuleExplanation:
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
        return RuleExplanation(
            rule,
            state,
            expected,
            mode,
            more_explanations=more_explanations,
            explored_rules_key=explored_spots,
            blocked_regions=blocked_regions,
        )

    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        access_rules,
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
        blocked_regions=blocked_regions,
    )


@singledispatch
def _rule_key(_: StardewRule) -> Optional[Tuple[str, str]]:
    return None


@_rule_key.register
def _(rule: Reach) -> Tuple[str, str]:
    return rule.spot, rule.resolution_hint


@_rule_key.register
def _(rule: Has) -> tuple[str, str]:
    return rule.item, "Has"


@_rule_key.register
def _(rule: Received) -> Optional[Tuple[str, str]]:
    if not rule.event:
        return None

    return rule.item, "Logic Event"


@_rule_key.register
def _(rule: AggregatingStardewRule) -> tuple[str, str]:
    return str(rule), "Aggregating"


@_rule_key.register
def _(rule: Count) -> tuple[str, str]:
    return str(rule.rules), str(rule.count)
