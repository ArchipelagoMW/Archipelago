import typing

from BaseClasses import Region, ItemClassification
from .Locations import WaffleLocation
from .Levels import level_info_dict
from .Items import WaffleItem
from .Names import LocationName
from .Options import Goal
from worlds.generic.Rules import add_rule

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WaffleWorld

GREEN_YOSHI_LEVELS = [
    LocationName.yoshis_island_2_region,
    LocationName.yoshis_island_3_region,
    LocationName.donut_plains_1_region,
    LocationName.donut_plains_4_region,
    LocationName.vanilla_dome_3_region,
    LocationName.vanilla_secret_2_region,
    LocationName.butter_bridge_2_region,
    LocationName.cookie_mountain_region,
    LocationName.forest_of_illusion_1_region,
    LocationName.forest_of_illusion_3_region,
    LocationName.chocolate_island_1_region,
    LocationName.chocolate_island_2_region,
    LocationName.valley_of_bowser_4_region,
    LocationName.special_zone_5_region,
    LocationName.special_zone_7_region,
    LocationName.special_zone_8_region,
]

BLUE_YOSHI_LEVELS = [
    LocationName.cheese_bridge_region,
    LocationName.star_road_2_region,
    LocationName.valley_of_bowser_2_region,
    LocationName.special_zone_3_region,
]

RED_YOSHI_LEVELS = [
    LocationName.star_road_1_region,
    LocationName.star_road_4_region,
]

YELLOW_YOSHI_LEVELS = [
    LocationName.star_road_3_region,
    LocationName.star_road_5_region,
]

def create_regions(world: "WaffleWorld", active_locations: typing.Dict[int,int]):
    menu_region = create_region(world, active_locations, 'Menu', None)

    yoshis_island_region = create_region(world, active_locations, LocationName.yoshis_island_region, None)

    yoshis_house_tile = create_region(world, active_locations, LocationName.yoshis_house_tile, None)

    yoshis_house_region_locations = []
    if world.options.goal == Goal.option_yoshi_house:
        yoshis_house_region_locations.append(LocationName.yoshis_house)
    yoshis_house_region = create_region(world, active_locations, LocationName.yoshis_house,
                                        yoshis_house_region_locations)

    yoshis_island_1_tile = create_region(world, active_locations, LocationName.yoshis_island_1_tile, None)
    yoshis_island_1_region = create_region(world, active_locations, LocationName.yoshis_island_1_region, None)
    yoshis_island_1_exit_1 = create_region(world, active_locations, LocationName.yoshis_island_1_exit_1,
                                           [LocationName.yoshis_island_1_exit_1])

    yoshis_island_2_tile = create_region(world, active_locations, LocationName.yoshis_island_2_tile, None)
    yoshis_island_2_region = create_region(world, active_locations, LocationName.yoshis_island_2_region, None)
    yoshis_island_2_exit_1 = create_region(world, active_locations, LocationName.yoshis_island_2_exit_1,
                                           [LocationName.yoshis_island_2_exit_1])

    yoshis_island_3_tile = create_region(world, active_locations, LocationName.yoshis_island_3_tile, None)
    yoshis_island_3_region = create_region(world, active_locations, LocationName.yoshis_island_3_region, None)
    yoshis_island_3_exit_1 = create_region(world, active_locations, LocationName.yoshis_island_3_exit_1,
                                           [LocationName.yoshis_island_3_exit_1])

    yoshis_island_4_tile = create_region(world, active_locations, LocationName.yoshis_island_4_tile, None)
    yoshis_island_4_region = create_region(world, active_locations, LocationName.yoshis_island_4_region, None)
    yoshis_island_4_exit_1 = create_region(world, active_locations, LocationName.yoshis_island_4_exit_1,
                                           [LocationName.yoshis_island_4_exit_1])

    yoshis_island_castle_tile = create_region(world, active_locations, LocationName.yoshis_island_castle_tile, None)
    yoshis_island_castle_region = create_region(world, active_locations, LocationName.yoshis_island_castle_region, None)
    yoshis_island_castle = create_region(world, active_locations, LocationName.yoshis_island_castle,
                                         [LocationName.yoshis_island_castle])

    yellow_switch_palace_tile = create_region(world, active_locations, LocationName.yellow_switch_palace_tile, None)
    yellow_switch_palace = create_region(world, active_locations, LocationName.yellow_switch_palace,
                                         [LocationName.yellow_switch_palace])


    donut_plains_1_tile = create_region(world, active_locations, LocationName.donut_plains_1_tile, None)
    donut_plains_1_region = create_region(world, active_locations, LocationName.donut_plains_1_region, None)
    donut_plains_1_exit_1 = create_region(world, active_locations, LocationName.donut_plains_1_exit_1, 
                                          [LocationName.donut_plains_1_exit_1])
    donut_plains_1_exit_2 = create_region(world, active_locations, LocationName.donut_plains_1_exit_2, 
                                          [LocationName.donut_plains_1_exit_2])

    donut_plains_2_tile = create_region(world, active_locations, LocationName.donut_plains_2_tile, None)
    donut_plains_2_region = create_region(world, active_locations, LocationName.donut_plains_2_region, None)
    donut_plains_2_exit_1 = create_region(world, active_locations, LocationName.donut_plains_2_exit_1, 
                                          [LocationName.donut_plains_2_exit_1])
    donut_plains_2_exit_2 = create_region(world, active_locations, LocationName.donut_plains_2_exit_2, 
                                          [LocationName.donut_plains_2_exit_2])
    
    donut_plains_3_tile = create_region(world, active_locations, LocationName.donut_plains_3_tile, None)
    donut_plains_3_region = create_region(world, active_locations, LocationName.donut_plains_3_region, None)
    donut_plains_3_exit_1 = create_region(world, active_locations, LocationName.donut_plains_3_exit_1,
                                          [LocationName.donut_plains_3_exit_1])

    donut_plains_4_tile = create_region(world, active_locations, LocationName.donut_plains_4_tile, None)
    donut_plains_4_region = create_region(world, active_locations, LocationName.donut_plains_4_region, None)
    donut_plains_4_exit_1 = create_region(world, active_locations, LocationName.donut_plains_4_exit_1,
                                          [LocationName.donut_plains_4_exit_1])

    donut_secret_1_tile = create_region(world, active_locations, LocationName.donut_secret_1_tile, None)
    donut_secret_1_region = create_region(world, active_locations, LocationName.donut_secret_1_region, None)
    donut_secret_1_exit_1 = create_region(world, active_locations, LocationName.donut_secret_1_exit_1,
                                          [LocationName.donut_secret_1_exit_1])
    donut_secret_1_exit_2 = create_region(world, active_locations, LocationName.donut_secret_1_exit_2,
                                          [LocationName.donut_secret_1_exit_2])

    donut_secret_2_tile = create_region(world, active_locations, LocationName.donut_secret_2_tile, None)
    donut_secret_2_region = create_region(world, active_locations, LocationName.donut_secret_2_region, None)
    donut_secret_2_exit_1 = create_region(world, active_locations, LocationName.donut_secret_2_exit_1,
                                          [LocationName.donut_secret_2_exit_1])

    donut_ghost_house_tile = create_region(world, active_locations, LocationName.donut_ghost_house_tile, None)
    donut_ghost_house_region = create_region(world, active_locations, LocationName.donut_ghost_house_region, None)
    donut_ghost_house_exit_1 = create_region(world, active_locations, LocationName.donut_ghost_house_exit_1, 
                                             [LocationName.donut_ghost_house_exit_1])
    donut_ghost_house_exit_2 = create_region(world, active_locations, LocationName.donut_ghost_house_exit_2, 
                                             [LocationName.donut_ghost_house_exit_2])

    donut_secret_house_tile = create_region(world, active_locations, LocationName.donut_secret_house_tile, None)
    donut_secret_house_region = create_region(world, active_locations, LocationName.donut_secret_house_region, None)
    donut_secret_house_exit_1 = create_region(world, active_locations, LocationName.donut_secret_house_exit_1, 
                                             [LocationName.donut_secret_house_exit_1])
    donut_secret_house_exit_2 = create_region(world, active_locations, LocationName.donut_secret_house_exit_2, 
                                             [LocationName.donut_secret_house_exit_2])

    donut_plains_castle_tile = create_region(world, active_locations, LocationName.donut_plains_castle_tile, None)
    donut_plains_castle_region = create_region(world, active_locations, LocationName.donut_plains_castle_region, None)
    donut_plains_castle = create_region(world, active_locations, LocationName.donut_plains_castle,
                                        [LocationName.donut_plains_castle])

    green_switch_palace_tile = create_region(world, active_locations, LocationName.green_switch_palace_tile, None)
    green_switch_palace = create_region(world, active_locations, LocationName.green_switch_palace,
                                        [LocationName.green_switch_palace])

    donut_plains_top_secret_tile = create_region(world, active_locations, LocationName.donut_plains_top_secret_tile, None)
    donut_plains_top_secret = create_region(world, active_locations, LocationName.donut_plains_top_secret, None)


    vanilla_dome_1_tile = create_region(world, active_locations, LocationName.vanilla_dome_1_tile, None)
    vanilla_dome_1_region = create_region(world, active_locations, LocationName.vanilla_dome_1_region, None)
    vanilla_dome_1_exit_1 = create_region(world, active_locations, LocationName.vanilla_dome_1_exit_1,
                                          [LocationName.vanilla_dome_1_exit_1])
    vanilla_dome_1_exit_2 = create_region(world, active_locations, LocationName.vanilla_dome_1_exit_2,
                                          [LocationName.vanilla_dome_1_exit_2])

    vanilla_dome_2_tile = create_region(world, active_locations, LocationName.vanilla_dome_2_tile, None)
    vanilla_dome_2_region = create_region(world, active_locations, LocationName.vanilla_dome_2_region, None)
    vanilla_dome_2_exit_1 = create_region(world, active_locations, LocationName.vanilla_dome_2_exit_1,
                                          [LocationName.vanilla_dome_2_exit_1])
    vanilla_dome_2_exit_2 = create_region(world, active_locations, LocationName.vanilla_dome_2_exit_2,
                                          [LocationName.vanilla_dome_2_exit_2])

    vanilla_dome_3_tile = create_region(world, active_locations, LocationName.vanilla_dome_3_tile, None)
    vanilla_dome_3_region = create_region(world, active_locations, LocationName.vanilla_dome_3_region, None)
    vanilla_dome_3_exit_1 = create_region(world, active_locations, LocationName.vanilla_dome_3_exit_1,
                                          [LocationName.vanilla_dome_3_exit_1])

    vanilla_dome_4_tile = create_region(world, active_locations, LocationName.vanilla_dome_4_tile, None)
    vanilla_dome_4_region = create_region(world, active_locations, LocationName.vanilla_dome_4_region, None)
    vanilla_dome_4_exit_1 = create_region(world, active_locations, LocationName.vanilla_dome_4_exit_1,
                                          [LocationName.vanilla_dome_4_exit_1])

    vanilla_secret_1_tile = create_region(world, active_locations, LocationName.vanilla_secret_1_tile, None)
    vanilla_secret_1_region = create_region(world, active_locations, LocationName.vanilla_secret_1_region, None)
    vanilla_secret_1_exit_1 = create_region(world, active_locations, LocationName.vanilla_secret_1_exit_1,
                                            [LocationName.vanilla_secret_1_exit_1])
    vanilla_secret_1_exit_2 = create_region(world, active_locations, LocationName.vanilla_secret_1_exit_2,
                                            [LocationName.vanilla_secret_1_exit_2])

    vanilla_secret_2_tile = create_region(world, active_locations, LocationName.vanilla_secret_2_tile, None)
    vanilla_secret_2_region = create_region(world, active_locations, LocationName.vanilla_secret_2_region, None)
    vanilla_secret_2_exit_1 = create_region(world, active_locations, LocationName.vanilla_secret_2_exit_1,
                                            [LocationName.vanilla_secret_2_exit_1])

    vanilla_secret_3_tile = create_region(world, active_locations, LocationName.vanilla_secret_3_tile, None)
    vanilla_secret_3_region = create_region(world, active_locations, LocationName.vanilla_secret_3_region, None)
    vanilla_secret_3_exit_1 = create_region(world, active_locations, LocationName.vanilla_secret_3_exit_1,
                                            [LocationName.vanilla_secret_3_exit_1])

    vanilla_ghost_house_tile = create_region(world, active_locations, LocationName.vanilla_ghost_house_tile, None)
    vanilla_ghost_house_region = create_region(world, active_locations, LocationName.vanilla_ghost_house_region, None)
    vanilla_ghost_house_exit_1 = create_region(world, active_locations, LocationName.vanilla_ghost_house_exit_1,
                                               [LocationName.vanilla_ghost_house_exit_1])

    vanilla_fortress_tile = create_region(world, active_locations, LocationName.vanilla_fortress_tile, None)
    vanilla_fortress_region = create_region(world, active_locations, LocationName.vanilla_fortress_region, None)
    vanilla_fortress = create_region(world, active_locations, LocationName.vanilla_fortress,
                                     [LocationName.vanilla_fortress])

    vanilla_dome_castle_tile = create_region(world, active_locations, LocationName.vanilla_dome_castle_tile, None)
    vanilla_dome_castle_region = create_region(world, active_locations, LocationName.vanilla_dome_castle_region, None)
    vanilla_dome_castle = create_region(world, active_locations, LocationName.vanilla_dome_castle,
                                        [LocationName.vanilla_dome_castle])

    red_switch_palace_tile = create_region(world, active_locations, LocationName.red_switch_palace_tile, None)
    red_switch_palace = create_region(world, active_locations, LocationName.red_switch_palace,
                                      [LocationName.red_switch_palace])


    butter_bridge_1_tile = create_region(world, active_locations, LocationName.butter_bridge_1_tile, None)
    butter_bridge_1_region = create_region(world, active_locations, LocationName.butter_bridge_1_region, None)
    butter_bridge_1_exit_1 = create_region(world, active_locations, LocationName.butter_bridge_1_exit_1,
                                           [LocationName.butter_bridge_1_exit_1])

    butter_bridge_2_tile = create_region(world, active_locations, LocationName.butter_bridge_2_tile, None)
    butter_bridge_2_region = create_region(world, active_locations, LocationName.butter_bridge_2_region, None)
    butter_bridge_2_exit_1 = create_region(world, active_locations, LocationName.butter_bridge_2_exit_1,
                                           [LocationName.butter_bridge_2_exit_1])

    cheese_bridge_tile = create_region(world, active_locations, LocationName.cheese_bridge_tile, None)
    cheese_bridge_region = create_region(world, active_locations, LocationName.cheese_bridge_region, None)
    cheese_bridge_exit_1 = create_region(world, active_locations, LocationName.cheese_bridge_exit_1, 
                                         [LocationName.cheese_bridge_exit_1])
    cheese_bridge_exit_2 = create_region(world, active_locations, LocationName.cheese_bridge_exit_2, 
                                         [LocationName.cheese_bridge_exit_2])

    cookie_mountain_tile = create_region(world, active_locations, LocationName.cookie_mountain_tile, None)
    cookie_mountain_region = create_region(world, active_locations, LocationName.cookie_mountain_region, None)
    cookie_mountain_exit_1 = create_region(world, active_locations, LocationName.cookie_mountain_exit_1,
                                          [LocationName.cookie_mountain_exit_1])

    soda_lake_tile = create_region(world, active_locations, LocationName.soda_lake_tile, None)
    soda_lake_region = create_region(world, active_locations, LocationName.soda_lake_region, None)
    soda_lake_exit_1 = create_region(world, active_locations, LocationName.soda_lake_exit_1,
                                     [LocationName.soda_lake_exit_1])

    twin_bridges_castle_tile = create_region(world, active_locations, LocationName.twin_bridges_castle_tile, None)
    twin_bridges_castle_region = create_region(world, active_locations, LocationName.twin_bridges_castle_region, None)
    twin_bridges_castle = create_region(world, active_locations, LocationName.twin_bridges_castle,
                                        [LocationName.twin_bridges_castle])


    forest_of_illusion_1_tile = create_region(world, active_locations, LocationName.forest_of_illusion_1_tile, None)
    forest_of_illusion_1_region = create_region(world, active_locations, LocationName.forest_of_illusion_1_region, None)
    forest_of_illusion_1_exit_1 = create_region(world, active_locations, LocationName.forest_of_illusion_1_exit_1, 
                                                [LocationName.forest_of_illusion_1_exit_1])
    forest_of_illusion_1_exit_2 = create_region(world, active_locations, LocationName.forest_of_illusion_1_exit_2, 
                                                [LocationName.forest_of_illusion_1_exit_2])

    forest_of_illusion_2_tile = create_region(world, active_locations, LocationName.forest_of_illusion_2_tile, None)
    forest_of_illusion_2_region = create_region(world, active_locations, LocationName.forest_of_illusion_2_region, None)
    forest_of_illusion_2_exit_1 = create_region(world, active_locations, LocationName.forest_of_illusion_2_exit_1, 
                                                [LocationName.forest_of_illusion_2_exit_1])
    forest_of_illusion_2_exit_2 = create_region(world, active_locations, LocationName.forest_of_illusion_2_exit_2, 
                                                [LocationName.forest_of_illusion_2_exit_2])

    forest_of_illusion_3_tile = create_region(world, active_locations, LocationName.forest_of_illusion_3_tile, None)
    forest_of_illusion_3_region = create_region(world, active_locations, LocationName.forest_of_illusion_3_region, None)
    forest_of_illusion_3_exit_1 = create_region(world, active_locations, LocationName.forest_of_illusion_3_exit_1,
                                                [LocationName.forest_of_illusion_3_exit_1])
    forest_of_illusion_3_exit_2 = create_region(world, active_locations, LocationName.forest_of_illusion_3_exit_2,
                                                [LocationName.forest_of_illusion_3_exit_2])

    forest_of_illusion_4_tile = create_region(world, active_locations, LocationName.forest_of_illusion_4_tile, None)
    forest_of_illusion_4_region = create_region(world, active_locations, LocationName.forest_of_illusion_4_region, None)
    forest_of_illusion_4_exit_1 = create_region(world, active_locations, LocationName.forest_of_illusion_4_exit_1,
                                                [LocationName.forest_of_illusion_4_exit_1])
    forest_of_illusion_4_exit_2 = create_region(world, active_locations, LocationName.forest_of_illusion_4_exit_2,
                                                [LocationName.forest_of_illusion_4_exit_2])

    forest_ghost_house_tile = create_region(world, active_locations, LocationName.forest_ghost_house_tile, None)
    forest_ghost_house_region = create_region(world, active_locations, LocationName.forest_ghost_house_region, None)
    forest_ghost_house_exit_1 = create_region(world, active_locations, LocationName.forest_ghost_house_exit_1, 
                                              [LocationName.forest_ghost_house_exit_1])
    forest_ghost_house_exit_2 = create_region(world, active_locations, LocationName.forest_ghost_house_exit_2, 
                                              [LocationName.forest_ghost_house_exit_2])

    forest_secret_tile = create_region(world, active_locations, LocationName.forest_secret_tile, None)
    forest_secret_region = create_region(world, active_locations, LocationName.forest_secret_region, None)
    forest_secret_exit_1 = create_region(world, active_locations, LocationName.forest_secret_exit_1,
                                         [LocationName.forest_secret_exit_1])

    forest_fortress_tile = create_region(world, active_locations, LocationName.forest_fortress_tile, None)
    forest_fortress_region = create_region(world, active_locations, LocationName.forest_fortress_region, None)
    forest_fortress = create_region(world, active_locations, LocationName.forest_fortress,
                                    [LocationName.forest_fortress])

    forest_castle_tile = create_region(world, active_locations, LocationName.forest_castle_tile, None)
    forest_castle_region = create_region(world, active_locations, LocationName.forest_castle_region, None)
    forest_castle = create_region(world, active_locations, LocationName.forest_castle,
                                  [LocationName.forest_castle])

    blue_switch_palace_tile = create_region(world, active_locations, LocationName.blue_switch_palace_tile, None)
    blue_switch_palace = create_region(world, active_locations, LocationName.blue_switch_palace,
                                       [LocationName.blue_switch_palace])


    chocolate_island_1_tile = create_region(world, active_locations, LocationName.chocolate_island_1_tile, None)
    chocolate_island_1_region = create_region(world, active_locations, LocationName.chocolate_island_1_region, None)
    chocolate_island_1_exit_1 = create_region(world, active_locations, LocationName.chocolate_island_1_exit_1,
                                              [LocationName.chocolate_island_1_exit_1])

    chocolate_island_2_tile = create_region(world, active_locations, LocationName.chocolate_island_2_tile, None)
    chocolate_island_2_region = create_region(world, active_locations, LocationName.chocolate_island_2_region, None)
    chocolate_island_2_exit_1 = create_region(world, active_locations, LocationName.chocolate_island_2_exit_1, 
                                              [LocationName.chocolate_island_2_exit_1])
    chocolate_island_2_exit_2 = create_region(world, active_locations, LocationName.chocolate_island_2_exit_2, 
                                              [LocationName.chocolate_island_2_exit_2])

    chocolate_island_3_tile = create_region(world, active_locations, LocationName.chocolate_island_3_tile, None)
    chocolate_island_3_region = create_region(world, active_locations, LocationName.chocolate_island_3_region, None)
    chocolate_island_3_exit_1 = create_region(world, active_locations, LocationName.chocolate_island_3_exit_1,
                                              [LocationName.chocolate_island_3_exit_1])
    chocolate_island_3_exit_2 = create_region(world, active_locations, LocationName.chocolate_island_3_exit_2,
                                              [LocationName.chocolate_island_3_exit_2])

    chocolate_island_4_tile = create_region(world, active_locations, LocationName.chocolate_island_4_tile, None)
    chocolate_island_4_region = create_region(world, active_locations, LocationName.chocolate_island_4_region, None)
    chocolate_island_4_exit_1 = create_region(world, active_locations, LocationName.chocolate_island_4_exit_1,
                                              [LocationName.chocolate_island_4_exit_1])

    chocolate_island_5_tile = create_region(world, active_locations, LocationName.chocolate_island_5_tile, None)
    chocolate_island_5_region = create_region(world, active_locations, LocationName.chocolate_island_5_region, None)
    chocolate_island_5_exit_1 = create_region(world, active_locations, LocationName.chocolate_island_5_exit_1,
                                              [LocationName.chocolate_island_5_exit_1])

    chocolate_ghost_house_tile = create_region(world, active_locations, LocationName.chocolate_ghost_house_tile, None)
    chocolate_ghost_house_region = create_region(world, active_locations, LocationName.chocolate_ghost_house_region, None)
    chocolate_ghost_house_exit_1 = create_region(world, active_locations, LocationName.chocolate_ghost_house_exit_1,
                                                 [LocationName.chocolate_ghost_house_exit_1])

    chocolate_secret_tile = create_region(world, active_locations, LocationName.chocolate_secret_tile, None)
    chocolate_secret_region = create_region(world, active_locations, LocationName.chocolate_secret_region, None)
    chocolate_secret_exit_1 = create_region(world, active_locations, LocationName.chocolate_secret_exit_1,
                                            [LocationName.chocolate_secret_exit_1])

    chocolate_fortress_tile = create_region(world, active_locations, LocationName.chocolate_fortress_tile, None)
    chocolate_fortress_region = create_region(world, active_locations, LocationName.chocolate_fortress_region, None)
    chocolate_fortress = create_region(world, active_locations, LocationName.chocolate_fortress,
                                       [LocationName.chocolate_fortress])

    chocolate_castle_tile = create_region(world, active_locations, LocationName.chocolate_castle_tile, None)
    chocolate_castle_region = create_region(world, active_locations, LocationName.chocolate_castle_region, None)
    chocolate_castle = create_region(world, active_locations, LocationName.chocolate_castle,
                                     [LocationName.chocolate_castle])

    sunken_ghost_ship_tile = create_region(world, active_locations, LocationName.sunken_ghost_ship_tile, None)
    sunken_ghost_ship_region = create_region(world, active_locations, LocationName.sunken_ghost_ship_region, None)
    sunken_ghost_ship = create_region(world, active_locations, LocationName.sunken_ghost_ship,
                                      [LocationName.sunken_ghost_ship])


    valley_of_bowser_1_tile = create_region(world, active_locations, LocationName.valley_of_bowser_1_tile, None)
    valley_of_bowser_1_region = create_region(world, active_locations, LocationName.valley_of_bowser_1_region, None)
    valley_of_bowser_1_exit_1 = create_region(world, active_locations, LocationName.valley_of_bowser_1_exit_1,
                                              [LocationName.valley_of_bowser_1_exit_1])

    valley_of_bowser_2_tile = create_region(world, active_locations, LocationName.valley_of_bowser_2_tile, None)
    valley_of_bowser_2_region = create_region(world, active_locations, LocationName.valley_of_bowser_2_region, None)
    valley_of_bowser_2_exit_1 = create_region(world, active_locations, LocationName.valley_of_bowser_2_exit_1,
                                              [LocationName.valley_of_bowser_2_exit_1])
    valley_of_bowser_2_exit_2 = create_region(world, active_locations, LocationName.valley_of_bowser_2_exit_2,
                                              [LocationName.valley_of_bowser_2_exit_2])

    valley_of_bowser_3_tile = create_region(world, active_locations, LocationName.valley_of_bowser_3_tile, None)
    valley_of_bowser_3_region = create_region(world, active_locations, LocationName.valley_of_bowser_3_region, None)
    valley_of_bowser_3_exit_1 = create_region(world, active_locations, LocationName.valley_of_bowser_3_exit_1,
                                              [LocationName.valley_of_bowser_3_exit_1])

    valley_of_bowser_4_tile = create_region(world, active_locations, LocationName.valley_of_bowser_4_tile, None)
    valley_of_bowser_4_region = create_region(world, active_locations, LocationName.valley_of_bowser_4_region, None)
    valley_of_bowser_4_exit_1 = create_region(world, active_locations, LocationName.valley_of_bowser_4_exit_1,
                                              [LocationName.valley_of_bowser_4_exit_1])
    valley_of_bowser_4_exit_2 = create_region(world, active_locations, LocationName.valley_of_bowser_4_exit_2,
                                              [LocationName.valley_of_bowser_4_exit_2])

    valley_ghost_house_tile = create_region(world, active_locations, LocationName.valley_ghost_house_tile, None)
    valley_ghost_house_region = create_region(world, active_locations, LocationName.valley_ghost_house_region, None)
    valley_ghost_house_exit_1 = create_region(world, active_locations, LocationName.valley_ghost_house_exit_1,
                                              [LocationName.valley_ghost_house_exit_1])
    valley_ghost_house_exit_2 = create_region(world, active_locations, LocationName.valley_ghost_house_exit_2,
                                              [LocationName.valley_ghost_house_exit_2])

    valley_fortress_tile = create_region(world, active_locations, LocationName.valley_fortress_tile, None)
    valley_fortress_region = create_region(world, active_locations, LocationName.valley_fortress_region, None)
    valley_fortress = create_region(world, active_locations, LocationName.valley_fortress,
                                    [LocationName.valley_fortress])

    valley_castle_tile = create_region(world, active_locations, LocationName.valley_castle_tile, None)
    valley_castle_region = create_region(world, active_locations, LocationName.valley_castle_region, None)
    valley_castle = create_region(world, active_locations, LocationName.valley_castle,
                                  [LocationName.valley_castle])

    front_door_tile = create_region(world, active_locations, LocationName.front_door_tile, None)
    front_door_region = create_region(world, active_locations, LocationName.front_door, None)
    back_door_tile = create_region(world, active_locations, LocationName.back_door_tile, None)
    back_door_region = create_region(world, active_locations, LocationName.back_door, None)
    bowser_region_locations = []
    if world.options.goal == Goal.option_bowser:
        bowser_region_locations += [LocationName.bowser]
    bowser_region = create_region(world, active_locations, LocationName.bowser_region, bowser_region_locations)

    donut_plains_entrance_pipe = create_region(world, active_locations, LocationName.donut_plains_entrance_pipe, None)
    donut_plains_exit_pipe = create_region(world, active_locations, LocationName.donut_plains_exit_pipe, None)
    vanilla_dome_bottom_entrance_pipe = create_region(world, active_locations, LocationName.vanilla_dome_bottom_entrance_pipe, None)
    vanilla_dome_top_entrance_pipe = create_region(world, active_locations, LocationName.vanilla_dome_top_entrance_pipe, None)
    vanilla_dome_top_exit_pipe = create_region(world, active_locations, LocationName.vanilla_dome_top_exit_pipe, None)
    twin_bridges_exit_pipe = create_region(world, active_locations, LocationName.twin_bridges_exit_pipe, None)
    chocolate_island_entrance_pipe = create_region(world, active_locations, LocationName.chocolate_island_entrance_pipe, None)
    chocolate_island_exit_pipe = create_region(world, active_locations, LocationName.chocolate_island_exit_pipe, None)
    valley_donut_entrance_pipe = create_region(world, active_locations, LocationName.valley_donut_entrance_pipe, None)
    valley_donut_exit_pipe = create_region(world, active_locations, LocationName.valley_donut_exit_pipe, None)
    valley_chocolate_entrance_pipe = create_region(world, active_locations, LocationName.valley_chocolate_entrance_pipe, None)
    valley_chocolate_exit_pipe = create_region(world, active_locations, LocationName.valley_chocolate_exit_pipe, None)

    donut_plains_star_road = create_region(world, active_locations, LocationName.donut_plains_star_road, None)
    vanilla_dome_star_road = create_region(world, active_locations, LocationName.vanilla_dome_star_road, None)
    twin_bridges_star_road = create_region(world, active_locations, LocationName.twin_bridges_star_road, None)
    forest_star_road = create_region(world, active_locations, LocationName.forest_star_road, None)
    valley_star_road = create_region(world, active_locations, LocationName.valley_star_road, None)
    star_road_donut = create_region(world, active_locations, LocationName.star_road_donut, None)
    star_road_vanilla = create_region(world, active_locations, LocationName.star_road_vanilla, None)
    star_road_twin_bridges = create_region(world, active_locations, LocationName.star_road_twin_bridges, None)
    star_road_forest = create_region(world, active_locations, LocationName.star_road_forest, None)
    star_road_valley = create_region(world, active_locations, LocationName.star_road_valley, None)
    star_road_special = create_region(world, active_locations, LocationName.star_road_special, None)
    special_star_road = create_region(world, active_locations, LocationName.special_star_road, None)

    star_road_1_tile = create_region(world, active_locations, LocationName.star_road_1_tile, None)
    star_road_1_region = create_region(world, active_locations, LocationName.star_road_1_region, None)
    star_road_1_exit_1 = create_region(world, active_locations, LocationName.star_road_1_exit_1,
                                       [LocationName.star_road_1_exit_1])
    star_road_1_exit_2 = create_region(world, active_locations, LocationName.star_road_1_exit_2,
                                       [LocationName.star_road_1_exit_2])

    star_road_2_tile = create_region(world, active_locations, LocationName.star_road_2_tile, None)
    star_road_2_region = create_region(world, active_locations, LocationName.star_road_2_region, None)
    star_road_2_exit_1 = create_region(world, active_locations, LocationName.star_road_2_exit_1,
                                       [LocationName.star_road_2_exit_1])
    star_road_2_exit_2 = create_region(world, active_locations, LocationName.star_road_2_exit_2,
                                       [LocationName.star_road_2_exit_2])

    star_road_3_tile = create_region(world, active_locations, LocationName.star_road_3_tile, None)
    star_road_3_region = create_region(world, active_locations, LocationName.star_road_3_region, None)
    star_road_3_exit_1 = create_region(world, active_locations, LocationName.star_road_3_exit_1,
                                       [LocationName.star_road_3_exit_1])
    star_road_3_exit_2 = create_region(world, active_locations, LocationName.star_road_3_exit_2,
                                       [LocationName.star_road_3_exit_2])

    star_road_4_tile = create_region(world, active_locations, LocationName.star_road_4_tile, None)
    star_road_4_region = create_region(world, active_locations, LocationName.star_road_4_region, None)
    star_road_4_exit_1 = create_region(world, active_locations, LocationName.star_road_4_exit_1,
                                       [LocationName.star_road_4_exit_1])
    star_road_4_exit_2 = create_region(world, active_locations, LocationName.star_road_4_exit_2,
                                       [LocationName.star_road_4_exit_2])

    star_road_5_tile = create_region(world, active_locations, LocationName.star_road_5_tile, None)
    star_road_5_region = create_region(world, active_locations, LocationName.star_road_5_region, None)
    star_road_5_exit_1 = create_region(world, active_locations, LocationName.star_road_5_exit_1,
                                       [LocationName.star_road_5_exit_1])
    star_road_5_exit_2 = create_region(world, active_locations, LocationName.star_road_5_exit_2,
                                       [LocationName.star_road_5_exit_2])

    special_zone_1_tile = create_region(world, active_locations, LocationName.special_zone_1_tile, None)
    special_zone_1_region = create_region(world, active_locations, LocationName.special_zone_1_region, None)
    special_zone_1_exit_1 = create_region(world, active_locations, LocationName.special_zone_1_exit_1, None)

    special_zone_2_tile = create_region(world, active_locations, LocationName.special_zone_2_tile, None)
    special_zone_2_region = create_region(world, active_locations, LocationName.special_zone_2_region, None)
    special_zone_2_exit_1 = create_region(world, active_locations, LocationName.special_zone_2_exit_1, None)

    special_zone_3_tile = create_region(world, active_locations, LocationName.special_zone_3_tile, None)
    special_zone_3_region = create_region(world, active_locations, LocationName.special_zone_3_region, None)
    special_zone_3_exit_1 = create_region(world, active_locations, LocationName.special_zone_3_exit_1, None)

    special_zone_4_tile = create_region(world, active_locations, LocationName.special_zone_4_tile, None)
    special_zone_4_region = create_region(world, active_locations, LocationName.special_zone_4_region, None)
    special_zone_4_exit_1 = create_region(world, active_locations, LocationName.special_zone_4_exit_1, None)

    special_zone_5_tile = create_region(world, active_locations, LocationName.special_zone_5_tile, None)
    special_zone_5_region = create_region(world, active_locations, LocationName.special_zone_5_region, None)
    special_zone_5_exit_1 = create_region(world, active_locations, LocationName.special_zone_5_exit_1, None)

    special_zone_6_tile = create_region(world, active_locations, LocationName.special_zone_6_tile, None)
    special_zone_6_region = create_region(world, active_locations, LocationName.special_zone_6_region, None)
    special_zone_6_exit_1 = create_region(world, active_locations, LocationName.special_zone_6_exit_1, None)

    special_zone_7_tile = create_region(world, active_locations, LocationName.special_zone_7_tile, None)
    special_zone_7_region = create_region(world, active_locations, LocationName.special_zone_7_region, None)
    special_zone_7_exit_1 = create_region(world, active_locations, LocationName.special_zone_7_exit_1, None)

    special_zone_8_tile = create_region(world, active_locations, LocationName.special_zone_8_tile, None)
    special_zone_8_region = create_region(world, active_locations, LocationName.special_zone_8_region, None)
    special_zone_8_exit_1 = create_region(world, active_locations, LocationName.special_zone_8_exit_1, None)

    special_complete = create_region(world, active_locations, LocationName.special_complete, None)

    yi_to_ysp = create_region(world, active_locations, LocationName.yi_to_ysp, None)
    ysp_from_yi = create_region(world, active_locations, LocationName.ysp_from_yi, None)
    yi_to_dp = create_region(world, active_locations, LocationName.yi_to_dp, None)
    dp_from_yi = create_region(world, active_locations, LocationName.dp_from_yi, None)
    dp_to_vd = create_region(world, active_locations, LocationName.dp_to_vd, None)
    vd_from_dp = create_region(world, active_locations, LocationName.vd_from_dp, None)
    tw_to_foi = create_region(world, active_locations, LocationName.tw_to_foi, None)
    foi_from_tw = create_region(world, active_locations, LocationName.foi_from_tw, None)
    foi_to_ci = create_region(world, active_locations, LocationName.foi_to_ci, None)
    ci_from_foi = create_region(world, active_locations, LocationName.ci_from_foi, None)
    foi_to_sr = create_region(world, active_locations, LocationName.foi_to_sr, None)
    sr_from_foi = create_region(world, active_locations, LocationName.sr_from_foi, None)
    ci_to_vob = create_region(world, active_locations, LocationName.ci_to_vob, None)
    vob_from_ci = create_region(world, active_locations, LocationName.vob_from_ci, None)

    # Set up the regions correctly.
    world.multiworld.regions += [
        menu_region,
        yoshis_island_region,
        yoshis_house_tile,
        yoshis_house_region,
        yoshis_island_1_tile,
        yoshis_island_1_region,
        yoshis_island_1_exit_1,
        yoshis_island_2_tile,
        yoshis_island_2_region,
        yoshis_island_2_exit_1,
        yoshis_island_3_tile,
        yoshis_island_3_region,
        yoshis_island_3_exit_1,
        yoshis_island_4_tile,
        yoshis_island_4_region,
        yoshis_island_4_exit_1,
        yoshis_island_castle_tile,
        yoshis_island_castle_region,
        yoshis_island_castle,
        yellow_switch_palace_tile,
        yellow_switch_palace,
        donut_plains_1_tile,
        donut_plains_1_region,
        donut_plains_1_exit_1,
        donut_plains_1_exit_2,
        donut_plains_2_tile,
        donut_plains_2_region,
        donut_plains_2_exit_1,
        donut_plains_2_exit_2,
        donut_plains_3_tile,
        donut_plains_3_region,
        donut_plains_3_exit_1,
        donut_plains_4_tile,
        donut_plains_4_region,
        donut_plains_4_exit_1,
        donut_secret_1_tile,
        donut_secret_1_region,
        donut_secret_1_exit_1,
        donut_secret_1_exit_2,
        donut_secret_2_tile,
        donut_secret_2_region,
        donut_secret_2_exit_1,
        donut_ghost_house_tile,
        donut_ghost_house_region,
        donut_ghost_house_exit_1,
        donut_ghost_house_exit_2,
        donut_secret_house_tile,
        donut_secret_house_region,
        donut_secret_house_exit_1,
        donut_secret_house_exit_2,
        donut_plains_castle_tile,
        donut_plains_castle_region,
        donut_plains_castle,
        green_switch_palace_tile,
        green_switch_palace,
        donut_plains_top_secret_tile,
        donut_plains_top_secret,
        vanilla_dome_1_tile,
        vanilla_dome_1_region,
        vanilla_dome_1_exit_1,
        vanilla_dome_1_exit_2,
        vanilla_dome_2_tile,
        vanilla_dome_2_region,
        vanilla_dome_2_exit_1,
        vanilla_dome_2_exit_2,
        vanilla_dome_3_tile,
        vanilla_dome_3_region,
        vanilla_dome_3_exit_1,
        vanilla_dome_4_tile,
        vanilla_dome_4_region,
        vanilla_dome_4_exit_1,
        vanilla_secret_1_tile,
        vanilla_secret_1_region,
        vanilla_secret_1_exit_1,
        vanilla_secret_1_exit_2,
        vanilla_secret_2_tile,
        vanilla_secret_2_region,
        vanilla_secret_2_exit_1,
        vanilla_secret_3_tile,
        vanilla_secret_3_region,
        vanilla_secret_3_exit_1,
        vanilla_ghost_house_tile,
        vanilla_ghost_house_region,
        vanilla_ghost_house_exit_1,
        vanilla_fortress_tile,
        vanilla_fortress_region,
        vanilla_fortress,
        vanilla_dome_castle_tile,
        vanilla_dome_castle_region,
        vanilla_dome_castle,
        red_switch_palace_tile,
        red_switch_palace,
        butter_bridge_1_tile,
        butter_bridge_1_region,
        butter_bridge_1_exit_1,
        butter_bridge_2_tile,
        butter_bridge_2_region,
        butter_bridge_2_exit_1,
        cheese_bridge_tile,
        cheese_bridge_region,
        cheese_bridge_exit_1,
        cheese_bridge_exit_2,
        cookie_mountain_tile,
        cookie_mountain_region,
        cookie_mountain_exit_1,
        soda_lake_tile,
        soda_lake_region,
        soda_lake_exit_1,
        twin_bridges_castle_tile,
        twin_bridges_castle_region,
        twin_bridges_castle,
        forest_of_illusion_1_tile,
        forest_of_illusion_1_region,
        forest_of_illusion_1_exit_1,
        forest_of_illusion_1_exit_2,
        forest_of_illusion_2_tile,
        forest_of_illusion_2_region,
        forest_of_illusion_2_exit_1,
        forest_of_illusion_2_exit_2,
        forest_of_illusion_3_tile,
        forest_of_illusion_3_region,
        forest_of_illusion_3_exit_1,
        forest_of_illusion_3_exit_2,
        forest_of_illusion_4_tile,
        forest_of_illusion_4_region,
        forest_of_illusion_4_exit_1,
        forest_of_illusion_4_exit_2,
        forest_ghost_house_tile,
        forest_ghost_house_region,
        forest_ghost_house_exit_1,
        forest_ghost_house_exit_2,
        forest_secret_tile,
        forest_secret_region,
        forest_secret_exit_1,
        forest_fortress_tile,
        forest_fortress_region,
        forest_fortress,
        forest_castle_tile,
        forest_castle_region,
        forest_castle,
        blue_switch_palace_tile,
        blue_switch_palace,
        chocolate_island_1_tile,
        chocolate_island_1_region,
        chocolate_island_1_exit_1,
        chocolate_island_2_tile,
        chocolate_island_2_region,
        chocolate_island_2_exit_1,
        chocolate_island_2_exit_2,
        chocolate_island_3_tile,
        chocolate_island_3_region,
        chocolate_island_3_exit_1,
        chocolate_island_3_exit_2,
        chocolate_island_4_tile,
        chocolate_island_4_region,
        chocolate_island_4_exit_1,
        chocolate_island_5_tile,
        chocolate_island_5_region,
        chocolate_island_5_exit_1,
        chocolate_ghost_house_tile,
        chocolate_ghost_house_region,
        chocolate_ghost_house_exit_1,
        chocolate_secret_tile,
        chocolate_secret_region,
        chocolate_secret_exit_1,
        chocolate_fortress_tile,
        chocolate_fortress_region,
        chocolate_fortress,
        chocolate_castle_tile,
        chocolate_castle_region,
        chocolate_castle,
        sunken_ghost_ship_tile,
        sunken_ghost_ship_region,
        sunken_ghost_ship,
        valley_of_bowser_1_tile,
        valley_of_bowser_1_region,
        valley_of_bowser_1_exit_1,
        valley_of_bowser_2_tile,
        valley_of_bowser_2_region,
        valley_of_bowser_2_exit_1,
        valley_of_bowser_2_exit_2,
        valley_of_bowser_3_tile,
        valley_of_bowser_3_region,
        valley_of_bowser_3_exit_1,
        valley_of_bowser_4_tile,
        valley_of_bowser_4_region,
        valley_of_bowser_4_exit_1,
        valley_of_bowser_4_exit_2,
        valley_ghost_house_tile,
        valley_ghost_house_region,
        valley_ghost_house_exit_1,
        valley_ghost_house_exit_2,
        valley_fortress_tile,
        valley_fortress_region,
        valley_fortress,
        valley_castle_tile,
        valley_castle_region,
        valley_castle,
        front_door_tile,
        front_door_region,
        back_door_tile,
        back_door_region,
        bowser_region,
        donut_plains_entrance_pipe,
        donut_plains_exit_pipe,
        vanilla_dome_bottom_entrance_pipe,
        vanilla_dome_top_entrance_pipe,
        vanilla_dome_top_exit_pipe,
        twin_bridges_exit_pipe,
        chocolate_island_entrance_pipe,
        chocolate_island_exit_pipe,
        valley_donut_entrance_pipe,
        valley_donut_exit_pipe,
        valley_chocolate_entrance_pipe,
        valley_chocolate_exit_pipe,
        donut_plains_star_road,
        vanilla_dome_star_road,
        twin_bridges_star_road,
        forest_star_road,
        valley_star_road,
        star_road_donut,
        star_road_vanilla,
        star_road_twin_bridges,
        star_road_forest,
        star_road_valley,
        star_road_special,
        special_star_road,
        star_road_1_tile,
        star_road_1_region,
        star_road_1_exit_1,
        star_road_1_exit_2,
        star_road_2_tile,
        star_road_2_region,
        star_road_2_exit_1,
        star_road_2_exit_2,
        star_road_3_tile,
        star_road_3_region,
        star_road_3_exit_1,
        star_road_3_exit_2,
        star_road_4_tile,
        star_road_4_region,
        star_road_4_exit_1,
        star_road_4_exit_2,
        star_road_5_tile,
        star_road_5_region,
        star_road_5_exit_1,
        star_road_5_exit_2,
        special_zone_1_tile,
        special_zone_1_region,
        special_zone_1_exit_1,
        special_zone_2_tile,
        special_zone_2_region,
        special_zone_2_exit_1,
        special_zone_3_tile,
        special_zone_3_region,
        special_zone_3_exit_1,
        special_zone_4_tile,
        special_zone_4_region,
        special_zone_4_exit_1,
        special_zone_5_tile,
        special_zone_5_region,
        special_zone_5_exit_1,
        special_zone_6_tile,
        special_zone_6_region,
        special_zone_6_exit_1,
        special_zone_7_tile,
        special_zone_7_region,
        special_zone_7_exit_1,
        special_zone_8_tile,
        special_zone_8_region,
        special_zone_8_exit_1,
        special_complete,
        yi_to_ysp,
        ysp_from_yi,
        yi_to_dp,
        dp_from_yi,
        dp_to_vd,
        vd_from_dp,
        tw_to_foi,
        foi_from_tw,
        foi_to_ci,
        ci_from_foi,
        foi_to_sr,
        sr_from_foi,
        ci_to_vob,
        vob_from_ci,
    ]

    add_location_to_region(world, active_locations, LocationName.special_zone_1_exit_1, LocationName.special_zone_1_exit_1)
    add_location_to_region(world, active_locations, LocationName.special_zone_2_exit_1, LocationName.special_zone_2_exit_1)
    add_location_to_region(world, active_locations, LocationName.special_zone_3_exit_1, LocationName.special_zone_3_exit_1)
    add_location_to_region(world, active_locations, LocationName.special_zone_4_exit_1, LocationName.special_zone_4_exit_1)
    add_location_to_region(world, active_locations, LocationName.special_zone_5_exit_1, LocationName.special_zone_5_exit_1)
    add_location_to_region(world, active_locations, LocationName.special_zone_6_exit_1, LocationName.special_zone_6_exit_1)
    add_location_to_region(world, active_locations, LocationName.special_zone_7_exit_1, LocationName.special_zone_7_exit_1)
    add_location_to_region(world, active_locations, LocationName.special_zone_8_exit_1, LocationName.special_zone_8_exit_1)

    if world.options.dragon_coin_checks:
        add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_dragon)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_dragon)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_dragon)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_dragon)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_dragon)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_dragon)
        add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_dragon)
        add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_dragon)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_dragon)
        add_location_to_region(world, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_dragon)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_dragon)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_dragon)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_dragon)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_dragon)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_dragon)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_dragon)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_dragon)
        add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_dragon)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_dragon)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_dragon)
        add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_dragon)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_dragon)
        add_location_to_region(world, active_locations, LocationName.soda_lake_region, LocationName.soda_lake_dragon)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_dragon)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_dragon)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_dragon)
        add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_dragon)
        add_location_to_region(world, active_locations, LocationName.forest_secret_region, LocationName.forest_secret_dragon)
        add_location_to_region(world, active_locations, LocationName.forest_castle_region, LocationName.forest_castle_dragon)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_dragon)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_dragon)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_dragon)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_dragon)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_dragon)
        add_location_to_region(world, active_locations, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship_dragon)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_dragon)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_dragon)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_dragon)
        add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_dragon)
        add_location_to_region(world, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_dragon)
        add_location_to_region(world, active_locations, LocationName.star_road_1_region, LocationName.star_road_1_dragon)

        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_dragon)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_dragon)
        add_location_to_region(world, active_locations, LocationName.special_zone_3_region, LocationName.special_zone_3_dragon)
        add_location_to_region(world, active_locations, LocationName.special_zone_4_region, LocationName.special_zone_4_dragon)
        add_location_to_region(world, active_locations, LocationName.special_zone_5_region, LocationName.special_zone_5_dragon)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_dragon)
        add_location_to_region(world, active_locations, LocationName.special_zone_7_region, LocationName.special_zone_7_dragon)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_dragon)

    if world.options.moon_checks:
        add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_moon)
        add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_moon)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_moon)
        add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_moon)
        add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_moon)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_moon)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_moon)

    if world.options.hidden_1up_checks:
        add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.vanilla_fortress_region, LocationName.vanilla_fortress_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.chocolate_castle_region, LocationName.chocolate_castle_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_hidden_1up)
        add_location_to_region(world, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_hidden_1up)
        
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_hidden_1up)
        
    if world.options.star_block_checks:
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_prize)
        add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_prize)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_prize)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_prize)

    if world.options.midway_point_checks:
        add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_midway)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_midway)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_midway)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_midway)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_midway)
        add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_midway)
        add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_midway)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_midway)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_midway)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_midway)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_midway)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_midway)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_midway)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_midway)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_midway)
        add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_midway)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_midway)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_midway)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_midway)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_midway)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_midway)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_midway)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_midway)
        add_location_to_region(world, active_locations, LocationName.chocolate_secret_region, LocationName.chocolate_secret_midway)
        add_location_to_region(world, active_locations, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress_midway)
        add_location_to_region(world, active_locations, LocationName.chocolate_castle_region, LocationName.chocolate_castle_midway)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_midway)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_midway)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_midway)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_midway)
        add_location_to_region(world, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_midway)

    if world.options.room_checks:
         add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_room_1)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_room_2)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_room_1)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_room_2)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_room_1)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_room_2)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_room_1)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_room_2)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_room_3)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_room_1)
         add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_room_2)
         add_location_to_region(world, active_locations, LocationName.yellow_switch_palace, LocationName.yellow_switch_palace_room_1)
         add_location_to_region(world, active_locations, LocationName.yellow_switch_palace, LocationName.yellow_switch_palace_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_room_3)
         add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_room_3)
         add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_room_3)
         add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_room_3)
         add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_room_4)
         add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_room_5)
         add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_room_6)
         add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_room_3)
         add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_room_4)
         add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_room_5)
         add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_room_1)
         add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_room_2)
         add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_room_3)
         add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_room_4)
         add_location_to_region(world, active_locations, LocationName.green_switch_palace, LocationName.green_switch_palace_room_1)
         add_location_to_region(world, active_locations, LocationName.green_switch_palace, LocationName.green_switch_palace_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_room_3)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_room_3)
         add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_room_3)
         add_location_to_region(world, active_locations, LocationName.vanilla_fortress_region, LocationName.vanilla_fortress_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_fortress_region, LocationName.vanilla_fortress_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_room_1)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_room_2)
         add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_room_3)
         add_location_to_region(world, active_locations, LocationName.red_switch_palace, LocationName.red_switch_palace_room_1)
         add_location_to_region(world, active_locations, LocationName.red_switch_palace, LocationName.red_switch_palace_room_2)
         add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_room_1)
         add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_room_2)
         add_location_to_region(world, active_locations, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_room_1)
         add_location_to_region(world, active_locations, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_room_2)
         add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_room_1)
         add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_room_2)
         add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_room_3)
         add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_room_1)
         add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_room_2)
         add_location_to_region(world, active_locations, LocationName.soda_lake_region, LocationName.soda_lake_room_1)
         add_location_to_region(world, active_locations, LocationName.soda_lake_region, LocationName.soda_lake_room_2)
         add_location_to_region(world, active_locations, LocationName.twin_bridges_castle_region, LocationName.twin_bridges_castle_room_1)
         add_location_to_region(world, active_locations, LocationName.twin_bridges_castle_region, LocationName.twin_bridges_castle_room_2)
         add_location_to_region(world, active_locations, LocationName.twin_bridges_castle_region, LocationName.twin_bridges_castle_room_3)
         add_location_to_region(world, active_locations, LocationName.twin_bridges_castle_region, LocationName.twin_bridges_castle_room_4)
         add_location_to_region(world, active_locations, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_room_1)
         add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_room_1)
         add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_room_1)
         add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_room_2)
         add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_room_3)
         add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_room_1)
         add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_room_2)
         add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_room_3)
         add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_room_1)
         add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_room_2)
         add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_room_3)
         add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_room_4)
         add_location_to_region(world, active_locations, LocationName.forest_secret_region, LocationName.forest_secret_room_1)
         add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_room_1)
         add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_room_2)
         add_location_to_region(world, active_locations, LocationName.forest_castle_region, LocationName.forest_castle_room_1)
         add_location_to_region(world, active_locations, LocationName.blue_switch_palace, LocationName.blue_switch_palace_room_1)
         add_location_to_region(world, active_locations, LocationName.blue_switch_palace, LocationName.blue_switch_palace_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_room_3)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_room_4)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_room_3)
         add_location_to_region(world, active_locations, LocationName.chocolate_ghost_house_region, LocationName.chocolate_ghost_house_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_ghost_house_region, LocationName.chocolate_ghost_house_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_ghost_house_region, LocationName.chocolate_ghost_house_room_3)
         add_location_to_region(world, active_locations, LocationName.chocolate_secret_region, LocationName.chocolate_secret_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_secret_region, LocationName.chocolate_secret_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_secret_region, LocationName.chocolate_secret_room_3)
         add_location_to_region(world, active_locations, LocationName.chocolate_secret_region, LocationName.chocolate_secret_room_4)
         add_location_to_region(world, active_locations, LocationName.chocolate_secret_region, LocationName.chocolate_secret_room_5)
         add_location_to_region(world, active_locations, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress_room_2)
         add_location_to_region(world, active_locations, LocationName.chocolate_castle_region, LocationName.chocolate_castle_room_1)
         add_location_to_region(world, active_locations, LocationName.chocolate_castle_region, LocationName.chocolate_castle_room_2)
         add_location_to_region(world, active_locations, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship_room_1)
         add_location_to_region(world, active_locations, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship_room_2)
         add_location_to_region(world, active_locations, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship_room_3)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_room_1)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_room_2)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_room_3)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_room_1)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_room_2)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_room_3)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_room_1)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_room_2)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_room_1)
         add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_room_2)
         add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_room_1)
         add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_room_2)
         add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_room_3)
         add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_room_4)
         add_location_to_region(world, active_locations, LocationName.valley_fortress_region, LocationName.valley_fortress_room_1)
         add_location_to_region(world, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_room_1)
         add_location_to_region(world, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_room_2)
         add_location_to_region(world, active_locations, LocationName.star_road_1_region, LocationName.star_road_1_room_1)
         add_location_to_region(world, active_locations, LocationName.star_road_1_region, LocationName.star_road_1_room_2)
         add_location_to_region(world, active_locations, LocationName.star_road_2_region, LocationName.star_road_2_room_1)
         add_location_to_region(world, active_locations, LocationName.star_road_2_region, LocationName.star_road_2_room_2)
         add_location_to_region(world, active_locations, LocationName.star_road_3_region, LocationName.star_road_3_room_1)
         add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_room_1)
         add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_room_1)
         add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_room_1)
         add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_room_2)
         add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_room_1)
         add_location_to_region(world, active_locations, LocationName.special_zone_3_region, LocationName.special_zone_3_room_1)
         add_location_to_region(world, active_locations, LocationName.special_zone_3_region, LocationName.special_zone_3_room_2)
         add_location_to_region(world, active_locations, LocationName.special_zone_3_region, LocationName.special_zone_3_room_3)
         add_location_to_region(world, active_locations, LocationName.special_zone_4_region, LocationName.special_zone_4_room_1)
         add_location_to_region(world, active_locations, LocationName.special_zone_5_region, LocationName.special_zone_5_room_1)
         add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_room_1)
         add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_room_2)
         add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_room_3)
         add_location_to_region(world, active_locations, LocationName.special_zone_7_region, LocationName.special_zone_7_room_1)
         add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_room_1)


    if "Yellow Switch Palace Blocks" in world.options.block_checks.value:
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_fortress_region, LocationName.vanilla_fortress_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_yellow_block_3)
        add_location_to_region(world, active_locations, LocationName.chocolate_castle_region, LocationName.chocolate_castle_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_castle_region, LocationName.chocolate_castle_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_3)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_4)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_5)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_6)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_7)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_8)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_9)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_10)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_11)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_12)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_13)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_14)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_15)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_16)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_17)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_18)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_19)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_20)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_21)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_22)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_23)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_24)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_25)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_26)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_27)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_28)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_29)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_30)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_31)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_32)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_33)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_34)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_35)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_36)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_37)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_38)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_39)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_40)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_41)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_42)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_43)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_44)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_45)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_46)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_47)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_48)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_49)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_50)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_51)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_52)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_53)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_54)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_55)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_56)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_57)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_58)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_59)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_60)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_61)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_62)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_63)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_64)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_65)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_66)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_67)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_68)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_69)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_70)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_71)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_72)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_73)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_74)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_75)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_76)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_77)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_78)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_79)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_80)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_81)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_82)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_83)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_84)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_85)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yellow_block_86)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.valley_fortress_region, LocationName.valley_fortress_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_yellow_block_3)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_yellow_block_4)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_2)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_3)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_4)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_5)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_6)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_7)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_8)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_9)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_10)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_11)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_12)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_13)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_14)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_15)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_16)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_17)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_18)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_19)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_yellow_block_20)


    if "Green Switch Palace Blocks" in world.options.block_checks.value:
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_green_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_green_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_green_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_green_block_1)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_green_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_3)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_4)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_5)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_6)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_7)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_8)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_9)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_10)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_11)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_12)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_13)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_14)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_15)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_green_block_16)
        add_location_to_region(world, active_locations, LocationName.chocolate_castle_region, LocationName.chocolate_castle_green_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress_green_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_castle_region, LocationName.forest_castle_green_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_green_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_green_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_green_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_green_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_green_block_3)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_green_block_4)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_green_block_5)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_green_block_6)
        add_location_to_region(world, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_green_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_fortress_region, LocationName.valley_fortress_green_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_green_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_green_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_green_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_green_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_green_block_2)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_green_block_3)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_green_block_4)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_green_block_5)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_green_block_6)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_green_block_7)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_2)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_3)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_4)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_5)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_6)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_7)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_8)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_9)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_10)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_11)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_12)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_13)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_14)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_15)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_16)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_17)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_18)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_19)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_green_block_20)


    if "P-Switch Blocks" in world.options.block_checks.value:
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_pswitch_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_pswitch_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_pswitch_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_pswitch_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_pswitch_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_pswitch_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_pswitch_coin_block_1)

        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_7)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_8)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_9)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_10)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_11)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_12)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_pswitch_coin_block_13)


    if "Flying Blocks" in world.options.block_checks.value:
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_flying_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_flying_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_flying_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_flying_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_flying_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_flying_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_flying_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_flying_block_3)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_flying_block_4)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_flying_block_5)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_flying_block_6)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_flying_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_flying_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_flying_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_flying_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_flying_block_1)

        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_flying_block_1)


    if "Invisible Blocks" in world.options.block_checks.value:
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_invis_life_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_invis_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_invis_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_invis_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_invis_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_invis_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_invis_life_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_invis_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_invis_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_invis_life_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_invis_coin_block_3)


    if "Coin Blocks" in world.options.block_checks.value:
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_multi_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_multi_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_7)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_8)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_9)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_10)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_11)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_12)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_13)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_14)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_15)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_16)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_17)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_18)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_19)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_20)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_21)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_22)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_23)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_24)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_25)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_26)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_27)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_28)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_29)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_coin_block_30)
        add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_multi_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_multi_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_coin_block_7)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_coin_block_8)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_7)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_8)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_9)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_coin_block_10)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_multi_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_7)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_8)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_9)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_10)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_11)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_12)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_13)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_14)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_15)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_16)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_17)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_18)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_19)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_20)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_21)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_22)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_23)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_coin_block_24)

        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_7)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_8)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_9)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_10)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_11)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_12)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_13)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_14)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_15)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_16)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_17)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_18)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_19)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_20)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_21)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_22)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_coin_block_23)
        add_location_to_region(world, active_locations, LocationName.special_zone_7_region, LocationName.special_zone_7_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_7_region, LocationName.special_zone_7_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_6)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_7)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_8)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_9)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_10)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_11)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_12)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_13)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_14)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_15)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_16)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_17)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_18)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_19)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_20)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_21)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_22)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_23)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_24)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_25)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_26)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_27)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_28)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_29)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_30)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_31)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_32)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_coin_block_33)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_coin_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_coin_block_3)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_coin_block_4)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_multi_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_coin_block_5)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_coin_block_6)


    if "Item Blocks" in world.options.block_checks.value:
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_gray_pow_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_directional_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_life_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_life_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_life_block_3)
        add_location_to_region(world, active_locations, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_life_block_4)
        add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_powerup_block_3)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_life_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_powerup_block_4)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_powerup_block_5)
        add_location_to_region(world, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_key_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_fortress_region, LocationName.vanilla_fortress_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_fortress_region, LocationName.vanilla_fortress_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_life_block_1)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.twin_bridges_castle_region, LocationName.twin_bridges_castle_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_wings_block_1)
        add_location_to_region(world, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_powerup_block_3)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_life_block_1)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.soda_lake_region, LocationName.soda_lake_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_life_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_house_region, LocationName.donut_secret_house_directional_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship_star_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_life_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_blue_pow_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_3)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_4)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_5)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_6)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_7)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_8)
        add_location_to_region(world, active_locations, LocationName.forest_fortress_region, LocationName.forest_fortress_life_block_9)
        add_location_to_region(world, active_locations, LocationName.chocolate_ghost_house_region, LocationName.chocolate_ghost_house_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_ghost_house_region, LocationName.chocolate_ghost_house_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_ghost_house_region, LocationName.chocolate_ghost_house_life_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_life_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_powerup_block_3)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_life_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_life_block_2)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_life_block_3)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_blue_pow_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_star_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_life_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_yoshi_block_2)
        add_location_to_region(world, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_blue_pow_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_vine_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_powerup_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_powerup_block_4)
        add_location_to_region(world, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_directional_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_star_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_star_block_2)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_life_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_directional_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_wings_block_1)
        add_location_to_region(world, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_secret_region, LocationName.chocolate_secret_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.chocolate_secret_region, LocationName.chocolate_secret_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_powerup_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_powerup_block_4)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_powerup_block_5)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_life_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_life_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_powerup_block_3)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_star_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_powerup_block_4)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_life_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_life_block_2)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle_life_block_3)
        add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_life_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_key_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_life_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_secret_region, LocationName.forest_secret_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_secret_region, LocationName.forest_secret_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.forest_secret_region, LocationName.forest_secret_life_block_1)
        add_location_to_region(world, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_2_region, LocationName.star_road_2_star_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_3_region, LocationName.star_road_3_key_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_4_region, LocationName.star_road_4_key_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_directional_coin_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_life_block_1)
        add_location_to_region(world, active_locations, LocationName.star_road_5_region, LocationName.star_road_5_vine_block_1)
        
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_blue_pow_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_star_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_7_region, LocationName.special_zone_7_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_7_region, LocationName.special_zone_7_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_7_region, LocationName.special_zone_7_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_life_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_5_region, LocationName.special_zone_5_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_vine_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_vine_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_vine_block_3)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_vine_block_4)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_life_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_vine_block_5)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_blue_pow_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_vine_block_6)
        add_location_to_region(world, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_powerup_block_2)
        add_location_to_region(world, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_powerup_block_3)
        add_location_to_region(world, active_locations, LocationName.special_zone_3_region, LocationName.special_zone_3_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_3_region, LocationName.special_zone_3_yoshi_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_3_region, LocationName.special_zone_3_wings_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_4_region, LocationName.special_zone_4_powerup_block_1)
        add_location_to_region(world, active_locations, LocationName.special_zone_4_region, LocationName.special_zone_4_star_block_1)

def connect_regions(world: "WaffleWorld", level_to_tile_dict):
    #connect(world, "Menu", LocationName.yoshis_island_region)
    possible_starting_regions = [
        LocationName.yoshis_island_region,
        LocationName.donut_plains_1_tile,
        LocationName.vanilla_dome_1_tile,
        LocationName.forest_of_illusion_1_tile,
        LocationName.special_zone_1_tile,
    ]
    connect(world, "Menu", possible_starting_regions[world.options.starting_location.value])

    # Connect starting locations both ways
    connect(world, LocationName.yoshis_house_tile, LocationName.yoshis_island_region)

    connect(world, LocationName.yoshis_island_region, LocationName.yoshis_house_tile)
    connect(world, LocationName.yoshis_island_region, LocationName.yoshis_island_1_tile)
    connect(world, LocationName.yoshis_island_region, LocationName.yoshis_island_2_tile)

    connect(world, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_exit_1)
    connect(world, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_exit_1)
    connect(world, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_exit_1)
    connect(world, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_exit_1)
    connect(world, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle)

    connect(world, LocationName.donut_plains_1_region, LocationName.donut_plains_1_exit_1)
    connect(world, LocationName.donut_plains_1_region, LocationName.donut_plains_1_exit_2)
    connect(world, LocationName.donut_plains_2_region, LocationName.donut_plains_2_exit_1)
    connect(world, LocationName.donut_plains_2_region, LocationName.donut_plains_2_exit_2)
    connect(world, LocationName.donut_secret_1_region, LocationName.donut_secret_1_exit_1)
    connect(world, LocationName.donut_secret_1_region, LocationName.donut_secret_1_exit_2)
    connect(world, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_exit_1)
    connect(world, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_exit_2)
    connect(world, LocationName.donut_secret_house_region, LocationName.donut_secret_house_exit_1)
    connect(world, LocationName.donut_secret_house_region, LocationName.donut_secret_house_exit_2)
    connect(world, LocationName.donut_plains_3_region, LocationName.donut_plains_3_exit_1)
    connect(world, LocationName.donut_plains_4_region, LocationName.donut_plains_4_exit_1)
    connect(world, LocationName.donut_secret_2_region, LocationName.donut_secret_2_exit_1)
    connect(world, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle)
    
    connect(world, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_exit_1)
    connect(world, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_exit_2)
    connect(world, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_exit_1)
    connect(world, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_exit_2)
    connect(world, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_exit_1)
    connect(world, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_exit_2)
    connect(world, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_exit_1)
    connect(world, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_exit_1)
    connect(world, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_exit_1)
    connect(world, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_exit_1)
    connect(world, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_exit_1)
    connect(world, LocationName.vanilla_fortress_region, LocationName.vanilla_fortress)
    connect(world, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle)
    
    connect(world, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_exit_1)
    connect(world, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_exit_1)
    connect(world, LocationName.cheese_bridge_region, LocationName.cheese_bridge_exit_1)
    connect(world, LocationName.cheese_bridge_region, LocationName.cheese_bridge_exit_2)
    connect(world, LocationName.soda_lake_region, LocationName.soda_lake_exit_1)
    connect(world, LocationName.cookie_mountain_region, LocationName.cookie_mountain_exit_1)
    connect(world, LocationName.twin_bridges_castle_region, LocationName.twin_bridges_castle)
                           
    connect(world, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_exit_1)
    connect(world, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_exit_2)
    connect(world, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_exit_1)
    connect(world, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_exit_2)
    connect(world, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_exit_1)
    connect(world, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_exit_2)
    connect(world, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_exit_1)
    connect(world, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_exit_2)
    connect(world, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_exit_1)
    connect(world, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_exit_2)
    connect(world, LocationName.forest_secret_region, LocationName.forest_secret_exit_1)
    connect(world, LocationName.forest_fortress_region, LocationName.forest_fortress)
    connect(world, LocationName.forest_castle_region, LocationName.forest_castle)
    
    connect(world, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_exit_1)
    connect(world, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_exit_1)
    connect(world, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_exit_2)
    connect(world, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_exit_1)
    connect(world, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_exit_2)
    connect(world, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_exit_1)
    connect(world, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_exit_1)
    connect(world, LocationName.chocolate_ghost_house_region, LocationName.chocolate_ghost_house_exit_1)
    connect(world, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress)
    connect(world, LocationName.chocolate_secret_region, LocationName.chocolate_secret_exit_1)
    connect(world, LocationName.chocolate_castle_region, LocationName.chocolate_castle)
            
    connect(world, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship)
    connect(world, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_exit_1)
    connect(world, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_exit_1)
    connect(world, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_exit_2)
    connect(world, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_exit_1)
    connect(world, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_exit_1)
    connect(world, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_exit_2)
    connect(world, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_exit_1)
    connect(world, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_exit_2)
    connect(world, LocationName.valley_fortress_region, LocationName.valley_fortress)
    connect(world, LocationName.valley_castle_region, LocationName.valley_castle)
    connect(world, LocationName.front_door, LocationName.bowser_region)
    connect(world, LocationName.back_door, LocationName.bowser_region)

    connect(world, LocationName.star_road_1_region, LocationName.star_road_1_exit_1)
    connect(world, LocationName.star_road_1_region, LocationName.star_road_1_exit_2)
    connect(world, LocationName.star_road_2_region, LocationName.star_road_2_exit_1)
    connect(world, LocationName.star_road_2_region, LocationName.star_road_2_exit_2)
    connect(world, LocationName.star_road_3_region, LocationName.star_road_3_exit_1)
    connect(world, LocationName.star_road_3_region, LocationName.star_road_3_exit_2)
    connect(world, LocationName.star_road_4_region, LocationName.star_road_4_exit_1)
    connect(world, LocationName.star_road_4_region, LocationName.star_road_4_exit_2)
    connect(world, LocationName.star_road_5_region, LocationName.star_road_5_exit_1)
    connect(world, LocationName.star_road_5_region, LocationName.star_road_5_exit_2)

    connect(world, LocationName.special_zone_1_region, LocationName.special_zone_1_exit_1)
    connect(world, LocationName.special_zone_2_region, LocationName.special_zone_2_exit_1)
    connect(world, LocationName.special_zone_3_region, LocationName.special_zone_3_exit_1)
    connect(world, LocationName.special_zone_4_region, LocationName.special_zone_4_exit_1)
    connect(world, LocationName.special_zone_5_region, LocationName.special_zone_5_exit_1)
    connect(world, LocationName.special_zone_6_region, LocationName.special_zone_6_exit_1)
    connect(world, LocationName.special_zone_7_region, LocationName.special_zone_7_exit_1)
    connect(world, LocationName.special_zone_8_region, LocationName.special_zone_8_exit_1)

    # Connect levels to each other
    should_cache = [
        LocationName.star_road_1_tile,
        LocationName.star_road_2_tile,
        LocationName.star_road_3_tile,
        LocationName.star_road_4_tile,
    ]
    future_star_cache = dict()

    for current_level_id, current_level_data in level_info_dict.items():
        # Connect tile regions to correct level regions
        adjust_exit = False

        if current_level_id not in level_to_tile_dict.keys():
            continue

        current_tile_id = level_to_tile_dict[current_level_id]
        current_tile_data = level_info_dict[current_tile_id]
        current_tile_name = current_tile_data.levelName

        if ("Star World - " not in current_tile_name) and (" - Star World" not in current_tile_name) and ("Pipe" not in current_tile_name) and ("Transition - " not in current_tile_name):
            current_tile_name += " - Tile"
            connect(world, current_tile_name, current_level_data.levelName)
        # Connect Exit regions to next tile regions
        if current_tile_data.exit1Path:
            next_tile_id = current_tile_data.exit1Path.otherLevelID
            if current_tile_id in world.swapped_exits:
                next_tile_id = current_tile_data.exit2Path.otherLevelID
                adjust_exit = True
            next_tile_name = level_info_dict[next_tile_id].levelName
            if ("Star World - " not in next_tile_name) and (" - Star World" not in next_tile_name) and ("Pipe" not in next_tile_name) and ("Transition - " not in next_tile_name):
                next_tile_name += " - Tile"
            else:
                if current_tile_name == LocationName.star_road_5_tile:
                    future_star_cache[next_tile_name] = current_tile_data.eventIDValue
                else:
                    if adjust_exit:
                        world.cached_connections[next_tile_name] = current_tile_data.eventIDValue + 1
                    else:
                        world.cached_connections[next_tile_name] = current_tile_data.eventIDValue
            if adjust_exit:
                current_exit_name = (current_level_data.levelName + " - Secret Exit")
            else:
                current_exit_name = (current_level_data.levelName + " - Normal Exit")
            connect(world, current_exit_name, next_tile_name)
            
        if current_tile_data.exit2Path:
            next_tile_id = current_tile_data.exit2Path.otherLevelID
            if current_tile_id in world.swapped_exits:
                try:
                    next_tile_id = current_tile_data.exit1Path.otherLevelID
                    adjust_exit = True
                except AttributeError:
                    pass
            next_tile_name = level_info_dict[next_tile_id].levelName
            if ("Star World - " not in next_tile_name) and (" - Star World" not in next_tile_name) and ("Pipe" not in next_tile_name) and ("Transition - " not in next_tile_name):
                next_tile_name += " - Tile"
            else:
                if current_tile_name in should_cache:
                    future_star_cache[next_tile_name] = current_tile_data.eventIDValue + 1
                else:
                    if adjust_exit:
                        world.cached_connections[next_tile_name] = current_tile_data.eventIDValue
                    else:
                        world.cached_connections[next_tile_name] = current_tile_data.eventIDValue + 1
            if adjust_exit:
                current_exit_name = (current_level_data.levelName + " - Normal Exit")
            else:
                current_exit_name = (current_level_data.levelName + " - Secret Exit")
            connect(world, current_exit_name, next_tile_name)

    # Fix cached connections
    for old_exit, event_id in future_star_cache.items():
        entrance = world.reverse_teleport_pairs[old_exit]
        world.cached_connections[entrance] = event_id

    # Connect teleport destination tiles with level tiles
    connect(world, LocationName.star_road_donut, LocationName.star_road_1_tile)
    connect(world, LocationName.star_road_vanilla, LocationName.star_road_2_tile)
    connect(world, LocationName.star_road_twin_bridges, LocationName.star_road_3_tile)
    connect(world, LocationName.star_road_forest, LocationName.star_road_4_tile)
    connect(world, LocationName.star_road_valley, LocationName.star_road_5_tile)
    connect(world, LocationName.special_star_road, LocationName.special_zone_1_tile)
    connect(world, LocationName.donut_plains_exit_pipe, LocationName.donut_plains_3_tile)
    connect(world, LocationName.valley_donut_exit_pipe, LocationName.donut_secret_2_tile)
    connect(world, LocationName.vanilla_dome_top_exit_pipe, LocationName.vanilla_secret_2_tile)
    connect(world, LocationName.twin_bridges_exit_pipe, LocationName.cheese_bridge_tile)
    connect(world, LocationName.valley_chocolate_exit_pipe, LocationName.chocolate_secret_tile)
    connect(world, LocationName.chocolate_island_exit_pipe, LocationName.chocolate_castle_tile)

    # Connect teleports
    for entrance, exit in world.teleport_pairs.items():
        connect(world, entrance, exit)
        if exit != LocationName.yoshis_house_tile:
            connect(world, exit, entrance)

    # Connect transition destination "tiles" with level tiles
    connect(world, LocationName.ysp_from_yi, LocationName.yellow_switch_palace_tile)
    connect(world, LocationName.dp_from_yi, LocationName.donut_plains_1_tile)
    connect(world, LocationName.vd_from_dp, LocationName.vanilla_dome_1_tile)
    connect(world, LocationName.foi_from_tw, LocationName.forest_of_illusion_1_tile)
    connect(world, LocationName.ci_from_foi, LocationName.forest_castle_tile)
    connect(world, LocationName.sr_from_foi, LocationName.forest_fortress_tile)
    connect(world, LocationName.vob_from_ci, LocationName.valley_of_bowser_1_tile)

    # Connect transitions
    for entrance, exit in world.transition_pairs.items():
        connect(world, entrance, exit)

    # Connect potential yoshi findings if applicable
    if not world.options.inventory_yoshi_logic:
        connect_blue_yoshi_levels(world, f"{LocationName.star_road_4_region} -> {LocationName.star_road_4_exit_2}")
        connect_blue_yoshi_levels(world, f"{LocationName.star_road_5_region} -> {LocationName.star_road_5_exit_1}")
        connect_blue_yoshi_levels(world, f"{LocationName.star_road_5_region} -> {LocationName.star_road_5_exit_2}")
        connect_blue_yoshi_levels(world, f"{LocationName.chocolate_island_3_region} -> {LocationName.chocolate_island_3_exit_2}")

        connect_green_yoshi_levels(world, f"{LocationName.donut_plains_1_region} -> {LocationName.donut_plains_1_exit_2}")
        connect_green_yoshi_levels(world, f"{LocationName.donut_plains_2_region} -> {LocationName.donut_plains_2_exit_2}")
        connect_green_yoshi_levels(world, f"{LocationName.vanilla_dome_1_region} -> {LocationName.vanilla_dome_1_exit_2}")
        connect_green_yoshi_levels(world, f"{LocationName.vanilla_dome_2_region} -> {LocationName.vanilla_dome_2_exit_1}")
        connect_green_yoshi_levels(world, f"{LocationName.vanilla_dome_2_region} -> {LocationName.vanilla_dome_2_exit_2}")
        connect_green_yoshi_levels(world, f"{LocationName.cheese_bridge_region} -> {LocationName.cheese_bridge_exit_1}")
        connect_green_yoshi_levels(world, f"{LocationName.chocolate_island_3_region} -> {LocationName.chocolate_island_3_exit_1}")
        connect_green_yoshi_levels(world, f"{LocationName.valley_of_bowser_4_region} -> {LocationName.valley_of_bowser_4_exit_2}")
        connect_green_yoshi_levels(world, f"{LocationName.star_road_3_region} -> {LocationName.star_road_3_exit_2}")
        connect_green_yoshi_levels(world, f"{LocationName.special_zone_3_region} -> {LocationName.special_zone_3_exit_1}")
        connect_green_yoshi_levels(world, f"{LocationName.special_zone_8_region} -> {LocationName.special_zone_8_exit_1}")


def connect_blue_yoshi_levels(world: "WaffleWorld", entrance_name: str):
    entrance = world.multiworld.get_entrance(entrance_name, world.player)
    for region_name in BLUE_YOSHI_LEVELS:
        region = world.multiworld.get_region(region_name, world.player)
        world.multiworld.register_indirect_condition(region, entrance)
    for region_name in GREEN_YOSHI_LEVELS:
        region = world.multiworld.get_region(region_name, world.player)
        world.multiworld.register_indirect_condition(region, entrance)
    for region_name in RED_YOSHI_LEVELS:
        region = world.multiworld.get_region(region_name, world.player)
        world.multiworld.register_indirect_condition(region, entrance)
    for region_name in YELLOW_YOSHI_LEVELS:
        region = world.multiworld.get_region(region_name, world.player)
        world.multiworld.register_indirect_condition(region, entrance)

def connect_green_yoshi_levels(world: "WaffleWorld", entrance_name: str):
    entrance = world.multiworld.get_entrance(entrance_name, world.player)
    for region_name in GREEN_YOSHI_LEVELS:
        region = world.multiworld.get_region(region_name, world.player)
        world.multiworld.register_indirect_condition(region, entrance)


def create_region(world: "WaffleWorld", active_locations: typing.Dict[str,int], name: str, locations: typing.List | None = None):
    ret = Region(name, world.player, world.multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = WaffleLocation(world.player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret

def add_location_to_region(world: "WaffleWorld", active_locations: typing.Dict[str,int], region_name: str, location_name: str,
                           rule: typing.Optional[typing.Callable] = None):
    region = world.multiworld.get_region(region_name, world.player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = WaffleLocation(world.player, location_name, loc_id, region)
        region.locations.append(location)
        if rule:
            add_rule(location, rule)


def add_event_to_region(world: "WaffleWorld", region_name: str, event_name: str, event_item=None):
    region = world.multiworld.get_region(region_name, world.player)
    event = WaffleLocation(world.player, event_name, None, region)
    if event_item:
        event.place_locked_item(WaffleItem(event_item, ItemClassification.progression, None, world.player))
    else:
        event.place_locked_item(WaffleItem(event_name, ItemClassification.progression, None, world.player))
    region.locations.append(event)


def connect(world: "WaffleWorld", source: str, target: str) -> None:
    source_region: Region = world.get_region(source)
    target_region: Region = world.get_region(target)
    source_region.connect(target_region)
