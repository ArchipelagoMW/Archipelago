import math

from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
# from ..AutoWorld import LogicMixin
from ..generic.Rules import add_rule, set_rule


def set_rules(world: MultiWorld, player: int):

    #if world.goal[player] != "knautilus":
    #    required_banana_birds = math.floor(
    #            world.number_of_banana_birds[player].value * (world.percentage_of_banana_birds[player].value / 100.0))

#        add_rule(world.get_location(LocationName.banana_bird_mother, player),
#                 lambda state: state.has(ItemName.banana_bird, player, required_banana_birds))

    world.completion_condition[player] = lambda state: state.has(ItemName.victory, player)
