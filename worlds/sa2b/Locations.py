import typing

from BaseClasses import Location
from .Names import LocationName


class SA2BLocation(Location):
    game: str = "Sonic Adventure 2: Battle"


first_mission_location_table = {
    LocationName.city_escape_1: 0xFF0000,
    LocationName.wild_canyon_1: 0xFF0001,
    LocationName.prison_lane_1: 0xFF0002,
    LocationName.metal_harbor_1: 0xFF0003,
    LocationName.green_forest_1: 0xFF0004,
    LocationName.pumpkin_hill_1: 0xFF0005,
    LocationName.mission_street_1: 0xFF0006,
    LocationName.aquatic_mine_1: 0xFF0007,
    LocationName.route_101_1: 0xFF0008,
    LocationName.hidden_base_1: 0xFF0009,
    LocationName.pyramid_cave_1: 0xFF000A,
    LocationName.death_chamber_1: 0xFF000B,
    LocationName.eternal_engine_1: 0xFF000C,
    LocationName.meteor_herd_1: 0xFF000D,
    LocationName.crazy_gadget_1: 0xFF000E,
    LocationName.final_rush_1: 0xFF000F,

    LocationName.iron_gate_1: 0xFF0010,
    LocationName.dry_lagoon_1: 0xFF0011,
    LocationName.sand_ocean_1: 0xFF0012,
    LocationName.radical_highway_1: 0xFF0013,
    LocationName.egg_quarters_1: 0xFF0014,
    LocationName.lost_colony_1: 0xFF0015,
    LocationName.weapons_bed_1: 0xFF0016,
    LocationName.security_hall_1: 0xFF0017,
    LocationName.white_jungle_1: 0xFF0018,
    LocationName.route_280_1: 0xFF0019,
    LocationName.sky_rail_1: 0xFF001A,
    LocationName.mad_space_1: 0xFF001B,
    LocationName.cosmic_wall_1: 0xFF001C,
    LocationName.final_chase_1: 0xFF001D,

    LocationName.cannon_core_1: 0xFF001E,
}

second_mission_location_table = {
    LocationName.city_escape_2: 0xFF0020,
    LocationName.wild_canyon_2: 0xFF0021,
    LocationName.prison_lane_2: 0xFF0022,
    LocationName.metal_harbor_2: 0xFF0023,
    LocationName.green_forest_2: 0xFF0024,
    LocationName.pumpkin_hill_2: 0xFF0025,
    LocationName.mission_street_2: 0xFF0026,
    LocationName.aquatic_mine_2: 0xFF0027,
    LocationName.route_101_2: 0xFF0028,
    LocationName.hidden_base_2: 0xFF0029,
    LocationName.pyramid_cave_2: 0xFF002A,
    LocationName.death_chamber_2: 0xFF002B,
    LocationName.eternal_engine_2: 0xFF002C,
    LocationName.meteor_herd_2: 0xFF002D,
    LocationName.crazy_gadget_2: 0xFF002E,
    LocationName.final_rush_2: 0xFF002F,

    LocationName.iron_gate_2: 0xFF0030,
    LocationName.dry_lagoon_2: 0xFF0031,
    LocationName.sand_ocean_2: 0xFF0032,
    LocationName.radical_highway_2: 0xFF0033,
    LocationName.egg_quarters_2: 0xFF0034,
    LocationName.lost_colony_2: 0xFF0035,
    LocationName.weapons_bed_2: 0xFF0036,
    LocationName.security_hall_2: 0xFF0037,
    LocationName.white_jungle_2: 0xFF0038,
    LocationName.route_280_2: 0xFF0039,
    LocationName.sky_rail_2: 0xFF003A,
    LocationName.mad_space_2: 0xFF003B,
    LocationName.cosmic_wall_2: 0xFF003C,
    LocationName.final_chase_2: 0xFF003D,

    LocationName.cannon_core_2: 0xFF003E,
}

third_mission_location_table = {
    LocationName.city_escape_3: 0xFF0040,
    LocationName.wild_canyon_3: 0xFF0041,
    LocationName.prison_lane_3: 0xFF0042,
    LocationName.metal_harbor_3: 0xFF0043,
    LocationName.green_forest_3: 0xFF0044,
    LocationName.pumpkin_hill_3: 0xFF0045,
    LocationName.mission_street_3: 0xFF0046,
    LocationName.aquatic_mine_3: 0xFF0047,
    LocationName.route_101_3: 0xFF0048,
    LocationName.hidden_base_3: 0xFF0049,
    LocationName.pyramid_cave_3: 0xFF004A,
    LocationName.death_chamber_3: 0xFF004B,
    LocationName.eternal_engine_3: 0xFF004C,
    LocationName.meteor_herd_3: 0xFF004D,
    LocationName.crazy_gadget_3: 0xFF004E,
    LocationName.final_rush_3: 0xFF004F,

    LocationName.iron_gate_3: 0xFF0050,
    LocationName.dry_lagoon_3: 0xFF0051,
    LocationName.sand_ocean_3: 0xFF0052,
    LocationName.radical_highway_3: 0xFF0053,
    LocationName.egg_quarters_3: 0xFF0054,
    LocationName.lost_colony_3: 0xFF0055,
    LocationName.weapons_bed_3: 0xFF0056,
    LocationName.security_hall_3: 0xFF0057,
    LocationName.white_jungle_3: 0xFF0058,
    LocationName.route_280_3: 0xFF0059,
    LocationName.sky_rail_3: 0xFF005A,
    LocationName.mad_space_3: 0xFF005B,
    LocationName.cosmic_wall_3: 0xFF005C,
    LocationName.final_chase_3: 0xFF005D,

    LocationName.cannon_core_3: 0xFF005E,
}

fourth_mission_location_table = {
    LocationName.city_escape_4: 0xFF0060,
    LocationName.wild_canyon_4: 0xFF0061,
    LocationName.prison_lane_4: 0xFF0062,
    LocationName.metal_harbor_4: 0xFF0063,
    LocationName.green_forest_4: 0xFF0064,
    LocationName.pumpkin_hill_4: 0xFF0065,
    LocationName.mission_street_4: 0xFF0066,
    LocationName.aquatic_mine_4: 0xFF0067,
    LocationName.route_101_4: 0xFF0068,
    LocationName.hidden_base_4: 0xFF0069,
    LocationName.pyramid_cave_4: 0xFF006A,
    LocationName.death_chamber_4: 0xFF006B,
    LocationName.eternal_engine_4: 0xFF006C,
    LocationName.meteor_herd_4: 0xFF006D,
    LocationName.crazy_gadget_4: 0xFF006E,
    LocationName.final_rush_4: 0xFF006F,

    LocationName.iron_gate_4: 0xFF0070,
    LocationName.dry_lagoon_4: 0xFF0071,
    LocationName.sand_ocean_4: 0xFF0072,
    LocationName.radical_highway_4: 0xFF0073,
    LocationName.egg_quarters_4: 0xFF0074,
    LocationName.lost_colony_4: 0xFF0075,
    LocationName.weapons_bed_4: 0xFF0076,
    LocationName.security_hall_4: 0xFF0077,
    LocationName.white_jungle_4: 0xFF0078,
    LocationName.route_280_4: 0xFF0079,
    LocationName.sky_rail_4: 0xFF007A,
    LocationName.mad_space_4: 0xFF007B,
    LocationName.cosmic_wall_4: 0xFF007C,
    LocationName.final_chase_4: 0xFF007D,

    LocationName.cannon_core_4: 0xFF007E,
}

fifth_mission_location_table = {
    LocationName.city_escape_5: 0xFF0080,
    LocationName.wild_canyon_5: 0xFF0081,
    LocationName.prison_lane_5: 0xFF0082,
    LocationName.metal_harbor_5: 0xFF0083,
    LocationName.green_forest_5: 0xFF0084,
    LocationName.pumpkin_hill_5: 0xFF0085,
    LocationName.mission_street_5: 0xFF0086,
    LocationName.aquatic_mine_5: 0xFF0087,
    LocationName.route_101_5: 0xFF0088,
    LocationName.hidden_base_5: 0xFF0089,
    LocationName.pyramid_cave_5: 0xFF008A,
    LocationName.death_chamber_5: 0xFF008B,
    LocationName.eternal_engine_5: 0xFF008C,
    LocationName.meteor_herd_5: 0xFF008D,
    LocationName.crazy_gadget_5: 0xFF008E,
    LocationName.final_rush_5: 0xFF008F,

    LocationName.iron_gate_5: 0xFF0090,
    LocationName.dry_lagoon_5: 0xFF0091,
    LocationName.sand_ocean_5: 0xFF0092,
    LocationName.radical_highway_5: 0xFF0093,
    LocationName.egg_quarters_5: 0xFF0094,
    LocationName.lost_colony_5: 0xFF0095,
    LocationName.weapons_bed_5: 0xFF0096,
    LocationName.security_hall_5: 0xFF0097,
    LocationName.white_jungle_5: 0xFF0098,
    LocationName.route_280_5: 0xFF0099,
    LocationName.sky_rail_5: 0xFF009A,
    LocationName.mad_space_5: 0xFF009B,
    LocationName.cosmic_wall_5: 0xFF009C,
    LocationName.final_chase_5: 0xFF009D,

    LocationName.cannon_core_5: 0xFF009E,
}

upgrade_location_table = {
    LocationName.city_escape_upgrade: 0xFF00A0,
    LocationName.wild_canyon_upgrade: 0xFF00A1,
    LocationName.prison_lane_upgrade: 0xFF00A2,
    LocationName.metal_harbor_upgrade: 0xFF00A3,
    LocationName.green_forest_upgrade: 0xFF00A4,
    LocationName.pumpkin_hill_upgrade: 0xFF00A5,
    LocationName.mission_street_upgrade: 0xFF00A6,
    LocationName.aquatic_mine_upgrade: 0xFF00A7,
    LocationName.hidden_base_upgrade: 0xFF00A9,
    LocationName.pyramid_cave_upgrade: 0xFF00AA,
    LocationName.death_chamber_upgrade: 0xFF00AB,
    LocationName.eternal_engine_upgrade: 0xFF00AC,
    LocationName.meteor_herd_upgrade: 0xFF00AD,
    LocationName.crazy_gadget_upgrade: 0xFF00AE,
    LocationName.final_rush_upgrade: 0xFF00AF,

    LocationName.iron_gate_upgrade: 0xFF00B0,
    LocationName.dry_lagoon_upgrade: 0xFF00B1,
    LocationName.sand_ocean_upgrade: 0xFF00B2,
    LocationName.radical_highway_upgrade: 0xFF00B3,
    LocationName.egg_quarters_upgrade: 0xFF00B4,
    LocationName.lost_colony_upgrade: 0xFF00B5,
    LocationName.weapons_bed_upgrade: 0xFF00B6,
    LocationName.security_hall_upgrade: 0xFF00B7,
    LocationName.white_jungle_upgrade: 0xFF00B8,
    LocationName.sky_rail_upgrade: 0xFF00BA,
    LocationName.mad_space_upgrade: 0xFF00BB,
    LocationName.cosmic_wall_upgrade: 0xFF00BC,
    LocationName.final_chase_upgrade: 0xFF00BD,
}

boss_gate_location_table = {
    LocationName.gate_1_boss: 0xFF0100,
    LocationName.gate_2_boss: 0xFF0101,
    LocationName.gate_3_boss: 0xFF0102,
    LocationName.gate_4_boss: 0xFF0103,
    LocationName.gate_5_boss: 0xFF0104,
}

chao_garden_beginner_location_table = {
    LocationName.chao_race_crab_pool_1: 0xFF0200,
    LocationName.chao_race_crab_pool_2: 0xFF0201,
    LocationName.chao_race_crab_pool_3: 0xFF0202,
    LocationName.chao_race_stump_valley_1: 0xFF0203,
    LocationName.chao_race_stump_valley_2: 0xFF0204,
    LocationName.chao_race_stump_valley_3: 0xFF0205,
    LocationName.chao_race_mushroom_forest_1: 0xFF0206,
    LocationName.chao_race_mushroom_forest_2: 0xFF0207,
    LocationName.chao_race_mushroom_forest_3: 0xFF0208,
    LocationName.chao_race_block_canyon_1: 0xFF0209,
    LocationName.chao_race_block_canyon_2: 0xFF020A,
    LocationName.chao_race_block_canyon_3: 0xFF020B,

    LocationName.chao_beginner_karate: 0xFF0300,
}

chao_garden_intermediate_location_table = {
    LocationName.chao_race_aquamarine_1: 0xFF020C,
    LocationName.chao_race_aquamarine_2: 0xFF020D,
    LocationName.chao_race_aquamarine_3: 0xFF020E,
    LocationName.chao_race_aquamarine_4: 0xFF020F,
    LocationName.chao_race_aquamarine_5: 0xFF0210,
    LocationName.chao_race_topaz_1: 0xFF0211,
    LocationName.chao_race_topaz_2: 0xFF0212,
    LocationName.chao_race_topaz_3: 0xFF0213,
    LocationName.chao_race_topaz_4: 0xFF0214,
    LocationName.chao_race_topaz_5: 0xFF0215,
    LocationName.chao_race_peridot_1: 0xFF0216,
    LocationName.chao_race_peridot_2: 0xFF0217,
    LocationName.chao_race_peridot_3: 0xFF0218,
    LocationName.chao_race_peridot_4: 0xFF0219,
    LocationName.chao_race_peridot_5: 0xFF021A,
    LocationName.chao_race_garnet_1: 0xFF021B,
    LocationName.chao_race_garnet_2: 0xFF021C,
    LocationName.chao_race_garnet_3: 0xFF021D,
    LocationName.chao_race_garnet_4: 0xFF021E,
    LocationName.chao_race_garnet_5: 0xFF021F,
    LocationName.chao_race_onyx_1: 0xFF0220,
    LocationName.chao_race_onyx_2: 0xFF0221,
    LocationName.chao_race_onyx_3: 0xFF0222,
    LocationName.chao_race_onyx_4: 0xFF0223,
    LocationName.chao_race_onyx_5: 0xFF0224,
    LocationName.chao_race_diamond_1: 0xFF0225,
    LocationName.chao_race_diamond_2: 0xFF0226,
    LocationName.chao_race_diamond_3: 0xFF0227,
    LocationName.chao_race_diamond_4: 0xFF0228,
    LocationName.chao_race_diamond_5: 0xFF0229,

    LocationName.chao_standard_karate: 0xFF0301,
}

chao_garden_expert_location_table = {
    LocationName.chao_race_challenge_1: 0xFF022A,
    LocationName.chao_race_challenge_2: 0xFF022B,
    LocationName.chao_race_challenge_3: 0xFF022C,
    LocationName.chao_race_challenge_4: 0xFF022D,
    LocationName.chao_race_challenge_5: 0xFF022E,
    LocationName.chao_race_challenge_6: 0xFF022F,
    LocationName.chao_race_challenge_7: 0xFF0230,
    LocationName.chao_race_challenge_8: 0xFF0231,
    LocationName.chao_race_challenge_9: 0xFF0232,
    LocationName.chao_race_challenge_10: 0xFF0233,
    LocationName.chao_race_challenge_11: 0xFF0234,
    LocationName.chao_race_challenge_12: 0xFF0235,

    LocationName.chao_race_hero_1: 0xFF0236,
    LocationName.chao_race_hero_2: 0xFF0237,
    LocationName.chao_race_hero_3: 0xFF0238,
    LocationName.chao_race_hero_4: 0xFF0239,

    LocationName.chao_race_dark_1: 0xFF023A,
    LocationName.chao_race_dark_2: 0xFF023B,
    LocationName.chao_race_dark_3: 0xFF023C,
    LocationName.chao_race_dark_4: 0xFF023D,

    LocationName.chao_expert_karate: 0xFF0302,
    LocationName.chao_super_karate: 0xFF0303,
}

other_location_table = {
    # LocationName.green_hill: 0xFF001F,
    LocationName.biolizard: 0xFF003F,
}

all_locations = {
    **first_mission_location_table,
    **second_mission_location_table,
    **third_mission_location_table,
    **fourth_mission_location_table,
    **fifth_mission_location_table,
    **upgrade_location_table,
    **boss_gate_location_table,
    **chao_garden_beginner_location_table,
    **chao_garden_intermediate_location_table,
    **chao_garden_expert_location_table,
    **other_location_table,
}

boss_gate_set = [
    LocationName.gate_1_boss,
    LocationName.gate_2_boss,
    LocationName.gate_3_boss,
    LocationName.gate_4_boss,
    LocationName.gate_5_boss,
]

chao_karate_set = [
    LocationName.chao_beginner_karate,
    LocationName.chao_standard_karate,
    LocationName.chao_expert_karate,
    LocationName.chao_super_karate,
]

chao_race_prize_set = [
    LocationName.chao_race_crab_pool_3,
    LocationName.chao_race_stump_valley_3,
    LocationName.chao_race_mushroom_forest_3,
    LocationName.chao_race_block_canyon_3,

    LocationName.chao_race_aquamarine_5,
    LocationName.chao_race_topaz_5,
    LocationName.chao_race_peridot_5,
    LocationName.chao_race_garnet_5,
    LocationName.chao_race_onyx_5,
    LocationName.chao_race_diamond_5,

    LocationName.chao_race_challenge_4,
    LocationName.chao_race_challenge_8,
    LocationName.chao_race_challenge_12,

    LocationName.chao_race_hero_2,
    LocationName.chao_race_hero_4,

    LocationName.chao_race_dark_2,
    LocationName.chao_race_dark_4,
]


def setup_locations(world, player: int):
    location_table = {}
    chao_location_table = {}
    location_table.update({**first_mission_location_table})

    if world.include_missions[player].value >= 2:
        location_table.update({**second_mission_location_table})

    if world.include_missions[player].value >= 3:
        location_table.update({**third_mission_location_table})

    if world.include_missions[player].value >= 4:
        location_table.update({**fourth_mission_location_table})

    if world.include_missions[player].value >= 5:
        location_table.update({**fifth_mission_location_table})

    location_table.update({**upgrade_location_table})

    location_table.update({**other_location_table})

    if world.chao_garden_difficulty[player].value >= 1:
        chao_location_table.update({**chao_garden_beginner_location_table})
    if world.chao_garden_difficulty[player].value >= 2:
        chao_location_table.update({**chao_garden_intermediate_location_table})
    if world.chao_garden_difficulty[player].value >= 3:
        chao_location_table.update({**chao_garden_expert_location_table})

    for key, value in chao_location_table.items():
        if key in chao_karate_set:
            if world.include_chao_karate[player]:
                location_table[key] = value
        elif key not in chao_race_prize_set:
            if world.chao_race_checks[player] == "all":
                location_table[key] = value
        else:
            location_table[key] = value

    for x in range(len(boss_gate_set)):
        if x < world.number_of_level_gates[player].value:
            location_table[boss_gate_set[x]] = boss_gate_location_table[boss_gate_set[x]]

    return location_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
