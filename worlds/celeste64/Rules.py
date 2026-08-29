from typing import Dict, List, Tuple, Callable

from BaseClasses import CollectionState, Region
from worlds.generic.Rules import set_rule

from . import Celeste64World
from .Names import ItemName, LocationName, RegionName


def set_rules(world: Celeste64World):
    if world.options.logic_difficulty == "standard":
        world.active_logic_mapping = location_standard_moves_logic
        world.active_region_logic_mapping = region_standard_moves_logic
    else:
        world.active_logic_mapping = location_hard_moves_logic
        world.active_region_logic_mapping = region_hard_moves_logic

    for location in world.multiworld.get_locations(world.player):
        set_rule(location, lambda state, location=location: location_rule(state, world, location.name))

    # Completion condition.
    world.multiworld.completion_condition[world.player] = lambda state: goal_rule(state, world)


location_standard_moves_logic: Dict[str, List[List[str]]] = {
    LocationName.strawberry_1:  [[ItemName.ground_dash],
                                 [ItemName.air_dash],
                                 [ItemName.climb]],
    LocationName.strawberry_2:  [[ItemName.air_dash],
                                 [ItemName.skid_jump]],
    LocationName.strawberry_3:  [[ItemName.air_dash],
                                 [ItemName.skid_jump]],
    LocationName.strawberry_4:  [[ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_5:  [[ItemName.air_dash]],
    LocationName.strawberry_9:  [[ItemName.dash_refill, ItemName.air_dash]],
    LocationName.strawberry_10: [[ItemName.climb]],
    LocationName.strawberry_11: [[ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_13: [[ItemName.breakables, ItemName.air_dash],
                                 [ItemName.breakables, ItemName.ground_dash]],
    LocationName.strawberry_14: [[ItemName.feather, ItemName.air_dash]],
    LocationName.strawberry_15: [[ItemName.feather, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_16: [[ItemName.feather]],
    LocationName.strawberry_17: [[ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block]],
    LocationName.strawberry_18: [[ItemName.double_dash_refill, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_19: [[ItemName.double_dash_refill, ItemName.spring, ItemName.air_dash, ItemName.skid_jump]],
    LocationName.strawberry_20: [[ItemName.feather, ItemName.breakables, ItemName.air_dash]],

    LocationName.strawberry_21: [[ItemName.cassette, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_22: [[ItemName.cassette, ItemName.dash_refill, ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_23: [[ItemName.cassette, ItemName.coin, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_24: [[ItemName.cassette, ItemName.dash_refill, ItemName.traffic_block, ItemName.air_dash]],
    LocationName.strawberry_25: [[ItemName.cassette, ItemName.double_dash_refill, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_26: [[ItemName.cassette, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_27: [[ItemName.cassette, ItemName.feather, ItemName.coin, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_28: [[ItemName.cassette, ItemName.feather, ItemName.coin, ItemName.air_dash, ItemName.climb]],
    LocationName.strawberry_29: [[ItemName.cassette, ItemName.dash_refill, ItemName.coin, ItemName.air_dash, ItemName.skid_jump]],
    LocationName.strawberry_30: [[ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.spring, ItemName.breakables, ItemName.air_dash, ItemName.climb]],

    LocationName.theo_1:     [[ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.theo_2:     [[ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],
    LocationName.theo_3:     [[ItemName.traffic_block, ItemName.breakables, ItemName.air_dash]],

    LocationName.sign_2: [[ItemName.breakables, ItemName.ground_dash],
                          [ItemName.breakables, ItemName.air_dash]],

    LocationName.car_2: [[ItemName.breakables, ItemName.ground_dash, ItemName.climb],
                         [ItemName.breakables, ItemName.air_dash, ItemName.climb]],
}

location_hard_moves_logic: Dict[str, List[List[str]]] = {
    LocationName.strawberry_5:  [[ItemName.ground_dash],
                                 [ItemName.air_dash]],
    LocationName.strawberry_10: [[ItemName.air_dash],
                                 [ItemName.climb]],
    LocationName.strawberry_11: [[ItemName.ground_dash],
                                 [ItemName.air_dash],
                                 [ItemName.skid_jump]],
    LocationName.strawberry_13: [[ItemName.breakables, ItemName.ground_dash],
                                 [ItemName.breakables, ItemName.air_dash]],
    LocationName.strawberry_14: [[ItemName.feather, ItemName.air_dash],
                                 [ItemName.air_dash, ItemName.climb],
                                 [ItemName.double_dash_refill, ItemName.air_dash]],
    LocationName.strawberry_15: [[ItemName.feather],
                                 [ItemName.ground_dash, ItemName.air_dash]],
    LocationName.strawberry_17: [[ItemName.double_dash_refill]],
    LocationName.strawberry_18: [[ItemName.air_dash, ItemName.climb],
                                 [ItemName.double_dash_refill, ItemName.air_dash]],
    LocationName.strawberry_19: [[ItemName.air_dash]],
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
    LocationName.strawberry_30: [[ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.traffic_block, ItemName.breakables, ItemName.air_dash, ItemName.climb, ItemName.skid_jump],
                                 [ItemName.cassette, ItemName.dash_refill, ItemName.double_dash_refill, ItemName.traffic_block, ItemName.breakables, ItemName.spring, ItemName.air_dash, ItemName.climb]],

    LocationName.sign_2: [[ItemName.breakables, ItemName.ground_dash],
                          [ItemName.breakables, ItemName.air_dash]],

    LocationName.car_2: [[ItemName.breakables, ItemName.ground_dash],
                         [ItemName.breakables, ItemName.air_dash]],
}


region_standard_moves_logic: Dict[Tuple[str], List[List[str]]] = {
    (RegionName.forsaken_city, RegionName.granny_island):        [[ItemName.checkpoint_2], [ItemName.checkpoint_3], [ItemName.checkpoint_4]],
    (RegionName.forsaken_city, RegionName.highway_island):       [[ItemName.checkpoint_5], [ItemName.checkpoint_6]],
    (RegionName.forsaken_city, RegionName.ne_feathers_island):   [[ItemName.checkpoint_7]],
    (RegionName.forsaken_city, RegionName.se_house_island):      [[ItemName.checkpoint_8]],
    (RegionName.forsaken_city, RegionName.badeline_tower_upper): [[ItemName.checkpoint_9]],
    (RegionName.forsaken_city, RegionName.badeline_island):      [[ItemName.checkpoint_10]],

    (RegionName.intro_islands, RegionName.granny_island): [[ItemName.ground_dash],
                                                           [ItemName.air_dash],
                                                           [ItemName.skid_jump],
                                                           [ItemName.climb]],

    (RegionName.granny_island, RegionName.highway_island): [[ItemName.air_dash, ItemName.dash_refill]],
    (RegionName.granny_island, RegionName.nw_girders_island): [[ItemName.traffic_block]],
    (RegionName.granny_island, RegionName.badeline_tower_lower): [[ItemName.air_dash, ItemName.climb, ItemName.dash_refill]],
    (RegionName.granny_island, RegionName.se_house_island): [[ItemName.air_dash, ItemName.climb, ItemName.double_dash_refill]],
    
    (RegionName.highway_island, RegionName.granny_island): [[ItemName.traffic_block], [ItemName.air_dash, ItemName.dash_refill]],
    (RegionName.highway_island, RegionName.ne_feathers_island): [[ItemName.feather]],
    (RegionName.highway_island, RegionName.nw_girders_island): [[ItemName.cannot_access]],
    
    (RegionName.nw_girders_island, RegionName.highway_island): [[ItemName.traffic_block]],
    
    (RegionName.ne_feathers_island, RegionName.highway_island): [[ItemName.feather]],
    (RegionName.ne_feathers_island, RegionName.badeline_tower_lower): [[ItemName.feather]],
    (RegionName.ne_feathers_island, RegionName.badeline_tower_upper): [[ItemName.climb, ItemName.air_dash, ItemName.feather]],
    
    (RegionName.se_house_island, RegionName.granny_island): [[ItemName.air_dash, ItemName.traffic_block, ItemName.double_dash_refill]],
    (RegionName.se_house_island, RegionName.badeline_tower_lower): [[ItemName.air_dash, ItemName.double_dash_refill]],
    
    (RegionName.badeline_tower_lower, RegionName.se_house_island): [[ItemName.cannot_access]],
    (RegionName.badeline_tower_lower, RegionName.ne_feathers_island): [[ItemName.air_dash, ItemName.breakables, ItemName.feather]],
    (RegionName.badeline_tower_lower, RegionName.granny_island): [[ItemName.cannot_access]],
    (RegionName.badeline_tower_lower, RegionName.badeline_tower_upper): [[ItemName.cannot_access]],
    
    (RegionName.badeline_tower_upper, RegionName.badeline_island): [[ItemName.air_dash, ItemName.climb, ItemName.double_dash_refill, ItemName.feather, ItemName.traffic_block, ItemName.breakables]],
    (RegionName.badeline_tower_upper, RegionName.se_house_island): [[ItemName.air_dash], [ItemName.ground_dash]],
    (RegionName.badeline_tower_upper, RegionName.ne_feathers_island): [[ItemName.air_dash], [ItemName.ground_dash]],
    (RegionName.badeline_tower_upper, RegionName.granny_island): [[ItemName.dash_refill]],
    
    (RegionName.badeline_island, RegionName.badeline_tower_upper): [[ItemName.air_dash], [ItemName.ground_dash]],
}

region_hard_moves_logic: Dict[Tuple[str], List[List[str]]] = {
    (RegionName.forsaken_city, RegionName.granny_island):        [[ItemName.checkpoint_2], [ItemName.checkpoint_3], [ItemName.checkpoint_4]],
    (RegionName.forsaken_city, RegionName.highway_island):       [[ItemName.checkpoint_5], [ItemName.checkpoint_6]],
    (RegionName.forsaken_city, RegionName.ne_feathers_island):   [[ItemName.checkpoint_7]],
    (RegionName.forsaken_city, RegionName.se_house_island):      [[ItemName.checkpoint_8]],
    (RegionName.forsaken_city, RegionName.badeline_tower_upper): [[ItemName.checkpoint_9]],
    (RegionName.forsaken_city, RegionName.badeline_island):      [[ItemName.checkpoint_10]],

    (RegionName.granny_island, RegionName.nw_girders_island): [[ItemName.traffic_block]],
    (RegionName.granny_island, RegionName.badeline_tower_lower): [[ItemName.air_dash], [ItemName.ground_dash]],
    (RegionName.granny_island, RegionName.se_house_island): [[ItemName.air_dash, ItemName.double_dash_refill], [ItemName.ground_dash]],
    
    (RegionName.highway_island, RegionName.nw_girders_island): [[ItemName.air_dash, ItemName.ground_dash]],
    
    (RegionName.nw_girders_island, RegionName.highway_island): [[ItemName.traffic_block], [ItemName.air_dash, ItemName.ground_dash]],
    
    (RegionName.ne_feathers_island, RegionName.highway_island): [[ItemName.feather], [ItemName.air_dash], [ItemName.ground_dash], [ItemName.skid_jump]],
    (RegionName.ne_feathers_island, RegionName.badeline_tower_lower): [[ItemName.feather], [ItemName.air_dash], [ItemName.ground_dash]],
    (RegionName.ne_feathers_island, RegionName.badeline_tower_upper): [[ItemName.feather]],
    
    (RegionName.se_house_island, RegionName.granny_island): [[ItemName.traffic_block]],
    (RegionName.se_house_island, RegionName.badeline_tower_lower): [[ItemName.air_dash], [ItemName.ground_dash]],
    
    (RegionName.badeline_tower_upper, RegionName.badeline_island): [[ItemName.air_dash, ItemName.climb, ItemName.feather, ItemName.traffic_block],
                                                                    [ItemName.air_dash, ItemName.climb, ItemName.feather, ItemName.skid_jump],
                                                                    [ItemName.air_dash, ItemName.climb, ItemName.ground_dash, ItemName.traffic_block],
                                                                    [ItemName.air_dash, ItemName.climb, ItemName.ground_dash, ItemName.skid_jump]],

    (RegionName.badeline_island, RegionName.badeline_tower_upper): [[ItemName.air_dash], [ItemName.ground_dash]],
}


def location_rule(state: CollectionState, world: Celeste64World, loc: str) -> bool:
    if loc not in world.active_logic_mapping:
        return True

    for possible_access in world.active_logic_mapping[loc]:
        if state.has_all(possible_access, world.player):
            return True

    return False

def region_connection_rule(state: CollectionState, world: Celeste64World, region_connection: Tuple[str]) -> bool:
    if region_connection not in world.active_region_logic_mapping:
        return True

    for possible_access in world.active_region_logic_mapping[region_connection]:
        if state.has_all(possible_access, world.player):
            return True

    return False

def goal_rule(state: CollectionState, world: Celeste64World) -> bool:
    if not state.has(ItemName.strawberry, world.player, world.strawberries_required):
        return False

    goal_region: Region = world.multiworld.get_region(RegionName.badeline_island, world.player)
    return state.can_reach(goal_region)

def connect_region(world: Celeste64World, region: Region, dest_regions: List[str]):
    rules: Dict[str, Callable[[CollectionState], bool]] = {}

    for dest_region in dest_regions:
        region_connection: Tuple[str] = (region.name, dest_region)
        rules[dest_region] = lambda state, region_connection=region_connection: region_connection_rule(state, world, region_connection)

    region.add_exits(dest_regions, rules)
