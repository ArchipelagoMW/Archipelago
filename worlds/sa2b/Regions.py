import typing
import math

from BaseClasses import MultiWorld, Region, Entrance, ItemClassification
from worlds.AutoWorld import World
from .Items import SA2BItem, minigame_trap_table
from .Locations import *
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

    city_escape_region = create_region(multiworld, player, active_locations, LocationName.city_escape_region,
                                       city_escape_region_locations)

    metal_harbor_region = create_region(multiworld, player, active_locations, LocationName.metal_harbor_region,
                                        metal_harbor_region_locations)

    green_forest_region = create_region(multiworld, player, active_locations, LocationName.green_forest_region,
                                        green_forest_region_locations)

    pyramid_cave_region = create_region(multiworld, player, active_locations, LocationName.pyramid_cave_region,
                                        pyramid_cave_region_locations)

    crazy_gadget_region = create_region(multiworld, player, active_locations, LocationName.crazy_gadget_region,
                                        crazy_gadget_region_locations)

    final_rush_region = create_region(multiworld, player, active_locations, LocationName.final_rush_region,
                                      final_rush_region_locations)

    prison_lane_region = create_region(multiworld, player, active_locations, LocationName.prison_lane_region,
                                       prison_lane_region_locations)

    mission_street_region = create_region(multiworld, player, active_locations, LocationName.mission_street_region,
                                          mission_street_region_locations)

    route_101_region = create_region(multiworld, player, active_locations, LocationName.route_101_region,
                                     route_101_region_locations)

    hidden_base_region = create_region(multiworld, player, active_locations, LocationName.hidden_base_region,
                                       hidden_base_region_locations)

    eternal_engine_region = create_region(multiworld, player, active_locations, LocationName.eternal_engine_region,
                                          eternal_engine_region_locations)

    wild_canyon_region = create_region(multiworld, player, active_locations, LocationName.wild_canyon_region,
                                       wild_canyon_region_locations)

    pumpkin_hill_region = create_region(multiworld, player, active_locations, LocationName.pumpkin_hill_region,
                                        pumpkin_hill_region_locations)

    aquatic_mine_region = create_region(multiworld, player, active_locations, LocationName.aquatic_mine_region,
                                        aquatic_mine_region_locations)

    death_chamber_region = create_region(multiworld, player, active_locations, LocationName.death_chamber_region,
                                         death_chamber_region_locations)

    meteor_herd_region = create_region(multiworld, player, active_locations, LocationName.meteor_herd_region,
                                       meteor_herd_region_locations)

    radical_highway_region = create_region(multiworld, player, active_locations, LocationName.radical_highway_region,
                                           radical_highway_region_locations)

    white_jungle_region = create_region(multiworld, player, active_locations, LocationName.white_jungle_region,
                                        white_jungle_region_locations)

    sky_rail_region = create_region(multiworld, player, active_locations, LocationName.sky_rail_region,
                                    sky_rail_region_locations)

    final_chase_region = create_region(multiworld, player, active_locations, LocationName.final_chase_region,
                                       final_chase_region_locations)

    iron_gate_region = create_region(multiworld, player, active_locations, LocationName.iron_gate_region,
                                     iron_gate_region_locations)

    sand_ocean_region = create_region(multiworld, player, active_locations, LocationName.sand_ocean_region,
                                      sand_ocean_region_locations)

    lost_colony_region = create_region(multiworld, player, active_locations, LocationName.lost_colony_region,
                                       lost_colony_region_locations)

    weapons_bed_region = create_region(multiworld, player, active_locations, LocationName.weapons_bed_region,
                                       weapons_bed_region_locations)

    cosmic_wall_region = create_region(multiworld, player, active_locations, LocationName.cosmic_wall_region,
                                       cosmic_wall_region_locations)

    dry_lagoon_region = create_region(multiworld, player, active_locations, LocationName.dry_lagoon_region,
                                      dry_lagoon_region_locations)

    egg_quarters_region = create_region(multiworld, player, active_locations, LocationName.egg_quarters_region,
                                        egg_quarters_region_locations)

    security_hall_region = create_region(multiworld, player, active_locations, LocationName.security_hall_region,
                                         security_hall_region_locations)

    route_280_region = create_region(multiworld, player, active_locations, LocationName.route_280_region,
                                     route_280_region_locations)

    mad_space_region = create_region(multiworld, player, active_locations, LocationName.mad_space_region,
                                     mad_space_region_locations)

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
    elif world.options.goal in [0, 2, 4, 5, 6, 8]:
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
            LocationName.green_hill_itembox_1, 
            LocationName.green_hill_itembox_2, 
            LocationName.green_hill_itembox_3, 
            LocationName.green_hill_itembox_4, 
            LocationName.green_hill_itembox_5, 
            LocationName.green_hill_itembox_6, 
            LocationName.green_hill_itembox_7, 
            LocationName.green_hill_itembox_8, 
            LocationName.green_hill_itembox_9, 
            LocationName.green_hill_itembox_10,
            LocationName.green_hill_itembox_11,
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
    elif world.options.goal == 8:
        trap_item_mapping = { minigame: world.options.minigame_madness_requirement.value for minigame in minigame_trap_table.keys() }
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.biolizard_region,
                lambda state: (state.has_all_counts(trap_item_mapping, player)))

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

        elif world.options.logic_difficulty.value == 2:
            connect(multiworld, player, names, LocationName.metal_harbor_region, LocationName.animal_phoenix)

            connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_skunk)
            connect(multiworld, player, names, LocationName.crazy_gadget_region, LocationName.animal_phoenix)

            connect(multiworld, player, names, LocationName.weapons_bed_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.eggman_jet_engine, player)))

            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_gorilla)
            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_raccoon)
            connect(multiworld, player, names, LocationName.mad_space_region, LocationName.animal_halffish)

            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_otter)
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_rabbit)
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_cheetah)
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_warthog)
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_parrot)
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_condor)
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_raccoon)
            connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_phoenix)

        if world.options.keysanity:
            connect(multiworld, player, names, LocationName.mission_street_region, LocationName.animal_phoenix,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.tails_bazooka, player)))

            connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_raccoon,
                    lambda state: (state.has(ItemName.eggman_jet_engine, player)))

            if world.options.logic_difficulty.value == 0:
                connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))

                connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.sonic_bounce_bracelet, player) and
                                       state.has(ItemName.sonic_flame_ring, player)))

                connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.eggman_jet_engine, player) and
                                       state.has(ItemName.eggman_large_cannon, player)))

                connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.eggman_jet_engine, player) and
                                       state.has(ItemName.eggman_large_cannon, player)))
            if world.options.logic_difficulty.value == 1:
                connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.knuckles_shovel_claws, player)))

                connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.sonic_flame_ring, player)))

                connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.eggman_jet_engine, player)))

                connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.eggman_jet_engine, player)))
            if world.options.logic_difficulty.value == 2:
                connect(multiworld, player, names, LocationName.wild_canyon_region, LocationName.animal_dragon)

                connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.sonic_flame_ring, player)))

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

            connect(multiworld, player, names, LocationName.eternal_engine_region, LocationName.animal_halffish,
                    lambda state: (state.has(ItemName.tails_booster, player) and
                                   state.has(ItemName.tails_bazooka, player)))

            connect(multiworld, player, names, LocationName.iron_gate_region, LocationName.animal_dragon)

            connect(multiworld, player, names, LocationName.sand_ocean_region, LocationName.animal_skeleton_dog)

            connect(multiworld, player, names, LocationName.radical_highway_region, LocationName.animal_unicorn)

            connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_raccoon)
            connect(multiworld, player, names, LocationName.lost_colony_region, LocationName.animal_skeleton_dog)

            connect(multiworld, player, names, LocationName.sky_rail_region, LocationName.animal_phoenix)

            if world.options.logic_difficulty.value == 0:
                connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.sonic_light_shoes, player) and
                                       state.has(ItemName.sonic_bounce_bracelet, player) and
                                       state.has(ItemName.sonic_mystic_melody, player)))

                connect(multiworld, player, names, LocationName.death_chamber_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.knuckles_shovel_claws, player) and
                                       state.has(ItemName.knuckles_hammer_gloves, player)))

                connect(multiworld, player, names, LocationName.security_hall_region, LocationName.animal_phoenix,
                        lambda state: (state.has(ItemName.rouge_pick_nails, player)))

                connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.shadow_air_shoes, player)))

                connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.tails_booster, player) and
                                       state.has(ItemName.eggman_jet_engine, player) and
                                       state.has(ItemName.knuckles_air_necklace, player) and
                                       state.has(ItemName.knuckles_hammer_gloves, player)))
            elif world.options.logic_difficulty.value == 1:
                connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog)

                connect(multiworld, player, names, LocationName.death_chamber_region, LocationName.animal_skeleton_dog,
                        lambda state: (state.has(ItemName.knuckles_shovel_claws, player) and
                                       state.has(ItemName.knuckles_hammer_gloves, player)))

                connect(multiworld, player, names, LocationName.security_hall_region, LocationName.animal_phoenix,
                        lambda state: (state.has(ItemName.rouge_pick_nails, player)))

                connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_dragon)

                connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_dragon,
                        lambda state: (state.has(ItemName.tails_booster, player) and
                                       state.has(ItemName.knuckles_hammer_gloves, player)))
            elif world.options.logic_difficulty.value == 2:
                connect(multiworld, player, names, LocationName.pyramid_cave_region, LocationName.animal_skeleton_dog)

                connect(multiworld, player, names, LocationName.death_chamber_region, LocationName.animal_skeleton_dog)

                connect(multiworld, player, names, LocationName.security_hall_region, LocationName.animal_phoenix)

                connect(multiworld, player, names, LocationName.white_jungle_region, LocationName.animal_dragon)

                connect(multiworld, player, names, LocationName.cannon_core_region, LocationName.animal_dragon)

    if world.options.black_market_slots.value > 0:
        connect(multiworld, player, names, LocationName.gate_0_region, LocationName.black_market_region)


def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id != 0:
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
