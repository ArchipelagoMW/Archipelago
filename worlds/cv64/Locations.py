import typing

from BaseClasses import Location
from .Names import LocationName


class CV64Location(Location):
    game: str = "Castlevania 64"

    progress_byte: int = 0x000000
    progress_bit:  int = 0
    inverted_bit: bool = False

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, prog_byte: int = None,
                 prog_bit: int = None, invert: bool = False):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit = prog_bit
        self.inverted_bit = invert


class LocationData(typing.NamedTuple):
    code: typing.Optional[int]
    rom_offset: int
    loc_type: str = "normal"


main_location_table = {
    # Forest of Silence locations
    LocationName.forest_pillars_right:   LocationData(0xC64001, 0x10C67B),
    LocationName.forest_pillars_top:     LocationData(0xC64002, 0x10C71B),
    LocationName.forest_bone_mom:        LocationData(0xC64003, 0x10C6BB),
    LocationName.forest_lgaz_in:         LocationData(0xC64004, 0x10C68B),
    LocationName.forest_lgaz_top:        LocationData(0xC64005, 0x10C693),
    LocationName.forest_hgaz_in:         LocationData(0xC64006, 0x10C6C3),
    LocationName.forest_hgaz_top:        LocationData(0xC64007, 0x10C6E3),
    LocationName.forest_weretiger_sw:    LocationData(0xC64008, 0x10C6CB),
    LocationName.forest_weretiger_gate:  LocationData(0xC64009, 0x10C683),
    LocationName.forest_dirge_tomb:      LocationData(0xC6400A, 0x10C743),
    LocationName.forest_corpse_save:     LocationData(0xC6400B, 0x10C6A3),
    LocationName.forest_dbridge_wall:    LocationData(0xC6400C, 0x10C69B),
    LocationName.forest_dbridge_sw:      LocationData(0xC6400D, 0x10C6D3),
    LocationName.forest_dbridge_gate_r:  LocationData(0xC6400E, 0x10C6AB),
    LocationName.forest_dbridge_tomb:    LocationData(0xC6400F, 0x10C76B),
    LocationName.forest_bface_tomb_l:    LocationData(0xC64010, 0x10C75B),
    LocationName.forest_bface_tomb_u:    LocationData(0xC64025, 0x10C77B),
    LocationName.forest_ibridge:         LocationData(0xC64011, 0x10C713),
    LocationName.forest_werewolf_tomb:   LocationData(0xC64012, 0x10C733),
    LocationName.forest_werewolf_tree:   LocationData(0xC64013, 0x10C6B3),
    LocationName.forest_final_sw:        LocationData(0xC64014, 0x10C72B),
    LocationName.forest_dirge_plaque:    LocationData(0xC640A6, 0x7C7F9D, "invisible"),
    LocationName.forest_werewolf_plaque: LocationData(0xC640A7, 0xBFC937, "invisible"),
    # Castle Wall Main Area locations
    LocationName.cw_ground_middle:  LocationData(0xC64015, 0x10C7F7),
    LocationName.cw_rrampart:       LocationData(0xC64016, 0x10C7FF),
    LocationName.cw_lrampart:       LocationData(0xC64017, 0x10C807),
    LocationName.cw_dragon_sw:      LocationData(0xC64018, 0x10C817),
    LocationName.cw_drac_sw:        LocationData(0xC64019, 0x10C80F),
    LocationName.cw_shelf_visible:  LocationData(0xC640A8, 0x7F99A9),
    LocationName.cw_shelf_sandbags: LocationData(0xC640A9, 0x7F9A3E, "invisible"),
    # Castle Wall Tower locations
    LocationName.cwr_bottom:        LocationData(0xC6401A, 0x10C7E7),
    LocationName.cwl_bottom:        LocationData(0xC6401B, 0x10C7DF),
    LocationName.cwl_bridge:        LocationData(0xC6401C, 0x10C7EF),
    # Villa Front Yard locations
    LocationName.villafy_outer_gate_l:          LocationData(0xC6401D, 0x10C87F),
    LocationName.villafy_outer_gate_r:          LocationData(0xC6401E, 0x10C887),
    LocationName.villafy_dog_platform:          LocationData(0xC6401F, 0x10C89F),
    LocationName.villafy_gate_marker:           LocationData(0xC64020, 0x10C8A7),
    LocationName.villafy_villa_marker:          LocationData(0xC64021, 0x10C897),
    LocationName.villafy_inner_gate:            LocationData(0xC640AA, 0xBFC95F),
    LocationName.villafy_tombstone:             LocationData(0xC640AB, 0x8099CC, "invisible"),
    LocationName.villafy_fountain_fl:           LocationData(0xC640AC, 0xBFC957),
    LocationName.villafy_fountain_fr:           LocationData(0xC640AD, 0x80997D),
    LocationName.villafy_fountain_ml:           LocationData(0xC640AE, 0x809956),
    LocationName.villafy_fountain_mr:           LocationData(0xC640AF, 0x80992D),
    LocationName.villafy_fountain_rl:           LocationData(0xC640B0, 0xBFC95B),
    LocationName.villafy_fountain_rr:           LocationData(0xC640B1, 0x80993C),
    # Villa Foyer locations
    LocationName.villafo_pot_r:                 LocationData(0xC64022, 0x10C8AF),
    LocationName.villafo_pot_l:                 LocationData(0xC64023, 0x10C8B7),
    LocationName.villafo_rear_l:                LocationData(0xC6403F, 0x10C8BF),
    LocationName.villafo_rear_r:                LocationData(0xC64024, 0x10C8C7),
    LocationName.villafo_mid_l:                 LocationData(0xC64026, 0x10C8D7),
    LocationName.villafo_front_l:               LocationData(0xC64027, 0x10C8DF),
    LocationName.villafo_front_r:               LocationData(0xC64028, 0x10C8E7),
    LocationName.villafo_serv_ent:              LocationData(0xC64029, 0x10C8EF),
    LocationName.villafo_sofa:                  LocationData(0xC640B2, 0x81F07C, "invisible"),
    # Villa Living Area locations
    LocationName.villala_hallway_stairs:        LocationData(0xC6402A, 0x10C927),
    LocationName.villala_llivingroom_pot_r:     LocationData(0xC6402B, 0x10C90F),
    LocationName.villala_llivingroom_pot_l:     LocationData(0xC6402C, 0x10C917),
    LocationName.villala_llivingroom_light:     LocationData(0xC6402D, 0x10C91F),
    LocationName.villala_vincent:               LocationData(0xC6402E, 0xBFC203, "npc"),
    LocationName.villala_storeroom_l:           LocationData(0xC640B3, 0x83A5CA),
    LocationName.villala_storeroom_r:           LocationData(0xC640B4, 0xBFC97F),
    LocationName.villala_storeroom_s:           LocationData(0xC640B5, 0x83A604, "invisible"),
    LocationName.villala_bedroom_chairs:        LocationData(0xC640B6, 0x83A588),
    LocationName.villala_bedroom_bed:           LocationData(0xC640B7, 0x83A593),
    LocationName.villala_slivingroom_table:     LocationData(0xC640B8, 0x83A635, "invisible"),
    LocationName.villala_diningroom_roses:      LocationData(0xC640B9, 0xBFC98B, "invisible"),
    LocationName.villala_archives_table:        LocationData(0xC640BA, 0xBFC98F, "invisible"),
    LocationName.villala_archives_rear:         LocationData(0xC640BB, 0x83A5B1),
    LocationName.villala_llivingroom_lion:      LocationData(0xC640BC, 0x83A610, "invisible"),
    LocationName.villala_llivingroom_painting:  LocationData(0xC640BD, 0xBFC987, "invisible"),
    LocationName.villala_exit_knight:           LocationData(0xC640BE, 0x83A61B),
    # Villa Maze locations
    LocationName.villam_malus_torch:            LocationData(0xC6402F, 0x10C967),
    LocationName.villam_frankieturf_l:          LocationData(0xC64030, 0x10C947),
    LocationName.villam_frankieturf_ru:         LocationData(0xC64031, 0x10C9A7),
    LocationName.villam_fgarden_f:              LocationData(0xC64032, 0x10C96F),
    LocationName.villam_fgarden_mf:             LocationData(0xC64033, 0x10C977),
    LocationName.villam_fgarden_mr:             LocationData(0xC64034, 0x10C95F),
    LocationName.villam_fgarden_r:              LocationData(0xC64035, 0x10C97F),
    LocationName.villam_rplatform_de:           LocationData(0xC64036, 0x10C94F),
    LocationName.villam_exit_de:                LocationData(0xC64037, 0x10C957),
    LocationName.villam_serv_path:              LocationData(0xC64038, 0x10C92F),
    LocationName.villam_crypt_ent:              LocationData(0xC64039, 0x10C93F),
    LocationName.villam_crypt_upstream:         LocationData(0xC6403A, 0x10C937),
    LocationName.villam_malus_bush:             LocationData(0xC640BF, 0x850FEC, "invisible"),
    # Villa Crypt locations
    LocationName.villac_ent_l:                  LocationData(0xC6403B, 0x10CF4B),
    LocationName.villac_ent_r:                  LocationData(0xC6403C, 0x10CF63),
    LocationName.villac_wall_l:                 LocationData(0xC6403D, 0x10CF6B),
    LocationName.villac_wall_r:                 LocationData(0xC6403E, 0x10CF5B),
    LocationName.villac_coffin_r:               LocationData(0xC64040, 0x10CF53),
    # Tunnel locations
    LocationName.tunnel_landing:                LocationData(0xC64041, 0x10C9AF),
    LocationName.tunnel_landing_rc:             LocationData(0xC64042, 0x10C9B7),
    LocationName.tunnel_stone_alcove_l:         LocationData(0xC64043, 0x10CA9F),
    LocationName.tunnel_lbucket_quag:           LocationData(0xC64044, 0x10C9DF),
    LocationName.tunnel_lbucket_albert:         LocationData(0xC64045, 0x10C9E7),
    LocationName.tunnel_albert_camp:            LocationData(0xC64046, 0x10C9D7),
    LocationName.tunnel_albert_quag:            LocationData(0xC64047, 0x10C9CF),
    LocationName.tunnel_gondola_rc_sdoor_r:     LocationData(0xC64048, 0x10CA27),
    LocationName.tunnel_gondola_rc_sdoor_m:     LocationData(0xC64049, 0x10CAA7),
    LocationName.tunnel_gondola_rc:             LocationData(0xC6404A, 0x10CAB7),
    LocationName.tunnel_rgondola_station:       LocationData(0xC6404B, 0x10C9C7),
    LocationName.tunnel_gondola_transfer:       LocationData(0xC6404C, 0x10CA2F),
    LocationName.tunnel_corpse_bucket_quag:     LocationData(0xC6404D, 0x10C9F7),
    LocationName.tunnel_corpse_bucket_mdoor_r:  LocationData(0xC6404E, 0x10CA37),
    LocationName.tunnel_shovel_quag_start:      LocationData(0xC6404F, 0x10C9FF),
    LocationName.tunnel_exit_quag_start:        LocationData(0xC64050, 0x10CA07),
    LocationName.tunnel_shovel_quag_end:        LocationData(0xC64051, 0x10CA0F),
    LocationName.tunnel_exit_quag_end:          LocationData(0xC64052, 0x10CA3F),
    LocationName.tunnel_shovel_save:            LocationData(0xC64053, 0x10CA17),
    LocationName.tunnel_shovel_mdoor_l:         LocationData(0xC64054, 0x10CA47),
    LocationName.tunnel_shovel_sdoor_l:         LocationData(0xC64055, 0x10CA4F),
    LocationName.tunnel_shovel_sdoor_m:         LocationData(0xC64056, 0x10CAAF),
    LocationName.tunnel_twin_arrows:            LocationData(0xC640C0, 0xBFC9B7, "invisible"),
    LocationName.tunnel_lonesome_bucket:        LocationData(0xC640C1, 0x86D8E1, "invisible"),
    LocationName.tunnel_shovel:                 LocationData(0xC640C2, 0x86D8FC, "invisible"),
    # Underground Waterway locations
    LocationName.uw_near_ent:           LocationData(0xC64057, 0x10CB03),
    LocationName.uw_across_ent:         LocationData(0xC64058, 0x10CAF3),
    LocationName.uw_poison_parkour:     LocationData(0xC64059, 0x10CAFB),
    LocationName.uw_waterfall_alcove:   LocationData(0xC6405A, 0x10CB23),
    LocationName.uw_bricks_save:        LocationData(0xC6405D, 0x10CB33),
    LocationName.uw_above_skel_ledge:   LocationData(0xC6405E, 0x10CB2B),
    # Castle Center Basement locations
    LocationName.ccb_skel_hallway_ent:          LocationData(0xC6405F, 0x10CB67),
    LocationName.ccb_skel_hallway_jun:          LocationData(0xC64060, 0x10CBD7),
    LocationName.ccb_skel_hallway_tc:           LocationData(0xC64061, 0x10CB6F),
    LocationName.ccb_behemoth_l_ff:             LocationData(0xC64062, 0x10CB77),
    LocationName.ccb_behemoth_l_mf:             LocationData(0xC64063, 0x10CBA7),
    LocationName.ccb_behemoth_l_mr:             LocationData(0xC64064, 0x10CB7F),
    LocationName.ccb_behemoth_l_fr:             LocationData(0xC64065, 0x10CBAF),
    LocationName.ccb_behemoth_r_ff:             LocationData(0xC64066, 0x10CBB7),
    LocationName.ccb_behemoth_r_mf:             LocationData(0xC64067, 0x10CB87),
    LocationName.ccb_behemoth_r_mr:             LocationData(0xC64068, 0x10CBBF),
    LocationName.ccb_behemoth_r_fr:             LocationData(0xC64069, 0x10CB8F),
    LocationName.ccb_mandrag_shelf:             LocationData(0xC6406A, 0xBFC1E3, "npc"),
    LocationName.ccb_torture_rack:              LocationData(0xC640C3, 0x8985E5, "invisible"),
    LocationName.ccb_torture_rafters:           LocationData(0xC640C4, 0x8985D6),
    # Castle Center Elevator Room locations
    LocationName.ccelv_near_machine:            LocationData(0xC6406B, 0x10CBF7),
    LocationName.ccelv_atop_machine:            LocationData(0xC6406C, 0x10CC17),
    LocationName.ccelv_pipes:                   LocationData(0xC6406D, 0x10CC07),
    LocationName.ccelv_staircase:               LocationData(0xC6406E, 0x10CBFF),
    # Castle Center Factory Floor locations
    LocationName.ccff_gears_side:               LocationData(0xC6406F, 0x10CC33),
    LocationName.ccff_gears_mid:                LocationData(0xC64070, 0x10CC3B),
    LocationName.ccff_gears_corner:             LocationData(0xC64071, 0x10CC43),
    LocationName.ccff_lizard_pit:               LocationData(0xC64072, 0x10CC4B),
    LocationName.ccff_lizard_corner:            LocationData(0xC64073, 0x10CC53),
    LocationName.ccff_redcarpet_knight:         LocationData(0xC640C5, 0x8C44D9, "invisible"),
    LocationName.ccff_lizard_knight:            LocationData(0xC640C6, 0x8C44E7, "invisible"),
    # Castle Center Lizard-man Lab locations
    LocationName.ccll_brokenstairs_floor:       LocationData(0xC64074, 0x10CC8F),
    LocationName.ccll_brokenstairs_save:        LocationData(0xC64075, 0x10CC87),
    LocationName.ccll_glassknight_l:            LocationData(0xC64076, 0x10CC97),
    LocationName.ccll_glassknight_r:            LocationData(0xC64077, 0x10CC77),
    LocationName.ccll_butlers_door:             LocationData(0xC64078, 0x10CC7F),
    LocationName.ccll_butlers_side:             LocationData(0xC64079, 0x10CC9F),
    LocationName.ccll_cwhall_butlerflames_past: LocationData(0xC6407A, 0x10CCA7),
    LocationName.ccll_cwhall_cwflames:          LocationData(0xC6407B, 0x10CCAF),
    LocationName.ccll_cwhall_wall:              LocationData(0xC6407C, 0x10CCB7),
    LocationName.ccll_heinrich:                 LocationData(0xC6407D, 0xBFC20F, "npc"),
    LocationName.ccll_brokenstairs_knight:      LocationData(0xC640CD, 0x8DF782, "invisible"),
    LocationName.ccll_cwhall_flamethrower:      LocationData(0xC640CE, 0x8DF580, "invisible"),
    # Castle Center Library location
    LocationName.ccl_bookcase:                  LocationData(0xC640CF, 0x8F1197),
    # Castle Center Invention Area locations
    LocationName.ccia_nitro_shelf:              LocationData(0xC6407E, 0xBFC1C3, "npc"),
    LocationName.ccia_nitrohall_torch:          LocationData(0xC6407F, 0x10CCD7),
    LocationName.ccia_inventions_crusher:       LocationData(0xC64080, 0x10CCDF),
    LocationName.ccia_inventions_maids:         LocationData(0xC64081, 0x10CCE7),
    LocationName.ccia_maids_outer:              LocationData(0xC64082, 0x10CCFF),
    LocationName.ccia_maids_inner:              LocationData(0xC64083, 0x10CD07),
    LocationName.ccia_nitro_crates:             LocationData(0xC640D0, 0x90FCE9, "invisible"),
    LocationName.ccia_nitrohall_flamethrower:   LocationData(0xC640D1, 0x90FCDA, "invisible"),
    LocationName.ccia_inventions_round:         LocationData(0xC640D2, 0x90FBA7, "invisible"),
    LocationName.ccia_inventions_famicart:      LocationData(0xC640D3, 0x90FBB3, "invisible"),
    LocationName.ccia_inventions_zeppelin:      LocationData(0xC640D4, 0x90FBC0),
    LocationName.ccia_maids_vase:               LocationData(0xC640D5, 0x90FF1D, "invisible"),
    LocationName.ccia_stairs_knight:            LocationData(0xC640D6, 0x90FE5C, "invisible"),
    # Duel Tower locations
    LocationName.dt_stones_start:   LocationData(0xC64084, 0x10CE73),
    LocationName.dt_werebull_arena: LocationData(0xC64085, 0x10CE7B),
    LocationName.dt_ibridge_l:      LocationData(0xC64086, 0x10CE8B),
    LocationName.dt_ibridge_r:      LocationData(0xC64087, 0x10CE93),
    # Tower Of Execution locations
    LocationName.toe_midsavespikes_r:   LocationData(0xC64088, 0x10CD1F),
    LocationName.toe_midsavespikes_l:   LocationData(0xC64089, 0x10CD27),
    LocationName.toe_elec_grate:        LocationData(0xC6408A, 0x10CD17),
    LocationName.toe_ibridge:           LocationData(0xC6408B, 0x10CD47),
    LocationName.toe_top:               LocationData(0xC6408C, 0x10CD4F),
    LocationName.toe_keygate_l:         LocationData(0xC6408D, 0x10CD37),
    # Tower Of Science locations
    LocationName.tosci_elevator:        LocationData(0xC6408E, 0x10CE0B),
    LocationName.tosci_plain_sr:        LocationData(0xC6408F, 0x10CDF3),
    LocationName.tosci_stairs_sr:       LocationData(0xC64090, 0x10CE13),
    LocationName.tosci_three_door_hall: LocationData(0xC64091, 0x10CDFB),
    LocationName.tosci_ibridge_t:       LocationData(0xC64092, 0x10CE3B),
    LocationName.tosci_conveyor_sr:     LocationData(0xC64093, 0x10CE33),
    LocationName.tosci_exit:            LocationData(0xC64094, 0x10CE03),
    LocationName.tosci_key3_r:          LocationData(0xC64095, 0x10CE1B),
    LocationName.tosci_key3_l:          LocationData(0xC64096, 0x10CE23),
    # Tower Of Sorcery locations
    LocationName.tosor_stained_tower:   LocationData(0xC64097, 0x10CDB3),
    LocationName.tosor_savepoint:       LocationData(0xC64098, 0x10CDBB),
    LocationName.tosor_trickshot:       LocationData(0xC64099, 0x10CDD3),
    LocationName.tosor_yellow_bubble:   LocationData(0xC6409A, 0x10CDDB),
    LocationName.tosor_blue_platforms:  LocationData(0xC6409B, 0x10CDC3),
    LocationName.tosor_side_isle:       LocationData(0xC6409C, 0x10CDCB),
    LocationName.tosor_ibridge:         LocationData(0xC6409D, 0x10CDE3),
    # Room Of Clocks locations
    LocationName.roc_ent_l: LocationData(0xC6409E, 0x10CF7B),
    LocationName.roc_gs_r:  LocationData(0xC6409F, 0x10CFB3),
    LocationName.roc_ent_r: LocationData(0xC640A0, 0x10CFBB),
    # Clock Tower locations
    LocationName.ct_gearclimb_side: LocationData(0xC640A1, 0x10CEB3),
    LocationName.ct_gearclimb_mid: LocationData(0xC640A2, 0x10CEC3),
    LocationName.ct_finalroom_platform: LocationData(0xC640A3, 0x10CEBB),
    LocationName.ct_bp_chasm_fl: LocationData(0xC640D7, 0x99BC4D),
    LocationName.ct_bp_chasm_fr: LocationData(0xC640D8, 0x99BC3E),
    LocationName.ct_bp_chasm_k: LocationData(0xC640D9, 0x99BC30),
    # Castle Keep locations
    LocationName.ck_behind_drac: LocationData(0xC640A4, 0x10CE9B),
    LocationName.ck_cube: LocationData(0xC640A5, 0x10CEA3),
    LocationName.ck_flame_l: LocationData(0xC640DA, 0x9778C8, "invisible"),
    LocationName.ck_flame_r: LocationData(0xC640DB, 0xBFCA6B, "invisible")
}

carrie_only_location_table = {
    LocationName.uw_carrie1: LocationData(0xC6405B, 0x10CB0B),
    LocationName.uw_carrie2: LocationData(0xC6405C, 0x10CB13)
}

cc_lizard_generator_table = {
    LocationName.ccff_lizard_coffin_nfr: LocationData(0xC640C7, 0x8C450A),
    LocationName.ccff_lizard_coffin_nmr: LocationData(0xC640C8, 0xBFC9D7),
    LocationName.ccff_lizard_coffin_nml: LocationData(0xC640C9, 0xBFC9DB),
    LocationName.ccff_lizard_coffin_nfl: LocationData(0xC640CA, 0x8C451C),
    LocationName.ccff_lizard_coffin_fl:  LocationData(0xC640CB, 0x8C44fD),
    LocationName.ccff_lizard_coffin_fr:  LocationData(0xC640CC, 0x8C44F5)
}

event_location_table = {
    LocationName.forest_boss_one:       LocationData(None, 0x000000, "event"),
    LocationName.forest_boss_two:       LocationData(None, 0x000000, "event"),
    LocationName.forest_boss_three:     LocationData(None, 0x000000, "event"),
    LocationName.cw_boss:               LocationData(None, 0x000000, "event"),
    LocationName.villa_boss_one:        LocationData(None, 0x000000, "event"),
    LocationName.villa_boss_two:        LocationData(None, 0x000000, "event"),
    LocationName.uw_boss:               LocationData(None, 0x000000, "event"),
    LocationName.cc_boss_one:           LocationData(None, 0x000000, "event"),
    LocationName.cc_boss_two:           LocationData(None, 0x000000, "event"),
    LocationName.dt_boss_one:           LocationData(None, 0x000000, "event"),
    LocationName.dt_boss_two:           LocationData(None, 0x000000, "event"),
    LocationName.dt_boss_three:         LocationData(None, 0x000000, "event"),
    LocationName.dt_boss_four:          LocationData(None, 0x000000, "event"),
    LocationName.roc_boss:              LocationData(None, 0x000000, "event"),
    LocationName.ck_boss_one:           LocationData(None, 0x000000, "event"),
    LocationName.ck_boss_two:           LocationData(None, 0x000000, "event"),
    LocationName.cc_behind_the_seal:    LocationData(None, 0x000000, "event"),
    LocationName.the_end:               LocationData(None, 0x000000, "event"),
}

all_locations = {
    **main_location_table,
    **carrie_only_location_table,
    **cc_lizard_generator_table,
    **event_location_table
}

location_table = {}


def setup_locations(world, player: int):
    location_table = {**main_location_table,
                      **event_location_table}

    if world.carrie_logic[player].value:
        location_table.update({**carrie_only_location_table})

    if world.lizard_generator_items[player].value:
        location_table.update({**cc_lizard_generator_table})

    return location_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
