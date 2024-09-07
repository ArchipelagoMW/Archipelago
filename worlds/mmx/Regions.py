from BaseClasses import MultiWorld, Region, ItemClassification
from .Locations import MMXLocation
from .Items import MMXItem
from .Names import LocationName, RegionName, EventName
from worlds.AutoWorld import World

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from . import MMXWorld


def create_regions(world: "MMXWorld", active_locations: Dict[int, str]) -> None:
    multiworld = world.multiworld
    player = world.player

    menu = create_region(multiworld, player, active_locations, 'Menu')

    intro = create_region(multiworld, player, active_locations, RegionName.intro)

    armored_armadillo = create_region(multiworld, player, active_locations, RegionName.armored_armadillo)
    armored_armadillo_ride_1 = create_region(multiworld, player, active_locations, RegionName.armored_armadillo_ride_1)
    armored_armadillo_excavator_1 = create_region(multiworld, player, active_locations, RegionName.armored_armadillo_excavator_1)
    armored_armadillo_ride_2 = create_region(multiworld, player, active_locations, RegionName.armored_armadillo_ride_2)
    armored_armadillo_excavator_2 = create_region(multiworld, player, active_locations, RegionName.armored_armadillo_excavator_2)
    armored_armadillo_ride_3 = create_region(multiworld, player, active_locations, RegionName.armored_armadillo_ride_3)
    armored_armadillo_boss = create_region(multiworld, player, active_locations, RegionName.armored_armadillo_boss)

    chill_penguin = create_region(multiworld, player, active_locations, RegionName.chill_penguin)
    chill_penguin_entrance = create_region(multiworld, player, active_locations, RegionName.chill_penguin_entrance)
    chill_penguin_icicles = create_region(multiworld, player, active_locations, RegionName.chill_penguin_icicles)
    chill_penguin_ride = create_region(multiworld, player, active_locations, RegionName.chill_penguin_ride)
    chill_penguin_boss = create_region(multiworld, player, active_locations, RegionName.chill_penguin_boss)

    spark_mandrill = create_region(multiworld, player, active_locations, RegionName.spark_mandrill)
    spark_mandrill_entrance = create_region(multiworld, player, active_locations, RegionName.spark_mandrill_entrance)
    spark_mandrill_mid_boss = create_region(multiworld, player, active_locations, RegionName.spark_mandrill_mid_boss)
    spark_mandrill_deep = create_region(multiworld, player, active_locations, RegionName.spark_mandrill_deep)
    spark_mandrill_boss = create_region(multiworld, player, active_locations, RegionName.spark_mandrill_boss)

    launch_octopus = create_region(multiworld, player, active_locations, RegionName.launch_octopus)
    launch_octopus_sea = create_region(multiworld, player, active_locations, RegionName.launch_octopus_sea)
    launch_octopus_base = create_region(multiworld, player, active_locations, RegionName.launch_octopus_base)
    launch_octopus_boss = create_region(multiworld, player, active_locations, RegionName.launch_octopus_boss)

    boomer_kuwanger = create_region(multiworld, player, active_locations, RegionName.boomer_kuwanger)
    boomer_kuwanger_basement = create_region(multiworld, player, active_locations, RegionName.boomer_kuwanger_basement)
    boomer_kuwanger_elevator = create_region(multiworld, player, active_locations, RegionName.boomer_kuwanger_elevator)
    boomer_kuwanger_outside = create_region(multiworld, player, active_locations, RegionName.boomer_kuwanger_outside)
    boomer_kuwanger_top = create_region(multiworld, player, active_locations, RegionName.boomer_kuwanger_top)
    boomer_kuwanger_boss = create_region(multiworld, player, active_locations, RegionName.boomer_kuwanger_boss)

    sting_chameleon = create_region(multiworld, player, active_locations, RegionName.sting_chameleon)
    sting_chameleon_forest = create_region(multiworld, player, active_locations, RegionName.sting_chameleon_forest)
    sting_chameleon_cave_top = create_region(multiworld, player, active_locations, RegionName.sting_chameleon_cave_top)
    sting_chameleon_cave = create_region(multiworld, player, active_locations, RegionName.sting_chameleon_cave)
    sting_chameleon_cave_bottom = create_region(multiworld, player, active_locations, RegionName.sting_chameleon_cave_bottom)
    sting_chameleon_hill = create_region(multiworld, player, active_locations, RegionName.sting_chameleon_hill)
    sting_chameleon_swamp = create_region(multiworld, player, active_locations, RegionName.sting_chameleon_swamp)
    sting_chameleon_boss = create_region(multiworld, player, active_locations, RegionName.sting_chameleon_boss)
    
    storm_eagle = create_region(multiworld, player, active_locations, RegionName.storm_eagle)
    storm_eagle_airport = create_region(multiworld, player, active_locations, RegionName.storm_eagle_airport)
    storm_eagle_glass = create_region(multiworld, player, active_locations, RegionName.storm_eagle_glass)
    storm_eagle_metal = create_region(multiworld, player, active_locations, RegionName.storm_eagle_metal)
    storm_eagle_aircraft = create_region(multiworld, player, active_locations, RegionName.storm_eagle_aircraft)
    storm_eagle_boss = create_region(multiworld, player, active_locations, RegionName.storm_eagle_boss)

    flame_mammoth = create_region(multiworld, player, active_locations, RegionName.flame_mammoth)
    flame_mammoth_conveyors_1 = create_region(multiworld, player, active_locations, RegionName.flame_mammoth_conveyors_1)
    flame_mammoth_lava_river_1 = create_region(multiworld, player, active_locations, RegionName.flame_mammoth_lava_river_1)
    flame_mammoth_conveyors_2 = create_region(multiworld, player, active_locations, RegionName.flame_mammoth_conveyors_2)
    flame_mammoth_lava_river_2 = create_region(multiworld, player, active_locations, RegionName.flame_mammoth_lava_river_2)
    flame_mammoth_boss = create_region(multiworld, player, active_locations, RegionName.flame_mammoth_boss)

    sigma_fortress = create_region(multiworld, player, active_locations, RegionName.sigma_fortress)

    sigma_fortress_1 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_1)
    sigma_fortress_1_outside = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_outside)
    sigma_fortress_1_vile = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_vile)
    sigma_fortress_1_vertical = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_vertical)
    sigma_fortress_1_rematch_1 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_rematch_1)
    sigma_fortress_1_before_boss = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_before_boss)
    sigma_fortress_1_boss = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_boss)
    
    sigma_fortress_2 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_2)
    sigma_fortress_2_start = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_start)
    sigma_fortress_2_rematch_1 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_rematch_1)
    sigma_fortress_2_ride = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_ride)
    sigma_fortress_2_rematch_2 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_rematch_2)
    sigma_fortress_2_before_boss = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_before_boss)
    sigma_fortress_2_boss = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_boss)

    sigma_fortress_3 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3)
    sigma_fortress_3_rematch_1 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_1)
    sigma_fortress_3_rematch_2 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_2)
    sigma_fortress_3_rematch_3 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_3)
    sigma_fortress_3_rematch_4 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_4)
    sigma_fortress_3_rematch_5 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_5)
    sigma_fortress_3_after_rematch_1 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_1)
    sigma_fortress_3_after_rematch_2 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_2)
    sigma_fortress_3_after_rematch_3 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_3)
    sigma_fortress_3_after_rematch_4 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_4)
    sigma_fortress_3_after_rematch_5 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_5)
    sigma_fortress_3_boss = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_boss)

    sigma_fortress_4 = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_4)
    sigma_fortress_4_dog = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_4_dog)
    sigma_fortress_4_sigma = create_region(multiworld, player, active_locations, RegionName.sigma_fortress_4_sigma)

    multiworld.regions += [
        menu,
        intro,
        armored_armadillo,
        armored_armadillo_ride_1,
        armored_armadillo_excavator_1,
        armored_armadillo_ride_2,
        armored_armadillo_excavator_2,
        armored_armadillo_ride_3,
        armored_armadillo_boss,
        chill_penguin,
        chill_penguin_entrance,
        chill_penguin_icicles,
        chill_penguin_ride,
        chill_penguin_boss,
        spark_mandrill,
        spark_mandrill_entrance,
        spark_mandrill_mid_boss,
        spark_mandrill_deep,
        spark_mandrill_boss,
        launch_octopus,
        launch_octopus_sea,
        launch_octopus_base,
        launch_octopus_boss,
        boomer_kuwanger,
        boomer_kuwanger_basement,
        boomer_kuwanger_elevator,
        boomer_kuwanger_outside,
        boomer_kuwanger_top,
        boomer_kuwanger_boss,
        sting_chameleon,
        sting_chameleon_forest,
        sting_chameleon_cave_top,
        sting_chameleon_cave,
        sting_chameleon_cave_bottom,
        sting_chameleon_hill,
        sting_chameleon_swamp,
        sting_chameleon_boss,
        storm_eagle,
        storm_eagle_airport,
        storm_eagle_glass,
        storm_eagle_metal,
        storm_eagle_aircraft,
        storm_eagle_boss,
        flame_mammoth,
        flame_mammoth_conveyors_1,
        flame_mammoth_lava_river_1,
        flame_mammoth_conveyors_2,
        flame_mammoth_lava_river_2,
        flame_mammoth_boss,
        sigma_fortress,
        sigma_fortress_1,
        sigma_fortress_1_outside,
        sigma_fortress_1_vile,
        sigma_fortress_1_vertical,
        sigma_fortress_1_rematch_1,
        sigma_fortress_1_before_boss,
        sigma_fortress_1_boss,
        sigma_fortress_2,
        sigma_fortress_2_start,
        sigma_fortress_2_rematch_1,
        sigma_fortress_2_ride,
        sigma_fortress_2_rematch_2,
        sigma_fortress_2_before_boss,
        sigma_fortress_2_boss,
        sigma_fortress_3,
        sigma_fortress_3_rematch_1,
        sigma_fortress_3_rematch_2,
        sigma_fortress_3_rematch_3,
        sigma_fortress_3_rematch_4,
        sigma_fortress_3_rematch_5,
        sigma_fortress_3_after_rematch_1,
        sigma_fortress_3_after_rematch_2,
        sigma_fortress_3_after_rematch_3,
        sigma_fortress_3_after_rematch_4,
        sigma_fortress_3_after_rematch_5,
        sigma_fortress_3_boss,
        sigma_fortress_4,
        sigma_fortress_4_dog,
        sigma_fortress_4_sigma,
    ]

    # Intro
    add_location_to_region(multiworld, player, active_locations, RegionName.intro, LocationName.intro_completed)
    add_location_to_region(multiworld, player, active_locations, RegionName.intro, LocationName.intro_mini_boss_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.intro, LocationName.intro_mini_boss_2)

    # Armored Armadillo
    add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_excavator_1, LocationName.armored_armadillo_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_excavator_1, LocationName.armored_armadillo_mini_boss_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_excavator_2, LocationName.armored_armadillo_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_excavator_2, LocationName.armored_armadillo_mini_boss_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_ride_3, LocationName.armored_armadillo_hadouken)
    add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_boss, LocationName.armored_armadillo_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_boss, LocationName.armored_armadillo_clear)
    add_event_to_region(multiworld, player, RegionName.armored_armadillo_boss, EventName.armored_armadillo_clear)
 
    # Chill Penguin
    add_location_to_region(multiworld, player, active_locations, RegionName.chill_penguin_ride, LocationName.chill_penguin_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.chill_penguin_icicles, LocationName.chill_penguin_legs)
    add_location_to_region(multiworld, player, active_locations, RegionName.chill_penguin_boss, LocationName.chill_penguin_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.chill_penguin_boss, LocationName.chill_penguin_clear)
    add_event_to_region(multiworld, player, RegionName.chill_penguin_boss, EventName.chill_penguin_clear)
 
    # Spark Mandrill
    add_location_to_region(multiworld, player, active_locations, RegionName.spark_mandrill_entrance, LocationName.spark_mandrill_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.spark_mandrill_mid_boss, LocationName.spark_mandrill_mini_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.spark_mandrill_deep, LocationName.spark_mandrill_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.spark_mandrill_boss, LocationName.spark_mandrill_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.spark_mandrill_boss, LocationName.spark_mandrill_clear)
    add_event_to_region(multiworld, player, RegionName.spark_mandrill_boss, EventName.spark_mandrill_clear)
 
    # Launch Octopus
    add_location_to_region(multiworld, player, active_locations, RegionName.launch_octopus_sea, LocationName.launch_octopus_mini_boss_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.launch_octopus_sea, LocationName.launch_octopus_mini_boss_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.launch_octopus_sea, LocationName.launch_octopus_mini_boss_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.launch_octopus_sea, LocationName.launch_octopus_mini_boss_4)
    add_location_to_region(multiworld, player, active_locations, RegionName.launch_octopus_base, LocationName.launch_octopus_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.launch_octopus_boss, LocationName.launch_octopus_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.launch_octopus_boss, LocationName.launch_octopus_clear)
    add_event_to_region(multiworld, player, RegionName.launch_octopus_boss, EventName.launch_octopus_clear)
 
    # Boomer Kuwanger
    add_location_to_region(multiworld, player, active_locations, RegionName.boomer_kuwanger_top, LocationName.boomer_kuwanger_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.boomer_kuwanger_boss, LocationName.boomer_kuwanger_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.boomer_kuwanger_boss, LocationName.boomer_kuwanger_clear)
    add_event_to_region(multiworld, player, RegionName.boomer_kuwanger_boss, EventName.boomer_kuwanger_clear)
 
    # Sting Chameleon
    add_location_to_region(multiworld, player, active_locations, RegionName.sting_chameleon_cave_bottom, LocationName.sting_chameleon_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.sting_chameleon_cave_top, LocationName.sting_chameleon_body)
    add_location_to_region(multiworld, player, active_locations, RegionName.sting_chameleon_boss, LocationName.sting_chameleon_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.sting_chameleon_boss, LocationName.sting_chameleon_clear)
    add_event_to_region(multiworld, player, RegionName.sting_chameleon_boss, EventName.sting_chameleon_clear)

    # Storm Eagle
    add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_airport, LocationName.storm_eagle_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_glass, LocationName.storm_eagle_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_metal, LocationName.storm_eagle_helmet)
    add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_boss, LocationName.storm_eagle_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_boss, LocationName.storm_eagle_clear)
    add_event_to_region(multiworld, player, RegionName.storm_eagle_boss, EventName.storm_eagle_clear)

    # Storm Eagle
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_mammoth_lava_river_1, LocationName.flame_mammoth_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_mammoth_lava_river_1, LocationName.flame_mammoth_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_mammoth_lava_river_1, LocationName.flame_mammoth_arms)
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_mammoth_boss, LocationName.flame_mammoth_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_mammoth_boss, LocationName.flame_mammoth_clear)
    add_event_to_region(multiworld, player, RegionName.flame_mammoth_boss, EventName.flame_mammoth_clear)

    # Sigma's Fortress 1
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_vile, LocationName.sigma_fortress_1_vile)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_rematch_1, LocationName.sigma_fortress_1_boomer_kuwanger)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_1_boss, LocationName.sigma_fortress_1_bospider)
    add_event_to_region(multiworld, player, RegionName.sigma_fortress_1_boss, EventName.sigma_fortress_1_clear)

    # Sigma's Fortress 2
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_rematch_1, LocationName.sigma_fortress_2_chill_penguin)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_rematch_2, LocationName.sigma_fortress_2_storm_eagle)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_2_boss, LocationName.sigma_fortress_2_rangda_bangda)
    add_event_to_region(multiworld, player, RegionName.sigma_fortress_2_boss, EventName.sigma_fortress_2_clear)

    # Sigma's Fortress 3
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_1, LocationName.sigma_fortress_3_armored_armadillo)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_2, LocationName.sigma_fortress_3_sting_chameleon)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_3, LocationName.sigma_fortress_3_spark_mandrill)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_4, LocationName.sigma_fortress_3_launch_octopus)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_rematch_5, LocationName.sigma_fortress_3_flame_mammoth)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_boss, LocationName.sigma_fortress_3_d_rex)
    add_event_to_region(multiworld, player, RegionName.sigma_fortress_3_boss, EventName.sigma_fortress_3_clear)

    # Sigma's Fortress 4
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_4_dog, LocationName.sigma_fortress_4_velguarder)
    add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_4_sigma, LocationName.sigma_fortress_4_sigma)

    if world.options.pickupsanity:
        add_location_to_region(multiworld, player, active_locations, RegionName.intro, LocationName.intro_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.intro, LocationName.intro_hp_2)

        # Armored Armadillo
        add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_excavator_1, LocationName.armored_armadillo_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_excavator_1, LocationName.armored_armadillo_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.armored_armadillo_ride_3, LocationName.armored_armadillo_hp_3)

        # Chill Penguin
        add_location_to_region(multiworld, player, active_locations, RegionName.chill_penguin_ride, LocationName.chill_penguin_hp_1)

        # Launch Octopus
        add_location_to_region(multiworld, player, active_locations, RegionName.launch_octopus_sea, LocationName.launch_octopus_hp_1)

        # Sting Chameleon
        add_location_to_region(multiworld, player, active_locations, RegionName.sting_chameleon_hill, LocationName.sting_chameleon_1up)
        add_location_to_region(multiworld, player, active_locations, RegionName.sting_chameleon_swamp, LocationName.sting_chameleon_hp_1)

        # Storm Eagle
        add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_airport, LocationName.storm_eagle_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_airport, LocationName.storm_eagle_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_airport, LocationName.storm_eagle_hp_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_airport, LocationName.storm_eagle_1up_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_metal, LocationName.storm_eagle_1up_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_metal, LocationName.storm_eagle_1up_2)
        #add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_aircraft, LocationName.storm_eagle_hp_4)
        #add_location_to_region(multiworld, player, active_locations, RegionName.storm_eagle_aircraft, LocationName.storm_eagle_energy_1)

        # Flame Mammoth
        add_location_to_region(multiworld, player, active_locations, RegionName.flame_mammoth_conveyors_1, LocationName.flame_mammoth_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.flame_mammoth_lava_river_1, LocationName.flame_mammoth_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.flame_mammoth_lava_river_1, LocationName.flame_mammoth_1up)

        # Sigma's Fortress 3
        add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_1, LocationName.sigma_fortress_3_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_2, LocationName.sigma_fortress_3_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_2, LocationName.sigma_fortress_3_energy_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_3, LocationName.sigma_fortress_3_hp_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_3, LocationName.sigma_fortress_3_energy_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_4, LocationName.sigma_fortress_3_hp_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_4, LocationName.sigma_fortress_3_energy_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.sigma_fortress_3_after_rematch_4, LocationName.sigma_fortress_3_1up)


def connect_regions(world: World) -> None:
    connect(world, "Menu", RegionName.intro)
    
    connect(world, RegionName.intro, RegionName.armored_armadillo)
    connect(world, RegionName.intro, RegionName.chill_penguin)
    connect(world, RegionName.intro, RegionName.spark_mandrill)
    connect(world, RegionName.intro, RegionName.launch_octopus)
    connect(world, RegionName.intro, RegionName.boomer_kuwanger)
    connect(world, RegionName.intro, RegionName.sting_chameleon)
    connect(world, RegionName.intro, RegionName.storm_eagle)
    connect(world, RegionName.intro, RegionName.flame_mammoth)

    connect(world, RegionName.armored_armadillo, RegionName.armored_armadillo_ride_1)
    connect(world, RegionName.armored_armadillo_ride_1, RegionName.armored_armadillo_excavator_1)
    connect(world, RegionName.armored_armadillo_excavator_1, RegionName.armored_armadillo_ride_2)
    connect(world, RegionName.armored_armadillo_ride_2, RegionName.armored_armadillo_excavator_2)
    connect(world, RegionName.armored_armadillo_excavator_2, RegionName.armored_armadillo_ride_3)
    connect(world, RegionName.armored_armadillo_ride_3, RegionName.armored_armadillo_boss)

    connect(world, RegionName.chill_penguin, RegionName.chill_penguin_entrance)
    connect(world, RegionName.chill_penguin_entrance, RegionName.chill_penguin_icicles)
    connect(world, RegionName.chill_penguin_icicles, RegionName.chill_penguin_ride)
    connect(world, RegionName.chill_penguin_ride, RegionName.chill_penguin_boss)
    
    connect(world, RegionName.spark_mandrill, RegionName.spark_mandrill_entrance)
    connect(world, RegionName.spark_mandrill_entrance, RegionName.spark_mandrill_mid_boss)
    connect(world, RegionName.spark_mandrill_mid_boss, RegionName.spark_mandrill_deep)
    connect(world, RegionName.spark_mandrill_deep, RegionName.spark_mandrill_boss)

    connect(world, RegionName.launch_octopus, RegionName.launch_octopus_sea)
    connect(world, RegionName.launch_octopus_sea, RegionName.launch_octopus_base)
    connect(world, RegionName.launch_octopus_sea, RegionName.launch_octopus_boss)

    connect(world, RegionName.boomer_kuwanger, RegionName.boomer_kuwanger_basement)
    connect(world, RegionName.boomer_kuwanger_basement, RegionName.boomer_kuwanger_elevator)
    connect(world, RegionName.boomer_kuwanger_elevator, RegionName.boomer_kuwanger_outside)
    connect(world, RegionName.boomer_kuwanger_outside, RegionName.boomer_kuwanger_top)
    connect(world, RegionName.boomer_kuwanger_top, RegionName.boomer_kuwanger_boss)

    connect(world, RegionName.sting_chameleon, RegionName.sting_chameleon_forest)
    connect(world, RegionName.sting_chameleon_forest, RegionName.sting_chameleon_cave)
    connect(world, RegionName.sting_chameleon_cave, RegionName.sting_chameleon_cave_top)
    connect(world, RegionName.sting_chameleon_cave, RegionName.sting_chameleon_cave_bottom)
    connect(world, RegionName.sting_chameleon_cave, RegionName.sting_chameleon_hill)
    connect(world, RegionName.sting_chameleon_hill, RegionName.sting_chameleon_swamp)
    connect(world, RegionName.sting_chameleon_swamp, RegionName.sting_chameleon_boss)

    connect(world, RegionName.storm_eagle, RegionName.storm_eagle_airport)
    connect(world, RegionName.storm_eagle_airport, RegionName.storm_eagle_glass)
    connect(world, RegionName.storm_eagle_glass, RegionName.storm_eagle_metal)
    connect(world, RegionName.storm_eagle_metal, RegionName.storm_eagle_aircraft)
    connect(world, RegionName.storm_eagle_aircraft, RegionName.storm_eagle_boss)

    connect(world, RegionName.flame_mammoth, RegionName.flame_mammoth_conveyors_1)
    connect(world, RegionName.flame_mammoth_conveyors_1, RegionName.flame_mammoth_lava_river_1)
    connect(world, RegionName.flame_mammoth_lava_river_1, RegionName.flame_mammoth_conveyors_2)
    connect(world, RegionName.flame_mammoth_conveyors_2, RegionName.flame_mammoth_lava_river_2)
    connect(world, RegionName.flame_mammoth_lava_river_2, RegionName.flame_mammoth_boss)

    connect(world, RegionName.intro, RegionName.sigma_fortress)

    connect(world, RegionName.sigma_fortress, RegionName.sigma_fortress_1)
    connect(world, RegionName.sigma_fortress_1, RegionName.sigma_fortress_1_outside)
    connect(world, RegionName.sigma_fortress_1_outside, RegionName.sigma_fortress_1_vile)
    connect(world, RegionName.sigma_fortress_1_vile, RegionName.sigma_fortress_1_vertical)
    connect(world, RegionName.sigma_fortress_1_vertical, RegionName.sigma_fortress_1_rematch_1)
    connect(world, RegionName.sigma_fortress_1_rematch_1, RegionName.sigma_fortress_1_before_boss)
    connect(world, RegionName.sigma_fortress_1_before_boss, RegionName.sigma_fortress_1_boss)

    connect(world, RegionName.sigma_fortress_2, RegionName.sigma_fortress_2_start)
    connect(world, RegionName.sigma_fortress_2_start, RegionName.sigma_fortress_2_rematch_1)
    connect(world, RegionName.sigma_fortress_2_rematch_1, RegionName.sigma_fortress_2_ride)
    connect(world, RegionName.sigma_fortress_2_ride, RegionName.sigma_fortress_2_rematch_2)
    connect(world, RegionName.sigma_fortress_2_rematch_2, RegionName.sigma_fortress_2_before_boss)
    connect(world, RegionName.sigma_fortress_2_before_boss, RegionName.sigma_fortress_2_boss)

    connect(world, RegionName.sigma_fortress_3, RegionName.sigma_fortress_3_rematch_1)
    connect(world, RegionName.sigma_fortress_3_rematch_1, RegionName.sigma_fortress_3_after_rematch_1)
    connect(world, RegionName.sigma_fortress_3_after_rematch_1, RegionName.sigma_fortress_3_rematch_2)
    connect(world, RegionName.sigma_fortress_3_rematch_2, RegionName.sigma_fortress_3_after_rematch_2)
    connect(world, RegionName.sigma_fortress_3_after_rematch_2, RegionName.sigma_fortress_3_rematch_3)
    connect(world, RegionName.sigma_fortress_3_rematch_3, RegionName.sigma_fortress_3_after_rematch_3)
    connect(world, RegionName.sigma_fortress_3_after_rematch_3, RegionName.sigma_fortress_3_rematch_4)
    connect(world, RegionName.sigma_fortress_3_rematch_4, RegionName.sigma_fortress_3_after_rematch_4)
    connect(world, RegionName.sigma_fortress_3_after_rematch_4, RegionName.sigma_fortress_3_rematch_5)
    connect(world, RegionName.sigma_fortress_3_rematch_5, RegionName.sigma_fortress_3_after_rematch_5)
    connect(world, RegionName.sigma_fortress_3_after_rematch_5, RegionName.sigma_fortress_3_boss)

    connect(world, RegionName.sigma_fortress_4, RegionName.sigma_fortress_4_dog)
    connect(world, RegionName.sigma_fortress_4_dog, RegionName.sigma_fortress_4_sigma)
    
    if world.options.sigma_all_levels:
        connect(world, RegionName.sigma_fortress, RegionName.sigma_fortress_2)
        connect(world, RegionName.sigma_fortress, RegionName.sigma_fortress_3)
        connect(world, RegionName.sigma_fortress, RegionName.sigma_fortress_4)
    else:
        connect(world, RegionName.sigma_fortress_1_boss, RegionName.sigma_fortress_2)
        connect(world, RegionName.sigma_fortress_2_boss, RegionName.sigma_fortress_3)
        connect(world, RegionName.sigma_fortress_3_boss, RegionName.sigma_fortress_4)

    # Connect checkpoints
    if world.options.logic_helmet_checkpoints.value:
        connect(world, RegionName.spark_mandrill, RegionName.spark_mandrill_deep)

        connect(world, RegionName.sigma_fortress_1, RegionName.sigma_fortress_1_vertical)
        connect(world, RegionName.sigma_fortress_1, RegionName.sigma_fortress_1_before_boss)

        connect(world, RegionName.sigma_fortress_2, RegionName.sigma_fortress_2_ride)
        connect(world, RegionName.sigma_fortress_2, RegionName.sigma_fortress_2_before_boss)

        connect(world, RegionName.sigma_fortress_3, RegionName.sigma_fortress_3_after_rematch_1)
        connect(world, RegionName.sigma_fortress_3, RegionName.sigma_fortress_3_after_rematch_2)
        connect(world, RegionName.sigma_fortress_3, RegionName.sigma_fortress_3_after_rematch_3)
        connect(world, RegionName.sigma_fortress_3, RegionName.sigma_fortress_3_after_rematch_4)
        connect(world, RegionName.sigma_fortress_3, RegionName.sigma_fortress_3_after_rematch_5)


def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None) -> Region:
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = MMXLocation(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret


def add_event_to_region(multiworld: MultiWorld, player: int, region_name: str, event_name: str, event_item=None) -> None:
    region = multiworld.get_region(region_name, player)
    event = MMXLocation(player, event_name, None, region)
    if event_item:
        event.place_locked_item(MMXItem(event_item, ItemClassification.progression, None, player))
    else:
        event.place_locked_item(MMXItem(event_name, ItemClassification.progression, None, player))
    region.locations.append(event)


def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str) -> None:
    region = multiworld.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = MMXLocation(player, location_name, loc_id, region)
        region.locations.append(location)


def connect(world: World, source: str, target: str) -> None:
    source_region: Region = world.multiworld.get_region(source, world.player)
    target_region: Region = world.multiworld.get_region(target, world.player)
    source_region.connect(target_region)
