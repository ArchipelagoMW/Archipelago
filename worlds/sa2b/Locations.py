import typing

from BaseClasses import Location, MultiWorld
from .Names import LocationName
from .Missions import stage_name_prefixes, mission_orders


class SA2BLocation(Location):
    game: str = "Sonic Adventure 2: Battle"


mission_location_table = {
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

chao_key_location_table = {
    LocationName.city_escape_chao_1: 0xFF0400,
    LocationName.wild_canyon_chao_1: 0xFF0401,
    LocationName.prison_lane_chao_1: 0xFF0402,
    LocationName.metal_harbor_chao_1: 0xFF0403,
    LocationName.green_forest_chao_1: 0xFF0404,
    LocationName.pumpkin_hill_chao_1: 0xFF0405,
    LocationName.mission_street_chao_1: 0xFF0406,
    LocationName.aquatic_mine_chao_1: 0xFF0407,
    LocationName.hidden_base_chao_1: 0xFF0409,
    LocationName.pyramid_cave_chao_1: 0xFF040A,
    LocationName.death_chamber_chao_1: 0xFF040B,
    LocationName.eternal_engine_chao_1: 0xFF040C,
    LocationName.meteor_herd_chao_1: 0xFF040D,
    LocationName.crazy_gadget_chao_1: 0xFF040E,
    LocationName.final_rush_chao_1: 0xFF040F,

    LocationName.iron_gate_chao_1: 0xFF0410,
    LocationName.dry_lagoon_chao_1: 0xFF0411,
    LocationName.sand_ocean_chao_1: 0xFF0412,
    LocationName.radical_highway_chao_1: 0xFF0413,
    LocationName.egg_quarters_chao_1: 0xFF0414,
    LocationName.lost_colony_chao_1: 0xFF0415,
    LocationName.weapons_bed_chao_1: 0xFF0416,
    LocationName.security_hall_chao_1: 0xFF0417,
    LocationName.white_jungle_chao_1: 0xFF0418,
    LocationName.sky_rail_chao_1: 0xFF041A,
    LocationName.mad_space_chao_1: 0xFF041B,
    LocationName.cosmic_wall_chao_1: 0xFF041C,
    LocationName.final_chase_chao_1: 0xFF041D,

    LocationName.cannon_core_chao_1: 0xFF041E,

    LocationName.city_escape_chao_2: 0xFF0420,
    LocationName.wild_canyon_chao_2: 0xFF0421,
    LocationName.prison_lane_chao_2: 0xFF0422,
    LocationName.metal_harbor_chao_2: 0xFF0423,
    LocationName.green_forest_chao_2: 0xFF0424,
    LocationName.pumpkin_hill_chao_2: 0xFF0425,
    LocationName.mission_street_chao_2: 0xFF0426,
    LocationName.aquatic_mine_chao_2: 0xFF0427,
    LocationName.hidden_base_chao_2: 0xFF0429,
    LocationName.pyramid_cave_chao_2: 0xFF042A,
    LocationName.death_chamber_chao_2: 0xFF042B,
    LocationName.eternal_engine_chao_2: 0xFF042C,
    LocationName.meteor_herd_chao_2: 0xFF042D,
    LocationName.crazy_gadget_chao_2: 0xFF042E,
    LocationName.final_rush_chao_2: 0xFF042F,

    LocationName.iron_gate_chao_2: 0xFF0430,
    LocationName.dry_lagoon_chao_2: 0xFF0431,
    LocationName.sand_ocean_chao_2: 0xFF0432,
    LocationName.radical_highway_chao_2: 0xFF0433,
    LocationName.egg_quarters_chao_2: 0xFF0434,
    LocationName.lost_colony_chao_2: 0xFF0435,
    LocationName.weapons_bed_chao_2: 0xFF0436,
    LocationName.security_hall_chao_2: 0xFF0437,
    LocationName.white_jungle_chao_2: 0xFF0438,
    LocationName.sky_rail_chao_2: 0xFF043A,
    LocationName.mad_space_chao_2: 0xFF043B,
    LocationName.cosmic_wall_chao_2: 0xFF043C,
    LocationName.final_chase_chao_2: 0xFF043D,

    LocationName.cannon_core_chao_2: 0xFF043E,

    LocationName.city_escape_chao_3: 0xFF0440,
    LocationName.wild_canyon_chao_3: 0xFF0441,
    LocationName.prison_lane_chao_3: 0xFF0442,
    LocationName.metal_harbor_chao_3: 0xFF0443,
    LocationName.green_forest_chao_3: 0xFF0444,
    LocationName.pumpkin_hill_chao_3: 0xFF0445,
    LocationName.mission_street_chao_3: 0xFF0446,
    LocationName.aquatic_mine_chao_3: 0xFF0447,
    LocationName.pyramid_cave_chao_3: 0xFF044A,
    LocationName.death_chamber_chao_3: 0xFF044B,
    LocationName.eternal_engine_chao_3: 0xFF044C,
    LocationName.meteor_herd_chao_3: 0xFF044D,
    LocationName.crazy_gadget_chao_3: 0xFF044E,
    LocationName.final_rush_chao_3: 0xFF044F,

    LocationName.iron_gate_chao_3: 0xFF0450,
    LocationName.dry_lagoon_chao_3: 0xFF0451,
    LocationName.sand_ocean_chao_3: 0xFF0452,
    LocationName.radical_highway_chao_3: 0xFF0453,
    LocationName.egg_quarters_chao_3: 0xFF0454,
    LocationName.lost_colony_chao_3: 0xFF0455,
    LocationName.weapons_bed_chao_3: 0xFF0456,
    LocationName.security_hall_chao_3: 0xFF0457,
    LocationName.white_jungle_chao_3: 0xFF0458,
    LocationName.sky_rail_chao_3: 0xFF045A,
    LocationName.mad_space_chao_3: 0xFF045B,
    LocationName.cosmic_wall_chao_3: 0xFF045C,
    LocationName.final_chase_chao_3: 0xFF045D,

    LocationName.cannon_core_chao_3: 0xFF045E,
}

pipe_location_table = {
    LocationName.city_escape_pipe_1: 0xFF0500,
    LocationName.wild_canyon_pipe_1: 0xFF0501,
    LocationName.prison_lane_pipe_1: 0xFF0502,
    LocationName.metal_harbor_pipe_1: 0xFF0503,
    LocationName.green_forest_pipe_1: 0xFF0504,
    LocationName.pumpkin_hill_pipe_1: 0xFF0505,
    LocationName.mission_street_pipe_1: 0xFF0506,
    LocationName.aquatic_mine_pipe_1: 0xFF0507,
    LocationName.hidden_base_pipe_1: 0xFF0509,
    LocationName.pyramid_cave_pipe_1: 0xFF050A,
    LocationName.death_chamber_pipe_1: 0xFF050B,
    LocationName.eternal_engine_pipe_1: 0xFF050C,
    LocationName.meteor_herd_pipe_1: 0xFF050D,
    LocationName.crazy_gadget_pipe_1: 0xFF050E,
    LocationName.final_rush_pipe_1: 0xFF050F,

    LocationName.iron_gate_pipe_1: 0xFF0510,
    LocationName.dry_lagoon_pipe_1: 0xFF0511,
    LocationName.sand_ocean_pipe_1: 0xFF0512,
    LocationName.radical_highway_pipe_1: 0xFF0513,
    LocationName.egg_quarters_pipe_1: 0xFF0514,
    LocationName.lost_colony_pipe_1: 0xFF0515,
    LocationName.weapons_bed_pipe_1: 0xFF0516,
    LocationName.security_hall_pipe_1: 0xFF0517,
    LocationName.white_jungle_pipe_1: 0xFF0518,
    LocationName.sky_rail_pipe_1: 0xFF051A,
    LocationName.mad_space_pipe_1: 0xFF051B,
    LocationName.cosmic_wall_pipe_1: 0xFF051C,
    LocationName.final_chase_pipe_1: 0xFF051D,

    LocationName.cannon_core_pipe_1: 0xFF051E,

    LocationName.city_escape_pipe_2: 0xFF0520,
    LocationName.wild_canyon_pipe_2: 0xFF0521,
    LocationName.prison_lane_pipe_2: 0xFF0522,
    LocationName.green_forest_pipe_2: 0xFF0524,
    LocationName.mission_street_pipe_2: 0xFF0526,
    LocationName.aquatic_mine_pipe_2: 0xFF0527,
    LocationName.hidden_base_pipe_2: 0xFF0529,
    LocationName.pyramid_cave_pipe_2: 0xFF052A,
    LocationName.death_chamber_pipe_2: 0xFF052B,
    LocationName.eternal_engine_pipe_2: 0xFF052C,
    LocationName.meteor_herd_pipe_2: 0xFF052D,
    LocationName.crazy_gadget_pipe_2: 0xFF052E,
    LocationName.final_rush_pipe_2: 0xFF052F,

    LocationName.iron_gate_pipe_2: 0xFF0530,
    LocationName.sand_ocean_pipe_2: 0xFF0532,
    LocationName.radical_highway_pipe_2: 0xFF0533,
    LocationName.egg_quarters_pipe_2: 0xFF0534,
    LocationName.lost_colony_pipe_2: 0xFF0535,
    LocationName.weapons_bed_pipe_2: 0xFF0536,
    LocationName.white_jungle_pipe_2: 0xFF0538,
    LocationName.sky_rail_pipe_2: 0xFF053A,
    LocationName.mad_space_pipe_2: 0xFF053B,
    LocationName.cosmic_wall_pipe_2: 0xFF053C,
    LocationName.final_chase_pipe_2: 0xFF053D,

    LocationName.cannon_core_pipe_2: 0xFF053E,

    LocationName.city_escape_pipe_3: 0xFF0540,
    LocationName.wild_canyon_pipe_3: 0xFF0541,
    LocationName.prison_lane_pipe_3: 0xFF0542,
    LocationName.mission_street_pipe_3: 0xFF0546,
    LocationName.aquatic_mine_pipe_3: 0xFF0547,
    LocationName.hidden_base_pipe_3: 0xFF0549,
    LocationName.pyramid_cave_pipe_3: 0xFF054A,
    LocationName.death_chamber_pipe_3: 0xFF054B,
    LocationName.eternal_engine_pipe_3: 0xFF054C,
    LocationName.meteor_herd_pipe_3: 0xFF054D,
    LocationName.crazy_gadget_pipe_3: 0xFF054E,

    LocationName.iron_gate_pipe_3: 0xFF0550,
    LocationName.sand_ocean_pipe_3: 0xFF0552,
    LocationName.radical_highway_pipe_3: 0xFF0553,
    LocationName.weapons_bed_pipe_3: 0xFF0556,
    LocationName.white_jungle_pipe_3: 0xFF0558,
    LocationName.sky_rail_pipe_3: 0xFF055A,
    LocationName.mad_space_pipe_3: 0xFF055B,
    LocationName.cosmic_wall_pipe_3: 0xFF055C,
    LocationName.final_chase_pipe_3: 0xFF055D,

    LocationName.cannon_core_pipe_3: 0xFF055E,

    LocationName.city_escape_pipe_4: 0xFF0560,
    LocationName.hidden_base_pipe_4: 0xFF0569,
    LocationName.pyramid_cave_pipe_4: 0xFF056A,
    LocationName.eternal_engine_pipe_4: 0xFF056C,
    LocationName.crazy_gadget_pipe_4: 0xFF056E,

    LocationName.iron_gate_pipe_4: 0xFF0570,
    LocationName.sand_ocean_pipe_4: 0xFF0572,
    LocationName.weapons_bed_pipe_4: 0xFF0576,
    LocationName.white_jungle_pipe_4: 0xFF0578,
    LocationName.sky_rail_pipe_4: 0xFF057A,
    LocationName.mad_space_pipe_4: 0xFF057B,
    LocationName.cosmic_wall_pipe_4: 0xFF057C,

    LocationName.cannon_core_pipe_4: 0xFF057E,

    LocationName.hidden_base_pipe_5: 0xFF0589,
    LocationName.eternal_engine_pipe_5: 0xFF058C,

    LocationName.iron_gate_pipe_5: 0xFF0590,
    LocationName.sand_ocean_pipe_5: 0xFF0592,
    LocationName.weapons_bed_pipe_5: 0xFF0596,
    LocationName.sky_rail_pipe_5: 0xFF059A,
    LocationName.cosmic_wall_pipe_5: 0xFF059C,

    LocationName.cannon_core_pipe_5: 0xFF059E,

    LocationName.sky_rail_pipe_6: 0xFF05BA,
}

hidden_whistle_location_table = {
    LocationName.city_escape_hidden_1: 0xFF0700,
    LocationName.prison_lane_hidden_1: 0xFF0702,
    LocationName.green_forest_hidden_1: 0xFF0704,
    LocationName.pumpkin_hill_hidden_1: 0xFF0705,
    LocationName.mission_street_hidden_1: 0xFF0706,
    LocationName.death_chamber_hidden_1: 0xFF070B,
    LocationName.crazy_gadget_hidden_1: 0xFF070E,

    LocationName.dry_lagoon_hidden_1: 0xFF0711,
    LocationName.radical_highway_hidden_1: 0xFF0713,
    LocationName.egg_quarters_hidden_1: 0xFF0714,
    LocationName.lost_colony_hidden_1: 0xFF0715,
    LocationName.security_hall_hidden_1: 0xFF0717,
    LocationName.white_jungle_hidden_1: 0xFF0718,

    LocationName.cannon_core_hidden_1: 0xFF071E,

    LocationName.city_escape_hidden_2: 0xFF0720,
    LocationName.prison_lane_hidden_2: 0xFF0722,
    LocationName.green_forest_hidden_2: 0xFF0724,
    LocationName.mission_street_hidden_2: 0xFF0726,
    LocationName.death_chamber_hidden_2: 0xFF072B,

    LocationName.radical_highway_hidden_2: 0xFF0733,
    LocationName.egg_quarters_hidden_2: 0xFF0734,
    LocationName.white_jungle_hidden_2: 0xFF0738,

    LocationName.city_escape_hidden_3: 0xFF0740,
    LocationName.prison_lane_hidden_3: 0xFF0742,
    LocationName.green_forest_hidden_3: 0xFF0744,
    LocationName.mission_street_hidden_3: 0xFF0746,

    LocationName.radical_highway_hidden_3: 0xFF0753,
    LocationName.white_jungle_hidden_3: 0xFF0758,

    LocationName.city_escape_hidden_4: 0xFF0760,
    LocationName.green_forest_hidden_4: 0xFF0764,
    LocationName.mission_street_hidden_4: 0xFF0766,

    LocationName.city_escape_hidden_5: 0xFF0780,
}

beetle_location_table = {
    LocationName.city_escape_beetle: 0xFF0600,
    LocationName.wild_canyon_beetle: 0xFF0601,
    LocationName.prison_lane_beetle: 0xFF0602,
    LocationName.metal_harbor_beetle: 0xFF0603,
    LocationName.green_forest_beetle: 0xFF0604,
    LocationName.mission_street_beetle: 0xFF0606,
    LocationName.aquatic_mine_beetle: 0xFF0607,
    LocationName.hidden_base_beetle: 0xFF0609,
    LocationName.pyramid_cave_beetle: 0xFF060A,
    LocationName.death_chamber_beetle: 0xFF060B,
    LocationName.eternal_engine_beetle: 0xFF060C,
    LocationName.meteor_herd_beetle: 0xFF060D,
    LocationName.crazy_gadget_beetle: 0xFF060E,
    LocationName.final_rush_beetle: 0xFF060F,

    LocationName.iron_gate_beetle: 0xFF0610,
    LocationName.dry_lagoon_beetle: 0xFF0611,
    LocationName.sand_ocean_beetle: 0xFF0612,
    LocationName.radical_highway_beetle: 0xFF0613,
    LocationName.egg_quarters_beetle: 0xFF0614,
    LocationName.lost_colony_beetle: 0xFF0615,
    LocationName.security_hall_beetle: 0xFF0617,
    LocationName.white_jungle_beetle: 0xFF0618,
    LocationName.sky_rail_beetle: 0xFF061A,
    LocationName.mad_space_beetle: 0xFF061B,
    LocationName.cosmic_wall_beetle: 0xFF061C,
    LocationName.final_chase_beetle: 0xFF061D,

    LocationName.cannon_core_beetle: 0xFF061E,
}

omochao_location_table = {
    LocationName.city_escape_omo_1: 0xFF0800,
    LocationName.wild_canyon_omo_1: 0xFF0801,
    LocationName.prison_lane_omo_1: 0xFF0802,
    LocationName.metal_harbor_omo_1: 0xFF0803,
    LocationName.pumpkin_hill_omo_1: 0xFF0805,
    LocationName.mission_street_omo_1: 0xFF0806,
    LocationName.aquatic_mine_omo_1: 0xFF0807,
    LocationName.hidden_base_omo_1: 0xFF0809,
    LocationName.pyramid_cave_omo_1: 0xFF080A,
    LocationName.death_chamber_omo_1: 0xFF080B,
    LocationName.eternal_engine_omo_1: 0xFF080C,
    LocationName.meteor_herd_omo_1: 0xFF080D,
    LocationName.crazy_gadget_omo_1: 0xFF080E,
    LocationName.final_rush_omo_1: 0xFF080F,

    LocationName.iron_gate_omo_1: 0xFF0810,
    LocationName.dry_lagoon_omo_1: 0xFF0811,
    LocationName.sand_ocean_omo_1: 0xFF0812,
    LocationName.radical_highway_omo_1: 0xFF0813,
    LocationName.egg_quarters_omo_1: 0xFF0814,
    LocationName.lost_colony_omo_1: 0xFF0815,
    LocationName.weapons_bed_omo_1: 0xFF0816,
    LocationName.security_hall_omo_1: 0xFF0817,
    LocationName.white_jungle_omo_1: 0xFF0818,
    LocationName.mad_space_omo_1: 0xFF081B,
    LocationName.cosmic_wall_omo_1: 0xFF081C,
    LocationName.final_chase_omo_1: 0xFF081D,

    LocationName.cannon_core_omo_1: 0xFF081E,

    LocationName.city_escape_omo_2: 0xFF0820,
    LocationName.wild_canyon_omo_2: 0xFF0821,
    LocationName.prison_lane_omo_2: 0xFF0822,
    LocationName.metal_harbor_omo_2: 0xFF0823,
    LocationName.pumpkin_hill_omo_2: 0xFF0825,
    LocationName.mission_street_omo_2: 0xFF0826,
    LocationName.aquatic_mine_omo_2: 0xFF0827,
    LocationName.hidden_base_omo_2: 0xFF0829,
    LocationName.pyramid_cave_omo_2: 0xFF082A,
    LocationName.death_chamber_omo_2: 0xFF082B,
    LocationName.eternal_engine_omo_2: 0xFF082C,
    LocationName.meteor_herd_omo_2: 0xFF082D,
    LocationName.crazy_gadget_omo_2: 0xFF082E,
    LocationName.final_rush_omo_2: 0xFF082F,

    LocationName.iron_gate_omo_2: 0xFF0830,
    LocationName.dry_lagoon_omo_2: 0xFF0831,
    LocationName.sand_ocean_omo_2: 0xFF0832,
    LocationName.radical_highway_omo_2: 0xFF0833,
    LocationName.egg_quarters_omo_2: 0xFF0834,
    LocationName.lost_colony_omo_2: 0xFF0835,
    LocationName.weapons_bed_omo_2: 0xFF0836,
    LocationName.security_hall_omo_2: 0xFF0837,
    LocationName.white_jungle_omo_2: 0xFF0838,
    LocationName.mad_space_omo_2: 0xFF083B,

    LocationName.cannon_core_omo_2: 0xFF083E,

    LocationName.city_escape_omo_3: 0xFF0840,
    LocationName.wild_canyon_omo_3: 0xFF0841,
    LocationName.prison_lane_omo_3: 0xFF0842,
    LocationName.metal_harbor_omo_3: 0xFF0843,
    LocationName.pumpkin_hill_omo_3: 0xFF0845,
    LocationName.mission_street_omo_3: 0xFF0846,
    LocationName.aquatic_mine_omo_3: 0xFF0847,
    LocationName.hidden_base_omo_3: 0xFF0849,
    LocationName.pyramid_cave_omo_3: 0xFF084A,
    LocationName.death_chamber_omo_3: 0xFF084B,
    LocationName.eternal_engine_omo_3: 0xFF084C,
    LocationName.meteor_herd_omo_3: 0xFF084D,
    LocationName.crazy_gadget_omo_3: 0xFF084E,
    LocationName.final_rush_omo_3: 0xFF084F,

    LocationName.iron_gate_omo_3: 0xFF0850,
    LocationName.dry_lagoon_omo_3: 0xFF0851,
    LocationName.radical_highway_omo_3: 0xFF0853,
    LocationName.egg_quarters_omo_3: 0xFF0854,
    LocationName.lost_colony_omo_3: 0xFF0855,
    LocationName.weapons_bed_omo_3: 0xFF0856,
    LocationName.security_hall_omo_3: 0xFF0857,
    LocationName.white_jungle_omo_3: 0xFF0858,
    LocationName.mad_space_omo_3: 0xFF085B,

    LocationName.cannon_core_omo_3: 0xFF085E,

    LocationName.city_escape_omo_4: 0xFF0860,
    LocationName.wild_canyon_omo_4: 0xFF0861,
    LocationName.prison_lane_omo_4: 0xFF0862,
    LocationName.metal_harbor_omo_4: 0xFF0863,
    LocationName.pumpkin_hill_omo_4: 0xFF0865,
    LocationName.mission_street_omo_4: 0xFF0866,
    LocationName.aquatic_mine_omo_4: 0xFF0867,
    LocationName.hidden_base_omo_4: 0xFF0869,
    LocationName.pyramid_cave_omo_4: 0xFF086A,
    LocationName.death_chamber_omo_4: 0xFF086B,
    LocationName.eternal_engine_omo_4: 0xFF086C,
    LocationName.crazy_gadget_omo_4: 0xFF086E,

    LocationName.iron_gate_omo_4: 0xFF0870,
    LocationName.dry_lagoon_omo_4: 0xFF0871,
    LocationName.radical_highway_omo_4: 0xFF0873,
    LocationName.egg_quarters_omo_4: 0xFF0874,
    LocationName.lost_colony_omo_4: 0xFF0875,
    LocationName.security_hall_omo_4: 0xFF0877,
    LocationName.white_jungle_omo_4: 0xFF0878,
    LocationName.mad_space_omo_4: 0xFF087B,

    LocationName.cannon_core_omo_4: 0xFF087E,

    LocationName.city_escape_omo_5: 0xFF0880,
    LocationName.wild_canyon_omo_5: 0xFF0881,
    LocationName.prison_lane_omo_5: 0xFF0882,
    LocationName.metal_harbor_omo_5: 0xFF0883,
    LocationName.pumpkin_hill_omo_5: 0xFF0885,
    LocationName.mission_street_omo_5: 0xFF0886,
    LocationName.aquatic_mine_omo_5: 0xFF0887,
    LocationName.death_chamber_omo_5: 0xFF088B,
    LocationName.eternal_engine_omo_5: 0xFF088C,
    LocationName.crazy_gadget_omo_5: 0xFF088E,

    LocationName.iron_gate_omo_5: 0xFF0890,
    LocationName.dry_lagoon_omo_5: 0xFF0891,
    LocationName.radical_highway_omo_5: 0xFF0893,
    LocationName.egg_quarters_omo_5: 0xFF0894,
    LocationName.lost_colony_omo_5: 0xFF0895,
    LocationName.security_hall_omo_5: 0xFF0897,
    LocationName.white_jungle_omo_5: 0xFF0898,
    LocationName.mad_space_omo_5: 0xFF089B,

    LocationName.cannon_core_omo_5: 0xFF089E,

    LocationName.city_escape_omo_6: 0xFF08A0,
    LocationName.wild_canyon_omo_6: 0xFF08A1,
    LocationName.prison_lane_omo_6: 0xFF08A2,
    LocationName.pumpkin_hill_omo_6: 0xFF08A5,
    LocationName.mission_street_omo_6: 0xFF08A6,
    LocationName.aquatic_mine_omo_6: 0xFF08A7,
    LocationName.death_chamber_omo_6: 0xFF08AB,
    LocationName.eternal_engine_omo_6: 0xFF08AC,
    LocationName.crazy_gadget_omo_6: 0xFF08AE,

    LocationName.iron_gate_omo_6: 0xFF08B0,
    LocationName.dry_lagoon_omo_6: 0xFF08B1,
    LocationName.radical_highway_omo_6: 0xFF08B3,
    LocationName.egg_quarters_omo_6: 0xFF08B4,
    LocationName.lost_colony_omo_6: 0xFF08B5,
    LocationName.security_hall_omo_6: 0xFF08B7,

    LocationName.cannon_core_omo_6: 0xFF08BE,

    LocationName.city_escape_omo_7: 0xFF08C0,
    LocationName.wild_canyon_omo_7: 0xFF08C1,
    LocationName.prison_lane_omo_7: 0xFF08C2,
    LocationName.pumpkin_hill_omo_7: 0xFF08C5,
    LocationName.mission_street_omo_7: 0xFF08C6,
    LocationName.aquatic_mine_omo_7: 0xFF08C7,
    LocationName.death_chamber_omo_7: 0xFF08CB,
    LocationName.eternal_engine_omo_7: 0xFF08CC,
    LocationName.crazy_gadget_omo_7: 0xFF08CE,

    LocationName.dry_lagoon_omo_7: 0xFF08D1,
    LocationName.radical_highway_omo_7: 0xFF08D3,
    LocationName.egg_quarters_omo_7: 0xFF08D4,
    LocationName.lost_colony_omo_7: 0xFF08D5,
    LocationName.security_hall_omo_7: 0xFF08D7,

    LocationName.cannon_core_omo_7: 0xFF08DE,

    LocationName.city_escape_omo_8: 0xFF08E0,
    LocationName.wild_canyon_omo_8: 0xFF08E1,
    LocationName.prison_lane_omo_8: 0xFF08E2,
    LocationName.pumpkin_hill_omo_8: 0xFF08E5,
    LocationName.mission_street_omo_8: 0xFF08E6,
    LocationName.death_chamber_omo_8: 0xFF08EB,
    LocationName.eternal_engine_omo_8: 0xFF08EC,
    LocationName.crazy_gadget_omo_8: 0xFF08EE,

    LocationName.dry_lagoon_omo_8: 0xFF08F1,
    LocationName.radical_highway_omo_8: 0xFF08F3,
    LocationName.lost_colony_omo_8: 0xFF08F5,
    LocationName.security_hall_omo_8: 0xFF08F7,

    LocationName.cannon_core_omo_8: 0xFF08FE,

    LocationName.city_escape_omo_9: 0xFF0900,
    LocationName.wild_canyon_omo_9: 0xFF0901,
    LocationName.prison_lane_omo_9: 0xFF0902,
    LocationName.pumpkin_hill_omo_9: 0xFF0905,
    LocationName.death_chamber_omo_9: 0xFF090B,
    LocationName.eternal_engine_omo_9: 0xFF090C,
    LocationName.crazy_gadget_omo_9: 0xFF090E,

    LocationName.dry_lagoon_omo_9: 0xFF0911,
    LocationName.security_hall_omo_9: 0xFF0917,

    LocationName.cannon_core_omo_9: 0xFF091E,

    LocationName.city_escape_omo_10: 0xFF0920,
    LocationName.wild_canyon_omo_10: 0xFF0921,
    LocationName.prison_lane_omo_10: 0xFF0922,
    LocationName.pumpkin_hill_omo_10: 0xFF0925,
    LocationName.eternal_engine_omo_10: 0xFF092C,
    LocationName.crazy_gadget_omo_10: 0xFF092E,

    LocationName.dry_lagoon_omo_10: 0xFF0931,
    LocationName.security_hall_omo_10: 0xFF0937,

    LocationName.city_escape_omo_11: 0xFF0940,
    LocationName.pumpkin_hill_omo_11: 0xFF0945,
    LocationName.eternal_engine_omo_11: 0xFF094C,
    LocationName.crazy_gadget_omo_11: 0xFF094E,

    LocationName.dry_lagoon_omo_11: 0xFF0951,
    LocationName.security_hall_omo_11: 0xFF0957,

    LocationName.city_escape_omo_12: 0xFF0960,
    LocationName.eternal_engine_omo_12: 0xFF096C,
    LocationName.crazy_gadget_omo_12: 0xFF096E,

    LocationName.dry_lagoon_omo_12: 0xFF0971,
    LocationName.security_hall_omo_12: 0xFF0977,

    LocationName.city_escape_omo_13: 0xFF0980,
    LocationName.crazy_gadget_omo_13: 0xFF098E,

    LocationName.city_escape_omo_14: 0xFF09A0,
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

    LocationName.chao_standard_karate: 0xFF0301,
}

chao_garden_expert_location_table = {
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

    LocationName.chao_expert_karate: 0xFF0302,
    LocationName.chao_super_karate: 0xFF0303,
}

kart_race_beginner_location_table = {
    LocationName.kart_race_beginner_sonic: 0xFF0A00,
    LocationName.kart_race_beginner_tails: 0xFF0A01,
    LocationName.kart_race_beginner_knuckles: 0xFF0A02,
    LocationName.kart_race_beginner_shadow: 0xFF0A03,
    LocationName.kart_race_beginner_eggman: 0xFF0A04,
    LocationName.kart_race_beginner_rouge: 0xFF0A05,
}

kart_race_standard_location_table = {
    LocationName.kart_race_standard_sonic: 0xFF0A06,
    LocationName.kart_race_standard_tails: 0xFF0A07,
    LocationName.kart_race_standard_knuckles: 0xFF0A08,
    LocationName.kart_race_standard_shadow: 0xFF0A09,
    LocationName.kart_race_standard_eggman: 0xFF0A0A,
    LocationName.kart_race_standard_rouge: 0xFF0A0B,
}

kart_race_expert_location_table = {
    LocationName.kart_race_expert_sonic: 0xFF0A0C,
    LocationName.kart_race_expert_tails: 0xFF0A0D,
    LocationName.kart_race_expert_knuckles: 0xFF0A0E,
    LocationName.kart_race_expert_shadow: 0xFF0A0F,
    LocationName.kart_race_expert_eggman: 0xFF0A10,
    LocationName.kart_race_expert_rouge: 0xFF0A11,
}

kart_race_mini_location_table = {
    LocationName.kart_race_beginner: 0xFF0A12,
    LocationName.kart_race_standard: 0xFF0A13,
    LocationName.kart_race_expert: 0xFF0A14,
}

green_hill_location_table = {
    LocationName.green_hill: 0xFF001F,
}

green_hill_chao_location_table = {
    LocationName.green_hill_chao_1: 0xFF041F,
}

final_boss_location_table = {
    # LocationName.biolizard: 0xFF003F,
    LocationName.finalhazard: 0xFF005F,
}

grand_prix_location_table = {
    LocationName.grand_prix: 0xFF007F,
}

all_locations = {
    **mission_location_table,
    **upgrade_location_table,
    **boss_gate_location_table,
    **chao_key_location_table,
    **pipe_location_table,
    **hidden_whistle_location_table,
    **beetle_location_table,
    **omochao_location_table,
    **chao_garden_beginner_location_table,
    **chao_garden_intermediate_location_table,
    **chao_garden_expert_location_table,
    **kart_race_beginner_location_table,
    **kart_race_standard_location_table,
    **kart_race_expert_location_table,
    **kart_race_mini_location_table,
    **green_hill_location_table,
    **green_hill_chao_location_table,
    **final_boss_location_table,
    **grand_prix_location_table,
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


def setup_locations(world: MultiWorld, player: int, mission_map: typing.Dict[int, int], mission_count_map: typing.Dict[int, int]):
    location_table = {}
    chao_location_table = {}

    if world.goal[player] == 3:
        if world.kart_race_checks[player] == 2:
            location_table.update({**kart_race_beginner_location_table})
            location_table.update({**kart_race_standard_location_table})
            location_table.update({**kart_race_expert_location_table})
        elif world.kart_race_checks[player] == 1:
            location_table.update({**kart_race_mini_location_table})
        location_table.update({**grand_prix_location_table})
    else:
        for i in range(31):
            mission_count = mission_count_map[i]
            mission_order: typing.List[int] = mission_orders[mission_map[i]]
            stage_prefix: str = stage_name_prefixes[i]

            for j in range(mission_count):
                mission_number = mission_order[j]
                location_name: str = stage_prefix + str(mission_number)
                location_table[location_name] = mission_location_table[location_name]

        location_table.update({**upgrade_location_table})

        if world.keysanity[player]:
            location_table.update({**chao_key_location_table})

        if world.whistlesanity[player].value == 1:
            location_table.update({**pipe_location_table})
        elif world.whistlesanity[player].value == 2:
            location_table.update({**hidden_whistle_location_table})
        elif world.whistlesanity[player].value == 3:
            location_table.update({**pipe_location_table})
            location_table.update({**hidden_whistle_location_table})

        if world.beetlesanity[player]:
            location_table.update({**beetle_location_table})

        if world.omosanity[player]:
            location_table.update({**omochao_location_table})

        if world.kart_race_checks[player] == 2:
            location_table.update({**kart_race_beginner_location_table})
            location_table.update({**kart_race_standard_location_table})
            location_table.update({**kart_race_expert_location_table})
        elif world.kart_race_checks[player] == 1:
            location_table.update({**kart_race_mini_location_table})

        if world.goal[player].value == 0 or world.goal[player].value == 2:
            location_table.update({**final_boss_location_table})

        if world.goal[player].value == 1 or world.goal[player].value == 2:
            location_table.update({**green_hill_location_table})

            if world.keysanity[player]:
                location_table.update({**green_hill_chao_location_table})

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
