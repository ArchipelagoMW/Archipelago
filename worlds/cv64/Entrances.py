import typing

from BaseClasses import Entrance
from .Names import IName, RName
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
        if source_stage in active_stage_list:
            if multiworld.character_stages[player].value == 2:
                if active_stage_list[active_stage_list.index(source_stage) - 1] == RName.villa:
                    return stage_dict[active_stage_list[active_stage_list.index(source_stage) + 2]].start_region_name
                elif active_stage_list[active_stage_list.index(source_stage) - 2] == RName.castle_center:
                    return stage_dict[active_stage_list[active_stage_list.index(source_stage) + 3]].start_region_name

            return stage_dict[active_stage_list[active_stage_list.index(source_stage) + 1]].start_region_name

        return "Menu"
    
    def get_alt_stage_start(source_stage):
        if multiworld.character_stages[player].value == 2:
            if source_stage == RName.villa:
                return stage_dict[active_stage_list[active_stage_list.index(RName.villa) + 2]].start_region_name
            return stage_dict[active_stage_list[active_stage_list.index(RName.castle_center) + 3]].start_region_name
        
        return "Menu"

    def get_prev_stage_end(source_stage):
        if source_stage in active_stage_list:
            if active_stage_list.index(source_stage) - 1 >= 0:
                if multiworld.character_stages[player].value == 2:
                    if active_stage_list[active_stage_list.index(source_stage) - 2] == RName.villa:
                        return stage_dict[RName.villa].end_region_name
                    elif active_stage_list[active_stage_list.index(source_stage) - 3] == RName.castle_center:
                        return stage_dict[RName.castle_center].end_region_name
                    elif active_stage_list[active_stage_list.index(source_stage) - 3] == RName.villa:
                        return stage_dict[active_stage_list[active_stage_list.index(source_stage) - 2]].end_region_name
                    elif active_stage_list[active_stage_list.index(source_stage) - 5] == RName.castle_center:
                        return stage_dict[active_stage_list[active_stage_list.index(source_stage) - 3]].end_region_name

                return stage_dict[active_stage_list[active_stage_list.index(source_stage) - 1]].end_region_name

        return "Menu"

    s1s_per_warp = multiworld.special1s_per_warp[player].value

    all_entrances = [
        EntranceData(RName.menu, stage_dict[active_stage_list[0]].start_region_name),
        EntranceData(RName.menu, RName.warp1,
                     lambda state: state.has(IName.special_one, player, s1s_per_warp)),
        EntranceData(RName.menu, RName.warp2,
                     lambda state: state.has(IName.special_one, player, s1s_per_warp * 2)),
        EntranceData(RName.menu, RName.warp3,
                     lambda state: state.has(IName.special_one, player, s1s_per_warp * 3)),
        EntranceData(RName.menu, RName.warp4,
                     lambda state: state.has(IName.special_one, player, s1s_per_warp * 4)),
        EntranceData(RName.menu, RName.warp5,
                     lambda state: state.has(IName.special_one, player, s1s_per_warp * 5)),
        EntranceData(RName.menu, RName.warp6,
                     lambda state: state.has(IName.special_one, player, s1s_per_warp * 6)),
        EntranceData(RName.menu, RName.warp7,
                     lambda state: state.has(IName.special_one, player, s1s_per_warp * 7)),
        EntranceData(RName.warp1, stage_dict[active_warp_list[0]].mid_region_name),
        EntranceData(RName.warp2, stage_dict[active_warp_list[1]].mid_region_name),
        EntranceData(RName.warp3, stage_dict[active_warp_list[2]].mid_region_name),
        EntranceData(RName.warp4, stage_dict[active_warp_list[3]].mid_region_name),
        EntranceData(RName.warp5, stage_dict[active_warp_list[4]].mid_region_name),
        EntranceData(RName.warp6, stage_dict[active_warp_list[5]].mid_region_name),
        EntranceData(RName.warp7, stage_dict[active_warp_list[6]].mid_region_name),
        # Forest of Silence
        EntranceData(RName.forest_start, RName.forest_mid),
        EntranceData(RName.forest_mid, RName.forest_end),
        EntranceData(RName.forest_end, get_next_stage_start(RName.forest_of_silence)),
        # Castle Wall
        EntranceData(RName.cw_start, RName.cw_exit),
        EntranceData(RName.cw_start, get_next_stage_start(RName.castle_wall), hard_entrance=True),
        EntranceData(RName.cw_start, RName.cw_ltower,
                     lambda state: state.has(IName.left_tower_key, player)),
        EntranceData(RName.cw_ltower, get_next_stage_start(RName.castle_wall)),
        # Villa
        EntranceData(RName.villa_start, RName.villa_main),
        EntranceData(RName.villa_main, RName.villa_start, hard_entrance=True, carrie_entrance=True),
        EntranceData(RName.villa_main, RName.villa_storeroom,
                     lambda state: state.has(IName.storeroom_key, player)),
        EntranceData(RName.villa_main, RName.villa_archives,
                     lambda state: state.has(IName.archives_key, player)),
        EntranceData(RName.villa_main, RName.villa_maze,
                     lambda state: state.has(IName.garden_key, player)),
        EntranceData(RName.villa_storeroom, RName.villa_main,
                     lambda state: state.has(IName.storeroom_key, player)),
        EntranceData(RName.villa_maze, RName.villa_servants,
                     lambda state: state.has(IName.garden_key, player)),
        EntranceData(RName.villa_maze, RName.villa_crypt,
                     lambda state: state.has(IName.copper_key, player), easy_rule=True),
        EntranceData(RName.villa_servants, RName.villa_main,
                     lambda state: state.has(IName.garden_key, player)),
        EntranceData(RName.villa_crypt, RName.villa_maze),
        EntranceData(RName.villa_crypt, get_next_stage_start(RName.villa)),
        EntranceData(RName.villa_crypt, get_alt_stage_start(RName.villa)),
        # Tunnel
        EntranceData(RName.tunnel_start, RName.tunnel_end),
        EntranceData(RName.tunnel_end, get_next_stage_start(RName.tunnel)),
        # Underground Waterway
        EntranceData(RName.uw_main, RName.uw_end),
        EntranceData(RName.uw_end, RName.uw_main, hard_entrance=True),
        EntranceData(RName.uw_end, get_next_stage_start(RName.underground_waterway)),
        # Castle Center
        EntranceData(RName.cc_main, RName.cc_torture_chamber,
                     lambda state: (state.has(IName.chamber_key, player))),
        EntranceData(RName.cc_main, RName.cc_library,
                     lambda state: (state.has(IName.magical_nitro, player)
                                    and state.has(IName.mandragora, player))),
        EntranceData(RName.castle_center, RName.cc_crystal,
                     lambda state: (state.has(IName.magical_nitro, player, 2)
                                    and state.has(IName.mandragora, player, 2))),
        EntranceData(RName.cc_crystal, RName.cc_elev_top),
        EntranceData(RName.castle_center, get_next_stage_start(RName.castle_center)),
        EntranceData(RName.castle_center, get_alt_stage_start(RName.castle_center)),
        # Duel Tower
        EntranceData(RName.dt_main, get_prev_stage_end(RName.duel_tower)),
        EntranceData(RName.dt_main, get_next_stage_start(RName.duel_tower)),
        # Tower of Execution
        EntranceData(RName.toe_main, get_prev_stage_end(RName.tower_of_execution)),
        EntranceData(RName.toe_main, RName.toe_ledge,
                     lambda state: state.has(IName.execution_key, player), easy_rule=True),
        EntranceData(RName.toe_main, get_next_stage_start(RName.tower_of_execution)),
        # Tower of Science
        EntranceData(RName.tosci_start, get_prev_stage_end(RName.tower_of_science)),
        EntranceData(RName.tosci_start, RName.tosci_three_doors,
                     lambda state: state.has(IName.science_key_one, player)),
        EntranceData(RName.tosci_start, RName.tosci_conveyors,
                     lambda state: state.has(IName.science_key_two, player)),
        EntranceData(RName.tosci_conveyors, RName.tosci_start,
                     lambda state: state.has(IName.science_key_two, player)),
        EntranceData(RName.tosci_conveyors, RName.tosci_key3,
                     lambda state: state.has(IName.science_key_three, player)),
        EntranceData(RName.tosci_conveyors, get_next_stage_start(RName.tower_of_science)),
        # Tower of Sorcery
        EntranceData(RName.tosor_main, get_prev_stage_end(RName.tower_of_sorcery)),
        EntranceData(RName.tosor_main, get_next_stage_start(RName.tower_of_sorcery)),
        # Room of Clocks
        EntranceData(RName.roc_main, get_next_stage_start(RName.room_of_clocks)),
        # Clock Tower
        EntranceData(RName.ct_start, RName.ct_middle,
                     lambda state: state.has(IName.clocktower_key_one, player)),
        EntranceData(RName.ct_middle, RName.ct_start,
                     lambda state: state.has(IName.clocktower_key_one, player)),
        EntranceData(RName.ct_middle, RName.ct_end,
                     lambda state: state.has(IName.clocktower_key_two, player)),
        EntranceData(RName.ct_end, RName.ct_middle,
                     lambda state: state.has(IName.clocktower_key_two, player)),
        EntranceData(RName.ct_end, get_next_stage_start(RName.clock_tower),
                     lambda state: state.has(IName.clocktower_key_three, player)),
        # Castle Keep
        EntranceData(RName.ck_main, RName.roc_main, hard_entrance=True),
        EntranceData(RName.ck_main, RName.ck_drac_chamber,
                     lambda state: state.has(IName.special_two, player, required_special2s))
    ]

    for data in all_entrances:
        entrance_not_too_hard: bool = multiworld.hard_logic[player].value == 1 or data.hard_entrance is False
        doable_as_pref_char: bool = multiworld.carrie_logic[player].value == 1 or data.carrie_entrance is False
        rule_not_too_easy: bool = multiworld.hard_logic[player].value == 0 or data.easy_rule is False

        if entrance_not_too_hard and doable_as_pref_char and data.parent_region in active_regions:
            created_entrance = Entrance(player, data.target_region, active_regions[data.parent_region])
            if data.rule and rule_not_too_easy:
                created_entrance.access_rule = data.rule
            created_entrance.connect(active_regions[data.target_region])
            active_regions[data.parent_region].exits.append(created_entrance)
