from BaseClasses import CollectionState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import Shapez2World


def extended_has(world: "Shapez2World", state: CollectionState, item: str) -> bool:
    return state.has(item, world.player) or item in world.starting_items


def extended_has_all(world: "Shapez2World", state: CollectionState, *items: str) -> bool:
    return all(
        state.has(item, world.player) or item in world.starting_items
        for item in items
    )


def extended_has_any(world: "Shapez2World", state: CollectionState, *items: str) -> bool:
    return state.has_any(items, world.player) or any(item in world.starting_items for item in items)


def extended_has_from_list_unique(world: "Shapez2World", state: CollectionState, count: int, *items: str) -> bool:
    found = 0
    for item in items:
        if state.has(item, world.player) or item in world.starting_items:
            found += 1
        if found >= count:
            return True
    return False
