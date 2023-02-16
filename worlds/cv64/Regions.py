import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import CV64Item
from .Locations import CV64Location, LocationData, all_locations
from .Names import ItemName, RegionName
from .Stages import CV64Stage, stage_dict

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


def create_regions(multiworld, player: int, active_locations, active_stage_list, active_warp_list, required_special2s):
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

    class EntranceData(typing.NamedTuple):
        stage: typing.Optional[str]
        target_region: str
        rule: typing.Optional[typing.Callable]
        easy_rule: bool = False
        hard_entrance: bool = False
        carrie_entrance: bool = False

    exits_lists = {
        # Menus
        RegionName.menu:
            [EntranceData(None, stage_dict[active_stage_list[0]].start_region_name, None),
             EntranceData(None, RegionName.warp1,
                          lambda state: (
                              state.has(ItemName.special_one, player, multiworld.special1s_per_warp[player].value))),
             EntranceData(None, RegionName.warp2,
                          lambda state: (state.has(ItemName.special_one, player,
                                                   multiworld.special1s_per_warp[player].value * 2))),
             EntranceData(None, RegionName.warp3,
                          lambda state: (state.has(ItemName.special_one, player,
                                                   multiworld.special1s_per_warp[player].value * 3))),
             EntranceData(None, RegionName.warp4,
                          lambda state: (state.has(ItemName.special_one, player,
                                                   multiworld.special1s_per_warp[player].value * 4))),
             EntranceData(None, RegionName.warp5,
                          lambda state: (state.has(ItemName.special_one, player,
                                                   multiworld.special1s_per_warp[player].value * 5))),
             EntranceData(None, RegionName.warp6,
                          lambda state: (state.has(ItemName.special_one, player,
                                                   multiworld.special1s_per_warp[player].value * 6))),
             EntranceData(None, RegionName.warp7,
                          lambda state: (state.has(ItemName.special_one, player,
                                                   multiworld.special1s_per_warp[player].value * 7)))],
        RegionName.warp1:
            [EntranceData(None, active_warp_list[0], None)],
        RegionName.warp2:
            [EntranceData(None, active_warp_list[1], None)],
        RegionName.warp3:
            [EntranceData(None, active_warp_list[2], None)],
        RegionName.warp4:
            [EntranceData(None, active_warp_list[3], None)],
        RegionName.warp5:
            [EntranceData(None, active_warp_list[4], None)],
        RegionName.warp6:
            [EntranceData(None, active_warp_list[5], None)],
        RegionName.warp7:
            [EntranceData(None, active_warp_list[6], None)],
        # Forest of Silence
        RegionName.forest_start:
            [EntranceData(RegionName.forest_of_silence, RegionName.forest_mid, None)],
        RegionName.forest_mid:
            [EntranceData(RegionName.forest_of_silence, RegionName.forest_end, None)],
        RegionName.forest_end:
            [EntranceData(RegionName.forest_of_silence, get_next_stage_start(RegionName.forest_of_silence), None)],
        # Castle Wall
        RegionName.cw_start:
            [EntranceData(RegionName.castle_wall, RegionName.cw_exit, None),
             EntranceData(RegionName.castle_wall, get_next_stage_start(RegionName.castle_wall), None,
                          hard_entrance=True),
             EntranceData(RegionName.castle_wall, RegionName.cw_ltower,
                          lambda state: (state.has(ItemName.left_tower_key, player)))],
        RegionName.cw_ltower:
            [EntranceData(RegionName.castle_wall, get_next_stage_start(RegionName.castle_wall), None)],
        # Villa
        RegionName.villa_start:
            [EntranceData(RegionName.villa, RegionName.villa_main, None)],
        RegionName.villa_main:
            [EntranceData(RegionName.villa, RegionName.villa_start, None, hard_entrance=True, carrie_entrance=True),
             EntranceData(RegionName.villa, RegionName.villa_storeroom,
                          lambda state: (state.has(ItemName.storeroom_key, player))),
             EntranceData(RegionName.villa, RegionName.villa_archives,
                          lambda state: (state.has(ItemName.archives_key, player))),
             EntranceData(RegionName.villa, RegionName.villa_maze,
                          lambda state: (state.has(ItemName.garden_key, player)))],
        RegionName.villa_storeroom:
            [EntranceData(RegionName.villa, RegionName.villa_main,
                          lambda state: (state.has(ItemName.storeroom_key, player)))],
        RegionName.villa_maze:
            [EntranceData(RegionName.villa, RegionName.villa_servants,
                          lambda state: (state.has(ItemName.garden_key, player))),
             EntranceData(RegionName.villa, RegionName.villa_crypt,
                          lambda state: (state.has(ItemName.copper_key, player)), easy_rule=True)],
        RegionName.villa_servants:
            [EntranceData(RegionName.villa, RegionName.villa_main,
                          lambda state: (state.has(ItemName.garden_key, player)))],
        RegionName.villa_crypt:
            [EntranceData(RegionName.villa, RegionName.villa_maze, None),
             EntranceData(RegionName.villa,
                          stage_dict[
                              active_stage_list[active_stage_list.index(RegionName.villa) + 1]].start_region_name,
                          None),
             EntranceData(RegionName.villa,
                          stage_dict[
                              active_stage_list[active_stage_list.index(RegionName.villa) + 2]].start_region_name,
                          None)],
        # Tunnel
        RegionName.tunnel_start:
            [EntranceData(RegionName.tunnel, RegionName.tunnel_end, None)],
        RegionName.tunnel_end:
            [EntranceData(RegionName.tunnel, get_next_stage_start(RegionName.tunnel), None)],
        # Underground Waterway
        RegionName.uw_main:
            [EntranceData(RegionName.underground_waterway, RegionName.uw_end, None)],
        RegionName.uw_end:
            [EntranceData(RegionName.underground_waterway, RegionName.uw_main, None, hard_entrance=True),
             EntranceData(RegionName.underground_waterway, get_next_stage_start(RegionName.underground_waterway),
                          None)],
        # Castle Center
        RegionName.cc_main:
            [EntranceData(RegionName.castle_center, RegionName.cc_torture_chamber,
                          lambda state: (state.has(ItemName.chamber_key, player))),
             EntranceData(RegionName.castle_center, RegionName.cc_library,
                          lambda state: (state.has(ItemName.magical_nitro, player) and
                                         state.has(ItemName.mandragora, player))),
             EntranceData(RegionName.castle_center, RegionName.cc_crystal,
                          lambda state: (state.has(ItemName.magical_nitro, player, 2) and
                                         state.has(ItemName.mandragora, player, 2)))],
        RegionName.cc_crystal:
            [EntranceData(RegionName.castle_center, RegionName.cc_elev_top, None)],
        RegionName.cc_elev_top:
            [EntranceData(RegionName.castle_center,
                          stage_dict[active_stage_list[
                              active_stage_list.index(RegionName.castle_center) + 1]].start_region_name, None),
             EntranceData(RegionName.castle_center,
                          stage_dict[active_stage_list[
                              active_stage_list.index(RegionName.castle_center) + 3]].start_region_name, None)],
        # Duel Tower
        RegionName.duel_tower:
            [EntranceData(RegionName.duel_tower, get_prev_stage_end(RegionName.duel_tower), None),
             EntranceData(RegionName.duel_tower, get_next_stage_start(RegionName.duel_tower), None)],
        # Tower of Execution
        RegionName.toe_main:
            [EntranceData(RegionName.tower_of_execution, get_prev_stage_end(RegionName.tower_of_execution), None),
             EntranceData(RegionName.tower_of_execution, RegionName.toe_ledge,
                          lambda state: (state.has(ItemName.execution_key, player)), easy_rule=True),
             EntranceData(RegionName.tower_of_execution, get_next_stage_start(RegionName.tower_of_execution), None)],
        # Tower of Science
        RegionName.tosci_start:
            [EntranceData(RegionName.tower_of_science, get_prev_stage_end(RegionName.tower_of_science), None),
             EntranceData(RegionName.tower_of_science, RegionName.tosci_three_doors,
                          lambda state: (state.has(ItemName.science_key_one, player))),
             EntranceData(RegionName.tower_of_science, RegionName.tosci_conveyors,
                          lambda state: (state.has(ItemName.science_key_two, player)))],
        RegionName.tosci_conveyors:
            [EntranceData(RegionName.tower_of_science, RegionName.tosci_start,
                          lambda state: (state.has(ItemName.science_key_two, player))),
             EntranceData(RegionName.tower_of_science, RegionName.tosci_key3,
                          lambda state: (state.has(ItemName.science_key_three, player))),
             EntranceData(RegionName.tower_of_science, get_next_stage_start(RegionName.tower_of_science), None)],
        # Tower of Sorcery
        RegionName.tower_of_sorcery:
            [EntranceData(RegionName.tower_of_sorcery, get_prev_stage_end(RegionName.tower_of_sorcery), None),
             EntranceData(RegionName.tower_of_sorcery, get_next_stage_start(RegionName.tower_of_sorcery), None)],
        # Room of Clocks
        RegionName.room_of_clocks:
            [EntranceData(RegionName.room_of_clocks, get_next_stage_start(RegionName.room_of_clocks), None)],
        # Clock Tower
        RegionName.ct_start:
            [EntranceData(RegionName.clock_tower, RegionName.ct_middle,
                          lambda state: (state.has(ItemName.clocktower_key_one, player)))],
        RegionName.ct_middle:
            [EntranceData(RegionName.clock_tower, RegionName.ct_start,
                          lambda state: (state.has(ItemName.clocktower_key_one, player))),
             EntranceData(RegionName.clock_tower, RegionName.ct_end,
                          lambda state: (state.has(ItemName.clocktower_key_two, player)))],
        RegionName.ct_end:
            [EntranceData(RegionName.clock_tower, RegionName.ct_middle,
                          lambda state: (state.has(ItemName.clocktower_key_two, player))),
             EntranceData(RegionName.clock_tower, get_next_stage_start(RegionName.clock_tower),
                          lambda state: (state.has(ItemName.clocktower_key_three, player)))],
        # Castle Keep
        RegionName.castle_keep:
            [EntranceData(RegionName.castle_keep, RegionName.room_of_clocks, None, hard_entrance=True),
             EntranceData(RegionName.castle_keep, RegionName.drac_chamber,
                          lambda state: (state.has(ItemName.special_two, player, required_special2s)))]
    }

    location_lists = {}
    for name, data in active_locations.items():
        if data.region not in location_lists:
            location_lists[data.region] = []
        location_lists[data.region].append(name)

    # Set up the regions correctly
    created_regions = []
    for region in region_list:
        locations = None
        exits = None
        if region in location_lists:
            locations = location_lists[region]
        if region in exits_lists:
            exits = exits_lists[region]
        created_region = create_region(multiworld, player, region, locations, exits)
        created_regions.append(created_region)

    # Connect the regions correctly
    for region in created_regions:
        for entrance in region.exits:
            entrance.connect(created_regions[created_regions.index(entrance.name)], player)

    multiworld.regions.append(created_regions)


def create_region(world: MultiWorld, player: int, name: str, locations=None, entrances=None):
    # Shamelessly stolen from the SA2B definition which was, in turn, shamelessly stolen from the ROR2 definition.
    # Anyone feeling like continuing the chain?
    ret = Region(name, None, name, player)
    ret.world = world
    if locations and locations != []:
        for location in locations:
            loc_data = all_locations[location]
            loc_id = loc_data.code
            created_location = CV64Location(player, location, loc_id, ret, loc_data.rom_offset, loc_data.loc_type)
            ret.locations.append(created_location)
    if entrances:
        for data in entrances:
            if world.hard_logic or not data.hard_entrance:
                if world.carrie_logic or not data.carrie_entrance:
                    created_entrance = Entrance(player, data.target_region, ret)
                    if not world.hard_logic or not data.easy_rule:
                        created_entrance.access_rule = data.rule
                    else:
                        created_entrance.access_rule = None
                    ret.exits.append(created_entrance)

    return ret


def connect(world: MultiWorld, player: int, source: str, target: str, rule: typing.Optional[typing.Callable] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    connection = Entrance(player, target, source_region)

    if rule:
        connection.access_rule = rule

    connection.connect(target_region)
