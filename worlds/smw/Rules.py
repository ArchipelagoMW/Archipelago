import math

from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule


def set_rules(world: World):

    if world.options.goal == "yoshi_egg_hunt":
        required_yoshi_eggs = world.required_egg_count

        add_rule(world.multiworld.get_location(LocationName.yoshis_house, world.player),
                 lambda state: state.has(ItemName.yoshi_egg, world.player, required_yoshi_eggs))
    else:
        add_rule(world.multiworld.get_location(LocationName.bowser, world.player), lambda state: state.has(ItemName.mario_carry, world.player))

    world.multiworld.completion_condition[world.player] = lambda state: state.has(ItemName.victory, world.player)
