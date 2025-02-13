from typing import Dict, List

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

from . import CelesteWorld
from .Names import ItemName, LocationName


def set_rules(world: CelesteWorld):
    # Completion condition.
    world.multiworld.completion_condition[world.player] = lambda state: goal_rule(state, world)


def location_rule(state: CollectionState, world: CelesteWorld, loc: str) -> bool:
    return True


def goal_rule(state: CollectionState, world: CelesteWorld) -> bool:
    if not state.has(ItemName.strawberry, world.player, world.strawberries_required):
        return False

    return True
