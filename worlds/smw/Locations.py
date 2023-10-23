import typing

from BaseClasses import Location
from .Names import LocationName


class SMWLocation(Location):
    game: str = "Super Mario World"

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, prog_byte: int = None, prog_bit: int = None):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit  = prog_bit


level_location_table = {
    LocationName.yoshis_island_1_exit_1:  0xBC0000,
    LocationName.yoshis_island_2_exit_1:  0xBC0001,
    LocationName.yoshis_island_3_exit_1:  0xBC0002,
    LocationName.yoshis_island_4_exit_1:  0xBC0003,
    LocationName.yoshis_island_castle:    0xBC0004,
    LocationName.yoshis_island_koopaling: 0xBC00A0,

    LocationName.yellow_switch_palace: 0xBC0005,

    LocationName.donut_plains_1_exit_1:     0xBC0006,
    LocationName.donut_plains_1_exit_2:     0xBC0007,
    LocationName.donut_plains_2_exit_1:     0xBC0008,
    LocationName.donut_plains_2_exit_2:     0xBC0009,
    LocationName.donut_plains_3_exit_1:     0xBC000A,
    LocationName.donut_plains_4_exit_1:     0xBC000B,
    LocationName.donut_secret_1_exit_1:     0xBC000C,
    LocationName.donut_secret_1_exit_2:     0xBC000D,
    LocationName.donut_secret_2_exit_1:     0xBC0063,
    LocationName.donut_ghost_house_exit_1:  0xBC000E,
    LocationName.donut_ghost_house_exit_2:  0xBC000F,
    LocationName.donut_secret_house_exit_1: 0xBC0010,
    LocationName.donut_secret_house_exit_2: 0xBC0011,
    LocationName.donut_plains_castle:       0xBC0012,
    LocationName.donut_plains_koopaling:    0xBC00A1,

    LocationName.green_switch_palace: 0xBC0013,

    LocationName.vanilla_dome_1_exit_1:      0xBC0014,
    LocationName.vanilla_dome_1_exit_2:      0xBC0015,
    LocationName.vanilla_dome_2_exit_1:      0xBC0016,
    LocationName.vanilla_dome_2_exit_2:      0xBC0017,
    LocationName.vanilla_dome_3_exit_1:      0xBC0018,
    LocationName.vanilla_dome_4_exit_1:      0xBC0019,
    LocationName.vanilla_secret_1_exit_1:    0xBC001A,
    LocationName.vanilla_secret_1_exit_2:    0xBC001B,
    LocationName.vanilla_secret_2_exit_1:    0xBC001C,
    LocationName.vanilla_secret_3_exit_1:    0xBC001D,
    LocationName.vanilla_ghost_house_exit_1: 0xBC001E,
    LocationName.vanilla_fortress:           0xBC0020,
    LocationName.vanilla_reznor:             0xBC00B0,
    LocationName.vanilla_dome_castle:        0xBC0021,
    LocationName.vanilla_dome_koopaling:     0xBC00A2,

    LocationName.red_switch_palace: 0xBC0022,

    LocationName.butter_bridge_1_exit_1: 0xBC0023,
    LocationName.butter_bridge_2_exit_1: 0xBC0024,
    LocationName.cheese_bridge_exit_1:   0xBC0025,
    LocationName.cheese_bridge_exit_2:   0xBC0026,
    LocationName.cookie_mountain_exit_1: 0xBC0027,
    LocationName.soda_lake_exit_1:       0xBC0028,
    LocationName.twin_bridges_castle:    0xBC0029,
    LocationName.twin_bridges_koopaling: 0xBC00A3,

    LocationName.forest_of_illusion_1_exit_1: 0xBC002A,
    LocationName.forest_of_illusion_1_exit_2: 0xBC002B,
    LocationName.forest_of_illusion_2_exit_1: 0xBC002C,
    LocationName.forest_of_illusion_2_exit_2: 0xBC002D,
    LocationName.forest_of_illusion_3_exit_1: 0xBC002E,
    LocationName.forest_of_illusion_3_exit_2: 0xBC002F,
    LocationName.forest_of_illusion_4_exit_1: 0xBC0030,
    LocationName.forest_of_illusion_4_exit_2: 0xBC0031,
    LocationName.forest_ghost_house_exit_1:   0xBC0032,
    LocationName.forest_ghost_house_exit_2:   0xBC0033,
    LocationName.forest_secret_exit_1:        0xBC0034,
    LocationName.forest_fortress:             0xBC0035,
    LocationName.forest_reznor:               0xBC00B1,
    LocationName.forest_castle:               0xBC0036,
    LocationName.forest_koopaling:            0xBC00A4,

    LocationName.blue_switch_palace:      0xBC0037,

    LocationName.chocolate_island_1_exit_1:    0xBC0038,
    LocationName.chocolate_island_2_exit_1:    0xBC0039,
    LocationName.chocolate_island_2_exit_2:    0xBC003A,
    LocationName.chocolate_island_3_exit_1:    0xBC003B,
    LocationName.chocolate_island_3_exit_2:    0xBC003C,
    LocationName.chocolate_island_4_exit_1:    0xBC003D,
    LocationName.chocolate_island_5_exit_1:    0xBC003E,
    LocationName.chocolate_ghost_house_exit_1: 0xBC003F,
    LocationName.chocolate_secret_exit_1:      0xBC0041,
    LocationName.chocolate_fortress:           0xBC0042,
    LocationName.chocolate_reznor:             0xBC00B2,
    LocationName.chocolate_castle:             0xBC0043,
    LocationName.chocolate_koopaling:          0xBC00A5,

    LocationName.sunken_ghost_ship:    0xBC0044,

    LocationName.valley_of_bowser_1_exit_1: 0xBC0045,
    LocationName.valley_of_bowser_2_exit_1: 0xBC0046,
    LocationName.valley_of_bowser_2_exit_2: 0xBC0047,
    LocationName.valley_of_bowser_3_exit_1: 0xBC0048,
    LocationName.valley_of_bowser_4_exit_1: 0xBC0049,
    LocationName.valley_of_bowser_4_exit_2: 0xBC004A,
    LocationName.valley_ghost_house_exit_1: 0xBC004B,
    LocationName.valley_ghost_house_exit_2: 0xBC004C,
    LocationName.valley_fortress:           0xBC004E,
    LocationName.valley_reznor:             0xBC00B3,
    LocationName.valley_castle:             0xBC004F,
    LocationName.valley_koopaling:          0xBC00A6,

    LocationName.star_road_1_exit_1: 0xBC0051,
    LocationName.star_road_1_exit_2: 0xBC0052,
    LocationName.star_road_2_exit_1: 0xBC0053,
    LocationName.star_road_2_exit_2: 0xBC0054,
    LocationName.star_road_3_exit_1: 0xBC0055,
    LocationName.star_road_3_exit_2: 0xBC0056,
    LocationName.star_road_4_exit_1: 0xBC0057,
    LocationName.star_road_4_exit_2: 0xBC0058,
    LocationName.star_road_5_exit_1: 0xBC0059,
    LocationName.star_road_5_exit_2: 0xBC005A,

    LocationName.special_zone_1_exit_1: 0xBC005B,
    LocationName.special_zone_2_exit_1: 0xBC005C,
    LocationName.special_zone_3_exit_1: 0xBC005D,
    LocationName.special_zone_4_exit_1: 0xBC005E,
    LocationName.special_zone_5_exit_1: 0xBC005F,
    LocationName.special_zone_6_exit_1: 0xBC0060,
    LocationName.special_zone_7_exit_1: 0xBC0061,
    LocationName.special_zone_8_exit_1: 0xBC0062,
}

dragon_coin_location_table = {
    LocationName.yoshis_island_1_dragon: 0xBC0100,
    LocationName.yoshis_island_2_dragon: 0xBC0101,
    LocationName.yoshis_island_3_dragon: 0xBC0102,
    LocationName.yoshis_island_4_dragon: 0xBC0103,

    LocationName.donut_plains_1_dragon: 0xBC0106,
    LocationName.donut_plains_2_dragon: 0xBC0108,
    LocationName.donut_plains_3_dragon: 0xBC010A,
    LocationName.donut_plains_4_dragon: 0xBC010B,
    LocationName.donut_secret_1_dragon: 0xBC010C,
    LocationName.donut_secret_2_dragon: 0xBC010D,

    LocationName.vanilla_dome_1_dragon:      0xBC0114,
    LocationName.vanilla_dome_2_dragon:      0xBC0116,
    LocationName.vanilla_dome_3_dragon:      0xBC0118,
    LocationName.vanilla_dome_4_dragon:      0xBC0119,
    LocationName.vanilla_secret_1_dragon:    0xBC011A,
    LocationName.vanilla_secret_2_dragon:    0xBC011C,
    LocationName.vanilla_secret_3_dragon:    0xBC011D,
    LocationName.vanilla_ghost_house_dragon: 0xBC011E,

    LocationName.butter_bridge_1_dragon: 0xBC0123,
    LocationName.butter_bridge_2_dragon: 0xBC0124,
    LocationName.cheese_bridge_dragon:   0xBC0125,
    LocationName.cookie_mountain_dragon: 0xBC0127,
    LocationName.soda_lake_dragon:       0xBC0128,

    LocationName.forest_of_illusion_2_dragon: 0xBC012C,
    LocationName.forest_of_illusion_3_dragon: 0xBC012E,
    LocationName.forest_of_illusion_4_dragon: 0xBC0130,
    LocationName.forest_ghost_house_dragon:   0xBC0132,
    LocationName.forest_secret_dragon:        0xBC0134,
    LocationName.forest_castle_dragon:        0xBC0136,

    LocationName.chocolate_island_1_dragon:    0xBC0138,
    LocationName.chocolate_island_2_dragon:    0xBC0139,
    LocationName.chocolate_island_3_dragon:    0xBC013B,
    LocationName.chocolate_island_4_dragon:    0xBC013D,
    LocationName.chocolate_island_5_dragon:    0xBC013E,

    LocationName.sunken_ghost_ship_dragon: 0xBC0144,

    LocationName.valley_of_bowser_1_dragon: 0xBC0145,
    LocationName.valley_of_bowser_2_dragon: 0xBC0146,
    LocationName.valley_of_bowser_3_dragon: 0xBC0148,
    LocationName.valley_ghost_house_dragon: 0xBC014B,
    LocationName.valley_castle_dragon:      0xBC014F,

    LocationName.star_road_1_dragon: 0xBC0151,

    LocationName.special_zone_1_dragon: 0xBC015B,
    LocationName.special_zone_2_dragon: 0xBC015C,
    LocationName.special_zone_3_dragon: 0xBC015D,
    LocationName.special_zone_4_dragon: 0xBC015E,
    LocationName.special_zone_5_dragon: 0xBC015F,
    LocationName.special_zone_6_dragon: 0xBC0160,
    LocationName.special_zone_7_dragon: 0xBC0161,
    LocationName.special_zone_8_dragon: 0xBC0162,
}

bowser_location_table = {
    LocationName.bowser: 0xBC0200,
}

yoshi_house_location_table = {
    LocationName.yoshis_house: 0xBC0201,
}

all_locations = {
    **level_location_table,
    **dragon_coin_location_table,
    **bowser_location_table,
    **yoshi_house_location_table,
}

special_zone_level_names = [
    LocationName.special_zone_1_exit_1,
    LocationName.special_zone_2_exit_1,
    LocationName.special_zone_3_exit_1,
    LocationName.special_zone_4_exit_1,
    LocationName.special_zone_5_exit_1,
    LocationName.special_zone_6_exit_1,
    LocationName.special_zone_7_exit_1,
    LocationName.special_zone_8_exit_1,
]

special_zone_dragon_coin_names = [
    LocationName.special_zone_1_dragon,
    LocationName.special_zone_2_dragon,
    LocationName.special_zone_3_dragon,
    LocationName.special_zone_4_dragon,
    LocationName.special_zone_5_dragon,
    LocationName.special_zone_6_dragon,
    LocationName.special_zone_7_dragon,
    LocationName.special_zone_8_dragon,
]

location_table = {}


def setup_locations(world, player: int):
    location_table = {**level_location_table}

    # Dragon Coins here
    if world.dragon_coin_checks[player].value:
        location_table.update({**dragon_coin_location_table})

    if world.goal[player] == "yoshi_egg_hunt":
        location_table.update({**yoshi_house_location_table})
    else:
        location_table.update({**bowser_location_table})

    return location_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
