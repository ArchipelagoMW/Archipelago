import math

from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from .Names import LocationName, ItemName


def set_rules(world: World):

    if False:#world.options.include_trade_sequence:
        add_rule(world.multiworld.get_location(LocationName.barnacles_island, world.player),
                    lambda state: state.has(ItemName.shell, world.player))

        add_rule(world.multiworld.get_location(LocationName.blues_beach_hut, world.player),
                    lambda state: state.has(ItemName.present, world.player))

        add_rule(world.multiworld.get_location(LocationName.brambles_bungalow, world.player),
                    lambda state: state.has(ItemName.flower, world.player))

        add_rule(world.multiworld.get_location(LocationName.barters_swap_shop, world.player),
                    lambda state: state.has(ItemName.mirror, world.player))


    if world.options.goal != "knautilus":
        required_banana_birds = math.floor(
                world.options.number_of_banana_birds.value * (world.options.percentage_of_banana_birds.value / 100.0))

        add_rule(world.multiworld.get_location(LocationName.banana_bird_mother, world.player),
                 lambda state: state.has(ItemName.banana_bird, world.player, required_banana_birds))

    world.multiworld.completion_condition[world.player] = lambda state: state.has(ItemName.victory, world.player)
