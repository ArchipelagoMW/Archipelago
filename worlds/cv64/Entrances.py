import typing

from BaseClasses import Entrance
from .Names import IName, RName
from .Stages import stage_info


class EntranceData(typing.NamedTuple):
    parent_region: str
    target_region: str
    rule: typing.Optional[typing.Callable] = None
    easy_rule: bool = False
    hard_entrance: bool = False
    carrie_entrance: bool = False


def create_entrances(multiworld, player: int, active_stage_exits, active_warp_list, required_special2s, active_regions):
    def get_prev_stage_start(source_stage):
        if source_stage in active_stage_exits:
            if active_stage_exits[source_stage][0] != "Menu":
                return stage_info[active_stage_exits[source_stage][0]].end_region_name
        return "Menu"

    def get_next_stage_start(source_stage):
        if source_stage in active_stage_exits:
            return stage_info[active_stage_exits[source_stage][1]].start_region_name
        return "Menu"

    def get_alt_stage_start(source_stage):
        if source_stage in active_stage_exits:
            return stage_info[active_stage_exits[source_stage][2]].start_region_name
        return "Menu"

    all_entrances = [
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
        EntranceData(RName.villa_servants, RName.villa_main),
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
        EntranceData(RName.cc_lower, RName.cc_torture_chamber,
                     lambda state: (state.has(IName.chamber_key, player))),
        EntranceData(RName.cc_lower, RName.cc_upper),
        EntranceData(RName.cc_upper, RName.cc_lower),
        EntranceData(RName.cc_lower, RName.cc_library,
                     lambda state: (state.has(IName.magical_nitro, player)
                                    and state.has(IName.mandragora, player))),
        EntranceData(RName.cc_lower, RName.cc_crystal,
                     lambda state: (state.has(IName.magical_nitro, player, 2)
                                    and state.has(IName.mandragora, player, 2))),
        EntranceData(RName.cc_crystal, RName.cc_elev_top),
        EntranceData(RName.cc_elev_top, get_next_stage_start(RName.castle_center)),
        EntranceData(RName.cc_elev_top, get_alt_stage_start(RName.castle_center)),
        # Duel Tower
        EntranceData(RName.dt_main, get_prev_stage_start(RName.duel_tower)),
        EntranceData(RName.dt_main, get_next_stage_start(RName.duel_tower)),
        # Tower of Execution
        EntranceData(RName.toe_main, get_prev_stage_start(RName.tower_of_execution)),
        EntranceData(RName.toe_main, RName.toe_ledge,
                     lambda state: state.has(IName.execution_key, player), easy_rule=True),
        EntranceData(RName.toe_main, get_next_stage_start(RName.tower_of_execution)),
        # Tower of Science
        EntranceData(RName.tosci_start, get_prev_stage_start(RName.tower_of_science)),
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
        EntranceData(RName.tosor_main, get_prev_stage_start(RName.tower_of_sorcery)),
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
        EntranceData(RName.ck_main, RName.ck_drac_chamber)
    ]

    # Set up the starting stage and warp entrances
    for i in range(len(active_warp_list)):
        if i == 0:
            menu_exit = Entrance(player, stage_info[active_warp_list[i]].start_region_name, active_regions["Menu"])
            active_regions["Menu"].exits.append(menu_exit)
            menu_exit.connect(active_regions[stage_info[active_warp_list[i]].start_region_name])
        else:
            menu_exit = Entrance(player, f"Warp {i}", active_regions["Menu"])
            warp_exit = Entrance(player, stage_info[active_warp_list[i]].mid_region_name, active_regions[f"Warp {i}"])
            menu_exit.access_rule = lambda state, warp_num=i: state.has(IName.special_one, player, multiworld.
                                                                        special1s_per_warp[player].value * warp_num)
            active_regions["Menu"].exits.append(menu_exit)
            active_regions[f"Warp {i}"].exits.append(warp_exit)
            menu_exit.connect(active_regions[f"Warp {i}"])
            warp_exit.connect(active_regions[stage_info[active_warp_list[i]].mid_region_name])

    # Set up the in-stage entrances
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
