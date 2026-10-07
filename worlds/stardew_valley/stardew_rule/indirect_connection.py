from functools import singledispatch
from typing import Set

from . import StardewRule, Reach, Count, AggregatingStardewRule, Has

MAX_DEPTH = 100


def look_for_indirect_connection(rule: StardewRule) -> Set[str]:
    required_regions = set()
    items_to_ignore = set()
    _find(rule, required_regions, items_to_ignore, depth=0)
    return required_regions


@singledispatch
def _find(rule: StardewRule, regions: Set[str], items_to_ignore: Set[str], depth: int):
    ...


@_find.register
def _(rule: AggregatingStardewRule, regions: Set[str], items_to_ignore: Set[str], depth: int):
    assert depth < MAX_DEPTH, "Recursion depth exceeded"
    for r in rule.original_rules:
        _find(r, regions, items_to_ignore, depth + 1)


@_find.register
def _(rule: Count, regions: Set[str], items_to_ignore: Set[str], depth: int):
    assert depth < MAX_DEPTH, "Recursion depth exceeded"
    for r in rule.rules:
        _find(r, regions, items_to_ignore, depth + 1)


@_find.register
def _(rule: Has, regions: Set[str], items_to_ignore: Set[str], depth: int):
    assert depth < MAX_DEPTH, f"Recursion depth exceeded on {rule.item}"
    if rule.item in items_to_ignore:
        return
    items_to_ignore.add(rule.item)
    r = rule.other_rules[rule.item]
    _find(r, regions, items_to_ignore, depth + 1)


@_find.register
def _(rule: Reach, regions: Set[str], items_to_ignore: Set[str], depth: int):
    assert depth < MAX_DEPTH, "Recursion depth exceeded"
    if rule.resolution_hint == "Region":
        regions.add(rule.spot)
