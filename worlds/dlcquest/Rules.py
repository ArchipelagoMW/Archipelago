import collections
import typing
from __init__ import create_event
from BaseClasses import LocationProgressType, MultiWorld
from ..generic.Rules import add_rule, set_rule
from .Regions import DLCquestRegion
from .Locations import Victory

def set_rules(world, player, option)
    set_rule(world.get_entrance("Moving", player),
             lambda state: state.has("Movement Pack", player))
    set_rule(world.get_entrance("Tree", player),
             lambda state: state.has("Time is Money Pack", player))
    set_rule(world.get_entrance("Cloud", player),
             lambda state: state.has("Psychological Warfare Pack", player))
    set_rule(world.get_entrance("Behind Tree Double Jump", player),
             lambda state: state.has("Double jump Pack", player))
    set_rule(world.get_entrance("Forest Entrance", player),
             lambda state: state.has("Map Pack", player))
    set_rule(world.get_entrance("Cloud Double Jump", player),
             lambda state: state.has("Double jump Pack", player))
    set_rule(world.get_entrance("Behind Ogre", player),
             lambda state: state.has("Gun Pack", player))


    world.get_region("The Final Boss Room", player).place_locked_item(create_event("Victory"))
    add_rule(world.get_location("Victory", player), lambda state: state.can_reach("The Final Boss Room", 'Region', player) and
                                                            state.has("Horse Armor Pack", player))
    world.completion_condition[player] = lambda state: state.has("Victory", player)



