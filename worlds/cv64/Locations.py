import typing

from BaseClasses import Location
from .Names import LocationName, RegionName


class CV64Location(Location):
    game: str = "Castlevania 64"

    cv64_rom_offset: int
    cv64_loc_type: str

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, cv64_rom_offset: int = None,
                 cv64_loc_type: str = None):
        super().__init__(player, name, address, parent)
        self.cv64_rom_offset = cv64_rom_offset
        self.cv64_loc_type = cv64_loc_type


class LocationData(typing.NamedTuple):
    code: typing.Optional[int]
    cv64_rom_offset: int
    region: str
    cv64_loc_type: str = "normal"


main_location_table = {
    # Forest of Silence locations
    LocationName.forest_pillars_right:   LocationData(0xC64001, 0x10C67B, RegionName.forest_start),
    LocationName.forest_pillars_top:     LocationData(0xC64002, 0x10C71B, RegionName.forest_start),
    LocationName.forest_bone_mom:        LocationData(0xC64003, 0x10C6BB, RegionName.forest_start),
    LocationName.forest_lgaz_in:         LocationData(0xC64004, 0x10C68B, RegionName.forest_start),
    LocationName.forest_lgaz_top:        LocationData(0xC64005, 0x10C693, RegionName.forest_start),
    LocationName.forest_hgaz_in:         LocationData(0xC64006, 0x10C6C3, RegionName.forest_start),
    LocationName.forest_hgaz_top:        LocationData(0xC64007, 0x10C6E3, RegionName.forest_start),
    LocationName.forest_weretiger_sw:    LocationData(0xC64008, 0x10C6CB, RegionName.forest_start),
    LocationName.forest_weretiger_gate:  LocationData(0xC64009, 0x10C683, RegionName.forest_start),
    LocationName.forest_dirge_plaque:    LocationData(0xC6400A, 0x7C7F9D, RegionName.forest_start, "inv"),
    LocationName.forest_dirge_tomb:      LocationData(0xC6400B, 0x10C743, RegionName.forest_start),
    LocationName.forest_corpse_save:     LocationData(0xC6400C, 0x10C6A3, RegionName.forest_start),
    LocationName.forest_dbridge_wall:    LocationData(0xC6400D, 0x10C69B, RegionName.forest_start),
    LocationName.forest_dbridge_sw:      LocationData(0xC6400E, 0x10C6D3, RegionName.forest_start),
    LocationName.forest_dbridge_gate_r:  LocationData(0xC6400F, 0x10C6AB, RegionName.forest_mid),
    LocationName.forest_dbridge_tomb:    LocationData(0xC64010, 0x10C76B, RegionName.forest_mid),
    LocationName.forest_bface_tomb_l:    LocationData(0xC64011, 0x10C75B, RegionName.forest_mid),
    LocationName.forest_bface_tomb_u:    LocationData(0xC64012, 0x10C77B, RegionName.forest_mid),
    LocationName.forest_ibridge:         LocationData(0xC64013, 0x10C713, RegionName.forest_mid),
    LocationName.forest_werewolf_tomb:   LocationData(0xC64014, 0x10C733, RegionName.forest_mid),
    LocationName.forest_werewolf_plaque: LocationData(0xC64015, 0xBFC937, RegionName.forest_mid, "inv"),
    LocationName.forest_werewolf_tree:   LocationData(0xC64016, 0x10C6B3, RegionName.forest_mid),
    LocationName.forest_final_sw:        LocationData(0xC64017, 0x10C72B, RegionName.forest_mid),
    # Castle Wall locations
    LocationName.cwr_bottom:        LocationData(0xC64018, 0x10C7E7, RegionName.cw_start),
    LocationName.cw_dragon_sw:      LocationData(0xC64019, 0x10C817, RegionName.cw_start),
    LocationName.cw_rrampart:       LocationData(0xC6401A, 0x10C7FF, RegionName.cw_start),
    LocationName.cw_lrampart:       LocationData(0xC6401B, 0x10C807, RegionName.cw_start),
    LocationName.cw_shelf_visible:  LocationData(0xC6401C, 0x7F99A9, RegionName.cw_start),
    LocationName.cw_shelf_sandbags: LocationData(0xC6401D, 0x7F9A3E, RegionName.cw_start, "inv"),
    LocationName.cw_ground_middle:  LocationData(0xC6401E, 0x10C7F7, RegionName.cw_start),
    LocationName.cwl_bottom:        LocationData(0xC6401F, 0x10C7DF, RegionName.cw_ltower),
    LocationName.cwl_bridge:        LocationData(0xC64020, 0x10C7EF, RegionName.cw_ltower),
    LocationName.cw_drac_sw:        LocationData(0xC64021, 0x10C80F, RegionName.cw_ltower),
    # Villa locations
    LocationName.villafy_outer_gate_l:          LocationData(0xC64022, 0x10C87F, RegionName.villa_start),
    LocationName.villafy_outer_gate_r:          LocationData(0xC64023, 0x10C887, RegionName.villa_start),
    LocationName.villafy_dog_platform:          LocationData(0xC64024, 0x10C89F, RegionName.villa_start),
    LocationName.villafy_inner_gate:            LocationData(0xC64025, 0xBFC95F, RegionName.villa_start),
    LocationName.villafy_gate_marker:           LocationData(0xC64026, 0x10C8A7, RegionName.villa_main),
    LocationName.villafy_villa_marker:          LocationData(0xC64027, 0x10C897, RegionName.villa_main),
    LocationName.villafy_tombstone:             LocationData(0xC64028, 0x8099CC, RegionName.villa_main, "inv"),
    LocationName.villafy_fountain_fl:           LocationData(0xC64029, 0xBFC957, RegionName.villa_main),
    LocationName.villafy_fountain_fr:           LocationData(0xC6402A, 0x80997D, RegionName.villa_main),
    LocationName.villafy_fountain_ml:           LocationData(0xC6402B, 0x809956, RegionName.villa_main),
    LocationName.villafy_fountain_mr:           LocationData(0xC6402C, 0x80992D, RegionName.villa_main),
    LocationName.villafy_fountain_rl:           LocationData(0xC6402D, 0xBFC95B, RegionName.villa_main),
    LocationName.villafy_fountain_rr:           LocationData(0xC6402E, 0x80993C, RegionName.villa_main),
    LocationName.villafo_front_r:               LocationData(0xC6402F, 0x10C8E7, RegionName.villa_main),
    LocationName.villafo_front_l:               LocationData(0xC64030, 0x10C8DF, RegionName.villa_main),
    LocationName.villafo_mid_l:                 LocationData(0xC64031, 0x10C8D7, RegionName.villa_main),
    LocationName.villafo_rear_r:                LocationData(0xC64032, 0x10C8C7, RegionName.villa_main),
    LocationName.villafo_rear_l:                LocationData(0xC64033, 0x10C8BF, RegionName.villa_main),
    LocationName.villafo_pot_r:                 LocationData(0xC64034, 0x10C8AF, RegionName.villa_main),
    LocationName.villafo_pot_l:                 LocationData(0xC64035, 0x10C8B7, RegionName.villa_main),
    LocationName.villala_hallway_stairs:        LocationData(0xC64036, 0x10C927, RegionName.villa_main),
    LocationName.villala_bedroom_chairs:        LocationData(0xC64037, 0x83A588, RegionName.villa_main),
    LocationName.villala_bedroom_bed:           LocationData(0xC64038, 0x83A593, RegionName.villa_main),
    LocationName.villala_vincent:               LocationData(0xC64039, 0xBFC203, RegionName.villa_main, "npc"),
    LocationName.villala_slivingroom_table:     LocationData(0xC6403A, 0x83A635, RegionName.villa_main, "inv"),
    LocationName.villala_diningroom_roses:      LocationData(0xC6403B, 0xBFC98B, RegionName.villa_main, "inv"),
    LocationName.villala_llivingroom_pot_r:     LocationData(0xC6403C, 0x10C90F, RegionName.villa_main),
    LocationName.villala_llivingroom_pot_l:     LocationData(0xC6403D, 0x10C917, RegionName.villa_main),
    LocationName.villala_llivingroom_painting:  LocationData(0xC6403E, 0xBFC987, RegionName.villa_main, "inv"),
    LocationName.villala_llivingroom_light:     LocationData(0xC6403F, 0x10C91F, RegionName.villa_main),
    LocationName.villala_llivingroom_lion:      LocationData(0xC64040, 0x83A610, RegionName.villa_main, "inv"),
    LocationName.villala_exit_knight:           LocationData(0xC64041, 0x83A61B, RegionName.villa_main),
    LocationName.villala_storeroom_l:           LocationData(0xC64042, 0x83A5CA, RegionName.villa_storeroom),
    LocationName.villala_storeroom_r:           LocationData(0xC64043, 0xBFC97F, RegionName.villa_storeroom),
    LocationName.villala_storeroom_s:           LocationData(0xC64044, 0x83A604, RegionName.villa_storeroom, "inv"),
    LocationName.villala_archives_table:        LocationData(0xC64045, 0xBFC98F, RegionName.villa_archives, "inv"),
    LocationName.villala_archives_rear:         LocationData(0xC64046, 0x83A5B1, RegionName.villa_archives),
    LocationName.villam_malus_torch:            LocationData(0xC64047, 0x10C967, RegionName.villa_maze),
    LocationName.villam_malus_bush:             LocationData(0xC64048, 0x850FEC, RegionName.villa_maze, "inv"),
    LocationName.villam_frankieturf_l:          LocationData(0xC64049, 0x10C947, RegionName.villa_maze),
    LocationName.villam_frankieturf_ru:         LocationData(0xC6404A, 0x10C9A7, RegionName.villa_maze),
    LocationName.villam_fgarden_f:              LocationData(0xC6404B, 0x10C96F, RegionName.villa_maze),
    LocationName.villam_fgarden_mf:             LocationData(0xC6404C, 0x10C977, RegionName.villa_maze),
    LocationName.villam_fgarden_mr:             LocationData(0xC6404D, 0x10C95F, RegionName.villa_maze),
    LocationName.villam_fgarden_r:              LocationData(0xC6404E, 0x10C97F, RegionName.villa_maze),
    LocationName.villam_rplatform_de:           LocationData(0xC6404F, 0x10C94F, RegionName.villa_maze),
    LocationName.villam_exit_de:                LocationData(0xC64050, 0x10C957, RegionName.villa_maze),
    LocationName.villam_serv_path:              LocationData(0xC64051, 0x10C92F, RegionName.villa_maze),
    LocationName.villafo_serv_ent:              LocationData(0xC64052, 0x10C8EF, RegionName.villa_servants),
    LocationName.villam_crypt_ent:              LocationData(0xC64053, 0x10C93F, RegionName.villa_crypt),
    LocationName.villam_crypt_upstream:         LocationData(0xC64054, 0x10C937, RegionName.villa_crypt),
    LocationName.villac_ent_l:                  LocationData(0xC64055, 0x10CF4B, RegionName.villa_crypt),
    LocationName.villac_ent_r:                  LocationData(0xC64056, 0x10CF63, RegionName.villa_crypt),
    LocationName.villac_wall_l:                 LocationData(0xC64057, 0x10CF6B, RegionName.villa_crypt),
    LocationName.villac_wall_r:                 LocationData(0xC64058, 0x10CF5B, RegionName.villa_crypt),
    LocationName.villac_coffin_r:               LocationData(0xC64059, 0x10CF53, RegionName.villa_crypt),
    # Tunnel locations
    LocationName.tunnel_landing:                LocationData(0xC6405A, 0x10C9AF, RegionName.tunnel_start),
    LocationName.tunnel_landing_rc:             LocationData(0xC6405B, 0x10C9B7, RegionName.tunnel_start),
    LocationName.tunnel_stone_alcove_l:         LocationData(0xC6405C, 0x10CA9F, RegionName.tunnel_start),
    LocationName.tunnel_twin_arrows:            LocationData(0xC6405D, 0xBFC9B7, RegionName.tunnel_start, "inv"),
    LocationName.tunnel_lonesome_bucket:        LocationData(0xC6405E, 0x86D8E1, RegionName.tunnel_start, "inv"),
    LocationName.tunnel_lbucket_quag:           LocationData(0xC6405F, 0x10C9DF, RegionName.tunnel_start),
    LocationName.tunnel_lbucket_albert:         LocationData(0xC64060, 0x10C9E7, RegionName.tunnel_start),
    LocationName.tunnel_albert_camp:            LocationData(0xC64061, 0x10C9D7, RegionName.tunnel_start),
    LocationName.tunnel_albert_quag:            LocationData(0xC64062, 0x10C9CF, RegionName.tunnel_start),
    LocationName.tunnel_gondola_rc_sdoor_r:     LocationData(0xC64063, 0x10CA27, RegionName.tunnel_start),
    LocationName.tunnel_gondola_rc_sdoor_m:     LocationData(0xC64064, 0x10CAA7, RegionName.tunnel_start),
    LocationName.tunnel_gondola_rc:             LocationData(0xC64065, 0x10CAB7, RegionName.tunnel_start),
    LocationName.tunnel_rgondola_station:       LocationData(0xC64066, 0x10C9C7, RegionName.tunnel_start),
    LocationName.tunnel_gondola_transfer:       LocationData(0xC64067, 0x10CA2F, RegionName.tunnel_start),
    LocationName.tunnel_corpse_bucket_quag:     LocationData(0xC64068, 0x10C9F7, RegionName.tunnel_end),
    LocationName.tunnel_corpse_bucket_mdoor_r:  LocationData(0xC64069, 0x10CA37, RegionName.tunnel_end),
    LocationName.tunnel_shovel_quag_start:      LocationData(0xC6406A, 0x10C9FF, RegionName.tunnel_end),
    LocationName.tunnel_exit_quag_start:        LocationData(0xC6406B, 0x10CA07, RegionName.tunnel_end),
    LocationName.tunnel_shovel_quag_end:        LocationData(0xC6406C, 0x10CA0F, RegionName.tunnel_end),
    LocationName.tunnel_exit_quag_end:          LocationData(0xC6406D, 0x10CA3F, RegionName.tunnel_end),
    LocationName.tunnel_shovel:                 LocationData(0xC6406E, 0x86D8FC, RegionName.tunnel_end, "inv"),
    LocationName.tunnel_shovel_save:            LocationData(0xC6406F, 0x10CA17, RegionName.tunnel_end),
    LocationName.tunnel_shovel_mdoor_l:         LocationData(0xC64070, 0x10CA47, RegionName.tunnel_end),
    LocationName.tunnel_shovel_sdoor_l:         LocationData(0xC64071, 0x10CA4F, RegionName.tunnel_end),
    LocationName.tunnel_shovel_sdoor_m:         LocationData(0xC64072, 0x10CAAF, RegionName.tunnel_end),
    # Underground Waterway locations
    LocationName.uw_near_ent:           LocationData(0xC64073, 0x10CB03, RegionName.uw_main),
    LocationName.uw_across_ent:         LocationData(0xC64074, 0x10CAF3, RegionName.uw_main),
    LocationName.uw_poison_parkour:     LocationData(0xC64075, 0x10CAFB, RegionName.uw_main),
    LocationName.uw_waterfall_alcove:   LocationData(0xC64076, 0x10CB23, RegionName.uw_main),
    LocationName.uw_bricks_save:        LocationData(0xC64077, 0x10CB33, RegionName.uw_main),
    LocationName.uw_above_skel_ledge:   LocationData(0xC64078, 0x10CB2B, RegionName.uw_main),
    # Castle Center locations
    LocationName.ccb_skel_hallway_ent:          LocationData(0xC64079, 0x10CB67, RegionName.cc_main),
    LocationName.ccb_skel_hallway_jun:          LocationData(0xC6407A, 0x10CBD7, RegionName.cc_main),
    LocationName.ccb_skel_hallway_tc:           LocationData(0xC6407B, 0x10CB6F, RegionName.cc_main),
    LocationName.ccb_behemoth_l_ff:             LocationData(0xC6407C, 0x10CB77, RegionName.cc_main),
    LocationName.ccb_behemoth_l_mf:             LocationData(0xC6407D, 0x10CBA7, RegionName.cc_main),
    LocationName.ccb_behemoth_l_mr:             LocationData(0xC6407E, 0x10CB7F, RegionName.cc_main),
    LocationName.ccb_behemoth_l_fr:             LocationData(0xC6407F, 0x10CBAF, RegionName.cc_main),
    LocationName.ccb_behemoth_r_ff:             LocationData(0xC64080, 0x10CBB7, RegionName.cc_main),
    LocationName.ccb_behemoth_r_mf:             LocationData(0xC64081, 0x10CB87, RegionName.cc_main),
    LocationName.ccb_behemoth_r_mr:             LocationData(0xC64082, 0x10CBBF, RegionName.cc_main),
    LocationName.ccb_behemoth_r_fr:             LocationData(0xC64083, 0x10CB8F, RegionName.cc_main),
    LocationName.ccelv_near_machine:            LocationData(0xC64084, 0x10CBF7, RegionName.cc_main),
    LocationName.ccelv_atop_machine:            LocationData(0xC64085, 0x10CC17, RegionName.cc_main),
    LocationName.ccelv_pipes:                   LocationData(0xC64086, 0x10CC07, RegionName.cc_main),
    LocationName.ccelv_staircase:               LocationData(0xC64087, 0x10CBFF, RegionName.cc_main),
    LocationName.ccff_redcarpet_knight:         LocationData(0xC64088, 0x8C44D9, RegionName.cc_main, "inv"),
    LocationName.ccff_gears_side:               LocationData(0xC64089, 0x10CC33, RegionName.cc_main),
    LocationName.ccff_gears_mid:                LocationData(0xC6408A, 0x10CC3B, RegionName.cc_main),
    LocationName.ccff_gears_corner:             LocationData(0xC6408B, 0x10CC43, RegionName.cc_main),
    LocationName.ccff_lizard_knight:            LocationData(0xC6408C, 0x8C44E7, RegionName.cc_main, "inv"),
    LocationName.ccff_lizard_pit:               LocationData(0xC6408D, 0x10CC4B, RegionName.cc_main),
    LocationName.ccff_lizard_corner:            LocationData(0xC6408E, 0x10CC53, RegionName.cc_main),
    LocationName.ccll_brokenstairs_floor:       LocationData(0xC6408F, 0x10CC8F, RegionName.cc_main),
    LocationName.ccll_brokenstairs_knight:      LocationData(0xC64090, 0x8DF782, RegionName.cc_main, "inv"),
    LocationName.ccll_brokenstairs_save:        LocationData(0xC64091, 0x10CC87, RegionName.cc_main),
    LocationName.ccll_glassknight_l:            LocationData(0xC64092, 0x10CC97, RegionName.cc_main),
    LocationName.ccll_glassknight_r:            LocationData(0xC64093, 0x10CC77, RegionName.cc_main),
    LocationName.ccll_butlers_door:             LocationData(0xC64094, 0x10CC7F, RegionName.cc_main),
    LocationName.ccll_butlers_side:             LocationData(0xC64095, 0x10CC9F, RegionName.cc_main),
    LocationName.ccll_cwhall_butlerflames_past: LocationData(0xC64096, 0x10CCA7, RegionName.cc_main),
    LocationName.ccll_cwhall_flamethrower:      LocationData(0xC64097, 0x8DF580, RegionName.cc_main, "inv"),
    LocationName.ccll_cwhall_cwflames:          LocationData(0xC64098, 0x10CCAF, RegionName.cc_main),
    LocationName.ccll_heinrich:                 LocationData(0xC64099, 0xBFC20F, RegionName.cc_main, "npc"),
    LocationName.ccia_nitro_crates:             LocationData(0xC6409A, 0x90FCE9, RegionName.cc_main, "inv"),
    LocationName.ccia_nitro_shelf:              LocationData(0xC6409B, 0xBFC1C3, RegionName.cc_main, "npc"),
    LocationName.ccia_stairs_knight:            LocationData(0xC6409C, 0x90FE5C, RegionName.cc_main, "inv"),
    LocationName.ccia_maids_vase:               LocationData(0xC6409D, 0x90FF1D, RegionName.cc_main, "inv"),
    LocationName.ccia_maids_outer:              LocationData(0xC6409E, 0x10CCFF, RegionName.cc_main),
    LocationName.ccia_maids_inner:              LocationData(0xC6409F, 0x10CD07, RegionName.cc_main),
    LocationName.ccia_inventions_maids:         LocationData(0xC640A0, 0x10CCE7, RegionName.cc_main),
    LocationName.ccia_inventions_crusher:       LocationData(0xC640A1, 0x10CCDF, RegionName.cc_main),
    LocationName.ccia_inventions_famicart:      LocationData(0xC640A2, 0x90FBB3, RegionName.cc_main, "inv"),
    LocationName.ccia_inventions_zeppelin:      LocationData(0xC640A3, 0x90FBC0, RegionName.cc_main),
    LocationName.ccia_inventions_round:         LocationData(0xC640A4, 0x90FBA7, RegionName.cc_main, "inv"),
    LocationName.ccia_nitrohall_flamethrower:   LocationData(0xC640A5, 0x90FCDA, RegionName.cc_main, "inv"),
    LocationName.ccia_nitrohall_torch:          LocationData(0xC640A6, 0x10CCD7, RegionName.cc_main),
    LocationName.ccb_mandrag_shelf:             LocationData(0xC640A7, 0xBFC1E3, RegionName.cc_torture_chamber, "npc"),
    LocationName.ccb_torture_rack:              LocationData(0xC640A8, 0x8985E5, RegionName.cc_torture_chamber, "inv"),
    LocationName.ccb_torture_rafters:           LocationData(0xC640A9, 0x8985D6, RegionName.cc_torture_chamber),
    LocationName.ccll_cwhall_wall:              LocationData(0xC640AA, 0x10CCB7, RegionName.cc_library),
    LocationName.ccl_bookcase:                  LocationData(0xC640AB, 0x8F1197, RegionName.cc_library),
    # Duel Tower locations
    LocationName.dt_ibridge_l:      LocationData(0xC640AC, 0x10CE8B, RegionName.dt_main),
    LocationName.dt_ibridge_r:      LocationData(0xC640AD, 0x10CE93, RegionName.dt_main),
    LocationName.dt_stones_start:   LocationData(0xC640AE, 0x10CE73, RegionName.dt_main),
    LocationName.dt_werebull_arena: LocationData(0xC640AF, 0x10CE7B, RegionName.dt_main),
    # Tower Of Execution locations
    LocationName.toe_midsavespikes_r:   LocationData(0xC640B0, 0x10CD1F, RegionName.toe_main),
    LocationName.toe_midsavespikes_l:   LocationData(0xC640B1, 0x10CD27, RegionName.toe_main),
    LocationName.toe_elec_grate:        LocationData(0xC640B2, 0x10CD17, RegionName.toe_main),
    LocationName.toe_ibridge:           LocationData(0xC640B3, 0x10CD47, RegionName.toe_main),
    LocationName.toe_top:               LocationData(0xC640B4, 0x10CD4F, RegionName.toe_main),
    LocationName.toe_keygate_l:         LocationData(0xC640B5, 0x10CD37, RegionName.toe_ledge),
    # Tower Of Science locations
    LocationName.tosci_elevator:        LocationData(0xC640B6, 0x10CE0B, RegionName.tosci_start),
    LocationName.tosci_plain_sr:        LocationData(0xC640B7, 0x10CDF3, RegionName.tosci_start),
    LocationName.tosci_stairs_sr:       LocationData(0xC640B8, 0x10CE13, RegionName.tosci_start),
    LocationName.tosci_three_door_hall: LocationData(0xC640B9, 0x10CDFB, RegionName.tosci_three_doors),
    LocationName.tosci_ibridge_t:       LocationData(0xC640BA, 0x10CE3B, RegionName.tosci_conveyors),
    LocationName.tosci_conveyor_sr:     LocationData(0xC640BB, 0x10CE33, RegionName.tosci_conveyors),
    LocationName.tosci_exit:            LocationData(0xC640BC, 0x10CE03, RegionName.tosci_conveyors),
    LocationName.tosci_key3_r:          LocationData(0xC640BD, 0x10CE1B, RegionName.tosci_key3),
    LocationName.tosci_key3_l:          LocationData(0xC640BE, 0x10CE23, RegionName.tosci_key3),
    # Tower Of Sorcery locations
    LocationName.tosor_stained_tower:   LocationData(0xC640BF, 0x10CDB3, RegionName.tosor_main),
    LocationName.tosor_savepoint:       LocationData(0xC640C0, 0x10CDBB, RegionName.tosor_main),
    LocationName.tosor_trickshot:       LocationData(0xC640C1, 0x10CDD3, RegionName.tosor_main),
    LocationName.tosor_yellow_bubble:   LocationData(0xC640C2, 0x10CDDB, RegionName.tosor_main),
    LocationName.tosor_blue_platforms:  LocationData(0xC640C3, 0x10CDC3, RegionName.tosor_main),
    LocationName.tosor_side_isle:       LocationData(0xC640C4, 0x10CDCB, RegionName.tosor_main),
    LocationName.tosor_ibridge:         LocationData(0xC640C5, 0x10CDE3, RegionName.tosor_main),
    # Room Of Clocks locations
    LocationName.roc_ent_l: LocationData(0xC640C6, 0x10CF7B, RegionName.roc_main),
    LocationName.roc_gs_r:  LocationData(0xC640C7, 0x10CFB3, RegionName.roc_main),
    LocationName.roc_ent_r: LocationData(0xC640C8, 0x10CFBB, RegionName.roc_main),
    # Clock Tower locations
    LocationName.ct_gearclimb_side:     LocationData(0xC640C9, 0x10CEB3, RegionName.ct_start),
    LocationName.ct_gearclimb_mid:      LocationData(0xC640CA, 0x10CEC3, RegionName.ct_start),
    LocationName.ct_bp_chasm_fl:        LocationData(0xC640CB, 0x99BC4D, RegionName.ct_middle),
    LocationName.ct_bp_chasm_fr:        LocationData(0xC640CC, 0x99BC3E, RegionName.ct_middle),
    LocationName.ct_bp_chasm_k:         LocationData(0xC640CD, 0x99BC30, RegionName.ct_middle),
    LocationName.ct_finalroom_platform: LocationData(0xC640CE, 0x10CEBB, RegionName.ct_end),
    # Castle Keep locations
    LocationName.ck_flame_l:     LocationData(0xC640CF, 0x9778C8, RegionName.ck_main, "inv"),
    LocationName.ck_flame_r:     LocationData(0xC640D0, 0xBFCA6B, RegionName.ck_main, "inv"),
    LocationName.ck_behind_drac: LocationData(0xC640D1, 0x10CE9B, RegionName.ck_main),
    LocationName.ck_cube:        LocationData(0xC640D2, 0x10CEA3, RegionName.ck_main)
}

carrie_only_location_table = {
    LocationName.uw_carrie1: LocationData(0xC640D3, 0x10CB0B, RegionName.uw_main),
    LocationName.uw_carrie2: LocationData(0xC640D4, 0x10CB13, RegionName.uw_main)
}

cc_lizard_generator_table = {
    LocationName.ccff_lizard_coffin_nfr: LocationData(0xC640D5, 0x8C450A, RegionName.cc_main),
    LocationName.ccff_lizard_coffin_nmr: LocationData(0xC640D6, 0xBFC9D7, RegionName.cc_main),
    LocationName.ccff_lizard_coffin_nml: LocationData(0xC640D7, 0xBFC9DB, RegionName.cc_main),
    LocationName.ccff_lizard_coffin_nfl: LocationData(0xC640D8, 0x8C451C, RegionName.cc_main),
    LocationName.ccff_lizard_coffin_fl:  LocationData(0xC640D9, 0x8C44fD, RegionName.cc_main),
    LocationName.ccff_lizard_coffin_fr:  LocationData(0xC640DA, 0x8C44F5, RegionName.cc_main)
}

boss_table = {
    LocationName.forest_boss_one:       LocationData(None, 0x000000, RegionName.forest_start, "event"),
    LocationName.forest_boss_two:       LocationData(None, 0x000000, RegionName.forest_start, "event"),
    LocationName.forest_boss_three:     LocationData(None, 0x000000, RegionName.forest_end, "event"),
    LocationName.cw_boss:               LocationData(None, 0x000000, RegionName.cw_start, "event"),
    LocationName.villa_boss_one:        LocationData(None, 0x000000, RegionName.villa_crypt, "event"),
    LocationName.villa_boss_two:        LocationData(None, 0x000000, RegionName.villa_crypt, "event"),
    LocationName.uw_boss:               LocationData(None, 0x000000, RegionName.underground_waterway, "event"),
    LocationName.cc_boss_one:           LocationData(None, 0x000000, RegionName.cc_crystal, "event"),
    LocationName.cc_boss_two:           LocationData(None, 0x000000, RegionName.cc_crystal, "event"),
    LocationName.dt_boss_one:           LocationData(None, 0x000000, RegionName.dt_main, "event"),
    LocationName.dt_boss_two:           LocationData(None, 0x000000, RegionName.dt_main, "event"),
    LocationName.dt_boss_three:         LocationData(None, 0x000000, RegionName.dt_main, "event"),
    LocationName.dt_boss_four:          LocationData(None, 0x000000, RegionName.dt_main, "event"),
    LocationName.roc_boss:              LocationData(None, 0x000000, RegionName.roc_main, "event"),
    LocationName.ck_boss_one:           LocationData(None, 0x000000, RegionName.ck_main, "event"),
    LocationName.ck_boss_two:           LocationData(None, 0x000000, RegionName.ck_main, "event"),
}

crystal_table = {
    LocationName.cc_behind_the_seal:    LocationData(None, 0x000000, RegionName.ck_main, "event"),
}

end_table = {
    LocationName.the_end:               LocationData(None, 0x000000, RegionName.ck_drac_chamber, "event"),
}

all_locations = {
    **main_location_table,
    **carrie_only_location_table,
    **cc_lizard_generator_table,
    **boss_table,
    **crystal_table,
    **end_table
}

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}


def create_locations(world, player: int, active_regions):
    location_table = {**main_location_table,
                      **end_table}

    if world.draculas_condition[player].value == 1:
        location_table.update({**crystal_table})
    elif world.draculas_condition[player].value == 2:
        location_table.update({**boss_table})
        if world.vincent_fight_condition[player].value == 0:
            del location_table[LocationName.ck_boss_two]
        if world.renon_fight_condition[player].value == 0:
            del location_table[LocationName.ck_boss_one]

    if world.carrie_logic[player].value:
        location_table.update({**carrie_only_location_table})

    if world.lizard_generator_items[player].value:
        location_table.update({**cc_lizard_generator_table})

    for loc, data in location_table.items():
        if data.region in active_regions:
            created_location = CV64Location(player, loc, data.code, active_regions[data.region],
                                            data.cv64_rom_offset, data.cv64_loc_type)
            active_regions[data.region].locations.append(created_location)
