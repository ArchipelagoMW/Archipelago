from typing import Dict, List

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

from . import Celeste64World
from .Names import ItemName, LocationName


def set_rules(world: Celeste64World):
    if world.options.logic_difficulty == "standard":
        if world.options.move_shuffle:
            world.active_logic_mapping = location_standard_moves_logic
        else:
            world.active_logic_mapping = location_standard_logic
    else:
        if world.options.move_shuffle:
            world.active_logic_mapping = location_hard_moves_logic
        else:
            world.active_logic_mapping = location_hard_logic

    for location in world.multiworld.get_locations(world.player):
        set_rule(location, lambda state, location=location: location_rule(state, world, location.name))

    if world.options.logic_difficulty == "standard":
        if world.options.move_shuffle:
            world.goal_logic_mapping = goal_standard_moves_logic
        else:
            world.goal_logic_mapping = goal_standard_logic
    else:
        if world.options.move_shuffle:
            world.goal_logic_mapping = goal_hard_moves_logic
        else:
            world.goal_logic_mapping = goal_hard_logic

    # Completion condition.
    world.multiworld.completion_condition[world.player] = lambda state: goal_rule(state, world)


goal_standard_logic: List[List[str]] = [[ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.double_dash_refill]]
goal_hard_logic: List[List[str]] = [[]]
goal_standard_moves_logic: List[List[str]] = [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb]]
goal_hard_moves_logic: List[List[str]] = [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb],
                                          [ItemName.traffic_block, ItemName.air_dash, ItemName.skid_jump],
                                          [ItemName.ground_dash, ItemName.air_dash, ItemName.skid_jump],
                                          [ItemName.feather, ItemName.traffic_block, ItemName.air_dash],
                                          [ItemName.traffic_block, ItemName.ground_dash, ItemName.air_dash]]


location_standard_logic: Dict[str, List[List[str]]] = {
    LocationName.strawberry_4:  [[ItemName.traffic_block, ItemName.breakables]],
    LocationName.strawberry_6:  [[ItemName.dash_refill],
                                 [ItemName.traffic_block]],
    LocationName.strawberry_7:  [[ItemName.dash_refill],
                                 [ItemName.traffic_block]],
    LocationName.strawberry_8:  [[ItemName.traffic_block]],
    LocationName.strawberry_9:  [[ItemName.dash_refill]],
    LocationName.strawberry_11: [[ItemName.dash_refill],
                                 [ItemName.traffic_block]],
    LocationName.strawberry_12: [[ItemName.dash_refill, ItemName.double_dash_refill],
                                 [ItemName.traffic_block, ItemName.double_dash_refill]],
    LocationName.strawberry_13: [[ItemName.dash_refill, ItemName.breakables],
                                 [ItemName.traffic_block, ItemName.breakables]],
    LocationName.strawberry_14: [[ItemName.dash_refill, ItemName.feather],
                                 [ItemName.traffic_block, ItemName.feather]],
    LocationName.strawberry_15: [[ItemName.dash_refill, ItemName.feather],
                                 [ItemName.traffic_block, ItemName.feather]],
    LocationName.strawberry_16: [[ItemName.dash_refill, ItemName.feather],
                                 [ItemName.traffic_block, ItemName.feather]],
    LocationName.strawberry_17: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block]],
    LocationName.strawberry_18: [[ItemName.dash_refill, ItemName.double_dash_refill],
                                 [ItemName.traffic_block, ItemName.feather, ItemName.double_dash_refill]],
    LocationName.strawberry_19: [[ItemName.dash_refill, ItemName.double_dash_refill, ItemName.spring],
                                 [ItemName.traffic_block, ItemName.double_dash_refill, ItemName.feather, ItemName.spring]],
    LocationName.strawberry_20: [[ItemName.dash_refill, ItemName.feather, ItemName.breakables],
                                 [ItemName.traffic_block, ItemName.feather, ItemName.breakables]],

    LocationName.strawberry_21: [[ItemName.cassette, ItemName.traffic_block, ItemName.breakables]],
    LocationName.strawberry_22: [[ItemName.cassette, ItemName.dash_refill, ItemName.breakables]],
    LocationName.strawberry_23: [[ItemName.cassette, ItemName.dash_refill, ItemName.coin],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.coin]],
    LocationName.strawberry_24: [[ItemName.cassette, ItemName.dash_refill, ItemName.traffic_block]],
    LocationName.strawberry_25: [[ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.feather, ItemName.double_dash_refill]],
    LocationName.strawberry_26: [[ItemName.cassette, ItemName.dash_refill],
                                 [ItemName.cassette, ItemName.traffic_block]],
    LocationName.strawberry_27: [[ItemName.cassette, ItemName.dash_refill, ItemName.feather, ItemName.coin],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.feather, ItemName.coin]],
    LocationName.strawberry_28: [[ItemName.cassette, ItemName.dash_refill, ItemName.feather, ItemName.coin],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.feather, ItemName.coin]],
    LocationName.strawberry_29: [[ItemName.cassette, ItemName.dash_refill, ItemName.feather, ItemName.coin]],
    LocationName.strawberry_30: [[ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.spring, ItemName.breakables]],

    LocationName.theo_1:     [[ItemName.traffic_block, ItemName.breakables]],
    LocationName.theo_2:     [[ItemName.traffic_block, ItemName.breakables]],
    LocationName.theo_3:     [[ItemName.traffic_block, ItemName.breakables]],
    LocationName.badeline_1: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables]],
    LocationName.badeline_2: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables]],
    LocationName.badeline_3: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables]],

    LocationName.sign_2: [[ItemName.breakables]],
    LocationName.sign_3: [[ItemName.dash_refill],
                          [ItemName.traffic_block]],
    LocationName.sign_4: [[ItemName.dash_refill, ItemName.double_dash_refill],
                          [ItemName.dash_refill, ItemName.feather],
                          [ItemName.traffic_block, ItemName.feather]],
    LocationName.sign_5: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables]],

    LocationName.car_2: [[ItemName.breakables]],
}

location_hard_logic: Dict[str, List[List[str]]] = {
    LocationName.strawberry_13: [[ItemName.breakables]],
    LocationName.strawberry_17: [[ItemName.double_dash_refill, ItemName.traffic_block]],
    LocationName.strawberry_20: [[ItemName.breakables]],

    LocationName.strawberry_21: [[ItemName.cassette, ItemName.traffic_block, ItemName.breakables]],
    LocationName.strawberry_22: [[ItemName.cassette]],
    LocationName.strawberry_23: [[ItemName.cassette, ItemName.coin]],
    LocationName.strawberry_24: [[ItemName.cassette]],
    LocationName.strawberry_25: [[ItemName.cassette, ItemName.double_dash_refill]],
    LocationName.strawberry_26: [[ItemName.cassette]],
    LocationName.strawberry_27: [[ItemName.cassette]],
    LocationName.strawberry_28: [[ItemName.cassette, ItemName.feather]],
    LocationName.strawberry_29: [[ItemName.cassette]],
    LocationName.strawberry_30: [[ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.traffic_block, ItemName.breakables]],

    LocationName.sign_2: [[ItemName.breakables]],

    LocationName.car_2: [[ItemName.breakables]],
}

location_standard_moves_logic: Dict[str, List[List[str]]] = {
    LocationName.strawberry_1:  [[ItemName.ground_dash],
                                 [ItemName.air_dash],
                                 [ItemName.skid_jump],
                                 [ItemName.climb]],
    LocationName.strawberry_2:  [[ItemName.ground_dash],
                                 [ItemName.air_dash],
                                 [ItemName.skid_jump],
                                 [ItemName.climb]],
    LocationName.strawberry_3:  [[ItemName.air_dash],
                                 [ItemName.skid_jump]],
    LocationName.strawberry_4:  [[ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_5:  [[ItemName.air_dash]],
    LocationName.strawberry_6:  [[ItemName.dash_refill, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.ground_dash],
                                 [ItemName.traffic_block, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.skid_jump],
                                 [ItemName.traffic_block, ItemName.climb]],
    LocationName.strawberry_7:  [[ItemName.dash_refill, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.ground_dash],
                                 [ItemName.traffic_block, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.skid_jump],
                                 [ItemName.traffic_block, ItemName.climb]],
    LocationName.strawberry_8:  [[ItemName.traffic_block, ItemName.ground_dash],
                                 [ItemName.traffic_block, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.skid_jump],
                                 [ItemName.traffic_block, ItemName.climb]],
    LocationName.strawberry_9:  [[ItemName.dash_refill, ItemName.air_dash]],
    LocationName.strawberry_10: [[ItemName.climb]],
    LocationName.strawberry_11: [[ItemName.dash_refill, ItemName.air_dash, ItemName.climb],
                                 [ItemName.traffic_block, ItemName.climb]],
    LocationName.strawberry_12: [[ItemName.dash_refill, ItemName.double_dash_refill, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.double_dash_refill, ItemName.air_dash]],
    LocationName.strawberry_13: [[ItemName.dash_refill, ItemName.breakables, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.breakables, ItemName.ground_dash],
                                 [ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_14: [[ItemName.dash_refill, ItemName.feather, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.feather, ItemName.air_dash]],
    LocationName.strawberry_15: [[ItemName.dash_refill, ItemName.feather, ItemName.air_dash, ItemName.climb],
                                 [ItemName.traffic_block, ItemName.feather, ItemName.climb]],
    LocationName.strawberry_16: [[ItemName.dash_refill, ItemName.feather, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.feather]],
    LocationName.strawberry_17: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.ground_dash],
                                 [ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.air_dash],
                                 [ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.skid_jump],
                                 [ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.climb]],
    LocationName.strawberry_18: [[ItemName.dash_refill, ItemName.double_dash_refill, ItemName.air_dash, ItemName.climb],
                                 [ItemName.traffic_block, ItemName.feather, ItemName.double_dash_refill, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_19: [[ItemName.dash_refill, ItemName.double_dash_refill, ItemName.spring, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.double_dash_refill, ItemName.feather, ItemName.spring, ItemName.air_dash]],
    LocationName.strawberry_20: [[ItemName.dash_refill, ItemName.feather, ItemName.breakables, ItemName.air_dash],
                                 [ItemName.traffic_block, ItemName.feather, ItemName.breakables, ItemName.air_dash]],

    LocationName.strawberry_21: [[ItemName.cassette, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_22: [[ItemName.cassette, ItemName.dash_refill, ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_23: [[ItemName.cassette, ItemName.dash_refill, ItemName.coin, ItemName.air_dash, ItemName.climb],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.coin, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_24: [[ItemName.cassette, ItemName.dash_refill, ItemName.traffic_block, ItemName.air_dash]],
    LocationName.strawberry_25: [[ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.air_dash, ItemName.climb],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.feather, ItemName.double_dash_refill, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_26: [[ItemName.cassette, ItemName.dash_refill, ItemName.air_dash, ItemName.climb],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_27: [[ItemName.cassette, ItemName.dash_refill, ItemName.feather, ItemName.coin, ItemName.air_dash],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.feather, ItemName.coin, ItemName.air_dash]],
    LocationName.strawberry_28: [[ItemName.cassette, ItemName.dash_refill, ItemName.feather, ItemName.coin, ItemName.air_dash, ItemName.climb],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.feather, ItemName.coin, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_29: [[ItemName.cassette, ItemName.dash_refill, ItemName.feather, ItemName.coin, ItemName.air_dash, ItemName.skid_jump]],
    LocationName.strawberry_30: [[ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.spring, ItemName.breakables, ItemName.air_dash, ItemName.climb]],

    LocationName.granny_1:   [[ItemName.ground_dash],
                              [ItemName.air_dash],
                              [ItemName.skid_jump],
                              [ItemName.climb]],
    LocationName.granny_2:   [[ItemName.ground_dash],
                              [ItemName.air_dash],
                              [ItemName.skid_jump],
                              [ItemName.climb]],
    LocationName.granny_3:   [[ItemName.ground_dash],
                              [ItemName.air_dash],
                              [ItemName.skid_jump],
                              [ItemName.climb]],
    LocationName.theo_1:     [[ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.theo_2:     [[ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.theo_3:     [[ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.badeline_1: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb]],
    LocationName.badeline_2: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb]],
    LocationName.badeline_3: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb]],

    LocationName.sign_1: [[ItemName.ground_dash],
                          [ItemName.air_dash],
                          [ItemName.skid_jump],
                          [ItemName.climb]],
    LocationName.sign_2: [[ItemName.breakables, ItemName.ground_dash],
                          [ItemName.breakables, ItemName.air_dash]],
    LocationName.sign_3:  [[ItemName.dash_refill, ItemName.air_dash],
                           [ItemName.traffic_block, ItemName.ground_dash],
                           [ItemName.traffic_block, ItemName.air_dash],
                           [ItemName.traffic_block, ItemName.skid_jump],
                           [ItemName.traffic_block, ItemName.climb]],
    LocationName.sign_4: [[ItemName.dash_refill, ItemName.double_dash_refill, ItemName.air_dash],
                          [ItemName.dash_refill, ItemName.feather, ItemName.air_dash],
                          [ItemName.traffic_block, ItemName.feather, ItemName.ground_dash],
                          [ItemName.traffic_block, ItemName.feather, ItemName.air_dash],
                          [ItemName.traffic_block, ItemName.feather, ItemName.skid_jump],
                          [ItemName.traffic_block, ItemName.feather, ItemName.climb]],
    LocationName.sign_5: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb]],

    LocationName.car_2: [[ItemName.breakables, ItemName.ground_dash],
                         [ItemName.breakables, ItemName.air_dash]],
}

location_hard_moves_logic: Dict[str, List[List[str]]] = {
    LocationName.strawberry_3:  [[ItemName.air_dash],
                                 [ItemName.skid_jump]],
    LocationName.strawberry_5:  [[ItemName.ground_dash],
                                 [ItemName.air_dash]],
    LocationName.strawberry_8:  [[ItemName.traffic_block],
                                 [ItemName.ground_dash, ItemName.air_dash]],
    LocationName.strawberry_10: [[ItemName.air_dash],
                                 [ItemName.climb]],
    LocationName.strawberry_11: [[ItemName.ground_dash],
                                 [ItemName.air_dash],
                                 [ItemName.skid_jump]],
    LocationName.strawberry_12: [[ItemName.feather],
                                 [ItemName.ground_dash],
                                 [ItemName.air_dash]],
    LocationName.strawberry_13: [[ItemName.breakables, ItemName.ground_dash],
                                 [ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_14: [[ItemName.feather, ItemName.air_dash],
                                 [ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_15: [[ItemName.feather],
                                 [ItemName.ground_dash, ItemName.air_dash]],
    LocationName.strawberry_17: [[ItemName.double_dash_refill, ItemName.traffic_block]],
    LocationName.strawberry_18: [[ItemName.air_dash, ItemName.climb],
                                 [ItemName.double_dash_refill, ItemName.air_dash]],
    LocationName.strawberry_19: [[ItemName.air_dash, ItemName.skid_jump],
                                 [ItemName.double_dash_refill, ItemName.spring, ItemName.air_dash],
                                 [ItemName.spring, ItemName.ground_dash, ItemName.air_dash]],
    LocationName.strawberry_20: [[ItemName.breakables, ItemName.air_dash]],

    LocationName.strawberry_21: [[ItemName.cassette, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_22: [[ItemName.cassette, ItemName.ground_dash, ItemName.air_dash],
                                 [ItemName.cassette, ItemName.dash_refill, ItemName.air_dash]],
    LocationName.strawberry_23: [[ItemName.cassette, ItemName.coin, ItemName.air_dash]],
    LocationName.strawberry_24: [[ItemName.cassette, ItemName.ground_dash, ItemName.air_dash],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.air_dash]],
    LocationName.strawberry_25: [[ItemName.cassette, ItemName.double_dash_refill, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_26: [[ItemName.cassette, ItemName.ground_dash],
                                 [ItemName.cassette, ItemName.air_dash]],
    LocationName.strawberry_27: [[ItemName.cassette, ItemName.air_dash, ItemName.skid_jump],
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.coin, ItemName.air_dash],
                                 [ItemName.cassette, ItemName.coin, ItemName.ground_dash],
                                 [ItemName.cassette, ItemName.feather, ItemName.coin, ItemName.air_dash]],
    LocationName.strawberry_28: [[ItemName.cassette, ItemName.feather, ItemName.air_dash],
                                 [ItemName.cassette, ItemName.feather, ItemName.climb]],
    LocationName.strawberry_29: [[ItemName.cassette, ItemName.dash_refill, ItemName.air_dash, ItemName.skid_jump],
                                 [ItemName.cassette, ItemName.ground_dash, ItemName.air_dash]],
    LocationName.strawberry_30: [[ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.traffic_block, ItemName.breakables, ItemName.ground_dash, ItemName.air_dash, ItemName.climb, ItemName.skid_jump],
                                 [ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.traffic_block, ItemName.breakables, ItemName.feather, ItemName.air_dash, ItemName.climb, ItemName.skid_jump],
                                 [ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.traffic_block, ItemName.breakables, ItemName.spring, ItemName.ground_dash, ItemName.air_dash, ItemName.climb],
                                 [ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.traffic_block, ItemName.breakables, ItemName.spring, ItemName.feather, ItemName.air_dash, ItemName.climb]],

    LocationName.badeline_1: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb],
                              [ItemName.traffic_block, ItemName.air_dash, ItemName.skid_jump],
                              [ItemName.ground_dash, ItemName.air_dash, ItemName.skid_jump],
                              [ItemName.feather, ItemName.traffic_block, ItemName.air_dash],
                              [ItemName.traffic_block, ItemName.ground_dash, ItemName.air_dash]],
    LocationName.badeline_2: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb],
                              [ItemName.traffic_block, ItemName.air_dash, ItemName.skid_jump],
                              [ItemName.ground_dash, ItemName.air_dash, ItemName.skid_jump],
                              [ItemName.feather, ItemName.traffic_block, ItemName.air_dash],
                              [ItemName.traffic_block, ItemName.ground_dash, ItemName.air_dash]],
    LocationName.badeline_3: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb],
                              [ItemName.traffic_block, ItemName.air_dash, ItemName.skid_jump],
                              [ItemName.ground_dash, ItemName.air_dash, ItemName.skid_jump],
                              [ItemName.feather, ItemName.traffic_block, ItemName.air_dash],
                              [ItemName.traffic_block, ItemName.ground_dash, ItemName.air_dash]],

    LocationName.sign_2: [[ItemName.breakables, ItemName.ground_dash],
                          [ItemName.breakables, ItemName.air_dash]],
    LocationName.sign_5: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb],
                          [ItemName.traffic_block, ItemName.air_dash, ItemName.skid_jump],
                          [ItemName.ground_dash, ItemName.air_dash, ItemName.skid_jump],
                          [ItemName.feather, ItemName.traffic_block, ItemName.air_dash],
                          [ItemName.traffic_block, ItemName.ground_dash, ItemName.air_dash]],

    LocationName.car_2: [[ItemName.breakables, ItemName.ground_dash],
                         [ItemName.breakables, ItemName.air_dash]],
}


def location_rule(state: CollectionState, world: Celeste64World, loc: str) -> bool:

    if loc not in world.active_logic_mapping:
        return True

    for possible_access in world.active_logic_mapping[loc]:
        if state.has_all(possible_access, world.player):
            return True

    return False

def goal_rule(state: CollectionState, world: Celeste64World) -> bool:
    if not state.has(ItemName.strawberry, world.player, world.strawberries_required):
        return False

    for possible_access in world.goal_logic_mapping:
        if state.has_all(possible_access, world.player):
            return True

    return False
