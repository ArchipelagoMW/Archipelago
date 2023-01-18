import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import ArcaneItem
from .Locations import ArcaneLocation
from .Names import LocationName, ItemName


def create_regions(world, player: int, active_locations, episode_ending_list):
    menu_region = create_region(world, player, active_locations, 'Menu', None, None)

    # S1E1 regions
    s1e1_start_region_location = [
        LocationName.s1e1_well,
        LocationName.s1e1_shed_wall
    ]
    s1e1_start_region = create_region(world, player, active_locations, LocationName.s1e1r_start,
                                      s1e1_start_region_location, None)

    s1e1_shed_region_locations = [
        LocationName.s1e1_shed_logs,
        LocationName.s1e1_keg
    ]
    if LocationName.s1e1_end in episode_ending_list:
        s1e1_shed_region_locations.append(LocationName.s1e1_end)
    s1e1_shed_region = create_region(world, player, active_locations, LocationName.s1e1r_shed,
                                     s1e1_shed_region_locations, None)

    # S1E2 regions
    s1e2_start_region_locations = [
        LocationName.s1e2_bedroom_drawer,
        LocationName.s1e2_bedroom_lamp
    ]
    s1e2_start_region = create_region(world, player, active_locations, LocationName.s1e2r_start,
                                      s1e2_start_region_locations, None)

    s1e2_wardrobe_region_locations = [
        LocationName.s1e2_alvin_1,
        LocationName.s1e2_alvin_2
    ]
    s1e2_wardrobe_region = create_region(world, player, active_locations, LocationName.s1e2r_wardrobe,
                                         s1e2_wardrobe_region_locations, None)

    s1e2_livingroom_region_locations = [
        LocationName.s1e2_idol_shelf
    ]
    if LocationName.s1e2_end in episode_ending_list:
        s1e2_livingroom_region_locations.append(LocationName.s1e2_end)
    s1e2_livingroom_region = create_region(world, player, active_locations, LocationName.s1e2r_livingroom,
                                           s1e2_livingroom_region_locations, None)

    # S1E3 regions
    s1e3_start_region_locations = [
        LocationName.s1e3_seth_cover,
        LocationName.s1e3_globe,
        LocationName.s1e3_shelf,
        LocationName.s1e3_table,
        LocationName.s1e3_chandelier
    ]
    s1e3_start_region = create_region(world, player, active_locations, LocationName.s1e3r_start,
                                      s1e3_start_region_locations, None)

    s1e3_elevator_region_locations = [
        LocationName.s1e3_elevator,
        LocationName.s1e3_lever
    ]
    if LocationName.s1e3_end in episode_ending_list:
        s1e3_elevator_region_locations.append(LocationName.s1e3_end)
    s1e3_elevator_region = create_region(world, player, active_locations, LocationName.s1e3r_elevator,
                                         s1e3_elevator_region_locations, None)

    # S1E4 regions
    s1e4_start_region_locations = [
        LocationName.s1e4_waves
    ]
    s1e4_start_region = create_region(world, player, active_locations, LocationName.s1e4r_start,
                                      s1e4_start_region_locations, None)

    s1e4_range_region_locations = [
        LocationName.s1e4_chest,
        LocationName.s1e4_bottle
    ]
    s1e4_range_region = create_region(world, player, active_locations, LocationName.s1e4r_range,
                                      s1e4_range_region_locations, None)

    s1e4_stone_region_locations = [
        LocationName.s1e4_stone,
    ]
    if LocationName.s1e4_end in episode_ending_list:
        s1e4_stone_region_locations.append(LocationName.s1e4_end)
    s1e4_stone_region = create_region(world, player, active_locations, LocationName.s1e4r_stone,
                                      s1e4_stone_region_locations, None)

    # S2E1 regions
    s2e1_start_region_locations = [
        LocationName.s2e1_hobo
    ]
    s2e1_start_region = create_region(world, player, active_locations, LocationName.s2e1r_start,
                                      s2e1_start_region_locations, None)

    s2e1_warehouse_region_locations = [
        LocationName.s2e1_crane,
        LocationName.s2e1_exit,
        LocationName.s2e1_box1,
        LocationName.s2e1_box2,
        LocationName.s2e1_box3
    ]
    s2e1_warehouse_region = create_region(world, player, active_locations, LocationName.s2e1r_warehouse,
                                          s2e1_warehouse_region_locations, None)

    s2e1_alicia_region_locations = [
        LocationName.s2e1_table,
        LocationName.s2e1_phonograph,
        LocationName.s2e1_hole,
        LocationName.s2e1_message
    ]
    if LocationName.s2e1_end in episode_ending_list:
        s2e1_alicia_region_locations.append(LocationName.s2e1_end)
    s2e1_alicia_region = create_region(world, player, active_locations, LocationName.s2e1r_alicia,
                                       s2e1_alicia_region_locations, None)

    # S2E2 regions
    s2e2_start_region_locations = [
        LocationName.s2e2_violin,
        LocationName.s2e2_drawer,
        LocationName.s2e2_painting,
        LocationName.s2e2_guy,
        LocationName.s2e2_closet
    ]
    s2e2_start_region = create_region(world, player, active_locations, LocationName.s2e2r_start,
                                      s2e2_start_region_locations, None)

    s2e2_catacombs_region_locations = [
        LocationName.s2e2_hand_box
    ]
    if LocationName.s2e2_end in episode_ending_list:
        s2e2_catacombs_region_locations.append(LocationName.s2e2_end)
    s2e2_catacombs_region = create_region(world, player, active_locations, LocationName.s2e2r_catacombs,
                                          s2e2_catacombs_region_locations, None)

    # S2E3 locations
    s2e3_start_region_locations = [
        LocationName.s2e3_doorway,
        LocationName.s2e3_bench,
        LocationName.s2e3_closet
    ]
    s2e3_start_region = create_region(world, player, active_locations, LocationName.s2e3r_start,
                                      s2e3_start_region_locations, None)

    s2e3_udeck_region_locations = [
        LocationName.s2e3_reel,
        LocationName.s2e3_platform,
        LocationName.s2e3_bag
    ]
    s2e3_udeck_region = create_region(world, player, active_locations, LocationName.s2e3r_udeck,
                                      s2e3_udeck_region_locations, None)

    s2e3_ldeck_region_location = [
        LocationName.s2e3_leg_box
    ]
    s2e3_ldeck_region = create_region(world, player, active_locations, LocationName.s2e3r_ldeck,
                                      s2e3_ldeck_region_location, None)

    s2e3_dinghy_region_locations = [
        LocationName.s2e3_dinghy,
    ]
    if LocationName.s2e3_end in episode_ending_list:
        s2e3_dinghy_region_locations.append(LocationName.s2e3_end)
    s2e3_dinghy_region = create_region(world, player, active_locations, LocationName.s2e3r_dinghy,
                                       s2e3_dinghy_region_locations, None)

    # S2E4 regions
    s2e4_start_region_locations = [
        LocationName.s2e4_barn_bag,
        LocationName.s2e4_stand1,
        LocationName.s2e4_stand2
    ]
    s2e4_start_region = create_region(world, player, active_locations, LocationName.s2e4r_start,
                                      s2e4_start_region_locations, None)

    s2e4_cabins_region_location = [
        LocationName.s2e4_cabin_bag
    ]
    s2e4_cabins_region = create_region(world, player, active_locations, LocationName.s2e4r_cabins,
                                       s2e4_cabins_region_location, None)

    s2e4_safe_region_locations = [
        LocationName.s2e4_safe1,
        LocationName.s2e4_safe2,
        LocationName.s2e4_safe3
    ]
    s2e4_safe_region = create_region(world, player, active_locations, LocationName.s2e4r_safe,
                                     s2e4_safe_region_locations, None)

    s2e4_armored_car_region_locations = [
        LocationName.s2e4_chair,
        LocationName.s2e4_on_statue,
        LocationName.s2e4_in_statue_l,
        LocationName.s2e4_in_statue_r
    ]
    s2e4_armored_car_region = create_region(world, player, active_locations, LocationName.s2e4r_armored_car,
                                            s2e4_armored_car_region_locations, None)

    s2e4_roof_region_locations = [
        LocationName.s2e4_barnstable
    ]
    if LocationName.s2e4_end in episode_ending_list:
        s2e4_roof_region_locations.append(LocationName.s2e4_end)
    s2e4_roof_region = create_region(world, player, active_locations, LocationName.s2e4r_rooftop,
                                     s2e4_roof_region_locations, None)

    # S2E5 regions
    s2e5_start_region_locations = [
        LocationName.s2e5_smith,
        LocationName.s2e5_gondola,
        LocationName.s2e5_armadillo,
        LocationName.s2e5_w11,
        LocationName.s2e5_helmet,
        LocationName.s2e5_aztec
    ]
    s2e5_start_region = create_region(world, player, active_locations, LocationName.s2e5r_start,
                                      s2e5_start_region_locations, None)

    s2e5_model_region_locations = [
        LocationName.s2e5_model
    ]
    if LocationName.s2e5_end in episode_ending_list:
        s2e5_model_region_locations.append(LocationName.s2e5_end)
    s2e5_model_region = create_region(world, player, active_locations, LocationName.s2e5r_model,
                                      s2e5_model_region_locations, None)

    # S2E6 regions
    s2e6_start_region_locations = [
        LocationName.s2e6_urn_ped,
        LocationName.s2e6_vonarburg,
        LocationName.s2e6_on_fireplace
    ]
    s2e6_start_region = create_region(world, player, active_locations, LocationName.s2e6r_start,
                                      s2e6_start_region_locations, None)

    s2e6_warp_region_locations = [
        LocationName.s2e6_mom,
        LocationName.s2e6_in_fireplace,
        LocationName.s2e6_monk,
        LocationName.s2e6_cardinal,
        LocationName.s2e6_ashes
    ]
    s2e6_warp_region = create_region(world, player, active_locations, LocationName.s2e6r_warp,
                                     s2e6_warp_region_locations, None)

    s2e6_ages_region_locations = [
        LocationName.s2e6_paradox
    ]
    if LocationName.s2e6_end in episode_ending_list:
        s2e6_ages_region_locations.append(LocationName.s2e6_end)
    s2e6_ages_region = create_region(world, player, active_locations, LocationName.s2e6r_ages,
                                     s2e6_ages_region_locations, None)

    # S2E7 regions
    s2e7_start_region_locations = [
        LocationName.s2e7_bentley,
        LocationName.s2e7_perch
    ]
    s2e7_start_region = create_region(world, player, active_locations, LocationName.s2e7r_start,
                                      s2e7_start_region_locations, None)

    s2e7_bridge_region_location = [
        LocationName.s2e7_bridge
    ]
    s2e7_bridge_region = create_region(world, player, active_locations, LocationName.s2e7r_bridge,
                                       s2e7_bridge_region_location, None)

    s2e7_crypt_region_locations = [
        LocationName.s2e7_rcoffin1,
        LocationName.s2e7_rcoffin2,
        LocationName.s2e7_rcoffin3,
        LocationName.s2e7_lcoffin,
    ]
    s2e7_crypt_region = create_region(world, player, active_locations, LocationName.s2e7r_crypt,
                                      s2e7_crypt_region_locations, None)

    s2e7_alcove_region_locations = [
        LocationName.s2e7_eyes
    ]
    if LocationName.s2e7_end in episode_ending_list:
        s2e7_alcove_region_locations.append(LocationName.s2e7_end)
    s2e7_alcove_region = create_region(world, player, active_locations, LocationName.s2e7r_alcove,
                                       s2e7_alcove_region_locations, None)

    # S2E8 regions
    s2e8_start_region_locations = [
        LocationName.s2e8_trunk1,
        LocationName.s2e8_trunk2,
        LocationName.s2e8_ground
    ]
    s2e8_start_region = create_region(world, player, active_locations, LocationName.s2e8r_start,
                                      s2e8_start_region_locations, None)

    s2e8_pu_region_locations = [
        LocationName.s2e8_pu_l,
        LocationName.s2e8_pu_r
    ]
    s2e8_pu_region = create_region(world, player, active_locations, LocationName.s2e8r_pu,
                                   s2e8_pu_region_locations, None)

    s2e8_sn_region_locations = [
        LocationName.s2e8_sn
    ]
    if LocationName.s2e8_end in episode_ending_list:
        s2e8_sn_region_locations.append(LocationName.s2e8_end)
    s2e8_sn_region = create_region(world, player, active_locations, LocationName.s2e8r_sn,
                                   s2e8_sn_region_locations, None)

    # Set up the regions correctly.
    world.regions += [
        menu_region,
        # S1E1
        s1e1_start_region,
        s1e1_shed_region,
        # S1E2
        s1e2_start_region,
        s1e2_wardrobe_region,
        s1e2_livingroom_region,
        # S1E3
        s1e3_start_region,
        s1e3_elevator_region,
        # S1E4
        s1e4_start_region,
        s1e4_range_region,
        s1e4_stone_region,
        # S2E1
        s2e1_start_region,
        s2e1_warehouse_region,
        s2e1_alicia_region,
        # S2E2
        s2e2_start_region,
        s2e2_catacombs_region,
        # S2E3
        s2e3_start_region,
        s2e3_udeck_region,
        s2e3_ldeck_region,
        s2e3_dinghy_region,
        # S2E4
        s2e4_start_region,
        s2e4_cabins_region,
        s2e4_safe_region,
        s2e4_armored_car_region,
        s2e4_roof_region,
        # S2E5
        s2e5_start_region,
        s2e5_model_region,
        # S2E6
        s2e6_start_region,
        s2e6_warp_region,
        s2e6_ages_region,
        # S2E7
        s2e7_start_region,
        s2e7_bridge_region,
        s2e7_crypt_region,
        s2e7_alcove_region,
        # S2E8
        s2e8_start_region,
        s2e8_pu_region,
        s2e8_sn_region
    ]


def connect_regions(world, player):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, 'Menu', LocationName.s1e1r_start)
    connect(world, player, names, 'Menu', LocationName.s1e2r_start)
    connect(world, player, names, 'Menu', LocationName.s1e3r_start)
    connect(world, player, names, 'Menu', LocationName.s1e4r_start)
    connect(world, player, names, 'Menu', LocationName.s2e1r_start)
    connect(world, player, names, 'Menu', LocationName.s2e2r_start)
    connect(world, player, names, 'Menu', LocationName.s2e3r_start)
    connect(world, player, names, 'Menu', LocationName.s2e4r_start)
    connect(world, player, names, 'Menu', LocationName.s2e5r_start)
    connect(world, player, names, 'Menu', LocationName.s2e6r_start)
    connect(world, player, names, 'Menu', LocationName.s2e7r_start)
    connect(world, player, names, 'Menu', LocationName.s2e8r_start)

    # S1E1 connection
    connect(world, player, names, LocationName.s1e1r_start, LocationName.s1e1r_shed,
            lambda state: (state.has(ItemName.s1e1_matches, player)))
    # S1E2 connections
    connect(world, player, names, LocationName.s1e2r_start, LocationName.s1e2r_wardrobe,
            lambda state: (state.has(ItemName.s1e2_key, player)))
    connect(world, player, names, LocationName.s1e2r_start, LocationName.s1e2r_livingroom,
            lambda state: (state.has(ItemName.s1e2_newspaper, player) and state.has(ItemName.dagger, player)))
    # S1E3 connection
    connect(world, player, names, LocationName.s1e3r_start, LocationName.s1e3r_elevator,
            lambda state: (state.has(ItemName.s1e3_diamond, player, 2) and state.has(ItemName.s1e3_candelabra, player)))
    # S1E4 connections
    connect(world, player, names, LocationName.s1e4r_start, LocationName.s1e4r_range,
            lambda state: (state.has(ItemName.s1e4_ladder, player)))
    connect(world, player, names, LocationName.s1e4r_range, LocationName.s1e4r_stone,
            lambda state: (state.has(ItemName.s1e4_gun, player) and state.has(ItemName.note_l, player)
                           and state.has(ItemName.note_r, player) and state.has(ItemName.seth, player)
                           and state.has(ItemName.dagger, player) and state.has(ItemName.idol, player)))
    # S2E1 connections
    connect(world, player, names, LocationName.s2e1r_start, LocationName.s2e1r_warehouse,
            lambda state: (state.has(ItemName.s2e1_pallet, player) and state.has(ItemName.ibinoculars, player)))
    connect(world, player, names, LocationName.s2e1r_start, LocationName.s2e1r_alicia,
            lambda state: (state.has(ItemName.s2e1_wrench, player) and state.has(ItemName.s2e1_crowbar, player)
                           and state.has(ItemName.ibinoculars, player)))
    # S2E2 connection
    connect(world, player, names, LocationName.s2e2r_start, LocationName.s2e2r_catacombs,
            lambda state: (state.has(ItemName.s2e2_handle, player) and state.has(ItemName.s2e2_key, player) and
                           state.has(ItemName.s2e2_candelabra, player) and state.has(ItemName.s2e2_lighter, player)))
    # S2E3 connections
    connect(world, player, names, LocationName.s2e3r_start, LocationName.s2e3r_udeck,
            lambda state: (state.has(ItemName.s2e3_hammer, player)))
    connect(world, player, names, LocationName.s2e3r_udeck, LocationName.s2e3r_ldeck,
            lambda state: (state.has(ItemName.s2e3_helmet, player) and state.has(ItemName.s2e3_cleaner, player)
                           and state.has(ItemName.ibinoculars, player)))
    connect(world, player, names, LocationName.s2e3r_udeck, LocationName.s2e3r_dinghy,
            lambda state: (state.has(ItemName.s2e3_oars, player) and state.has(ItemName.legs, player)
                           and state.has(ItemName.ibinoculars, player)))
    # S2E4 connections
    connect(world, player, names, LocationName.s2e4r_start, LocationName.s2e4r_cabins,
            lambda state: (state.has(ItemName.s2e4_bottle, player)))
    connect(world, player, names, LocationName.s2e4r_cabins, LocationName.s2e4r_safe,
            lambda state: (state.has(ItemName.s2e4_stethoscope, player)))
    connect(world, player, names, LocationName.s2e4r_start, LocationName.s2e4r_armored_car,
            lambda state: (state.has(ItemName.s2e4_frog, player)))
    connect(world, player, names, LocationName.s2e4r_armored_car, LocationName.s2e4r_rooftop,
            lambda state: (state.has(ItemName.s2e4_matches, player) and state.has(ItemName.s2e4_matches, player)
                           and state.has(ItemName.s2e4_bucket, player) and state.has(ItemName.s2e4_ruby, player)
                           and state.has(ItemName.s2e4_alazif, player) and state.has(ItemName.s2e4_amulet, player)))
    # S2E5 connection
    connect(world, player, names, LocationName.s2e5r_start, LocationName.s2e5r_model,
            lambda state: (state.has(ItemName.s2e5_book, player) and state.has(ItemName.s2e5_slice, player, 4)))
    # S2E6 connections
    connect(world, player, names, LocationName.s2e6r_start, LocationName.s2e6r_warp,
            lambda state: (state.has(ItemName.s2e6_circlet, player)))
    connect(world, player, names, LocationName.s2e6r_warp, LocationName.s2e6r_ages,
            lambda state: (state.has(ItemName.s2e6_urn, player, 2) and state.has(ItemName.s2e6_card, player, 3)
                           and state.has(ItemName.s2e6_book, player)))
    # S2E7 connections
    connect(world, player, names, LocationName.s2e7r_start, LocationName.s2e7r_bridge,
            lambda state: (state.has(ItemName.s2e7_bird, player)))
    connect(world, player, names, LocationName.s2e7r_bridge, LocationName.s2e7r_crypt,
            lambda state: (state.has(ItemName.s2e7_cross, player)))
    connect(world, player, names, LocationName.s2e7r_crypt, LocationName.s2e7r_alcove,
            lambda state: (state.has(ItemName.ibinoculars, player) and state.has(ItemName.s2e7_arrows, player)
                           and state.has(ItemName.s2e7_rope, player) and state.has(ItemName.s2e7_crossbow, player)
                           and state.has(ItemName.yhe, player)))
    # S2E8 connections
    connect(world, player, names, LocationName.s2e8r_start, LocationName.s2e8r_pu,
            lambda state: (state.has(ItemName.ibinoculars, player) and state.has(ItemName.s2e8_towhook, player)
                           and state.has(ItemName.s2e8_shovel, player) and state.has(ItemName.s2e8_chalk, player)))
    connect(world, player, names, LocationName.s2e8r_pu, LocationName.s2e8r_sn,
            lambda state: (state.has(ItemName.wing, player, 2) and state.has(ItemName.heart, player)
                           and state.has(ItemName.legs, player) and state.has(ItemName.hand, player, 2)
                           and state.has(ItemName.eyes, player) and state.has(ItemName.s2e8_slab_c, player)
                           and state.has(ItemName.s2e8_slab_s, player) and state.has(ItemName.yhe, player)))


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None, exits=None):
    # Shamelessly stolen from the SA2B definition, which was in turn shamelessly stolen from the ROR2 definition.
    # Perhaps one day the chain will continue?
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            location = ArcaneLocation(player, location, loc_id, ret)
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
