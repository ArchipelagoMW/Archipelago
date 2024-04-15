from typing import Dict, List

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

from . import Celeste64World
from .Names import ItemName, LocationName


def set_rules(world: Celeste64World):
    for location in world.multiworld.get_locations(world.player):
        set_rule(location, lambda state, location=location: location_rule(state, world, location.name))

    # Completion condition.
    world.multiworld.completion_condition[world.player] = lambda state: (state.has(ItemName.strawberry, world.player, world.strawberries_required) and
                                                                         state.has_all({ItemName.feather,
                                                                                        ItemName.traffic_block,
                                                                                        ItemName.breakables,
                                                                                        ItemName.double_dash_refill}, world.player))


location_standard_logic: Dict[str, List[List[str]]] = {
    LocationName.strawberry_4:  [[ItemName.traffic_block, ItemName.breakables]],
    LocationName.strawberry_6:  [[ItemName.dash_refill],
                                 [ItemName.traffic_block]],
    LocationName.strawberry_7:  [[ItemName.dash_refill],
                                 [ItemName.traffic_block]],
    LocationName.strawberry_8:  [[ItemName.traffic_block]],
    LocationName.strawberry_9:  [[ItemName.dash_refill],
                                 [ItemName.traffic_block]],
    LocationName.strawberry_11: [[ItemName.dash_refill],
                                 [ItemName.traffic_block]],
    LocationName.strawberry_12: [[ItemName.dash_refill, ItemName.double_dash_refill],
                                 [ItemName.traffic_block], ItemName.double_dash_refill],
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
                                 [ItemName.cassette, ItemName.traffic_block, ItemName.feather, ItemName.coin]],
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
    LocationName.sign_3: [[ItemName.dash_refill]],
    LocationName.sign_4: [[ItemName.dash_refill, ItemName.double_dash_refill],
                          [ItemName.dash_refill, ItemName.feather],
                          [ItemName.traffic_block, ItemName.feather]],
    LocationName.sign_5: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables]],

    LocationName.car_2: [[ItemName.breakables]],
}


def location_rule(state: CollectionState, world: Celeste64World, loc: str) -> bool:
    if loc not in location_standard_logic:
        return True

    for possible_access in location_standard_logic[loc]:
        if state.has_all(possible_access, world.player):
            return True

    return False
