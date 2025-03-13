from __future__ import annotations

import functools
from typing import Callable, Mapping, NamedTuple, Sequence, Tuple, Union, TYPE_CHECKING

from BaseClasses import CollectionState

from .items import ItemType, filter_item_names
from .options import Logic

if TYPE_CHECKING:
    from . import WL4World


__all__ = ['Requirement', 'has', 'has_all', 'has_any', 'has_treasures', 'option', 'difficulty', 'not_difficulty', 'advanced_logic']


RequiredItem = Union[str, Tuple[str, int]]


helpers: Mapping[str, Tuple[str, int]] = {
    'Ground Pound':       ('Progressive Ground Pound', 1),
    'Super Ground Pound': ('Progressive Ground Pound', 2),
    'Grab':               ('Progressive Grab', 1),
    'Heavy Grab':         ('Progressive Grab', 2),
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

def has_all(items: Sequence[RequiredItem]) -> Requirement:
    return Requirement(lambda w, s: all(has(item).inner(w, s) for item in items))

def has_any(items: Sequence[RequiredItem]) -> Requirement:
    return Requirement(lambda w, s: any(has(item).inner(w, s) for item in items))

def has_treasures() -> Requirement:
    return Requirement(lambda w, s: sum(has(item).inner(w, s)
                                        for item in filter_item_names(type=ItemType.TREASURE))
                                    >= w.options.golden_treasure_count)


def option(option_name: str, choice: int):
    return Requirement(lambda w, _: getattr(w.options, option_name) == choice)

def difficulty(difficulty: int):
    return option('difficulty', difficulty)

def not_difficulty(_difficulty: int):
    return Requirement(lambda w, s: not difficulty(_difficulty).inner(w, s))

def advanced_logic():
    return option('logic', Logic.option_advanced)
