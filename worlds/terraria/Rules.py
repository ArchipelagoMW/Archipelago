from ..generic.Rules import set_rule
from .Locations import exclusion_table, events_table
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class TerrariaLogic(LogicMixin):
    # Defs here
    
    def temp(self, player: int):
        pass

def set_rules(world: MultiWorld, player: int):
    def reachable_locations(state):
        postgame_advancements = exclusion_table['postgame'].copy()
        for event in events_table.keys():
            postgame_advancements.add(event)
        return [location for location in world.get_locations() if
                location.player == player and
                location.name not in postgame_advancements and
                location.can_reach(state)]

    # 88 total achievements. Goal is to defeat Wall of Flesh. 
    goal = 20#int(world.achievement_goal[player].value)
    can_complete = lambda state: len(reachable_locations(state)) >= goal and state.can_reach('Hardmode', 'Region', player)

    if world.logic[player] != 'nologic':
        world.completion_condition[player] = lambda state: state.has('Victory', player)

    set_rule(world.get_entrance("Kill WoF", player), lambda state: True)
    set_rule(world.get_entrance("Kill Plantera", player), lambda state: True)
    set_rule(world.get_entrance("Kill Golem", player), lambda state: True)
    set_rule(world.get_entrance("Kill Moon Lord", player), lambda state: True)
    set_rule(world.get_entrance("Descend to Underworld", player), lambda state: True)
    set_rule(world.get_entrance("Go to Corruption", player), lambda state: True)
    set_rule(world.get_entrance("Go to Crimson", player), lambda state: True)
    set_rule(world.get_entrance("Go to Dungeon", player), lambda state: True)
    set_rule(world.get_entrance("Go to Jungle", player), lambda state: True)
    set_rule(world.get_entrance("Go to Hardmode Jungle", player), lambda state: True)

    set_rule(world.get_location("Still Hungry", player), lambda state: can_complete(state))

    