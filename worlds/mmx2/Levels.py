
from worlds.AutoWorld import World
from .Names import LocationName

location_id_to_level_id = {
    LocationName.intro_stage_clear:                     [0x00, 0x007, 0x00],
    LocationName.intro_stage_boss:                      [0x00, 0x000, 0x18],

    LocationName.wheel_gator_boss:                      [0x03, 0x000, 0x06],
    LocationName.wheel_gator_clear:                     [0x03, 0x001, 0x04],
    LocationName.wheel_gator_heart_tank:                [0x03, 0x002, 0x20],
    LocationName.wheel_gator_arms:                      [0x03, 0x003, 0x02],

    LocationName.bubble_crab_boss:                      [0x08, 0x000, 0x01],
    LocationName.bubble_crab_clear:                     [0x08, 0x001, 0x02],
    LocationName.bubble_crab_heart_tank:                [0x08, 0x002, 0x40],
    LocationName.bubble_crab_sub_tank:                  [0x08, 0x004, 0x10],
    LocationName.bubble_crab_mini_boss:                 [0x08, 0x020, 0x12],

    LocationName.flame_stag_boss:                       [0x06, 0x000, 0x02],
    LocationName.flame_stag_clear:                      [0x06, 0x001, 0x0E],
    LocationName.flame_stag_heart_tank:                 [0x06, 0x002, 0x02],
    LocationName.flame_stag_sub_tank:                   [0x06, 0x004, 0x20],

    LocationName.morph_moth_boss:                       [0x01, 0x000, 0x03],
    LocationName.morph_moth_clear:                      [0x01, 0x001, 0x04],
    LocationName.morph_moth_heart_tank:                 [0x01, 0x002, 0x01],
    LocationName.morph_moth_body:                       [0x01, 0x003, 0x04],
    LocationName.morph_moth_mini_boss_1:                [0x01, 0x000, 0x19],

    LocationName.magna_centipede_boss:                  [0x07, 0x000, 0x04],
    LocationName.magna_centipede_clear:                 [0x07, 0x001, 0x0C],
    LocationName.magna_centipede_heart_tank:            [0x07, 0x002, 0x08],
    LocationName.magna_centipede_sub_tank:              [0x07, 0x004, 0x40],
    LocationName.magna_centipede_mini_boss_1:           [0x07, 0x000, 0x1A],
    LocationName.magna_centipede_mini_boss_2:           [0x07, 0x000, 0x1B],
    
    LocationName.crystal_snail_boss:                    [0x02, 0x000, 0x05],
    LocationName.crystal_snail_clear:                   [0x02, 0x001, 0x00],
    LocationName.crystal_snail_heart_tank:              [0x02, 0x002, 0x10],
    LocationName.crystal_snail_helmet:                  [0x02, 0x003, 0x01],
    LocationName.crystal_snail_mini_boss_1:             [0x02, 0x020, 0x03],

    LocationName.overdrive_ostrich_boss:                [0x05, 0x000, 0x06],
    LocationName.overdrive_ostrich_clear:               [0x05, 0x001, 0x08],
    LocationName.overdrive_ostrich_heart_tank:          [0x05, 0x002, 0x04],
    LocationName.overdrive_ostrich_leg:                 [0x05, 0x003, 0x08],

    LocationName.wire_sponge_boss:                      [0x04, 0x000, 0x07],
    LocationName.wire_sponge_clear:                     [0x04, 0x001, 0x0A],
    LocationName.wire_sponge_heart_tank:                [0x04, 0x002, 0x80],
    LocationName.wire_sponge_sub_tank:                  [0x04, 0x004, 0x80],

    LocationName.agile_defeated:                        [0x09, 0x000, 0x08],
    LocationName.serges_defeated:                       [0x09, 0x000, 0x09],
    LocationName.violen_defeated:                       [0x09, 0x000, 0x0A],

    LocationName.x_hunter_stage_1_boss:                 [0x0A, 0x000, 0x0B],

    LocationName.x_hunter_stage_2_boss:                 [0x0A, 0x000, 0x0C],

    LocationName.x_hunter_stage_3_boss:                 [0x0A, 0x000, 0x0D],

    LocationName.x_hunter_stage_4_wheel_gator:          [0x0B, 0x000, 0x0E],
    LocationName.x_hunter_stage_4_bubble_crab:          [0x0B, 0x000, 0x0F],
    LocationName.x_hunter_stage_4_flame_stag:           [0x0B, 0x000, 0x10],
    LocationName.x_hunter_stage_4_morph_moth:           [0x0B, 0x000, 0x11],
    LocationName.x_hunter_stage_4_magna_centipede:      [0x0B, 0x000, 0x12],
    LocationName.x_hunter_stage_4_crystal_snail:        [0x0B, 0x000, 0x13],
    LocationName.x_hunter_stage_4_overdrive_ostrich:    [0x0B, 0x000, 0x14],
    LocationName.x_hunter_stage_4_wire_sponge:          [0x0B, 0x000, 0x15],

    LocationName.x_hunter_stage_5_zero:                 [0x0C, 0x000, 0x16],
    LocationName.victory:                               [0x0C, 0x000, 0x17],
}
