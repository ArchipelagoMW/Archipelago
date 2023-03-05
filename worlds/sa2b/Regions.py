import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import SA2BItem
from .Locations import SA2BLocation, boss_gate_location_table, boss_gate_set
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


def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None)

    gate_0_region = create_region(world, player, active_locations, 'Gate 0', None)

    if world.number_of_level_gates[player].value >= 1:
        gate_1_boss_region = create_region(world, player, active_locations, 'Gate 1 Boss', [LocationName.gate_1_boss])
        gate_1_region = create_region(world, player, active_locations, 'Gate 1', None)
        world.regions += [gate_1_region, gate_1_boss_region]

    if world.number_of_level_gates[player].value >= 2:
        gate_2_boss_region = create_region(world, player, active_locations, 'Gate 2 Boss', [LocationName.gate_2_boss])
        gate_2_region = create_region(world, player, active_locations, 'Gate 2', None)
        world.regions += [gate_2_region, gate_2_boss_region]

    if world.number_of_level_gates[player].value >= 3:
        gate_3_boss_region = create_region(world, player, active_locations, 'Gate 3 Boss', [LocationName.gate_3_boss])
        gate_3_region = create_region(world, player, active_locations, 'Gate 3', None)
        world.regions += [gate_3_region, gate_3_boss_region]

    if world.number_of_level_gates[player].value >= 4:
        gate_4_boss_region = create_region(world, player, active_locations, 'Gate 4 Boss', [LocationName.gate_4_boss])
        gate_4_region = create_region(world, player, active_locations, 'Gate 4', None)
        world.regions += [gate_4_region, gate_4_boss_region]

    if world.number_of_level_gates[player].value >= 5:
        gate_5_boss_region = create_region(world, player, active_locations, 'Gate 5 Boss', [LocationName.gate_5_boss])
        gate_5_region = create_region(world, player, active_locations, 'Gate 5', None)
        world.regions += [gate_5_region, gate_5_boss_region]

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
        LocationName.city_escape_beetle,
        LocationName.city_escape_upgrade,
    ]
    city_escape_region = create_region(world, player, active_locations, LocationName.city_escape_region,
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
        LocationName.metal_harbor_beetle,
        LocationName.metal_harbor_upgrade,
    ]
    metal_harbor_region = create_region(world, player, active_locations, LocationName.metal_harbor_region,
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
        LocationName.green_forest_upgrade,
    ]
    green_forest_region = create_region(world, player, active_locations, LocationName.green_forest_region,
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
        LocationName.pyramid_cave_beetle,
        LocationName.pyramid_cave_upgrade,
    ]
    pyramid_cave_region = create_region(world, player, active_locations, LocationName.pyramid_cave_region,
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
        LocationName.crazy_gadget_beetle,
        LocationName.crazy_gadget_upgrade,
    ]
    crazy_gadget_region = create_region(world, player, active_locations, LocationName.crazy_gadget_region,
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
        LocationName.final_rush_beetle,
        LocationName.final_rush_upgrade,
    ]
    final_rush_region = create_region(world, player, active_locations, LocationName.final_rush_region,
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
        LocationName.prison_lane_beetle,
        LocationName.prison_lane_upgrade,
    ]
    prison_lane_region = create_region(world, player, active_locations, LocationName.prison_lane_region,
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
        LocationName.mission_street_beetle,
        LocationName.mission_street_upgrade,
    ]
    mission_street_region = create_region(world, player, active_locations, LocationName.mission_street_region,
                                          mission_street_region_locations)

    route_101_region_locations = [
        LocationName.route_101_1,
        LocationName.route_101_2,
        LocationName.route_101_3,
        LocationName.route_101_4,
        LocationName.route_101_5,
    ]
    route_101_region = create_region(world, player, active_locations, LocationName.route_101_region,
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
        LocationName.hidden_base_beetle,
        LocationName.hidden_base_upgrade,
    ]
    hidden_base_region = create_region(world, player, active_locations, LocationName.hidden_base_region,
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
        LocationName.eternal_engine_beetle,
        LocationName.eternal_engine_upgrade,
    ]
    eternal_engine_region = create_region(world, player, active_locations, LocationName.eternal_engine_region,
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
        LocationName.wild_canyon_beetle,
        LocationName.wild_canyon_upgrade,
    ]
    wild_canyon_region = create_region(world, player, active_locations, LocationName.wild_canyon_region,
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
        LocationName.pumpkin_hill_upgrade,
    ]
    pumpkin_hill_region = create_region(world, player, active_locations, LocationName.pumpkin_hill_region,
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
        LocationName.aquatic_mine_beetle,
        LocationName.aquatic_mine_upgrade,
    ]
    aquatic_mine_region = create_region(world, player, active_locations, LocationName.aquatic_mine_region,
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
        LocationName.death_chamber_beetle,
        LocationName.death_chamber_upgrade,
    ]
    death_chamber_region = create_region(world, player, active_locations, LocationName.death_chamber_region,
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
        LocationName.meteor_herd_beetle,
        LocationName.meteor_herd_upgrade,
    ]
    meteor_herd_region = create_region(world, player, active_locations, LocationName.meteor_herd_region,
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
        LocationName.radical_highway_beetle,
        LocationName.radical_highway_upgrade,
    ]
    radical_highway_region = create_region(world, player, active_locations, LocationName.radical_highway_region,
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
        LocationName.white_jungle_beetle,
        LocationName.white_jungle_upgrade,
    ]
    white_jungle_region = create_region(world, player, active_locations, LocationName.white_jungle_region,
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
        LocationName.sky_rail_upgrade,
    ]
    sky_rail_region = create_region(world, player, active_locations, LocationName.sky_rail_region,
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
        LocationName.final_chase_beetle,
        LocationName.final_chase_upgrade,
    ]
    final_chase_region = create_region(world, player, active_locations, LocationName.final_chase_region,
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
        LocationName.iron_gate_beetle,
        LocationName.iron_gate_upgrade,
    ]
    iron_gate_region = create_region(world, player, active_locations, LocationName.iron_gate_region,
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
        LocationName.sand_ocean_beetle,
        LocationName.sand_ocean_upgrade,
    ]
    sand_ocean_region = create_region(world, player, active_locations, LocationName.sand_ocean_region,
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
        LocationName.lost_colony_beetle,
        LocationName.lost_colony_upgrade,
    ]
    lost_colony_region = create_region(world, player, active_locations, LocationName.lost_colony_region,
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
        LocationName.weapons_bed_upgrade,
    ]
    weapons_bed_region = create_region(world, player, active_locations, LocationName.weapons_bed_region,
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
        LocationName.cosmic_wall_beetle,
        LocationName.cosmic_wall_upgrade,
    ]
    cosmic_wall_region = create_region(world, player, active_locations, LocationName.cosmic_wall_region,
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
        LocationName.dry_lagoon_beetle,
        LocationName.dry_lagoon_upgrade,
    ]
    dry_lagoon_region = create_region(world, player, active_locations, LocationName.dry_lagoon_region,
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
        LocationName.egg_quarters_beetle,
        LocationName.egg_quarters_upgrade,
    ]
    egg_quarters_region = create_region(world, player, active_locations, LocationName.egg_quarters_region,
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
        LocationName.security_hall_beetle,
        LocationName.security_hall_upgrade,
    ]
    security_hall_region = create_region(world, player, active_locations, LocationName.security_hall_region,
                                         security_hall_region_locations)

    route_280_region_locations = [
        LocationName.route_280_1,
        LocationName.route_280_2,
        LocationName.route_280_3,
        LocationName.route_280_4,
        LocationName.route_280_5,
    ]
    route_280_region = create_region(world, player, active_locations, LocationName.route_280_region,
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
        LocationName.mad_space_beetle,
        LocationName.mad_space_upgrade,
    ]
    mad_space_region = create_region(world, player, active_locations, LocationName.mad_space_region,
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
        LocationName.cannon_core_beetle,
    ]
    cannon_core_region = create_region(world, player, active_locations, LocationName.cannon_core_region,
                                       cannon_core_region_locations)

    chao_garden_beginner_region_locations = [
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

        LocationName.chao_beginner_karate,
    ]
    chao_garden_beginner_region = create_region(world, player, active_locations, LocationName.chao_garden_beginner_region,
                                                chao_garden_beginner_region_locations)

    chao_garden_intermediate_region_locations = [
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

        LocationName.chao_standard_karate,
    ]
    chao_garden_intermediate_region = create_region(world, player, active_locations, LocationName.chao_garden_intermediate_region,
                                                    chao_garden_intermediate_region_locations)

    chao_garden_expert_region_locations = [
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

        LocationName.chao_expert_karate,
        LocationName.chao_super_karate,
    ]
    chao_garden_expert_region = create_region(world, player, active_locations, LocationName.chao_garden_expert_region,
                                              chao_garden_expert_region_locations)

    if world.goal[player] == 0 or world.goal[player] == 2:
        biolizard_region_locations = [
            LocationName.finalhazard,
        ]
        biolizard_region = create_region(world, player, active_locations, LocationName.biolizard_region,
                                         biolizard_region_locations)
        world.regions += [biolizard_region]

    if world.goal[player] == 1 or world.goal[player] == 2:
        green_hill_region_locations = [
            LocationName.green_hill,
            LocationName.green_hill_chao_1,
        ]
        green_hill_region = create_region(world, player, active_locations, LocationName.green_hill_region,
                                          green_hill_region_locations)
        world.regions += [green_hill_region]


    # Set up the regions correctly.
    world.regions += [
        menu_region,
        gate_0_region,
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
        chao_garden_beginner_region,
        chao_garden_intermediate_region,
        chao_garden_expert_region,
    ]


def connect_regions(world, player, gates: typing.List[LevelGate], cannon_core_emblems, gate_bosses, first_cannons_core_mission: str, final_cannons_core_mission: str):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, 'Menu', LocationName.gate_0_region)
    connect(world, player, names, LocationName.gate_0_region, LocationName.cannon_core_region,
            lambda state: (state.has(ItemName.emblem, player, cannon_core_emblems)))

    if world.goal[player] == 0:
        required_mission_name = first_cannons_core_mission

        if world.required_cannons_core_missions[player].value == 1:
            required_mission_name = final_cannons_core_mission

        connect(world, player, names, LocationName.cannon_core_region, LocationName.biolizard_region,
                lambda state: (state.can_reach(required_mission_name, "Location", player)))
    elif world.goal[player] == 1 or world.goal[player] == 2:
        connect(world, player, names, 'Menu', LocationName.green_hill_region,
                lambda state: (state.has(ItemName.white_emerald, player) and
                               state.has(ItemName.red_emerald, player) and
                               state.has(ItemName.cyan_emerald, player) and
                               state.has(ItemName.purple_emerald, player) and
                               state.has(ItemName.green_emerald, player) and
                               state.has(ItemName.yellow_emerald, player) and
                               state.has(ItemName.blue_emerald, player)))
        if world.goal[player] == 2:
            connect(world, player, names, LocationName.green_hill_region, LocationName.biolizard_region)

    for i in range(len(gates[0].gate_levels)):
        connect(world, player, names, LocationName.gate_0_region, shuffleable_regions[gates[0].gate_levels[i]])

    gates_len = len(gates)
    if gates_len >= 2:
        connect(world, player, names, LocationName.gate_0_region, LocationName.gate_1_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[1].gate_emblem_count)))

        if gate_bosses[1] == all_gate_bosses_table[king_boom_boo]:
            connect(world, player, names, LocationName.gate_1_boss_region, LocationName.gate_1_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(world, player, names, LocationName.gate_1_boss_region, LocationName.gate_1_region)

        for i in range(len(gates[1].gate_levels)):
            connect(world, player, names, LocationName.gate_1_region, shuffleable_regions[gates[1].gate_levels[i]])

    if gates_len >= 3:
        connect(world, player, names, LocationName.gate_1_region, LocationName.gate_2_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[2].gate_emblem_count)))

        if gate_bosses[2] == all_gate_bosses_table[king_boom_boo]:
            connect(world, player, names, LocationName.gate_2_boss_region, LocationName.gate_2_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(world, player, names, LocationName.gate_2_boss_region, LocationName.gate_2_region)

        for i in range(len(gates[2].gate_levels)):
            connect(world, player, names, LocationName.gate_2_region, shuffleable_regions[gates[2].gate_levels[i]])

    if gates_len >= 4:
        connect(world, player, names, LocationName.gate_2_region, LocationName.gate_3_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[3].gate_emblem_count)))

        if gate_bosses[3] == all_gate_bosses_table[king_boom_boo]:
            connect(world, player, names, LocationName.gate_3_boss_region, LocationName.gate_3_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(world, player, names, LocationName.gate_3_boss_region, LocationName.gate_3_region)

        for i in range(len(gates[3].gate_levels)):
            connect(world, player, names, LocationName.gate_3_region, shuffleable_regions[gates[3].gate_levels[i]])

    if gates_len >= 5:
        connect(world, player, names, LocationName.gate_3_region, LocationName.gate_4_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[4].gate_emblem_count)))

        if gate_bosses[4] == all_gate_bosses_table[king_boom_boo]:
            connect(world, player, names, LocationName.gate_4_boss_region, LocationName.gate_4_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(world, player, names, LocationName.gate_4_boss_region, LocationName.gate_4_region)

        for i in range(len(gates[4].gate_levels)):
            connect(world, player, names, LocationName.gate_4_region, shuffleable_regions[gates[4].gate_levels[i]])

    if gates_len >= 6:
        connect(world, player, names, LocationName.gate_4_region, LocationName.gate_5_boss_region,
                lambda state: (state.has(ItemName.emblem, player, gates[5].gate_emblem_count)))

        if gate_bosses[5] == all_gate_bosses_table[king_boom_boo]:
            connect(world, player, names, LocationName.gate_5_boss_region, LocationName.gate_5_region,
                    lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))
        else:
            connect(world, player, names, LocationName.gate_5_boss_region, LocationName.gate_5_region)

        for i in range(len(gates[5].gate_levels)):
            connect(world, player, names, LocationName.gate_5_region, shuffleable_regions[gates[5].gate_levels[i]])

    if gates_len == 1:
        connect(world, player, names, LocationName.gate_0_region, LocationName.chao_garden_beginner_region)
        connect(world, player, names, LocationName.gate_0_region, LocationName.chao_garden_intermediate_region)
        connect(world, player, names, LocationName.gate_0_region, LocationName.chao_garden_expert_region)
    elif gates_len == 2:
        connect(world, player, names, LocationName.gate_0_region, LocationName.chao_garden_beginner_region)
        connect(world, player, names, LocationName.gate_0_region, LocationName.chao_garden_intermediate_region)
        connect(world, player, names, LocationName.gate_1_region, LocationName.chao_garden_expert_region)
    elif gates_len == 3:
        connect(world, player, names, LocationName.gate_0_region, LocationName.chao_garden_beginner_region)
        connect(world, player, names, LocationName.gate_1_region, LocationName.chao_garden_intermediate_region)
        connect(world, player, names, LocationName.gate_2_region, LocationName.chao_garden_expert_region)
    elif gates_len == 4:
        connect(world, player, names, LocationName.gate_0_region, LocationName.chao_garden_beginner_region)
        connect(world, player, names, LocationName.gate_1_region, LocationName.chao_garden_intermediate_region)
        connect(world, player, names, LocationName.gate_3_region, LocationName.chao_garden_expert_region)
    elif gates_len == 5:
        connect(world, player, names, LocationName.gate_1_region, LocationName.chao_garden_beginner_region)
        connect(world, player, names, LocationName.gate_2_region, LocationName.chao_garden_intermediate_region)
        connect(world, player, names, LocationName.gate_3_region, LocationName.chao_garden_expert_region)
    elif gates_len >= 6:
        connect(world, player, names, LocationName.gate_1_region, LocationName.chao_garden_beginner_region)
        connect(world, player, names, LocationName.gate_2_region, LocationName.chao_garden_intermediate_region)
        connect(world, player, names, LocationName.gate_4_region, LocationName.chao_garden_expert_region)


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, world)
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id:
                location = SA2BLocation(player, location, loc_id, ret)
                ret.locations.append(location)

    return ret


def connect(world: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

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
