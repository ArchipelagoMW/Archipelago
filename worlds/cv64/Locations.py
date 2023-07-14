import typing

from BaseClasses import Location
from .Names import LName, RName


class CV64Location(Location):
    game: str = "Castlevania 64"

    cv64_rom_offset: int
    cv64_loc_type: str
    cv64_stage: str

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, cv64_rom_offset: int = None,
                 cv64_loc_type: str = None, cv64_stage: str = None):
        super().__init__(player, name, address, parent)
        self.cv64_rom_offset = cv64_rom_offset
        self.cv64_loc_type = cv64_loc_type
        self.cv64_stage = cv64_stage


class LocationData(typing.NamedTuple):
    code: typing.Optional[int]
    cv64_rom_offset: int
    region: str
    cv64_loc_type: str = "normal"


main_location_table = {
    # Forest of Silence locations
    LName.forest_pillars_right:   LocationData(0xC64001, 0x10C67B, RName.forest_start),
    LName.forest_pillars_top:     LocationData(0xC64002, 0x10C71B, RName.forest_start),
    LName.forest_bone_mom:        LocationData(0xC64003, 0x10C6BB, RName.forest_start),
    LName.forest_lgaz_in:         LocationData(0xC64004, 0x10C68B, RName.forest_start),
    LName.forest_lgaz_top:        LocationData(0xC64005, 0x10C693, RName.forest_start),
    LName.forest_hgaz_in:         LocationData(0xC64006, 0x10C6C3, RName.forest_start),
    LName.forest_hgaz_top:        LocationData(0xC64007, 0x10C6E3, RName.forest_start),
    LName.forest_weretiger_sw:    LocationData(0xC64008, 0x10C6CB, RName.forest_start),
    LName.forest_weretiger_gate:  LocationData(0xC64009, 0x10C683, RName.forest_start),
    LName.forest_dirge_plaque:    LocationData(0xC6400A, 0x7C7F9D, RName.forest_start, "inv"),
    LName.forest_dirge_tomb_u:    LocationData(0xC6400B, 0x10C743, RName.forest_start),
    LName.forest_corpse_save:     LocationData(0xC6400C, 0x10C6A3, RName.forest_start),
    LName.forest_dbridge_wall:    LocationData(0xC6400D, 0x10C69B, RName.forest_start),
    LName.forest_dbridge_sw:      LocationData(0xC6400E, 0x10C6D3, RName.forest_start),
    LName.forest_dbridge_gate_r:  LocationData(0xC6400F, 0x10C6AB, RName.forest_mid),
    LName.forest_dbridge_tomb_uf: LocationData(0xC64010, 0x10C76B, RName.forest_mid),
    LName.forest_bface_tomb_lf:   LocationData(0xC64011, 0x10C75B, RName.forest_mid),
    LName.forest_bface_tomb_u:    LocationData(0xC64012, 0x10C77B, RName.forest_mid),
    LName.forest_ibridge:         LocationData(0xC64013, 0x10C713, RName.forest_mid),
    LName.forest_werewolf_tomb_r: LocationData(0xC64014, 0x10C733, RName.forest_mid),
    LName.forest_werewolf_plaque: LocationData(0xC64015, 0xBFC8B7, RName.forest_mid, "inv"),
    LName.forest_werewolf_tree:   LocationData(0xC64016, 0x10C6B3, RName.forest_mid),
    LName.forest_final_sw:        LocationData(0xC64017, 0x10C72B, RName.forest_mid),
    # Castle Wall locations
    LName.cwr_bottom:        LocationData(0xC64018, 0x10C7E7, RName.cw_start),
    LName.cw_dragon_sw:      LocationData(0xC64019, 0x10C817, RName.cw_start),
    LName.cw_rrampart:       LocationData(0xC6401A, 0x10C7FF, RName.cw_start),
    LName.cw_lrampart:       LocationData(0xC6401B, 0x10C807, RName.cw_start),
    LName.cw_shelf_visible:  LocationData(0xC6401C, 0x7F99A9, RName.cw_start),
    LName.cw_shelf_sandbags: LocationData(0xC6401D, 0x7F9A3E, RName.cw_start, "inv"),
    LName.cw_ground_middle:  LocationData(0xC6401E, 0x10C7F7, RName.cw_start),
    LName.cwl_bottom:        LocationData(0xC6401F, 0x10C7DF, RName.cw_ltower),
    LName.cwl_bridge:        LocationData(0xC64020, 0x10C7EF, RName.cw_ltower),
    LName.cw_drac_sw:        LocationData(0xC64021, 0x10C80F, RName.cw_ltower),
    # Villa locations
    LName.villafy_outer_gate_l:          LocationData(0xC64022, 0x10C87F, RName.villa_start),
    LName.villafy_outer_gate_r:          LocationData(0xC64023, 0x10C887, RName.villa_start),
    LName.villafy_dog_platform:          LocationData(0xC64024, 0x10C89F, RName.villa_start),
    LName.villafy_inner_gate:            LocationData(0xC64025, 0xBFC8DF, RName.villa_start),
    LName.villafy_gate_marker:           LocationData(0xC64026, 0x10C8A7, RName.villa_main),
    LName.villafy_villa_marker:          LocationData(0xC64027, 0x10C897, RName.villa_main),
    LName.villafy_tombstone:             LocationData(0xC64028, 0x8099CC, RName.villa_main, "inv"),
    LName.villafy_fountain_fl:           LocationData(0xC64029, 0xBFC8D7, RName.villa_main),
    LName.villafy_fountain_fr:           LocationData(0xC6402A, 0x80997D, RName.villa_main),
    LName.villafy_fountain_ml:           LocationData(0xC6402B, 0x809956, RName.villa_main),
    LName.villafy_fountain_mr:           LocationData(0xC6402C, 0x80992D, RName.villa_main),
    LName.villafy_fountain_rl:           LocationData(0xC6402D, 0xBFC8DB, RName.villa_main),
    LName.villafy_fountain_rr:           LocationData(0xC6402E, 0x80993C, RName.villa_main),
    LName.villafo_front_r:               LocationData(0xC6402F, 0x10C8E7, RName.villa_main),
    LName.villafo_front_l:               LocationData(0xC64030, 0x10C8DF, RName.villa_main),
    LName.villafo_mid_l:                 LocationData(0xC64031, 0x10C8D7, RName.villa_main),
    LName.villafo_rear_r:                LocationData(0xC64032, 0x10C8C7, RName.villa_main),
    LName.villafo_rear_l:                LocationData(0xC64033, 0x10C8BF, RName.villa_main),
    LName.villafo_pot_r:                 LocationData(0xC64034, 0x10C8AF, RName.villa_main),
    LName.villafo_pot_l:                 LocationData(0xC64035, 0x10C8B7, RName.villa_main),
    LName.villafo_sofa:                  LocationData(0xC64036, 0x81F07C, RName.villa_main),
    LName.villala_hallway_stairs:        LocationData(0xC64037, 0x10C927, RName.villa_main),
    LName.villala_bedroom_chairs:        LocationData(0xC64038, 0x83A588, RName.villa_main),
    LName.villala_bedroom_bed:           LocationData(0xC64039, 0xBFC95B, RName.villa_main),
    LName.villala_vincent:               LocationData(0xC6403A, 0xBFC1BB, RName.villa_main, "npc"),
    LName.villala_slivingroom_table:     LocationData(0xC6403B, 0xBFC96B, RName.villa_main, "inv"),
    LName.villala_diningroom_roses:      LocationData(0xC6403C, 0xBFC90B, RName.villa_main, "inv"),
    LName.villala_llivingroom_pot_r:     LocationData(0xC6403D, 0x10C90F, RName.villa_main),
    LName.villala_llivingroom_pot_l:     LocationData(0xC6403E, 0x10C917, RName.villa_main),
    LName.villala_llivingroom_painting:  LocationData(0xC6403F, 0xBFC907, RName.villa_main, "inv"),
    LName.villala_llivingroom_light:     LocationData(0xC64040, 0x10C91F, RName.villa_main),
    LName.villala_llivingroom_lion:      LocationData(0xC64041, 0x83A610, RName.villa_main, "inv"),
    LName.villala_exit_knight:           LocationData(0xC64042, 0xBFC967, RName.villa_main),
    LName.villala_storeroom_l:           LocationData(0xC64043, 0xBFC95F, RName.villa_storeroom),
    LName.villala_storeroom_r:           LocationData(0xC64044, 0xBFC8FF, RName.villa_storeroom),
    LName.villala_storeroom_s:           LocationData(0xC64045, 0xBFC963, RName.villa_storeroom, "inv"),
    LName.villala_archives_table:        LocationData(0xC64046, 0xBFC90F, RName.villa_archives, "inv"),
    LName.villala_archives_rear:         LocationData(0xC64047, 0x83A5B1, RName.villa_archives),
    LName.villam_malus_torch:            LocationData(0xC64048, 0x10C967, RName.villa_maze),
    LName.villam_malus_bush:             LocationData(0xC64049, 0x850FEC, RName.villa_maze, "inv"),
    LName.villam_frankieturf_l:          LocationData(0xC6404A, 0x10C947, RName.villa_maze),
    LName.villam_frankieturf_ru:         LocationData(0xC6404B, 0x10C9A7, RName.villa_maze),
    LName.villam_fgarden_f:              LocationData(0xC6404C, 0x10C96F, RName.villa_maze),
    LName.villam_fgarden_mf:             LocationData(0xC6404D, 0x10C977, RName.villa_maze),
    LName.villam_fgarden_mr:             LocationData(0xC6404E, 0x10C95F, RName.villa_maze),
    LName.villam_fgarden_r:              LocationData(0xC6404F, 0x10C97F, RName.villa_maze),
    LName.villam_rplatform_de:           LocationData(0xC64050, 0x10C94F, RName.villa_maze),
    LName.villam_exit_de:                LocationData(0xC64051, 0x10C957, RName.villa_maze),
    LName.villam_serv_path:              LocationData(0xC64052, 0x10C92F, RName.villa_maze),
    LName.villafo_serv_ent:              LocationData(0xC64053, 0x10C8EF, RName.villa_servants),
    LName.villam_crypt_ent:              LocationData(0xC64054, 0x10C93F, RName.villa_crypt),
    LName.villam_crypt_upstream:         LocationData(0xC64055, 0x10C937, RName.villa_crypt),
    LName.villac_ent_l:                  LocationData(0xC64056, 0x10CF4B, RName.villa_crypt),
    LName.villac_ent_r:                  LocationData(0xC64057, 0x10CF63, RName.villa_crypt),
    LName.villac_wall_l:                 LocationData(0xC64058, 0x10CF6B, RName.villa_crypt),
    LName.villac_wall_r:                 LocationData(0xC64059, 0x10CF5B, RName.villa_crypt),
    LName.villac_coffin_r:               LocationData(0xC6405A, 0x10CF53, RName.villa_crypt),
    # Tunnel locations
    LName.tunnel_landing:                LocationData(0xC6405B, 0x10C9AF, RName.tunnel_start),
    LName.tunnel_landing_rc:             LocationData(0xC6405C, 0x10C9B7, RName.tunnel_start),
    LName.tunnel_stone_alcove_l:         LocationData(0xC6405D, 0x10CA9F, RName.tunnel_start),
    LName.tunnel_twin_arrows:            LocationData(0xC6405E, 0xBFC993, RName.tunnel_start, "inv"),
    LName.tunnel_lonesome_bucket:        LocationData(0xC6405F, 0xBFC99B, RName.tunnel_start, "inv"),
    LName.tunnel_lbucket_quag:           LocationData(0xC64060, 0x10C9DF, RName.tunnel_start),
    LName.tunnel_lbucket_albert:         LocationData(0xC64061, 0x10C9E7, RName.tunnel_start),
    LName.tunnel_albert_camp:            LocationData(0xC64062, 0x10C9D7, RName.tunnel_start),
    LName.tunnel_albert_quag:            LocationData(0xC64063, 0x10C9CF, RName.tunnel_start),
    LName.tunnel_gondola_rc_sdoor_r:     LocationData(0xC64064, 0x10CA27, RName.tunnel_start),
    LName.tunnel_gondola_rc_sdoor_m:     LocationData(0xC64065, 0x10CAA7, RName.tunnel_start),
    LName.tunnel_gondola_rc:             LocationData(0xC64066, 0x10CAB7, RName.tunnel_start),
    LName.tunnel_rgondola_station:       LocationData(0xC64067, 0x10C9C7, RName.tunnel_start),
    LName.tunnel_gondola_transfer:       LocationData(0xC64068, 0x10CA2F, RName.tunnel_start),
    LName.tunnel_corpse_bucket_quag:     LocationData(0xC64069, 0x10C9F7, RName.tunnel_end),
    LName.tunnel_corpse_bucket_mdoor_r:  LocationData(0xC6406A, 0x10CA37, RName.tunnel_end),
    LName.tunnel_shovel_quag_start:      LocationData(0xC6406B, 0x10C9FF, RName.tunnel_end),
    LName.tunnel_exit_quag_start:        LocationData(0xC6406C, 0x10CA07, RName.tunnel_end),
    LName.tunnel_shovel_quag_end:        LocationData(0xC6406D, 0x10CA0F, RName.tunnel_end),
    LName.tunnel_exit_quag_end:          LocationData(0xC6406E, 0x10CA3F, RName.tunnel_end),
    LName.tunnel_shovel:                 LocationData(0xC6406F, 0x86D8FC, RName.tunnel_end, "inv"),
    LName.tunnel_shovel_save:            LocationData(0xC64070, 0x10CA17, RName.tunnel_end),
    LName.tunnel_shovel_mdoor_l:         LocationData(0xC64071, 0x10CA47, RName.tunnel_end),
    LName.tunnel_shovel_sdoor_l:         LocationData(0xC64072, 0x10CA4F, RName.tunnel_end),
    LName.tunnel_shovel_sdoor_m:         LocationData(0xC64073, 0x10CAAF, RName.tunnel_end),
    # Underground Waterway locations
    LName.uw_near_ent:           LocationData(0xC64074, 0x10CB03, RName.uw_main),
    LName.uw_across_ent:         LocationData(0xC64075, 0x10CAF3, RName.uw_main),
    LName.uw_poison_parkour:     LocationData(0xC64076, 0x10CAFB, RName.uw_main),
    LName.uw_waterfall_alcove:   LocationData(0xC64077, 0x10CB23, RName.uw_main),
    LName.uw_bricks_save:        LocationData(0xC64078, 0x10CB33, RName.uw_main),
    LName.uw_above_skel_ledge:   LocationData(0xC64079, 0x10CB2B, RName.uw_main),
    # Castle Center locations
    LName.ccb_skel_hallway_ent:          LocationData(0xC6407A, 0x10CB67, RName.cc_lower),
    LName.ccb_skel_hallway_jun:          LocationData(0xC6407B, 0x10CBD7, RName.cc_lower),
    LName.ccb_skel_hallway_tc:           LocationData(0xC6407C, 0x10CB6F, RName.cc_lower),
    LName.ccb_behemoth_l_ff:             LocationData(0xC6407D, 0x10CB77, RName.cc_lower),
    LName.ccb_behemoth_l_mf:             LocationData(0xC6407E, 0x10CBA7, RName.cc_lower),
    LName.ccb_behemoth_l_mr:             LocationData(0xC6407F, 0x10CB7F, RName.cc_lower),
    LName.ccb_behemoth_l_fr:             LocationData(0xC64080, 0x10CBAF, RName.cc_lower),
    LName.ccb_behemoth_r_ff:             LocationData(0xC64081, 0x10CBB7, RName.cc_lower),
    LName.ccb_behemoth_r_mf:             LocationData(0xC64082, 0x10CB87, RName.cc_lower),
    LName.ccb_behemoth_r_mr:             LocationData(0xC64083, 0x10CBBF, RName.cc_lower),
    LName.ccb_behemoth_r_fr:             LocationData(0xC64084, 0x10CB8F, RName.cc_lower),
    LName.ccelv_near_machine:            LocationData(0xC64085, 0x10CBF7, RName.cc_lower),
    LName.ccelv_atop_machine:            LocationData(0xC64086, 0x10CC17, RName.cc_lower),
    LName.ccelv_pipes:                   LocationData(0xC64087, 0x10CC07, RName.cc_lower),
    LName.ccelv_staircase:               LocationData(0xC64088, 0x10CBFF, RName.cc_lower),
    LName.ccff_redcarpet_knight:         LocationData(0xC64089, 0x8C44D9, RName.cc_lower, "inv"),
    LName.ccff_gears_side:               LocationData(0xC6408A, 0x10CC33, RName.cc_lower),
    LName.ccff_gears_mid:                LocationData(0xC6408B, 0x10CC3B, RName.cc_lower),
    LName.ccff_gears_corner:             LocationData(0xC6408C, 0x10CC43, RName.cc_lower),
    LName.ccff_lizard_knight:            LocationData(0xC6408D, 0x8C44E7, RName.cc_lower, "inv"),
    LName.ccff_lizard_pit:               LocationData(0xC6408E, 0x10CC4B, RName.cc_lower),
    LName.ccff_lizard_corner:            LocationData(0xC6408F, 0x10CC53, RName.cc_lower),
    LName.ccll_brokenstairs_floor:       LocationData(0xC64090, 0x10CC8F, RName.cc_upper),
    LName.ccll_brokenstairs_knight:      LocationData(0xC64091, 0x8DF782, RName.cc_upper, "inv"),
    LName.ccll_brokenstairs_save:        LocationData(0xC64092, 0x10CC87, RName.cc_upper),
    LName.ccll_glassknight_l:            LocationData(0xC64093, 0x10CC97, RName.cc_upper),
    LName.ccll_glassknight_r:            LocationData(0xC64094, 0x10CC77, RName.cc_upper),
    LName.ccll_butlers_door:             LocationData(0xC64095, 0x10CC7F, RName.cc_upper),
    LName.ccll_butlers_side:             LocationData(0xC64096, 0x10CC9F, RName.cc_upper),
    LName.ccll_cwhall_butlerflames_past: LocationData(0xC64097, 0x10CCA7, RName.cc_upper),
    LName.ccll_cwhall_flamethrower:      LocationData(0xC64098, 0x8DF580, RName.cc_upper, "inv"),
    LName.ccll_cwhall_cwflames:          LocationData(0xC64099, 0x10CCAF, RName.cc_upper),
    LName.ccll_heinrich:                 LocationData(0xC6409A, 0xBFC1C7, RName.cc_upper, "npc"),
    LName.ccia_nitro_crates:             LocationData(0xC6409B, 0x90FCE9, RName.cc_upper, "inv"),
    LName.ccia_nitro_shelf_h:            LocationData(0xC6409C, 0xBFCBFB, RName.cc_upper),
    LName.ccia_stairs_knight:            LocationData(0xC6409D, 0x90FE5C, RName.cc_upper, "inv"),
    LName.ccia_maids_vase:               LocationData(0xC6409E, 0x90FF1D, RName.cc_upper, "inv"),
    LName.ccia_maids_outer:              LocationData(0xC6409F, 0x10CCFF, RName.cc_upper),
    LName.ccia_maids_inner:              LocationData(0xC640A0, 0x10CD07, RName.cc_upper),
    LName.ccia_inventions_maids:         LocationData(0xC640A1, 0x10CCE7, RName.cc_upper),
    LName.ccia_inventions_crusher:       LocationData(0xC640A2, 0x10CCDF, RName.cc_upper),
    LName.ccia_inventions_famicart:      LocationData(0xC640A3, 0x90FBB3, RName.cc_upper, "inv"),
    LName.ccia_inventions_zeppelin:      LocationData(0xC640A4, 0x90FBC0, RName.cc_upper),
    LName.ccia_inventions_round:         LocationData(0xC640A5, 0x90FBA7, RName.cc_upper, "inv"),
    LName.ccia_nitrohall_flamethrower:   LocationData(0xC640A6, 0x90FCDA, RName.cc_upper, "inv"),
    LName.ccia_nitrohall_torch:          LocationData(0xC640A7, 0x10CCD7, RName.cc_upper),
    LName.ccia_nitro_shelf_i:            LocationData(0xC640A8, 0xBFCBF7, RName.cc_upper),
    LName.ccb_mandrag_shelf_l:           LocationData(0xC640A9, 0xBFCBAB, RName.cc_torture_chamber),
    LName.ccb_mandrag_shelf_r:           LocationData(0xC640AA, 0xBFCBA7, RName.cc_torture_chamber),
    LName.ccb_torture_rack:              LocationData(0xC640AB, 0x8985E5, RName.cc_torture_chamber, "inv"),
    LName.ccb_torture_rafters:           LocationData(0xC640AC, 0x8985D6, RName.cc_torture_chamber),
    LName.ccll_cwhall_wall:              LocationData(0xC640AD, 0x10CCB7, RName.cc_library),
    LName.ccl_bookcase:                  LocationData(0xC640AE, 0x8F1197, RName.cc_library),
    # Duel Tower locations
    LName.dt_ibridge_l:      LocationData(0xC640AF, 0x10CE8B, RName.dt_main),
    LName.dt_ibridge_r:      LocationData(0xC640B0, 0x10CE93, RName.dt_main),
    LName.dt_stones_start:   LocationData(0xC640B1, 0x10CE73, RName.dt_main),
    LName.dt_werebull_arena: LocationData(0xC640B2, 0x10CE7B, RName.dt_main),
    # Tower Of Execution locations
    LName.toe_midsavespikes_r:   LocationData(0xC640B3, 0x10CD1F, RName.toe_main),
    LName.toe_midsavespikes_l:   LocationData(0xC640B4, 0x10CD27, RName.toe_main),
    LName.toe_elec_grate:        LocationData(0xC640B5, 0x10CD17, RName.toe_main),
    LName.toe_ibridge:           LocationData(0xC640B6, 0x10CD47, RName.toe_main),
    LName.toe_top:               LocationData(0xC640B7, 0x10CD4F, RName.toe_main),
    LName.toe_keygate_l:         LocationData(0xC640B8, 0x10CD37, RName.toe_ledge),
    # Tower Of Science locations
    LName.tosci_elevator:        LocationData(0xC640B9, 0x10CE0B, RName.tosci_start),
    LName.tosci_plain_sr:        LocationData(0xC640BA, 0x10CDF3, RName.tosci_start),
    LName.tosci_stairs_sr:       LocationData(0xC640BB, 0x10CE13, RName.tosci_start),
    LName.tosci_three_door_hall: LocationData(0xC640BC, 0x10CDFB, RName.tosci_three_doors),
    LName.tosci_ibridge_t:       LocationData(0xC640BD, 0x10CE3B, RName.tosci_conveyors),
    LName.tosci_conveyor_sr:     LocationData(0xC640BE, 0x10CE33, RName.tosci_conveyors),
    LName.tosci_exit:            LocationData(0xC640BF, 0x10CE03, RName.tosci_conveyors),
    LName.tosci_key3_r:          LocationData(0xC640C0, 0x10CE1B, RName.tosci_key3),
    LName.tosci_key3_l:          LocationData(0xC640C1, 0x10CE23, RName.tosci_key3),
    # Tower Of Sorcery locations
    LName.tosor_stained_tower:   LocationData(0xC640C2, 0x10CDB3, RName.tosor_main),
    LName.tosor_savepoint:       LocationData(0xC640C3, 0x10CDBB, RName.tosor_main),
    LName.tosor_trickshot:       LocationData(0xC640C4, 0x10CDD3, RName.tosor_main),
    LName.tosor_yellow_bubble:   LocationData(0xC640C5, 0x10CDDB, RName.tosor_main),
    LName.tosor_blue_platforms:  LocationData(0xC640C6, 0x10CDC3, RName.tosor_main),
    LName.tosor_side_isle:       LocationData(0xC640C7, 0x10CDCB, RName.tosor_main),
    LName.tosor_ibridge:         LocationData(0xC640C8, 0x10CDE3, RName.tosor_main),
    # Room Of Clocks locations
    LName.roc_ent_l:   LocationData(0xC640C9, 0x10CF7B, RName.roc_main),
    LName.roc_cont_r:  LocationData(0xC640CA, 0x10CFB3, RName.roc_main),
    LName.roc_ent_r:   LocationData(0xC640CB, 0x10CFBB, RName.roc_main),
    # Clock Tower locations
    LName.ct_gearclimb_side:     LocationData(0xC640CC, 0x10CEB3, RName.ct_start),
    LName.ct_gearclimb_mid:      LocationData(0xC640CD, 0x10CEC3, RName.ct_start),
    LName.ct_bp_chasm_fl:        LocationData(0xC640CE, 0x99BC4D, RName.ct_middle),
    LName.ct_bp_chasm_fr:        LocationData(0xC640CF, 0x99BC3E, RName.ct_middle),
    LName.ct_bp_chasm_k:         LocationData(0xC640D0, 0x99BC30, RName.ct_middle),
    LName.ct_finalroom_platform: LocationData(0xC640D1, 0x10CEBB, RName.ct_end),
    # Castle Keep locations
    LName.ck_flame_l:     LocationData(0xC640D2, 0x9778C8, RName.ck_main, "inv"),
    LName.ck_flame_r:     LocationData(0xC640D3, 0xBFCA5F, RName.ck_main, "inv"),
    LName.ck_behind_drac: LocationData(0xC640D4, 0x10CE9B, RName.ck_main),
    LName.ck_cube:        LocationData(0xC640D5, 0x10CEA3, RName.ck_main)
}

carrie_only_location_table = {
    LName.uw_carrie1: LocationData(0xC640D6, 0x10CB0B, RName.uw_main),
    LName.uw_carrie2: LocationData(0xC640D7, 0x10CB13, RName.uw_main)
}

cc_lizard_generator_table = {
    LName.ccff_lizard_coffin_nfr: LocationData(0xC640D8, 0x8C450A, RName.cc_lower),
    LName.ccff_lizard_coffin_nmr: LocationData(0xC640D9, 0xBFC9BB, RName.cc_lower),
    LName.ccff_lizard_coffin_nml: LocationData(0xC640DA, 0xBFC9BF, RName.cc_lower),
    LName.ccff_lizard_coffin_nfl: LocationData(0xC640DB, 0xBFC9FF, RName.cc_lower),
    LName.ccff_lizard_coffin_fl:  LocationData(0xC640DC, 0xBFC9FB, RName.cc_lower),
    LName.ccff_lizard_coffin_fr:  LocationData(0xC640DD, 0x8C44F5, RName.cc_lower)
}

multi_breakable_table = {
    # Forest of Silence 3HBs
    LName.forest_dirge_rock1:  LocationData(0xC640DE, 0x10C791, RName.forest_start),
    LName.forest_dirge_rock2:  LocationData(0xC640DF, 0x10C793, RName.forest_start),
    LName.forest_dirge_rock3:  LocationData(0xC640E0, 0x10C795, RName.forest_start),
    LName.forest_dirge_rock4:  LocationData(0xC640E1, 0x10C797, RName.forest_start),
    LName.forest_dirge_rock5:  LocationData(0xC640E2, 0x10C799, RName.forest_start),
    LName.forest_bridge_rock1: LocationData(0xC640E3, 0x10C79D, RName.forest_mid),
    LName.forest_bridge_rock2: LocationData(0xC640E4, 0x10C79F, RName.forest_mid),
    LName.forest_bridge_rock3: LocationData(0xC640E5, 0x10C7A1, RName.forest_mid),
    LName.forest_bridge_rock4: LocationData(0xC640E6, 0x10C7A3, RName.forest_mid),
    # Castle Wall 3HBs
    LName.cw_save_slab1: LocationData(0xC640E7, 0x10C84D, RName.cw_start),
    LName.cw_save_slab2: LocationData(0xC640E8, 0x10C84F, RName.cw_start),
    LName.cw_save_slab3: LocationData(0xC640E9, 0x10C851, RName.cw_start),
    LName.cw_save_slab4: LocationData(0xC640EA, 0x10C853, RName.cw_start),
    LName.cw_save_slab5: LocationData(0xC640EB, 0x10C855, RName.cw_start),
    LName.cw_drac_slab1: LocationData(0xC640EC, 0x10C859, RName.cw_ltower),
    LName.cw_drac_slab2: LocationData(0xC640ED, 0x10C85B, RName.cw_ltower),
    LName.cw_drac_slab3: LocationData(0xC640EE, 0x10C85D, RName.cw_ltower),
    LName.cw_drac_slab4: LocationData(0xC640EF, 0x10C85F, RName.cw_ltower),
    LName.cw_drac_slab5: LocationData(0xC640F0, 0x10C861, RName.cw_ltower),
    # Villa 3HBs
    LName.villafo_chandelier1: LocationData(0xC640F1, 0x10C8F5, RName.villa_main),
    LName.villafo_chandelier2: LocationData(0xC640F2, 0x10C8F7, RName.villa_main),
    LName.villafo_chandelier3: LocationData(0xC640F3, 0x10C8F9, RName.villa_main),
    LName.villafo_chandelier4: LocationData(0xC640F4, 0x10C8FB, RName.villa_main),
    LName.villafo_chandelier5: LocationData(0xC640F5, 0x10C8FD, RName.villa_main),
    # Tunnel 3HBs
    LName.tunnel_arrows_rock1:      LocationData(0xC640F6, 0x10CABD, RName.tunnel_start),
    LName.tunnel_arrows_rock2:      LocationData(0xC640F7, 0x10CABF, RName.tunnel_start),
    LName.tunnel_arrows_rock3:      LocationData(0xC640F8, 0x10CAC1, RName.tunnel_start),
    LName.tunnel_arrows_rock4:      LocationData(0xC640F9, 0x10CAC3, RName.tunnel_start),
    LName.tunnel_arrows_rock5:      LocationData(0xC640FA, 0x10CAC5, RName.tunnel_start),
    LName.tunnel_bucket_quag_rock1: LocationData(0xC640FB, 0x10CAC9, RName.tunnel_start),
    LName.tunnel_bucket_quag_rock2: LocationData(0xC640FC, 0x10CACB, RName.tunnel_start),
    LName.tunnel_bucket_quag_rock3: LocationData(0xC640FD, 0x10CACD, RName.tunnel_start),
    # Underground Waterway 3HBs
    LName.uw_first_ledge1:   LocationData(0xC640FE, 0x10CB39, RName.uw_main),
    LName.uw_first_ledge2:   LocationData(0xC640FF, 0x10CB3B, RName.uw_main),
    LName.uw_first_ledge3:   LocationData(0xC64100, 0x10CB3D, RName.uw_main),
    LName.uw_first_ledge4:   LocationData(0xC64101, 0x10CB3F, RName.uw_main),
    LName.uw_first_ledge5:   LocationData(0xC64102, 0x10CB41, RName.uw_main),
    LName.uw_first_ledge6:   LocationData(0xC64103, 0x10CB43, RName.uw_main),
    LName.uw_in_skel_ledge1: LocationData(0xC64104, 0x10CB45, RName.uw_main),
    LName.uw_in_skel_ledge2: LocationData(0xC64105, 0x10CB47, RName.uw_main),
    LName.uw_in_skel_ledge3: LocationData(0xC64106, 0x10CB49, RName.uw_main),
    # Castle Center 3HBs
    LName.ccb_behemoth_crate1: LocationData(0xC64107, 0x10CBDD, RName.cc_lower),
    LName.ccb_behemoth_crate2: LocationData(0xC64108, 0x10CBDF, RName.cc_lower),
    LName.ccb_behemoth_crate3: LocationData(0xC64109, 0x10CBE1, RName.cc_lower),
    LName.ccb_behemoth_crate4: LocationData(0xC6410A, 0x10CBE3, RName.cc_lower),
    LName.ccb_behemoth_crate5: LocationData(0xC6410B, 0x10CBE5, RName.cc_lower),
    LName.ccelv_stand1:        LocationData(0xC6410C, 0x10CC1D, RName.cc_lower),
    LName.ccelv_stand2:        LocationData(0xC6410D, 0x10CC1F, RName.cc_lower),
    LName.ccelv_stand3:        LocationData(0xC6410E, 0x10CC21, RName.cc_lower),
    LName.ccff_lizard_slab1:   LocationData(0xC6410F, 0x10CC61, RName.cc_lower),
    LName.ccff_lizard_slab2:   LocationData(0xC64110, 0x10CC63, RName.cc_lower),
    LName.ccff_lizard_slab3:   LocationData(0xC64111, 0x10CC65, RName.cc_lower),
    LName.ccff_lizard_slab4:   LocationData(0xC64112, 0x10CC67, RName.cc_lower),
    # Tower of Execution 3HBs
    LName.toe_ledge1: LocationData(0xC64113, 0x10CD5D, RName.toe_main),
    LName.toe_ledge2: LocationData(0xC64114, 0x10CD5F, RName.toe_main),
    LName.toe_ledge3: LocationData(0xC64115, 0x10CD61, RName.toe_main),
    LName.toe_ledge4: LocationData(0xC64116, 0x10CD63, RName.toe_main),
    # Tower of Science 3HBs
    LName.tosci_ibridge_b1: LocationData(0xC64118, 0x10CE59, RName.tosci_conveyors),
    LName.tosci_ibridge_b2: LocationData(0xC64119, 0x10CE5B, RName.tosci_conveyors),
    LName.tosci_ibridge_b3: LocationData(0xC6411A, 0x10CE5D, RName.tosci_conveyors),
    LName.tosci_ibridge_b4: LocationData(0xC6411B, 0x10CE5F, RName.tosci_conveyors),
    LName.tosci_ibridge_b5: LocationData(0xC6411C, 0x10CE61, RName.tosci_conveyors),
    LName.tosci_ibridge_b6: LocationData(0xC6411D, 0x10CE63, RName.tosci_conveyors),
    # Clock Tower 3HBs
    LName.ct_gearclimb_battery_slab1: LocationData(0xC6411E, 0x10CEF9, RName.ct_start),
    LName.ct_gearclimb_battery_slab2: LocationData(0xC6411F, 0x10CEFB, RName.ct_start),
    LName.ct_gearclimb_battery_slab3: LocationData(0xC64120, 0x10CEFD, RName.ct_start),
    LName.ct_gearclimb_door_slab1:    LocationData(0xC64121, 0x10CF01, RName.ct_start),
    LName.ct_gearclimb_door_slab2:    LocationData(0xC64122, 0x10CF03, RName.ct_start),
    LName.ct_gearclimb_door_slab3:    LocationData(0xC64123, 0x10CF05, RName.ct_start),
    LName.ct_finalroom_door_slab1:    LocationData(0xC64124, 0x10CEF5, RName.ct_end),
    LName.ct_finalroom_door_slab2:    LocationData(0xC64125, 0x10CEF7, RName.ct_end),
    LName.ct_finalroom_renon_slab1:   LocationData(0xC64126, 0x10CF09, RName.ct_end),
    LName.ct_finalroom_renon_slab2:   LocationData(0xC64127, 0x10CF0B, RName.ct_end),
    LName.ct_finalroom_renon_slab3:   LocationData(0xC64128, 0x10CF0D, RName.ct_end),
    LName.ct_finalroom_renon_slab4:   LocationData(0xC64129, 0x10CF0F, RName.ct_end),
    LName.ct_finalroom_renon_slab5:   LocationData(0xC6412A, 0x10CF11, RName.ct_end),
    LName.ct_finalroom_renon_slab6:   LocationData(0xC6412B, 0x10CF13, RName.ct_end),
    LName.ct_finalroom_renon_slab7:   LocationData(0xC6412C, 0x10CF15, RName.ct_end),
    LName.ct_finalroom_renon_slab8:   LocationData(0xC6412D, 0x10CF17, RName.ct_end),
}

multi_sub_weapon_table = {
    LName.toe_ledge5: LocationData(0xC64117, 0x10CD65, RName.toe_main),
}

sub_weapon_table = {
    # Forest of Silence sub-weapons
    LName.forest_pillars_left:    LocationData(0xC6412E, 0x10C6EB, RName.forest_start),
    LName.forest_dirge_ped:       LocationData(0xC6412F, 0x10C6FB, RName.forest_start),
    LName.forest_dbridge_gate_l:  LocationData(0xC64130, 0x10C6F3, RName.forest_mid),
    LName.forest_werewolf_island: LocationData(0xC64131, 0x10C703, RName.forest_mid),
    # Castle Wall sub-weapons
    LName.cw_pillar:       LocationData(0xC64132, 0x7F9A0F, RName.cw_start),
    LName.cw_shelf_torch:  LocationData(0xC64133, 0x10C82F, RName.cw_start),
    LName.cw_ground_left:  LocationData(0xC64134, 0x10C827, RName.cw_exit),
    LName.cw_ground_right: LocationData(0xC64135, 0x10C81F, RName.cw_exit),
    # Villa sub-weapons
    LName.villala_hallway_l:          LocationData(0xC64136, 0xBFC903, RName.villa_main),
    LName.villala_hallway_r:          LocationData(0xC64137, 0x83A5F1, RName.villa_main),
    LName.villala_slivingroom_mirror: LocationData(0xC64138, 0x83A5D9, RName.villa_main),
    LName.villala_archives_entrance:  LocationData(0xC64139, 0x83A5E5, RName.villa_archives),
    LName.villam_frankieturf_r:       LocationData(0xC6413A, 0x10C98F, RName.villa_maze),
    LName.villam_fplatform:           LocationData(0xC6413B, 0x10C987, RName.villa_maze),
    LName.villam_rplatform:           LocationData(0xC6413C, 0x10C997, RName.villa_maze),
    LName.villac_coffin_l:            LocationData(0xC6413D, 0x10CF73, RName.villa_crypt),
    # Tunnel sub-weapons
    LName.tunnel_stone_alcove_r:        LocationData(0xC6413E, 0x10CA57, RName.tunnel_start),
    LName.tunnel_lbucket_mdoor_l:       LocationData(0xC6413F, 0x10CA67, RName.tunnel_start),
    LName.tunnel_gondola_rc_sdoor_l:    LocationData(0xC64140, 0x10CA5F, RName.tunnel_start),
    LName.tunnel_corpse_bucket_mdoor_l: LocationData(0xC64141, 0x10CA6F, RName.tunnel_end),
    LName.tunnel_shovel_mdoor_r:        LocationData(0xC64142, 0x10CA77, RName.tunnel_end),
    LName.tunnel_shovel_sdoor_r:        LocationData(0xC64143, 0x10CA7F, RName.tunnel_end),
    # Castle Center sub-weapons
    LName.ccb_skel_hallway_ba:     LocationData(0xC64144, 0x10CBC7, RName.cc_lower),
    LName.ccelv_switch:            LocationData(0xC64145, 0x10CC0F, RName.cc_lower),
    LName.ccff_lizard_near_knight: LocationData(0xC64146, 0x10CC5B, RName.cc_lower),
    # Duel Tower sub-weapon
    LName.dt_stones_end: LocationData(0xC64147, 0x10CE83, RName.dt_main),
    # Tower of Execution sub-weapon
    LName.toe_keygate_r: LocationData(0xC64148, 0x10CD3F, RName.toe_ledge),
    # Tower of Science sub-weapon
    LName.tosci_key3_m:  LocationData(0xC64149, 0x10CE2B, RName.tosci_key3),
    # Room of Clocks sub-weapons
    LName.roc_elev_l: LocationData(0xC6414A, 0x10CF8B, RName.roc_main),
    LName.roc_elev_r: LocationData(0xC6414B, 0x10CF93, RName.roc_main),
    # Clock Tower sub-weapons
    LName.ct_bp_chasm_rl:  LocationData(0xC6414C, 0x99BC5A, RName.ct_middle),
    LName.ct_finalroom_fl: LocationData(0xC6414D, 0x10CED3, RName.ct_end),
    LName.ct_finalroom_fr: LocationData(0xC6414E, 0x10CECB, RName.ct_end),
    LName.ct_finalroom_rl: LocationData(0xC6414F, 0x10CEE3, RName.ct_end),
    LName.ct_finalroom_rr: LocationData(0xC64150, 0x10CEDB, RName.ct_end),
}

empty_breakables_table = {
    LName.forest_dirge_tomb_l:     LocationData(0xC64151, 0x10C74B, RName.forest_start),
    LName.forest_dbridge_tomb_l:   LocationData(0xC64152, 0x10C763, RName.forest_mid),
    LName.forest_dbridge_tomb_ur:  LocationData(0xC64153, 0x10C773, RName.forest_mid),
    LName.forest_bface_tomb_lr:    LocationData(0xC64154, 0x10C753, RName.forest_mid),
    LName.forest_werewolf_tomb_lf: LocationData(0xC64155, 0x10C783, RName.forest_mid),
    LName.forest_werewolf_tomb_lr: LocationData(0xC64156, 0x10C73B, RName.forest_mid),

    LName.villafo_mid_r: LocationData(0xC64157, 0x10C8CF, RName.villa_main),

    LName.roc_cont_l: LocationData(0xC64158, 0x10CFA3, RName.roc_main),
    LName.roc_exit:   LocationData(0xC64159, 0x10CF9B, RName.roc_main),
}

renon_shop_table = {
    LName.renon1: LocationData(0xC6415A, 0xBFD8E5, RName.renon, "shop"),
    LName.renon2: LocationData(0xC6415B, 0xBFD8E7, RName.renon, "shop"),
    LName.renon3: LocationData(0xC6415C, 0xBFD8E9, RName.renon, "shop"),
    LName.renon4: LocationData(0xC6415D, 0xBFD8EB, RName.renon, "shop"),
    LName.renon5: LocationData(0xC6415E, 0xBFD8ED, RName.renon, "shop"),
    LName.renon6: LocationData(0xC6415F, 0xBFD907, RName.renon, "shop"),
    LName.renon7: LocationData(0xC64160, 0xBFD909, RName.renon, "shop"),
}

boss_table = {
    LName.forest_boss_one:       LocationData(None, 0x000000, RName.forest_start, "event"),
    LName.forest_boss_two:       LocationData(None, 0x000000, RName.forest_start, "event"),
    LName.forest_boss_three:     LocationData(None, 0x000000, RName.forest_end, "event"),
    LName.cw_boss:               LocationData(None, 0x000000, RName.cw_start, "event"),
    LName.villa_boss_one:        LocationData(None, 0x000000, RName.villa_crypt, "event"),
    LName.villa_boss_two:        LocationData(None, 0x000000, RName.villa_crypt, "event"),
    LName.uw_boss:               LocationData(None, 0x000000, RName.uw_main, "event"),
    LName.cc_boss_one:           LocationData(None, 0x000000, RName.cc_crystal, "event"),
    LName.cc_boss_two:           LocationData(None, 0x000000, RName.cc_crystal, "event"),
    LName.dt_boss_one:           LocationData(None, 0x000000, RName.dt_main, "event"),
    LName.dt_boss_two:           LocationData(None, 0x000000, RName.dt_main, "event"),
    LName.dt_boss_three:         LocationData(None, 0x000000, RName.dt_main, "event"),
    LName.dt_boss_four:          LocationData(None, 0x000000, RName.dt_main, "event"),
    LName.roc_boss:              LocationData(None, 0x000000, RName.roc_main, "event"),
    LName.ck_boss_one:           LocationData(None, 0x000000, RName.ck_main, "event"),
    LName.ck_boss_two:           LocationData(None, 0x000000, RName.ck_main, "event"),
}

crystal_table = {
    LName.cc_behind_the_seal:    LocationData(None, 0x000000, RName.ck_main, "event"),
}

end_table = {
    LName.the_end:               LocationData(None, 0x000000, RName.ck_drac_chamber, "event"),
}

all_locations = {
    **main_location_table,
    **carrie_only_location_table,
    **cc_lizard_generator_table,
    **multi_breakable_table,
    **multi_sub_weapon_table,
    **sub_weapon_table,
    **empty_breakables_table,
    **renon_shop_table
}

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}


def create_locations(world, player: int, active_regions):
    location_table = {**main_location_table,
                      **end_table}

    if world.draculas_condition[player].value == 1:
        location_table.update({**crystal_table})
    elif world.draculas_condition[player].value == 2:
        location_table.update({**boss_table})
        # Delete Vincent and/or Renon from the active locations if disabled completely.
        if world.vincent_fight_condition[player].value == 0:
            del location_table[LName.ck_boss_two]
        if world.renon_fight_condition[player].value == 0:
            del location_table[LName.ck_boss_one]

    if world.carrie_logic[player].value:
        location_table.update({**carrie_only_location_table})

    if world.lizard_generator_items[player].value:
        location_table.update({**cc_lizard_generator_table})

    if world.multi_hit_breakables[player].value:
        location_table.update({**multi_breakable_table})

    if world.sub_weapon_shuffle[player].value > 1 and world.multi_hit_breakables[player].value:
        location_table.update({**multi_sub_weapon_table})

    if world.empty_breakables[player].value:
        location_table.update({**empty_breakables_table})

    if world.sub_weapon_shuffle[player].value > 1:
        location_table.update({**sub_weapon_table})

    if world.shopsanity[player].value:
        location_table.update({**renon_shop_table})

    for loc, data in location_table.items():
        if data.region in active_regions:
            stage = RName.regions_to_stages[data.region]
            created_location = CV64Location(player, loc, data.code, active_regions[data.region],
                                            data.cv64_rom_offset, data.cv64_loc_type, stage)
            active_regions[data.region].locations.append(created_location)
