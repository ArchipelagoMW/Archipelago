from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    return True


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):

    width_req = world.max_width[player]
    height_req = world.max_height[player]
    bomb_req = world.max_bombs[player]
    completion_requirements = lambda state: \
        state.has("Map Width", player, width_req) and \
        state.has("Map Height", player, height_req) and \
        state.has("Map Bomb", player, bomb_req)
    world.completion_condition[player] = lambda state: completion_requirements(state)
