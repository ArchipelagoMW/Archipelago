from ..generic.Rules import set_rule
from BaseClasses import Region, Entrance, Location, MultiWorld, Item

def set_rules(world: MultiWorld, player: int):
    if world.logic[player] != 'nologic': 
        world.completion_condition[player] = lambda state: len(world.get_reachable_locations(state, player)) >= 40

