import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import CV64Item
from .Locations import CV64Location
from .Names import LocationName, ItemName
from .Rom import rom_loc_offsets


class LevelGate:
    gate_levels: typing.List[int]
    gate_special_count: int

    def __init__(self, specials):
        self.gate_special_count = specials
        self.gate_levels = list()


shuffleable_regions = [
    LocationName.forest_of_silence,
    LocationName.castle_wall,
    LocationName.villa,
    LocationName.tunnel,
    LocationName.underground_waterway,
    LocationName.castle_center,
    LocationName.duel_tower,
    LocationName.tower_of_execution,
    LocationName.tower_of_science,
    LocationName.tower_of_sorcery,
    LocationName.room_of_clocks,
    LocationName.clock_tower,
]


def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None, None)
    warp2_region = create_region(world, player, active_locations, 'Warp 2', None, None)
    warp3_region = create_region(world, player, active_locations, 'Warp 3', None, None)
    warp4_region = create_region(world, player, active_locations, 'Warp 4', None, None)
    warp5_region = create_region(world, player, active_locations, 'Warp 5', None, None)
    warp6_region = create_region(world, player, active_locations, 'Warp 6', None, None)
    warp7_region = create_region(world, player, active_locations, 'Warp 7', None, None)
    warp8_region = create_region(world, player, active_locations, 'Warp 8', None, None)

    # Forest of Silence regions
    forest_start_region_locations = [
        LocationName.forest_pillars_right,
        LocationName.forest_pillars_top,
        LocationName.forest_bone_mom,
        LocationName.forest_lgaz_in,
        LocationName.forest_lgaz_top,
        LocationName.forest_hgaz_in,
        LocationName.forest_hgaz_top,
        LocationName.forest_weretiger_sw,
        LocationName.forest_weretiger_gate,
        LocationName.forest_dirge_tomb,
        LocationName.forest_corpse_save,
        LocationName.forest_dbridge_wall,
        LocationName.forest_dbridge_sw,
        LocationName.forest_dbridge_gate_r,
        LocationName.forest_dbridge_tomb,
        LocationName.forest_bface_tomb,
        LocationName.forest_ibridge,
        LocationName.forest_werewolf_tomb,
        LocationName.forest_werewolf_tree,
        LocationName.forest_final_sw,
    ]
    forest_start_region = create_region(world, player, active_locations, LocationName.forest_of_silence,
                                        forest_start_region_locations, None)

    # Castle Wall regions
    cw_main_region_locations = [
        LocationName.cw_ground_middle,
        LocationName.cw_rrampart,
        LocationName.cw_lrampart,
        LocationName.cw_dragon_sw,
        LocationName.cwr_bottom,
    ]
    cw_start_region = create_region(world, player, active_locations, LocationName.castle_wall,
                                    cw_main_region_locations, None)

    cw_ltower_region_locations = [
        LocationName.cw_drac_sw,
        LocationName.cwl_bottom,
        LocationName.cwl_bridge,
    ]
    cw_ltower_region = create_region(world, player, active_locations, LocationName.cw_ltower,
                                     cw_ltower_region_locations, None)

    villa_start_region_locations = [
        LocationName.villafy_outer_gate_l,
        LocationName.villafy_outer_gate_r,
        LocationName.villafy_dog_platform,
        LocationName.villafy_gate_marker,
        LocationName.villafy_villa_marker,
        LocationName.villafo_pot_r,
        LocationName.villafo_pot_l,
        LocationName.villafo_rear_r,
        LocationName.villafo_rear_l,
        LocationName.villafo_mid_r,
        LocationName.villafo_mid_l,
        LocationName.villafo_front_r,
        LocationName.villafo_front_l,
        LocationName.villala_hallway_stairs,
        LocationName.villala_llivingroom_pot_r,
        LocationName.villala_llivingroom_pot_l,
        LocationName.villala_llivingroom_light,
        LocationName.villala_vincent,
    ]
    villa_start_region = create_region(world, player, active_locations, LocationName.villa,
                                       villa_start_region_locations, None)

    villa_storeroom_region = create_region(world, player, active_locations, LocationName.villa_storeroom, None, None)
    villa_archives_region = create_region(world, player, active_locations, LocationName.villa_archives, None, None)

    villa_maze_region_locations = [
        LocationName.villam_malus_torch,
        LocationName.villam_frankieturf_l,
        LocationName.villam_frankieturf_ru,
        LocationName.villam_fgarden_f,
        LocationName.villam_fgarden_mf,
        LocationName.villam_fgarden_mr,
        LocationName.villam_fgarden_r,
        LocationName.villam_rplatform_de,
        LocationName.villam_exit_de,
        LocationName.villam_serv_path,
        LocationName.villafo_serv_ent,
    ]
    villa_maze_region = create_region(world, player, active_locations, LocationName.villa_maze_main,
                                      villa_maze_region_locations, None)

    villa_crypt_region_locations = [
        LocationName.villam_crypt_ent,
        LocationName.villam_crypt_upstream,
        LocationName.villac_ent_l,
        LocationName.villac_ent_r,
        LocationName.villac_wall_l,
        LocationName.villac_wall_r,
        # LocationName.villac_coffin_l,
        LocationName.villac_coffin_r,
    ]
    villa_crypt_region = create_region(world, player, active_locations, LocationName.villa_crypt,
                                       villa_crypt_region_locations, None)

    tunnel_region_locations = [
        LocationName.tunnel_landing,
        LocationName.tunnel_landing_rc,
        LocationName.tunnel_stone_alcove_l,
        LocationName.tunnel_lbucket_quag,
        LocationName.tunnel_lbucket_albert,
        LocationName.tunnel_albert_camp,
        LocationName.tunnel_albert_quag,
        LocationName.tunnel_gondola_rc_sdoor_r,
        LocationName.tunnel_gondola_rc_sdoor_m,
        LocationName.tunnel_gondola_rc,
        LocationName.tunnel_rgondola_station,
        LocationName.tunnel_gondola_transfer,
        LocationName.tunnel_corpse_bucket_quag,
        LocationName.tunnel_corpse_bucket_mdoor_r,
        LocationName.tunnel_shovel_quag_start,
        LocationName.tunnel_exit_quag_start,
        LocationName.tunnel_shovel_quag_end,
        LocationName.tunnel_exit_quag_end,
        LocationName.tunnel_shovel_save,
        LocationName.tunnel_shovel_mdoor_l,
        LocationName.tunnel_shovel_sdoor_l,
        LocationName.tunnel_shovel_sdoor_m,
    ]
    tunnel_region = create_region(world, player, active_locations, LocationName.tunnel,
                                  tunnel_region_locations, None)

    uw_start_region_locations = [
        LocationName.uw_near_ent,
        LocationName.uw_across_ent,
        LocationName.uw_poison_parkour,
        LocationName.uw_waterfall_alcove,
        LocationName.uw_bricks_save,
        LocationName.uw_above_skel_ledge,
    ]
    uw_start_region = create_region(world, player, active_locations, LocationName.underground_waterway,
                                    uw_start_region_locations, None)

    uw_carrie_region_locations = [
        LocationName.uw_carrie1,
        LocationName.uw_carrie2,
    ]
    uw_carrie_region = create_region(world, player, active_locations, LocationName.uw_carrie,
                                    uw_carrie_region_locations, None)

    cc_start_region_locations = [
        LocationName.ccb_skel_hallway_ent,
        LocationName.ccb_skel_hallway_jun,
        LocationName.ccb_skel_hallway_tc,
        LocationName.ccb_behemoth_l_ff,
        LocationName.ccb_behemoth_l_mf,
        LocationName.ccb_behemoth_l_mr,
        LocationName.ccb_behemoth_l_fr,
        LocationName.ccb_behemoth_r_ff,
        LocationName.ccb_behemoth_r_mf,
        LocationName.ccb_behemoth_r_mr,
        LocationName.ccb_behemoth_r_fr,
        LocationName.ccelv_near_machine,
        LocationName.ccelv_atop_machine,
        LocationName.ccelv_pipes,
        LocationName.ccelv_staircase,
        LocationName.ccff_gears_side,
        LocationName.ccff_gears_mid,
        LocationName.ccff_gears_corner,
        LocationName.ccff_lizard_pit,
        LocationName.ccff_lizard_corner,
        LocationName.ccll_brokenstairs_floor,
        LocationName.ccll_brokenstairs_save,
        LocationName.ccll_glassknight_l,
        LocationName.ccll_glassknight_r,
        LocationName.ccll_butlers_door,
        LocationName.ccll_butlers_side,
        LocationName.ccll_cwhall_butlerflames_past,
        LocationName.ccll_cwhall_cwflames,
        LocationName.ccll_lizardman,
        LocationName.ccia_nitro_shelf,
        LocationName.ccia_nitrohall_torch,
        LocationName.ccia_inventions_crusher,
        LocationName.ccia_inventions_maids,
        LocationName.ccia_maids_outer,
        LocationName.ccia_maids_inner,
    ]
    cc_start_region = create_region(world, player, active_locations, LocationName.castle_center,
                                    cc_start_region_locations, None)

    cc_tc_region_locations = [
        LocationName.ccb_mandrag_shelf
    ]
    cc_tc_region = create_region(world, player, active_locations, LocationName.cc_torture_chamber,
                                 cc_tc_region_locations, None)

    cc_library_region_locations = [
        LocationName.ccll_cwhall_wall
    ]
    cc_library_region = create_region(world, player, active_locations, LocationName.cc_library,
                                      cc_library_region_locations, None)

    cc_end_region = create_region(world, player, active_locations, LocationName.cc_elev_top, None, None)

    dt_region_locations = [
        LocationName.dt_stones_start,
        LocationName.dt_werebull_arena,
        LocationName.dt_ibridge_l,
        LocationName.dt_ibridge_r,
    ]
    dt_region = create_region(world, player, active_locations, LocationName.duel_tower,
                              dt_region_locations, None)

    toe_start_region_locations = [
        LocationName.toe_midsavespikes_r,
        LocationName.toe_midsavespikes_l,
        LocationName.toe_elec_grate,
        LocationName.toe_ibridge,
        LocationName.toe_top,
    ]
    toe_start_region = create_region(world, player, active_locations, LocationName.tower_of_execution,
                                     toe_start_region_locations, None)

    toe_gate_region_locations = [
        LocationName.toe_keygate_l
    ]
    toe_gate_region = create_region(world, player, active_locations, LocationName.toe_ledge,
                                    toe_gate_region_locations, None)

    tosci_start_region_locations = [
        LocationName.tosci_elevator,
        LocationName.tosci_plain_sr,
        LocationName.tosci_stairs_sr,
    ]
    tosci_start_region = create_region(world, player, active_locations, LocationName.tower_of_science,
                                       tosci_start_region_locations, None)

    tosci_door_hall_region_locations = [
        LocationName.tosci_three_door_hall,
    ]
    tosci_door_hall_region = create_region(world, player, active_locations, LocationName.tosci_key2,
                                           tosci_door_hall_region_locations, None)

    tosci_end_region_locations = [
        LocationName.tosci_ibridge_t,
        LocationName.tosci_conveyor_sr,
        LocationName.tosci_exit,
    ]
    tosci_end_region = create_region(world, player, active_locations, LocationName.tosci_conveyors,
                                     tosci_end_region_locations, None)

    tosci_key3_room_region_locations = [
        LocationName.tosci_key3_r,
        LocationName.tosci_key3_l,
    ]
    tosci_key3_room_region = create_region(world, player, active_locations, LocationName.tosci_key3,
                                       tosci_key3_room_region_locations, None)

    tosor_region_locations = [
        LocationName.tosor_stained_tower,
        LocationName.tosor_savepoint,
        LocationName.tosor_trickshot,
        LocationName.tosor_yellow_bubble,
        LocationName.tosor_blue_platforms,
        LocationName.tosor_side_isle,
        LocationName.tosor_ibridge,
    ]
    tosor_region = create_region(world, player, active_locations, LocationName.tower_of_sorcery,
                                 tosor_region_locations, None)

    roc_region_locations = [
        LocationName.roc_ent_l,
        LocationName.roc_gs_r,
        LocationName.roc_ent_r,
    ]
    roc_region = create_region(world, player, active_locations, LocationName.room_of_clocks,
                               roc_region_locations, None)

    ct_start_region_locations = [
        LocationName.ct_gearclimb_side,
        LocationName.ct_gearclimb_mid,
    ]
    ct_start_region = create_region(world, player, active_locations, LocationName.clock_tower,
                                    ct_start_region_locations, None)

    ct_mid_region = create_region(world, player, active_locations, LocationName.ct_middle, None, None)

    ct_end_region_locations = [
        LocationName.ct_finalroom_platform
    ]
    ct_end_region = create_region(world, player, active_locations, LocationName.ct_end,
                                    ct_end_region_locations, None)

    ck_region_locations = [
        LocationName.ck_behind_drac,
        LocationName.ck_cube,
    ]
    ck_region = create_region(world, player, active_locations, LocationName.castle_keep,
                                    ck_region_locations, None)

    drac_chamber_region_locations = [
        LocationName.the_end
    ]
    drac_chamber_region = create_region(world, player, active_locations, LocationName.drac_chamber,
                                        drac_chamber_region_locations, None)

    # Set up the regions correctly.
    world.regions += [
        menu_region,
        warp2_region,
        warp3_region,
        warp4_region,
        warp5_region,
        warp6_region,
        warp7_region,
        warp8_region,
        forest_start_region,
        cw_start_region,
        cw_ltower_region,
        villa_start_region,
        villa_storeroom_region,
        villa_archives_region,
        villa_maze_region,
        villa_crypt_region,
        tunnel_region,
        uw_start_region,
        uw_carrie_region,
        cc_start_region,
        cc_tc_region,
        cc_library_region,
        cc_end_region,
        dt_region,
        toe_start_region,
        toe_gate_region,
        tosci_start_region,
        tosci_door_hall_region,
        tosci_end_region,
        tosci_key3_room_region,
        tosor_region,
        roc_region,
        ct_start_region,
        ct_mid_region,
        ct_end_region,
        ck_region,
        drac_chamber_region,
    ]


def connect_regions(world, player):
    names: typing.Dict[str, int] = {}
    # connect(world, player, names, 'Menu', 'Warp 2',
    #         lambda state: (state.has(ItemName.special_two + 3, player)))

    connect(world, player, names, 'Menu', LocationName.forest_of_silence)

    connect(world, player, names, LocationName.forest_of_silence, LocationName.castle_wall)

    connect(world, player, names, LocationName.castle_wall, LocationName.cw_ltower,
            lambda state: (state.has(ItemName.left_tower_key, player)))

    connect(world, player, names, LocationName.castle_wall, LocationName.villa,
            lambda state: (state.has(ItemName.left_tower_key, player)))

    connect(world, player, names, LocationName.villa, LocationName.villa_storeroom,
            lambda state: (state.has(ItemName.storeroom_key, player)))

    connect(world, player, names, LocationName.villa, LocationName.villa_archives,
            lambda state: (state.has(ItemName.archives_key, player)))

    connect(world, player, names, LocationName.villa, LocationName.villa_maze_main,
            lambda state: (state.has(ItemName.garden_key, player)))

    connect(world, player, names, LocationName.villa_maze_main, LocationName.villa_crypt,
            lambda state: (state.has(ItemName.copper_key, player)))

    connect(world, player, names, LocationName.villa_crypt, LocationName.tunnel)
    connect(world, player, names, LocationName.villa_crypt, LocationName.underground_waterway)

    connect(world, player, names, LocationName.tunnel, LocationName.castle_center)

    connect(world, player, names, LocationName.underground_waterway, LocationName.castle_center)

    connect(world, player, names, LocationName.castle_center, LocationName.cc_torture_chamber,
            lambda state: (state.has(ItemName.chamber_key, player)))

    connect(world, player, names, LocationName.castle_center, LocationName.cc_library,
            lambda state: (state.has(ItemName.magical_nitro, player) and state.has(ItemName.mandragora, player)))

    connect(world, player, names, LocationName.castle_center, LocationName.cc_elev_top,
            lambda state: (state.has(ItemName.magical_nitro, player, 2) and state.has(ItemName.mandragora, player, 2)))

    connect(world, player, names, LocationName.cc_elev_top, LocationName.duel_tower)
    connect(world, player, names, LocationName.cc_elev_top, LocationName.tower_of_science)
    connect(world, player, names, LocationName.duel_tower, LocationName.tower_of_execution)

    connect(world, player, names, LocationName.tower_of_execution, LocationName.toe_ledge,
            lambda state: (state.has(ItemName.execution_key, player)))
    connect(world, player, names, LocationName.tower_of_execution, LocationName.room_of_clocks)

    connect(world, player, names, LocationName.tower_of_science, LocationName.tosci_key2,
            lambda state: (state.has(ItemName.science_key_one, player)))
    connect(world, player, names, LocationName.tower_of_science, LocationName.tosci_conveyors,
            lambda state: (state.has(ItemName.science_key_two, player)))
    connect(world, player, names, LocationName.tosci_conveyors, LocationName.tosci_key3,
            lambda state: (state.has(ItemName.science_key_three, player)))
    connect(world, player, names, LocationName.tosci_conveyors, LocationName.tower_of_sorcery)
    connect(world, player, names, LocationName.tower_of_sorcery, LocationName.room_of_clocks)
    connect(world, player, names, LocationName.room_of_clocks, LocationName.clock_tower)

    connect(world, player, names, LocationName.clock_tower, LocationName.ct_middle,
            lambda state: (state.has(ItemName.clocktower_key_one, player)))
    connect(world, player, names, LocationName.ct_middle, LocationName.ct_end,
            lambda state: (state.has(ItemName.clocktower_key_two, player)))
    connect(world, player, names, LocationName.ct_end, LocationName.castle_keep,
            lambda state: (state.has(ItemName.clocktower_key_three, player)))

    connect(world, player, names, LocationName.castle_keep, LocationName.drac_chamber)


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None, exits=None):
    # Shamelessly stolen from the SA2B definition, which was in turn shamelessly stolen from the ROR2 definition.
    # Perhaps one day the chain will continue?
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id:
                location = CV64Location(player, location, loc_id, ret)
                if loc_id != 0xC64000:
                    location.rom_offset = rom_loc_offsets[loc_id]
                ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


def connect(world: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

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
