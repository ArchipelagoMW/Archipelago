from __future__ import annotations

import collections
import enum
from dataclasses import dataclass, field
from functools import cached_property, singledispatch
from typing import Iterable, List, Optional, Set, Tuple

from BaseClasses import CollectionState, Entrance, Location, MultiWorld, Region
from worlds.generic.Rules import CollectionRule

from . import (AggregatingStardewRule, Count, Has, Reach, Received,
               StardewRule, TotalReceived, true_)


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
            assert exit.connected_region is not None, f"All exits should be connected, error at {exit}"
            neighbor = exit.connected_region

            # Always record the directed edge
            dest_graph[checking_region.name].add(neighbor.name)
            source_graph[neighbor.name].add(checking_region.name)

            # Traverse each region once to collect its exits
            if neighbor.name not in seen:
                seen.add(neighbor.name)
                to_check.append(neighbor)

    print("\n".join(f"{srcs} -> {name} -> {dest_graph[name]}" for name, srcs in sorted(source_graph.items())))

    return source_graph


region_graph: dict[str, set[str]] | None = None
path_cache: dict[str, list[list[str]]] = {}


def all_simple_paths_to_origin(start: str) -> list[list[str]]:
    if path_cache.get(start) is not None:
        return path_cache[start]
    results: list[list[str]] = []

    def dfs(current: str, path: list[str], visited: set[str]):
        assert region_graph is not None
        if current == "Stardew Valley":
            results.append(path.copy())
            return

        for parent in region_graph[current]:
            if parent not in visited:
                visited.add(parent)
                path.append(parent)
                dfs(parent, path, visited)
                path.pop()
                visited.remove(parent)

    dfs(start, [start], {start})
    path_cache[start] = results
    return results


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
    sub_rules: Iterable[StardewRule] = field(default_factory=list)
    more_explanations: List[StardewRule] = field(default_factory=list, repr=False, hash=False)
    explored_rules_key: Set[Tuple[str, str]] = field(default_factory=set, repr=False, hash=False)
    current_rule_explored: bool = False

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

        if self.mode == ExplainMode.CLIENT:
            sub_explanations = []
            for sub_rule in self.sub_rules:
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
                        )
                    )

            return sub_explanations

        return [
            _explain(sub_rule, self.state, self.expected, self.mode, self.more_explanations, self.explored_rules_key)
            for sub_rule in self.sub_rules
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
                _explain(rule, self.state, self.expected, self.mode, self.more_explanations, self.explored_rules_key),
                count,
            )
            for rule, count in self.rule.counter.items()
        ]


def explain(
    rule: CollectionRule, state: CollectionState, expected: bool | None = True, mode: ExplainMode = ExplainMode.VERBOSE
) -> RuleExplanation:
    if isinstance(rule, StardewRule):
        return _explain(rule, state, expected, mode, more_explanations=list(), explored_spots=set())
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
) -> RuleExplanation:
    return RuleExplanation(
        rule, state, expected, mode, more_explanations=more_explanations, explored_rules_key=explored_spots
    )


@_explain.register
def _(
    rule: AggregatingStardewRule,
    state: CollectionState,
    expected: bool | None,
    mode: ExplainMode,
    more_explanations: list[StardewRule],
    explored_spots: Set[Tuple[str, str]],
) -> RuleExplanation:
    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        rule.original_rules,
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
    )


@_explain.register
def _(
    rule: Count,
    state: CollectionState,
    expected: bool | None,
    mode: ExplainMode,
    more_explanations: list[StardewRule],
    explored_spots: Set[Tuple[str, str]],
) -> RuleExplanation:
    return CountExplanation(
        rule, state, expected, mode, rule.rules, more_explanations=more_explanations, explored_rules_key=explored_spots
    )


@_explain.register
def _(
    rule: Has,
    state: CollectionState,
    expected: bool | None,
    mode: ExplainMode,
    more_explanations: list[StardewRule],
    explored_spots: Set[Tuple[str, str]],
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
        )
    except KeyError:
        return RuleExplanation(
            rule, state, expected, mode, more_explanations=more_explanations, explored_rules_key=explored_spots
        )


@_explain.register
def _(
    rule: TotalReceived,
    state: CollectionState,
    expected: bool | None,
    mode: ExplainMode,
    more_explanations: list[StardewRule],
    explored_spots: Set[Tuple[str, str]],
) -> RuleExplanation:
    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        [Received(i, rule.player, 1) for i in rule.items],
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
    )


@_explain.register
def _(
    rule: Reach,
    state: CollectionState,
    expected: bool | None,
    mode: ExplainMode,
    more_explanations: list[StardewRule],
    explored_spots: set[Tuple[str, str]],
) -> RuleExplanation:
    access_rules: list[StardewRule] = []
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
        ), f"Spot of location should have a parent region, problem in {spot.name}"

        if isinstance(spot.access_rule, StardewRule) and spot.access_rule is not true_:
            access_rules.append(spot.access_rule)
        access_rules.append(Reach(spot.parent_region.name, "Region", rule.player))
    else:
        spot = state.multiworld.get_region(rule.spot, rule.player)

        global region_graph
        if region_graph is None:
            region_graph = access_graph(state.multiworld, rule.player)

        paths = all_simple_paths_to_origin(spot.name)

        # Keep only immediate parents that appear in at least one loop-free path
        valid_parent_regions: set[str] = set()
        for path in paths:
            if len(path) >= 2:
                valid_parent_regions.add(path[1])

        for entrance in spot.entrances:
            assert isinstance(
                entrance.parent_region, Region
            ), f"Entrance to region should have a parent region, problem is {entrance.name}"

            if entrance.parent_region.name in valid_parent_regions:
                access_rules.append(Reach(entrance.name, "Entrance", rule.player))
    if len(access_rules) == 0:
        return RuleExplanation(
            rule, state, expected, mode, more_explanations=more_explanations, explored_rules_key=explored_spots
        )

    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        access_rules,
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
    )


@_explain.register
def _(
    rule: Received,
    state: CollectionState,
    expected: bool | None,
    mode: ExplainMode,
    more_explanations: list[StardewRule],
    explored_spots: Set[Tuple[str, str]],
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
            rule, state, expected, mode, more_explanations=more_explanations, explored_rules_key=explored_spots
        )

    return RuleExplanation(
        rule,
        state,
        expected,
        mode,
        access_rules,
        more_explanations=more_explanations,
        explored_rules_key=explored_spots,
    )


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
