import typing
import math

from BaseClasses import MultiWorld, Region, Entrance, ItemClassification
from worlds.AutoWorld import World
from .Items import SA2BItem
from .Locations import SA2BLocation, boss_gate_location_table, boss_gate_set,\
                                     chao_stat_swim_table, chao_stat_fly_table, chao_stat_run_table,\
                                     chao_stat_power_table, chao_stat_stamina_table,\
                                     chao_stat_luck_table, chao_stat_intelligence_table, chao_animal_event_location_table,\
                                     chao_kindergarten_location_table, chao_kindergarten_basics_location_table, black_market_location_table
from .Names import LocationName, ItemName
from .GateBosses import get_boss_name, all_gate_bosses_table, king_boom_boo


class LevelGate:
    gate_levels: typing.List[int]
    gate_emblem_count: int

    def __init__(self, emblems):
        self.gate_emblem_count = emblems
        self.gate_levels = list()


shuffleable_regions = [
    LocationName.city_escape_region,
    LocationName.wild_canyon_region,
    LocationName.prison_lane_region,
    LocationName.metal_harbor_region,
    LocationName.green_forest_region,
    LocationName.pumpkin_hill_region,
    LocationName.mission_street_region,
    LocationName.aquatic_mine_region,
    LocationName.route_101_region,
    LocationName.hidden_base_region,
    LocationName.pyramid_cave_region,
    LocationName.death_chamber_region,
    LocationName.eternal_engine_region,
    LocationName.meteor_herd_region,
    LocationName.crazy_gadget_region,
    LocationName.final_rush_region,
    LocationName.iron_gate_region,
    LocationName.dry_lagoon_region,
    LocationName.sand_ocean_region,
    LocationName.radical_highway_region,
    LocationName.egg_quarters_region,
    LocationName.lost_colony_region,
    LocationName.weapons_bed_region,
    LocationName.security_hall_region,
    LocationName.white_jungle_region,
    LocationName.route_280_region,
    LocationName.sky_rail_region,
    LocationName.mad_space_region,
    LocationName.cosmic_wall_region,
    LocationName.final_chase_region,
]

gate_0_blacklist_regions = [
    LocationName.hidden_base_region,
    LocationName.eternal_engine_region,
    LocationName.crazy_gadget_region,
    LocationName.security_hall_region,
    LocationName.cosmic_wall_region,
]

gate_0_whitelist_regions = [
    LocationName.city_escape_region,
    LocationName.wild_canyon_region,
    LocationName.prison_lane_region,
    LocationName.metal_harbor_region,
    LocationName.green_forest_region,
    LocationName.pumpkin_hill_region,
    LocationName.mission_street_region,
    LocationName.aquatic_mine_region,
    LocationName.route_101_region,
    LocationName.pyramid_cave_region,
    LocationName.death_chamber_region,
    LocationName.meteor_herd_region,
    LocationName.final_rush_region,
    LocationName.iron_gate_region,
    LocationName.dry_lagoon_region,
    LocationName.sand_ocean_region,
    LocationName.radical_highway_region,
    LocationName.egg_quarters_region,
    LocationName.lost_colony_region,
    LocationName.weapons_bed_region,
    LocationName.white_jungle_region,
    LocationName.route_280_region,
    LocationName.sky_rail_region,
    LocationName.mad_space_region,
    LocationName.final_chase_region,
]


def create_regions(multiworld: MultiWorld, world: World, player: int, active_locations):
    menu_region = create_region(multiworld, player, active_locations, 'Menu', None)

    conditional_regions = []
    gate_0_region = create_region(multiworld, player, active_locations, 'Gate 0', None)
    conditional_regions += [gate_0_region]

    if world.options.number_of_level_gates.value >= 1:
        gate_1_boss_region = create_region(multiworld, player, active_locations, 'Gate 1 Boss', [LocationName.gate_1_boss])
        gate_1_region = create_region(multiworld, player, active_locations, 'Gate 1', None)
        conditional_regions += [gate_1_region, gate_1_boss_region]

    if world.options.number_of_level_gates.value >= 2:
        gate_2_boss_region = create_region(multiworld, player, active_locations, 'Gate 2 Boss', [LocationName.gate_2_boss])
        gate_2_region = create_region(multiworld, player, active_locations, 'Gate 2', None)
        conditional_regions += [gate_2_region, gate_2_boss_region]

    if world.options.number_of_level_gates.value >= 3:
        gate_3_boss_region = create_region(multiworld, player, active_locations, 'Gate 3 Boss', [LocationName.gate_3_boss])
        gate_3_region = create_region(multiworld, player, active_locations, 'Gate 3', None)
        conditional_regions += [gate_3_region, gate_3_boss_region]

    if world.options.number_of_level_gates.value >= 4:
        gate_4_boss_region = create_region(multiworld, player, active_locations, 'Gate 4 Boss', [LocationName.gate_4_boss])
        gate_4_region = create_region(multiworld, player, active_locations, 'Gate 4', None)
        conditional_regions += [gate_4_region, gate_4_boss_region]

    if world.options.number_of_level_gates.value >= 5:
        gate_5_boss_region = create_region(multiworld, player, active_locations, 'Gate 5 Boss', [LocationName.gate_5_boss])
        gate_5_region = create_region(multiworld, player, active_locations, 'Gate 5', None)
        conditional_regions += [gate_5_region, gate_5_boss_region]

    city_escape_region_locations = [
        LocationName.city_escape_1,
        LocationName.city_escape_2,
        LocationName.city_escape_3,
        LocationName.city_escape_4,
        LocationName.city_escape_5,
        LocationName.city_escape_chao_1,
        LocationName.city_escape_chao_2,
        LocationName.city_escape_chao_3,
        LocationName.city_escape_pipe_1,
        LocationName.city_escape_pipe_2,
        LocationName.city_escape_pipe_3,
        LocationName.city_escape_pipe_4,
        LocationName.city_escape_hidden_1,
        LocationName.city_escape_hidden_2,
        LocationName.city_escape_hidden_3,
        LocationName.city_escape_hidden_4,
        LocationName.city_escape_hidden_5,
        LocationName.city_escape_omo_1,
        LocationName.city_escape_omo_2,
        LocationName.city_escape_omo_3,
        LocationName.city_escape_omo_4,
        LocationName.city_escape_omo_5,
        LocationName.city_escape_omo_6,
        LocationName.city_escape_omo_7,
        LocationName.city_escape_omo_8,
        LocationName.city_escape_omo_9,
        LocationName.city_escape_omo_10,
        LocationName.city_escape_omo_11,
        LocationName.city_escape_omo_12,
        LocationName.city_escape_omo_13,
        LocationName.city_escape_omo_14,
        LocationName.city_escape_beetle,
        LocationName.city_escape_animal_1,
        LocationName.city_escape_animal_2,
        LocationName.city_escape_animal_3,
        LocationName.city_escape_animal_4,
        LocationName.city_escape_animal_5,
        LocationName.city_escape_animal_6,
        LocationName.city_escape_animal_7,
        LocationName.city_escape_animal_8,
        LocationName.city_escape_animal_9,
        LocationName.city_escape_animal_10,
        LocationName.city_escape_animal_11,
        LocationName.city_escape_animal_12,
        LocationName.city_escape_animal_13,
        LocationName.city_escape_animal_14,
        LocationName.city_escape_animal_15,
        LocationName.city_escape_animal_16,
        LocationName.city_escape_animal_17,
        LocationName.city_escape_animal_18,
        LocationName.city_escape_animal_19,
        LocationName.city_escape_animal_20,
        LocationName.city_escape_upgrade,
    ]
    city_escape_region = create_region(multiworld, player, active_locations, LocationName.city_escape_region,
                                       city_escape_region_locations)

    metal_harbor_region_locations = [
        LocationName.metal_harbor_1,
        LocationName.metal_harbor_2,
        LocationName.metal_harbor_3,
        LocationName.metal_harbor_4,
        LocationName.metal_harbor_5,
        LocationName.metal_harbor_chao_1,
        LocationName.metal_harbor_chao_2,
        LocationName.metal_harbor_chao_3,
        LocationName.metal_harbor_pipe_1,
        LocationName.metal_harbor_omo_1,
        LocationName.metal_harbor_omo_2,
        LocationName.metal_harbor_omo_3,
        LocationName.metal_harbor_omo_4,
        LocationName.metal_harbor_omo_5,
        LocationName.metal_harbor_beetle,
        LocationName.metal_harbor_animal_1,
        LocationName.metal_harbor_animal_2,
        LocationName.metal_harbor_animal_3,
        LocationName.metal_harbor_animal_4,
        LocationName.metal_harbor_animal_5,
        LocationName.metal_harbor_animal_6,
        LocationName.metal_harbor_animal_7,
        LocationName.metal_harbor_animal_8,
        LocationName.metal_harbor_animal_9,
        LocationName.metal_harbor_animal_10,
        LocationName.metal_harbor_animal_11,
        LocationName.metal_harbor_animal_12,
        LocationName.metal_harbor_animal_13,
        LocationName.metal_harbor_animal_14,
        LocationName.metal_harbor_upgrade,
    ]
    metal_harbor_region = create_region(multiworld, player, active_locations, LocationName.metal_harbor_region,
                                        metal_harbor_region_locations)

    green_forest_region_locations = [
        LocationName.green_forest_1,
        LocationName.green_forest_2,
        LocationName.green_forest_3,
        LocationName.green_forest_4,
        LocationName.green_forest_5,
        LocationName.green_forest_chao_1,
        LocationName.green_forest_chao_2,
        LocationName.green_forest_chao_3,
        LocationName.green_forest_pipe_1,
        LocationName.green_forest_pipe_2,
        LocationName.green_forest_hidden_1,
        LocationName.green_forest_hidden_2,
        LocationName.green_forest_hidden_3,
        LocationName.green_forest_hidden_4,
        LocationName.green_forest_beetle,
        LocationName.green_forest_animal_1,
        LocationName.green_forest_animal_2,
        LocationName.green_forest_animal_3,
        LocationName.green_forest_animal_4,
        LocationName.green_forest_animal_5,
        LocationName.green_forest_animal_6,
        LocationName.green_forest_animal_7,
        LocationName.green_forest_animal_8,
        LocationName.green_forest_animal_9,
        LocationName.green_forest_animal_10,
        LocationName.green_forest_animal_11,
        LocationName.green_forest_animal_12,
        LocationName.green_forest_animal_13,
        LocationName.green_forest_animal_14,
        LocationName.green_forest_animal_15,
        LocationName.green_forest_animal_16,
        LocationName.green_forest_animal_17,
        LocationName.green_forest_animal_18,
        LocationName.green_forest_upgrade,
    ]
    green_forest_region = create_region(multiworld, player, active_locations, LocationName.green_forest_region,
                                        green_forest_region_locations)

    pyramid_cave_region_locations = [
        LocationName.pyramid_cave_1,
        LocationName.pyramid_cave_2,
        LocationName.pyramid_cave_3,
        LocationName.pyramid_cave_4,
        LocationName.pyramid_cave_5,
        LocationName.pyramid_cave_chao_1,
        LocationName.pyramid_cave_chao_2,
        LocationName.pyramid_cave_chao_3,
        LocationName.pyramid_cave_pipe_1,
        LocationName.pyramid_cave_pipe_2,
        LocationName.pyramid_cave_pipe_3,
        LocationName.pyramid_cave_pipe_4,
        LocationName.pyramid_cave_omo_1,
        LocationName.pyramid_cave_omo_2,
        LocationName.pyramid_cave_omo_3,
        LocationName.pyramid_cave_omo_4,
        LocationName.pyramid_cave_beetle,
        LocationName.pyramid_cave_animal_1,
        LocationName.pyramid_cave_animal_2,
        LocationName.pyramid_cave_animal_3,
        LocationName.pyramid_cave_animal_4,
        LocationName.pyramid_cave_animal_5,
        LocationName.pyramid_cave_animal_6,
        LocationName.pyramid_cave_animal_7,
        LocationName.pyramid_cave_animal_8,
        LocationName.pyramid_cave_animal_9,
        LocationName.pyramid_cave_animal_10,
        LocationName.pyramid_cave_animal_11,
        LocationName.pyramid_cave_animal_12,
        LocationName.pyramid_cave_animal_13,
        LocationName.pyramid_cave_animal_14,
        LocationName.pyramid_cave_animal_15,
        LocationName.pyramid_cave_animal_16,
        LocationName.pyramid_cave_animal_17,
        LocationName.pyramid_cave_animal_18,
        LocationName.pyramid_cave_animal_19,
        LocationName.pyramid_cave_upgrade,
    ]
    pyramid_cave_region = create_region(multiworld, player, active_locations, LocationName.pyramid_cave_region,
                                        pyramid_cave_region_locations)

    crazy_gadget_region_locations = [
        LocationName.crazy_gadget_1,
        LocationName.crazy_gadget_2,
        LocationName.crazy_gadget_3,
        LocationName.crazy_gadget_4,
        LocationName.crazy_gadget_5,
        LocationName.crazy_gadget_chao_1,
        LocationName.crazy_gadget_chao_2,
        LocationName.crazy_gadget_chao_3,
        LocationName.crazy_gadget_pipe_1,
        LocationName.crazy_gadget_pipe_2,
        LocationName.crazy_gadget_pipe_3,
        LocationName.crazy_gadget_pipe_4,
        LocationName.crazy_gadget_hidden_1,
        LocationName.crazy_gadget_omo_1,
        LocationName.crazy_gadget_omo_2,
        LocationName.crazy_gadget_omo_3,
        LocationName.crazy_gadget_omo_4,
        LocationName.crazy_gadget_omo_5,
        LocationName.crazy_gadget_omo_6,
        LocationName.crazy_gadget_omo_7,
        LocationName.crazy_gadget_omo_8,
        LocationName.crazy_gadget_omo_9,
        LocationName.crazy_gadget_omo_10,
        LocationName.crazy_gadget_omo_11,
        LocationName.crazy_gadget_omo_12,
        LocationName.crazy_gadget_omo_13,
        LocationName.crazy_gadget_beetle,
        LocationName.crazy_gadget_animal_1,
        LocationName.crazy_gadget_animal_2,
        LocationName.crazy_gadget_animal_3,
        LocationName.crazy_gadget_animal_4,
        LocationName.crazy_gadget_animal_5,
        LocationName.crazy_gadget_animal_6,
        LocationName.crazy_gadget_animal_7,
        LocationName.crazy_gadget_animal_8,
        LocationName.crazy_gadget_animal_9,
        LocationName.crazy_gadget_animal_10,
        LocationName.crazy_gadget_animal_11,
        LocationName.crazy_gadget_animal_12,
        LocationName.crazy_gadget_animal_13,
        LocationName.crazy_gadget_animal_14,
        LocationName.crazy_gadget_animal_15,
        LocationName.crazy_gadget_animal_16,
        LocationName.crazy_gadget_upgrade,
    ]
    crazy_gadget_region = create_region(multiworld, player, active_locations, LocationName.crazy_gadget_region,
                                        crazy_gadget_region_locations)

    final_rush_region_locations = [
        LocationName.final_rush_1,
        LocationName.final_rush_2,
        LocationName.final_rush_3,
        LocationName.final_rush_4,
        LocationName.final_rush_5,
        LocationName.final_rush_chao_1,
        LocationName.final_rush_chao_2,
        LocationName.final_rush_chao_3,
        LocationName.final_rush_pipe_1,
        LocationName.final_rush_pipe_2,
        LocationName.final_rush_omo_1,
        LocationName.final_rush_omo_2,
        LocationName.final_rush_omo_3,
        LocationName.final_rush_beetle,
        LocationName.final_rush_animal_1,
        LocationName.final_rush_animal_2,
        LocationName.final_rush_animal_3,
        LocationName.final_rush_animal_4,
        LocationName.final_rush_animal_5,
        LocationName.final_rush_animal_6,
        LocationName.final_rush_animal_7,
        LocationName.final_rush_animal_8,
        LocationName.final_rush_animal_9,
        LocationName.final_rush_animal_10,
        LocationName.final_rush_animal_11,
        LocationName.final_rush_animal_12,
        LocationName.final_rush_animal_13,
        LocationName.final_rush_animal_14,
        LocationName.final_rush_animal_15,
        LocationName.final_rush_animal_16,
        LocationName.final_rush_upgrade,
    ]
    final_rush_region = create_region(multiworld, player, active_locations, LocationName.final_rush_region,
                                      final_rush_region_locations)

    prison_lane_region_locations = [
        LocationName.prison_lane_1,
        LocationName.prison_lane_2,
        LocationName.prison_lane_3,
        LocationName.prison_lane_4,
        LocationName.prison_lane_5,
        LocationName.prison_lane_chao_1,
        LocationName.prison_lane_chao_2,
        LocationName.prison_lane_chao_3,
        LocationName.prison_lane_pipe_1,
        LocationName.prison_lane_pipe_2,
        LocationName.prison_lane_pipe_3,
        LocationName.prison_lane_hidden_1,
        LocationName.prison_lane_hidden_2,
        LocationName.prison_lane_hidden_3,
        LocationName.prison_lane_omo_1,
        LocationName.prison_lane_omo_2,
        LocationName.prison_lane_omo_3,
        LocationName.prison_lane_omo_4,
        LocationName.prison_lane_omo_5,
        LocationName.prison_lane_omo_6,
        LocationName.prison_lane_omo_7,
        LocationName.prison_lane_omo_8,
        LocationName.prison_lane_omo_9,
        LocationName.prison_lane_omo_10,
        LocationName.prison_lane_beetle,
        LocationName.prison_lane_animal_1,
        LocationName.prison_lane_animal_2,
        LocationName.prison_lane_animal_3,
        LocationName.prison_lane_animal_4,
        LocationName.prison_lane_animal_5,
        LocationName.prison_lane_animal_6,
        LocationName.prison_lane_animal_7,
        LocationName.prison_lane_animal_8,
        LocationName.prison_lane_animal_9,
        LocationName.prison_lane_animal_10,
        LocationName.prison_lane_animal_11,
        LocationName.prison_lane_animal_12,
        LocationName.prison_lane_animal_13,
        LocationName.prison_lane_animal_14,
        LocationName.prison_lane_animal_15,
        LocationName.prison_lane_upgrade,
    ]
    prison_lane_region = create_region(multiworld, player, active_locations, LocationName.prison_lane_region,
                                       prison_lane_region_locations)

    mission_street_region_locations = [
        LocationName.mission_street_1,
        LocationName.mission_street_2,
        LocationName.mission_street_3,
        LocationName.mission_street_4,
        LocationName.mission_street_5,
        LocationName.mission_street_chao_1,
        LocationName.mission_street_chao_2,
        LocationName.mission_street_chao_3,
        LocationName.mission_street_pipe_1,
        LocationName.mission_street_pipe_2,
        LocationName.mission_street_pipe_3,
        LocationName.mission_street_hidden_1,
        LocationName.mission_street_hidden_2,
        LocationName.mission_street_hidden_3,
        LocationName.mission_street_hidden_4,
        LocationName.mission_street_omo_1,
        LocationName.mission_street_omo_2,
        LocationName.mission_street_omo_3,
        LocationName.mission_street_omo_4,
        LocationName.mission_street_omo_5,
        LocationName.mission_street_omo_6,
        LocationName.mission_street_omo_7,
        LocationName.mission_street_omo_8,
        LocationName.mission_street_beetle,
        LocationName.mission_street_animal_1,
        LocationName.mission_street_animal_2,
        LocationName.mission_street_animal_3,
        LocationName.mission_street_animal_4,
        LocationName.mission_street_animal_5,
        LocationName.mission_street_animal_6,
        LocationName.mission_street_animal_7,
        LocationName.mission_street_animal_8,
        LocationName.mission_street_animal_9,
        LocationName.mission_street_animal_10,
        LocationName.mission_street_animal_11,
        LocationName.mission_street_animal_12,
        LocationName.mission_street_animal_13,
        LocationName.mission_street_animal_14,
        LocationName.mission_street_animal_15,
        LocationName.mission_street_animal_16,
        LocationName.mission_street_upgrade,
    ]
    mission_street_region = create_region(multiworld, player, active_locations, LocationName.mission_street_region,
                                          mission_street_region_locations)

    route_101_region_locations = [
        LocationName.route_101_1,
        LocationName.route_101_2,
        LocationName.route_101_3,
        LocationName.route_101_4,
        LocationName.route_101_5,
    ]
    route_101_region = create_region(multiworld, player, active_locations, LocationName.route_101_region,
                                     route_101_region_locations)

    hidden_base_region_locations = [
        LocationName.hidden_base_1,
        LocationName.hidden_base_2,
        LocationName.hidden_base_3,
        LocationName.hidden_base_4,
        LocationName.hidden_base_5,
        LocationName.hidden_base_chao_1,
        LocationName.hidden_base_chao_2,
        LocationName.hidden_base_pipe_1,
        LocationName.hidden_base_pipe_2,
        LocationName.hidden_base_pipe_3,
        LocationName.hidden_base_pipe_4,
        LocationName.hidden_base_pipe_5,
        LocationName.hidden_base_omo_1,
        LocationName.hidden_base_omo_2,
        LocationName.hidden_base_omo_3,
        LocationName.hidden_base_omo_4,
        LocationName.hidden_base_beetle,
        LocationName.hidden_base_animal_1,
        LocationName.hidden_base_animal_2,
        LocationName.hidden_base_animal_3,
        LocationName.hidden_base_animal_4,
        LocationName.hidden_base_animal_5,
        LocationName.hidden_base_animal_6,
        LocationName.hidden_base_animal_7,
        LocationName.hidden_base_animal_8,
        LocationName.hidden_base_animal_9,
        LocationName.hidden_base_animal_10,
        LocationName.hidden_base_animal_11,
        LocationName.hidden_base_animal_12,
        LocationName.hidden_base_animal_13,
        LocationName.hidden_base_animal_14,
        LocationName.hidden_base_animal_15,
        LocationName.hidden_base_upgrade,
    ]
    hidden_base_region = create_region(multiworld, player, active_locations, LocationName.hidden_base_region,
                                       hidden_base_region_locations)

    eternal_engine_region_locations = [
        LocationName.eternal_engine_1,
        LocationName.eternal_engine_2,
        LocationName.eternal_engine_3,
        LocationName.eternal_engine_4,
        LocationName.eternal_engine_5,
        LocationName.eternal_engine_chao_1,
        LocationName.eternal_engine_chao_2,
        LocationName.eternal_engine_chao_3,
        LocationName.eternal_engine_pipe_1,
        LocationName.eternal_engine_pipe_2,
        LocationName.eternal_engine_pipe_3,
        LocationName.eternal_engine_pipe_4,
        LocationName.eternal_engine_pipe_5,
        LocationName.eternal_engine_omo_1,
        LocationName.eternal_engine_omo_2,
        LocationName.eternal_engine_omo_3,
        LocationName.eternal_engine_omo_4,
        LocationName.eternal_engine_omo_5,
        LocationName.eternal_engine_omo_6,
        LocationName.eternal_engine_omo_7,
        LocationName.eternal_engine_omo_8,
        LocationName.eternal_engine_omo_9,
        LocationName.eternal_engine_omo_10,
        LocationName.eternal_engine_omo_11,
        LocationName.eternal_engine_omo_12,
        LocationName.eternal_engine_beetle,
        LocationName.eternal_engine_animal_1,
        LocationName.eternal_engine_animal_2,
        LocationName.eternal_engine_animal_3,
        LocationName.eternal_engine_animal_4,
        LocationName.eternal_engine_animal_5,
        LocationName.eternal_engine_animal_6,
        LocationName.eternal_engine_animal_7,
        LocationName.eternal_engine_animal_8,
        LocationName.eternal_engine_animal_9,
        LocationName.eternal_engine_animal_10,
        LocationName.eternal_engine_animal_11,
        LocationName.eternal_engine_animal_12,
        LocationName.eternal_engine_animal_13,
        LocationName.eternal_engine_animal_14,
        LocationName.eternal_engine_animal_15,
        LocationName.eternal_engine_upgrade,
    ]
    eternal_engine_region = create_region(multiworld, player, active_locations, LocationName.eternal_engine_region,
                                          eternal_engine_region_locations)

    wild_canyon_region_locations = [
        LocationName.wild_canyon_1,
        LocationName.wild_canyon_2,
        LocationName.wild_canyon_3,
        LocationName.wild_canyon_4,
        LocationName.wild_canyon_5,
        LocationName.wild_canyon_chao_1,
        LocationName.wild_canyon_chao_2,
        LocationName.wild_canyon_chao_3,
        LocationName.wild_canyon_pipe_1,
        LocationName.wild_canyon_pipe_2,
        LocationName.wild_canyon_pipe_3,
        LocationName.wild_canyon_omo_1,
        LocationName.wild_canyon_omo_2,
        LocationName.wild_canyon_omo_3,
        LocationName.wild_canyon_omo_4,
        LocationName.wild_canyon_omo_5,
        LocationName.wild_canyon_omo_6,
        LocationName.wild_canyon_omo_7,
        LocationName.wild_canyon_omo_8,
        LocationName.wild_canyon_omo_9,
        LocationName.wild_canyon_omo_10,
        LocationName.wild_canyon_beetle,
        LocationName.wild_canyon_animal_1,
        LocationName.wild_canyon_animal_2,
        LocationName.wild_canyon_animal_3,
        LocationName.wild_canyon_animal_4,
        LocationName.wild_canyon_animal_5,
        LocationName.wild_canyon_animal_6,
        LocationName.wild_canyon_animal_7,
        LocationName.wild_canyon_animal_8,
        LocationName.wild_canyon_animal_9,
        LocationName.wild_canyon_animal_10,
        LocationName.wild_canyon_upgrade,
    ]
    wild_canyon_region = create_region(multiworld, player, active_locations, LocationName.wild_canyon_region,
                                       wild_canyon_region_locations)

    pumpkin_hill_region_locations = [
        LocationName.pumpkin_hill_1,
        LocationName.pumpkin_hill_2,
        LocationName.pumpkin_hill_3,
        LocationName.pumpkin_hill_4,
        LocationName.pumpkin_hill_5,
        LocationName.pumpkin_hill_chao_1,
        LocationName.pumpkin_hill_chao_2,
        LocationName.pumpkin_hill_chao_3,
        LocationName.pumpkin_hill_pipe_1,
        LocationName.pumpkin_hill_hidden_1,
        LocationName.pumpkin_hill_omo_1,
        LocationName.pumpkin_hill_omo_2,
        LocationName.pumpkin_hill_omo_3,
        LocationName.pumpkin_hill_omo_4,
        LocationName.pumpkin_hill_omo_5,
        LocationName.pumpkin_hill_omo_6,
        LocationName.pumpkin_hill_omo_7,
        LocationName.pumpkin_hill_omo_8,
        LocationName.pumpkin_hill_omo_9,
        LocationName.pumpkin_hill_omo_10,
        LocationName.pumpkin_hill_omo_11,
        LocationName.pumpkin_hill_animal_1,
        LocationName.pumpkin_hill_animal_2,
        LocationName.pumpkin_hill_animal_3,
        LocationName.pumpkin_hill_animal_4,
        LocationName.pumpkin_hill_animal_5,
        LocationName.pumpkin_hill_animal_6,
        LocationName.pumpkin_hill_animal_7,
        LocationName.pumpkin_hill_animal_8,
        LocationName.pumpkin_hill_animal_9,
        LocationName.pumpkin_hill_animal_10,
        LocationName.pumpkin_hill_animal_11,
        LocationName.pumpkin_hill_upgrade,
    ]
    pumpkin_hill_region = create_region(multiworld, player, active_locations, LocationName.pumpkin_hill_region,
                                        pumpkin_hill_region_locations)

    aquatic_mine_region_locations = [
        LocationName.aquatic_mine_1,
        LocationName.aquatic_mine_2,
        LocationName.aquatic_mine_3,
        LocationName.aquatic_mine_4,
        LocationName.aquatic_mine_5,
        LocationName.aquatic_mine_chao_1,
        LocationName.aquatic_mine_chao_2,
        LocationName.aquatic_mine_chao_3,
        LocationName.aquatic_mine_pipe_1,
        LocationName.aquatic_mine_pipe_2,
        LocationName.aquatic_mine_pipe_3,
        LocationName.aquatic_mine_omo_1,
        LocationName.aquatic_mine_omo_2,
        LocationName.aquatic_mine_omo_3,
        LocationName.aquatic_mine_omo_4,
        LocationName.aquatic_mine_omo_5,
        LocationName.aquatic_mine_omo_6,
        LocationName.aquatic_mine_omo_7,
        LocationName.aquatic_mine_beetle,
        LocationName.aquatic_mine_animal_1,
        LocationName.aquatic_mine_animal_2,
        LocationName.aquatic_mine_animal_3,
        LocationName.aquatic_mine_animal_4,
        LocationName.aquatic_mine_animal_5,
        LocationName.aquatic_mine_animal_6,
        LocationName.aquatic_mine_animal_7,
        LocationName.aquatic_mine_animal_8,
        LocationName.aquatic_mine_animal_9,
        LocationName.aquatic_mine_animal_10,
        LocationName.aquatic_mine_upgrade,
    ]
    aquatic_mine_region = create_region(multiworld, player, active_locations, LocationName.aquatic_mine_region,
                                        aquatic_mine_region_locations)

    death_chamber_region_locations = [
        LocationName.death_chamber_1,
        LocationName.death_chamber_2,
        LocationName.death_chamber_3,
        LocationName.death_chamber_4,
        LocationName.death_chamber_5,
        LocationName.death_chamber_chao_1,
        LocationName.death_chamber_chao_2,
        LocationName.death_chamber_chao_3,
        LocationName.death_chamber_pipe_1,
        LocationName.death_chamber_pipe_2,
        LocationName.death_chamber_pipe_3,
        LocationName.death_chamber_hidden_1,
        LocationName.death_chamber_hidden_2,
        LocationName.death_chamber_omo_1,
        LocationName.death_chamber_omo_2,
        LocationName.death_chamber_omo_3,
        LocationName.death_chamber_omo_4,
        LocationName.death_chamber_omo_5,
        LocationName.death_chamber_omo_6,
        LocationName.death_chamber_omo_7,
        LocationName.death_chamber_omo_8,
        LocationName.death_chamber_omo_9,
        LocationName.death_chamber_beetle,
        LocationName.death_chamber_animal_1,
        LocationName.death_chamber_animal_2,
        LocationName.death_chamber_animal_3,
        LocationName.death_chamber_animal_4,
        LocationName.death_chamber_animal_5,
        LocationName.death_chamber_animal_6,
        LocationName.death_chamber_animal_7,
        LocationName.death_chamber_animal_8,
        LocationName.death_chamber_animal_9,
        LocationName.death_chamber_animal_10,
        LocationName.death_chamber_upgrade,
    ]
    death_chamber_region = create_region(multiworld, player, active_locations, LocationName.death_chamber_region,
                                         death_chamber_region_locations)

    meteor_herd_region_locations = [
        LocationName.meteor_herd_1,
        LocationName.meteor_herd_2,
        LocationName.meteor_herd_3,
        LocationName.meteor_herd_4,
        LocationName.meteor_herd_5,
        LocationName.meteor_herd_chao_1,
        LocationName.meteor_herd_chao_2,
        LocationName.meteor_herd_chao_3,
        LocationName.meteor_herd_pipe_1,
        LocationName.meteor_herd_pipe_2,
        LocationName.meteor_herd_pipe_3,
        LocationName.meteor_herd_omo_1,
        LocationName.meteor_herd_omo_2,
        LocationName.meteor_herd_omo_3,
        LocationName.meteor_herd_beetle,
        LocationName.meteor_herd_animal_1,
        LocationName.meteor_herd_animal_2,
        LocationName.meteor_herd_animal_3,
        LocationName.meteor_herd_animal_4,
        LocationName.meteor_herd_animal_5,
        LocationName.meteor_herd_animal_6,
        LocationName.meteor_herd_animal_7,
        LocationName.meteor_herd_animal_8,
        LocationName.meteor_herd_animal_9,
        LocationName.meteor_herd_animal_10,
        LocationName.meteor_herd_animal_11,
        LocationName.meteor_herd_upgrade,
    ]
    meteor_herd_region = create_region(multiworld, player, active_locations, LocationName.meteor_herd_region,
                                       meteor_herd_region_locations)

    radical_highway_region_locations = [
        LocationName.radical_highway_1,
        LocationName.radical_highway_2,
        LocationName.radical_highway_3,
        LocationName.radical_highway_4,
        LocationName.radical_highway_5,
        LocationName.radical_highway_chao_1,
        LocationName.radical_highway_chao_2,
        LocationName.radical_highway_chao_3,
        LocationName.radical_highway_pipe_1,
        LocationName.radical_highway_pipe_2,
        LocationName.radical_highway_pipe_3,
        LocationName.radical_highway_hidden_1,
        LocationName.radical_highway_hidden_2,
        LocationName.radical_highway_hidden_3,
        LocationName.radical_highway_omo_1,
        LocationName.radical_highway_omo_2,
        LocationName.radical_highway_omo_3,
        LocationName.radical_highway_omo_4,
        LocationName.radical_highway_omo_5,
        LocationName.radical_highway_omo_6,
        LocationName.radical_highway_omo_7,
        LocationName.radical_highway_omo_8,
        LocationName.radical_highway_beetle,
        LocationName.radical_highway_animal_1,
        LocationName.radical_highway_animal_2,
        LocationName.radical_highway_animal_3,
        LocationName.radical_highway_animal_4,
        LocationName.radical_highway_animal_5,
        LocationName.radical_highway_animal_6,
        LocationName.radical_highway_animal_7,
        LocationName.radical_highway_animal_8,
        LocationName.radical_highway_animal_9,
        LocationName.radical_highway_animal_10,
        LocationName.radical_highway_animal_11,
        LocationName.radical_highway_animal_12,
        LocationName.radical_highway_animal_13,
        LocationName.radical_highway_animal_14,
        LocationName.radical_highway_animal_15,
        LocationName.radical_highway_animal_16,
        LocationName.radical_highway_animal_17,
        LocationName.radical_highway_animal_18,
        LocationName.radical_highway_animal_19,
        LocationName.radical_highway_animal_20,
        LocationName.radical_highway_upgrade,
    ]
    radical_highway_region = create_region(multiworld, player, active_locations, LocationName.radical_highway_region,
                                           radical_highway_region_locations)

    white_jungle_region_locations = [
        LocationName.white_jungle_1,
        LocationName.white_jungle_2,
        LocationName.white_jungle_3,
        LocationName.white_jungle_4,
        LocationName.white_jungle_5,
        LocationName.white_jungle_chao_1,
        LocationName.white_jungle_chao_2,
        LocationName.white_jungle_chao_3,
        LocationName.white_jungle_pipe_1,
        LocationName.white_jungle_pipe_2,
        LocationName.white_jungle_pipe_3,
        LocationName.white_jungle_pipe_4,
        LocationName.white_jungle_hidden_1,
        LocationName.white_jungle_hidden_2,
        LocationName.white_jungle_hidden_3,
        LocationName.white_jungle_omo_1,
        LocationName.white_jungle_omo_2,
        LocationName.white_jungle_omo_3,
        LocationName.white_jungle_omo_4,
        LocationName.white_jungle_omo_5,
        LocationName.white_jungle_beetle,
        LocationName.white_jungle_animal_1,
        LocationName.white_jungle_animal_2,
        LocationName.white_jungle_animal_3,
        LocationName.white_jungle_animal_4,
        LocationName.white_jungle_animal_5,
        LocationName.white_jungle_animal_6,
        LocationName.white_jungle_animal_7,
        LocationName.white_jungle_animal_8,
        LocationName.white_jungle_animal_9,
        LocationName.white_jungle_animal_10,
        LocationName.white_jungle_animal_11,
        LocationName.white_jungle_animal_12,
        LocationName.white_jungle_animal_13,
        LocationName.white_jungle_animal_14,
        LocationName.white_jungle_animal_15,
        LocationName.white_jungle_animal_16,
        LocationName.white_jungle_upgrade,
    ]
    white_jungle_region = create_region(multiworld, player, active_locations, LocationName.white_jungle_region,
                                        white_jungle_region_locations)

    sky_rail_region_locations = [
        LocationName.sky_rail_1,
        LocationName.sky_rail_2,
        LocationName.sky_rail_3,
        LocationName.sky_rail_4,
        LocationName.sky_rail_5,
        LocationName.sky_rail_chao_1,
        LocationName.sky_rail_chao_2,
        LocationName.sky_rail_chao_3,
        LocationName.sky_rail_pipe_1,
        LocationName.sky_rail_pipe_2,
        LocationName.sky_rail_pipe_3,
        LocationName.sky_rail_pipe_4,
        LocationName.sky_rail_pipe_5,
        LocationName.sky_rail_pipe_6,
        LocationName.sky_rail_beetle,
        LocationName.sky_rail_animal_1,
        LocationName.sky_rail_animal_2,
        LocationName.sky_rail_animal_3,
        LocationName.sky_rail_animal_4,
        LocationName.sky_rail_animal_5,
        LocationName.sky_rail_animal_6,
        LocationName.sky_rail_animal_7,
        LocationName.sky_rail_animal_8,
        LocationName.sky_rail_animal_9,
        LocationName.sky_rail_animal_10,
        LocationName.sky_rail_animal_11,
        LocationName.sky_rail_animal_12,
        LocationName.sky_rail_animal_13,
        LocationName.sky_rail_animal_14,
        LocationName.sky_rail_animal_15,
        LocationName.sky_rail_animal_16,
        LocationName.sky_rail_animal_17,
        LocationName.sky_rail_animal_18,
        LocationName.sky_rail_animal_19,
        LocationName.sky_rail_animal_20,
        LocationName.sky_rail_upgrade,
    ]
    sky_rail_region = create_region(multiworld, player, active_locations, LocationName.sky_rail_region,
                                    sky_rail_region_locations)

    final_chase_region_locations = [
        LocationName.final_chase_1,
        LocationName.final_chase_2,
        LocationName.final_chase_3,
        LocationName.final_chase_4,
        LocationName.final_chase_5,
        LocationName.final_chase_chao_1,
        LocationName.final_chase_chao_2,
        LocationName.final_chase_chao_3,
        LocationName.final_chase_pipe_1,
        LocationName.final_chase_pipe_2,
        LocationName.final_chase_pipe_3,
        LocationName.final_chase_omo_1,
        LocationName.final_chase_beetle,
        LocationName.final_chase_animal_1,
        LocationName.final_chase_animal_2,
        LocationName.final_chase_animal_3,
        LocationName.final_chase_animal_4,
        LocationName.final_chase_animal_5,
        LocationName.final_chase_animal_6,
        LocationName.final_chase_animal_7,
        LocationName.final_chase_animal_8,
        LocationName.final_chase_animal_9,
        LocationName.final_chase_animal_10,
        LocationName.final_chase_animal_11,
        LocationName.final_chase_animal_12,
        LocationName.final_chase_animal_13,
        LocationName.final_chase_animal_14,
        LocationName.final_chase_animal_15,
        LocationName.final_chase_animal_16,
        LocationName.final_chase_animal_17,
        LocationName.final_chase_upgrade,
    ]
    final_chase_region = create_region(multiworld, player, active_locations, LocationName.final_chase_region,
                                       final_chase_region_locations)

    iron_gate_region_locations = [
        LocationName.iron_gate_1,
        LocationName.iron_gate_2,
        LocationName.iron_gate_3,
        LocationName.iron_gate_4,
        LocationName.iron_gate_5,
        LocationName.iron_gate_chao_1,
        LocationName.iron_gate_chao_2,
        LocationName.iron_gate_chao_3,
        LocationName.iron_gate_pipe_1,
        LocationName.iron_gate_pipe_2,
        LocationName.iron_gate_pipe_3,
        LocationName.iron_gate_pipe_4,
        LocationName.iron_gate_pipe_5,
        LocationName.iron_gate_omo_1,
        LocationName.iron_gate_omo_2,
        LocationName.iron_gate_omo_3,
        LocationName.iron_gate_omo_4,
        LocationName.iron_gate_omo_5,
        LocationName.iron_gate_omo_6,
        LocationName.iron_gate_beetle,
        LocationName.iron_gate_animal_1,
        LocationName.iron_gate_animal_2,
        LocationName.iron_gate_animal_3,
        LocationName.iron_gate_animal_4,
        LocationName.iron_gate_animal_5,
        LocationName.iron_gate_animal_6,
        LocationName.iron_gate_animal_7,
        LocationName.iron_gate_animal_8,
        LocationName.iron_gate_animal_9,
        LocationName.iron_gate_animal_10,
        LocationName.iron_gate_animal_11,
        LocationName.iron_gate_animal_12,
        LocationName.iron_gate_animal_13,
        LocationName.iron_gate_animal_14,
        LocationName.iron_gate_animal_15,
        LocationName.iron_gate_upgrade,
    ]
    iron_gate_region = create_region(multiworld, player, active_locations, LocationName.iron_gate_region,
                                     iron_gate_region_locations)

    sand_ocean_region_locations = [
        LocationName.sand_ocean_1,
        LocationName.sand_ocean_2,
        LocationName.sand_ocean_3,
        LocationName.sand_ocean_4,
        LocationName.sand_ocean_5,
        LocationName.sand_ocean_chao_1,
        LocationName.sand_ocean_chao_2,
        LocationName.sand_ocean_chao_3,
        LocationName.sand_ocean_pipe_1,
        LocationName.sand_ocean_pipe_2,
        LocationName.sand_ocean_pipe_3,
        LocationName.sand_ocean_pipe_4,
        LocationName.sand_ocean_pipe_5,
        LocationName.sand_ocean_omo_1,
        LocationName.sand_ocean_omo_2,
        LocationName.sand_ocean_beetle,
        LocationName.sand_ocean_animal_1,
        LocationName.sand_ocean_animal_2,
        LocationName.sand_ocean_animal_3,
        LocationName.sand_ocean_animal_4,
        LocationName.sand_ocean_animal_5,
        LocationName.sand_ocean_animal_6,
        LocationName.sand_ocean_animal_7,
        LocationName.sand_ocean_animal_8,
        LocationName.sand_ocean_animal_9,
        LocationName.sand_ocean_animal_10,
        LocationName.sand_ocean_animal_11,
        LocationName.sand_ocean_animal_12,
        LocationName.sand_ocean_animal_13,
        LocationName.sand_ocean_animal_14,
        LocationName.sand_ocean_animal_15,
        LocationName.sand_ocean_upgrade,
    ]
    sand_ocean_region = create_region(multiworld, player, active_locations, LocationName.sand_ocean_region,
                                      sand_ocean_region_locations)

    lost_colony_region_locations = [
        LocationName.lost_colony_1,
        LocationName.lost_colony_2,
        LocationName.lost_colony_3,
        LocationName.lost_colony_4,
        LocationName.lost_colony_5,
        LocationName.lost_colony_chao_1,
        LocationName.lost_colony_chao_2,
        LocationName.lost_colony_chao_3,
        LocationName.lost_colony_pipe_1,
        LocationName.lost_colony_pipe_2,
        LocationName.lost_colony_hidden_1,
        LocationName.lost_colony_omo_1,
        LocationName.lost_colony_omo_2,
        LocationName.lost_colony_omo_3,
        LocationName.lost_colony_omo_4,
        LocationName.lost_colony_omo_5,
        LocationName.lost_colony_omo_6,
        LocationName.lost_colony_omo_7,
        LocationName.lost_colony_omo_8,
        LocationName.lost_colony_beetle,
        LocationName.lost_colony_animal_1,
        LocationName.lost_colony_animal_2,
        LocationName.lost_colony_animal_3,
        LocationName.lost_colony_animal_4,
        LocationName.lost_colony_animal_5,
        LocationName.lost_colony_animal_6,
        LocationName.lost_colony_animal_7,
        LocationName.lost_colony_animal_8,
        LocationName.lost_colony_animal_9,
        LocationName.lost_colony_animal_10,
        LocationName.lost_colony_animal_11,
        LocationName.lost_colony_animal_12,
        LocationName.lost_colony_animal_13,
        LocationName.lost_colony_animal_14,
        LocationName.lost_colony_upgrade,
    ]
    lost_colony_region = create_region(multiworld, player, active_locations, LocationName.lost_colony_region,
                                       lost_colony_region_locations)

    weapons_bed_region_locations = [
        LocationName.weapons_bed_1,
        LocationName.weapons_bed_2,
        LocationName.weapons_bed_3,
        LocationName.weapons_bed_4,
        LocationName.weapons_bed_5,
        LocationName.weapons_bed_chao_1,
        LocationName.weapons_bed_chao_2,
        LocationName.weapons_bed_chao_3,
        LocationName.weapons_bed_pipe_1,
        LocationName.weapons_bed_pipe_2,
        LocationName.weapons_bed_pipe_3,
        LocationName.weapons_bed_pipe_4,
        LocationName.weapons_bed_pipe_5,
        LocationName.weapons_bed_omo_1,
        LocationName.weapons_bed_omo_2,
        LocationName.weapons_bed_omo_3,
        LocationName.weapons_bed_animal_1,
        LocationName.weapons_bed_animal_2,
        LocationName.weapons_bed_animal_3,
        LocationName.weapons_bed_animal_4,
        LocationName.weapons_bed_animal_5,
        LocationName.weapons_bed_animal_6,
        LocationName.weapons_bed_animal_7,
        LocationName.weapons_bed_animal_8,
        LocationName.weapons_bed_animal_9,
        LocationName.weapons_bed_animal_10,
        LocationName.weapons_bed_animal_11,
        LocationName.weapons_bed_animal_12,
        LocationName.weapons_bed_animal_13,
        LocationName.weapons_bed_animal_14,
        LocationName.weapons_bed_animal_15,
        LocationName.weapons_bed_upgrade,
    ]
    weapons_bed_region = create_region(multiworld, player, active_locations, LocationName.weapons_bed_region,
                                       weapons_bed_region_locations)

    cosmic_wall_region_locations = [
        LocationName.cosmic_wall_1,
        LocationName.cosmic_wall_2,
        LocationName.cosmic_wall_3,
        LocationName.cosmic_wall_4,
        LocationName.cosmic_wall_5,
        LocationName.cosmic_wall_chao_1,
        LocationName.cosmic_wall_chao_2,
        LocationName.cosmic_wall_chao_3,
        LocationName.cosmic_wall_pipe_1,
        LocationName.cosmic_wall_pipe_2,
        LocationName.cosmic_wall_pipe_3,
        LocationName.cosmic_wall_pipe_4,
        LocationName.cosmic_wall_pipe_5,
        LocationName.cosmic_wall_omo_1,
        LocationName.cosmic_wall_beetle,
        LocationName.cosmic_wall_animal_1,
        LocationName.cosmic_wall_animal_2,
        LocationName.cosmic_wall_animal_3,
        LocationName.cosmic_wall_animal_4,
        LocationName.cosmic_wall_animal_5,
        LocationName.cosmic_wall_animal_6,
        LocationName.cosmic_wall_animal_7,
        LocationName.cosmic_wall_animal_8,
        LocationName.cosmic_wall_animal_9,
        LocationName.cosmic_wall_animal_10,
        LocationName.cosmic_wall_animal_11,
        LocationName.cosmic_wall_animal_12,
        LocationName.cosmic_wall_animal_13,
        LocationName.cosmic_wall_animal_14,
        LocationName.cosmic_wall_animal_15,
        LocationName.cosmic_wall_upgrade,
    ]
    cosmic_wall_region = create_region(multiworld, player, active_locations, LocationName.cosmic_wall_region,
                                       cosmic_wall_region_locations)

    dry_lagoon_region_locations = [
        LocationName.dry_lagoon_1,
        LocationName.dry_lagoon_2,
        LocationName.dry_lagoon_3,
        LocationName.dry_lagoon_4,
        LocationName.dry_lagoon_5,
        LocationName.dry_lagoon_chao_1,
        LocationName.dry_lagoon_chao_2,
        LocationName.dry_lagoon_chao_3,
        LocationName.dry_lagoon_pipe_1,
        LocationName.dry_lagoon_hidden_1,
        LocationName.dry_lagoon_omo_1,
        LocationName.dry_lagoon_omo_2,
        LocationName.dry_lagoon_omo_3,
        LocationName.dry_lagoon_omo_4,
        LocationName.dry_lagoon_omo_5,
        LocationName.dry_lagoon_omo_6,
        LocationName.dry_lagoon_omo_7,
        LocationName.dry_lagoon_omo_8,
        LocationName.dry_lagoon_omo_9,
        LocationName.dry_lagoon_omo_10,
        LocationName.dry_lagoon_omo_11,
        LocationName.dry_lagoon_omo_12,
        LocationName.dry_lagoon_beetle,
        LocationName.dry_lagoon_animal_1,
        LocationName.dry_lagoon_animal_2,
        LocationName.dry_lagoon_animal_3,
        LocationName.dry_lagoon_animal_4,
        LocationName.dry_lagoon_animal_5,
        LocationName.dry_lagoon_animal_6,
        LocationName.dry_lagoon_animal_7,
        LocationName.dry_lagoon_animal_8,
        LocationName.dry_lagoon_animal_9,
        LocationName.dry_lagoon_animal_10,
        LocationName.dry_lagoon_animal_11,
        LocationName.dry_lagoon_upgrade,
    ]
    dry_lagoon_region = create_region(multiworld, player, active_locations, LocationName.dry_lagoon_region,
                                      dry_lagoon_region_locations)

    egg_quarters_region_locations = [
        LocationName.egg_quarters_1,
        LocationName.egg_quarters_2,
        LocationName.egg_quarters_3,
        LocationName.egg_quarters_4,
        LocationName.egg_quarters_5,
        LocationName.egg_quarters_chao_1,
        LocationName.egg_quarters_chao_2,
        LocationName.egg_quarters_chao_3,
        LocationName.egg_quarters_pipe_1,
        LocationName.egg_quarters_pipe_2,
        LocationName.egg_quarters_hidden_1,
        LocationName.egg_quarters_hidden_2,
        LocationName.egg_quarters_omo_1,
        LocationName.egg_quarters_omo_2,
        LocationName.egg_quarters_omo_3,
        LocationName.egg_quarters_omo_4,
        LocationName.egg_quarters_omo_5,
        LocationName.egg_quarters_omo_6,
        LocationName.egg_quarters_omo_7,
        LocationName.egg_quarters_beetle,
        LocationName.egg_quarters_animal_1,
        LocationName.egg_quarters_animal_2,
        LocationName.egg_quarters_animal_3,
        LocationName.egg_quarters_animal_4,
        LocationName.egg_quarters_animal_5,
        LocationName.egg_quarters_animal_6,
        LocationName.egg_quarters_animal_7,
        LocationName.egg_quarters_animal_8,
        LocationName.egg_quarters_animal_9,
        LocationName.egg_quarters_animal_10,
        LocationName.egg_quarters_upgrade,
    ]
    egg_quarters_region = create_region(multiworld, player, active_locations, LocationName.egg_quarters_region,
                                        egg_quarters_region_locations)

    security_hall_region_locations = [
        LocationName.security_hall_1,
        LocationName.security_hall_2,
        LocationName.security_hall_3,
        LocationName.security_hall_4,
        LocationName.security_hall_5,
        LocationName.security_hall_chao_1,
        LocationName.security_hall_chao_2,
        LocationName.security_hall_chao_3,
        LocationName.security_hall_pipe_1,
        LocationName.security_hall_hidden_1,
        LocationName.security_hall_omo_1,
        LocationName.security_hall_omo_2,
        LocationName.security_hall_omo_3,
        LocationName.security_hall_omo_4,
        LocationName.security_hall_omo_5,
        LocationName.security_hall_omo_6,
        LocationName.security_hall_omo_7,
        LocationName.security_hall_omo_8,
        LocationName.security_hall_omo_9,
        LocationName.security_hall_omo_10,
        LocationName.security_hall_omo_11,
        LocationName.security_hall_omo_12,
        LocationName.security_hall_beetle,
        LocationName.security_hall_animal_1,
        LocationName.security_hall_animal_2,
        LocationName.security_hall_animal_3,
        LocationName.security_hall_animal_4,
        LocationName.security_hall_animal_5,
        LocationName.security_hall_animal_6,
        LocationName.security_hall_animal_7,
        LocationName.security_hall_animal_8,
        LocationName.security_hall_upgrade,
    ]
    security_hall_region = create_region(multiworld, player, active_locations, LocationName.security_hall_region,
                                         security_hall_region_locations)

    route_280_region_locations = [
        LocationName.route_280_1,
        LocationName.route_280_2,
        LocationName.route_280_3,
        LocationName.route_280_4,
        LocationName.route_280_5,
    ]
    route_280_region = create_region(multiworld, player, active_locations, LocationName.route_280_region,
                                     route_280_region_locations)

    mad_space_region_locations = [
        LocationName.mad_space_1,
        LocationName.mad_space_2,
        LocationName.mad_space_3,
        LocationName.mad_space_4,
        LocationName.mad_space_5,
        LocationName.mad_space_chao_1,
        LocationName.mad_space_chao_2,
        LocationName.mad_space_chao_3,
        LocationName.mad_space_pipe_1,
        LocationName.mad_space_pipe_2,
        LocationName.mad_space_pipe_3,
        LocationName.mad_space_pipe_4,
        LocationName.mad_space_omo_1,
        LocationName.mad_space_omo_2,
        LocationName.mad_space_omo_3,
        LocationName.mad_space_omo_4,
        LocationName.mad_space_omo_5,
        LocationName.mad_space_beetle,
        LocationName.mad_space_animal_1,
        LocationName.mad_space_animal_2,
        LocationName.mad_space_animal_3,
        LocationName.mad_space_animal_4,
        LocationName.mad_space_animal_5,
        LocationName.mad_space_animal_6,
        LocationName.mad_space_animal_7,
        LocationName.mad_space_animal_8,
        LocationName.mad_space_animal_9,
        LocationName.mad_space_animal_10,
        LocationName.mad_space_upgrade,
    ]
    mad_space_region = create_region(multiworld, player, active_locations, LocationName.mad_space_region,
                                     mad_space_region_locations)

    cannon_core_region_locations = [
        LocationName.cannon_core_1,
        LocationName.cannon_core_2,
        LocationName.cannon_core_3,
        LocationName.cannon_core_4,
        LocationName.cannon_core_5,
        LocationName.cannon_core_chao_1,
        LocationName.cannon_core_chao_2,
        LocationName.cannon_core_chao_3,
        LocationName.cannon_core_pipe_1,
        LocationName.cannon_core_pipe_2,
        LocationName.cannon_core_pipe_3,
        LocationName.cannon_core_pipe_4,
        LocationName.cannon_core_pipe_5,
        LocationName.cannon_core_hidden_1,
        LocationName.cannon_core_omo_1,
        LocationName.cannon_core_omo_2,
        LocationName.cannon_core_omo_3,
        LocationName.cannon_core_omo_4,
        LocationName.cannon_core_omo_5,
        LocationName.cannon_core_omo_6,
        LocationName.cannon_core_omo_7,
        LocationName.cannon_core_omo_8,
        LocationName.cannon_core_omo_9,
        LocationName.cannon_core_animal_1,
        LocationName.cannon_core_animal_2,
        LocationName.cannon_core_animal_3,
        LocationName.cannon_core_animal_4,
        LocationName.cannon_core_animal_5,
        LocationName.cannon_core_animal_6,
        LocationName.cannon_core_animal_7,
        LocationName.cannon_core_animal_8,
        LocationName.cannon_core_animal_9,
        LocationName.cannon_core_animal_10,
        LocationName.cannon_core_animal_11,
        LocationName.cannon_core_animal_12,
        LocationName.cannon_core_animal_13,
        LocationName.cannon_core_animal_14,
        LocationName.cannon_core_animal_15,
        LocationName.cannon_core_animal_16,
        LocationName.cannon_core_animal_17,
        LocationName.cannon_core_animal_18,
        LocationName.cannon_core_animal_19,
        LocationName.cannon_core_beetle,
    ]
    cannon_core_region = create_region(multiworld, player, active_locations, LocationName.cannon_core_region,
                                       cannon_core_region_locations)

    chao_race_beginner_region_locations = [
        LocationName.chao_race_crab_pool_1,
        LocationName.chao_race_crab_pool_2,
        LocationName.chao_race_crab_pool_3,
        LocationName.chao_race_stump_valley_1,
        LocationName.chao_race_stump_valley_2,
        LocationName.chao_race_stump_valley_3,
        LocationName.chao_race_mushroom_forest_1,
        LocationName.chao_race_mushroom_forest_2,
        LocationName.chao_race_mushroom_forest_3,
        LocationName.chao_race_block_canyon_1,
        LocationName.chao_race_block_canyon_2,
        LocationName.chao_race_block_canyon_3,
    ]
    chao_race_beginner_region = create_region(multiworld, player, active_locations, LocationName.chao_race_beginner_region,
                                              chao_race_beginner_region_locations)

    chao_karate_beginner_region_locations = [
        LocationName.chao_beginner_karate_1,
        LocationName.chao_beginner_karate_2,
        LocationName.chao_beginner_karate_3,
        LocationName.chao_beginner_karate_4,
        LocationName.chao_beginner_karate_5,
    ]
    chao_karate_beginner_region = create_region(multiworld, player, active_locations, LocationName.chao_karate_beginner_region,
                                                chao_karate_beginner_region_locations)

    chao_race_intermediate_region_locations = [
        LocationName.chao_race_challenge_1,
        LocationName.chao_race_challenge_2,
        LocationName.chao_race_challenge_3,
        LocationName.chao_race_challenge_4,
        LocationName.chao_race_challenge_5,
        LocationName.chao_race_challenge_6,
        LocationName.chao_race_challenge_7,
        LocationName.chao_race_challenge_8,
        LocationName.chao_race_challenge_9,
        LocationName.chao_race_challenge_10,
        LocationName.chao_race_challenge_11,
        LocationName.chao_race_challenge_12,

        LocationName.chao_race_hero_1,
        LocationName.chao_race_hero_2,
        LocationName.chao_race_hero_3,
        LocationName.chao_race_hero_4,

        LocationName.chao_race_dark_1,
        LocationName.chao_race_dark_2,
        LocationName.chao_race_dark_3,
        LocationName.chao_race_dark_4,
    ]
    chao_race_intermediate_region = create_region(multiworld, player, active_locations, LocationName.chao_race_intermediate_region,
                                                  chao_race_intermediate_region_locations)

    chao_karate_intermediate_region_locations = [
        LocationName.chao_standard_karate_1,
        LocationName.chao_standard_karate_2,
        LocationName.chao_standard_karate_3,
        LocationName.chao_standard_karate_4,
        LocationName.chao_standard_karate_5,
    ]
    chao_karate_intermediate_region = create_region(multiworld, player, active_locations, LocationName.chao_karate_intermediate_region,
                                                    chao_karate_intermediate_region_locations)

    chao_race_expert_region_locations = [
        LocationName.chao_race_aquamarine_1,
        LocationName.chao_race_aquamarine_2,
        LocationName.chao_race_aquamarine_3,
        LocationName.chao_race_aquamarine_4,
        LocationName.chao_race_aquamarine_5,
        LocationName.chao_race_topaz_1,
        LocationName.chao_race_topaz_2,
        LocationName.chao_race_topaz_3,
        LocationName.chao_race_topaz_4,
        LocationName.chao_race_topaz_5,
        LocationName.chao_race_peridot_1,
        LocationName.chao_race_peridot_2,
        LocationName.chao_race_peridot_3,
        LocationName.chao_race_peridot_4,
        LocationName.chao_race_peridot_5,
        LocationName.chao_race_garnet_1,
        LocationName.chao_race_garnet_2,
        LocationName.chao_race_garnet_3,
        LocationName.chao_race_garnet_4,
        LocationName.chao_race_garnet_5,
        LocationName.chao_race_onyx_1,
        LocationName.chao_race_onyx_2,
        LocationName.chao_race_onyx_3,
        LocationName.chao_race_onyx_4,
        LocationName.chao_race_onyx_5,
        LocationName.chao_race_diamond_1,
        LocationName.chao_race_diamond_2,
        LocationName.chao_race_diamond_3,
        LocationName.chao_race_diamond_4,
        LocationName.chao_race_diamond_5,
    ]
    chao_race_expert_region = create_region(multiworld, player, active_locations, LocationName.chao_race_expert_region,
                                            chao_race_expert_region_locations)

    chao_karate_expert_region_locations = [
        LocationName.chao_expert_karate_1,
        LocationName.chao_expert_karate_2,
        LocationName.chao_expert_karate_3,
        LocationName.chao_expert_karate_4,
        LocationName.chao_expert_karate_5,
    ]
    chao_karate_expert_region = create_region(multiworld, player, active_locations, LocationName.chao_karate_expert_region,
                                              chao_karate_expert_region_locations)

    chao_karate_super_region_locations = [
        LocationName.chao_super_karate_1,
        LocationName.chao_super_karate_2,
        LocationName.chao_super_karate_3,
        LocationName.chao_super_karate_4,
        LocationName.chao_super_karate_5,
    ]
    chao_karate_super_region = create_region(multiworld, player, active_locations, LocationName.chao_karate_super_region,
                                             chao_karate_super_region_locations)

    if world.options.goal == 7 or world.options.chao_animal_parts:
        animal_penguin_region_locations = [
            LocationName.animal_penguin,
            LocationName.chao_penguin_arms,
            LocationName.chao_penguin_forehead,
            LocationName.chao_penguin_legs,
        ]
        animal_penguin_region = create_region(multiworld, player, active_locations, LocationName.animal_penguin,
                                              animal_penguin_region_locations)
        conditional_regions += [animal_penguin_region]

        animal_seal_region_locations = [
            LocationName.animal_seal,
            LocationName.chao_seal_arms,
            LocationName.chao_seal_tail,
        ]
        animal_seal_region = create_region(multiworld, player, active_locations, LocationName.animal_seal,
                                           animal_seal_region_locations)
        conditional_regions += [animal_seal_region]

        animal_otter_region_locations = [
            LocationName.animal_otter,
            LocationName.chao_otter_arms,
            LocationName.chao_otter_ears,
            LocationName.chao_otter_face,
            LocationName.chao_otter_legs,
            LocationName.chao_otter_tail,
        ]
        animal_otter_region = create_region(multiworld, player, active_locations, LocationName.animal_otter,
                                            animal_otter_region_locations)
        conditional_regions += [animal_otter_region]

        animal_rabbit_region_locations = [
            LocationName.animal_rabbit,
            LocationName.chao_rabbit_arms,
            LocationName.chao_rabbit_ears,
            LocationName.chao_rabbit_legs,
            LocationName.chao_rabbit_tail,
        ]
        animal_rabbit_region = create_region(multiworld, player, active_locations, LocationName.animal_rabbit,
                                             animal_rabbit_region_locations)
        conditional_regions += [animal_rabbit_region]

        animal_cheetah_region_locations = [
            LocationName.animal_cheetah,
            LocationName.chao_cheetah_arms,
            LocationName.chao_cheetah_ears,
            LocationName.chao_cheetah_legs,
            LocationName.chao_cheetah_tail,
        ]
        animal_cheetah_region = create_region(multiworld, player, active_locations, LocationName.animal_cheetah,
                                              animal_cheetah_region_locations)
        conditional_regions += [animal_cheetah_region]

        animal_warthog_region_locations = [
            LocationName.animal_warthog,
            LocationName.chao_warthog_arms,
            LocationName.chao_warthog_ears,
            LocationName.chao_warthog_face,
            LocationName.chao_warthog_legs,
            LocationName.chao_warthog_tail,
        ]
        animal_warthog_region = create_region(multiworld, player, active_locations, LocationName.animal_warthog,
                                              animal_warthog_region_locations)
        conditional_regions += [animal_warthog_region]

        animal_bear_region_locations = [
            LocationName.animal_bear,
            LocationName.chao_bear_arms,
            LocationName.chao_bear_ears,
            LocationName.chao_bear_legs,
        ]
        animal_bear_region = create_region(multiworld, player, active_locations, LocationName.animal_bear,
                                           animal_bear_region_locations)
        conditional_regions += [animal_bear_region]

        animal_tiger_region_locations = [
            LocationName.animal_tiger,
            LocationName.chao_tiger_arms,
            LocationName.chao_tiger_ears,
            LocationName.chao_tiger_legs,
            LocationName.chao_tiger_tail,
        ]
        animal_tiger_region = create_region(multiworld, player, active_locations, LocationName.animal_tiger,
                                            animal_tiger_region_locations)
        conditional_regions += [animal_tiger_region]

        animal_gorilla_region_locations = [
            LocationName.animal_gorilla,
            LocationName.chao_gorilla_arms,
            LocationName.chao_gorilla_ears,
            LocationName.chao_gorilla_forehead,
            LocationName.chao_gorilla_legs,
        ]
        animal_gorilla_region = create_region(multiworld, player, active_locations, LocationName.animal_gorilla,
                                              animal_gorilla_region_locations)
        conditional_regions += [animal_gorilla_region]

        animal_peacock_region_locations = [
            LocationName.animal_peacock,
            LocationName.chao_peacock_forehead,
            LocationName.chao_peacock_legs,
            LocationName.chao_peacock_tail,
            LocationName.chao_peacock_wings,
        ]
        animal_peacock_region = create_region(multiworld, player, active_locations, LocationName.animal_peacock,
                                              animal_peacock_region_locations)
        conditional_regions += [animal_peacock_region]

        animal_parrot_region_locations = [
            LocationName.animal_parrot,
            LocationName.chao_parrot_forehead,
            LocationName.chao_parrot_legs,
            LocationName.chao_parrot_tail,
            LocationName.chao_parrot_wings,
        ]
        animal_parrot_region = create_region(multiworld, player, active_locations, LocationName.animal_parrot,
                                             animal_parrot_region_locations)
        conditional_regions += [animal_parrot_region]

        animal_condor_region_locations = [
            LocationName.animal_condor,
            LocationName.chao_condor_ears,
            LocationName.chao_condor_legs,
            LocationName.chao_condor_tail,
            LocationName.chao_condor_wings,
        ]
        animal_condor_region = create_region(multiworld, player, active_locations, LocationName.animal_condor,
                                             animal_condor_region_locations)
        conditional_regions += [animal_condor_region]

        animal_skunk_region_locations = [
            LocationName.animal_skunk,
            LocationName.chao_skunk_arms,
            LocationName.chao_skunk_forehead,
            LocationName.chao_skunk_legs,
            LocationName.chao_skunk_tail,
        ]
        animal_skunk_region = create_region(multiworld, player, active_locations, LocationName.animal_skunk,
                                            animal_skunk_region_locations)
        conditional_regions += [animal_skunk_region]

        animal_sheep_region_locations = [
            LocationName.animal_sheep,
            LocationName.chao_sheep_arms,
            LocationName.chao_sheep_ears,
            LocationName.chao_sheep_legs,
            LocationName.chao_sheep_horn,
            LocationName.chao_sheep_tail,
        ]
        animal_sheep_region = create_region(multiworld, player, active_locations, LocationName.animal_sheep,
                                            animal_sheep_region_locations)
        conditional_regions += [animal_sheep_region]

        animal_raccoon_region_locations = [
            LocationName.animal_raccoon,
            LocationName.chao_raccoon_arms,
            LocationName.chao_raccoon_ears,
            LocationName.chao_raccoon_legs,
        ]
        animal_raccoon_region = create_region(multiworld, player, active_locations, LocationName.animal_raccoon,
                                              animal_raccoon_region_locations)
        conditional_regions += [animal_raccoon_region]

        animal_halffish_region_locations = [
            LocationName.animal_halffish,
        ]
        animal_halffish_region = create_region(multiworld, player, active_locations, LocationName.animal_halffish,
                                               animal_halffish_region_locations)
        conditional_regions += [animal_halffish_region]

        animal_skeleton_dog_region_locations = [
            LocationName.animal_skeleton_dog,
        ]
        animal_skeleton_dog_region = create_region(multiworld, player, active_locations, LocationName.animal_skeleton_dog,
                                                   animal_skeleton_dog_region_locations)
        conditional_regions += [animal_skeleton_dog_region]

        animal_bat_region_locations = [
            LocationName.animal_bat,
        ]
        animal_bat_region = create_region(multiworld, player, active_locations, LocationName.animal_bat,
                                          animal_bat_region_locations)
        conditional_regions += [animal_bat_region]

        animal_dragon_region_locations = [
            LocationName.animal_dragon,
            LocationName.chao_dragon_arms,
            LocationName.chao_dragon_ears,
            LocationName.chao_dragon_legs,
            LocationName.chao_dragon_horn,
            LocationName.chao_dragon_tail,
            LocationName.chao_dragon_wings,
        ]
        animal_dragon_region = create_region(multiworld, player, active_locations, LocationName.animal_dragon,
                                             animal_dragon_region_locations)
        conditional_regions += [animal_dragon_region]

        animal_unicorn_region_locations = [
            LocationName.animal_unicorn,
            LocationName.chao_unicorn_arms,
            LocationName.chao_unicorn_ears,
            LocationName.chao_unicorn_forehead,
            LocationName.chao_unicorn_legs,
            LocationName.chao_unicorn_tail,
        ]
        animal_unicorn_region = create_region(multiworld, player, active_locations, LocationName.animal_unicorn,
                                              animal_unicorn_region_locations)
        conditional_regions += [animal_unicorn_region]

        animal_phoenix_region_locations = [
            LocationName.animal_phoenix,
            LocationName.chao_phoenix_forehead,
            LocationName.chao_phoenix_legs,
            LocationName.chao_phoenix_tail,
            LocationName.chao_phoenix_wings,
        ]
        animal_phoenix_region = create_region(multiworld, player, active_locations, LocationName.animal_phoenix,
                                              animal_phoenix_region_locations)
        conditional_regions += [animal_phoenix_region]

    if world.options.chao_kindergarten:
        chao_kindergarten_region_locations = list(chao_kindergarten_location_table.keys()) + list(chao_kindergarten_basics_location_table.keys())
        chao_kindergarten_region = create_region(multiworld, player, active_locations, LocationName.chao_kindergarten_region,
                                                 chao_kindergarten_region_locations)
        conditional_regions += [chao_kindergarten_region]

    if world.options.black_market_slots.value > 0:

        black_market_region_locations = list(black_market_location_table.keys())
        black_market_region = create_region(multiworld, player, active_locations, LocationName.black_market_region,
                                            black_market_region_locations)
        conditional_regions += [black_market_region]

    kart_race_beginner_region_locations = []
    if world.options.kart_race_checks == 2:
        kart_race_beginner_region_locations.extend([
            LocationName.kart_race_beginner_sonic,
            LocationName.kart_race_beginner_tails,
            LocationName.kart_race_beginner_knuckles,
            LocationName.kart_race_beginner_shadow,
            LocationName.kart_race_beginner_eggman,
            LocationName.kart_race_beginner_rouge,
        ])
    if world.options.kart_race_checks == 1:
        kart_race_beginner_region_locations.append(LocationName.kart_race_beginner)
    kart_race_beginner_region = create_region(multiworld, player, active_locations, LocationName.kart_race_beginner_region,
                                              kart_race_beginner_region_locations)

    kart_race_standard_region_locations = []
    if world.options.kart_race_checks == 2:
        kart_race_standard_region_locations.extend([
            LocationName.kart_race_standard_sonic,
            LocationName.kart_race_standard_tails,
            LocationName.kart_race_standard_knuckles,
            LocationName.kart_race_standard_shadow,
            LocationName.kart_race_standard_eggman,
            LocationName.kart_race_standard_rouge,
        ])
    if world.options.kart_race_checks == 1:
        kart_race_standard_region_locations.append(LocationName.kart_race_standard)
    kart_race_standard_region = create_region(multiworld, player, active_locations, LocationName.kart_race_standard_region,
                                              kart_race_standard_region_locations)

    kart_race_expert_region_locations = []
    if world.options.kart_race_checks == 2:
        kart_race_expert_region_locations.extend([
            LocationName.kart_race_expert_sonic,
            LocationName.kart_race_expert_tails,
            LocationName.kart_race_expert_knuckles,
            LocationName.kart_race_expert_shadow,
            LocationName.kart_race_expert_eggman,
            LocationName.kart_race_expert_rouge,
        ])
    if world.options.kart_race_checks == 1:
        kart_race_expert_region_locations.append(LocationName.kart_race_expert)
    kart_race_expert_region = create_region(multiworld, player, active_locations, LocationName.kart_race_expert_region,
                                            kart_race_expert_region_locations)

    if world.options.goal == 3:
        grand_prix_region_locations = [
            LocationName.grand_prix,
        ]
        grand_prix_region = create_region(multiworld, player, active_locations, LocationName.grand_prix_region,
                                          grand_prix_region_locations)
        conditional_regions += [grand_prix_region]
    elif world.options.goal in [0, 2, 4, 5, 6]:
        biolizard_region_locations = [
            LocationName.finalhazard,
        ]
        biolizard_region = create_region(multiworld, player, active_locations, LocationName.biolizard_region,
                                         biolizard_region_locations)
        conditional_regions += [biolizard_region]
    elif world.options.goal == 7:
        chaos_chao_region_locations = [
            LocationName.chaos_chao,
        ]
        chaos_chao_region = create_region(multiworld, player, active_locations, LocationName.chaos_chao_region,
                                          chaos_chao_region_locations)
        conditional_regions += [chaos_chao_region]

    if world.options.goal in [1, 2]:
        green_hill_region_locations = [
            LocationName.green_hill,
            LocationName.green_hill_chao_1,
            #LocationName.green_hill_animal_1,
        ]
        green_hill_region = create_region(multiworld, player, active_locations, LocationName.green_hill_region,
                                          green_hill_region_locations)
        conditional_regions += [green_hill_region]

    if world.options.goal in [4, 5, 6]:
        for i in range(16):
            boss_region_locations = [
                "Boss Rush - " + str(i + 1),
            ]
            boss_region = create_region(multiworld, player, active_locations, "Boss Rush " + str(i + 1),
                                        boss_region_locations)
            conditional_regions += [boss_region]


    # Set up the regions correctly.
    multiworld.regions += [
        menu_region,
        city_escape_region,
        metal_harbor_region,
        green_forest_region,
        pyramid_cave_region,
        crazy_gadget_region,
        final_rush_region,
        prison_lane_region,
        mission_street_region,
        route_101_region,
        hidden_base_region,
        eternal_engine_region,
        wild_canyon_region,
        pumpkin_hill_region,
        aquatic_mine_region,
        death_chamber_region,
        meteor_herd_region,
        radical_highway_region,
        white_jungle_region,
        sky_rail_region,
        final_chase_region,
        iron_gate_region,
        sand_ocean_region,
        lost_colony_region,
        weapons_bed_region,
        cosmic_wall_region,
        dry_lagoon_region,
        egg_quarters_region,
        security_hall_region,
        route_280_region,
        mad_space_region,
        cannon_core_region,
        chao_race_beginner_region,
        chao_karate_beginner_region,
        chao_race_intermediate_region,
        chao_karate_intermediate_region,
        chao_race_expert_region,
        chao_karate_expert_region,
        chao_karate_super_region,
        kart_race_beginner_region,
        kart_race_standard_region,
        kart_race_expert_region,
    ]

    multiworld.regions += conditional_regions


def connect_regions(multiworld: MultiWorld, world: World, player: int, gates: typing.List[LevelGate], cannon_core_emblems, gate_bosses, boss_rush_bosses, first_cannons_core_mission: str, final_cannons_core_mission: str):
    names: typing.Dict[str, int] = {}

    connect(multiworld, player, names, 'Menu', LocationName.gate_0_region)
    connect(multiworld, player, names, LocationName.gate_0_region, LocationName.cannon_core_region,
            lambda state: (state.has(ItemName.emblem, player, cannon_core_emblems)))

    if world.options.goal == 0:
        required_mission_name = first_cannons_core_mission

        if world.options.required_cannons_core_missions.value == 1:
            required_mission_name = final_cannons_core_mission

        connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.biolizard_region,
                lambda state: (state.can_reach(required_mission_name, "Location", player)))
    elif world.options.goal in [1, 2]:
        connect(multiworld, player, names, 'Menu', LocationName.green_hill_region,
                lambda state: (state.has(ItemName.white_emerald, player) and
                               state.has(ItemName.red_emerald, player) and
                               state.has(ItemName.cyan_emerald, player) and
                               state.has(ItemName.purple_emerald, player) and
                               state.has(ItemName.green_emerald, player) and
                               state.has(ItemName.yellow_emerald, player) and
                               state.has(ItemName.blue_emerald, player)))
        if world.options.goal == 2:
            connect(multiworld, player, names, LocationName.green_hill_region, LocationName.biolizard_region)
    elif world.options.goal == 3:
        connect(multiworld, player, names, LocationName.kart_race_expert_region, LocationName.grand_prix_region)
    elif world.options.goal in [4, 5, 6]:
        if world.options.goal == 4:
            connect(multiworld, player, names, LocationName.gate_0_region, LocationName.boss_rush_1_region)
        elif world.options.goal == 5:
            required_mission_name = first_cannons_core_mission

            if world.options.required_cannons_core_missions.value == 1:
                required_mission_name = final_cannons_core_mission

            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.boss_rush_1_region,
                    lambda state: (state.can_reach(required_mission_name, "Location", player)))
        elif world.options.goal == 6:
            connect(multiworld, player, names, LocationName.gate_0_region, LocationName.boss_rush_1_region,
                    lambda state: (state.has(ItemName.white_emerald, player) and
                                   state.has(ItemName.red_emerald, player) and
                                   state.has(ItemName.cyan_emerald, player) and
                                   state.has(ItemName.purple_emerald, player) and
                                   state.has(ItemName.green_emerald, player) and
                                   state.has(ItemName.yellow_emerald, player) and
                                   state.has(ItemName.blue_emerald, player)))

        for i in range(15):
            if boss_rush_bosses[i] == all_gate_bosses_table[king_boom_boo]:
                connect(multiworld, player, names, "Boss Rush " + str(i + 1), "Boss Rush " + str(i + 2),
                        lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
            else:
                connect(multiworld, player, names, "Boss Rush " + str(i + 1), "Boss Rush " + str(i + 2))

        connect(multiworld, player, names, LocationName.boss_rush_16_region, LocationName.biolizard_region)
    elif world.options.goal == 7:
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chaos_chao,
                lambda state: (state.has_all(chao_animal_event_location_table.keys(), player)))

    for i in range(len(gates[0].gate_levels)):
        connect(multiworld, player, names, LocationName.gate_0_region, shuffleable_regions[gates[0].gate_levels[i]])

    gates_len = len(gates)
    if gates_len >= 2:
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.gate_1_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[1].gate_emblem_count)))

        if gate_bosses[1] == all_gate_bosses_table[king_boom_boo]:
            connect(multiworld, player, names, LocationName.gate_1_boss_region, LocationName.gate_1_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(multiworld, player, names, LocationName.gate_1_boss_region, LocationName.gate_1_region)

        for i in range(len(gates[1].gate_levels)):
            connect(multiworld, player, names, LocationName.gate_1_region, shuffleable_regions[gates[1].gate_levels[i]])

    if gates_len >= 3:
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.gate_2_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[2].gate_emblem_count)))

        if gate_bosses[2] == all_gate_bosses_table[king_boom_boo]:
            connect(multiworld, player, names, LocationName.gate_2_boss_region, LocationName.gate_2_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(multiworld, player, names, LocationName.gate_2_boss_region, LocationName.gate_2_region)

        for i in range(len(gates[2].gate_levels)):
            connect(multiworld, player, names, LocationName.gate_2_region, shuffleable_regions[gates[2].gate_levels[i]])

    if gates_len >= 4:
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.gate_3_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[3].gate_emblem_count)))

        if gate_bosses[3] == all_gate_bosses_table[king_boom_boo]:
            connect(multiworld, player, names, LocationName.gate_3_boss_region, LocationName.gate_3_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(multiworld, player, names, LocationName.gate_3_boss_region, LocationName.gate_3_region)

        for i in range(len(gates[3].gate_levels)):
            connect(multiworld, player, names, LocationName.gate_3_region, shuffleable_regions[gates[3].gate_levels[i]])

    if gates_len >= 5:
        connect(multiworld, player, names, LocationName.gate_3_region, LocationName.gate_4_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[4].gate_emblem_count)))

        if gate_bosses[4] == all_gate_bosses_table[king_boom_boo]:
            connect(multiworld, player, names, LocationName.gate_4_boss_region, LocationName.gate_4_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(multiworld, player, names, LocationName.gate_4_boss_region, LocationName.gate_4_region)

        for i in range(len(gates[4].gate_levels)):
            connect(multiworld, player, names, LocationName.gate_4_region, shuffleable_regions[gates[4].gate_levels[i]])

    if gates_len >= 6:
        connect(multiworld, player, names, LocationName.gate_4_region, LocationName.gate_5_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[5].gate_emblem_count)))

        if gate_bosses[5] == all_gate_bosses_table[king_boom_boo]:
            connect(multiworld, player, names, LocationName.gate_5_boss_region, LocationName.gate_5_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(multiworld, player, names, LocationName.gate_5_boss_region, LocationName.gate_5_region)

        for i in range(len(gates[5].gate_levels)):
            connect(multiworld, player, names, LocationName.gate_5_region, shuffleable_regions[gates[5].gate_levels[i]])

    if gates_len == 1:
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_race_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_race_expert_region)

        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_karate_beginner_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_karate_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_karate_expert_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_karate_super_region)

        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.kart_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.kart_race_standard_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.kart_race_expert_region)

        if world.options.chao_kindergarten:
            connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_kindergarten_region)
    elif gates_len == 2:
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_race_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_race_expert_region)

        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_karate_beginner_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_karate_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_karate_expert_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_karate_super_region)

        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.kart_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.kart_race_standard_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.kart_race_expert_region)

        if world.options.chao_kindergarten:
            connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_kindergarten_region)
    elif gates_len == 3:
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_race_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_race_expert_region)

        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_karate_beginner_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_karate_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_karate_expert_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_karate_super_region)

        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.kart_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.kart_race_standard_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.kart_race_expert_region)

        if world.options.chao_kindergarten:
            connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_kindergarten_region)
    elif gates_len == 4:
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_race_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_3_region, LocationName.chao_race_expert_region)

        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.chao_karate_beginner_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_karate_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_karate_expert_region)
        connect(multiworld, player, names, LocationName.gate_3_region, LocationName.chao_karate_super_region)

        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.kart_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.kart_race_standard_region)
        connect(multiworld, player, names, LocationName.gate_3_region, LocationName.kart_race_expert_region)

        if world.options.chao_kindergarten:
            connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_kindergarten_region)
    elif gates_len == 5:
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_race_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_3_region, LocationName.chao_race_expert_region)

        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_karate_beginner_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_karate_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_3_region, LocationName.chao_karate_expert_region)
        connect(multiworld, player, names, LocationName.gate_4_region, LocationName.chao_karate_super_region)

        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.kart_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.kart_race_standard_region)
        connect(multiworld, player, names, LocationName.gate_3_region, LocationName.kart_race_expert_region)

        if world.options.chao_kindergarten:
            connect(multiworld, player, names, LocationName.gate_3_region, LocationName.chao_kindergarten_region)
    elif gates_len >= 6:
        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_race_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_4_region, LocationName.chao_race_expert_region)

        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.chao_karate_beginner_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.chao_karate_intermediate_region)
        connect(multiworld, player, names, LocationName.gate_3_region, LocationName.chao_karate_expert_region)
        connect(multiworld, player, names, LocationName.gate_4_region, LocationName.chao_karate_super_region)

        connect(multiworld, player, names, LocationName.gate_1_region, LocationName.kart_race_beginner_region)
        connect(multiworld, player, names, LocationName.gate_2_region, LocationName.kart_race_standard_region)
        connect(multiworld, player, names, LocationName.gate_4_region, LocationName.kart_race_expert_region)

        if world.options.chao_kindergarten:
            connect(multiworld, player, names, LocationName.gate_3_region, LocationName.chao_kindergarten_region)

    stat_checks_per_gate = world.options.chao_stats.value / (gates_len)
    for index in range(1, world.options.chao_stats.value + 1):
        if (index % world.options.chao_stats_frequency.value) == (world.options.chao_stats.value % world.options.chao_stats_frequency.value):
            gate_val    = math.ceil(index / stat_checks_per_gate) - 1
            gate_region = multiworld.get_region("Gate " + str(gate_val), player)

            loc_name_swim = LocationName.chao_stat_swim_base + str(index)
            loc_id_swim   = chao_stat_swim_table[loc_name_swim]
            location_swim = SA2BLocation(player, loc_name_swim, loc_id_swim, gate_region)
            gate_region.locations.append(location_swim)

            loc_name_fly = LocationName.chao_stat_fly_base + str(index)
            loc_id_fly   = chao_stat_fly_table[loc_name_fly]
            location_fly = SA2BLocation(player, loc_name_fly, loc_id_fly, gate_region)
            gate_region.locations.append(location_fly)

            loc_name_run = LocationName.chao_stat_run_base + str(index)
            loc_id_run   = chao_stat_run_table[loc_name_run]
            location_run = SA2BLocation(player, loc_name_run, loc_id_run, gate_region)
            gate_region.locations.append(location_run)

            loc_name_power = LocationName.chao_stat_power_base + str(index)
            loc_id_power   = chao_stat_power_table[loc_name_power]
            location_power = SA2BLocation(player, loc_name_power, loc_id_power, gate_region)
            gate_region.locations.append(location_power)

            if world.options.chao_stats_stamina:
                loc_name_stamina = LocationName.chao_stat_stamina_base + str(index)
                loc_id_stamina   = chao_stat_stamina_table[loc_name_stamina]
                location_stamina = SA2BLocation(player, loc_name_stamina, loc_id_stamina, gate_region)
                gate_region.locations.append(location_stamina)

            if world.options.chao_stats_hidden:
                loc_name_luck = LocationName.chao_stat_luck_base + str(index)
                loc_id_luck   = chao_stat_luck_table[loc_name_luck]
                location_luck = SA2BLocation(player, loc_name_luck, loc_id_luck, gate_region)
                gate_region.locations.append(location_luck)

                loc_name_intelligence = LocationName.chao_stat_intelligence_base + str(index)
                loc_id_intelligence   = chao_stat_intelligence_table[loc_name_intelligence]
                location_intelligence = SA2BLocation(player, loc_name_intelligence, loc_id_intelligence, gate_region)
                gate_region.locations.append(location_intelligence)

    # Handle access to Animal Parts
    if world.options.goal == 7 or world.options.chao_animal_parts:
        connect(multiworld, player, names, LocationName.city_escape_region, LocationName.animal_rabbit)
        connect(multiworld, player, names, LocationName.city_escape_region, LocationName.animal_skunk)
        connect(multiworld, player, names, LocationName.city_escape_region, LocationName.animal_sheep)
        connect(multiworld, player, names, LocationName.city_escape_region, LocationName.animal_raccoon)

        connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_cheetah)
        connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_peacock)
        connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_condor)
        connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_sheep)

        connect(multiworld, player, names, LocationName.prison_lane_region, LocationName.animal_otter)
        connect(multiworld, player, names, LocationName.prison_lane_region, LocationName.animal_tiger)
        connect(multiworld, player, names, LocationName.prison_lane_region, LocationName.animal_gorilla)
        connect(multiworld, player, names, LocationName.prison_lane_region, LocationName.animal_sheep)
        connect(multiworld, player, names, LocationName.prison_lane_region, LocationName.animal_unicorn,
                lambda state: (state.has(ItemName.tails_booster, player)))

        connect(multiworld, player, names, LocationName.metal_harbor_region, LocationName.animal_penguin)
        connect(multiworld, player, names, LocationName.metal_harbor_region, LocationName.animal_seal)
        connect(multiworld, player, names, LocationName.metal_harbor_region, LocationName.animal_peacock)
        connect(multiworld, player, names, LocationName.metal_harbor_region, LocationName.animal_raccoon)

        connect(multiworld, player, names, LocationName.green_forest_region, LocationName.animal_rabbit)
        connect(multiworld, player, names, LocationName.green_forest_region, LocationName.animal_cheetah)
        connect(multiworld, player, names, LocationName.green_forest_region, LocationName.animal_parrot)
        connect(multiworld, player, names, LocationName.green_forest_region, LocationName.animal_raccoon)
        connect(multiworld, player, names, LocationName.green_forest_region, LocationName.animal_halffish)

        connect(multiworld, player, names, LocationName.pumpkin_hill_region, LocationName.animal_cheetah)
        connect(multiworld, player, names, LocationName.pumpkin_hill_region, LocationName.animal_warthog)
        connect(multiworld, player, names, LocationName.pumpkin_hill_region, LocationName.animal_skeleton_dog)
        connect(multiworld, player, names, LocationName.pumpkin_hill_region, LocationName.animal_bat)

        connect(multiworld, player, names, LocationName.mission_street_region, LocationName.animal_rabbit)
        connect(multiworld, player, names, LocationName.mission_street_region, LocationName.animal_warthog)
        connect(multiworld, player, names, LocationName.mission_street_region, LocationName.animal_gorilla)
        connect(multiworld, player, names, LocationName.mission_street_region, LocationName.animal_sheep)

        connect(multiworld, player, names, LocationName.aquatic_mine_region, LocationName.animal_penguin)
        connect(multiworld, player, names, LocationName.aquatic_mine_region, LocationName.animal_seal)
        connect(multiworld, player, names, LocationName.aquatic_mine_region, LocationName.animal_condor)
        connect(multiworld, player, names, LocationName.aquatic_mine_region, LocationName.animal_skunk)
        connect(multiworld, player, names, LocationName.aquatic_mine_region, LocationName.animal_dragon)

        connect(multiworld, player, names, LocationName.hidden_base_region, LocationName.animal_penguin,
                lambda state: (state.has(ItemName.tails_booster, player)))
        connect(multiworld, player, names, LocationName.hidden_base_region, LocationName.animal_otter,
                lambda state: (state.has(ItemName.tails_booster, player)))
        connect(multiworld, player, names, LocationName.hidden_base_region, LocationName.animal_tiger,
                lambda state: (state.has(ItemName.tails_booster, player)))
        connect(multiworld, player, names, LocationName.hidden_base_region, LocationName.animal_skunk)
        connect(multiworld, player, names, LocationName.hidden_base_region, LocationName.animal_halffish,
                lambda state: (state.has(ItemName.tails_booster, player)))

        connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_peacock)
        connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_condor)
        connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_sheep)
        connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_bat)

        connect(multiworld, player, names, LocationName.death_chamber_region, LocationName.animal_rabbit)
        connect(multiworld, player, names, LocationName.death_chamber_region, LocationName.animal_tiger)
        connect(multiworld, player, names, LocationName.death_chamber_region, LocationName.animal_gorilla)
        connect(multiworld, player, names, LocationName.death_chamber_region, LocationName.animal_skunk)

        connect(multiworld, player, names, LocationName.eternal_engine_region, LocationName.animal_warthog)
        connect(multiworld, player, names, LocationName.eternal_engine_region, LocationName.animal_parrot,
                lambda state: (state.has(ItemName.tails_booster, player)))
        connect(multiworld, player, names, LocationName.eternal_engine_region, LocationName.animal_condor)
        connect(multiworld, player, names, LocationName.eternal_engine_region, LocationName.animal_raccoon)

        connect(multiworld, player, names, LocationName.meteor_herd_region, LocationName.animal_penguin)
        connect(multiworld, player, names, LocationName.meteor_herd_region, LocationName.animal_seal)
        connect(multiworld, player, names, LocationName.meteor_herd_region, LocationName.animal_rabbit)
        connect(multiworld, player, names, LocationName.meteor_herd_region, LocationName.animal_sheep)
        connect(multiworld, player, names, LocationName.meteor_herd_region, LocationName.animal_phoenix)

        connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_seal)
        connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_bear)
        connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_tiger)

        connect(multiworld, player, names, LocationName.final_rush_region, LocationName.animal_penguin)
        connect(multiworld, player, names, LocationName.final_rush_region, LocationName.animal_peacock)
        connect(multiworld, player, names, LocationName.final_rush_region, LocationName.animal_condor)
        connect(multiworld, player, names, LocationName.final_rush_region, LocationName.animal_sheep)
        connect(multiworld, player, names, LocationName.final_rush_region, LocationName.animal_dragon,
                lambda state: (state.has(ItemName.sonic_bounce_bracelet, player)))

        connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_rabbit)
        connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_tiger)
        connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_gorilla)
        connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_skunk)

        connect(multiworld, player, names, LocationName.dry_lagoon_region, LocationName.animal_penguin)
        connect(multiworld, player, names, LocationName.dry_lagoon_region, LocationName.animal_otter)
        connect(multiworld, player, names, LocationName.dry_lagoon_region, LocationName.animal_peacock)
        connect(multiworld, player, names, LocationName.dry_lagoon_region, LocationName.animal_sheep)
        connect(multiworld, player, names, LocationName.dry_lagoon_region, LocationName.animal_unicorn)

        connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_peacock)
        connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_parrot)
        connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_raccoon)
        connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_bat)

        connect(multiworld, player, names, LocationName.radical_highway_region, LocationName.animal_seal)
        connect(multiworld, player, names, LocationName.radical_highway_region, LocationName.animal_cheetah)
        connect(multiworld, player, names, LocationName.radical_highway_region, LocationName.animal_warthog)
        connect(multiworld, player, names, LocationName.radical_highway_region, LocationName.animal_raccoon)

        connect(multiworld, player, names, LocationName.egg_quarters_region, LocationName.animal_bear)
        connect(multiworld, player, names, LocationName.egg_quarters_region, LocationName.animal_gorilla)
        connect(multiworld, player, names, LocationName.egg_quarters_region, LocationName.animal_parrot)
        connect(multiworld, player, names, LocationName.egg_quarters_region, LocationName.animal_skunk)
        connect(multiworld, player, names, LocationName.egg_quarters_region, LocationName.animal_halffish)

        connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_rabbit)
        connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_warthog)
        connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_bat)

        connect(multiworld, player, names, LocationName.weapons_bed_region, LocationName.animal_seal)
        connect(multiworld, player, names, LocationName.weapons_bed_region, LocationName.animal_otter)
        connect(multiworld, player, names, LocationName.weapons_bed_region, LocationName.animal_cheetah)
        connect(multiworld, player, names, LocationName.weapons_bed_region, LocationName.animal_sheep)

        connect(multiworld, player, names, LocationName.security_hall_region, LocationName.animal_tiger)
        connect(multiworld, player, names, LocationName.security_hall_region, LocationName.animal_parrot)
        connect(multiworld, player, names, LocationName.security_hall_region, LocationName.animal_condor)
        connect(multiworld, player, names, LocationName.security_hall_region, LocationName.animal_raccoon)

        connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_bear)
        connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_peacock)
        connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_parrot)
        connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_skunk)

        connect(multiworld, player, names, LocationName.sky_rail_region, LocationName.animal_bear)
        connect(multiworld, player, names, LocationName.sky_rail_region, LocationName.animal_tiger)
        connect(multiworld, player, names, LocationName.sky_rail_region, LocationName.animal_condor)
        connect(multiworld, player, names, LocationName.sky_rail_region, LocationName.animal_sheep)

        connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_peacock)
        connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_parrot)

        connect(multiworld, player, names, LocationName.cosmic_wall_region, LocationName.animal_otter,
                lambda state: (state.has(ItemName.eggman_jet_engine, player)))
        connect(multiworld, player, names, LocationName.cosmic_wall_region, LocationName.animal_rabbit)
        connect(multiworld, player, names, LocationName.cosmic_wall_region, LocationName.animal_cheetah,
                lambda state: (state.has(ItemName.eggman_jet_engine, player)))
        connect(multiworld, player, names, LocationName.cosmic_wall_region, LocationName.animal_sheep,
                lambda state: (state.has(ItemName.eggman_jet_engine, player)))
        connect(multiworld, player, names, LocationName.cosmic_wall_region, LocationName.animal_dragon,
                lambda state: (state.has(ItemName.eggman_jet_engine, player)))

        connect(multiworld, player, names, LocationName.final_chase_region, LocationName.animal_penguin)
        connect(multiworld, player, names, LocationName.final_chase_region, LocationName.animal_otter)
        connect(multiworld, player, names, LocationName.final_chase_region, LocationName.animal_tiger)
        connect(multiworld, player, names, LocationName.final_chase_region, LocationName.animal_skunk)
        connect(multiworld, player, names, LocationName.final_chase_region, LocationName.animal_phoenix)

        connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_seal)
        connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_bear,
                lambda state: (state.has(ItemName.tails_booster, player)))
        connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_gorilla)
        connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_skunk)

        if world.options.goal in [1, 2]:
            connect(multiworld, player, names, LocationName.green_hill_region, LocationName.animal_penguin)
            connect(multiworld, player, names, LocationName.green_hill_region, LocationName.animal_otter)
            connect(multiworld, player, names, LocationName.green_hill_region, LocationName.animal_gorilla)
            connect(multiworld, player, names, LocationName.green_hill_region, LocationName.animal_raccoon)
            connect(multiworld, player, names, LocationName.green_hill_region, LocationName.animal_unicorn)

        if world.options.logic_difficulty.value == 0:
            connect(multiworld, player, names, LocationName.metal_harbor_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.sonic_light_shoes, player)))

            connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_skunk,
                    lambda state: (state.has(ItemName.sonic_bounce_bracelet, player)))
            connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.sonic_light_shoes, player) and
                                   state.has(ItemName.sonic_bounce_bracelet, player) and
                                   state.has(ItemName.sonic_flame_ring, player)))

            connect(multiworld, player, names, LocationName.weapons_bed_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.eggman_jet_engine, player) and
                                   state.has(ItemName.eggman_large_cannon, player)))

            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_gorilla,
                    lambda state: (state.has(ItemName.rouge_iron_boots, player)))
            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_raccoon,
                    lambda state: (state.has(ItemName.rouge_iron_boots, player)))
            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_halffish,
                    lambda state: (state.has(ItemName.rouge_iron_boots, player)))

            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_otter,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.eggman_jet_engine, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_rabbit,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.eggman_jet_engine, player) and
                                   state.has(ItemName.knuckles_air_necklace, player) and
                                   state.has(ItemName.knuckles_hammer_gloves, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_cheetah,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.eggman_jet_engine, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_warthog,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.eggman_jet_engine, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_parrot,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.eggman_jet_engine, player) and
                                   state.has(ItemName.knuckles_air_necklace, player) and
                                   state.has(ItemName.knuckles_hammer_gloves, player) and
                                   (state.has(ItemName.sonic_bounce_bracelet, player) or
                                    state.has(ItemName.sonic_flame_ring, player))))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_condor,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.eggman_jet_engine, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_raccoon,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   (state.has(ItemName.eggman_jet_engine, player) or
                                    state.has(ItemName.eggman_large_cannon, player))))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.eggman_jet_engine, player)))

        elif world.options.logic_difficulty.value == 1:
            connect(multiworld, player, names, LocationName.metal_harbor_region, LocationName.animal_phoenix)

            connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_skunk)
            connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.sonic_light_shoes, player) and
                                   state.has(ItemName.sonic_flame_ring, player)))

            connect(multiworld, player, names, LocationName.weapons_bed_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.eggman_jet_engine, player)))

            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_gorilla)
            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_raccoon)
            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_halffish)

            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_otter,
                    lambda state: (state.has(ItemName.tails_booster, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_rabbit,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.knuckles_hammer_gloves, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_cheetah,
                    lambda state: (state.has(ItemName.tails_booster, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_warthog,
                    lambda state: (state.has(ItemName.tails_booster, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_parrot,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.knuckles_hammer_gloves, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_condor,
                    lambda state: (state.has(ItemName.tails_booster, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_raccoon,
                    lambda state: (state.has(ItemName.tails_booster, player)))
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.tails_booster, player)))

        if world.options.keysanity:
            connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_dragon,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))

            connect(multiworld, player, names, LocationName.mission_street_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.tails_bazooka, player)))

            connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog,
                    lambda state: (state.has(ItemName.sonic_light_shoes, player) and
                                   state.has(ItemName.sonic_flame_ring, player)))

            connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_raccoon,
                    lambda state: (state.has(ItemName.eggman_jet_engine, player)))

            if world.options.logic_difficulty.value == 0:
                connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.eggman_jet_engine, player) and
                                       state.has(ItemName.eggman_large_cannon, player)))

                connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.eggman_jet_engine, player) and
                                       state.has(ItemName.eggman_large_cannon, player)))
            if world.options.logic_difficulty.value == 1:
                connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.eggman_jet_engine, player)))

                connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.eggman_jet_engine, player)))

        else:
            connect(multiworld, player, names, LocationName.city_escape_region, LocationName.animal_unicorn)

            connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_dragon)

            connect(multiworld, player, names, LocationName.pumpkin_hill_region, LocationName.animal_halffish)

            connect(multiworld, player, names, LocationName.mission_street_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.tails_booster, player)))

            connect(multiworld, player, names, LocationName.death_chamber_region, LocationName.animal_skeleton_dog,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player) and
                                   state.has(ItemName.knuckles_hammer_gloves, player)))

            connect(multiworld, player, names, LocationName.eternal_engine_region, LocationName.animal_halffish,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.tails_bazooka, player)))

            connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_dragon)

            connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_skeleton_dog)

            connect(multiworld, player, names, LocationName.radical_highway_region, LocationName.animal_unicorn)

            connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_raccoon)
            connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_skeleton_dog)

            connect(multiworld, player, names, LocationName.security_hall_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.rouge_pick_nails, player)))

            connect(multiworld, player, names, LocationName.sky_rail_region, LocationName.animal_phoenix)

            if world.options.logic_difficulty.value == 0:
                connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.sonic_light_shoes, player) and
                                       state.has(ItemName.sonic_bounce_bracelet, player) and
                                       state.has(ItemName.sonic_mystic_melody, player)))

                connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.shadow_air_shoes, player)))

                connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.tails_booster, player) and
                                       state.has(ItemName.eggman_jet_engine, player) and
                                       state.has(ItemName.knuckles_air_necklace, player) and
                                       state.has(ItemName.knuckles_hammer_gloves, player)))
            elif world.options.logic_difficulty.value == 1:
                connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog)

                connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_dragon)

                connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.tails_booster, player) and
                                       state.has(ItemName.knuckles_hammer_gloves, player)))

    if world.options.black_market_slots.value > 0:
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.black_market_region)


def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id:
                location = SA2BLocation(player, location, loc_id, ret)
                ret.locations.append(location)

    return ret


def connect(multiworld: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = multiworld.get_region(source, player)
    target_region = multiworld.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
