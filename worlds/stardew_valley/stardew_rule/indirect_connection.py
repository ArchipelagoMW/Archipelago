from functools import singledispatch
from typing import Set

from . import StardewRule, Reach, Count, AggregatingStardewRule, Has


def look_for_indirect_connection(rule: StardewRule) -> Set[str]:
    required_regions = set()
    _find(rule, required_regions, depth=0)
    return required_regions


@singledispatch
def _find(rule: StardewRule, regions: Set[str], depth: int):
    ...


@_find.register
def _(rule: AggregatingStardewRule, regions: Set[str], depth: int):
    assert depth < 50, "Recursion depth exceeded"
    for r in rule.original_rules:
        _find(r, regions, depth + 1)


@_find.register
def _(rule: Count, regions: Set[str], depth: int):
    assert depth < 50, "Recursion depth exceeded"
    for r in rule.rules:
        _find(r, regions, depth + 1)


@_find.register
def _(rule: Has, regions: Set[str], depth: int):
    assert depth < 50, f"Recursion depth exceeded on {rule.item}"
    r = rule.other_rules[rule.item]
    _find(r, regions, depth + 1)


@_find.register
def _(rule: Reach, regions: Set[str], depth: int):
    assert depth < 50, "Recursion depth exceeded"
    if rule.resolution_hint == "Region":
        regions.add(rule.spot)
