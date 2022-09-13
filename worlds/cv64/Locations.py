import typing

from BaseClasses import Location
from .Names import LocationName


class CV64Location(Location):
    game: str = "Castlevania 64"

    progress_byte: int = 0x000000
    progress_bit:  int = 0
    inverted_bit: bool = False

    rom_offset: int

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, prog_byte: int = None,
                 prog_bit: int = None, invert: bool = False):
        super().__init__(player, name, address, parent)
        self.progress_byte = prog_byte
        self.progress_bit = prog_bit
        self.inverted_bit = invert


forest_location_table = {
    LocationName.forest_pillars_right:  0xC64001,
    LocationName.forest_pillars_top:  0xC64002,
    LocationName.forest_bone_mom:  0xC64003,
    LocationName.forest_lgaz_in:  0xC64004,
    LocationName.forest_lgaz_top:  0xC64005,
    LocationName.forest_hgaz_in:  0xC64006,
    LocationName.forest_hgaz_top:  0xC64007,
    LocationName.forest_weretiger_sw:  0xC64008,
    LocationName.forest_weretiger_gate:  0xC64009,
    LocationName.forest_dirge_tomb: 0xC6400A,
    LocationName.forest_corpse_save: 0xC6400B,
    LocationName.forest_dbridge_wall: 0xC6400C,
    LocationName.forest_dbridge_sw: 0xC6400D,
    LocationName.forest_dbridge_gate_r: 0xC6400E,
    LocationName.forest_dbridge_tomb: 0xC6400F,
    LocationName.forest_bface_tomb: 0xC64010,
    LocationName.forest_ibridge: 0xC64011,
    LocationName.forest_werewolf_tomb: 0xC64012,
    LocationName.forest_werewolf_tree: 0xC64013,
    LocationName.forest_final_sw: 0xC64014,
}

cw_location_table = {
    LocationName.cw_ground_middle: 0xC64015,
    LocationName.cw_rrampart: 0xC64016,
    LocationName.cw_lrampart: 0xC64017,
    LocationName.cw_dragon_sw: 0xC64018,
    LocationName.cw_drac_sw: 0xC64019,
    LocationName.cwr_bottom: 0xC6401A,
    LocationName.cwl_bottom: 0xC6401B,
    LocationName.cwl_bridge: 0xC6401C,
}

villa_location_table = {
    LocationName.villafy_outer_gate_l: 0xC6401D,
    LocationName.villafy_outer_gate_r: 0xC6401E,
    LocationName.villafy_dog_platform: 0xC6401F,
    LocationName.villafy_gate_marker: 0xC64020,
    LocationName.villafy_villa_marker: 0xC64021,
    LocationName.villafo_pot_r: 0xC64022,
    LocationName.villafo_pot_l: 0xC64023,
    LocationName.villafo_rear_l: 0xC6403F,
    LocationName.villafo_rear_r: 0xC64024,
    LocationName.villafo_mid_r: 0xC64025,
    LocationName.villafo_mid_l: 0xC64026,
    LocationName.villafo_front_l: 0xC64027,
    LocationName.villafo_front_r: 0xC64028,
    LocationName.villafo_serv_ent: 0xC64029,
    LocationName.villala_hallway_stairs: 0xC6402A,
    LocationName.villala_llivingroom_pot_r: 0xC6402B,
    LocationName.villala_llivingroom_pot_l: 0xC6402C,
    LocationName.villala_llivingroom_light: 0xC6402D,
    LocationName.villala_vincent: 0xC6402E,
    LocationName.villam_malus_torch: 0xC6402F,
    LocationName.villam_frankieturf_l: 0xC64030,
    LocationName.villam_frankieturf_ru: 0xC64031,
    LocationName.villam_fgarden_f: 0xC64032,
    LocationName.villam_fgarden_mf: 0xC64033,
    LocationName.villam_fgarden_mr: 0xC64034,
    LocationName.villam_fgarden_r: 0xC64035,
    LocationName.villam_rplatform_de: 0xC64036,
    LocationName.villam_exit_de: 0xC64037,
    LocationName.villam_serv_path: 0xC64038,
    LocationName.villam_crypt_ent: 0xC64039,
    LocationName.villam_crypt_upstream: 0xC6403A,
    LocationName.villac_ent_l: 0xC6403B,
    LocationName.villac_ent_r: 0xC6403C,
    LocationName.villac_wall_l: 0xC6403D,
    LocationName.villac_wall_r: 0xC6403E,
    LocationName.villac_coffin_r: 0xC64040,
}

tunnel_location_table = {
    LocationName.tunnel_landing: 0xC64041,
    LocationName.tunnel_landing_rc: 0xC64042,
    LocationName.tunnel_stone_alcove_l: 0xC64043,
    LocationName.tunnel_lbucket_quag: 0xC64044,
    LocationName.tunnel_lbucket_albert: 0xC64045,
    LocationName.tunnel_albert_camp: 0xC64046,
    LocationName.tunnel_albert_quag: 0xC64047,
    LocationName.tunnel_gondola_rc_sdoor_r: 0xC64048,
    LocationName.tunnel_gondola_rc_sdoor_m: 0xC64049,
    LocationName.tunnel_gondola_rc: 0xC6404A,
    LocationName.tunnel_rgondola_station: 0xC6404B,
    LocationName.tunnel_gondola_transfer: 0xC6404C,
    LocationName.tunnel_corpse_bucket_quag: 0xC6404D,
    LocationName.tunnel_corpse_bucket_mdoor_r: 0xC6404E,
    LocationName.tunnel_shovel_quag_start: 0xC6404F,
    LocationName.tunnel_exit_quag_start: 0xC64050,
    LocationName.tunnel_shovel_quag_end: 0xC64051,
    LocationName.tunnel_exit_quag_end: 0xC64052,
    LocationName.tunnel_shovel_save: 0xC64053,
    LocationName.tunnel_shovel_mdoor_l: 0xC64054,
    LocationName.tunnel_shovel_sdoor_l: 0xC64055,
    LocationName.tunnel_shovel_sdoor_m: 0xC64056,
}

uw_location_table = {
    LocationName.uw_near_ent: 0xC64057,
    LocationName.uw_across_ent: 0xC64058,
    LocationName.uw_poison_parkour: 0xC64059,
    LocationName.uw_waterfall_alcove: 0xC6405A,
    LocationName.uw_carrie1: 0xC6405B,
    LocationName.uw_carrie2: 0xC6405C,
    LocationName.uw_bricks_save: 0xC6405D,
    LocationName.uw_above_skel_ledge: 0xC6405E,
}

cc_location_table = {
    LocationName.ccb_skel_hallway_ent: 0xC6405F,
    LocationName.ccb_skel_hallway_jun: 0xC64060,
    LocationName.ccb_skel_hallway_tc: 0xC64061,
    LocationName.ccb_behemoth_l_ff: 0xC64062,
    LocationName.ccb_behemoth_l_mf: 0xC64063,
    LocationName.ccb_behemoth_l_mr: 0xC64064,
    LocationName.ccb_behemoth_l_fr: 0xC64065,
    LocationName.ccb_behemoth_r_ff: 0xC64066,
    LocationName.ccb_behemoth_r_mf: 0xC64067,
    LocationName.ccb_behemoth_r_mr: 0xC64068,
    LocationName.ccb_behemoth_r_fr: 0xC64069,
    LocationName.ccb_mandrag_shelf: 0xC6406A,
    LocationName.ccelv_near_machine: 0xC6406B,
    LocationName.ccelv_atop_machine: 0xC6406C,
    LocationName.ccelv_pipes: 0xC6406D,
    LocationName.ccelv_staircase: 0xC6406E,
    LocationName.ccff_gears_side: 0xC6406F,
    LocationName.ccff_gears_mid: 0xC64070,
    LocationName.ccff_gears_corner: 0xC64071,
    LocationName.ccff_lizard_pit: 0xC64072,
    LocationName.ccff_lizard_corner: 0xC64073,
    LocationName.ccll_brokenstairs_floor: 0xC64074,
    LocationName.ccll_brokenstairs_save: 0xC64075,
    LocationName.ccll_glassknight_l: 0xC64076,
    LocationName.ccll_glassknight_r: 0xC64077,
    LocationName.ccll_butlers_door: 0xC64078,
    LocationName.ccll_butlers_side: 0xC64079,
    LocationName.ccll_cwhall_butlerflames_past: 0xC6407A,
    LocationName.ccll_cwhall_cwflames: 0xC6407B,
    LocationName.ccll_cwhall_wall: 0xC6407C,
    LocationName.ccll_lizardman: 0xC6407D,
    LocationName.ccia_nitro_shelf: 0xC6407E,
    LocationName.ccia_nitrohall_torch: 0xC6407F,
    LocationName.ccia_inventions_crusher: 0xC64080,
    LocationName.ccia_inventions_maids: 0xC64081,
    LocationName.ccia_maids_outer: 0xC64082,
    LocationName.ccia_maids_inner: 0xC64083,
}

dt_location_table = {
    LocationName.dt_stones_start: 0xC64084,
    LocationName.dt_werebull_arena: 0xC64085,
    LocationName.dt_ibridge_l: 0xC64086,
    LocationName.dt_ibridge_r: 0xC64087,
}

toe_location_table = {
    LocationName.toe_midsavespikes_r: 0xC64088,
    LocationName.toe_midsavespikes_l: 0xC64089,
    LocationName.toe_elec_grate: 0xC6408A,
    LocationName.toe_ibridge: 0xC6408B,
    LocationName.toe_top: 0xC6408C,
    LocationName.toe_keygate_l: 0xC6408D,
}

tosci_location_table = {
    LocationName.tosci_elevator: 0xC6408E,
    LocationName.tosci_plain_sr: 0xC6408F,
    LocationName.tosci_stairs_sr: 0xC64090,
    LocationName.tosci_three_door_hall: 0xC64091,
    LocationName.tosci_ibridge_t: 0xC64092,
    LocationName.tosci_conveyor_sr: 0xC64093,
    LocationName.tosci_exit: 0xC64094,
    LocationName.tosci_key3_r: 0xC64095,
    LocationName.tosci_key3_l: 0xC64096,
}

tosor_location_table = {
    LocationName.tosor_stained_tower: 0xC64097,
    LocationName.tosor_savepoint: 0xC64098,
    LocationName.tosor_trickshot: 0xC64099,
    LocationName.tosor_yellow_bubble: 0xC6409A,
    LocationName.tosor_blue_platforms: 0xC6409B,
    LocationName.tosor_side_isle: 0xC6409C,
    LocationName.tosor_ibridge: 0xC6409D,
}

roc_location_table = {
    LocationName.roc_ent_l: 0xC6409E,
    LocationName.roc_gs_r: 0xC6409F,
    LocationName.roc_ent_r: 0xC640A0,
}

ct_location_table = {
    LocationName.ct_gearclimb_side: 0xC640A1,
    LocationName.ct_gearclimb_mid: 0xC640A2,
    LocationName.ct_finalroom_platform: 0xC640A3,
}

ck_location_table = {
    LocationName.ck_behind_drac: 0xC640A4,
    LocationName.ck_cube: 0xC640A5,
    LocationName.the_end: 0xC64000
}

all_locations = {
    **forest_location_table,
    **cw_location_table,
    **villa_location_table,
    **tunnel_location_table,
    **uw_location_table,
    **cc_location_table,
    **dt_location_table,
    **toe_location_table,
    **tosci_location_table,
    **tosor_location_table,
    **roc_location_table,
    **ct_location_table,
    **ck_location_table,
}

location_table = {}


def setup_locations(world, player: int):
    locations_table = {**forest_location_table, **cw_location_table, **villa_location_table, **tunnel_location_table,
                       **uw_location_table, **cc_location_table, **dt_location_table, **toe_location_table,
                       **tosci_location_table, **tosor_location_table, **roc_location_table, **ct_location_table,
                       **ck_location_table}

    return locations_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
