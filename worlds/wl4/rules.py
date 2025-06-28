from __future__ import annotations

import functools
from typing import Callable, Iterable, NamedTuple, TYPE_CHECKING

from BaseClasses import CollectionState

from .items import ItemType, filter_item_names
from .options import Logic

if TYPE_CHECKING:
    from . import WL4World


__all__ = ["Requirement", "has", "has_all", "has_any", "has_treasures", "option", "difficulty", "not_difficulty", "advanced_logic"]


RequiredItem = str | tuple[str, int]


helpers: dict[str, tuple[str, int]] = {
    "Ground Pound":       ("Progressive Ground Pound", 1),
    "Super Ground Pound": ("Progressive Ground Pound", 2),
    "Grab":               ("Progressive Grab", 1),
    "Heavy Grab":         ("Progressive Grab", 2),
}


def resolve_helper(item_name: RequiredItem):
    if isinstance(item_name, str):
        return helpers.get(item_name, (item_name, 1))
    return item_name


class Requirement(NamedTuple):
    inner: Callable[[WL4World, CollectionState], bool]

    def __or__(self, rhs: Requirement):
        return Requirement(lambda w, s: self.inner(w, s) or rhs.inner(w, s))

    def __and__(self, rhs: Requirement):
        return Requirement(lambda w, s: self.inner(w, s) and rhs.inner(w, s))

    def apply_world(self, world: WL4World):
        return functools.partial(self.inner, world)


def has(item_name: RequiredItem) -> Requirement:
    item, count = resolve_helper(item_name)
    return Requirement(lambda w, s: s.has(item, w.player, count))

def _has_all(items: list[tuple[str, int]], state: CollectionState, player: int, ):
    for item, count in items:
        if not state.has(item, player, count):
            return False
    return True

def has_all(items: Iterable[RequiredItem]) -> Requirement:
    resolved_items = [resolve_helper(item) for item in items]
    return Requirement(lambda w, s: _has_all(resolved_items, s, w.player))

def _has_any(items: list[tuple[str, int]], state: CollectionState, player: int):
    for item, count in items:
        if state.has(item, player, count):
            return True
    return False

def has_any(items: Iterable[RequiredItem]) -> Requirement:
    resolved_items = [resolve_helper(item) for item in items]
    return Requirement(lambda w, s: _has_any(resolved_items, s, w.player))

treasures = list(filter_item_names(type=ItemType.TREASURE))

def treasure_count(state: CollectionState, player: int):
    count = 0
    for treasure in treasures:
        if state.has(treasure, player):
            count += 1
    return count

def has_treasures() -> Requirement:
    return Requirement(lambda w, s: treasure_count(s, w.player) >= w.options.golden_treasure_count.value)


def option(option_name: str, choice: int):
    return Requirement(lambda w, _: getattr(w.options, option_name).value == choice)

def difficulty(difficulty: int):
    return option("difficulty", difficulty)

def not_difficulty(_difficulty: int):
    return Requirement(lambda w, s: not difficulty(_difficulty).inner(w, s))

def advanced_logic():
    return option("logic", Logic.option_advanced)
