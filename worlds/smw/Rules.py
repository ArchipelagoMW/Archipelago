import math

from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule, set_rule


def set_rules(world: MultiWorld, player: int):

    if world.goal[player] == "yoshi_egg_hunt":
        required_yoshi_eggs = max(math.floor(
                world.number_of_yoshi_eggs[player].value * (world.percentage_of_yoshi_eggs[player].value / 100.0)), 1)

        add_rule(world.get_location(LocationName.yoshis_house, player),
                 lambda state: state.has(ItemName.yoshi_egg, player, required_yoshi_eggs))
    else:
        add_rule(world.get_location(LocationName.bowser, player), lambda state: state.has(ItemName.mario_carry, player))

    world.completion_condition[player] = lambda state: state.has(ItemName.victory, player)
