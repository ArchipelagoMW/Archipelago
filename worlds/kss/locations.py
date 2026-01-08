from typing import NamedTuple
from BaseClasses import Location
from .names import location_names, item_names
from .items import BASE_ID


class KSSLocation(Location):
    game = "Kirby Super Star"


class LocationData(NamedTuple):
    code: int | None
    tag: str = ""


green_greens_locations = {
    location_names.sb_whispy: LocationData(BASE_ID + 0),
    location_names.sb_gg_maxim: LocationData(BASE_ID + 0x100, "maxim"),
    location_names.sb_gg_1up: LocationData(BASE_ID + 0x200, "one_up")
}

float_islands_locations = {
    location_names.sb_lololo: LocationData(BASE_ID + 1),
    location_names.sb_fl_1up: LocationData(BASE_ID + 0x201, "one_up"),
    location_names.sb_fl_candy: LocationData(BASE_ID + 0x400, "candy"),
}

bubbly_clouds_locations = {
    location_names.sb_kracko: LocationData(BASE_ID + 2),
    location_names.sb_bc_1up: LocationData(BASE_ID + 0x202, "one_up"),
    location_names.sb_bc_maxim: LocationData(BASE_ID + 0x101, "maxim"),
    location_names.sb_bc_1up_moon: LocationData(BASE_ID + 0x203, "one_up")
}

mt_dedede_locations = {
    location_names.sb_dedede: LocationData(BASE_ID + 3),
    location_names.sb_complete: LocationData(None),
}

spring_breeze_locations = {
    **green_greens_locations,
    **float_islands_locations,
    **bubbly_clouds_locations,
    **mt_dedede_locations,
}

peanut_plains_locations = {
    location_names.db_stage_1: LocationData(BASE_ID + 4),
    location_names.db_pp_1up_1: LocationData(BASE_ID + 0x204, "one_up"),
    location_names.db_pp_maxim_1: LocationData(BASE_ID + 0x102, "maxim"),
    location_names.db_pp_sword: LocationData(BASE_ID + 0x800, "essence"),
    location_names.db_pp_maxim_2: LocationData(BASE_ID + 0x103, "maxim"),
    location_names.db_pp_1up_2: LocationData(BASE_ID + 0x205, "one_up"),
    location_names.db_pp_candy: LocationData(BASE_ID + 0x401, "candy"),
    location_names.db_pp_maxim_3: LocationData(BASE_ID + 0x104, "maxim"),
}

mallow_castle_locations = {
    location_names.db_stage_2: LocationData(BASE_ID + 5),
    location_names.db_switch_1: LocationData(BASE_ID + 9),
    location_names.db_mc_1up_1: LocationData(BASE_ID + 0x206, "one_up"),
    location_names.db_mc_wheel: LocationData(BASE_ID + 0x801, "essence"),
    location_names.db_mc_maxim_1: LocationData(BASE_ID + 0x105, "maxim"),
    location_names.db_mc_1up_2: LocationData(BASE_ID + 0x207, "one_up"),
    location_names.db_mc_1up_3: LocationData(BASE_ID + 0x208, "one_up"),
    location_names.db_mc_1up_4: LocationData(BASE_ID + 0x209, "one_up"),
    location_names.db_mc_1up_5: LocationData(BASE_ID + 0x20A, "one_up"),
}

bonus_1_locations = {
    location_names.db_b1_maxim_l: LocationData(BASE_ID + 0x106, "maxim"),
    location_names.db_b1_maxim_r: LocationData(BASE_ID + 0x107, "maxim"),
    location_names.db_b1_beam: LocationData(BASE_ID + 0x802, "essence"),
    location_names.db_b1_fire: LocationData(BASE_ID + 0x803, "essence"),
    location_names.db_b1_mirror: LocationData(BASE_ID + 0x804, "essence"),
    location_names.db_b1_fighter: LocationData(BASE_ID + 0x805, "essence"),
    location_names.db_b1_cutter: LocationData(BASE_ID + 0x806, "essence"),
    location_names.db_b1_plasma: LocationData(BASE_ID + 0x807, "essence"),
    location_names.db_b1_ninja: LocationData(BASE_ID + 0x808, "essence"),
    location_names.db_b1_sword: LocationData(BASE_ID + 0x809, "essence"),
    location_names.db_b1_bomb: LocationData(BASE_ID + 0x80A, "essence"),
    location_names.db_b1_hammer: LocationData(BASE_ID + 0x80B, "essence"),
}

cocoa_cave_locations = {
    location_names.db_stage_3: LocationData(BASE_ID + 6),
    location_names.db_iron_mam: LocationData(BASE_ID + 11),
    location_names.db_cc_maxim_1: LocationData(BASE_ID + 0x108, "maxim"),
    location_names.db_cc_1up_1: LocationData(BASE_ID + 0x20B, "one_up"),
    location_names.db_cc_1up_2: LocationData(BASE_ID + 0x20C, "one_up"),
}

candy_mountain_locations = {
    location_names.db_stage_4: LocationData(BASE_ID + 7),
    location_names.db_switch_2: LocationData(BASE_ID + 10),
    location_names.db_cm_1up_1: LocationData(BASE_ID + 0x20D, "one_up"),
    location_names.db_cm_hammer: LocationData(BASE_ID + 0x80C, "essence"),
    location_names.db_cm_1up_2: LocationData(BASE_ID + 0x20E, "one_up"),
    location_names.db_cm_1up_3: LocationData(BASE_ID + 0x20F, "one_up"),
    location_names.db_cm_1up_4: LocationData(BASE_ID + 0x210, "one_up"),
    location_names.db_cm_candy: LocationData(BASE_ID + 0x402, "candy"),
    location_names.db_cm_maxim_1: LocationData(BASE_ID + 0x109, "maxim"),
    location_names.db_cm_maxim_2: LocationData(BASE_ID + 0x10A, "maxim"),
    location_names.db_cm_1up_5: LocationData(BASE_ID + 0x211, "one_up"),
    location_names.db_cm_copy: LocationData(BASE_ID + 0x80D, "essence"),
    location_names.db_cm_1up_6: LocationData(BASE_ID + 0x212, "one_up"),
    location_names.db_cm_maxim_3: LocationData(BASE_ID + 0x10B, "maxim")
}

bonus_2_locations = {
    location_names.db_b2_wheel: LocationData(BASE_ID + 0x80E, "essence"),
    location_names.db_b2_yoyo: LocationData(BASE_ID + 0x80F, "essence"),
    location_names.db_b2_wing: LocationData(BASE_ID + 0x810, "essence"),
    location_names.db_b2_stone: LocationData(BASE_ID + 0x811, "essence"),
    location_names.db_b2_parasol: LocationData(BASE_ID + 0x812, "essence"),
    location_names.db_b2_jet: LocationData(BASE_ID + 0x813, "essence"),
    location_names.db_b2_ice: LocationData(BASE_ID + 0x814, "essence"),
    location_names.db_b2_suplex: LocationData(BASE_ID + 0x815, "essence"),
    location_names.db_b2_copy: LocationData(BASE_ID + 0x816, "essence"),
    location_names.db_b2_maxim: LocationData(BASE_ID + 0x10C, "maxim"),
}

dyna_blade_nest_locations = {
    location_names.db_stage_5: LocationData(BASE_ID + 8),
    location_names.db_complete: LocationData(None),
    location_names.db_db_cutter: LocationData(BASE_ID + 0x860, "essence"),
    location_names.db_db_beam: LocationData(BASE_ID + 0x861, "essence"),
    location_names.db_db_fire: LocationData(BASE_ID + 0x862, "essence"),
    location_names.db_db_sword: LocationData(BASE_ID + 0x863, "essence"),
}

dyna_blade_locations = {
    **peanut_plains_locations,
    **mallow_castle_locations,
    **cocoa_cave_locations,
    **candy_mountain_locations,
    **dyna_blade_nest_locations,
    **bonus_1_locations,
    **bonus_2_locations,
}

gourmet_race_locations = {
    location_names.gr_stage_1: LocationData(BASE_ID + 12),
    location_names.gr_stage_2: LocationData(BASE_ID + 13),
    location_names.gr_stage_3: LocationData(BASE_ID + 14),
    location_names.gr_complete: LocationData(None),
    location_names.gr_jet: LocationData(BASE_ID + 0x817, "essence"),
    location_names.gr_parasol: LocationData(BASE_ID + 0x818, "essence"),
    location_names.gr_ninja: LocationData(BASE_ID + 0x819, "essence"),
    location_names.gr_wing: LocationData(BASE_ID + 0x81A, "essence"),
    location_names.gr_wheel: LocationData(BASE_ID + 0x81B, "essence"),
}

subtree_locations = {
    location_names.tgco_fatty_whale: LocationData(BASE_ID + 15),
    location_names.tgco_treasure_1: LocationData(BASE_ID + 19),
    location_names.tgco_treasure_2: LocationData(BASE_ID + 20),
    location_names.tgco_treasure_3: LocationData(BASE_ID + 21),
    location_names.tgco_treasure_4: LocationData(BASE_ID + 22),
    location_names.tgco_treasure_5: LocationData(BASE_ID + 23),
    location_names.tgco_treasure_6: LocationData(BASE_ID + 24),
    location_names.tgco_treasure_7: LocationData(BASE_ID + 25),
    location_names.tgco_treasure_8: LocationData(BASE_ID + 26),
    location_names.tgco_treasure_9: LocationData(BASE_ID + 27),
    location_names.tgco_treasure_10: LocationData(BASE_ID + 28),
    location_names.tgco_treasure_11: LocationData(BASE_ID + 29),
    location_names.tgco_treasure_12: LocationData(BASE_ID + 30),
    location_names.tgco_treasure_13: LocationData(BASE_ID + 31),
    location_names.tgco_st_1up_1: LocationData(BASE_ID + 0x213, "one_up"),
    location_names.tgco_st_maxim_1: LocationData(BASE_ID + 0x10D, "maxim"),
    location_names.tgco_st_1up_2: LocationData(BASE_ID + 0x214, "one_up"),
    location_names.tgco_st_maxim_2: LocationData(BASE_ID + 0x10E, "maxim"),
    location_names.tgco_st_jet: LocationData(BASE_ID + 0x81C, "essence"),
    location_names.tgco_st_mirror: LocationData(BASE_ID + 0x81D, "essence"),
    location_names.tgco_st_sword: LocationData(BASE_ID + 0x81E, "essence"),
    location_names.tgco_st_maxim_3: LocationData(BASE_ID + 0x10F, "maxim"),
}

crystal_locations = {
    location_names.tgco_virus: LocationData(BASE_ID + 16),
    location_names.tgco_treasure_14: LocationData(BASE_ID + 32),
    location_names.tgco_treasure_15: LocationData(BASE_ID + 33),
    location_names.tgco_treasure_16: LocationData(BASE_ID + 34),
    location_names.tgco_treasure_17: LocationData(BASE_ID + 35),
    location_names.tgco_treasure_18: LocationData(BASE_ID + 36),
    location_names.tgco_treasure_19: LocationData(BASE_ID + 37),
    location_names.tgco_treasure_20: LocationData(BASE_ID + 38),
    location_names.tgco_treasure_21: LocationData(BASE_ID + 39),
    location_names.tgco_treasure_22: LocationData(BASE_ID + 40),
    location_names.tgco_treasure_23: LocationData(BASE_ID + 41),
    location_names.tgco_treasure_24: LocationData(BASE_ID + 42),
    location_names.tgco_treasure_25: LocationData(BASE_ID + 43),
    location_names.tgco_treasure_26: LocationData(BASE_ID + 44),
    location_names.tgco_treasure_27: LocationData(BASE_ID + 45),
    location_names.tgco_treasure_28: LocationData(BASE_ID + 46),
    location_names.tgco_treasure_29: LocationData(BASE_ID + 47),
    location_names.tgco_cr_1up_1: LocationData(BASE_ID + 0x215, "one_up"),
    location_names.tgco_cr_maxim_1: LocationData(BASE_ID + 0x110, "maxim"),
    location_names.tgco_cr_maxim_2: LocationData(BASE_ID + 0x111, "maxim"),
    location_names.tgco_cr_maxim_3: LocationData(BASE_ID + 0x112, "maxim"),
    location_names.tgco_cr_maxim_4: LocationData(BASE_ID + 0x113, "maxim"),
    location_names.tgco_cr_fighter: LocationData(BASE_ID + 0x81F, "essence"),
    location_names.tgco_cr_wing: LocationData(BASE_ID + 0x820, "essence"),
    location_names.tgco_cr_jet: LocationData(BASE_ID + 0x821, "essence"),
    location_names.tgco_cr_maxim_5: LocationData(BASE_ID + 0x114, "maxim"),
}

old_tower_locations = {
    location_names.tgco_chameleon: LocationData(BASE_ID + 17),
    location_names.tgco_treasure_30: LocationData(BASE_ID + 48),
    location_names.tgco_treasure_31: LocationData(BASE_ID + 49),
    location_names.tgco_treasure_32: LocationData(BASE_ID + 50),
    location_names.tgco_treasure_33: LocationData(BASE_ID + 51),
    location_names.tgco_treasure_34: LocationData(BASE_ID + 52),
    location_names.tgco_treasure_35: LocationData(BASE_ID + 53),
    location_names.tgco_treasure_36: LocationData(BASE_ID + 54),
    location_names.tgco_treasure_37: LocationData(BASE_ID + 55),
    location_names.tgco_treasure_38: LocationData(BASE_ID + 56),
    location_names.tgco_treasure_39: LocationData(BASE_ID + 57),
    location_names.tgco_treasure_40: LocationData(BASE_ID + 58),
    location_names.tgco_treasure_41: LocationData(BASE_ID + 59),
    location_names.tgco_treasure_42: LocationData(BASE_ID + 60),
    location_names.tgco_treasure_43: LocationData(BASE_ID + 61),
    location_names.tgco_treasure_44: LocationData(BASE_ID + 62),
    location_names.tgco_treasure_45: LocationData(BASE_ID + 63),
    location_names.tgco_ot_maxim_1: LocationData(BASE_ID + 0x115, "maxim"),
    location_names.tgco_ot_maxim_2: LocationData(BASE_ID + 0x116, "maxim"),
    location_names.tgco_ot_1up_1: LocationData(BASE_ID + 0x216, "one_up"),
    location_names.tgco_ot_maxim_3: LocationData(BASE_ID + 0x117, "maxim"),
    location_names.tgco_ot_maxim_4: LocationData(BASE_ID + 0x118, "maxim"),
    location_names.tgco_ot_sleep_1: LocationData(BASE_ID + 0x822, "essence"),
    location_names.tgco_ot_sleep_2: LocationData(BASE_ID + 0x823, "essence"),
    location_names.tgco_ot_sleep_3: LocationData(BASE_ID + 0x824, "essence"),
    location_names.tgco_ot_sleep_4: LocationData(BASE_ID + 0x825, "essence"),
    location_names.tgco_ot_sleep_5: LocationData(BASE_ID + 0x826, "essence"),
    location_names.tgco_ot_sleep_6: LocationData(BASE_ID + 0x827, "essence"),
    location_names.tgco_ot_sleep_7: LocationData(BASE_ID + 0x828, "essence"),
    location_names.tgco_ot_sleep_8: LocationData(BASE_ID + 0x829, "essence"),
    location_names.tgco_ot_maxim_5: LocationData(BASE_ID + 0x119, "maxim"),
    location_names.tgco_ot_ninja: LocationData(BASE_ID + 0x82A, "essence"),
    location_names.tgco_ot_wing: LocationData(BASE_ID + 0x82B, "essence"),
    location_names.tgco_ot_plasma: LocationData(BASE_ID + 0x82C, "essence"),
    location_names.tgco_ot_maxim_6: LocationData(BASE_ID + 0x11A, "maxim"),
    location_names.tgco_ot_mirror: LocationData(BASE_ID + 0x82D, "essence"),
    location_names.tgco_ot_maxim_7: LocationData(BASE_ID + 0x11B, "maxim"),
    location_names.tgco_ot_maxim_8: LocationData(BASE_ID + 0x11C, "maxim"),
    location_names.tgco_ot_maxim_9: LocationData(BASE_ID + 0x11D, "maxim"),
    location_names.tgco_ot_maxim_10: LocationData(BASE_ID + 0x11E, "maxim"),
    location_names.tgco_ot_maxim_11: LocationData(BASE_ID + 0x11F, "maxim"),
    location_names.tgco_ot_maxim_12: LocationData(BASE_ID + 0x120, "maxim"),
    location_names.tgco_ot_1up_2: LocationData(BASE_ID + 0x217, "one_up"),
}

garden_locations = {
    location_names.tgco_wham_bam: LocationData(BASE_ID + 18),
    location_names.tgco_complete: LocationData(None),
    location_names.tgco_treasure_46: LocationData(BASE_ID + 64),
    location_names.tgco_treasure_47: LocationData(BASE_ID + 65),
    location_names.tgco_treasure_48: LocationData(BASE_ID + 66),
    location_names.tgco_treasure_49: LocationData(BASE_ID + 67),
    location_names.tgco_treasure_50: LocationData(BASE_ID + 68),
    location_names.tgco_treasure_51: LocationData(BASE_ID + 69),
    location_names.tgco_treasure_52: LocationData(BASE_ID + 70),
    location_names.tgco_treasure_53: LocationData(BASE_ID + 71),
    location_names.tgco_treasure_54: LocationData(BASE_ID + 72),
    location_names.tgco_treasure_55: LocationData(BASE_ID + 73),
    location_names.tgco_treasure_56: LocationData(BASE_ID + 74),
    location_names.tgco_treasure_57: LocationData(BASE_ID + 75),
    location_names.tgco_treasure_58: LocationData(BASE_ID + 76),
    location_names.tgco_treasure_59: LocationData(BASE_ID + 77),
    location_names.tgco_treasure_60: LocationData(BASE_ID + 78),
    location_names.tgco_ga_jet: LocationData(BASE_ID + 0x82E, "essence"),
    location_names.tgco_ga_wing_1: LocationData(BASE_ID + 0x82F, "essence"),
    location_names.tgco_ga_ninja: LocationData(BASE_ID + 0x830, "essence"),
    location_names.tgco_ga_maxim_1: LocationData(BASE_ID + 0x121, "maxim"),
    location_names.tgco_ga_maxim_2: LocationData(BASE_ID + 0x122, "maxim"),
    location_names.tgco_ga_maxim_3: LocationData(BASE_ID + 0x123, "maxim"),
    location_names.tgco_ga_maxim_4: LocationData(BASE_ID + 0x124, "maxim"),
    location_names.tgco_ga_maxim_11: LocationData(BASE_ID + 0x159, "maxim"),
    location_names.tgco_ga_1up_1: LocationData(BASE_ID + 0x218, "one_up"),
    location_names.tgco_ga_1up_6: LocationData(BASE_ID + 0x230, "one_up"),
    location_names.tgco_ga_wing_2: LocationData(BASE_ID + 0x831, "essence"),
    location_names.tgco_ga_plasma: LocationData(BASE_ID + 0x832, "essence"),
    location_names.tgco_ga_maxim_5: LocationData(BASE_ID + 0x125, "maxim"),
    location_names.tgco_ga_wheel: LocationData(BASE_ID + 0x833, "essence"),
    location_names.tgco_ga_sleep: LocationData(BASE_ID + 0x834, "essence"),
    location_names.tgco_ga_parasol_1: LocationData(BASE_ID + 0x835, "essence"),
    location_names.tgco_ga_1up_2: LocationData(BASE_ID + 0x219, "one_up"),
    location_names.tgco_ga_maxim_6: LocationData(BASE_ID + 0x126, "maxim"),
    location_names.tgco_ga_maxim_7: LocationData(BASE_ID + 0x127, "maxim"),
    location_names.tgco_ga_1up_3: LocationData(BASE_ID + 0x21A, "one_up"),
    location_names.tgco_ga_1up_4: LocationData(BASE_ID + 0x21B, "one_up"),
    location_names.tgco_ga_1up_5: LocationData(BASE_ID + 0x21C, "one_up"),
    location_names.tgco_ga_maxim_8: LocationData(BASE_ID + 0x128, "maxim"),
    location_names.tgco_ga_maxim_9: LocationData(BASE_ID + 0x129, "maxim"),
    location_names.tgco_ga_bomb: LocationData(BASE_ID + 0x836, "essence"),
    location_names.tgco_ga_ice: LocationData(BASE_ID + 0x837, "essence"),
    location_names.tgco_ga_parasol_2: LocationData(BASE_ID + 0x838, "essence"),
    location_names.tgco_ga_maxim_10: LocationData(BASE_ID + 0x12A, "maxim"),
}

tgco_locations = {
    **subtree_locations,
    **crystal_locations,
    **old_tower_locations,
    **garden_locations,
}

romk_chapter_1_locations = {
    location_names.romk_chapter_1: LocationData(BASE_ID + 79),
}

romk_chapter_2_locations = {
    location_names.romk_chapter_2: LocationData(BASE_ID + 80),
    location_names.romk_c2_maxim_1: LocationData(BASE_ID + 0x12B, "maxim"),
    location_names.romk_c2_maxim_2: LocationData(BASE_ID + 0x12C, "maxim"),
    location_names.romk_c2_parasol: LocationData(BASE_ID + 0x839, "essence"),
    location_names.romk_c2_bomb: LocationData(BASE_ID + 0x83A, "essence"),
    location_names.romk_c2_wing: LocationData(BASE_ID + 0x83B, "essence"),
}

romk_chapter_3_locations = {
    location_names.romk_chapter_3: LocationData(BASE_ID + 81),
    location_names.romk_c3_1up_1: LocationData(BASE_ID + 0x21D, "one_up"),
    location_names.romk_c3_cutter_1: LocationData(BASE_ID + 0x83C, "essence"),
    location_names.romk_c3_sword: LocationData(BASE_ID + 0x83D, "essence"),
    location_names.romk_c3_fighter: LocationData(BASE_ID + 0x83E, "essence"),
    location_names.romk_c3_1up_3: LocationData(BASE_ID + 0x232, "one_up"),
    location_names.romk_c3_cutter_2: LocationData(BASE_ID + 0x83F, "essence"),
    location_names.romk_c3_ice: LocationData(BASE_ID + 0x840, "essence"),
    location_names.romk_c3_1up_2: LocationData(BASE_ID + 0x22F, "one_up"),
    location_names.romk_c3_maxim_1: LocationData(BASE_ID + 0x12D, "maxim"),
    location_names.romk_c3_mirror: LocationData(BASE_ID + 0x841, "essence"),
    location_names.romk_c3_parasol: LocationData(BASE_ID + 0x842, "essence"),
    location_names.romk_c3_ninja: LocationData(BASE_ID + 0x843, "essence"),
    location_names.romk_c3_wheel: LocationData(BASE_ID + 0x844, "essence"),
}

romk_chapter_4_locations = {
    location_names.romk_chapter_4: LocationData(BASE_ID + 82),
    location_names.romk_c4_sword: LocationData(BASE_ID + 0x864, "essence"),
    location_names.romk_c4_candy_1: LocationData(BASE_ID + 0x403, "candy"),
    location_names.romk_c4_maxim_1: LocationData(BASE_ID + 0x12E, "maxim"),
    location_names.romk_c4_fire: LocationData(BASE_ID + 0x845, "essence"),
    location_names.romk_c4_yoyo: LocationData(BASE_ID + 0x846, "essence"),
    location_names.romk_c4_beam: LocationData(BASE_ID + 0x847, "essence"),
    location_names.romk_c4_maxim_2: LocationData(BASE_ID + 0x12F, "maxim"),
}

romk_chapter_5_locations = {
    location_names.romk_chapter_5: LocationData(BASE_ID + 83),
    location_names.romk_c5_maxim_1: LocationData(BASE_ID + 0x130, "maxim"),
    location_names.romk_c5_maxim_2: LocationData(BASE_ID + 0x131, "maxim"),
    location_names.romk_c5_sword: LocationData(BASE_ID + 0x848, "essence"),
    location_names.romk_c5_wing: LocationData(BASE_ID + 0x849, "essence"),
    location_names.romk_c5_ice: LocationData(BASE_ID + 0x84A, "essence"),
    location_names.romk_c5_parasol: LocationData(BASE_ID + 0x84B, "essence"),
    location_names.romk_c5_beam: LocationData(BASE_ID + 0x84C, "essence"),
    location_names.romk_c5_hammer: LocationData(BASE_ID + 0x84D, "essence"),
    location_names.romk_c5_plasma: LocationData(BASE_ID + 0x84E, "essence"),
    location_names.romk_c5_cutter: LocationData(BASE_ID + 0x84F, "essence"),
    location_names.romk_c5_mirror: LocationData(BASE_ID + 0x850, "essence"),
    location_names.romk_c5_maxim_3: LocationData(BASE_ID + 0x132, "maxim"),
}

romk_chapter_6_locations = {
    location_names.romk_chapter_6: LocationData(BASE_ID + 84),
    location_names.romk_c6_parasol: LocationData(BASE_ID + 0x851, "essence"),
    location_names.romk_c6_jet: LocationData(BASE_ID + 0x852, "essence"),
    location_names.romk_c6_wing_1: LocationData(BASE_ID + 0x853, "essence"),
    location_names.romk_c6_candy: LocationData(BASE_ID + 0x404, "candy"),
    location_names.romk_c6_maxim_1: LocationData(BASE_ID + 0x133, "maxim"),
    location_names.romk_c6_wing_2: LocationData(BASE_ID + 0x854, "essence"),
    location_names.romk_c6_suplex: LocationData(BASE_ID + 0x855, "essence"),
    location_names.romk_c6_yoyo: LocationData(BASE_ID + 0x856, "essence"),
    location_names.romk_c6_1up_1: LocationData(BASE_ID + 0x21E, "one_up"),
    location_names.romk_c6_1up_2: LocationData(BASE_ID + 0x21F, "one_up"),
    location_names.romk_c6_maxim_2: LocationData(BASE_ID + 0x134, "maxim"),
    location_names.romk_c6_bomb: LocationData(BASE_ID + 0x857, "essence"),
    location_names.romk_c6_maxim_3: LocationData(BASE_ID + 0x135, "maxim"),
}

romk_chapter_7_locations = {
    location_names.romk_chapter_7: LocationData(BASE_ID + 85),
    location_names.romk_complete: LocationData(None),
    location_names.romk_c7_cutter_1: LocationData(BASE_ID + 0x858, "essence"),
    location_names.romk_c7_parasol: LocationData(BASE_ID + 0x859, "essence"),
    location_names.romk_c7_yoyo: LocationData(BASE_ID + 0x85A, "essence"),
    location_names.romk_c7_stone: LocationData(BASE_ID + 0x85B, "essence"),
    location_names.romk_c7_ninja_1: LocationData(BASE_ID + 0x85C, "essence"),
    location_names.romk_c7_maxim_1: LocationData(BASE_ID + 0x136, "maxim"),
    location_names.romk_c7_maxim_2: LocationData(BASE_ID + 0x137, "maxim"),
    location_names.romk_c7_maxim_3: LocationData(BASE_ID + 0x138, "maxim"),
    location_names.romk_c7_ninja_2: LocationData(BASE_ID + 0x85D, "essence"),
    location_names.romk_c7_sleep: LocationData(BASE_ID + 0x85E, "essence"),
    location_names.romk_c7_cutter_2: LocationData(BASE_ID + 0x85F, "essence"),
    location_names.romk_c7_maxim_4: LocationData(BASE_ID + 0x139, "maxim"),
}

revenge_of_meta_knight_locations = {
    **romk_chapter_1_locations,
    **romk_chapter_2_locations,
    **romk_chapter_3_locations,
    **romk_chapter_4_locations,
    **romk_chapter_5_locations,
    **romk_chapter_6_locations,
    **romk_chapter_7_locations,
}

floria_locations = {
    location_names.mww_floria: LocationData(BASE_ID + 87),
    location_names.mww_cutter: LocationData(BASE_ID + 88),
    location_names.mww_fighter: LocationData(BASE_ID + 89),
    location_names.mww_ice: LocationData(BASE_ID + 90),
    location_names.mww_fl_maxim: LocationData(BASE_ID + 0x13A, "maxim"),
}

aqualiss_locations = {
    location_names.mww_aqualiss: LocationData(BASE_ID + 91),
    location_names.mww_beam: LocationData(BASE_ID + 92),
    location_names.mww_parasol: LocationData(BASE_ID + 93),
    location_names.mww_sword: LocationData(BASE_ID + 94),
    location_names.mww_aq_1up_1: LocationData(BASE_ID + 0x220, "one_up"),
    location_names.mww_aq_maxim_1: LocationData(BASE_ID + 0x13B, "maxim"),
    location_names.mww_aq_1up_2: LocationData(BASE_ID + 0x221, "one_up"),
    location_names.mww_aq_maxim_2: LocationData(BASE_ID + 0x13C, "maxim"),
    location_names.mww_aq_maxim_3: LocationData(BASE_ID + 0x13D, "maxim"),
    location_names.mww_aq_1up_3: LocationData(BASE_ID + 0x222, "one_up"),
    location_names.mww_aq_maxim_4: LocationData(BASE_ID + 0x13E, "maxim"),

}

skyhigh_locations = {
    location_names.mww_skyhigh: LocationData(BASE_ID + 95),
    location_names.mww_jet: LocationData(BASE_ID + 96),
    location_names.mww_wheel: LocationData(BASE_ID + 97),
    location_names.mww_wing: LocationData(BASE_ID + 98),
    location_names.mww_sh_1up_1: LocationData(BASE_ID + 0x223, "one_up"),
    location_names.mww_sh_maxim_1: LocationData(BASE_ID + 0x13F, "maxim"),
    location_names.mww_sh_candy: LocationData(BASE_ID + 0x405, "candy"),
    location_names.mww_sh_maxim_2: LocationData(BASE_ID + 0x140, "maxim"),
}

hotbeat_locations = {
    location_names.mww_hotbeat: LocationData(BASE_ID + 99),
    location_names.mww_fire: LocationData(BASE_ID + 100),
    location_names.mww_suplex: LocationData(BASE_ID + 101),
    location_names.mww_hb_candy: LocationData(BASE_ID + 0x406, "candy"),
    location_names.mww_hb_maxim_1: LocationData(BASE_ID + 0x141, "maxim"),
    location_names.mww_hb_maxim_2: LocationData(BASE_ID + 0x142, "maxim"),
    location_names.mww_hb_maxim_3: LocationData(BASE_ID + 0x143, "maxim"),
    location_names.mww_hb_1up_1: LocationData(BASE_ID + 0x224, "one_up"),
    location_names.mww_hb_1up_2: LocationData(BASE_ID + 0x225, "one_up"),
    location_names.mww_hb_1up_3: LocationData(BASE_ID + 0x231, "one_up"),
    location_names.mww_hb_maxim_4: LocationData(BASE_ID + 0x144, "maxim"),
    location_names.mww_hb_maxim_5: LocationData(BASE_ID + 0x145, "maxim"),
    location_names.mww_hb_1up_4: LocationData(BASE_ID + 0x226, "one_up"),
    location_names.mww_hb_maxim_6: LocationData(BASE_ID + 0x146, "maxim"),
    location_names.mww_hb_maxim_7: LocationData(BASE_ID + 0x147, "maxim"),
}

cavios_locations = {
    location_names.mww_cavios: LocationData(BASE_ID + 102),
    location_names.mww_bomb: LocationData(BASE_ID + 103),
    location_names.mww_hammer: LocationData(BASE_ID + 104),
    location_names.mww_stone: LocationData(BASE_ID + 105),
    location_names.mww_cv_maxim_1: LocationData(BASE_ID + 0x148, "maxim"),
    location_names.mww_cv_maxim_2: LocationData(BASE_ID + 0x149, "maxim"),
    location_names.mww_cv_maxim_3: LocationData(BASE_ID + 0x14A, "maxim"),
    location_names.mww_cv_1up_1: LocationData(BASE_ID + 0x227, "one_up"),
    location_names.mww_cv_maxim_4: LocationData(BASE_ID + 0x14B, "maxim"),
    location_names.mww_cv_maxim_5: LocationData(BASE_ID + 0x14C, "maxim"),
    location_names.mww_cv_1up_2: LocationData(BASE_ID + 0x228, "one_up"),
    location_names.mww_cv_candy: LocationData(BASE_ID + 0x407, "candy"),
}

mecheye_locations = {
    location_names.mww_mecheye: LocationData(BASE_ID + 106),
    location_names.mww_plasma: LocationData(BASE_ID + 107),
    location_names.mww_yoyo: LocationData(BASE_ID + 108),
    location_names.mww_me_1up_1: LocationData(BASE_ID + 0x229, "one_up"),
    location_names.mww_me_candy: LocationData(BASE_ID + 0x408, "candy"),
    location_names.mww_me_1up_2: LocationData(BASE_ID + 0x22A, "one_up"),
    location_names.mww_me_maxim_1: LocationData(BASE_ID + 0x14D, "maxim"),
    location_names.mww_me_maxim_2: LocationData(BASE_ID + 0x14E, "maxim"),
    location_names.mww_me_1up_3: LocationData(BASE_ID + 0x22B, "one_up"),
    location_names.mww_me_1up_4: LocationData(BASE_ID + 0x22C, "one_up"),
    location_names.mww_me_1up_5: LocationData(BASE_ID + 0x22D, "one_up"),
    location_names.mww_me_maxim_3: LocationData(BASE_ID + 0x14F, "maxim"),
}

halfmoon_locations = {
    location_names.mww_halfmoon: LocationData(BASE_ID + 109),
    location_names.mww_mirror: LocationData(BASE_ID + 110),
    location_names.mww_ninja: LocationData(BASE_ID + 111),
    location_names.mww_hm_maxim_1: LocationData(BASE_ID + 0x150, "maxim"),
    location_names.mww_hm_maxim_2: LocationData(BASE_ID + 0x151, "maxim"),
    location_names.mww_hm_1up_1: LocationData(BASE_ID + 0x22E, "one_up"),
    location_names.mww_hm_maxim_3: LocationData(BASE_ID + 0x152, "maxim"),
    location_names.mww_hm_maxim_4: LocationData(BASE_ID + 0x153, "maxim"),
}

copy_planet_locations = {
    location_names.mww_copy: LocationData(BASE_ID + 112)
}

space_locations = {
    location_names.mww_complete: LocationData(None)
}

milky_way_wishes_locations = {
    **floria_locations,
    **aqualiss_locations,
    **skyhigh_locations,
    **hotbeat_locations,
    **cavios_locations,
    **mecheye_locations,
    **halfmoon_locations,
    **copy_planet_locations,
    **space_locations
}

the_arena_locations = {
    location_names.arena_1: LocationData(BASE_ID + 113),
    location_names.arena_2: LocationData(BASE_ID + 114),
    location_names.arena_3: LocationData(BASE_ID + 115),
    location_names.arena_4: LocationData(BASE_ID + 116),
    location_names.arena_5: LocationData(BASE_ID + 117),
    location_names.arena_6: LocationData(BASE_ID + 118),
    location_names.arena_7: LocationData(BASE_ID + 119),
    location_names.arena_8: LocationData(BASE_ID + 120),
    location_names.arena_9: LocationData(BASE_ID + 121),
    location_names.arena_10: LocationData(BASE_ID + 122),
    location_names.arena_11: LocationData(BASE_ID + 123),
    location_names.arena_12: LocationData(BASE_ID + 124),
    location_names.arena_13: LocationData(BASE_ID + 125),
    location_names.arena_14: LocationData(BASE_ID + 126),
    location_names.arena_15: LocationData(BASE_ID + 127),
    location_names.arena_16: LocationData(BASE_ID + 128),
    location_names.arena_17: LocationData(BASE_ID + 129),
    location_names.arena_18: LocationData(BASE_ID + 130),
    location_names.arena_19: LocationData(BASE_ID + 131),
    location_names.arena_complete: LocationData(None),
    location_names.arena_maxim_1: LocationData(BASE_ID + 0x154, "arena_maxim"),
    location_names.arena_maxim_2: LocationData(BASE_ID + 0x155, "arena_maxim"),
    location_names.arena_maxim_3: LocationData(BASE_ID + 0x156, "arena_maxim"),
    location_names.arena_maxim_4: LocationData(BASE_ID + 0x157, "arena_maxim"),
    location_names.arena_maxim_5: LocationData(BASE_ID + 0x158, "arena_maxim"),
}

location_table = {
    **spring_breeze_locations,
    **dyna_blade_locations,
    **gourmet_race_locations,
    **tgco_locations,
    **revenge_of_meta_knight_locations,
    **milky_way_wishes_locations,
    **the_arena_locations
}
