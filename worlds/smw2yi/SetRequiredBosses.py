from typing import Tuple
from ..generic.Rules import add_rule
from .Locations import get_locations
from BaseClasses import MultiWorld

import random

def load_req_bosses(world: MultiWorld, player: int) -> str:
    bosses_required = lambda state: True
    list_of_bosses = world.random.sample(range(1, 12), world.bosses_for_unlock[player].value)


    if 1 in list_of_bosses:
        add_rule(world.get_location("King Bowser's Castle: Stars", player), lambda state: state.has("Key", player))
    if 2 in list_of_bosses:
        add_rule(world.get_location("King Bowser's Castle: Stars", player), lambda state: state.has("Key", player))
    if 3 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
    if 4 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
    if 5 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
    if 6 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
    if 7 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
    if 8 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
    if 9 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
    if 10 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
    if 11 in list_of_bosses:
        add_rule(world.get_location("Required Bosses", player), lambda state: state.has("Cannon Unlock BoB", player))
        
    return bosses_required