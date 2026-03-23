import typing

from BaseClasses import Region, Entrance
from worlds.AutoWorld import World
from .Locations import DKC3Location
from .Names import LocationName, ItemName


def create_regions(world: World, active_locations):
    menu_region = create_region(world, active_locations, 'Menu', None)

    overworld_1_region_locations = {}
    if world.options.goal != "knautilus":
        overworld_1_region_locations.update({LocationName.banana_bird_mother: []})
    overworld_1_region = create_region(world, active_locations, LocationName.overworld_1_region,
                                       overworld_1_region_locations)

    overworld_2_region_locations = {}
    overworld_2_region = create_region(world, active_locations, LocationName.overworld_2_region,
                                       overworld_2_region_locations)

    overworld_3_region_locations = {}
    overworld_3_region = create_region(world, active_locations, LocationName.overworld_3_region,
                                       overworld_3_region_locations)

    overworld_4_region_locations = {}
    overworld_4_region = create_region(world, active_locations, LocationName.overworld_4_region,
                                       overworld_4_region_locations)


    lake_orangatanga_region = create_region(world, active_locations, LocationName.lake_orangatanga_region, None)
    kremwood_forest_region = create_region(world, active_locations, LocationName.kremwood_forest_region, None)
    cotton_top_cove_region = create_region(world, active_locations, LocationName.cotton_top_cove_region, None)
    mekanos_region = create_region(world, active_locations, LocationName.mekanos_region, None)
    k3_region = create_region(world, active_locations, LocationName.k3_region, None)
    razor_ridge_region = create_region(world, active_locations, LocationName.razor_ridge_region, None)
    kaos_kore_region = create_region(world, active_locations, LocationName.kaos_kore_region, None)
    krematoa_region = create_region(world, active_locations, LocationName.krematoa_region, None)


    lakeside_limbo_region_locations = {
        LocationName.lakeside_limbo_flag    : [0x657, 1],
        LocationName.lakeside_limbo_bonus_1 : [0x657, 2],
        LocationName.lakeside_limbo_bonus_2 : [0x657, 3],
        LocationName.lakeside_limbo_dk      : [0x657, 5],
    }
    if world.options.kongsanity:
        lakeside_limbo_region_locations[LocationName.lakeside_limbo_kong] = []
    lakeside_limbo_region = create_region(world, active_locations, LocationName.lakeside_limbo_region,
                                          lakeside_limbo_region_locations)

    doorstop_dash_region_locations = {
        LocationName.doorstop_dash_flag    : [0x65A, 1],
        LocationName.doorstop_dash_bonus_1 : [0x65A, 2],
        LocationName.doorstop_dash_bonus_2 : [0x65A, 3],
        LocationName.doorstop_dash_dk      : [0x65A, 5],
    }
    if world.options.kongsanity:
        doorstop_dash_region_locations[LocationName.doorstop_dash_kong] = []
    doorstop_dash_region = create_region(world, active_locations, LocationName.doorstop_dash_region,
                                         doorstop_dash_region_locations)

    tidal_trouble_region_locations = {
        LocationName.tidal_trouble_flag    : [0x659, 1],
        LocationName.tidal_trouble_bonus_1 : [0x659, 2],
        LocationName.tidal_trouble_bonus_2 : [0x659, 3],
        LocationName.tidal_trouble_dk      : [0x659, 5],
    }
    if world.options.kongsanity:
        tidal_trouble_region_locations[LocationName.tidal_trouble_kong] = []
    tidal_trouble_region = create_region(world, active_locations, LocationName.tidal_trouble_region,
                                         tidal_trouble_region_locations)

    skiddas_row_region_locations = {
        LocationName.skiddas_row_flag    : [0x65D, 1],
        LocationName.skiddas_row_bonus_1 : [0x65D, 2],
        LocationName.skiddas_row_bonus_2 : [0x65D, 3],
        LocationName.skiddas_row_dk      : [0x65D, 5],
    }
    if world.options.kongsanity:
        skiddas_row_region_locations[LocationName.skiddas_row_kong] = []
    skiddas_row_region = create_region(world, active_locations, LocationName.skiddas_row_region,
                                       skiddas_row_region_locations)

    murky_mill_region_locations = {
        LocationName.murky_mill_flag    : [0x65C, 1],
        LocationName.murky_mill_bonus_1 : [0x65C, 2],
        LocationName.murky_mill_bonus_2 : [0x65C, 3],
        LocationName.murky_mill_dk      : [0x65C, 5],
    }
    if world.options.kongsanity:
        murky_mill_region_locations[LocationName.murky_mill_kong] = []
    murky_mill_region = create_region(world, active_locations, LocationName.murky_mill_region,
                                      murky_mill_region_locations)

    barrel_shield_bust_up_region_locations = {
        LocationName.barrel_shield_bust_up_flag     : [0x662, 1],
        LocationName.barrel_shield_bust_up_bonus_1  : [0x662, 2],
        LocationName.barrel_shield_bust_up_bonus_2  : [0x662, 3],
        LocationName.barrel_shield_bust_up_dk       : [0x662, 5],
    }
    if world.options.kongsanity:
        barrel_shield_bust_up_region_locations[LocationName.barrel_shield_bust_up_kong] = []
    barrel_shield_bust_up_region = create_region(world, active_locations,
                                                 LocationName.barrel_shield_bust_up_region,
                                                 barrel_shield_bust_up_region_locations)

    riverside_race_region_locations = {
        LocationName.riverside_race_flag    : [0x664, 1],
        LocationName.riverside_race_bonus_1 : [0x664, 2],
        LocationName.riverside_race_bonus_2 : [0x664, 3],
        LocationName.riverside_race_dk      : [0x664, 5],
    }
    if world.options.kongsanity:
        riverside_race_region_locations[LocationName.riverside_race_kong] = []
    riverside_race_region = create_region(world, active_locations, LocationName.riverside_race_region,
                                          riverside_race_region_locations)

    squeals_on_wheels_region_locations = {
        LocationName.squeals_on_wheels_flag    : [0x65B, 1],
        LocationName.squeals_on_wheels_bonus_1 : [0x65B, 2],
        LocationName.squeals_on_wheels_bonus_2 : [0x65B, 3],
        LocationName.squeals_on_wheels_dk      : [0x65B, 5],
    }
    if world.options.kongsanity:
        squeals_on_wheels_region_locations[LocationName.squeals_on_wheels_kong] = []
    squeals_on_wheels_region = create_region(world, active_locations, LocationName.squeals_on_wheels_region,
                                             squeals_on_wheels_region_locations)

    springin_spiders_region_locations = {
        LocationName.springin_spiders_flag    : [0x661, 1],
        LocationName.springin_spiders_bonus_1 : [0x661, 2],
        LocationName.springin_spiders_bonus_2 : [0x661, 3],
        LocationName.springin_spiders_dk      : [0x661, 5],
    }
    if world.options.kongsanity:
        springin_spiders_region_locations[LocationName.springin_spiders_kong] = []
    springin_spiders_region = create_region(world, active_locations, LocationName.springin_spiders_region,
                                            springin_spiders_region_locations)

    bobbing_barrel_brawl_region_locations = {
        LocationName.bobbing_barrel_brawl_flag     : [0x666, 1],
        LocationName.bobbing_barrel_brawl_bonus_1  : [0x666, 2],
        LocationName.bobbing_barrel_brawl_bonus_2  : [0x666, 3],
        LocationName.bobbing_barrel_brawl_dk       : [0x666, 5],
    }
    if world.options.kongsanity:
        bobbing_barrel_brawl_region_locations[LocationName.bobbing_barrel_brawl_kong] = []
    bobbing_barrel_brawl_region = create_region(world, active_locations,
                                                LocationName.bobbing_barrel_brawl_region,
                                                bobbing_barrel_brawl_region_locations)

    bazzas_blockade_region_locations = {
        LocationName.bazzas_blockade_flag    : [0x667, 1],
        LocationName.bazzas_blockade_bonus_1 : [0x667, 2],
        LocationName.bazzas_blockade_bonus_2 : [0x667, 3],
        LocationName.bazzas_blockade_dk      : [0x667, 5],
    }
    if world.options.kongsanity:
        bazzas_blockade_region_locations[LocationName.bazzas_blockade_kong] = []
    bazzas_blockade_region = create_region(world, active_locations, LocationName.bazzas_blockade_region,
                                           bazzas_blockade_region_locations)

    rocket_barrel_ride_region_locations = {
        LocationName.rocket_barrel_ride_flag    : [0x66A, 1],
        LocationName.rocket_barrel_ride_bonus_1 : [0x66A, 2],
        LocationName.rocket_barrel_ride_bonus_2 : [0x66A, 3],
        LocationName.rocket_barrel_ride_dk      : [0x66A, 5],
    }
    if world.options.kongsanity:
        rocket_barrel_ride_region_locations[LocationName.rocket_barrel_ride_kong] = []
    rocket_barrel_ride_region = create_region(world, active_locations, LocationName.rocket_barrel_ride_region,
                                              rocket_barrel_ride_region_locations)

    kreeping_klasps_region_locations = {
        LocationName.kreeping_klasps_flag     : [0x658, 1],
        LocationName.kreeping_klasps_bonus_1  : [0x658, 2],
        LocationName.kreeping_klasps_bonus_2  : [0x658, 3],
        LocationName.kreeping_klasps_dk       : [0x658, 5],
    }
    if world.options.kongsanity:
        kreeping_klasps_region_locations[LocationName.kreeping_klasps_kong] = []
    kreeping_klasps_region = create_region(world, active_locations, LocationName.kreeping_klasps_region,
                                           kreeping_klasps_region_locations)

    tracker_barrel_trek_region_locations = {
        LocationName.tracker_barrel_trek_flag    : [0x66B, 1],
        LocationName.tracker_barrel_trek_bonus_1 : [0x66B, 2],
        LocationName.tracker_barrel_trek_bonus_2 : [0x66B, 3],
        LocationName.tracker_barrel_trek_dk      : [0x66B, 5],
    }
    if world.options.kongsanity:
        tracker_barrel_trek_region_locations[LocationName.tracker_barrel_trek_kong] = []
    tracker_barrel_trek_region = create_region(world, active_locations, LocationName.tracker_barrel_trek_region,
                                               tracker_barrel_trek_region_locations)

    fish_food_frenzy_region_locations = {
        LocationName.fish_food_frenzy_flag    : [0x668, 1],
        LocationName.fish_food_frenzy_bonus_1 : [0x668, 2],
        LocationName.fish_food_frenzy_bonus_2 : [0x668, 3],
        LocationName.fish_food_frenzy_dk      : [0x668, 5],
    }
    if world.options.kongsanity:
        fish_food_frenzy_region_locations[LocationName.fish_food_frenzy_kong] = []
    fish_food_frenzy_region = create_region(world, active_locations, LocationName.fish_food_frenzy_region,
                                            fish_food_frenzy_region_locations)

    fire_ball_frenzy_region_locations = {
        LocationName.fire_ball_frenzy_flag    : [0x66D, 1],
        LocationName.fire_ball_frenzy_bonus_1 : [0x66D, 2],
        LocationName.fire_ball_frenzy_bonus_2 : [0x66D, 3],
        LocationName.fire_ball_frenzy_dk      : [0x66D, 5],
    }
    if world.options.kongsanity:
        fire_ball_frenzy_region_locations[LocationName.fire_ball_frenzy_kong] = []
    fire_ball_frenzy_region = create_region(world, active_locations, LocationName.fire_ball_frenzy_region,
                                            fire_ball_frenzy_region_locations)

    demolition_drain_pipe_region_locations = {
        LocationName.demolition_drain_pipe_flag    : [0x672, 1],
        LocationName.demolition_drain_pipe_bonus_1 : [0x672, 2],
        LocationName.demolition_drain_pipe_bonus_2 : [0x672, 3],
        LocationName.demolition_drain_pipe_dk      : [0x672, 5],
    }
    if world.options.kongsanity:
        demolition_drain_pipe_region_locations[LocationName.demolition_drain_pipe_kong] = []
    demolition_drain_pipe_region = create_region(world, active_locations,
                                                 LocationName.demolition_drain_pipe_region,
                                                 demolition_drain_pipe_region_locations)

    ripsaw_rage_region_locations = {
        LocationName.ripsaw_rage_flag    : [0x660, 1],
        LocationName.ripsaw_rage_bonus_1 : [0x660, 2],
        LocationName.ripsaw_rage_bonus_2 : [0x660, 3],
        LocationName.ripsaw_rage_dk      : [0x660, 5],
    }
    if world.options.kongsanity:
        ripsaw_rage_region_locations[LocationName.ripsaw_rage_kong] = []
    ripsaw_rage_region = create_region(world, active_locations, LocationName.ripsaw_rage_region,
                                       ripsaw_rage_region_locations)

    blazing_bazookas_region_locations = {
        LocationName.blazing_bazookas_flag    : [0x66E, 1],
        LocationName.blazing_bazookas_bonus_1 : [0x66E, 2],
        LocationName.blazing_bazookas_bonus_2 : [0x66E, 3],
        LocationName.blazing_bazookas_dk      : [0x66E, 5],
    }
    if world.options.kongsanity:
        blazing_bazookas_region_locations[LocationName.blazing_bazookas_kong] = []
    blazing_bazookas_region = create_region(world, active_locations, LocationName.blazing_bazookas_region,
                                            blazing_bazookas_region_locations)

    low_g_labyrinth_region_locations = {
        LocationName.low_g_labyrinth_flag     : [0x670, 1],
        LocationName.low_g_labyrinth_bonus_1  : [0x670, 2],
        LocationName.low_g_labyrinth_bonus_2  : [0x670, 3],
        LocationName.low_g_labyrinth_dk       : [0x670, 5],
    }
    if world.options.kongsanity:
        low_g_labyrinth_region_locations[LocationName.low_g_labyrinth_kong] = []
    low_g_labyrinth_region = create_region(world, active_locations, LocationName.low_g_labyrinth_region,
                                           low_g_labyrinth_region_locations)

    krevice_kreepers_region_locations = {
        LocationName.krevice_kreepers_flag    : [0x673, 1],
        LocationName.krevice_kreepers_bonus_1 : [0x673, 2],
        LocationName.krevice_kreepers_bonus_2 : [0x673, 3],
        LocationName.krevice_kreepers_dk      : [0x673, 5],
    }
    if world.options.kongsanity:
        krevice_kreepers_region_locations[LocationName.krevice_kreepers_kong] = []
    krevice_kreepers_region = create_region(world, active_locations, LocationName.krevice_kreepers_region,
                                            krevice_kreepers_region_locations)

    tearaway_toboggan_region_locations = {
        LocationName.tearaway_toboggan_flag    : [0x65F, 1],
        LocationName.tearaway_toboggan_bonus_1 : [0x65F, 2],
        LocationName.tearaway_toboggan_bonus_2 : [0x65F, 3],
        LocationName.tearaway_toboggan_dk      : [0x65F, 5],
    }
    if world.options.kongsanity:
        tearaway_toboggan_region_locations[LocationName.tearaway_toboggan_kong] = []
    tearaway_toboggan_region = create_region(world, active_locations, LocationName.tearaway_toboggan_region,
                                             tearaway_toboggan_region_locations)

    barrel_drop_bounce_region_locations = {
        LocationName.barrel_drop_bounce_flag    : [0x66C, 1],
        LocationName.barrel_drop_bounce_bonus_1 : [0x66C, 2],
        LocationName.barrel_drop_bounce_bonus_2 : [0x66C, 3],
        LocationName.barrel_drop_bounce_dk      : [0x66C, 5],
    }
    if world.options.kongsanity:
        barrel_drop_bounce_region_locations[LocationName.barrel_drop_bounce_kong] = []
    barrel_drop_bounce_region = create_region(world, active_locations, LocationName.barrel_drop_bounce_region,
                                              barrel_drop_bounce_region_locations)

    krack_shot_kroc_region_locations = {
        LocationName.krack_shot_kroc_flag    : [0x66F, 1],
        LocationName.krack_shot_kroc_bonus_1 : [0x66F, 2],
        LocationName.krack_shot_kroc_bonus_2 : [0x66F, 3],
        LocationName.krack_shot_kroc_dk      : [0x66F, 5],
    }
    if world.options.kongsanity:
        krack_shot_kroc_region_locations[LocationName.krack_shot_kroc_kong] = []
    krack_shot_kroc_region = create_region(world, active_locations, LocationName.krack_shot_kroc_region,
                                           krack_shot_kroc_region_locations)

    lemguin_lunge_region_locations = {
        LocationName.lemguin_lunge_flag    : [0x65E, 1],
        LocationName.lemguin_lunge_bonus_1 : [0x65E, 2],
        LocationName.lemguin_lunge_bonus_2 : [0x65E, 3],
        LocationName.lemguin_lunge_dk      : [0x65E, 5],
    }
    if world.options.kongsanity:
        lemguin_lunge_region_locations[LocationName.lemguin_lunge_kong] = []
    lemguin_lunge_region = create_region(world, active_locations, LocationName.lemguin_lunge_region,
                                         lemguin_lunge_region_locations)

    buzzer_barrage_region_locations = {
        LocationName.buzzer_barrage_flag    : [0x676, 1],
        LocationName.buzzer_barrage_bonus_1 : [0x676, 2],
        LocationName.buzzer_barrage_bonus_2 : [0x676, 3],
        LocationName.buzzer_barrage_dk      : [0x676, 5],
    }
    if world.options.kongsanity:
        buzzer_barrage_region_locations[LocationName.buzzer_barrage_kong] = []
    buzzer_barrage_region = create_region(world, active_locations, LocationName.buzzer_barrage_region,
                                          buzzer_barrage_region_locations)

    kong_fused_cliffs_region_locations = {
        LocationName.kong_fused_cliffs_flag    : [0x674, 1],
        LocationName.kong_fused_cliffs_bonus_1 : [0x674, 2],
        LocationName.kong_fused_cliffs_bonus_2 : [0x674, 3],
        LocationName.kong_fused_cliffs_dk      : [0x674, 5],
    }
    if world.options.kongsanity:
        kong_fused_cliffs_region_locations[LocationName.kong_fused_cliffs_kong] = []
    kong_fused_cliffs_region = create_region(world, active_locations, LocationName.kong_fused_cliffs_region,
                                             kong_fused_cliffs_region_locations)

    floodlit_fish_region_locations = {
        LocationName.floodlit_fish_flag    : [0x669, 1],
        LocationName.floodlit_fish_bonus_1 : [0x669, 2],
        LocationName.floodlit_fish_bonus_2 : [0x669, 3],
        LocationName.floodlit_fish_dk      : [0x669, 5],
    }
    if world.options.kongsanity:
        floodlit_fish_region_locations[LocationName.floodlit_fish_kong] = []
    floodlit_fish_region = create_region(world, active_locations, LocationName.floodlit_fish_region,
                                         floodlit_fish_region_locations)

    pothole_panic_region_locations = {
        LocationName.pothole_panic_flag    : [0x677, 1],
        LocationName.pothole_panic_bonus_1 : [0x677, 2],
        LocationName.pothole_panic_bonus_2 : [0x677, 3],
        LocationName.pothole_panic_dk      : [0x677, 5],
    }
    if world.options.kongsanity:
        pothole_panic_region_locations[LocationName.pothole_panic_kong] = []
    pothole_panic_region = create_region(world, active_locations, LocationName.pothole_panic_region,
                                         pothole_panic_region_locations)

    ropey_rumpus_region_locations = {
        LocationName.ropey_rumpus_flag    : [0x675, 1],
        LocationName.ropey_rumpus_bonus_1 : [0x675, 2],
        LocationName.ropey_rumpus_bonus_2 : [0x675, 3],
        LocationName.ropey_rumpus_dk      : [0x675, 5],
    }
    if world.options.kongsanity:
        ropey_rumpus_region_locations[LocationName.ropey_rumpus_kong] = []
    ropey_rumpus_region = create_region(world, active_locations, LocationName.ropey_rumpus_region,
                                        ropey_rumpus_region_locations)

    konveyor_rope_clash_region_locations = {
        LocationName.konveyor_rope_clash_flag     : [0x657, 1],
        LocationName.konveyor_rope_clash_bonus_1  : [0x657, 2],
        LocationName.konveyor_rope_clash_bonus_2  : [0x657, 3],
        LocationName.konveyor_rope_clash_dk       : [0x657, 5],
    }
    if world.options.kongsanity:
        konveyor_rope_clash_region_locations[LocationName.konveyor_rope_clash_kong] = []
    konveyor_rope_clash_region = create_region(world, active_locations, LocationName.konveyor_rope_clash_region,
                                               konveyor_rope_clash_region_locations)

    creepy_caverns_region_locations = {
        LocationName.creepy_caverns_flag    : [0x678, 1],
        LocationName.creepy_caverns_bonus_1 : [0x678, 2],
        LocationName.creepy_caverns_bonus_2 : [0x678, 3],
        LocationName.creepy_caverns_dk      : [0x678, 5],
    }
    if world.options.kongsanity:
        creepy_caverns_region_locations[LocationName.creepy_caverns_kong] = []
    creepy_caverns_region = create_region(world, active_locations, LocationName.creepy_caverns_region,
                                          creepy_caverns_region_locations)

    lightning_lookout_region_locations = {
        LocationName.lightning_lookout_flag     : [0x665, 1],
        LocationName.lightning_lookout_bonus_1  : [0x665, 2],
        LocationName.lightning_lookout_bonus_2  : [0x665, 3],
        LocationName.lightning_lookout_dk       : [0x665, 5],
    }
    if world.options.kongsanity:
        lightning_lookout_region_locations[LocationName.lightning_lookout_kong] = []
    lightning_lookout_region = create_region(world, active_locations, LocationName.lightning_lookout_region,
                                             lightning_lookout_region_locations)

    koindozer_klamber_region_locations = {
        LocationName.koindozer_klamber_flag     : [0x679, 1],
        LocationName.koindozer_klamber_bonus_1  : [0x679, 2],
        LocationName.koindozer_klamber_bonus_2  : [0x679, 3],
        LocationName.koindozer_klamber_dk       : [0x679, 5],
    }
    if world.options.kongsanity:
        koindozer_klamber_region_locations[LocationName.koindozer_klamber_kong] = []
    koindozer_klamber_region = create_region(world, active_locations, LocationName.koindozer_klamber_region,
                                             koindozer_klamber_region_locations)

    poisonous_pipeline_region_locations = {
        LocationName.poisonous_pipeline_flag    : [0x671, 1],
        LocationName.poisonous_pipeline_bonus_1 : [0x671, 2],
        LocationName.poisonous_pipeline_bonus_2 : [0x671, 3],
        LocationName.poisonous_pipeline_dk      : [0x671, 5],
    }
    if world.options.kongsanity:
        poisonous_pipeline_region_locations[LocationName.poisonous_pipeline_kong] = []
    poisonous_pipeline_region = create_region(world, active_locations, LocationName.poisonous_pipeline_region,
                                              poisonous_pipeline_region_locations)

    stampede_sprint_region_locations = {
        LocationName.stampede_sprint_flag     : [0x67B, 1],
        LocationName.stampede_sprint_bonus_1  : [0x67B, 2],
        LocationName.stampede_sprint_bonus_2  : [0x67B, 3],
        LocationName.stampede_sprint_bonus_3  : [0x67B, 4],
        LocationName.stampede_sprint_dk       : [0x67B, 5],
    }
    if world.options.kongsanity:
        stampede_sprint_region_locations[LocationName.stampede_sprint_kong] = []
    stampede_sprint_region = create_region(world, active_locations, LocationName.stampede_sprint_region,
                                           stampede_sprint_region_locations)

    criss_cross_cliffs_region_locations = {
        LocationName.criss_cross_cliffs_flag    : [0x67C, 1],
        LocationName.criss_cross_cliffs_bonus_1 : [0x67C, 2],
        LocationName.criss_cross_cliffs_bonus_2 : [0x67C, 3],
        LocationName.criss_cross_cliffs_dk      : [0x67C, 5],
    }
    if world.options.kongsanity:
        criss_cross_cliffs_region_locations[LocationName.criss_cross_cliffs_kong] = []
    criss_cross_cliffs_region = create_region(world, active_locations, LocationName.criss_cross_cliffs_region,
                                              criss_cross_cliffs_region_locations)

    tyrant_twin_tussle_region_locations = {
        LocationName.tyrant_twin_tussle_flag    : [0x67D, 1],
        LocationName.tyrant_twin_tussle_bonus_1 : [0x67D, 2],
        LocationName.tyrant_twin_tussle_bonus_2 : [0x67D, 3],
        LocationName.tyrant_twin_tussle_bonus_3 : [0x67D, 4],
        LocationName.tyrant_twin_tussle_dk      : [0x67D, 5],
    }
    if world.options.kongsanity:
        tyrant_twin_tussle_region_locations[LocationName.tyrant_twin_tussle_kong] = []
    tyrant_twin_tussle_region = create_region(world, active_locations, LocationName.tyrant_twin_tussle_region,
                                              tyrant_twin_tussle_region_locations)

    swoopy_salvo_region_locations = {
        LocationName.swoopy_salvo_flag    : [0x663, 1],
        LocationName.swoopy_salvo_bonus_1 : [0x663, 2],
        LocationName.swoopy_salvo_bonus_2 : [0x663, 3],
        LocationName.swoopy_salvo_bonus_3 : [0x663, 4],
        LocationName.swoopy_salvo_dk      : [0x663, 5],
    }
    if world.options.kongsanity:
        swoopy_salvo_region_locations[LocationName.swoopy_salvo_kong] = []
    swoopy_salvo_region = create_region(world, active_locations, LocationName.swoopy_salvo_region,
                                        swoopy_salvo_region_locations)

    rocket_rush_region_locations = {
        LocationName.rocket_rush_flag : [0x67E, 1],
        LocationName.rocket_rush_dk   : [0x67E, 5],
    }
    rocket_rush_region = create_region(world, active_locations, LocationName.rocket_rush_region,
                                       rocket_rush_region_locations)

    belchas_barn_region_locations = {
        LocationName.belchas_barn: [0x64F, 1],
    }
    belchas_barn_region = create_region(world, active_locations, LocationName.belchas_barn_region,
                                        belchas_barn_region_locations)

    arichs_ambush_region_locations = {
        LocationName.arichs_ambush: [0x650, 1],
    }
    arichs_ambush_region = create_region(world, active_locations, LocationName.arichs_ambush_region,
                                         arichs_ambush_region_locations)

    squirts_showdown_region_locations = {
        LocationName.squirts_showdown: [0x651, 1],
    }
    squirts_showdown_region = create_region(world, active_locations, LocationName.squirts_showdown_region,
                                            squirts_showdown_region_locations)

    kaos_karnage_region_locations = {
        LocationName.kaos_karnage: [0x652, 1],
    }
    kaos_karnage_region = create_region(world, active_locations, LocationName.kaos_karnage_region,
                                        kaos_karnage_region_locations)

    bleaks_house_region_locations = {
        LocationName.bleaks_house: [0x653, 1],
    }
    bleaks_house_region = create_region(world, active_locations, LocationName.bleaks_house_region,
                                        bleaks_house_region_locations)

    barboss_barrier_region_locations = {
        LocationName.barboss_barrier: [0x654, 1],
    }
    barboss_barrier_region = create_region(world, active_locations, LocationName.barboss_barrier_region,
                                           barboss_barrier_region_locations)

    kastle_kaos_region_locations = {
        LocationName.kastle_kaos: [0x655, 1],
    }
    kastle_kaos_region = create_region(world, active_locations, LocationName.kastle_kaos_region,
                                       kastle_kaos_region_locations)

    knautilus_region_locations = {
        LocationName.knautilus: [0x656, 1],
    }
    knautilus_region = create_region(world, active_locations, LocationName.knautilus_region,
                                     knautilus_region_locations)

    belchas_burrow_region_locations = {
        LocationName.belchas_burrow: [0x647, 1],
    }
    belchas_burrow_region = create_region(world, active_locations, LocationName.belchas_burrow_region,
                                          belchas_burrow_region_locations)

    kong_cave_region_locations = {
        LocationName.kong_cave: [0x645, 1],
    }
    kong_cave_region = create_region(world, active_locations, LocationName.kong_cave_region,
                                     kong_cave_region_locations)

    undercover_cove_region_locations = {
        LocationName.undercover_cove: [0x644, 1],
    }
    undercover_cove_region = create_region(world, active_locations, LocationName.undercover_cove_region,
                                           undercover_cove_region_locations)

    ks_cache_region_locations = {
        LocationName.ks_cache: [0x642, 1],
    }
    ks_cache_region = create_region(world, active_locations, LocationName.ks_cache_region,
                                    ks_cache_region_locations)

    hill_top_hoard_region_locations = {
        LocationName.hill_top_hoard: [0x643, 1],
    }
    hill_top_hoard_region = create_region(world, active_locations, LocationName.hill_top_hoard_region,
                                          hill_top_hoard_region_locations)

    bounty_beach_region_locations = {
        LocationName.bounty_beach: [0x646, 1],
    }
    bounty_beach_region = create_region(world, active_locations, LocationName.bounty_beach_region,
                                        bounty_beach_region_locations)

    smugglers_cove_region_locations = {
        LocationName.smugglers_cove: [0x648, 1],
    }
    smugglers_cove_region = create_region(world, active_locations, LocationName.smugglers_cove_region,
                                          smugglers_cove_region_locations)

    arichs_hoard_region_locations = {
        LocationName.arichs_hoard: [0x649, 1],
    }
    arichs_hoard_region = create_region(world, active_locations, LocationName.arichs_hoard_region,
                                        arichs_hoard_region_locations)

    bounty_bay_region_locations = {
        LocationName.bounty_bay: [0x64A, 1],
    }
    bounty_bay_region = create_region(world, active_locations, LocationName.bounty_bay_region,
                                      bounty_bay_region_locations)

    sky_high_secret_region_locations = {}
    if False:#world.options.include_trade_sequence:
        sky_high_secret_region_locations[LocationName.sky_high_secret] = [0x64B, 1]
    sky_high_secret_region = create_region(world, active_locations, LocationName.sky_high_secret_region,
                                           sky_high_secret_region_locations)

    glacial_grotto_region_locations = {
        LocationName.glacial_grotto: [0x64C, 1],
    }
    glacial_grotto_region = create_region(world, active_locations, LocationName.glacial_grotto_region,
                                          glacial_grotto_region_locations)

    cifftop_cache_region_locations = {}
    if False:#world.options.include_trade_sequence:
        cifftop_cache_region_locations[LocationName.cifftop_cache] = [0x64D, 1]
    cifftop_cache_region = create_region(world, active_locations, LocationName.cifftop_cache_region,
                                         cifftop_cache_region_locations)

    sewer_stockpile_region_locations = {
        LocationName.sewer_stockpile: [0x64E, 1],
    }
    sewer_stockpile_region = create_region(world, active_locations, LocationName.sewer_stockpile_region,
                                           sewer_stockpile_region_locations)


    # Set up the regions correctly.
    world.multiworld.regions += [
        menu_region,
        overworld_1_region,
        overworld_2_region,
        overworld_3_region,
        overworld_4_region,
        lake_orangatanga_region,
        kremwood_forest_region,
        cotton_top_cove_region,
        mekanos_region,
        k3_region,
        razor_ridge_region,
        kaos_kore_region,
        krematoa_region,
        lakeside_limbo_region,
        doorstop_dash_region,
        tidal_trouble_region,
        skiddas_row_region,
        murky_mill_region,
        barrel_shield_bust_up_region,
        riverside_race_region,
        squeals_on_wheels_region,
        springin_spiders_region,
        bobbing_barrel_brawl_region,
        bazzas_blockade_region,
        rocket_barrel_ride_region,
        kreeping_klasps_region,
        tracker_barrel_trek_region,
        fish_food_frenzy_region,
        fire_ball_frenzy_region,
        demolition_drain_pipe_region,
        ripsaw_rage_region,
        blazing_bazookas_region,
        low_g_labyrinth_region,
        krevice_kreepers_region,
        tearaway_toboggan_region,
        barrel_drop_bounce_region,
        krack_shot_kroc_region,
        lemguin_lunge_region,
        buzzer_barrage_region,
        kong_fused_cliffs_region,
        floodlit_fish_region,
        pothole_panic_region,
        ropey_rumpus_region,
        konveyor_rope_clash_region,
        creepy_caverns_region,
        lightning_lookout_region,
        koindozer_klamber_region,
        poisonous_pipeline_region,
        stampede_sprint_region,
        criss_cross_cliffs_region,
        tyrant_twin_tussle_region,
        swoopy_salvo_region,
        rocket_rush_region,
        belchas_barn_region,
        arichs_ambush_region,
        squirts_showdown_region,
        kaos_karnage_region,
        bleaks_house_region,
        barboss_barrier_region,
        kastle_kaos_region,
        knautilus_region,
        belchas_burrow_region,
        kong_cave_region,
        undercover_cove_region,
        ks_cache_region,
        hill_top_hoard_region,
        bounty_beach_region,
        smugglers_cove_region,
        arichs_hoard_region,
        bounty_bay_region,
        sky_high_secret_region,
        glacial_grotto_region,
        cifftop_cache_region,
        sewer_stockpile_region,
    ]
    
    bazaar_region_locations = {}
    bramble_region_locations = {}
    flower_spot_region_locations = {}
    barter_region_locations = {}
    barnacle_region_locations = {}
    blue_region_locations = {}
    blizzard_region_locations = {}

    if False:#world.options.include_trade_sequence:
        bazaar_region_locations.update({
            LocationName.bazaars_general_store_1: [0x615, 2, True],
            LocationName.bazaars_general_store_2: [0x615, 3, True],
        })

        bramble_region_locations[LocationName.brambles_bungalow] = [0x619, 2]

        #flower_spot_region_locations.update({
        #    LocationName.flower_spot: [0x615, 3, True],
        #})

        barter_region_locations[LocationName.barters_swap_shop] = [0x61B, 3]

        barnacle_region_locations[LocationName.barnacles_island] = [0x61D, 2]

        blue_region_locations[LocationName.blues_beach_hut] = [0x621, 4]

        blizzard_region_locations[LocationName.blizzards_basecamp] = [0x625, 4, True]

    bazaar_region = create_region(world, active_locations, LocationName.bazaar_region, bazaar_region_locations)
    bramble_region = create_region(world, active_locations, LocationName.bramble_region,
                                   bramble_region_locations)
    flower_spot_region = create_region(world, active_locations, LocationName.flower_spot_region,
                                       flower_spot_region_locations)
    barter_region = create_region(world, active_locations, LocationName.barter_region, barter_region_locations)
    barnacle_region = create_region(world, active_locations, LocationName.barnacle_region,
                                    barnacle_region_locations)
    blue_region = create_region(world, active_locations, LocationName.blue_region, blue_region_locations)
    blizzard_region = create_region(world, active_locations, LocationName.blizzard_region,
                                    blizzard_region_locations)

    world.multiworld.regions += [
        bazaar_region,
        bramble_region,
        flower_spot_region,
        barter_region,
        barnacle_region,
        blue_region,
        blizzard_region,
    ]


def connect_regions(world: World, level_list):
    names: typing.Dict[str, int] = {}

    # Overworld
    connect(world, world.player, names, 'Menu', LocationName.overworld_1_region)
    connect(world, world.player, names, LocationName.overworld_1_region, LocationName.overworld_2_region,
            lambda state: (state.has(ItemName.progressive_boat, world.player, 1)))
    connect(world, world.player, names, LocationName.overworld_2_region, LocationName.overworld_3_region,
            lambda state: (state.has(ItemName.progressive_boat, world.player, 3)))
    connect(world, world.player, names, LocationName.overworld_1_region, LocationName.overworld_4_region,
            lambda state: (state.has(ItemName.dk_coin, world.player, world.options.dk_coins_for_gyrocopter.value) and
                           state.has(ItemName.progressive_boat, world.player, 3)))

    # World Connections
    connect(world, world.player, names, LocationName.overworld_1_region, LocationName.lake_orangatanga_region)
    connect(world, world.player, names, LocationName.overworld_1_region, LocationName.kremwood_forest_region)
    connect(world, world.player, names, LocationName.overworld_1_region, LocationName.bounty_beach_region)
    connect(world, world.player, names, LocationName.overworld_1_region, LocationName.bazaar_region)

    connect(world, world.player, names, LocationName.overworld_2_region, LocationName.cotton_top_cove_region)
    connect(world, world.player, names, LocationName.overworld_2_region, LocationName.mekanos_region)
    connect(world, world.player, names, LocationName.overworld_2_region, LocationName.kong_cave_region)
    connect(world, world.player, names, LocationName.overworld_2_region, LocationName.bramble_region)

    connect(world, world.player, names, LocationName.overworld_3_region, LocationName.k3_region)
    connect(world, world.player, names, LocationName.overworld_3_region, LocationName.razor_ridge_region)
    connect(world, world.player, names, LocationName.overworld_3_region, LocationName.kaos_kore_region)
    connect(world, world.player, names, LocationName.overworld_3_region, LocationName.krematoa_region)
    connect(world, world.player, names, LocationName.overworld_3_region, LocationName.undercover_cove_region)
    connect(world, world.player, names, LocationName.overworld_3_region, LocationName.flower_spot_region)
    connect(world, world.player, names, LocationName.overworld_3_region, LocationName.barter_region)

    connect(world, world.player, names, LocationName.overworld_4_region, LocationName.belchas_burrow_region)
    connect(world, world.player, names, LocationName.overworld_4_region, LocationName.ks_cache_region)
    connect(world, world.player, names, LocationName.overworld_4_region, LocationName.hill_top_hoard_region)


    # Lake Orangatanga Connections
    lake_orangatanga_levels = [
        level_list[0],
        level_list[1],
        level_list[2],
        level_list[3],
        level_list[4],
        LocationName.belchas_barn_region,
        LocationName.barnacle_region,
        LocationName.smugglers_cove_region,
    ]

    for i in range(0, len(lake_orangatanga_levels)):
        connect(world, world.player, names, LocationName.lake_orangatanga_region, lake_orangatanga_levels[i])

    # Kremwood Forest Connections
    kremwood_forest_levels = [
        level_list[5],
        level_list[6],
        level_list[7],
        level_list[8],
        level_list[9],
        LocationName.arichs_ambush_region,
        LocationName.arichs_hoard_region,
    ]

    for i in range(0, len(kremwood_forest_levels) - 1):
        connect(world, world.player, names, LocationName.kremwood_forest_region, kremwood_forest_levels[i])

    connection = connect(world, world.player, names, LocationName.kremwood_forest_region, kremwood_forest_levels[-1],
                         lambda state: (state.can_reach(LocationName.riverside_race_flag, "Location", world.player)))
    world.multiworld.register_indirect_condition(world.get_location(LocationName.riverside_race_flag).parent_region,
                                                 connection)

    # Cotton-Top Cove Connections
    cotton_top_cove_levels = [
        LocationName.blue_region,
        level_list[10],
        level_list[11],
        level_list[12],
        level_list[13],
        level_list[14],
        LocationName.squirts_showdown_region,
        LocationName.bounty_bay_region,
    ]

    for i in range(0, len(cotton_top_cove_levels)):
        connect(world, world.player, names, LocationName.cotton_top_cove_region, cotton_top_cove_levels[i])

    # Mekanos Connections
    mekanos_levels = [
        level_list[15],
        level_list[16],
        level_list[17],
        level_list[18],
        level_list[19],
        LocationName.kaos_karnage_region,
    ]

    for i in range(0, len(mekanos_levels)):
        connect(world, world.player, names, LocationName.mekanos_region, mekanos_levels[i])
        
    if False:#world.options.include_trade_sequence:
        connect(world, world.player, names, LocationName.mekanos_region, LocationName.sky_high_secret_region,
                lambda state: (state.has(ItemName.bowling_ball, world.player, 1)))
    else:
        connection = connect(world, world.player, names, LocationName.mekanos_region,
                             LocationName.sky_high_secret_region,
                             lambda state: (state.can_reach(LocationName.bleaks_house, "Location", world.player)))
        world.multiworld.register_indirect_condition(world.get_location(LocationName.bleaks_house).parent_region,
                                                     connection)

    # K3 Connections
    k3_levels = [
        level_list[20],
        level_list[21],
        level_list[22],
        level_list[23],
        level_list[24],
        LocationName.bleaks_house_region,
        LocationName.blizzard_region,
        LocationName.glacial_grotto_region,
    ]

    for i in range(0, len(k3_levels)):
        connect(world, world.player, names, LocationName.k3_region, k3_levels[i])

    # Razor Ridge Connections
    razor_ridge_levels = [
        level_list[25],
        level_list[26],
        level_list[27],
        level_list[28],
        level_list[29],
        LocationName.barboss_barrier_region,
    ]

    for i in range(0, len(razor_ridge_levels)):
        connect(world, world.player, names, LocationName.razor_ridge_region, razor_ridge_levels[i])
        
    if False:#world.options.include_trade_sequence:
        connect(world, world.player, names, LocationName.razor_ridge_region, LocationName.cifftop_cache_region,
                lambda state: (state.has(ItemName.wrench, world.player, 1)))
    else:
        connect(world, world.player, names, LocationName.razor_ridge_region, LocationName.cifftop_cache_region)

    # KAOS Kore Connections
    kaos_kore_levels = [
        level_list[30],
        level_list[31],
        level_list[32],
        level_list[33],
        level_list[34],
        LocationName.sewer_stockpile_region,
    ]

    for i in range(0, len(kaos_kore_levels)):
        connect(world, world.player, names, LocationName.kaos_kore_region, kaos_kore_levels[i])

    # Krematoa Connections
    krematoa_levels = [
        level_list[35],
        level_list[36],
        level_list[37],
        level_list[38],
        LocationName.rocket_rush_region,
    ]

    for i in range(0, len(krematoa_levels)):
        connect(world, world.player, names, LocationName.krematoa_region, krematoa_levels[i],
                lambda state, i=i: (state.has(ItemName.bonus_coin, world.player, world.options.krematoa_bonus_coin_cost.value * (i+1))))

    if world.options.goal == "knautilus":
        connect(world, world.player, names, LocationName.kaos_kore_region, LocationName.knautilus_region)
        connect(world, world.player, names, LocationName.krematoa_region, LocationName.kastle_kaos_region,
                lambda state: (state.has(ItemName.krematoa_cog, world.player, 5)))
    else:
        connect(world, world.player, names, LocationName.kaos_kore_region, LocationName.kastle_kaos_region)
        connect(world, world.player, names, LocationName.krematoa_region, LocationName.knautilus_region,
                lambda state: (state.has(ItemName.krematoa_cog, world.player, 5)))


def create_region(world: World, active_locations, name: str, locations=None):
    # Shamelessly stolen from the ROR2 definition
    ret = Region(name, world.player, world.multiworld)
    if locations:
        for locationName, locationData in locations.items():
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                loc_byte   = locationData[0] if (len(locationData) > 0) else 0
                loc_bit    = locationData[1] if (len(locationData) > 1) else 0
                loc_invert = locationData[2] if (len(locationData) > 2) else False

                location = DKC3Location(world.player, locationName, loc_id, ret, loc_byte, loc_bit, loc_invert)
                ret.locations.append(location)

    return ret


def connect(world: World, player: int, used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = world.multiworld.get_region(source, player)
    target_region = world.multiworld.get_region(target, player)

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
    return connection
