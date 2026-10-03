from typing import Dict
from BaseClasses import MultiWorld, Region


# I Tried turning this into a for loop a list of all the rooms, but it would skip rooms ocaionaly so I just left it like this
def create_regions(multiworld: MultiWorld, player: int) -> Dict[str, Region]:

    # Create Menu region
    menu = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)

    arbiters_grounds_entrance = Region("Arbiters Grounds Entrance", player, multiworld)
    multiworld.regions.append(arbiters_grounds_entrance)

    arbiters_grounds_lobby = Region("Arbiters Grounds Lobby", player, multiworld)
    multiworld.regions.append(arbiters_grounds_lobby)

    arbiters_grounds_east_wing = Region(
        "Arbiters Grounds East Wing", player, multiworld
    )
    multiworld.regions.append(arbiters_grounds_east_wing)

    arbiters_grounds_west_wing = Region(
        "Arbiters Grounds West Wing", player, multiworld
    )
    multiworld.regions.append(arbiters_grounds_west_wing)

    arbiters_grounds_after_poe_gate = Region(
        "Arbiters Grounds After Poe Gate", player, multiworld
    )
    multiworld.regions.append(arbiters_grounds_after_poe_gate)

    arbiters_grounds_boss_room = Region(
        "Arbiters Grounds Boss Room", player, multiworld
    )
    multiworld.regions.append(arbiters_grounds_boss_room)

    city_in_the_sky_boss_room = Region("City in The Sky Boss Room", player, multiworld)
    multiworld.regions.append(city_in_the_sky_boss_room)

    city_in_the_sky_central_tower_second_floor = Region(
        "City in The Sky Central Tower Second Floor", player, multiworld
    )
    multiworld.regions.append(city_in_the_sky_central_tower_second_floor)

    city_in_the_sky_east_wing = Region("City in The Sky East Wing", player, multiworld)
    multiworld.regions.append(city_in_the_sky_east_wing)

    city_in_the_sky_entrance = Region("City in The Sky Entrance", player, multiworld)
    multiworld.regions.append(city_in_the_sky_entrance)

    city_in_the_sky_lobby = Region("City in The Sky Lobby", player, multiworld)
    multiworld.regions.append(city_in_the_sky_lobby)

    city_in_the_sky_north_wing = Region(
        "City in The Sky North Wing", player, multiworld
    )
    multiworld.regions.append(city_in_the_sky_north_wing)

    city_in_the_sky_west_wing = Region("City in The Sky West Wing", player, multiworld)
    multiworld.regions.append(city_in_the_sky_west_wing)

    forest_temple_boss_room = Region("Forest Temple Boss Room", player, multiworld)
    multiworld.regions.append(forest_temple_boss_room)

    forest_temple_east_wing = Region("Forest Temple East Wing", player, multiworld)
    multiworld.regions.append(forest_temple_east_wing)

    forest_temple_entrance = Region("Forest Temple Entrance", player, multiworld)
    multiworld.regions.append(forest_temple_entrance)

    forest_temple_lobby = Region("Forest Temple Lobby", player, multiworld)
    multiworld.regions.append(forest_temple_lobby)

    forest_temple_north_wing = Region("Forest Temple North Wing", player, multiworld)
    multiworld.regions.append(forest_temple_north_wing)

    forest_temple_west_wing = Region("Forest Temple West Wing", player, multiworld)
    multiworld.regions.append(forest_temple_west_wing)

    ook = Region("Ook", player, multiworld)
    multiworld.regions.append(ook)

    goron_mines_boss_room = Region("Goron Mines Boss Room", player, multiworld)
    multiworld.regions.append(goron_mines_boss_room)

    goron_mines_crystal_switch_room = Region(
        "Goron Mines Crystal Switch Room", player, multiworld
    )
    multiworld.regions.append(goron_mines_crystal_switch_room)

    goron_mines_entrance = Region("Goron Mines Entrance", player, multiworld)
    multiworld.regions.append(goron_mines_entrance)

    goron_mines_lower_west_wing = Region(
        "Goron Mines Lower West Wing", player, multiworld
    )
    multiworld.regions.append(goron_mines_lower_west_wing)

    goron_mines_magnet_room = Region("Goron Mines Magnet Room", player, multiworld)
    multiworld.regions.append(goron_mines_magnet_room)

    goron_mines_north_wing = Region("Goron Mines North Wing", player, multiworld)
    multiworld.regions.append(goron_mines_north_wing)

    goron_mines_upper_east_wing = Region(
        "Goron Mines Upper East Wing", player, multiworld
    )
    multiworld.regions.append(goron_mines_upper_east_wing)

    ganondorf_castle = Region("Ganondorf Castle", player, multiworld)
    multiworld.regions.append(ganondorf_castle)

    hyrule_castle_entrance = Region("Hyrule Castle Entrance", player, multiworld)
    multiworld.regions.append(hyrule_castle_entrance)

    hyrule_castle_graveyard = Region("Hyrule Castle Graveyard", player, multiworld)
    multiworld.regions.append(hyrule_castle_graveyard)

    hyrule_castle_inside_east_wing = Region(
        "Hyrule Castle Inside East Wing", player, multiworld
    )
    multiworld.regions.append(hyrule_castle_inside_east_wing)

    hyrule_castle_inside_west_wing = Region(
        "Hyrule Castle Inside West Wing", player, multiworld
    )
    multiworld.regions.append(hyrule_castle_inside_west_wing)

    hyrule_castle_main_hall = Region("Hyrule Castle Main Hall", player, multiworld)
    multiworld.regions.append(hyrule_castle_main_hall)

    hyrule_castle_outside_east_wing = Region(
        "Hyrule Castle Outside East Wing", player, multiworld
    )
    multiworld.regions.append(hyrule_castle_outside_east_wing)

    hyrule_castle_outside_west_wing = Region(
        "Hyrule Castle Outside West Wing", player, multiworld
    )
    multiworld.regions.append(hyrule_castle_outside_west_wing)

    hyrule_castle_third_floor_balcony = Region(
        "Hyrule Castle Third Floor Balcony", player, multiworld
    )
    multiworld.regions.append(hyrule_castle_third_floor_balcony)

    hyrule_castle_tower_climb = Region("Hyrule Castle Tower Climb", player, multiworld)
    multiworld.regions.append(hyrule_castle_tower_climb)

    hyrule_castle_treasure_room = Region(
        "Hyrule Castle Treasure Room", player, multiworld
    )
    multiworld.regions.append(hyrule_castle_treasure_room)

    lakebed_temple_boss_room = Region("Lakebed Temple Boss Room", player, multiworld)
    multiworld.regions.append(lakebed_temple_boss_room)

    lakebed_temple_central_room = Region(
        "Lakebed Temple Central Room", player, multiworld
    )
    multiworld.regions.append(lakebed_temple_central_room)

    lakebed_temple_east_wing_first_floor = Region(
        "Lakebed Temple East Wing First Floor", player, multiworld
    )
    multiworld.regions.append(lakebed_temple_east_wing_first_floor)

    lakebed_temple_east_wing_second_floor = Region(
        "Lakebed Temple East Wing Second Floor", player, multiworld
    )
    multiworld.regions.append(lakebed_temple_east_wing_second_floor)

    lakebed_temple_entrance = Region("Lakebed Temple Entrance", player, multiworld)
    multiworld.regions.append(lakebed_temple_entrance)

    lakebed_temple_west_wing = Region("Lakebed Temple West Wing", player, multiworld)
    multiworld.regions.append(lakebed_temple_west_wing)

    palace_of_twilight_entrance = Region(
        "Palace of Twilight Entrance", player, multiworld
    )
    multiworld.regions.append(palace_of_twilight_entrance)

    palace_of_twilight_west_wing = Region(
        "Palace of Twilight West Wing", player, multiworld
    )
    multiworld.regions.append(palace_of_twilight_west_wing)

    palace_of_twilight_east_wing = Region(
        "Palace of Twilight East Wing", player, multiworld
    )
    multiworld.regions.append(palace_of_twilight_east_wing)

    palace_of_twilight_central_first_room = Region(
        "Palace of Twilight Central First Room", player, multiworld
    )
    multiworld.regions.append(palace_of_twilight_central_first_room)

    palace_of_twilight_outside_room = Region(
        "Palace of Twilight Outside Room", player, multiworld
    )
    multiworld.regions.append(palace_of_twilight_outside_room)

    palace_of_twilight_north_tower = Region(
        "Palace of Twilight North Tower", player, multiworld
    )
    multiworld.regions.append(palace_of_twilight_north_tower)

    palace_of_twilight_boss_room = Region(
        "Palace of Twilight Boss Room", player, multiworld
    )
    multiworld.regions.append(palace_of_twilight_boss_room)

    snowpeak_ruins_left_door = Region("Snowpeak Ruins Left Door", player, multiworld)
    multiworld.regions.append(snowpeak_ruins_left_door)

    snowpeak_ruins_right_door = Region("Snowpeak Ruins Right Door", player, multiworld)
    multiworld.regions.append(snowpeak_ruins_right_door)

    snowpeak_ruins_boss_room = Region("Snowpeak Ruins Boss Room", player, multiworld)
    multiworld.regions.append(snowpeak_ruins_boss_room)

    snowpeak_ruins_caged_freezard_room = Region(
        "Snowpeak Ruins Caged Freezard Room", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_caged_freezard_room)

    snowpeak_ruins_caged_freezard_room_lower = Region(
        "Snowpeak Ruins Caged Freezard Room Lower", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_caged_freezard_room_lower)

    snowpeak_ruins_chapel = Region("Snowpeak Ruins Chapel", player, multiworld)
    multiworld.regions.append(snowpeak_ruins_chapel)

    snowpeak_ruins_darkhammer_room = Region(
        "Snowpeak Ruins Darkhammer Room", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_darkhammer_room)

    snowpeak_ruins_east_courtyard = Region(
        "Snowpeak Ruins East Courtyard", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_east_courtyard)

    snowpeak_ruins_entrance = Region("Snowpeak Ruins Entrance", player, multiworld)
    multiworld.regions.append(snowpeak_ruins_entrance)

    snowpeak_ruins_northeast_chilfos_room_first_floor = Region(
        "Snowpeak Ruins Northeast Chilfos Room First Floor", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_northeast_chilfos_room_first_floor)

    snowpeak_ruins_northeast_chilfos_room_second_floor = Region(
        "Snowpeak Ruins Northeast Chilfos Room Second Floor", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_northeast_chilfos_room_second_floor)

    snowpeak_ruins_second_floor_mini_freezard_room = Region(
        "Snowpeak Ruins Second Floor Mini Freezard Room", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_second_floor_mini_freezard_room)

    snowpeak_ruins_west_cannon_room = Region(
        "Snowpeak Ruins West Cannon Room", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_west_cannon_room)

    snowpeak_ruins_west_courtyard = Region(
        "Snowpeak Ruins West Courtyard", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_west_courtyard)

    snowpeak_ruins_wooden_beam_room = Region(
        "Snowpeak Ruins Wooden Beam Room", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_wooden_beam_room)

    snowpeak_ruins_yeto_and_yeta = Region(
        "Snowpeak Ruins Yeto and Yeta", player, multiworld
    )
    multiworld.regions.append(snowpeak_ruins_yeto_and_yeta)

    temple_of_time_armos_antechamber = Region(
        "Temple of Time Armos Antechamber", player, multiworld
    )
    multiworld.regions.append(temple_of_time_armos_antechamber)

    temple_of_time_boss_room = Region("Temple of Time Boss Room", player, multiworld)
    multiworld.regions.append(temple_of_time_boss_room)

    temple_of_time_central_mechanical_platform = Region(
        "Temple of Time Central Mechanical Platform", player, multiworld
    )
    multiworld.regions.append(temple_of_time_central_mechanical_platform)

    temple_of_time_connecting_corridors = Region(
        "Temple of Time Connecting Corridors", player, multiworld
    )
    multiworld.regions.append(temple_of_time_connecting_corridors)

    temple_of_time_crumbling_corridor = Region(
        "Temple of Time Crumbling Corridor", player, multiworld
    )
    multiworld.regions.append(temple_of_time_crumbling_corridor)

    temple_of_time_darknut_arena = Region(
        "Temple of Time Darknut Arena", player, multiworld
    )
    multiworld.regions.append(temple_of_time_darknut_arena)

    temple_of_time_entrance = Region("Temple of Time Entrance", player, multiworld)
    multiworld.regions.append(temple_of_time_entrance)

    temple_of_time_floor_switch_puzzle_room = Region(
        "Temple of Time Floor Switch Puzzle Room", player, multiworld
    )
    multiworld.regions.append(temple_of_time_floor_switch_puzzle_room)

    temple_of_time_moving_wall_hallways = Region(
        "Temple of Time Moving Wall Hallways", player, multiworld
    )
    multiworld.regions.append(temple_of_time_moving_wall_hallways)

    temple_of_time_scales_of_time = Region(
        "Temple of Time Scales of Time", player, multiworld
    )
    multiworld.regions.append(temple_of_time_scales_of_time)

    temple_of_time_upper_spike_trap_corridor = Region(
        "Temple of Time Upper Spike Trap Corridor", player, multiworld
    )
    multiworld.regions.append(temple_of_time_upper_spike_trap_corridor)

    death_mountain_near_kakariko = Region(
        "Death Mountain Near Kakariko", player, multiworld
    )
    multiworld.regions.append(death_mountain_near_kakariko)

    death_mountain_trail = Region("Death Mountain Trail", player, multiworld)
    multiworld.regions.append(death_mountain_trail)

    death_mountain_volcano = Region("Death Mountain Volcano", player, multiworld)
    multiworld.regions.append(death_mountain_volcano)

    death_mountain_outside_sumo_hall = Region(
        "Death Mountain Outside Sumo Hall", player, multiworld
    )
    multiworld.regions.append(death_mountain_outside_sumo_hall)

    death_mountain_elevator_lower = Region(
        "Death Mountain Elevator Lower", player, multiworld
    )
    multiworld.regions.append(death_mountain_elevator_lower)

    death_mountain_sumo_hall = Region("Death Mountain Sumo Hall", player, multiworld)
    multiworld.regions.append(death_mountain_sumo_hall)

    death_mountain_sumo_hall_elevator = Region(
        "Death Mountain Sumo Hall Elevator", player, multiworld
    )
    multiworld.regions.append(death_mountain_sumo_hall_elevator)

    death_mountain_sumo_hall_goron_mines_tunnel = Region(
        "Death Mountain Sumo Hall Goron Mines Tunnel", player, multiworld
    )
    multiworld.regions.append(death_mountain_sumo_hall_goron_mines_tunnel)

    hidden_village = Region("Hidden Village", player, multiworld)
    multiworld.regions.append(hidden_village)

    hidden_village_impaz_house = Region(
        "Hidden Village Impaz House", player, multiworld
    )
    multiworld.regions.append(hidden_village_impaz_house)

    kakariko_gorge = Region("Kakariko Gorge", player, multiworld)
    multiworld.regions.append(kakariko_gorge)

    kakariko_gorge_cave_entrance = Region(
        "Kakariko Gorge Cave Entrance", player, multiworld
    )
    multiworld.regions.append(kakariko_gorge_cave_entrance)

    kakariko_gorge_behind_gate = Region(
        "Kakariko Gorge Behind Gate", player, multiworld
    )
    multiworld.regions.append(kakariko_gorge_behind_gate)

    eldin_lantern_cave = Region("Eldin Lantern Cave", player, multiworld)
    multiworld.regions.append(eldin_lantern_cave)

    kakariko_gorge_keese_grotto = Region(
        "Kakariko Gorge Keese Grotto", player, multiworld
    )
    multiworld.regions.append(kakariko_gorge_keese_grotto)

    eldin_field = Region("Eldin Field", player, multiworld)
    multiworld.regions.append(eldin_field)

    eldin_field_near_castle_town = Region(
        "Eldin Field Near Castle Town", player, multiworld
    )
    multiworld.regions.append(eldin_field_near_castle_town)

    eldin_field_lava_cave_ledge = Region(
        "Eldin Field Lava Cave Ledge", player, multiworld
    )
    multiworld.regions.append(eldin_field_lava_cave_ledge)

    eldin_field_from_lava_cave_lower = Region(
        "Eldin Field From Lava Cave Lower", player, multiworld
    )
    multiworld.regions.append(eldin_field_from_lava_cave_lower)

    north_eldin_field = Region("North Eldin Field", player, multiworld)
    multiworld.regions.append(north_eldin_field)

    eldin_field_outside_hidden_village = Region(
        "Eldin Field Outside Hidden Village", player, multiworld
    )
    multiworld.regions.append(eldin_field_outside_hidden_village)

    eldin_field_grotto_platform = Region(
        "Eldin Field Grotto Platform", player, multiworld
    )
    multiworld.regions.append(eldin_field_grotto_platform)

    eldin_field_lava_cave_upper = Region(
        "Eldin Field Lava Cave Upper", player, multiworld
    )
    multiworld.regions.append(eldin_field_lava_cave_upper)

    eldin_field_lava_cave_lower = Region(
        "Eldin Field Lava Cave Lower", player, multiworld
    )
    multiworld.regions.append(eldin_field_lava_cave_lower)

    eldin_field_bomskit_grotto = Region(
        "Eldin Field Bomskit Grotto", player, multiworld
    )
    multiworld.regions.append(eldin_field_bomskit_grotto)

    eldin_field_water_bomb_fish_grotto = Region(
        "Eldin Field Water Bomb Fish Grotto", player, multiworld
    )
    multiworld.regions.append(eldin_field_water_bomb_fish_grotto)

    eldin_field_stalfos_grotto = Region(
        "Eldin Field Stalfos Grotto", player, multiworld
    )
    multiworld.regions.append(eldin_field_stalfos_grotto)

    lower_kakariko_village = Region("Lower Kakariko Village", player, multiworld)
    multiworld.regions.append(lower_kakariko_village)

    upper_kakariko_village = Region("Upper Kakariko Village", player, multiworld)
    multiworld.regions.append(upper_kakariko_village)

    kakariko_top_of_watchtower = Region(
        "Kakariko Top of Watchtower", player, multiworld
    )
    multiworld.regions.append(kakariko_top_of_watchtower)

    kakariko_village_behind_gate = Region(
        "Kakariko Village Behind Gate", player, multiworld
    )
    multiworld.regions.append(kakariko_village_behind_gate)

    kakariko_renados_sanctuary_front_left_door = Region(
        "Kakariko Renados Sanctuary Front Left Door", player, multiworld
    )
    multiworld.regions.append(kakariko_renados_sanctuary_front_left_door)

    kakariko_renados_sanctuary_front_right_door = Region(
        "Kakariko Renados Sanctuary Front Right Door", player, multiworld
    )
    multiworld.regions.append(kakariko_renados_sanctuary_front_right_door)

    kakariko_renados_sanctuary_back_left_door = Region(
        "Kakariko Renados Sanctuary Back Left Door", player, multiworld
    )
    multiworld.regions.append(kakariko_renados_sanctuary_back_left_door)

    kakariko_renados_sanctuary_back_right_door = Region(
        "Kakariko Renados Sanctuary Back Right Door", player, multiworld
    )
    multiworld.regions.append(kakariko_renados_sanctuary_back_right_door)

    kakariko_renados_sanctuary = Region(
        "Kakariko Renados Sanctuary", player, multiworld
    )
    multiworld.regions.append(kakariko_renados_sanctuary)

    kakariko_renados_sanctuary_basement = Region(
        "Kakariko Renados Sanctuary Basement", player, multiworld
    )
    multiworld.regions.append(kakariko_renados_sanctuary_basement)

    kakariko_malo_mart = Region("Kakariko Malo Mart", player, multiworld)
    multiworld.regions.append(kakariko_malo_mart)

    kakariko_elde_inn_left_door = Region(
        "Kakariko Elde Inn Left Door", player, multiworld
    )
    multiworld.regions.append(kakariko_elde_inn_left_door)

    kakariko_elde_inn_right_door = Region(
        "Kakariko Elde Inn Right Door", player, multiworld
    )
    multiworld.regions.append(kakariko_elde_inn_right_door)

    kakariko_elde_inn = Region("Kakariko Elde Inn", player, multiworld)
    multiworld.regions.append(kakariko_elde_inn)

    kakariko_bug_house_door = Region("Kakariko Bug House Door", player, multiworld)
    multiworld.regions.append(kakariko_bug_house_door)

    kakariko_bug_house_ceiling_hole = Region(
        "Kakariko Bug House Ceiling Hole", player, multiworld
    )
    multiworld.regions.append(kakariko_bug_house_ceiling_hole)

    kakariko_bug_house = Region("Kakariko Bug House", player, multiworld)
    multiworld.regions.append(kakariko_bug_house)

    kakariko_barnes_bomb_shop_lower = Region(
        "Kakariko Barnes Bomb Shop Lower", player, multiworld
    )
    multiworld.regions.append(kakariko_barnes_bomb_shop_lower)

    kakariko_barnes_bomb_shop_upper = Region(
        "Kakariko Barnes Bomb Shop Upper", player, multiworld
    )
    multiworld.regions.append(kakariko_barnes_bomb_shop_upper)

    kakariko_watchtower_lower_door = Region(
        "Kakariko Watchtower Lower Door", player, multiworld
    )
    multiworld.regions.append(kakariko_watchtower_lower_door)

    kakariko_watchtower_dig_spot = Region(
        "Kakariko Watchtower Dig Spot", player, multiworld
    )
    multiworld.regions.append(kakariko_watchtower_dig_spot)

    kakariko_watchtower_upper_door = Region(
        "Kakariko Watchtower Upper Door", player, multiworld
    )
    multiworld.regions.append(kakariko_watchtower_upper_door)

    kakariko_watchtower = Region("Kakariko Watchtower", player, multiworld)
    multiworld.regions.append(kakariko_watchtower)

    kakariko_graveyard = Region("Kakariko Graveyard", player, multiworld)
    multiworld.regions.append(kakariko_graveyard)

    south_faron_woods = Region("South Faron Woods", player, multiworld)
    multiworld.regions.append(south_faron_woods)

    south_faron_woods_behind_gate = Region(
        "South Faron Woods Behind Gate", player, multiworld
    )
    multiworld.regions.append(south_faron_woods_behind_gate)

    south_faron_woods_coros_ledge = Region(
        "South Faron Woods Coros Ledge", player, multiworld
    )
    multiworld.regions.append(south_faron_woods_coros_ledge)

    south_faron_woods_owl_statue_area = Region(
        "South Faron Woods Owl Statue Area", player, multiworld
    )
    multiworld.regions.append(south_faron_woods_owl_statue_area)

    south_faron_woods_above_owl_statue = Region(
        "South Faron Woods Above Owl Statue", player, multiworld
    )
    multiworld.regions.append(south_faron_woods_above_owl_statue)

    faron_woods_coros_house_lower = Region(
        "Faron Woods Coros House Lower", player, multiworld
    )
    multiworld.regions.append(faron_woods_coros_house_lower)

    faron_woods_coros_house_upper = Region(
        "Faron Woods Coros House Upper", player, multiworld
    )
    multiworld.regions.append(faron_woods_coros_house_upper)

    faron_woods_cave_southern_entrance = Region(
        "Faron Woods Cave Southern Entrance", player, multiworld
    )
    multiworld.regions.append(faron_woods_cave_southern_entrance)

    faron_woods_cave = Region("Faron Woods Cave", player, multiworld)
    multiworld.regions.append(faron_woods_cave)

    mist_area_near_faron_woods_cave = Region(
        "Mist Area Near Faron Woods Cave", player, multiworld
    )
    multiworld.regions.append(mist_area_near_faron_woods_cave)

    mist_area_inside_mist = Region("Mist Area Inside Mist", player, multiworld)
    multiworld.regions.append(mist_area_inside_mist)

    mist_area_under_owl_statue_chest = Region(
        "Mist Area Under Owl Statue Chest", player, multiworld
    )
    multiworld.regions.append(mist_area_under_owl_statue_chest)

    mist_area_near_owl_statue_chest = Region(
        "Mist Area Near Owl Statue Chest", player, multiworld
    )
    multiworld.regions.append(mist_area_near_owl_statue_chest)

    mist_area_center_stump = Region("Mist Area Center Stump", player, multiworld)
    multiworld.regions.append(mist_area_center_stump)

    mist_area_outside_faron_mist_cave = Region(
        "Mist Area Outside Faron Mist Cave", player, multiworld
    )
    multiworld.regions.append(mist_area_outside_faron_mist_cave)

    mist_area_near_north_faron_woods = Region(
        "Mist Area Near North Faron Woods", player, multiworld
    )
    multiworld.regions.append(mist_area_near_north_faron_woods)

    faron_woods_cave_northern_entrance = Region(
        "Faron Woods Cave Northern Entrance", player, multiworld
    )
    multiworld.regions.append(faron_woods_cave_northern_entrance)

    mist_area_faron_mist_cave = Region("Mist Area Faron Mist Cave", player, multiworld)
    multiworld.regions.append(mist_area_faron_mist_cave)

    north_faron_woods = Region("North Faron Woods", player, multiworld)
    multiworld.regions.append(north_faron_woods)

    faron_field = Region("Faron Field", player, multiworld)
    multiworld.regions.append(faron_field)

    faron_field_behind_boulder = Region(
        "Faron Field Behind Boulder", player, multiworld
    )
    multiworld.regions.append(faron_field_behind_boulder)

    faron_field_corner_grotto = Region("Faron Field Corner Grotto", player, multiworld)
    multiworld.regions.append(faron_field_corner_grotto)

    faron_field_fishing_grotto = Region(
        "Faron Field Fishing Grotto", player, multiworld
    )
    multiworld.regions.append(faron_field_fishing_grotto)

    lost_woods = Region("Lost Woods", player, multiworld)
    multiworld.regions.append(lost_woods)

    lost_woods_lower_battle_arena = Region(
        "Lost Woods Lower Battle Arena", player, multiworld
    )
    multiworld.regions.append(lost_woods_lower_battle_arena)

    lost_woods_upper_battle_arena = Region(
        "Lost Woods Upper Battle Arena", player, multiworld
    )
    multiworld.regions.append(lost_woods_upper_battle_arena)

    lost_woods_baba_serpent_grotto = Region(
        "Lost Woods Baba Serpent Grotto", player, multiworld
    )
    multiworld.regions.append(lost_woods_baba_serpent_grotto)

    sacred_grove_before_block = Region("Sacred Grove Before Block", player, multiworld)
    multiworld.regions.append(sacred_grove_before_block)

    sacred_grove_upper = Region("Sacred Grove Upper", player, multiworld)
    multiworld.regions.append(sacred_grove_upper)

    sacred_grove_lower = Region("Sacred Grove Lower", player, multiworld)
    multiworld.regions.append(sacred_grove_lower)

    sacred_grove_past = Region("Sacred Grove Past", player, multiworld)
    multiworld.regions.append(sacred_grove_past)

    sacred_grove_past_behind_window = Region(
        "Sacred Grove Past Behind Window", player, multiworld
    )
    multiworld.regions.append(sacred_grove_past_behind_window)

    gerudo_desert_cave_of_ordeals_floors_01_11 = Region(
        "Gerudo Desert Cave of Ordeals Floors 01-11", player, multiworld
    )
    multiworld.regions.append(gerudo_desert_cave_of_ordeals_floors_01_11)

    gerudo_desert_cave_of_ordeals_floors_12_21 = Region(
        "Gerudo Desert Cave of Ordeals Floors 12-21", player, multiworld
    )
    multiworld.regions.append(gerudo_desert_cave_of_ordeals_floors_12_21)

    gerudo_desert_cave_of_ordeals_floors_22_31 = Region(
        "Gerudo Desert Cave of Ordeals Floors 22-31", player, multiworld
    )

    multiworld.regions.append(gerudo_desert_cave_of_ordeals_floors_22_31)

    gerudo_desert_cave_of_ordeals_floors_32_41 = Region(
        "Gerudo Desert Cave of Ordeals Floors 32-41", player, multiworld
    )
    multiworld.regions.append(gerudo_desert_cave_of_ordeals_floors_32_41)

    gerudo_desert_cave_of_ordeals_floors_42_50 = Region(
        "Gerudo Desert Cave of Ordeals Floors 42-50", player, multiworld
    )
    multiworld.regions.append(gerudo_desert_cave_of_ordeals_floors_42_50)

    gerudo_desert = Region("Gerudo Desert", player, multiworld)
    multiworld.regions.append(gerudo_desert)

    gerudo_desert_cave_of_ordeals_plateau = Region(
        "Gerudo Desert Cave of Ordeals Plateau", player, multiworld
    )
    multiworld.regions.append(gerudo_desert_cave_of_ordeals_plateau)

    gerudo_desert_basin = Region("Gerudo Desert Basin", player, multiworld)
    multiworld.regions.append(gerudo_desert_basin)

    gerudo_desert_north_east_ledge = Region(
        "Gerudo Desert North East Ledge", player, multiworld
    )
    multiworld.regions.append(gerudo_desert_north_east_ledge)

    gerudo_desert_outside_bulblin_camp = Region(
        "Gerudo Desert Outside Bulblin Camp", player, multiworld
    )
    multiworld.regions.append(gerudo_desert_outside_bulblin_camp)

    gerudo_desert_skulltula_grotto = Region(
        "Gerudo Desert Skulltula Grotto", player, multiworld
    )
    multiworld.regions.append(gerudo_desert_skulltula_grotto)

    gerudo_desert_chu_grotto = Region("Gerudo Desert Chu Grotto", player, multiworld)
    multiworld.regions.append(gerudo_desert_chu_grotto)

    gerudo_desert_rock_grotto = Region("Gerudo Desert Rock Grotto", player, multiworld)
    multiworld.regions.append(gerudo_desert_rock_grotto)

    bulblin_camp = Region("Bulblin Camp", player, multiworld)
    multiworld.regions.append(bulblin_camp)

    outside_arbiters_grounds = Region("Outside Arbiters Grounds", player, multiworld)
    multiworld.regions.append(outside_arbiters_grounds)

    mirror_chamber_lower = Region("Mirror Chamber Lower", player, multiworld)
    multiworld.regions.append(mirror_chamber_lower)

    mirror_chamber_upper = Region("Mirror Chamber Upper", player, multiworld)
    multiworld.regions.append(mirror_chamber_upper)

    mirror_chamber_portal = Region("Mirror of Twilight", player, multiworld)
    multiworld.regions.append(mirror_chamber_portal)

    castle_town_west = Region("Castle Town West", player, multiworld)
    multiworld.regions.append(castle_town_west)

    castle_town_star_game = Region("Castle Town STAR Game", player, multiworld)
    multiworld.regions.append(castle_town_star_game)

    castle_town_center = Region("Castle Town Center", player, multiworld)
    multiworld.regions.append(castle_town_center)

    castle_town_goron_house_left_door = Region(
        "Castle Town Goron House Left Door", player, multiworld
    )
    multiworld.regions.append(castle_town_goron_house_left_door)

    castle_town_goron_house_right_door = Region(
        "Castle Town Goron House Right Door", player, multiworld
    )
    multiworld.regions.append(castle_town_goron_house_right_door)

    castle_town_goron_house = Region("Castle Town Goron House", player, multiworld)
    multiworld.regions.append(castle_town_goron_house)

    castle_town_malo_mart = Region("Castle Town Malo Mart", player, multiworld)
    multiworld.regions.append(castle_town_malo_mart)

    castle_town_north = Region("Castle Town North", player, multiworld)
    multiworld.regions.append(castle_town_north)

    castle_town_north_behind_first_door = Region(
        "Castle Town North Behind First Door", player, multiworld
    )
    multiworld.regions.append(castle_town_north_behind_first_door)

    castle_town_north_inside_barrier = Region(
        "Castle Town North Inside Barrier", player, multiworld
    )
    multiworld.regions.append(castle_town_north_inside_barrier)

    castle_town_east = Region("Castle Town East", player, multiworld)
    multiworld.regions.append(castle_town_east)

    castle_town_doctors_office_balcony = Region(
        "Castle Town Doctors Office Balcony", player, multiworld
    )
    multiworld.regions.append(castle_town_doctors_office_balcony)

    castle_town_doctors_office_left_door = Region(
        "Castle Town Doctors Office Left Door", player, multiworld
    )
    multiworld.regions.append(castle_town_doctors_office_left_door)

    castle_town_doctors_office_right_door = Region(
        "Castle Town Doctors Office Right Door", player, multiworld
    )
    multiworld.regions.append(castle_town_doctors_office_right_door)

    castle_town_doctors_office_entrance = Region(
        "Castle Town Doctors Office Entrance", player, multiworld
    )
    multiworld.regions.append(castle_town_doctors_office_entrance)

    castle_town_doctors_office_lower = Region(
        "Castle Town Doctors Office Lower", player, multiworld
    )
    multiworld.regions.append(castle_town_doctors_office_lower)

    castle_town_doctors_office_upper = Region(
        "Castle Town Doctors Office Upper", player, multiworld
    )
    multiworld.regions.append(castle_town_doctors_office_upper)

    castle_town_south = Region("Castle Town South", player, multiworld)
    multiworld.regions.append(castle_town_south)

    castle_town_agithas_house = Region("Castle Town Agithas House", player, multiworld)
    multiworld.regions.append(castle_town_agithas_house)

    castle_town_seer_house = Region("Castle Town Seer House", player, multiworld)
    multiworld.regions.append(castle_town_seer_house)

    castle_town_jovanis_house = Region("Castle Town Jovanis House", player, multiworld)
    multiworld.regions.append(castle_town_jovanis_house)

    castle_town_telmas_bar = Region("Castle Town Telmas Bar", player, multiworld)
    multiworld.regions.append(castle_town_telmas_bar)

    lanayru_field = Region("Lanayru Field", player, multiworld)
    multiworld.regions.append(lanayru_field)

    lanayru_field_cave_entrance = Region(
        "Lanayru Field Cave Entrance", player, multiworld
    )
    multiworld.regions.append(lanayru_field_cave_entrance)

    lanayru_field_behind_boulder = Region(
        "Lanayru Field Behind Boulder", player, multiworld
    )
    multiworld.regions.append(lanayru_field_behind_boulder)

    hyrule_field_near_spinner_rails = Region(
        "Hyrule Field Near Spinner Rails", player, multiworld
    )
    multiworld.regions.append(hyrule_field_near_spinner_rails)

    lanayru_ice_puzzle_cave = Region("Lanayru Ice Puzzle Cave", player, multiworld)
    multiworld.regions.append(lanayru_ice_puzzle_cave)

    lanayru_field_chu_grotto = Region("Lanayru Field Chu Grotto", player, multiworld)
    multiworld.regions.append(lanayru_field_chu_grotto)

    lanayru_field_skulltula_grotto = Region(
        "Lanayru Field Skulltula Grotto", player, multiworld
    )
    multiworld.regions.append(lanayru_field_skulltula_grotto)

    lanayru_field_poe_grotto = Region("Lanayru Field Poe Grotto", player, multiworld)
    multiworld.regions.append(lanayru_field_poe_grotto)

    outside_castle_town_west = Region("Outside Castle Town West", player, multiworld)
    multiworld.regions.append(outside_castle_town_west)

    outside_castle_town_west_grotto_ledge = Region(
        "Outside Castle Town West Grotto Ledge", player, multiworld
    )
    multiworld.regions.append(outside_castle_town_west_grotto_ledge)

    outside_castle_town_west_helmasaur_grotto = Region(
        "Outside Castle Town West Helmasaur Grotto", player, multiworld
    )

    multiworld.regions.append(outside_castle_town_west_helmasaur_grotto)

    outside_castle_town_east = Region("Outside Castle Town East", player, multiworld)
    multiworld.regions.append(outside_castle_town_east)

    outside_castle_town_south = Region("Outside Castle Town South", player, multiworld)
    multiworld.regions.append(outside_castle_town_south)

    outside_castle_town_south_inside_boulder = Region(
        "Outside Castle Town South Inside Boulder", player, multiworld
    )
    multiworld.regions.append(outside_castle_town_south_inside_boulder)

    outside_castle_town_south_tektite_grotto = Region(
        "Outside Castle Town South Tektite Grotto", player, multiworld
    )
    multiworld.regions.append(outside_castle_town_south_tektite_grotto)

    lake_hylia_bridge = Region("Lake Hylia Bridge", player, multiworld)
    multiworld.regions.append(lake_hylia_bridge)

    lake_hylia_bridge_grotto_ledge = Region(
        "Lake Hylia Bridge Grotto Ledge", player, multiworld
    )
    multiworld.regions.append(lake_hylia_bridge_grotto_ledge)

    lake_hylia_bridge_bubble_grotto = Region(
        "Lake Hylia Bridge Bubble Grotto", player, multiworld
    )
    multiworld.regions.append(lake_hylia_bridge_bubble_grotto)

    lake_hylia = Region("Lake Hylia", player, multiworld)
    multiworld.regions.append(lake_hylia)

    lake_hylia_cave_entrance = Region("Lake Hylia Cave Entrance", player, multiworld)
    multiworld.regions.append(lake_hylia_cave_entrance)

    lake_hylia_lakebed_temple_entrance = Region(
        "Lake Hylia Lakebed Temple Entrance", player, multiworld
    )
    multiworld.regions.append(lake_hylia_lakebed_temple_entrance)

    lake_hylia_lanayru_spring = Region("Lake Hylia Lanayru Spring", player, multiworld)
    multiworld.regions.append(lake_hylia_lanayru_spring)

    lake_hylia_long_cave = Region("Lake Hylia Long Cave", player, multiworld)
    multiworld.regions.append(lake_hylia_long_cave)

    lake_hylia_shell_blade_grotto = Region(
        "Lake Hylia Shell Blade Grotto", player, multiworld
    )
    multiworld.regions.append(lake_hylia_shell_blade_grotto)

    lake_hylia_water_toadpoli_grotto = Region(
        "Lake Hylia Water Toadpoli Grotto", player, multiworld
    )
    multiworld.regions.append(lake_hylia_water_toadpoli_grotto)

    upper_zoras_river = Region("Upper Zoras River", player, multiworld)
    multiworld.regions.append(upper_zoras_river)

    upper_zoras_river_izas_house = Region(
        "Upper Zoras River Izas House", player, multiworld
    )
    multiworld.regions.append(upper_zoras_river_izas_house)

    fishing_hole = Region("Fishing Hole", player, multiworld)
    multiworld.regions.append(fishing_hole)

    fishing_hole_house = Region("Fishing Hole House", player, multiworld)
    multiworld.regions.append(fishing_hole_house)

    zoras_domain = Region("Zoras Domain", player, multiworld)
    multiworld.regions.append(zoras_domain)

    zoras_domain_west_ledge = Region("Zoras Domain West Ledge", player, multiworld)
    multiworld.regions.append(zoras_domain_west_ledge)

    zoras_throne_room = Region("Zoras Domain Throne Room", player, multiworld)
    multiworld.regions.append(zoras_throne_room)

    outside_links_house = Region("Outside Links House", player, multiworld)
    multiworld.regions.append(outside_links_house)

    ordon_links_house = Region("Ordon Links House", player, multiworld)
    multiworld.regions.append(ordon_links_house)

    ordon_village = Region("Ordon Village", player, multiworld)
    multiworld.regions.append(ordon_village)

    ordon_seras_shop = Region("Ordon Seras Shop", player, multiworld)
    multiworld.regions.append(ordon_seras_shop)

    ordon_shield_house = Region("Ordon Shield House", player, multiworld)
    multiworld.regions.append(ordon_shield_house)

    ordon_sword_house = Region("Ordon Sword House", player, multiworld)
    multiworld.regions.append(ordon_sword_house)

    ordon_bos_house_left_door = Region("Ordon Bos House Left Door", player, multiworld)
    multiworld.regions.append(ordon_bos_house_left_door)

    ordon_bos_house_right_door = Region(
        "Ordon Bos House Right Door", player, multiworld
    )
    multiworld.regions.append(ordon_bos_house_right_door)

    ordon_bos_house = Region("Ordon Bos House", player, multiworld)
    multiworld.regions.append(ordon_bos_house)

    ordon_ranch_entrance = Region("Ordon Ranch Entrance", player, multiworld)
    multiworld.regions.append(ordon_ranch_entrance)

    ordon_ranch = Region("Ordon Ranch", player, multiworld)
    multiworld.regions.append(ordon_ranch)

    ordon_ranch_stable = Region("Ordon Ranch Stable", player, multiworld)
    multiworld.regions.append(ordon_ranch_stable)

    ordon_ranch_grotto = Region("Ordon Ranch Grotto", player, multiworld)
    multiworld.regions.append(ordon_ranch_grotto)

    ordon_spring = Region("Ordon Spring", player, multiworld)
    multiworld.regions.append(ordon_spring)

    ordon_bridge = Region("Ordon Bridge", player, multiworld)
    multiworld.regions.append(ordon_bridge)

    snowpeak_climb_lower = Region("Snowpeak Climb Lower", player, multiworld)
    multiworld.regions.append(snowpeak_climb_lower)

    snowpeak_climb_upper = Region("Snowpeak Climb Upper", player, multiworld)
    multiworld.regions.append(snowpeak_climb_upper)

    snowpeak_ice_keese_grotto = Region("Snowpeak Ice Keese Grotto", player, multiworld)
    multiworld.regions.append(snowpeak_ice_keese_grotto)

    snowpeak_freezard_grotto = Region("Snowpeak Freezard Grotto", player, multiworld)
    multiworld.regions.append(snowpeak_freezard_grotto)

    snowpeak_summit_upper = Region("Snowpeak Summit Upper", player, multiworld)
    multiworld.regions.append(snowpeak_summit_upper)

    snowpeak_summit_lower = Region("Snowpeak Summit Lower", player, multiworld)
    multiworld.regions.append(snowpeak_summit_lower)
