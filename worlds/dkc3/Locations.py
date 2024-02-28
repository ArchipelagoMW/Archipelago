import typing

from BaseClasses import Location
from .Names import LocationName
from worlds.AutoWorld import World


class DKC3Location(Location):
    game: str = "Donkey Kong Country 3"

    progress_byte: int = 0x000000
    progress_bit:  int = 0
    inverted_bit: bool = False

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, prog_byte: int = None, prog_bit: int = None, invert: bool = False):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit  = prog_bit
        self.inverted_bit  = invert


level_location_table = {
    LocationName.lakeside_limbo_flag:    0xDC3000,
    LocationName.lakeside_limbo_bonus_1: 0xDC3001,
    LocationName.lakeside_limbo_bonus_2: 0xDC3002,
    LocationName.lakeside_limbo_dk:      0xDC3003,

    LocationName.doorstop_dash_flag:    0xDC3004,
    LocationName.doorstop_dash_bonus_1: 0xDC3005,
    LocationName.doorstop_dash_bonus_2: 0xDC3006,
    LocationName.doorstop_dash_dk:      0xDC3007,
    
    LocationName.tidal_trouble_flag:    0xDC3008,
    LocationName.tidal_trouble_bonus_1: 0xDC3009,
    LocationName.tidal_trouble_bonus_2: 0xDC300A,
    LocationName.tidal_trouble_dk:      0xDC300B,

    LocationName.skiddas_row_flag:    0xDC300C,
    LocationName.skiddas_row_bonus_1: 0xDC300D,
    LocationName.skiddas_row_bonus_2: 0xDC300E,
    LocationName.skiddas_row_dk:      0xDC300F,
    
    LocationName.murky_mill_flag:    0xDC3010,
    LocationName.murky_mill_bonus_1: 0xDC3011,
    LocationName.murky_mill_bonus_2: 0xDC3012,
    LocationName.murky_mill_dk:      0xDC3013,

    LocationName.barrel_shield_bust_up_flag:    0xDC3014,
    LocationName.barrel_shield_bust_up_bonus_1: 0xDC3015,
    LocationName.barrel_shield_bust_up_bonus_2: 0xDC3016,
    LocationName.barrel_shield_bust_up_dk:      0xDC3017,
    
    LocationName.riverside_race_flag:    0xDC3018,
    LocationName.riverside_race_bonus_1: 0xDC3019,
    LocationName.riverside_race_bonus_2: 0xDC301A,
    LocationName.riverside_race_dk:      0xDC301B,

    LocationName.squeals_on_wheels_flag:    0xDC301C,
    LocationName.squeals_on_wheels_bonus_1: 0xDC301D,
    LocationName.squeals_on_wheels_bonus_2: 0xDC301E,
    LocationName.squeals_on_wheels_dk:      0xDC301F,
    
    LocationName.springin_spiders_flag:    0xDC3020,
    LocationName.springin_spiders_bonus_1: 0xDC3021,
    LocationName.springin_spiders_bonus_2: 0xDC3022,
    LocationName.springin_spiders_dk:      0xDC3023,

    LocationName.bobbing_barrel_brawl_flag:    0xDC3024,
    LocationName.bobbing_barrel_brawl_bonus_1: 0xDC3025,
    LocationName.bobbing_barrel_brawl_bonus_2: 0xDC3026,
    LocationName.bobbing_barrel_brawl_dk:      0xDC3027,
    
    LocationName.bazzas_blockade_flag:    0xDC3028,
    LocationName.bazzas_blockade_bonus_1: 0xDC3029,
    LocationName.bazzas_blockade_bonus_2: 0xDC302A,
    LocationName.bazzas_blockade_dk:      0xDC302B,

    LocationName.rocket_barrel_ride_flag:    0xDC302C,
    LocationName.rocket_barrel_ride_bonus_1: 0xDC302D,
    LocationName.rocket_barrel_ride_bonus_2: 0xDC302E,
    LocationName.rocket_barrel_ride_dk:      0xDC302F,
    
    LocationName.kreeping_klasps_flag:    0xDC3030,
    LocationName.kreeping_klasps_bonus_1: 0xDC3031,
    LocationName.kreeping_klasps_bonus_2: 0xDC3032,
    LocationName.kreeping_klasps_dk:      0xDC3033,

    LocationName.tracker_barrel_trek_flag:    0xDC3034,
    LocationName.tracker_barrel_trek_bonus_1: 0xDC3035,
    LocationName.tracker_barrel_trek_bonus_2: 0xDC3036,
    LocationName.tracker_barrel_trek_dk:      0xDC3037,
    
    LocationName.fish_food_frenzy_flag:    0xDC3038,
    LocationName.fish_food_frenzy_bonus_1: 0xDC3039,
    LocationName.fish_food_frenzy_bonus_2: 0xDC303A,
    LocationName.fish_food_frenzy_dk:      0xDC303B,

    LocationName.fire_ball_frenzy_flag:    0xDC303C,
    LocationName.fire_ball_frenzy_bonus_1: 0xDC303D,
    LocationName.fire_ball_frenzy_bonus_2: 0xDC303E,
    LocationName.fire_ball_frenzy_dk:      0xDC303F,
    
    LocationName.demolition_drain_pipe_flag:    0xDC3040,
    LocationName.demolition_drain_pipe_bonus_1: 0xDC3041,
    LocationName.demolition_drain_pipe_bonus_2: 0xDC3042,
    LocationName.demolition_drain_pipe_dk:      0xDC3043,

    LocationName.ripsaw_rage_flag:    0xDC3044,
    LocationName.ripsaw_rage_bonus_1: 0xDC3045,
    LocationName.ripsaw_rage_bonus_2: 0xDC3046,
    LocationName.ripsaw_rage_dk:      0xDC3047,
    
    LocationName.blazing_bazookas_flag:    0xDC3048,
    LocationName.blazing_bazookas_bonus_1: 0xDC3049,
    LocationName.blazing_bazookas_bonus_2: 0xDC304A,
    LocationName.blazing_bazookas_dk:      0xDC304B,

    LocationName.low_g_labyrinth_flag:    0xDC304C,
    LocationName.low_g_labyrinth_bonus_1: 0xDC304D,
    LocationName.low_g_labyrinth_bonus_2: 0xDC304E,
    LocationName.low_g_labyrinth_dk:      0xDC304F,
    
    LocationName.krevice_kreepers_flag:    0xDC3050,
    LocationName.krevice_kreepers_bonus_1: 0xDC3051,
    LocationName.krevice_kreepers_bonus_2: 0xDC3052,
    LocationName.krevice_kreepers_dk:      0xDC3053,

    LocationName.tearaway_toboggan_flag:    0xDC3054,
    LocationName.tearaway_toboggan_bonus_1: 0xDC3055,
    LocationName.tearaway_toboggan_bonus_2: 0xDC3056,
    LocationName.tearaway_toboggan_dk:      0xDC3057,
    
    LocationName.barrel_drop_bounce_flag:    0xDC3058,
    LocationName.barrel_drop_bounce_bonus_1: 0xDC3059,
    LocationName.barrel_drop_bounce_bonus_2: 0xDC305A,
    LocationName.barrel_drop_bounce_dk:      0xDC305B,

    LocationName.krack_shot_kroc_flag:    0xDC305C,
    LocationName.krack_shot_kroc_bonus_1: 0xDC305D,
    LocationName.krack_shot_kroc_bonus_2: 0xDC305E,
    LocationName.krack_shot_kroc_dk:      0xDC305F,
    
    LocationName.lemguin_lunge_flag:    0xDC3060,
    LocationName.lemguin_lunge_bonus_1: 0xDC3061,
    LocationName.lemguin_lunge_bonus_2: 0xDC3062,
    LocationName.lemguin_lunge_dk:      0xDC3063,

    LocationName.buzzer_barrage_flag:    0xDC3064,
    LocationName.buzzer_barrage_bonus_1: 0xDC3065,
    LocationName.buzzer_barrage_bonus_2: 0xDC3066,
    LocationName.buzzer_barrage_dk:      0xDC3067,
    
    LocationName.kong_fused_cliffs_flag:    0xDC3068,
    LocationName.kong_fused_cliffs_bonus_1: 0xDC3069,
    LocationName.kong_fused_cliffs_bonus_2: 0xDC306A,
    LocationName.kong_fused_cliffs_dk:      0xDC306B,

    LocationName.floodlit_fish_flag:    0xDC306C,
    LocationName.floodlit_fish_bonus_1: 0xDC306D,
    LocationName.floodlit_fish_bonus_2: 0xDC306E,
    LocationName.floodlit_fish_dk:      0xDC306F,
    
    LocationName.pothole_panic_flag:    0xDC3070,
    LocationName.pothole_panic_bonus_1: 0xDC3071,
    LocationName.pothole_panic_bonus_2: 0xDC3072,
    LocationName.pothole_panic_dk:      0xDC3073,

    LocationName.ropey_rumpus_flag:    0xDC3074,
    LocationName.ropey_rumpus_bonus_1: 0xDC3075,
    LocationName.ropey_rumpus_bonus_2: 0xDC3076,
    LocationName.ropey_rumpus_dk:      0xDC3077,
    
    LocationName.konveyor_rope_clash_flag:    0xDC3078,
    LocationName.konveyor_rope_clash_bonus_1: 0xDC3079,
    LocationName.konveyor_rope_clash_bonus_2: 0xDC307A,
    LocationName.konveyor_rope_clash_dk:      0xDC307B,

    LocationName.creepy_caverns_flag:    0xDC307C,
    LocationName.creepy_caverns_bonus_1: 0xDC307D,
    LocationName.creepy_caverns_bonus_2: 0xDC307E,
    LocationName.creepy_caverns_dk:      0xDC307F,
    
    LocationName.lightning_lookout_flag:    0xDC3080,
    LocationName.lightning_lookout_bonus_1: 0xDC3081,
    LocationName.lightning_lookout_bonus_2: 0xDC3082,
    LocationName.lightning_lookout_dk:      0xDC3083,

    LocationName.koindozer_klamber_flag:    0xDC3084,
    LocationName.koindozer_klamber_bonus_1: 0xDC3085,
    LocationName.koindozer_klamber_bonus_2: 0xDC3086,
    LocationName.koindozer_klamber_dk:      0xDC3087,
    
    LocationName.poisonous_pipeline_flag:    0xDC3088,
    LocationName.poisonous_pipeline_bonus_1: 0xDC3089,
    LocationName.poisonous_pipeline_bonus_2: 0xDC308A,
    LocationName.poisonous_pipeline_dk:      0xDC308B,

    LocationName.stampede_sprint_flag:    0xDC308C,
    LocationName.stampede_sprint_bonus_1: 0xDC308D,
    LocationName.stampede_sprint_bonus_2: 0xDC308E,
    LocationName.stampede_sprint_bonus_3: 0xDC308F,
    LocationName.stampede_sprint_dk:      0xDC3090,
    
    LocationName.criss_cross_cliffs_flag:    0xDC3091,
    LocationName.criss_cross_cliffs_bonus_1: 0xDC3092,
    LocationName.criss_cross_cliffs_bonus_2: 0xDC3093,
    LocationName.criss_cross_cliffs_dk:      0xDC3094,

    LocationName.tyrant_twin_tussle_flag:    0xDC3095,
    LocationName.tyrant_twin_tussle_bonus_1: 0xDC3096,
    LocationName.tyrant_twin_tussle_bonus_2: 0xDC3097,
    LocationName.tyrant_twin_tussle_bonus_3: 0xDC3098,
    LocationName.tyrant_twin_tussle_dk:      0xDC3099,
    
    LocationName.swoopy_salvo_flag:    0xDC309A,
    LocationName.swoopy_salvo_bonus_1: 0xDC309B,
    LocationName.swoopy_salvo_bonus_2: 0xDC309C,
    LocationName.swoopy_salvo_bonus_3: 0xDC309D,
    LocationName.swoopy_salvo_dk:      0xDC309E,

    LocationName.rocket_rush_flag:    0xDC309F,
    LocationName.rocket_rush_dk:      0xDC30A0,
}

kong_location_table = {
    LocationName.lakeside_limbo_kong: 0xDC3100,
    LocationName.doorstop_dash_kong:  0xDC3104,
    LocationName.tidal_trouble_kong:  0xDC3108,
    LocationName.skiddas_row_kong:    0xDC310C,
    LocationName.murky_mill_kong:     0xDC3110,

    LocationName.barrel_shield_bust_up_kong: 0xDC3114,
    LocationName.riverside_race_kong:        0xDC3118,
    LocationName.squeals_on_wheels_kong:     0xDC311C,
    LocationName.springin_spiders_kong:      0xDC3120,
    LocationName.bobbing_barrel_brawl_kong:  0xDC3124,

    LocationName.bazzas_blockade_kong:     0xDC3128,
    LocationName.rocket_barrel_ride_kong:  0xDC312C,
    LocationName.kreeping_klasps_kong:     0xDC3130,
    LocationName.tracker_barrel_trek_kong: 0xDC3134,
    LocationName.fish_food_frenzy_kong:    0xDC3138,

    LocationName.fire_ball_frenzy_kong:      0xDC313C,
    LocationName.demolition_drain_pipe_kong: 0xDC3140,
    LocationName.ripsaw_rage_kong:           0xDC3144,
    LocationName.blazing_bazookas_kong:      0xDC3148,
    LocationName.low_g_labyrinth_kong:       0xDC314C,

    LocationName.krevice_kreepers_kong:   0xDC3150,
    LocationName.tearaway_toboggan_kong:  0xDC3154,
    LocationName.barrel_drop_bounce_kong: 0xDC3158,
    LocationName.krack_shot_kroc_kong:    0xDC315C,
    LocationName.lemguin_lunge_kong:      0xDC3160,

    LocationName.buzzer_barrage_kong:    0xDC3164,
    LocationName.kong_fused_cliffs_kong: 0xDC3168,
    LocationName.floodlit_fish_kong:     0xDC316C,
    LocationName.pothole_panic_kong:     0xDC3170,
    LocationName.ropey_rumpus_kong:      0xDC3174,

    LocationName.konveyor_rope_clash_kong: 0xDC3178,
    LocationName.creepy_caverns_kong:      0xDC317C,
    LocationName.lightning_lookout_kong:   0xDC3180,
    LocationName.koindozer_klamber_kong:   0xDC3184,
    LocationName.poisonous_pipeline_kong:  0xDC3188,

    LocationName.stampede_sprint_kong:    0xDC318C,
    LocationName.criss_cross_cliffs_kong: 0xDC3191,
    LocationName.tyrant_twin_tussle_kong: 0xDC3195,
    LocationName.swoopy_salvo_kong:       0xDC319A,
}


boss_location_table = {
    LocationName.belchas_barn:     0xDC30A1,
    LocationName.arichs_ambush:    0xDC30A2,
    LocationName.squirts_showdown: 0xDC30A3,
    LocationName.kaos_karnage:     0xDC30A4,
    LocationName.bleaks_house:     0xDC30A5,
    LocationName.barboss_barrier:  0xDC30A6,
    LocationName.kastle_kaos:      0xDC30A7,
    LocationName.knautilus:        0xDC30A8,
}

secret_cave_location_table = {
    LocationName.belchas_burrow:  0xDC30A9,
    LocationName.kong_cave:       0xDC30AA,
    LocationName.undercover_cove: 0xDC30AB,
    LocationName.ks_cache:        0xDC30AC,
    LocationName.hill_top_hoard:  0xDC30AD,
    LocationName.bounty_beach:    0xDC30AE,
    LocationName.smugglers_cove:  0xDC30AF,
    LocationName.arichs_hoard:    0xDC30B0,
    LocationName.bounty_bay:      0xDC30B1,
    LocationName.sky_high_secret: 0xDC30B2,
    LocationName.glacial_grotto:  0xDC30B3,
    LocationName.cifftop_cache:   0xDC30B4,
    LocationName.sewer_stockpile: 0xDC30B5,
    LocationName.banana_bird_mother: 0xDC30B6,
}

brothers_bear_location_table = {
    LocationName.bazaars_general_store_1: 0xDC30B7,
    LocationName.bazaars_general_store_2: 0xDC30B8,
    LocationName.brambles_bungalow:       0xDC30B9,
    LocationName.flower_spot:             0xDC30BA,
    LocationName.barters_swap_shop:       0xDC30BB,
    LocationName.barnacles_island:        0xDC30BC,
    LocationName.blues_beach_hut:         0xDC30BD,
    LocationName.blizzards_basecamp:      0xDC30BE,
}

all_locations = {
    **level_location_table,
    **boss_location_table,
    **secret_cave_location_table,
    **brothers_bear_location_table,
    **kong_location_table,
}

location_table = {}


def setup_locations(world: World):
    location_table = {**level_location_table, **boss_location_table, **secret_cave_location_table}

    if False:#world.options.include_trade_sequence:
        location_table.update({**brothers_bear_location_table})

    if world.options.kongsanity:
        location_table.update({**kong_location_table})

    return location_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
