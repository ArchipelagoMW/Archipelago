import typing

from BaseClasses import Entrance
from .Names import ItemName, RegionName
from .Stages import stage_dict


class EntranceData(typing.NamedTuple):
    parent_region: str
    target_region: str
    rule: typing.Optional[typing.Callable] = None
    easy_rule: bool = False
    hard_entrance: bool = False
    carrie_entrance: bool = False


def create_entrances(multiworld, player: int, active_stage_list, active_warp_list, required_special2s, active_regions):
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

    s1s_per_warp = multiworld.special1s_per_warp[player].value

    all_entrances = [
        EntranceData(RegionName.menu, stage_dict[active_stage_list[0]].start_region_name),
        EntranceData(RegionName.menu, RegionName.warp1,
                     lambda state: state.has(ItemName.special_one, player, s1s_per_warp)),
        EntranceData(RegionName.menu, RegionName.warp2,
                     lambda state: state.has(ItemName.special_one, player, s1s_per_warp * 2)),
        EntranceData(RegionName.menu, RegionName.warp3,
                     lambda state: state.has(ItemName.special_one, player, s1s_per_warp * 3)),
        EntranceData(RegionName.menu, RegionName.warp4,
                     lambda state: state.has(ItemName.special_one, player, s1s_per_warp * 4)),
        EntranceData(RegionName.menu, RegionName.warp5,
                     lambda state: state.has(ItemName.special_one, player, s1s_per_warp * 5)),
        EntranceData(RegionName.menu, RegionName.warp6,
                     lambda state: state.has(ItemName.special_one, player, s1s_per_warp * 6)),
        EntranceData(RegionName.menu, RegionName.warp7,
                     lambda state: state.has(ItemName.special_one, player, s1s_per_warp * 7)),
        EntranceData(RegionName.warp1, stage_dict[active_warp_list[0]].mid_region_name),
        EntranceData(RegionName.warp2, stage_dict[active_warp_list[1]].mid_region_name),
        EntranceData(RegionName.warp3, stage_dict[active_warp_list[2]].mid_region_name),
        EntranceData(RegionName.warp4, stage_dict[active_warp_list[3]].mid_region_name),
        EntranceData(RegionName.warp5, stage_dict[active_warp_list[4]].mid_region_name),
        EntranceData(RegionName.warp6, stage_dict[active_warp_list[5]].mid_region_name),
        EntranceData(RegionName.warp7, stage_dict[active_warp_list[6]].mid_region_name),
        # Forest of Silence
        EntranceData(RegionName.forest_start, RegionName.forest_mid),
        EntranceData(RegionName.forest_mid, RegionName.forest_end),
        EntranceData(RegionName.forest_end, get_next_stage_start(RegionName.forest_of_silence)),
        # Castle Wall
        EntranceData(RegionName.cw_start, RegionName.cw_exit),
        EntranceData(RegionName.cw_start, get_next_stage_start(RegionName.castle_wall), hard_entrance=True),
        EntranceData(RegionName.cw_start, RegionName.cw_ltower,
                     lambda state: state.has(ItemName.left_tower_key, player)),
        EntranceData(RegionName.cw_ltower, get_next_stage_start(RegionName.castle_wall)),
        # Villa
        EntranceData(RegionName.villa_start, RegionName.villa_main),
        EntranceData(RegionName.villa_main, RegionName.villa_start, hard_entrance=True, carrie_entrance=True),
        EntranceData(RegionName.villa_main, RegionName.villa_storeroom,
                     lambda state: state.has(ItemName.storeroom_key, player)),
        EntranceData(RegionName.villa_main, RegionName.villa_archives,
                     lambda state: state.has(ItemName.archives_key, player)),
        EntranceData(RegionName.villa_main, RegionName.villa_maze,
                     lambda state: state.has(ItemName.garden_key, player)),
        EntranceData(RegionName.villa_storeroom, RegionName.villa_main,
                     lambda state: state.has(ItemName.storeroom_key, player)),
        EntranceData(RegionName.villa_maze, RegionName.villa_servants,
                     lambda state: state.has(ItemName.garden_key, player)),
        EntranceData(RegionName.villa_maze, RegionName.villa_crypt,
                     lambda state: state.has(ItemName.copper_key, player), easy_rule=True),
        EntranceData(RegionName.villa_servants, RegionName.villa_main,
                     lambda state: state.has(ItemName.garden_key, player)),
        EntranceData(RegionName.villa_crypt, RegionName.villa_maze),
        EntranceData(RegionName.villa_crypt, get_next_stage_start(RegionName.villa)),
        EntranceData(RegionName.villa_crypt,
                     stage_dict[active_stage_list[active_stage_list.index(RegionName.villa) + 2]].start_region_name),
        # Tunnel
        EntranceData(RegionName.tunnel_start, RegionName.tunnel_end),
        EntranceData(RegionName.tunnel_end, get_next_stage_start(RegionName.tunnel)),
        # Underground Waterway
        EntranceData(RegionName.uw_main, RegionName.uw_end),
        EntranceData(RegionName.uw_end, RegionName.uw_main, hard_entrance=True),
        EntranceData(RegionName.uw_end, get_next_stage_start(RegionName.underground_waterway)),
        # Castle Center
        EntranceData(RegionName.cc_main, RegionName.cc_torture_chamber,
                     lambda state: (state.has(ItemName.chamber_key, player))),
        EntranceData(RegionName.cc_main, RegionName.cc_library,
                     lambda state: (state.has(ItemName.magical_nitro, player)
                                    and state.has(ItemName.mandragora, player))),
        EntranceData(RegionName.castle_center, RegionName.cc_crystal,
                     lambda state: (state.has(ItemName.magical_nitro, player, 2)
                                    and state.has(ItemName.mandragora, player, 2))),
        EntranceData(RegionName.cc_crystal, RegionName.cc_elev_top),
        EntranceData(RegionName.castle_center, get_next_stage_start(RegionName.castle_center)),
        EntranceData(RegionName.castle_center, stage_dict[
            active_stage_list[active_stage_list.index(RegionName.castle_center) + 3]].start_region_name),
        # Duel Tower
        EntranceData(RegionName.dt_main, get_prev_stage_end(RegionName.duel_tower)),
        EntranceData(RegionName.dt_main, get_next_stage_start(RegionName.duel_tower)),
        # Tower of Execution
        EntranceData(RegionName.toe_main, get_prev_stage_end(RegionName.tower_of_execution)),
        EntranceData(RegionName.toe_main, RegionName.toe_ledge,
                     lambda state: state.has(ItemName.execution_key, player), easy_rule=True),
        EntranceData(RegionName.toe_main, get_next_stage_start(RegionName.tower_of_execution)),
        # Tower of Science
        EntranceData(RegionName.tosci_start, get_prev_stage_end(RegionName.tower_of_science)),
        EntranceData(RegionName.tosci_start, RegionName.tosci_three_doors,
                     lambda state: state.has(ItemName.science_key_one, player)),
        EntranceData(RegionName.tosci_start, RegionName.tosci_conveyors,
                     lambda state: state.has(ItemName.science_key_two, player)),
        EntranceData(RegionName.tosci_conveyors, RegionName.tosci_start,
                     lambda state: state.has(ItemName.science_key_two, player)),
        EntranceData(RegionName.tosci_conveyors, RegionName.tosci_key3,
                     lambda state: state.has(ItemName.science_key_three, player)),
        EntranceData(RegionName.tosci_conveyors, get_next_stage_start(RegionName.tower_of_science)),
        # Tower of Sorcery
        EntranceData(RegionName.tosor_main, get_prev_stage_end(RegionName.tower_of_sorcery)),
        EntranceData(RegionName.tosor_main, get_next_stage_start(RegionName.tower_of_sorcery)),
        # Room of Clocks
        EntranceData(RegionName.roc_main, get_next_stage_start(RegionName.room_of_clocks)),
        # Clock Tower
        EntranceData(RegionName.ct_start, RegionName.ct_middle,
                     lambda state: state.has(ItemName.clocktower_key_one, player)),
        EntranceData(RegionName.ct_middle, RegionName.ct_start,
                     lambda state: state.has(ItemName.clocktower_key_one, player)),
        EntranceData(RegionName.ct_middle, RegionName.ct_end,
                     lambda state: state.has(ItemName.clocktower_key_two, player)),
        EntranceData(RegionName.ct_end, RegionName.ct_middle,
                     lambda state: state.has(ItemName.clocktower_key_two, player)),
        EntranceData(RegionName.ct_end, get_next_stage_start(RegionName.clock_tower),
                     lambda state: state.has(ItemName.clocktower_key_three, player)),
        # Castle Keep
        EntranceData(RegionName.ck_main, RegionName.roc_main, hard_entrance=True),
        EntranceData(RegionName.ck_main, RegionName.ck_drac_chamber,
                     lambda state: state.has(ItemName.special_two, player, required_special2s))
    ]

    for data in all_entrances:
        entrance_not_too_hard: bool = multiworld.hard_logic[player].value is 1 or data.hard_entrance is False
        doable_as_pref_char: bool = multiworld.carrie_logic[player].value is 1 or data.carrie_entrance is False
        rule_not_too_easy: bool = multiworld.hard_logic[player].value is 0 or data.easy_rule is False

        if entrance_not_too_hard and doable_as_pref_char and data.parent_region in active_regions:
            created_entrance = Entrance(player, data.target_region, active_regions[data.parent_region])
            if data.rule and rule_not_too_easy:
                created_entrance.access_rule = data.rule
            created_entrance.connect(active_regions[data.target_region])
            active_regions[data.parent_region].exits.append(created_entrance)
