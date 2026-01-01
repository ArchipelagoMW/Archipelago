from .data import ename, iname, rname
from .stages import get_stage_info
from .options import CV64Options

from typing import Dict, List, Tuple, Union

# # #    KEY    # # #
# "connection" = The name of the Region the Entrance connects into. If it's a Tuple[str, str], we take the stage in
#                active_stage_exits given in the second string and then the stage given in that stage's slot given in
#                the first string, and take the start or end Region of that stage.
# "rule" = What rule should be applied to the Entrance during set_rules, as defined in self.rules in the CV64Rules class
#          definition in rules.py.
# "add conds" = A list of player options conditions that must be satisfied for the Entrance to be added. Can be of
#               varying length depending on how many conditions need to be satisfied. In the add_conds dict's tuples,
#               the first element is the name of the option, the second is the option value to check for, and the third
#               is a boolean for whether we are evaluating for the option value or not.
entrance_info = {
    # Forest of Silence
    ename.forest_dbridge_gate: {"connection": rname.forest_mid},
    ename.forest_werewolf_gate: {"connection": rname.forest_end},
    ename.forest_end: {"connection": ("next", rname.forest_of_silence)},
    # Castle Wall
    ename.cw_portcullis_c: {"connection": rname.cw_exit},
    ename.cw_lt_skip: {"connection": ("next", rname.castle_wall), "add conds": ["hard"]},
    ename.cw_lt_door: {"connection": rname.cw_ltower, "rule": iname.left_tower_key},
    ename.cw_end: {"connection": ("next", rname.castle_wall)},
    # Villa
    ename.villa_dog_gates: {"connection": rname.villa_main},
    ename.villa_snipe_dogs: {"connection": rname.villa_start, "add conds": ["carrie", "hard"]},
    ename.villa_to_storeroom: {"connection": rname.villa_storeroom, "rule": iname.storeroom_key},
    ename.villa_to_archives: {"connection": rname.villa_archives, "rule": iname.archives_key},
    ename.villa_renon: {"connection": rname.renon, "add conds": ["shopsanity"]},
    ename.villa_to_maze: {"connection": rname.villa_maze, "rule": iname.garden_key},
    ename.villa_from_storeroom: {"connection": rname.villa_main, "rule": iname.storeroom_key},
    ename.villa_from_maze: {"connection": rname.villa_servants, "rule": iname.garden_key},
    ename.villa_servant_door: {"connection": rname.villa_main},
    ename.villa_copper_door: {"connection": rname.villa_crypt, "rule": iname.copper_key,
                              "add conds": ["not hard"]},
    ename.villa_copper_skip: {"connection": rname.villa_crypt, "add conds": ["hard"]},
    ename.villa_bridge_door: {"connection": rname.villa_maze},
    ename.villa_end_r: {"connection": ("next", rname.villa)},
    ename.villa_end_c: {"connection": ("alt", rname.villa)},
    # Tunnel
    ename.tunnel_start_renon: {"connection": rname.renon, "add conds": ["shopsanity"]},
    ename.tunnel_gondolas: {"connection": rname.tunnel_end},
    ename.tunnel_end_renon: {"connection": rname.renon, "add conds": ["shopsanity"]},
    ename.tunnel_end: {"connection": ("next", rname.tunnel)},
    # Underground Waterway
    ename.uw_renon: {"connection": rname.renon, "add conds": ["shopsanity"]},
    ename.uw_final_waterfall: {"connection": rname.uw_end},
    ename.uw_waterfall_skip: {"connection": rname.uw_main, "add conds": ["hard"]},
    ename.uw_end: {"connection": ("next", rname.underground_waterway)},
    # Castle Center
    ename.cc_tc_door: {"connection": rname.cc_torture_chamber, "rule": iname.chamber_key},
    ename.cc_renon: {"connection": rname.renon, "add conds": ["shopsanity"]},
    ename.cc_lower_wall: {"connection": rname.cc_crystal, "rule": "Bomb 2"},
    ename.cc_upper_wall: {"connection": rname.cc_library, "rule": "Bomb 1"},
    ename.cc_elevator: {"connection": rname.cc_elev_top},
    ename.cc_exit_r: {"connection": ("next", rname.castle_center)},
    ename.cc_exit_c: {"connection": ("alt", rname.castle_center)},
    # Duel Tower
    ename.dt_start: {"connection": ("prev", rname.duel_tower)},
    ename.dt_end: {"connection": ("next", rname.duel_tower)},
    # Tower of Execution
    ename.toe_start: {"connection": ("prev", rname.tower_of_execution)},
    ename.toe_gate: {"connection": rname.toe_ledge, "rule": iname.execution_key,
                     "add conds": ["not hard"]},
    ename.toe_gate_skip: {"connection": rname.toe_ledge, "add conds": ["hard"]},
    ename.toe_end: {"connection": ("next", rname.tower_of_execution)},
    # Tower of Science
    ename.tosci_start: {"connection": ("prev", rname.tower_of_science)},
    ename.tosci_key1_door: {"connection": rname.tosci_three_doors, "rule": iname.science_key1},
    ename.tosci_to_key2_door: {"connection": rname.tosci_conveyors, "rule": iname.science_key2},
    ename.tosci_from_key2_door: {"connection": rname.tosci_start, "rule": iname.science_key2},
    ename.tosci_key3_door: {"connection": rname.tosci_key3, "rule": iname.science_key3},
    ename.tosci_end: {"connection": ("next", rname.tower_of_science)},
    # Tower of Sorcery
    ename.tosor_start: {"connection": ("prev", rname.tower_of_sorcery)},
    ename.tosor_end: {"connection": ("next", rname.tower_of_sorcery)},
    # Room of Clocks
    ename.roc_gate: {"connection": ("next", rname.room_of_clocks)},
    # Clock Tower
    ename.ct_to_door1: {"connection": rname.ct_middle, "rule": iname.clocktower_key1},
    ename.ct_from_door1: {"connection": rname.ct_start, "rule": iname.clocktower_key1},
    ename.ct_to_door2: {"connection": rname.ct_end, "rule": iname.clocktower_key2},
    ename.ct_from_door2: {"connection": rname.ct_middle, "rule": iname.clocktower_key2},
    ename.ct_renon: {"connection": rname.renon, "add conds": ["shopsanity"]},
    ename.ct_door_3: {"connection": ("next", rname.clock_tower), "rule": iname.clocktower_key3},
    # Castle Keep
    ename.ck_slope_jump: {"connection": rname.roc_main, "add conds": ["hard"]},
    ename.ck_drac_door: {"connection": rname.ck_drac_chamber, "rule": "Dracula"}
}

add_conds = {"carrie": ("carrie_logic", True, True),
             "hard": ("hard_logic", True, True),
             "not hard": ("hard_logic", False, True),
             "shopsanity": ("shopsanity", True, True)}

stage_connection_types = {"prev": "end region",
                          "next": "start region",
                          "alt": "start region"}


def get_entrance_info(entrance: str, info: str) -> Union[str, Tuple[str, str], List[str], None]:
    return entrance_info[entrance].get(info, None)


def get_warp_entrances(active_warp_list: List[str]) -> Dict[str, str]:
    # Create the starting stage Entrance.
    warp_entrances = {get_stage_info(active_warp_list[0], "start region"): "Start stage"}

    # Create the warp Entrances.
    for i in range(1, len(active_warp_list)):
        mid_stage_region = get_stage_info(active_warp_list[i], "mid region")
        warp_entrances.update({mid_stage_region: f"Warp {i}"})

    return warp_entrances


def verify_entrances(options: CV64Options, entrances: List[str],
                     active_stage_exits: Dict[str, Dict[str, Union[str, int, None]]]) -> Dict[str, str]:
    verified_entrances = {}

    for ent_name in entrances:
        ent_add_conds = get_entrance_info(ent_name, "add conds")

        # Check any options that might be associated with the Entrance before adding it.
        add_it = True
        if ent_add_conds is not None:
            for cond in ent_add_conds:
                if not ((getattr(options, add_conds[cond][0]).value == add_conds[cond][1]) == add_conds[cond][2]):
                    add_it = False

        if not add_it:
            continue

        # Add the Entrance to the verified Entrances if the above check passes.
        connection = get_entrance_info(ent_name, "connection")

        # If the Entrance is a connection to a different stage, get the corresponding other stage Region.
        if isinstance(connection, tuple):
            connecting_stage = active_stage_exits[connection[1]][connection[0]]
            # Stages that lead backwards at the beginning of the line will appear leading to "Menu".
            if connecting_stage in ["Menu", None]:
                continue
            connection = get_stage_info(connecting_stage, stage_connection_types[connection[0]])
        verified_entrances.update({connection: ent_name})

    return verified_entrances
