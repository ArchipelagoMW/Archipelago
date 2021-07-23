from ..generic.Rules import set_rule, add_rule

from graph.vanilla.graph_locations import locationsDict
from logic.logic import Logic
import logging

def set_accessFrom_rule(location, player, accessFrom):
    add_rule(location, lambda state: any((state.can_reach(accessName, player=player) and rule(state)) for accessName, rule in accessFrom.items()))

def set_rules(world, player):
    world.completion_condition[player] = lambda state: state.has('Mother Brain', player)

    for key, value in locationsDict.items():
        location = world.get_location(key, player)
        set_rule(location, value.Available)
        if value.AccessFrom is not None:
            set_accessFrom_rule(location, player, value.AccessFrom)
        if value.PostAvailable is not None:
            add_rule(location, value.PostAvailable)
            
    for accessPoint in Logic.accessPoints:
        for key, value1 in accessPoint.intraTransitions.items():
            set_rule(world.get_entrance(accessPoint.Name + "|" + key, player), value1)
