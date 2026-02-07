from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, LocationProgressType
from worlds.generic.Rules import add_rule, set_rule

from . import items

if TYPE_CHECKING:
    from .world import TVRUHHWorld

def set_all_rules(world: TVRUHHWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)





def set_all_entrance_rules(world: TVRUHHWorld) -> None:
    start_to_50monsters = world.get_entrance("Start to having 50 Monsters unlocked")
    start_to_quickplay = world.get_entrance("Start to Quickplay")

    set_rule(start_to_50monsters,lambda state: state.has_from_list(items.monster_list, world.player, 50))
    set_rule(start_to_quickplay,lambda state: state.has("Quickplay Unlock",world.player))


def set_all_location_rules(world: TVRUHHWorld) -> None:
    pass



def set_completion_condition(world: TVRUHHWorld):
    pass