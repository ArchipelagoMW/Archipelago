import collections
import typing

from BaseClasses import LocationProgressType, MultiWorld
from ..generic.Rules import add_rule, set_rule
from .Regions import DLCquestRegion

def set_rules(world, player, option)
    set_rule(world.get_entrance("mouving", player),
             lambda state: state.has("Movement Pack", player))
    set_rule(world.get_entrance("tree", player),
             lambda state: state.has("Time is Money Pack", player))
    set_rule(world.get_entrance("Cloud", player),
             lambda state: state.has("Psychological Warfare Pack", player))
    set_rule(world.get_entrance("behind tree double jump", player),
             lambda state: state.has("Double jump Pack", player))
    set_rule(world.get_entrance("Forest Entrance", player),
             lambda state: state.has("Map Pack", player))
    set_rule(world.get_entrance("Psychological warfare double jump", player),
             lambda state: state.has("Double jump Pack", player))

