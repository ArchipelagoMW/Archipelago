import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import SMWLocation
from .Levels import level_info_dict
from .Names import LocationName, ItemName
from worlds.generic.Rules import add_rule, set_rule


def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None)

    yoshis_island_region = create_region(world, player, active_locations, LocationName.yoshis_island_region, None)


    yoshis_house_tile = create_region(world, player, active_locations, LocationName.yoshis_house_tile, None)

    yoshis_house_region_locations = []
    if world.goal[player] == "yoshi_egg_hunt":
        yoshis_house_region_locations.append(LocationName.yoshis_house)
    yoshis_house_region = create_region(world, player, active_locations, LocationName.yoshis_house,
                                        yoshis_house_region_locations)

    yoshis_island_1_tile = create_region(world, player, active_locations, LocationName.yoshis_island_1_tile, None)
    yoshis_island_1_region = create_region(world, player, active_locations, LocationName.yoshis_island_1_region, None)
    yoshis_island_1_exit_1 = create_region(world, player, active_locations, LocationName.yoshis_island_1_exit_1,
                                           [LocationName.yoshis_island_1_exit_1])

    yoshis_island_2_tile = create_region(world, player, active_locations, LocationName.yoshis_island_2_tile, None)
    yoshis_island_2_region = create_region(world, player, active_locations, LocationName.yoshis_island_2_region, None)
    yoshis_island_2_exit_1 = create_region(world, player, active_locations, LocationName.yoshis_island_2_exit_1,
                                           [LocationName.yoshis_island_2_exit_1])

    yoshis_island_3_tile = create_region(world, player, active_locations, LocationName.yoshis_island_3_tile, None)
    yoshis_island_3_region = create_region(world, player, active_locations, LocationName.yoshis_island_3_region, None)
    yoshis_island_3_exit_1 = create_region(world, player, active_locations, LocationName.yoshis_island_3_exit_1,
                                           [LocationName.yoshis_island_3_exit_1])

    yoshis_island_4_tile = create_region(world, player, active_locations, LocationName.yoshis_island_4_tile, None)
    yoshis_island_4_region = create_region(world, player, active_locations, LocationName.yoshis_island_4_region, None)
    yoshis_island_4_exit_1 = create_region(world, player, active_locations, LocationName.yoshis_island_4_exit_1,
                                           [LocationName.yoshis_island_4_exit_1])

    yoshis_island_castle_tile = create_region(world, player, active_locations, LocationName.yoshis_island_castle_tile, None)
    yoshis_island_castle_region = create_region(world, player, active_locations, LocationName.yoshis_island_castle_region, None)
    yoshis_island_castle = create_region(world, player, active_locations, LocationName.yoshis_island_castle,
                                         [LocationName.yoshis_island_castle, LocationName.yoshis_island_koopaling])

    yellow_switch_palace_tile = create_region(world, player, active_locations, LocationName.yellow_switch_palace_tile, None)
    yellow_switch_palace = create_region(world, player, active_locations, LocationName.yellow_switch_palace,
                                         [LocationName.yellow_switch_palace])


    donut_plains_1_tile = create_region(world, player, active_locations, LocationName.donut_plains_1_tile, None)
    donut_plains_1_region = create_region(world, player, active_locations, LocationName.donut_plains_1_region, None)
    donut_plains_1_exit_1 = create_region(world, player, active_locations, LocationName.donut_plains_1_exit_1,
                                          [LocationName.donut_plains_1_exit_1])
    donut_plains_1_exit_2 = create_region(world, player, active_locations, LocationName.donut_plains_1_exit_2,
                                          [LocationName.donut_plains_1_exit_2])

    donut_plains_2_tile = create_region(world, player, active_locations, LocationName.donut_plains_2_tile, None)
    donut_plains_2_region = create_region(world, player, active_locations, LocationName.donut_plains_2_region, None)
    donut_plains_2_exit_1 = create_region(world, player, active_locations, LocationName.donut_plains_2_exit_1,
                                           [LocationName.donut_plains_2_exit_1])
    donut_plains_2_exit_2 = create_region(world, player, active_locations, LocationName.donut_plains_2_exit_2,
                                          [LocationName.donut_plains_2_exit_2])

    donut_plains_3_tile = create_region(world, player, active_locations, LocationName.donut_plains_3_tile, None)
    donut_plains_3_region = create_region(world, player, active_locations, LocationName.donut_plains_3_region, None)
    donut_plains_3_exit_1 = create_region(world, player, active_locations, LocationName.donut_plains_3_exit_1,
                                          [LocationName.donut_plains_3_exit_1])

    donut_plains_4_tile = create_region(world, player, active_locations, LocationName.donut_plains_4_tile, None)
    donut_plains_4_region = create_region(world, player, active_locations, LocationName.donut_plains_4_region, None)
    donut_plains_4_exit_1 = create_region(world, player, active_locations, LocationName.donut_plains_4_exit_1,
                                          [LocationName.donut_plains_4_exit_1])

    donut_secret_1_tile = create_region(world, player, active_locations, LocationName.donut_secret_1_tile, None)
    donut_secret_1_region = create_region(world, player, active_locations, LocationName.donut_secret_1_region, None)
    donut_secret_1_exit_1 = create_region(world, player, active_locations, LocationName.donut_secret_1_exit_1,
                                          [LocationName.donut_secret_1_exit_1])
    donut_secret_1_exit_2 = create_region(world, player, active_locations, LocationName.donut_secret_1_exit_2,
                                          [LocationName.donut_secret_1_exit_2])

    donut_secret_2_tile = create_region(world, player, active_locations, LocationName.donut_secret_2_tile, None)
    donut_secret_2_region = create_region(world, player, active_locations, LocationName.donut_secret_2_region, None)
    donut_secret_2_exit_1 = create_region(world, player, active_locations, LocationName.donut_secret_2_exit_1,
                                          [LocationName.donut_secret_2_exit_1])

    donut_ghost_house_tile = create_region(world, player, active_locations, LocationName.donut_ghost_house_tile, None)
    donut_ghost_house_region = create_region(world, player, active_locations, LocationName.donut_ghost_house_region, None)
    donut_ghost_house_exit_1 = create_region(world, player, active_locations, LocationName.donut_ghost_house_exit_1,
                                             [LocationName.donut_ghost_house_exit_1])
    donut_ghost_house_exit_2 = create_region(world, player, active_locations, LocationName.donut_ghost_house_exit_2,
                                             [LocationName.donut_ghost_house_exit_2])

    donut_secret_house_tile = create_region(world, player, active_locations, LocationName.donut_secret_house_tile, None)
    donut_secret_house_region = create_region(world, player, active_locations, LocationName.donut_secret_house_region, None)
    donut_secret_house_exit_1 = create_region(world, player, active_locations, LocationName.donut_secret_house_exit_1,
                                              [LocationName.donut_secret_house_exit_1])
    donut_secret_house_exit_2 = create_region(world, player, active_locations, LocationName.donut_secret_house_exit_2,
                                              [LocationName.donut_secret_house_exit_2])

    donut_plains_castle_tile = create_region(world, player, active_locations, LocationName.donut_plains_castle_tile, None)
    donut_plains_castle_region = create_region(world, player, active_locations, LocationName.donut_plains_castle_region, None)
    donut_plains_castle = create_region(world, player, active_locations, LocationName.donut_plains_castle,
                                        [LocationName.donut_plains_castle, LocationName.donut_plains_koopaling])

    green_switch_palace_tile = create_region(world, player, active_locations, LocationName.green_switch_palace_tile, None)
    green_switch_palace = create_region(world, player, active_locations, LocationName.green_switch_palace,
                                        [LocationName.green_switch_palace])

    donut_plains_top_secret_tile = create_region(world, player, active_locations, LocationName.donut_plains_top_secret_tile, None)
    donut_plains_top_secret = create_region(world, player, active_locations, LocationName.donut_plains_top_secret, None)


    vanilla_dome_1_tile = create_region(world, player, active_locations, LocationName.vanilla_dome_1_tile, None)
    vanilla_dome_1_region = create_region(world, player, active_locations, LocationName.vanilla_dome_1_region, None)
    vanilla_dome_1_exit_1 = create_region(world, player, active_locations, LocationName.vanilla_dome_1_exit_1,
                                          [LocationName.vanilla_dome_1_exit_1])
    vanilla_dome_1_exit_2 = create_region(world, player, active_locations, LocationName.vanilla_dome_1_exit_2,
                                          [LocationName.vanilla_dome_1_exit_2])

    vanilla_dome_2_tile = create_region(world, player, active_locations, LocationName.vanilla_dome_2_tile, None)
    vanilla_dome_2_region = create_region(world, player, active_locations, LocationName.vanilla_dome_2_region, None)
    vanilla_dome_2_exit_1 = create_region(world, player, active_locations, LocationName.vanilla_dome_2_exit_1,
                                          [LocationName.vanilla_dome_2_exit_1])
    vanilla_dome_2_exit_2 = create_region(world, player, active_locations, LocationName.vanilla_dome_2_exit_2,
                                          [LocationName.vanilla_dome_2_exit_2])

    vanilla_dome_3_tile = create_region(world, player, active_locations, LocationName.vanilla_dome_3_tile, None)
    vanilla_dome_3_region = create_region(world, player, active_locations, LocationName.vanilla_dome_3_region, None)
    vanilla_dome_3_exit_1 = create_region(world, player, active_locations, LocationName.vanilla_dome_3_exit_1,
                                          [LocationName.vanilla_dome_3_exit_1])

    vanilla_dome_4_tile = create_region(world, player, active_locations, LocationName.vanilla_dome_4_tile, None)
    vanilla_dome_4_region = create_region(world, player, active_locations, LocationName.vanilla_dome_4_region, None)
    vanilla_dome_4_exit_1 = create_region(world, player, active_locations, LocationName.vanilla_dome_4_exit_1,
                                          [LocationName.vanilla_dome_4_exit_1])

    vanilla_secret_1_tile = create_region(world, player, active_locations, LocationName.vanilla_secret_1_tile, None)
    vanilla_secret_1_region = create_region(world, player, active_locations, LocationName.vanilla_secret_1_region, None)
    vanilla_secret_1_exit_1 = create_region(world, player, active_locations, LocationName.vanilla_secret_1_exit_1,
                                            [LocationName.vanilla_secret_1_exit_1])
    vanilla_secret_1_exit_2 = create_region(world, player, active_locations, LocationName.vanilla_secret_1_exit_2,
                                            [LocationName.vanilla_secret_1_exit_2])

    vanilla_secret_2_tile = create_region(world, player, active_locations, LocationName.vanilla_secret_2_tile, None)
    vanilla_secret_2_region = create_region(world, player, active_locations, LocationName.vanilla_secret_2_region, None)
    vanilla_secret_2_exit_1 = create_region(world, player, active_locations, LocationName.vanilla_secret_2_exit_1,
                                            [LocationName.vanilla_secret_2_exit_1])

    vanilla_secret_3_tile = create_region(world, player, active_locations, LocationName.vanilla_secret_3_tile, None)
    vanilla_secret_3_region = create_region(world, player, active_locations, LocationName.vanilla_secret_3_region, None)
    vanilla_secret_3_exit_1 = create_region(world, player, active_locations, LocationName.vanilla_secret_3_exit_1,
                                            [LocationName.vanilla_secret_3_exit_1])

    vanilla_ghost_house_tile = create_region(world, player, active_locations, LocationName.vanilla_ghost_house_tile, None)
    vanilla_ghost_house_region = create_region(world, player, active_locations, LocationName.vanilla_ghost_house_region, None)
    vanilla_ghost_house_exit_1 = create_region(world, player, active_locations, LocationName.vanilla_ghost_house_exit_1,
                                               [LocationName.vanilla_ghost_house_exit_1])

    vanilla_fortress_tile = create_region(world, player, active_locations, LocationName.vanilla_fortress_tile, None)
    vanilla_fortress_region = create_region(world, player, active_locations, LocationName.vanilla_fortress_region, None)
    vanilla_fortress = create_region(world, player, active_locations, LocationName.vanilla_fortress,
                                     [LocationName.vanilla_fortress, LocationName.vanilla_reznor])

    vanilla_dome_castle_tile = create_region(world, player, active_locations, LocationName.vanilla_dome_castle_tile, None)
    vanilla_dome_castle_region = create_region(world, player, active_locations, LocationName.vanilla_dome_castle_region, None)
    vanilla_dome_castle = create_region(world, player, active_locations, LocationName.vanilla_dome_castle,
                                        [LocationName.vanilla_dome_castle, LocationName.vanilla_dome_koopaling])

    red_switch_palace_tile = create_region(world, player, active_locations, LocationName.red_switch_palace_tile, None)
    red_switch_palace = create_region(world, player, active_locations, LocationName.red_switch_palace,
                                      [LocationName.red_switch_palace])


    butter_bridge_1_tile = create_region(world, player, active_locations, LocationName.butter_bridge_1_tile, None)
    butter_bridge_1_region = create_region(world, player, active_locations, LocationName.butter_bridge_1_region, None)
    butter_bridge_1_exit_1 = create_region(world, player, active_locations, LocationName.butter_bridge_1_exit_1,
                                           [LocationName.butter_bridge_1_exit_1])

    butter_bridge_2_tile = create_region(world, player, active_locations, LocationName.butter_bridge_2_tile, None)
    butter_bridge_2_region = create_region(world, player, active_locations, LocationName.butter_bridge_2_region, None)
    butter_bridge_2_exit_1 = create_region(world, player, active_locations, LocationName.butter_bridge_2_exit_1,
                                           [LocationName.butter_bridge_2_exit_1])

    cheese_bridge_tile = create_region(world, player, active_locations, LocationName.cheese_bridge_tile, None)
    cheese_bridge_region = create_region(world, player, active_locations, LocationName.cheese_bridge_region, None)
    cheese_bridge_exit_1 = create_region(world, player, active_locations, LocationName.cheese_bridge_exit_1,
                                         [LocationName.cheese_bridge_exit_1])
    cheese_bridge_exit_2 = create_region(world, player, active_locations, LocationName.cheese_bridge_exit_2,
                                         [LocationName.cheese_bridge_exit_2])

    cookie_mountain_tile = create_region(world, player, active_locations, LocationName.cookie_mountain_tile, None)
    cookie_mountain_region = create_region(world, player, active_locations, LocationName.cookie_mountain_region, None)
    cookie_mountain_exit_1 = create_region(world, player, active_locations, LocationName.cookie_mountain_exit_1,
                                          [LocationName.cookie_mountain_exit_1])

    soda_lake_tile = create_region(world, player, active_locations, LocationName.soda_lake_tile, None)
    soda_lake_region = create_region(world, player, active_locations, LocationName.soda_lake_region, None)
    soda_lake_exit_1 = create_region(world, player, active_locations, LocationName.soda_lake_exit_1,
                                     [LocationName.soda_lake_exit_1])

    twin_bridges_castle_tile = create_region(world, player, active_locations, LocationName.twin_bridges_castle_tile, None)
    twin_bridges_castle_region = create_region(world, player, active_locations, LocationName.twin_bridges_castle_region, None)
    twin_bridges_castle = create_region(world, player, active_locations, LocationName.twin_bridges_castle,
                                        [LocationName.twin_bridges_castle, LocationName.twin_bridges_koopaling])


    forest_of_illusion_1_tile = create_region(world, player, active_locations, LocationName.forest_of_illusion_1_tile, None)
    forest_of_illusion_1_region = create_region(world, player, active_locations, LocationName.forest_of_illusion_1_region, None)
    forest_of_illusion_1_exit_1 = create_region(world, player, active_locations, LocationName.forest_of_illusion_1_exit_1,
                                                [LocationName.forest_of_illusion_1_exit_1])
    forest_of_illusion_1_exit_2 = create_region(world, player, active_locations, LocationName.forest_of_illusion_1_exit_2,
                                                [LocationName.forest_of_illusion_1_exit_2])

    forest_of_illusion_2_tile = create_region(world, player, active_locations, LocationName.forest_of_illusion_2_tile, None)
    forest_of_illusion_2_region = create_region(world, player, active_locations, LocationName.forest_of_illusion_2_region, None)
    forest_of_illusion_2_exit_1 = create_region(world, player, active_locations, LocationName.forest_of_illusion_2_exit_1,
                                                [LocationName.forest_of_illusion_2_exit_1])
    forest_of_illusion_2_exit_2 = create_region(world, player, active_locations, LocationName.forest_of_illusion_2_exit_2,
                                                [LocationName.forest_of_illusion_2_exit_2])

    forest_of_illusion_3_tile = create_region(world, player, active_locations, LocationName.forest_of_illusion_3_tile, None)
    forest_of_illusion_3_region = create_region(world, player, active_locations, LocationName.forest_of_illusion_3_region, None)
    forest_of_illusion_3_exit_1 = create_region(world, player, active_locations, LocationName.forest_of_illusion_3_exit_1,
                                                [LocationName.forest_of_illusion_3_exit_1])
    forest_of_illusion_3_exit_2 = create_region(world, player, active_locations, LocationName.forest_of_illusion_3_exit_2,
                                                [LocationName.forest_of_illusion_3_exit_2])

    forest_of_illusion_4_tile = create_region(world, player, active_locations, LocationName.forest_of_illusion_4_tile, None)
    forest_of_illusion_4_region = create_region(world, player, active_locations, LocationName.forest_of_illusion_4_region, None)
    forest_of_illusion_4_exit_1 = create_region(world, player, active_locations, LocationName.forest_of_illusion_4_exit_1,
                                                [LocationName.forest_of_illusion_4_exit_1])
    forest_of_illusion_4_exit_2 = create_region(world, player, active_locations, LocationName.forest_of_illusion_4_exit_2,
                                                [LocationName.forest_of_illusion_4_exit_2])

    forest_ghost_house_tile = create_region(world, player, active_locations, LocationName.forest_ghost_house_tile, None)
    forest_ghost_house_region = create_region(world, player, active_locations, LocationName.forest_ghost_house_region, None)
    forest_ghost_house_exit_1 = create_region(world, player, active_locations, LocationName.forest_ghost_house_exit_1,
                                              [LocationName.forest_ghost_house_exit_1])
    forest_ghost_house_exit_2 = create_region(world, player, active_locations, LocationName.forest_ghost_house_exit_2,
                                              [LocationName.forest_ghost_house_exit_2])

    forest_secret_tile = create_region(world, player, active_locations, LocationName.forest_secret_tile, None)
    forest_secret_region = create_region(world, player, active_locations, LocationName.forest_secret_region, None)
    forest_secret_exit_1 = create_region(world, player, active_locations, LocationName.forest_secret_exit_1,
                                         [LocationName.forest_secret_exit_1])

    forest_fortress_tile = create_region(world, player, active_locations, LocationName.forest_fortress_tile, None)
    forest_fortress_region = create_region(world, player, active_locations, LocationName.forest_fortress_region, None)
    forest_fortress = create_region(world, player, active_locations, LocationName.forest_fortress,
                                    [LocationName.forest_fortress, LocationName.forest_reznor])

    forest_castle_tile = create_region(world, player, active_locations, LocationName.forest_castle_tile, None)
    forest_castle_region = create_region(world, player, active_locations, LocationName.forest_castle_region, None)
    forest_castle = create_region(world, player, active_locations, LocationName.forest_castle,
                                  [LocationName.forest_castle, LocationName.forest_koopaling])

    blue_switch_palace_tile = create_region(world, player, active_locations, LocationName.blue_switch_palace_tile, None)
    blue_switch_palace = create_region(world, player, active_locations, LocationName.blue_switch_palace,
                                       [LocationName.blue_switch_palace])


    chocolate_island_1_tile = create_region(world, player, active_locations, LocationName.chocolate_island_1_tile, None)
    chocolate_island_1_region = create_region(world, player, active_locations, LocationName.chocolate_island_1_region, None)
    chocolate_island_1_exit_1 = create_region(world, player, active_locations, LocationName.chocolate_island_1_exit_1,
                                              [LocationName.chocolate_island_1_exit_1])

    chocolate_island_2_tile = create_region(world, player, active_locations, LocationName.chocolate_island_2_tile, None)
    chocolate_island_2_region = create_region(world, player, active_locations, LocationName.chocolate_island_2_region, None)
    chocolate_island_2_exit_1 = create_region(world, player, active_locations, LocationName.chocolate_island_2_exit_1,
                                              [LocationName.chocolate_island_2_exit_1])
    chocolate_island_2_exit_2 = create_region(world, player, active_locations, LocationName.chocolate_island_2_exit_2,
                                              [LocationName.chocolate_island_2_exit_2])

    chocolate_island_3_tile = create_region(world, player, active_locations, LocationName.chocolate_island_3_tile, None)
    chocolate_island_3_region = create_region(world, player, active_locations, LocationName.chocolate_island_3_region, None)
    chocolate_island_3_exit_1 = create_region(world, player, active_locations, LocationName.chocolate_island_3_exit_1,
                                              [LocationName.chocolate_island_3_exit_1])
    chocolate_island_3_exit_2 = create_region(world, player, active_locations, LocationName.chocolate_island_3_exit_2,
                                              [LocationName.chocolate_island_3_exit_2])

    chocolate_island_4_tile = create_region(world, player, active_locations, LocationName.chocolate_island_4_tile, None)
    chocolate_island_4_region = create_region(world, player, active_locations, LocationName.chocolate_island_4_region, None)
    chocolate_island_4_exit_1 = create_region(world, player, active_locations, LocationName.chocolate_island_4_exit_1,
                                              [LocationName.chocolate_island_4_exit_1])

    chocolate_island_5_tile = create_region(world, player, active_locations, LocationName.chocolate_island_5_tile, None)
    chocolate_island_5_region = create_region(world, player, active_locations, LocationName.chocolate_island_5_region, None)
    chocolate_island_5_exit_1 = create_region(world, player, active_locations, LocationName.chocolate_island_5_exit_1,
                                              [LocationName.chocolate_island_5_exit_1])

    chocolate_ghost_house_tile = create_region(world, player, active_locations, LocationName.chocolate_ghost_house_tile, None)
    chocolate_ghost_house_region = create_region(world, player, active_locations, LocationName.chocolate_ghost_house_region, None)
    chocolate_ghost_house_exit_1 = create_region(world, player, active_locations, LocationName.chocolate_ghost_house_exit_1,
                                                 [LocationName.chocolate_ghost_house_exit_1])

    chocolate_secret_tile = create_region(world, player, active_locations, LocationName.chocolate_secret_tile, None)
    chocolate_secret_region = create_region(world, player, active_locations, LocationName.chocolate_secret_region, None)
    chocolate_secret_exit_1 = create_region(world, player, active_locations, LocationName.chocolate_secret_exit_1,
                                            [LocationName.chocolate_secret_exit_1])

    chocolate_fortress_tile = create_region(world, player, active_locations, LocationName.chocolate_fortress_tile, None)
    chocolate_fortress_region = create_region(world, player, active_locations, LocationName.chocolate_fortress_region, None)
    chocolate_fortress = create_region(world, player, active_locations, LocationName.chocolate_fortress,
                                       [LocationName.chocolate_fortress, LocationName.chocolate_reznor])

    chocolate_castle_tile = create_region(world, player, active_locations, LocationName.chocolate_castle_tile, None)
    chocolate_castle_region = create_region(world, player, active_locations, LocationName.chocolate_castle_region, None)
    chocolate_castle = create_region(world, player, active_locations, LocationName.chocolate_castle,
                                     [LocationName.chocolate_castle, LocationName.chocolate_koopaling])

    sunken_ghost_ship_tile = create_region(world, player, active_locations, LocationName.sunken_ghost_ship_tile, None)
    sunken_ghost_ship_region = create_region(world, player, active_locations, LocationName.sunken_ghost_ship_region, None)
    sunken_ghost_ship = create_region(world, player, active_locations, LocationName.sunken_ghost_ship,
                                      [LocationName.sunken_ghost_ship])


    valley_of_bowser_1_tile = create_region(world, player, active_locations, LocationName.valley_of_bowser_1_tile, None)
    valley_of_bowser_1_region = create_region(world, player, active_locations, LocationName.valley_of_bowser_1_region, None)
    valley_of_bowser_1_exit_1 = create_region(world, player, active_locations, LocationName.valley_of_bowser_1_exit_1,
                                              [LocationName.valley_of_bowser_1_exit_1])

    valley_of_bowser_2_tile = create_region(world, player, active_locations, LocationName.valley_of_bowser_2_tile, None)
    valley_of_bowser_2_region = create_region(world, player, active_locations, LocationName.valley_of_bowser_2_region, None)
    valley_of_bowser_2_exit_1 = create_region(world, player, active_locations, LocationName.valley_of_bowser_2_exit_1,
                                              [LocationName.valley_of_bowser_2_exit_1])
    valley_of_bowser_2_exit_2 = create_region(world, player, active_locations, LocationName.valley_of_bowser_2_exit_2,
                                              [LocationName.valley_of_bowser_2_exit_2])

    valley_of_bowser_3_tile = create_region(world, player, active_locations, LocationName.valley_of_bowser_3_tile, None)
    valley_of_bowser_3_region = create_region(world, player, active_locations, LocationName.valley_of_bowser_3_region, None)
    valley_of_bowser_3_exit_1 = create_region(world, player, active_locations, LocationName.valley_of_bowser_3_exit_1,
                                              [LocationName.valley_of_bowser_3_exit_1])

    valley_of_bowser_4_tile = create_region(world, player, active_locations, LocationName.valley_of_bowser_4_tile, None)
    valley_of_bowser_4_region = create_region(world, player, active_locations, LocationName.valley_of_bowser_4_region, None)
    valley_of_bowser_4_exit_1 = create_region(world, player, active_locations, LocationName.valley_of_bowser_4_exit_1,
                                              [LocationName.valley_of_bowser_4_exit_1])
    valley_of_bowser_4_exit_2 = create_region(world, player, active_locations, LocationName.valley_of_bowser_4_exit_2,
                                              [LocationName.valley_of_bowser_4_exit_2])

    valley_ghost_house_tile = create_region(world, player, active_locations, LocationName.valley_ghost_house_tile, None)
    valley_ghost_house_region = create_region(world, player, active_locations, LocationName.valley_ghost_house_region, None)
    valley_ghost_house_exit_1 = create_region(world, player, active_locations, LocationName.valley_ghost_house_exit_1,
                                              [LocationName.valley_ghost_house_exit_1])
    valley_ghost_house_exit_2 = create_region(world, player, active_locations, LocationName.valley_ghost_house_exit_2,
                                              [LocationName.valley_ghost_house_exit_2])

    valley_fortress_tile = create_region(world, player, active_locations, LocationName.valley_fortress_tile, None)
    valley_fortress_region = create_region(world, player, active_locations, LocationName.valley_fortress_region, None)
    valley_fortress = create_region(world, player, active_locations, LocationName.valley_fortress,
                                    [LocationName.valley_fortress, LocationName.valley_reznor])

    valley_castle_tile = create_region(world, player, active_locations, LocationName.valley_castle_tile, None)
    valley_castle_region = create_region(world, player, active_locations, LocationName.valley_castle_region, None)
    valley_castle = create_region(world, player, active_locations, LocationName.valley_castle,
                                  [LocationName.valley_castle, LocationName.valley_koopaling])

    front_door_tile = create_region(world, player, active_locations, LocationName.front_door_tile, None)
    front_door_region = create_region(world, player, active_locations, LocationName.front_door, None)
    back_door_tile = create_region(world, player, active_locations, LocationName.back_door_tile, None)
    back_door_region = create_region(world, player, active_locations, LocationName.back_door, None)
    bowser_region_locations = []
    if world.goal[player] == "bowser":
        bowser_region_locations += [LocationName.bowser]
    bowser_region = create_region(world, player, active_locations, LocationName.bowser_region, bowser_region_locations)


    donut_plains_star_road = create_region(world, player, active_locations, LocationName.donut_plains_star_road, None)
    vanilla_dome_star_road = create_region(world, player, active_locations, LocationName.vanilla_dome_star_road, None)
    twin_bridges_star_road = create_region(world, player, active_locations, LocationName.twin_bridges_star_road, None)
    forest_star_road = create_region(world, player, active_locations, LocationName.forest_star_road, None)
    valley_star_road = create_region(world, player, active_locations, LocationName.valley_star_road, None)
    star_road_donut = create_region(world, player, active_locations, LocationName.star_road_donut, None)
    star_road_vanilla = create_region(world, player, active_locations, LocationName.star_road_vanilla, None)
    star_road_twin_bridges = create_region(world, player, active_locations, LocationName.star_road_twin_bridges, None)
    star_road_forest = create_region(world, player, active_locations, LocationName.star_road_forest, None)
    star_road_valley = create_region(world, player, active_locations, LocationName.star_road_valley, None)
    star_road_special = create_region(world, player, active_locations, LocationName.star_road_special, None)
    special_star_road = create_region(world, player, active_locations, LocationName.special_star_road, None)

    star_road_1_tile = create_region(world, player, active_locations, LocationName.star_road_1_tile, None)
    star_road_1_region = create_region(world, player, active_locations, LocationName.star_road_1_region, None)
    star_road_1_exit_1 = create_region(world, player, active_locations, LocationName.star_road_1_exit_1,
                                       [LocationName.star_road_1_exit_1])
    star_road_1_exit_2 = create_region(world, player, active_locations, LocationName.star_road_1_exit_2,
                                       [LocationName.star_road_1_exit_2])

    star_road_2_tile = create_region(world, player, active_locations, LocationName.star_road_2_tile, None)
    star_road_2_region = create_region(world, player, active_locations, LocationName.star_road_2_region, None)
    star_road_2_exit_1 = create_region(world, player, active_locations, LocationName.star_road_2_exit_1,
                                       [LocationName.star_road_2_exit_1])
    star_road_2_exit_2 = create_region(world, player, active_locations, LocationName.star_road_2_exit_2,
                                       [LocationName.star_road_2_exit_2])

    star_road_3_tile = create_region(world, player, active_locations, LocationName.star_road_3_tile, None)
    star_road_3_region = create_region(world, player, active_locations, LocationName.star_road_3_region, None)
    star_road_3_exit_1 = create_region(world, player, active_locations, LocationName.star_road_3_exit_1,
                                       [LocationName.star_road_3_exit_1])
    star_road_3_exit_2 = create_region(world, player, active_locations, LocationName.star_road_3_exit_2,
                                       [LocationName.star_road_3_exit_2])

    star_road_4_tile = create_region(world, player, active_locations, LocationName.star_road_4_tile, None)
    star_road_4_region = create_region(world, player, active_locations, LocationName.star_road_4_region, None)
    star_road_4_exit_1 = create_region(world, player, active_locations, LocationName.star_road_4_exit_1,
                                       [LocationName.star_road_4_exit_1])
    star_road_4_exit_2 = create_region(world, player, active_locations, LocationName.star_road_4_exit_2,
                                       [LocationName.star_road_4_exit_2])

    star_road_5_tile = create_region(world, player, active_locations, LocationName.star_road_5_tile, None)
    star_road_5_region = create_region(world, player, active_locations, LocationName.star_road_5_region, None)
    star_road_5_exit_1 = create_region(world, player, active_locations, LocationName.star_road_5_exit_1,
                                       [LocationName.star_road_5_exit_1])
    star_road_5_exit_2 = create_region(world, player, active_locations, LocationName.star_road_5_exit_2,
                                       [LocationName.star_road_5_exit_2])


    special_zone_1_tile = create_region(world, player, active_locations, LocationName.special_zone_1_tile, None)
    special_zone_1_region = create_region(world, player, active_locations, LocationName.special_zone_1_region, None)
    special_zone_1_exit_1 = create_region(world, player, active_locations, LocationName.special_zone_1_exit_1,
                                          [LocationName.special_zone_1_exit_1])

    special_zone_2_tile = create_region(world, player, active_locations, LocationName.special_zone_2_tile, None)
    special_zone_2_region = create_region(world, player, active_locations, LocationName.special_zone_2_region, None)
    special_zone_2_exit_1 = create_region(world, player, active_locations, LocationName.special_zone_2_exit_1,
                                          [LocationName.special_zone_2_exit_1])

    special_zone_3_tile = create_region(world, player, active_locations, LocationName.special_zone_3_tile, None)
    special_zone_3_region = create_region(world, player, active_locations, LocationName.special_zone_3_region, None)
    special_zone_3_exit_1 = create_region(world, player, active_locations, LocationName.special_zone_3_exit_1,
                                          [LocationName.special_zone_3_exit_1])

    special_zone_4_tile = create_region(world, player, active_locations, LocationName.special_zone_4_tile, None)
    special_zone_4_region = create_region(world, player, active_locations, LocationName.special_zone_4_region, None)
    special_zone_4_exit_1 = create_region(world, player, active_locations, LocationName.special_zone_4_exit_1,
                                          [LocationName.special_zone_4_exit_1])

    special_zone_5_tile = create_region(world, player, active_locations, LocationName.special_zone_5_tile, None)
    special_zone_5_region = create_region(world, player, active_locations, LocationName.special_zone_5_region, None)
    special_zone_5_exit_1 = create_region(world, player, active_locations, LocationName.special_zone_5_exit_1,
                                          [LocationName.special_zone_5_exit_1])

    special_zone_6_tile = create_region(world, player, active_locations, LocationName.special_zone_6_tile, None)
    special_zone_6_region = create_region(world, player, active_locations, LocationName.special_zone_6_region, None)
    special_zone_6_exit_1 = create_region(world, player, active_locations, LocationName.special_zone_6_exit_1,
                                          [LocationName.special_zone_6_exit_1])

    special_zone_7_tile = create_region(world, player, active_locations, LocationName.special_zone_7_tile, None)
    special_zone_7_region = create_region(world, player, active_locations, LocationName.special_zone_7_region, None)
    special_zone_7_exit_1 = create_region(world, player, active_locations, LocationName.special_zone_7_exit_1,
                                          [LocationName.special_zone_7_exit_1])

    special_zone_8_tile = create_region(world, player, active_locations, LocationName.special_zone_8_tile, None)
    special_zone_8_region = create_region(world, player, active_locations, LocationName.special_zone_8_region, None)
    special_zone_8_exit_1 = create_region(world, player, active_locations, LocationName.special_zone_8_exit_1,
                                          [LocationName.special_zone_8_exit_1])
    special_complete = create_region(world, player, active_locations, LocationName.special_complete, None)


    # Set up the regions correctly.
    world.regions += [
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
    ]


    if world.dragon_coin_checks[player]:
        add_location_to_region(world, player, active_locations, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_dragon,
                               lambda state: (state.has(ItemName.mario_spin_jump, player) and
                                              state.has(ItemName.progressive_powerup, player, 1)))
        add_location_to_region(world, player, active_locations, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_dragon,
                               lambda state: (state.has(ItemName.yoshi_activate, player) or
                                              state.has(ItemName.mario_climb, player)))
        add_location_to_region(world, player, active_locations, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_dragon,
                               lambda state: state.has(ItemName.p_switch, player))
        add_location_to_region(world, player, active_locations, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_dragon,
                               lambda state: (state.has(ItemName.yoshi_activate, player) or
                                              state.has(ItemName.mario_swim, player) or
                                              (state.has(ItemName.mario_carry, player) and state.has(ItemName.p_switch, player))))
        add_location_to_region(world, player, active_locations, LocationName.donut_plains_1_region, LocationName.donut_plains_1_dragon,
                               lambda state: (state.has(ItemName.mario_climb, player) or
                                               state.has(ItemName.yoshi_activate, player) or
                                               (state.has(ItemName.progressive_powerup, player, 3) and state.has(ItemName.mario_run, player))))
        add_location_to_region(world, player, active_locations, LocationName.donut_plains_2_region, LocationName.donut_plains_2_dragon)
        add_location_to_region(world, player, active_locations, LocationName.donut_plains_3_region, LocationName.donut_plains_3_dragon,
                               lambda state: ((state.has(ItemName.mario_spin_jump, player) and state.has(ItemName.progressive_powerup, player, 1) and state.has(ItemName.mario_climb, player) or
                                              state.has(ItemName.yoshi_activate, player) or
                                              (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3)))))
        add_location_to_region(world, player, active_locations, LocationName.donut_plains_4_region, LocationName.donut_plains_4_dragon)
        add_location_to_region(world, player, active_locations, LocationName.donut_secret_1_region, LocationName.donut_secret_1_dragon,
                               lambda state: state.has(ItemName.mario_swim, player))
        add_location_to_region(world, player, active_locations, LocationName.donut_secret_2_region, LocationName.donut_secret_2_dragon,
                               lambda state: (state.has(ItemName.mario_climb, player) or state.has(ItemName.yoshi_activate, player)))
        add_location_to_region(world, player, active_locations, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_dragon,
                               lambda state: (state.has(ItemName.mario_carry, player) and
                                              state.has(ItemName.mario_run, player) and
                                              (state.has(ItemName.super_star_active, player) or
                                               state.has(ItemName.progressive_powerup, player, 1))))
        add_location_to_region(world, player, active_locations, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_dragon,
                               lambda state: (state.has(ItemName.mario_swim, player) and
                                              state.has(ItemName.p_switch, player) and
                                              (state.has(ItemName.mario_climb, player) or state.has(ItemName.yoshi_activate, player))))
        add_location_to_region(world, player, active_locations, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_dragon)
        add_location_to_region(world, player, active_locations, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_dragon)
        add_location_to_region(world, player, active_locations, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_dragon,
                               lambda state: (state.has(ItemName.mario_climb, player) and
                                              state.has(ItemName.mario_carry, player)))
        add_location_to_region(world, player, active_locations, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_dragon,
                               lambda state: (state.has(ItemName.mario_run, player) and
                                              state.has(ItemName.progressive_powerup, player, 3)))
        add_location_to_region(world, player, active_locations, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_dragon,
                               lambda state: state.has(ItemName.mario_swim, player))
        add_location_to_region(world, player, active_locations, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_dragon,
                               lambda state: state.has(ItemName.mario_climb, player))
        add_location_to_region(world, player, active_locations, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_dragon)
        add_location_to_region(world, player, active_locations, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_dragon,
                               lambda state: (state.has(ItemName.mario_run, player) and
                                              state.has(ItemName.progressive_powerup, player, 3)))
        add_location_to_region(world, player, active_locations, LocationName.cheese_bridge_region, LocationName.cheese_bridge_dragon,
                               lambda state: (state.has(ItemName.yoshi_activate, player) or
                                              state.has(ItemName.mario_climb, player)))
        add_location_to_region(world, player, active_locations, LocationName.cookie_mountain_region, LocationName.cookie_mountain_dragon,
                               lambda state: (state.has(ItemName.yoshi_activate, player) or
                                              state.has(ItemName.mario_climb, player)))
        add_location_to_region(world, player, active_locations, LocationName.soda_lake_region, LocationName.soda_lake_dragon,
                               lambda state: state.has(ItemName.mario_swim, player))
        add_location_to_region(world, player, active_locations, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_dragon,
                               lambda state: state.has(ItemName.mario_swim, player))
        add_location_to_region(world, player, active_locations, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_dragon,
                               lambda state: (state.has(ItemName.yoshi_activate, player) or
                                              state.has(ItemName.mario_carry, player)))
        add_location_to_region(world, player, active_locations, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_dragon,
                               lambda state: (state.has(ItemName.yoshi_activate, player) or
                                              state.has(ItemName.mario_carry, player) or
                                              state.has(ItemName.p_switch, player) or
                                              state.has(ItemName.progressive_powerup, player, 2)))
        add_location_to_region(world, player, active_locations, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_dragon,
                               lambda state: state.has(ItemName.p_switch, player))
        add_location_to_region(world, player, active_locations, LocationName.forest_secret_region, LocationName.forest_secret_dragon)
        add_location_to_region(world, player, active_locations, LocationName.forest_castle_region, LocationName.forest_castle_dragon)
        add_location_to_region(world, player, active_locations, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_dragon,
                               lambda state: state.has(ItemName.mario_swim, player))
        add_location_to_region(world, player, active_locations, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_dragon,
                               lambda state: (state.has(ItemName.blue_switch_palace, player) and
                                              (state.has(ItemName.p_switch, player) or
                                               state.has(ItemName.green_switch_palace, player) or
                                               (state.has(ItemName.yellow_switch_palace, player) or state.has(ItemName.red_switch_palace, player)))))
        add_location_to_region(world, player, active_locations, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_dragon)
        add_location_to_region(world, player, active_locations, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_dragon,
                               lambda state: (state.has(ItemName.p_switch, player) and
                                              state.has(ItemName.progressive_powerup, player, 3)))
        add_location_to_region(world, player, active_locations, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_dragon,
                               lambda state: (state.has(ItemName.mario_swim, player) or
                                              (state.has(ItemName.mario_carry, player) and state.has(ItemName.p_switch, player))))
        add_location_to_region(world, player, active_locations, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship_dragon,
                               lambda state: (state.has(ItemName.mario_swim, player) and
                                              state.has(ItemName.super_star_active, player) and
                                              state.has(ItemName.progressive_powerup, player, 3)))
        add_location_to_region(world, player, active_locations, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_dragon)
        add_location_to_region(world, player, active_locations, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_dragon,
                               lambda state: state.has(ItemName.yoshi_activate, player))
        add_location_to_region(world, player, active_locations, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_dragon)
        add_location_to_region(world, player, active_locations, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_dragon,
                               lambda state: state.has(ItemName.p_switch, player))
        add_location_to_region(world, player, active_locations, LocationName.valley_castle_region, LocationName.valley_castle_dragon)
        add_location_to_region(world, player, active_locations, LocationName.star_road_1_region, LocationName.star_road_1_dragon,
                               lambda state: (state.has(ItemName.mario_spin_jump, player) and
                                              state.has(ItemName.progressive_powerup, player, 1)))
        add_location_to_region(world, player, active_locations, LocationName.special_zone_1_region, LocationName.special_zone_1_dragon,
                               lambda state: state.has(ItemName.mario_climb, player))
        add_location_to_region(world, player, active_locations, LocationName.special_zone_2_region, LocationName.special_zone_2_dragon,
                               lambda state: state.has(ItemName.p_balloon, player))
        add_location_to_region(world, player, active_locations, LocationName.special_zone_3_region, LocationName.special_zone_3_dragon,
                               lambda state: state.has(ItemName.yoshi_activate, player))
        add_location_to_region(world, player, active_locations, LocationName.special_zone_4_region, LocationName.special_zone_4_dragon,
                               lambda state: state.has(ItemName.progressive_powerup, player, 1))
        add_location_to_region(world, player, active_locations, LocationName.special_zone_5_region, LocationName.special_zone_5_dragon,
                               lambda state: state.has(ItemName.progressive_powerup, player, 1))
        add_location_to_region(world, player, active_locations, LocationName.special_zone_6_region, LocationName.special_zone_6_dragon,
                               lambda state: state.has(ItemName.mario_swim, player))
        add_location_to_region(world, player, active_locations, LocationName.special_zone_7_region, LocationName.special_zone_7_dragon,
                               lambda state: state.has(ItemName.progressive_powerup, player, 1))
        add_location_to_region(world, player, active_locations, LocationName.special_zone_8_region, LocationName.special_zone_8_dragon,
                               lambda state: state.has(ItemName.progressive_powerup, player, 1))



def connect_regions(world, player, level_to_tile_dict):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, "Menu", LocationName.yoshis_island_region)
    connect(world, player, names, LocationName.yoshis_island_region, LocationName.yoshis_house_tile)
    connect(world, player, names, LocationName.yoshis_house_tile, LocationName.donut_plains_top_secret)
    connect(world, player, names, LocationName.yoshis_island_region, LocationName.yoshis_island_1_tile)
    connect(world, player, names, LocationName.yoshis_island_region, LocationName.yoshis_island_2_tile)

    # Connect regions within levels using rules
    connect(world, player, names, LocationName.yoshis_island_1_region, LocationName.yoshis_island_1_exit_1)
    connect(world, player, names, LocationName.yoshis_island_2_region, LocationName.yoshis_island_2_exit_1)
    connect(world, player, names, LocationName.yoshis_island_3_region, LocationName.yoshis_island_3_exit_1)
    connect(world, player, names, LocationName.yoshis_island_4_region, LocationName.yoshis_island_4_exit_1)
    connect(world, player, names, LocationName.yoshis_island_castle_region, LocationName.yoshis_island_castle,
            lambda state: (state.has(ItemName.mario_climb, player)))

    connect(world, player, names, LocationName.donut_plains_1_region, LocationName.donut_plains_1_exit_1)
    connect(world, player, names, LocationName.donut_plains_1_region, LocationName.donut_plains_1_exit_2,
            lambda state: (state.has(ItemName.mario_carry, player) and
                           (state.has(ItemName.yoshi_activate, player) or
                           state.has(ItemName.green_switch_palace, player) or
                           (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3)))))
    connect(world, player, names, LocationName.donut_plains_2_region, LocationName.donut_plains_2_exit_1)
    connect(world, player, names, LocationName.donut_plains_2_region, LocationName.donut_plains_2_exit_2,
            lambda state: (state.has(ItemName.mario_carry, player) and
                           (state.has(ItemName.yoshi_activate, player) or
                           (state.has(ItemName.mario_spin_jump, player) and state.has(ItemName.mario_climb, player) and state.has(ItemName.progressive_powerup, player, 1)))))
    connect(world, player, names, LocationName.donut_secret_1_region, LocationName.donut_secret_1_exit_1,
            lambda state: state.has(ItemName.mario_swim, player))
    connect(world, player, names, LocationName.donut_secret_1_region, LocationName.donut_secret_1_exit_2,
            lambda state: (state.has(ItemName.mario_carry, player) and
                           state.has(ItemName.mario_swim, player) and
                           state.has(ItemName.p_switch, player)))
    connect(world, player, names, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_exit_1,
            lambda state: (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3)))
    connect(world, player, names, LocationName.donut_ghost_house_region, LocationName.donut_ghost_house_exit_2,
            lambda state: (state.has(ItemName.mario_climb, player) or
                           (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3))))
    connect(world, player, names, LocationName.donut_secret_house_region, LocationName.donut_secret_house_exit_1,
            lambda state: state.has(ItemName.p_switch, player))
    connect(world, player, names, LocationName.donut_secret_house_region, LocationName.donut_secret_house_exit_2,
            lambda state: (state.has(ItemName.p_switch, player) and state.has(ItemName.mario_carry, player) and
                           (state.has(ItemName.mario_climb, player) or
                            (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3)))))
    connect(world, player, names, LocationName.donut_plains_3_region, LocationName.donut_plains_3_exit_1)
    connect(world, player, names, LocationName.donut_plains_4_region, LocationName.donut_plains_4_exit_1)
    connect(world, player, names, LocationName.donut_secret_2_region, LocationName.donut_secret_2_exit_1)
    connect(world, player, names, LocationName.donut_plains_castle_region, LocationName.donut_plains_castle)
    
    connect(world, player, names, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_exit_1,
            lambda state: (state.has(ItemName.mario_run, player) and
                           (state.has(ItemName.super_star_active, player) or
                            state.has(ItemName.progressive_powerup, player, 1))))
    connect(world, player, names, LocationName.vanilla_dome_1_region, LocationName.vanilla_dome_1_exit_2,
            lambda state: (state.has(ItemName.mario_carry, player) and
                           ((state.has(ItemName.yoshi_activate, player) and state.has(ItemName.mario_climb, player)) or
                            (state.has(ItemName.yoshi_activate, player) and state.has(ItemName.red_switch_palace, player)) or
                            (state.has(ItemName.red_switch_palace, player) and state.has(ItemName.mario_climb, player)))))
    connect(world, player, names, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_exit_1,
            lambda state: (state.has(ItemName.mario_swim, player) and
                           (state.has(ItemName.mario_climb, player) or state.has(ItemName.yoshi_activate, player))))
    connect(world, player, names, LocationName.vanilla_dome_2_region, LocationName.vanilla_dome_2_exit_2,
            lambda state: (state.has(ItemName.mario_swim, player) and
                           state.has(ItemName.p_switch, player) and
                           state.has(ItemName.mario_carry, player) and
                           (state.has(ItemName.mario_climb, player) or state.has(ItemName.yoshi_activate, player))))
    connect(world, player, names, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_exit_1,
            lambda state: state.has(ItemName.mario_climb, player))
    connect(world, player, names, LocationName.vanilla_secret_1_region, LocationName.vanilla_secret_1_exit_2,
            lambda state: (state.has(ItemName.mario_climb, player) and
                           (state.has(ItemName.mario_carry, player) and state.has(ItemName.blue_switch_palace, player))))
    connect(world, player, names, LocationName.vanilla_ghost_house_region, LocationName.vanilla_ghost_house_exit_1,
            lambda state: state.has(ItemName.p_switch, player))
    connect(world, player, names, LocationName.vanilla_dome_3_region, LocationName.vanilla_dome_3_exit_1)
    connect(world, player, names, LocationName.vanilla_dome_4_region, LocationName.vanilla_dome_4_exit_1)
    connect(world, player, names, LocationName.vanilla_secret_2_region, LocationName.vanilla_secret_2_exit_1)
    connect(world, player, names, LocationName.vanilla_secret_3_region, LocationName.vanilla_secret_3_exit_1,
            lambda state: state.has(ItemName.mario_swim, player))
    connect(world, player, names, LocationName.vanilla_fortress_region, LocationName.vanilla_fortress,
            lambda state: state.has(ItemName.mario_swim, player))
    connect(world, player, names, LocationName.vanilla_dome_castle_region, LocationName.vanilla_dome_castle)
    
    connect(world, player, names, LocationName.butter_bridge_1_region, LocationName.butter_bridge_1_exit_1)
    connect(world, player, names, LocationName.butter_bridge_2_region, LocationName.butter_bridge_2_exit_1)
    connect(world, player, names, LocationName.cheese_bridge_region, LocationName.cheese_bridge_exit_1,
            lambda state: state.has(ItemName.mario_climb, player))
    connect(world, player, names, LocationName.cheese_bridge_region, LocationName.cheese_bridge_exit_2,
            lambda state: (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3)))
    connect(world, player, names, LocationName.soda_lake_region, LocationName.soda_lake_exit_1,
            lambda state: state.has(ItemName.mario_swim, player))
    connect(world, player, names, LocationName.cookie_mountain_region, LocationName.cookie_mountain_exit_1)
    connect(world, player, names, LocationName.twin_bridges_castle_region, LocationName.twin_bridges_castle,
            lambda state: (state.has(ItemName.mario_run, player) and
                           state.has(ItemName.mario_climb, player)))
                           
    connect(world, player, names, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_exit_1)
    connect(world, player, names, LocationName.forest_of_illusion_1_region, LocationName.forest_of_illusion_1_exit_2,
            lambda state: (state.has(ItemName.mario_carry, player) and
                           state.has(ItemName.p_balloon, player)))
    connect(world, player, names, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_exit_1,
            lambda state: state.has(ItemName.mario_swim, player))
    connect(world, player, names, LocationName.forest_of_illusion_2_region, LocationName.forest_of_illusion_2_exit_2,
            lambda state: (state.has(ItemName.mario_swim, player) and
                           state.has(ItemName.mario_carry, player)))
    connect(world, player, names, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_exit_1,
            lambda state: (state.has(ItemName.mario_carry, player) or
                           state.has(ItemName.yoshi_activate, player)))
    connect(world, player, names, LocationName.forest_of_illusion_3_region, LocationName.forest_of_illusion_3_exit_2,
            lambda state: (state.has(ItemName.mario_spin_jump, player) and
                           state.has(ItemName.mario_carry, player) and
                           state.has(ItemName.progressive_powerup, player, 1)))
    connect(world, player, names, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_exit_1)
    connect(world, player, names, LocationName.forest_of_illusion_4_region, LocationName.forest_of_illusion_4_exit_2,
            lambda state: state.has(ItemName.mario_carry, player))
    connect(world, player, names, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_exit_1,
            lambda state: state.has(ItemName.p_switch, player))
    connect(world, player, names, LocationName.forest_ghost_house_region, LocationName.forest_ghost_house_exit_2,
            lambda state: state.has(ItemName.p_switch, player))
    connect(world, player, names, LocationName.forest_secret_region, LocationName.forest_secret_exit_1)
    connect(world, player, names, LocationName.forest_fortress_region, LocationName.forest_fortress)
    connect(world, player, names, LocationName.forest_castle_region, LocationName.forest_castle)
    
    connect(world, player, names, LocationName.chocolate_island_1_region, LocationName.chocolate_island_1_exit_1,
            lambda state: state.has(ItemName.p_switch, player))
    connect(world, player, names, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_exit_1)
    connect(world, player, names, LocationName.chocolate_island_2_region, LocationName.chocolate_island_2_exit_2,
            lambda state: state.has(ItemName.mario_carry, player))
    connect(world, player, names, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_exit_1,
            lambda state: (state.has(ItemName.mario_climb, player) or
                           (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3))))
    connect(world, player, names, LocationName.chocolate_island_3_region, LocationName.chocolate_island_3_exit_2,
            lambda state: (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3)))
    connect(world, player, names, LocationName.chocolate_island_4_region, LocationName.chocolate_island_4_exit_1)
    connect(world, player, names, LocationName.chocolate_island_5_region, LocationName.chocolate_island_5_exit_1)
    connect(world, player, names, LocationName.chocolate_ghost_house_region, LocationName.chocolate_ghost_house_exit_1)
    connect(world, player, names, LocationName.chocolate_fortress_region, LocationName.chocolate_fortress)
    connect(world, player, names, LocationName.chocolate_secret_region, LocationName.chocolate_secret_exit_1,
            lambda state: state.has(ItemName.mario_run, player))
    connect(world, player, names, LocationName.chocolate_castle_region, LocationName.chocolate_castle,
            lambda state: (state.has(ItemName.progressive_powerup, player, 1)))
            
    connect(world, player, names, LocationName.sunken_ghost_ship_region, LocationName.sunken_ghost_ship,
            lambda state: state.has(ItemName.mario_swim, player))
    connect(world, player, names, LocationName.valley_of_bowser_1_region, LocationName.valley_of_bowser_1_exit_1)
    connect(world, player, names, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_exit_1)
    connect(world, player, names, LocationName.valley_of_bowser_2_region, LocationName.valley_of_bowser_2_exit_2,
            lambda state: state.has(ItemName.mario_carry, player))
    connect(world, player, names, LocationName.valley_of_bowser_3_region, LocationName.valley_of_bowser_3_exit_1)
    connect(world, player, names, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_exit_1,
            lambda state: state.has(ItemName.mario_climb, player))
    connect(world, player, names, LocationName.valley_of_bowser_4_region, LocationName.valley_of_bowser_4_exit_2,
            lambda state: (state.has(ItemName.mario_climb, player) and
                           state.has(ItemName.mario_carry, player) and
                           state.has(ItemName.yoshi_activate, player)))
    connect(world, player, names, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_exit_1,
            lambda state: state.has(ItemName.p_switch, player))
    connect(world, player, names, LocationName.valley_ghost_house_region, LocationName.valley_ghost_house_exit_2,
            lambda state: (state.has(ItemName.p_switch, player) and
                           state.has(ItemName.mario_carry, player) and
                           state.has(ItemName.mario_run, player)))
    connect(world, player, names, LocationName.valley_fortress_region, LocationName.valley_fortress,
            lambda state: state.has(ItemName.progressive_powerup, player, 1))
    connect(world, player, names, LocationName.valley_castle_region, LocationName.valley_castle)
    connect(world, player, names, LocationName.front_door, LocationName.bowser_region,
            lambda state: (state.has(ItemName.mario_climb, player) and
                           state.has(ItemName.mario_run, player) and
                           state.has(ItemName.mario_swim, player) and
                           state.has(ItemName.progressive_powerup, player, 1) and
                           state.has(ItemName.koopaling, player, world.bosses_required[player].value)))
    connect(world, player, names, LocationName.back_door, LocationName.bowser_region,
            lambda state: state.has(ItemName.koopaling, player, world.bosses_required[player].value))

    connect(world, player, names, LocationName.star_road_1_region, LocationName.star_road_1_exit_1,
            lambda state: (state.has(ItemName.mario_spin_jump, player) and
                           state.has(ItemName.progressive_powerup, player, 1)))
    connect(world, player, names, LocationName.star_road_1_region, LocationName.star_road_1_exit_2,
            lambda state: (state.has(ItemName.mario_spin_jump, player) and
                           state.has(ItemName.mario_carry, player) and
                           state.has(ItemName.progressive_powerup, player, 1)))
    connect(world, player, names, LocationName.star_road_2_region, LocationName.star_road_2_exit_1,
            lambda state: state.has(ItemName.mario_swim, player))
    connect(world, player, names, LocationName.star_road_2_region, LocationName.star_road_2_exit_2,
            lambda state: (state.has(ItemName.mario_swim, player) and
                           state.has(ItemName.mario_carry, player)))
    connect(world, player, names, LocationName.star_road_3_region, LocationName.star_road_3_exit_1)
    connect(world, player, names, LocationName.star_road_3_region, LocationName.star_road_3_exit_2,
            lambda state: state.has(ItemName.mario_carry, player))
    connect(world, player, names, LocationName.star_road_4_region, LocationName.star_road_4_exit_1)
    connect(world, player, names, LocationName.star_road_4_region, LocationName.star_road_4_exit_2,
            lambda state: (state.has(ItemName.mario_carry, player) and
                           (state.has(ItemName.yoshi_activate, player) or
                            (state.has(ItemName.green_switch_palace, player) and state.has(ItemName.red_switch_palace, player)))))
    connect(world, player, names, LocationName.star_road_5_region, LocationName.star_road_5_exit_1,
            lambda state: state.has(ItemName.p_switch, player))
    connect(world, player, names, LocationName.star_road_5_region, LocationName.star_road_5_exit_2,
            lambda state: (state.has(ItemName.mario_carry, player) and
                           state.has(ItemName.mario_climb, player) and
                           state.has(ItemName.p_switch, player) and
                           state.has(ItemName.yellow_switch_palace, player) and
                           state.has(ItemName.green_switch_palace, player) and
                           state.has(ItemName.red_switch_palace, player) and
                           state.has(ItemName.blue_switch_palace, player)))

    connect(world, player, names, LocationName.special_zone_1_region, LocationName.special_zone_1_exit_1,
            lambda state: (state.has(ItemName.mario_climb, player) and
                           (state.has(ItemName.p_switch, player) or
                            (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3)))))
    connect(world, player, names, LocationName.special_zone_2_region, LocationName.special_zone_2_exit_1,
            lambda state: state.has(ItemName.p_balloon, player))
    connect(world, player, names, LocationName.special_zone_3_region, LocationName.special_zone_3_exit_1,
            lambda state: (state.has(ItemName.mario_climb, player) or
                           state.has(ItemName.p_switch, player) or
                           (state.has(ItemName.mario_run, player) and state.has(ItemName.progressive_powerup, player, 3))))
    connect(world, player, names, LocationName.special_zone_4_region, LocationName.special_zone_4_exit_1,
            lambda state: state.has(ItemName.progressive_powerup, player, 1))
    connect(world, player, names, LocationName.special_zone_5_region, LocationName.special_zone_5_exit_1,
            lambda state: state.has(ItemName.progressive_powerup, player, 1))
    connect(world, player, names, LocationName.special_zone_6_region, LocationName.special_zone_6_exit_1,
            lambda state: state.has(ItemName.mario_swim, player))
    connect(world, player, names, LocationName.special_zone_7_region, LocationName.special_zone_7_exit_1,
            lambda state: state.has(ItemName.progressive_powerup, player, 1))
    connect(world, player, names, LocationName.special_zone_8_region, LocationName.special_zone_8_exit_1,
            lambda state: state.has(ItemName.progressive_powerup, player, 1))



    # Connect levels to each other
    for current_level_id, current_level_data in level_info_dict.items():
        # Connect tile regions to correct level regions

        if current_level_id not in level_to_tile_dict.keys():
            continue

        current_tile_id = level_to_tile_dict[current_level_id]
        current_tile_data = level_info_dict[current_tile_id]
        current_tile_name = current_tile_data.levelName
        if ("Star Road - " not in current_tile_name) and (" - Star Road" not in current_tile_name):
            current_tile_name += " - Tile"
            connect(world, player, names, current_tile_name, current_level_data.levelName)
        # Connect Exit regions to next tile regions
        if current_tile_data.exit1Path:
            next_tile_id = current_tile_data.exit1Path.otherLevelID
            if world.swap_donut_gh_exits[player] and current_tile_id == 0x04:
                next_tile_id = current_tile_data.exit2Path.otherLevelID
            next_tile_name = level_info_dict[next_tile_id].levelName
            if ("Star Road - " not in next_tile_name) and (" - Star Road" not in next_tile_name):
                next_tile_name += " - Tile"
            current_exit_name = (current_level_data.levelName + " - Normal Exit")
            connect(world, player, names, current_exit_name, next_tile_name)
        if current_tile_data.exit2Path:
            next_tile_id = current_tile_data.exit2Path.otherLevelID
            if world.swap_donut_gh_exits[player] and current_tile_id == 0x04:
                next_tile_id = current_tile_data.exit1Path.otherLevelID
            next_tile_name = level_info_dict[next_tile_id].levelName
            if ("Star Road - " not in next_tile_name) and (" - Star Road" not in next_tile_name):
                next_tile_name += " - Tile"
            current_exit_name = (current_level_data.levelName + " - Secret Exit")
            connect(world, player, names, current_exit_name, next_tile_name)

    connect(world, player, names, LocationName.donut_plains_star_road, LocationName.star_road_donut)
    connect(world, player, names, LocationName.star_road_donut, LocationName.donut_plains_star_road)
    connect(world, player, names, LocationName.star_road_donut, LocationName.star_road_1_tile)
    connect(world, player, names, LocationName.vanilla_dome_star_road, LocationName.star_road_vanilla)
    connect(world, player, names, LocationName.star_road_vanilla, LocationName.vanilla_dome_star_road)
    connect(world, player, names, LocationName.star_road_vanilla, LocationName.star_road_2_tile)
    connect(world, player, names, LocationName.twin_bridges_star_road, LocationName.star_road_twin_bridges)
    connect(world, player, names, LocationName.star_road_twin_bridges, LocationName.twin_bridges_star_road)
    connect(world, player, names, LocationName.star_road_twin_bridges, LocationName.star_road_3_tile)
    connect(world, player, names, LocationName.forest_star_road, LocationName.star_road_forest)
    connect(world, player, names, LocationName.star_road_forest, LocationName.forest_star_road)
    connect(world, player, names, LocationName.star_road_forest, LocationName.star_road_4_tile)
    connect(world, player, names, LocationName.valley_star_road, LocationName.star_road_valley)
    connect(world, player, names, LocationName.star_road_valley, LocationName.valley_star_road)
    connect(world, player, names, LocationName.star_road_valley, LocationName.star_road_5_tile)
    connect(world, player, names, LocationName.star_road_special, LocationName.special_star_road)
    connect(world, player, names, LocationName.special_star_road, LocationName.star_road_special)
    connect(world, player, names, LocationName.special_star_road, LocationName.special_zone_1_tile)
    
    connect(world, player, names, LocationName.star_road_valley, LocationName.front_door_tile)



def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, world)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = SMWLocation(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret

def add_location_to_region(world: MultiWorld, player: int, active_locations, region_name: str, location_name: str,
                           rule: typing.Optional[typing.Callable] = None):
    region = world.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = SMWLocation(player, location_name, loc_id, region)
        region.locations.append(location)
        if rule:
            add_rule(location, rule)



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
