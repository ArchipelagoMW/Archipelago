from typing import Callable

from BaseClasses import CollectionState, MultiWorld
from .Names import ItemName, LocationName
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule, CollectionRule


def set_rules(world: World):
    add_rule(world.multiworld.get_location(LocationName.strawberry_1, world.player),
                lambda state: state.has(ItemName.strawberry, world.player))
    pass
