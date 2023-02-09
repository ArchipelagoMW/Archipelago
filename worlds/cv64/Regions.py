import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import CV64Item
from .Locations import CV64Location, LocationData, all_locations
from .Names import ItemName, RegionName
from .Stages import CV64Stage, stage_dict


class RegionData(typing.NamedTuple):
    locations: typing.Optional[typing.List[str]]
    exits: typing.Optional[typing.List[str]]


shuffleable_stages = [
    RegionName.forest_of_silence,
    RegionName.castle_wall,
    RegionName.villa,
    RegionName.tunnel,
    RegionName.underground_waterway,
    RegionName.castle_center,
    RegionName.duel_tower,
    RegionName.tower_of_execution,
    RegionName.tower_of_science,
    RegionName.tower_of_sorcery,
    RegionName.room_of_clocks,
    RegionName.clock_tower,
]

region_list = [
    RegionName.menu,
    RegionName.warp1,
    RegionName.warp2,
    RegionName.warp3,
    RegionName.warp4,
    RegionName.warp5,
    RegionName.warp6,
    RegionName.warp7,
    RegionName.forest_start,
    RegionName.forest_mid,
    RegionName.forest_end,
    RegionName.cw_start,
    RegionName.cw_exit,
    RegionName.cw_ltower,
    RegionName.villa_start,
    RegionName.villa_main,
    RegionName.villa_storeroom,
    RegionName.villa_archives,
    RegionName.villa_maze,
    RegionName.villa_servants,
    RegionName.villa_crypt,
    RegionName.tunnel_start,
    RegionName.tunnel_end,
    RegionName.uw_main,
    RegionName.uw_end,
    RegionName.cc_main,
    RegionName.cc_crystal,
    RegionName.cc_torture_chamber,
    RegionName.cc_library,
    RegionName.cc_elev_top,
    RegionName.duel_tower,
    RegionName.toe_main,
    RegionName.toe_ledge,
    RegionName.tosci_start,
    RegionName.tosci_three_doors,
    RegionName.tosci_conveyors,
    RegionName.tosci_key3,
    RegionName.tower_of_sorcery,
    RegionName.room_of_clocks,
    RegionName.ct_start,
    RegionName.ct_middle,
    RegionName.ct_end,
    RegionName.castle_keep,
    RegionName.drac_chamber
]


def create_regions(multiworld, player: int, active_locations):
    location_lists = {}
    for name, data in active_locations.items():
        if data.region not in location_lists:
            location_lists[data.region] = []
        location_lists[data.region].append(name)

    # Set up the regions correctly
    for region in region_list:
        if region in location_lists:
            multiworld.regions.append(create_region(multiworld, player, active_locations, region, location_lists[region], None))
        else:
            multiworld.regions.append(create_region(multiworld, player, active_locations, region, None, None))


def connect_regions(world, player, active_stage_list, active_warp_list, required_special2s):
    names: typing.Dict[str, int] = {}

    connect(world, player, names, 'Menu', stage_dict[active_stage_list[0]].start_region_name)
    connect(world, player, names, 'Menu', 'Warp 1',
            lambda state: (state.has(ItemName.special_one, player, world.special1s_per_warp[player].value)))
    connect(world, player, names, 'Menu', 'Warp 2',
            lambda state: (state.has(ItemName.special_one, player, world.special1s_per_warp[player].value * 2)))
    connect(world, player, names, 'Menu', 'Warp 3',
            lambda state: (state.has(ItemName.special_one, player, world.special1s_per_warp[player].value * 3)))
    connect(world, player, names, 'Menu', 'Warp 4',
            lambda state: (state.has(ItemName.special_one, player, world.special1s_per_warp[player].value * 4)))
    connect(world, player, names, 'Menu', 'Warp 5',
            lambda state: (state.has(ItemName.special_one, player, world.special1s_per_warp[player].value * 5)))
    connect(world, player, names, 'Menu', 'Warp 6',
            lambda state: (state.has(ItemName.special_one, player, world.special1s_per_warp[player].value * 6)))
    connect(world, player, names, 'Menu', 'Warp 7',
            lambda state: (state.has(ItemName.special_one, player, world.special1s_per_warp[player].value * 7)))

    connect(world, player, names, 'Warp 1', stage_dict[active_warp_list[0]].mid_region_name)
    connect(world, player, names, 'Warp 2', stage_dict[active_warp_list[1]].mid_region_name)
    connect(world, player, names, 'Warp 3', stage_dict[active_warp_list[2]].mid_region_name)
    connect(world, player, names, 'Warp 4', stage_dict[active_warp_list[3]].mid_region_name)
    connect(world, player, names, 'Warp 5', stage_dict[active_warp_list[4]].mid_region_name)
    connect(world, player, names, 'Warp 6', stage_dict[active_warp_list[5]].mid_region_name)
    connect(world, player, names, 'Warp 7', stage_dict[active_warp_list[6]].mid_region_name)

    def get_next_stage_start(source_stage):
        if active_stage_list[active_stage_list.index(source_stage) - 1] == RegionName.villa:
            return stage_dict[active_stage_list[active_stage_list.index(source_stage) + 2]].start_region_name
        elif active_stage_list[active_stage_list.index(source_stage) - 2] == RegionName.castle_center:
            return stage_dict[active_stage_list[active_stage_list.index(source_stage) + 3]].start_region_name
        else:
            return stage_dict[active_stage_list[active_stage_list.index(source_stage) + 1]].start_region_name

    def get_prev_stage_end(source_stage):
        if active_stage_list.index(source_stage) - 1 >= 0:
            if active_stage_list[active_stage_list.index(source_stage) - 2] == RegionName.villa:
                return stage_dict[RegionName.villa].end_region_name
            elif active_stage_list[active_stage_list.index(source_stage) - 3] == RegionName.castle_center:
                return stage_dict[RegionName.castle_center].end_region_name
            elif active_stage_list[active_stage_list.index(source_stage) - 3] == RegionName.villa:
                return stage_dict[active_stage_list[active_stage_list.index(source_stage) - 2]].end_region_name
            elif active_stage_list[active_stage_list.index(source_stage) - 5] == RegionName.castle_center:
                return stage_dict[active_stage_list[active_stage_list.index(source_stage) - 3]].end_region_name
            else:
                return stage_dict[active_stage_list[active_stage_list.index(source_stage) - 1]].end_region_name
        else:
            return "Menu"
    # Forest connections
    connect(world, player, names, RegionName.forest_start, RegionName.forest_mid)
    connect(world, player, names, RegionName.forest_mid, RegionName.forest_end)
    connect(world, player, names, RegionName.forest_end, get_next_stage_start(RegionName.forest_of_silence))
    # Castle Wall connections
    connect(world, player, names, RegionName.cw_start, RegionName.cw_exit)
    if world.hard_logic[player]:
        connect(world, player, names, RegionName.cw_start, get_next_stage_start(RegionName.castle_wall))
    connect(world, player, names, RegionName.cw_start, RegionName.cw_ltower,
            lambda state: (state.has(ItemName.left_tower_key, player)))
    connect(world, player, names, RegionName.cw_ltower, get_next_stage_start(RegionName.castle_wall))
    # Villa connections
    connect(world, player, names, RegionName.villa_start, RegionName.villa_main)
    if world.hard_logic[player] and world.carrie_logic[player]:
        connect(world, player, names, RegionName.villa_main, RegionName.villa_start)
    connect(world, player, names, RegionName.villa_main, RegionName.villa_storeroom,
            lambda state: (state.has(ItemName.storeroom_key, player)))
    connect(world, player, names, RegionName.villa_storeroom, RegionName.villa_main,
            lambda state: (state.has(ItemName.storeroom_key, player)))
    connect(world, player, names, RegionName.villa_main, RegionName.villa_archives,
            lambda state: (state.has(ItemName.archives_key, player)))
    connect(world, player, names, RegionName.villa_main, RegionName.villa_maze,
            lambda state: (state.has(ItemName.garden_key, player)))
    connect(world, player, names, RegionName.villa_maze, RegionName.villa_servants,
            lambda state: (state.has(ItemName.garden_key, player)))
    connect(world, player, names, RegionName.villa_servants, RegionName.villa_main)
    if world.hard_logic[player]:
        connect(world, player, names, RegionName.villa_maze, RegionName.villa_crypt)
    else:
        connect(world, player, names, RegionName.villa_maze, RegionName.villa_crypt,
                lambda state: (state.has(ItemName.copper_key, player)))
    connect(world, player, names, RegionName.villa_crypt, RegionName.villa_maze)
    connect(world, player, names, RegionName.villa_crypt, stage_dict[active_stage_list[active_stage_list.index(RegionName.villa) + 1]].start_region_name)
    connect(world, player, names, RegionName.villa_crypt, stage_dict[active_stage_list[active_stage_list.index(RegionName.villa) + 2]].start_region_name)
    # Tunnel connections
    connect(world, player, names, RegionName.tunnel_start, RegionName.tunnel_end)
    connect(world, player, names, RegionName.tunnel_end, get_next_stage_start(RegionName.tunnel))
    # Waterway connections
    connect(world, player, names, RegionName.uw_main, RegionName.uw_end)
    if world.hard_logic[player]:
        connect(world, player, names, RegionName.uw_end, RegionName.uw_main)
    connect(world, player, names, RegionName.uw_end, get_next_stage_start(RegionName.underground_waterway))
    # Castle Center connections
    connect(world, player, names, RegionName.cc_main, RegionName.cc_torture_chamber,
            lambda state: (state.has(ItemName.chamber_key, player)))
    connect(world, player, names, RegionName.cc_main, RegionName.cc_crystal,
            lambda state: (state.has(ItemName.magical_nitro, player, 2) and state.has(ItemName.mandragora, player, 2)))
    connect(world, player, names, RegionName.cc_main, RegionName.cc_elev_top,
            lambda state: (state.has(ItemName.magical_nitro, player, 2) and state.has(ItemName.mandragora, player, 2)))
    # if world.hard_logic[player] and world.carrie_logic[player]:
    #     connect(world, player, names, RegionName.cc_main, RegionName.cc_library)
    # else: TODO: Confirm whether library jump is still RNG manipulable after picking up the items in the room or not.
    connect(world, player, names, RegionName.cc_main, RegionName.cc_library,
            lambda state: (state.has(ItemName.magical_nitro, player) and state.has(ItemName.mandragora, player)))
    connect(world, player, names, RegionName.cc_elev_top, stage_dict[active_stage_list[active_stage_list.index(RegionName.castle_center) + 1]].start_region_name)
    connect(world, player, names, RegionName.cc_elev_top, stage_dict[active_stage_list[active_stage_list.index(RegionName.castle_center) + 3]].start_region_name)
    # Duel Tower connections
    connect(world, player, names, RegionName.duel_tower, get_prev_stage_end(RegionName.duel_tower))
    connect(world, player, names, RegionName.duel_tower, get_next_stage_start(RegionName.duel_tower))
    # Tower of Execution connections
    connect(world, player, names, RegionName.toe_main, get_prev_stage_end(RegionName.tower_of_execution))
    if world.hard_logic[player]:
        connect(world, player, names, RegionName.toe_main, RegionName.toe_ledge)
    else:
        connect(world, player, names, RegionName.toe_main, RegionName.toe_ledge,
                lambda state: (state.has(ItemName.execution_key, player)))
    connect(world, player, names, RegionName.toe_main, get_next_stage_start(RegionName.tower_of_execution))
    # Tower of Science connections
    connect(world, player, names, RegionName.tosci_start, get_prev_stage_end(RegionName.tower_of_science))
    connect(world, player, names, RegionName.tosci_start, RegionName.tosci_three_doors,
            lambda state: (state.has(ItemName.science_key_one, player)))
    connect(world, player, names, RegionName.tosci_start, RegionName.tosci_conveyors,
            lambda state: (state.has(ItemName.science_key_two, player)))
    connect(world, player, names, RegionName.tosci_conveyors, RegionName.tosci_start,
            lambda state: (state.has(ItemName.science_key_two, player)))
    connect(world, player, names, RegionName.tosci_conveyors, RegionName.tosci_key3,
            lambda state: (state.has(ItemName.science_key_three, player)))
    connect(world, player, names, RegionName.tosci_conveyors, get_next_stage_start(RegionName.tower_of_science))
    # Tower of Sorcery connections
    connect(world, player, names, RegionName.tower_of_sorcery, get_prev_stage_end(RegionName.tower_of_sorcery))
    connect(world, player, names, RegionName.tower_of_sorcery, get_next_stage_start(RegionName.tower_of_sorcery))
    # Room of Clocks connection
    connect(world, player, names, RegionName.room_of_clocks, get_next_stage_start(RegionName.room_of_clocks))
    # Clock Tower connections
    connect(world, player, names, RegionName.ct_start, RegionName.ct_middle,
            lambda state: (state.has(ItemName.clocktower_key_one, player)))
    connect(world, player, names, RegionName.ct_middle, RegionName.ct_start,
            lambda state: (state.has(ItemName.clocktower_key_one, player)))
    connect(world, player, names, RegionName.ct_middle, RegionName.ct_end,
            lambda state: (state.has(ItemName.clocktower_key_two, player)))
    connect(world, player, names, RegionName.ct_end, RegionName.ct_middle,
            lambda state: (state.has(ItemName.clocktower_key_two, player)))
    connect(world, player, names, RegionName.ct_end, get_next_stage_start(RegionName.clock_tower),
            lambda state: (state.has(ItemName.clocktower_key_three, player)))
    # Castle Keep connections
    if world.hard_logic[player]:
        connect(world, player, names, RegionName.castle_keep, RegionName.room_of_clocks)
    connect(world, player, names, RegionName.castle_keep, RegionName.drac_chamber,
            lambda state: (state.has(ItemName.special_two, player, required_special2s)))


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None, exits=None):
    # Shamelessly stolen from the SA2B definition, which was in turn shamelessly stolen from the ROR2 definition.
    # Perhaps one day the chain will continue?
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_data = all_locations[location]
            loc_id = loc_data.code
            location = CV64Location(player, location, loc_id, ret)
            location.rom_offset = loc_data.rom_offset
            location.loc_type = loc_data.loc_type
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
