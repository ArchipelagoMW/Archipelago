import collections
import typing
from .Locations import DLCquestLocation
from ..generic.Rules import add_rule, set_rule
from .Regions import create_regions
from .Items import DLCquestItem
from BaseClasses import ItemClassification


def create_event(player, event: str):
    return DLCquestItem(event, ItemClassification.progression, None, player)

def set_rules(world, player, option):
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
    

    loc_win = DLCquestLocation(player,"Winning", None, world.get_region("The Final Boss Room", player))
    world.get_region("The Final Boss Room", player).locations.append(loc_win)
    loc_win.place_locked_item(create_event(player, "Victory"))
    set_rule(world.get_location("Winning", player), lambda state: state.can_reach("The Final Boss Room", 'Region', player) and
                                                            state.has("Horse Armor Pack", player)) and state.has("Finish The Fight Pack")
    world.completion_condition[player] = lambda state: state.has("Victory", player)



