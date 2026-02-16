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

    set_rule(world.get_entrance("Start to Quickplay"),lambda state: state.has("Quickplay",world.player))
    set_rule(world.get_entrance("Start to Alt Story"),lambda state: state.has("Alt. Story",world.player))

    for x in world.get_entrances():
        if str(x).__contains__("(QP) Monster Unlocked"):
            pass


def set_all_location_rules(world: TVRUHHWorld) -> None:
    pass



def set_completion_condition(world: TVRUHHWorld):
    pass