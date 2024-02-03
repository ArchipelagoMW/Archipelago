from typing import Callable

from BaseClasses import CollectionState, MultiWorld
from .Names import ItemName, LocationName
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, set_rule, CollectionRule



def set_rules(world: World):

    add_rule(world.multiworld.get_location(LocationName.strawberry_4,world.player),
             lambda state: state.has(ItemName.traffic_block, world.player) and
                           state.has(ItemName.breakables, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_5,world.player),
             lambda state: state.has(ItemName.breakables, world.player)) # Questionable
    add_rule(world.multiworld.get_location(LocationName.strawberry_6,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_8,world.player),
             lambda state: state.has(ItemName.traffic_block, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_9,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_11,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_12,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player) or
                           state.has(ItemName.double_dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_13,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.breakables, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_14,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.feather, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_15,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.feather, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_16,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.feather, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_17,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.double_dash_refill, world.player) and
                           state.has(ItemName.feather, world.player) and
                           state.has(ItemName.traffic_block, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_18,world.player),
             lambda state: state.has(ItemName.double_dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_19,world.player),
             lambda state: state.has(ItemName.double_dash_refill, world.player) and
                           state.has(ItemName.spring, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_20,world.player),
             lambda state: state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.feather, world.player) and
                           state.has(ItemName.breakables, world.player))

    add_rule(world.multiworld.get_location(LocationName.strawberry_21,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.traffic_block, world.player) and
                           state.has(ItemName.breakables, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_22,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.breakables, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_23,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.coin, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_24,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.traffic_block, world.player) and
                           state.has(ItemName.dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_25,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.double_dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_26,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_27,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.feather, world.player) and
                           state.has(ItemName.coin, world.player) and
                           state.has(ItemName.dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_28,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.feather, world.player) and
                           state.has(ItemName.coin, world.player) and
                           state.has(ItemName.dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_29,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.feather, world.player) and
                           state.has(ItemName.coin, world.player) and
                           state.has(ItemName.dash_refill, world.player))
    add_rule(world.multiworld.get_location(LocationName.strawberry_30,world.player),
             lambda state: state.has(ItemName.cassette, world.player) and
                           state.has(ItemName.feather, world.player) and
                           state.has(ItemName.traffic_block, world.player) and
                           state.has(ItemName.spring, world.player) and
                           state.has(ItemName.breakables, world.player) and
                           state.has(ItemName.dash_refill, world.player) and
                           state.has(ItemName.double_dash_refill, world.player))

    # Completion condition.
    world.multiworld.completion_condition[world.player] = lambda state: (state.has(ItemName.strawberry,world.player,world.options.strawberries_required.value) and
                                                                state.has(ItemName.feather, world.player) and
                                                                state.has(ItemName.traffic_block, world.player) and
                                                                state.has(ItemName.breakables, world.player) and
                                                                state.has(ItemName.dash_refill, world.player) and
                                                                state.has(ItemName.double_dash_refill, world.player))
