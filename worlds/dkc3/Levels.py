
from .Names import LocationName

class DKC3Level():
    nameIDAddress: int
    levelIDAddress: int
    nameID: int
    levelID: int
    
    def __init__(self, nameIDAddress: int, levelIDAddress: int, nameID: int, levelID: int):
        self.nameIDAddress = nameIDAddress
        self.levelIDAddress  = levelIDAddress
        self.nameID  = nameID
        self.levelID  = levelID


level_dict = {
    LocationName.lakeside_limbo_region: DKC3Level(0x34D19C, 0x34D19D, 0x01, 0x25),
    LocationName.doorstop_dash_region:  DKC3Level(0x34D1A7, 0x34D1A8, 0x02, 0x28),
    LocationName.tidal_trouble_region:  DKC3Level(0x34D1BD, 0x34D1BE, 0x04, 0x27),
    LocationName.skiddas_row_region:    DKC3Level(0x34D1C8, 0x34D1C9, 0x05, 0x2B),
    LocationName.murky_mill_region:     DKC3Level(0x34D1D3, 0x34D1D4, 0x0D, 0x2A),

    LocationName.barrel_shield_bust_up_region: DKC3Level(0x34D217, 0x34D218, 0x0B, 0x30),
    LocationName.riverside_race_region:        DKC3Level(0x34D22D, 0x34D22E, 0x0C, 0x32),
    LocationName.squeals_on_wheels_region:     DKC3Level(0x34D238, 0x34D239, 0x06, 0x29),
    LocationName.springin_spiders_region:      DKC3Level(0x34D24E, 0x34D24F, 0x0E, 0x2F),
    LocationName.bobbing_barrel_brawl_region:  DKC3Level(0x34D264, 0x34D265, 0x37, 0x34),

    LocationName.bazzas_blockade_region:     DKC3Level(0x34D29D, 0x34D29E, 0x14, 0x35),
    LocationName.rocket_barrel_ride_region:  DKC3Level(0x34D2A8, 0x34D2A9, 0x15, 0x38),
    LocationName.kreeping_klasps_region:     DKC3Level(0x34D2BE, 0x34D2BF, 0x16, 0x26),
    LocationName.tracker_barrel_trek_region: DKC3Level(0x34D2D4, 0x34D2D5, 0x17, 0x39),
    LocationName.fish_food_frenzy_region:    DKC3Level(0x34D2DF, 0x34D2E0, 0x18, 0x36),

    LocationName.fire_ball_frenzy_region:      DKC3Level(0x34D30D, 0x34D30E, 0x1B, 0x3B),
    LocationName.demolition_drain_pipe_region: DKC3Level(0x34D323, 0x34D324, 0x1D, 0x40),
    LocationName.ripsaw_rage_region:           DKC3Level(0x34D339, 0x34D33A, 0x1E, 0x2E),
    LocationName.blazing_bazookas_region:      DKC3Level(0x34D34F, 0x34D350, 0x1F, 0x3C),
    LocationName.low_g_labyrinth_region:       DKC3Level(0x34D35A, 0x34D35B, 0x20, 0x3E),

    LocationName.krevice_kreepers_region:   DKC3Level(0x34D388, 0x34D389, 0x23, 0x41),
    LocationName.tearaway_toboggan_region:  DKC3Level(0x34D393, 0x34D394, 0x24, 0x2D),
    LocationName.barrel_drop_bounce_region: DKC3Level(0x34D39E, 0x34D39F, 0x25, 0x3A),
    LocationName.krack_shot_kroc_region:    DKC3Level(0x34D3A9, 0x34D3AA, 0x26, 0x3D),
    LocationName.lemguin_lunge_region:      DKC3Level(0x34D3B4, 0x34D3B5, 0x27, 0x2C),

    LocationName.buzzer_barrage_region:    DKC3Level(0x34D40E, 0x34D40F, 0x2B, 0x44),
    LocationName.kong_fused_cliffs_region: DKC3Level(0x34D424, 0x34D425, 0x2D, 0x42),
    LocationName.floodlit_fish_region:     DKC3Level(0x34D42F, 0x34D430, 0x2E, 0x37),
    LocationName.pothole_panic_region:     DKC3Level(0x34D43A, 0x34D43B, 0x2F, 0x45),
    LocationName.ropey_rumpus_region:      DKC3Level(0x34D450, 0x34D451, 0x30, 0x43),

    LocationName.konveyor_rope_clash_region: DKC3Level(0x34D489, 0x34D48A, 0x38, 0x48),
    LocationName.creepy_caverns_region:      DKC3Level(0x34D49F, 0x34D4A0, 0x36, 0x46),
    LocationName.lightning_lookout_region:   DKC3Level(0x34D4AA, 0x34D4AB, 0x10, 0x33),
    LocationName.koindozer_klamber_region:   DKC3Level(0x34D4C0, 0x34D4C1, 0x34, 0x47),
    LocationName.poisonous_pipeline_region:  DKC3Level(0x34D4D6, 0x34D4D7, 0x39, 0x3F),

    LocationName.stampede_sprint_region:    DKC3Level(0x34D51A, 0x34D51B, 0x3D, 0x49),
    LocationName.criss_cross_cliffs_region: DKC3Level(0x34D525, 0x34D526, 0x3E, 0x4A),
    LocationName.tyrant_twin_tussle_region: DKC3Level(0x34D530, 0x34D531, 0x3F, 0x4B),
    LocationName.swoopy_salvo_region:       DKC3Level(0x34D53B, 0x34D53C, 0x40, 0x31),
    #LocationName.rocket_rush_region:        DKC3Level(0x34D546, 0x34D547, 0x05, 0x4C), # Rocket Rush is not getting shuffled
}

level_list = [
    LocationName.lakeside_limbo_region,
    LocationName.doorstop_dash_region,
    LocationName.tidal_trouble_region,
    LocationName.skiddas_row_region,
    LocationName.murky_mill_region,

    LocationName.barrel_shield_bust_up_region,
    LocationName.riverside_race_region,
    LocationName.squeals_on_wheels_region,
    LocationName.springin_spiders_region,
    LocationName.bobbing_barrel_brawl_region,

    LocationName.bazzas_blockade_region,
    LocationName.rocket_barrel_ride_region,
    LocationName.kreeping_klasps_region,
    LocationName.tracker_barrel_trek_region,
    LocationName.fish_food_frenzy_region,

    LocationName.fire_ball_frenzy_region,
    LocationName.demolition_drain_pipe_region,
    LocationName.ripsaw_rage_region,
    LocationName.blazing_bazookas_region,
    LocationName.low_g_labyrinth_region,

    LocationName.krevice_kreepers_region,
    LocationName.tearaway_toboggan_region,
    LocationName.barrel_drop_bounce_region,
    LocationName.krack_shot_kroc_region,
    LocationName.lemguin_lunge_region,

    LocationName.buzzer_barrage_region,
    LocationName.kong_fused_cliffs_region,
    LocationName.floodlit_fish_region,
    LocationName.pothole_panic_region,
    LocationName.ropey_rumpus_region,

    LocationName.konveyor_rope_clash_region,
    LocationName.creepy_caverns_region,
    LocationName.lightning_lookout_region,
    LocationName.koindozer_klamber_region,
    LocationName.poisonous_pipeline_region,

    LocationName.stampede_sprint_region,
    LocationName.criss_cross_cliffs_region,
    LocationName.tyrant_twin_tussle_region,
    LocationName.swoopy_salvo_region,
    #LocationName.rocket_rush_region,
]
