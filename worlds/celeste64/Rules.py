from worlds.generic.Rules import set_rule

from . import Celeste64World
from .Names import ItemName, LocationName


def set_rules(world: Celeste64World):
    set_rule(world.multiworld.get_location(LocationName.strawberry_4, world.player),
             lambda state: state.has_all({ItemName.traffic_block,
                                          ItemName.breakables}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_5, world.player),
             lambda state: state.has(ItemName.breakables, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_6, world.player),
             lambda state: state.has(ItemName.dash_refill, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_8, world.player),
             lambda state: state.has(ItemName.traffic_block, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_9, world.player),
             lambda state: state.has(ItemName.dash_refill, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_11, world.player),
             lambda state: state.has(ItemName.dash_refill, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_12, world.player),
             lambda state: state.has_all({ItemName.dash_refill,
                                          ItemName.double_dash_refill}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_13, world.player),
             lambda state: state.has_all({ItemName.dash_refill,
                                          ItemName.breakables}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_14, world.player),
             lambda state: state.has_all({ItemName.dash_refill,
                                          ItemName.feather}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_15, world.player),
             lambda state: state.has_all({ItemName.dash_refill,
                                          ItemName.feather}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_16, world.player),
             lambda state: state.has_all({ItemName.dash_refill,
                                          ItemName.feather}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_17, world.player),
             lambda state: state.has_all({ItemName.dash_refill,
                                          ItemName.double_dash_refill,
                                          ItemName.feather,
                                          ItemName.traffic_block}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_18, world.player),
             lambda state: state.has(ItemName.double_dash_refill, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_19, world.player),
             lambda state: state.has_all({ItemName.double_dash_refill,
                                          ItemName.spring}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_20, world.player),
             lambda state: state.has_all({ItemName.dash_refill,
                                          ItemName.feather,
                                          ItemName.breakables}, world.player))

    set_rule(world.multiworld.get_location(LocationName.strawberry_21, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.traffic_block,
                                          ItemName.breakables}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_22, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.dash_refill,
                                          ItemName.breakables}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_23, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.dash_refill,
                                          ItemName.coin}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_24, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.traffic_block,
                                          ItemName.dash_refill}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_25, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.dash_refill,
                                          ItemName.double_dash_refill}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_26, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.dash_refill}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_27, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.feather,
                                          ItemName.coin,
                                          ItemName.dash_refill}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_28, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.feather,
                                          ItemName.coin,
                                          ItemName.dash_refill}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_29, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.feather,
                                          ItemName.coin,
                                          ItemName.dash_refill}, world.player))
    set_rule(world.multiworld.get_location(LocationName.strawberry_30, world.player),
             lambda state: state.has_all({ItemName.cassette,
                                          ItemName.feather,
                                          ItemName.traffic_block,
                                          ItemName.spring,
                                          ItemName.breakables,
                                          ItemName.dash_refill,
                                          ItemName.double_dash_refill}, world.player))

    # Completion condition.
    world.multiworld.completion_condition[world.player] = lambda state: (state.has(ItemName.strawberry,world.player,world.options.strawberries_required.value) and
                                                                         state.has_all({ItemName.feather,
                                                                                        ItemName.traffic_block,
                                                                                        ItemName.breakables,
                                                                                        ItemName.dash_refill,
                                                                                        ItemName.double_dash_refill}, world.player))
