from worlds.generic.Rules import add_rule

from .Names import LocationName
from .Levels import possible_starting_entrances

from typing import TYPE_CHECKING, Dict, List
if TYPE_CHECKING:
    from . import WaffleWorld, WaffleProcedurePatch


smw_star_pairs = {
    LocationName.donut_plains_star_road: LocationName.star_road_donut,
    LocationName.vanilla_dome_star_road: LocationName.star_road_vanilla,
    LocationName.twin_bridges_star_road: LocationName.star_road_twin_bridges,
    LocationName.forest_star_road: LocationName.star_road_forest,
    LocationName.valley_star_road: LocationName.star_road_valley,
    LocationName.star_road_special: LocationName.special_star_road,
    LocationName.special_complete: LocationName.yoshis_house_tile,
}

smw_pipe_pairs = {
    LocationName.donut_plains_entrance_pipe: LocationName.valley_donut_exit_pipe,
    LocationName.valley_donut_entrance_pipe: LocationName.donut_plains_exit_pipe,
    LocationName.vanilla_dome_top_entrance_pipe: LocationName.vanilla_dome_top_exit_pipe,
    LocationName.vanilla_dome_bottom_entrance_pipe: LocationName.twin_bridges_exit_pipe,
    LocationName.chocolate_island_entrance_pipe: LocationName.valley_chocolate_exit_pipe,
    LocationName.valley_chocolate_entrance_pipe: LocationName.chocolate_island_exit_pipe,
}

smw_offscreen_event_indexes = {
    LocationName.valley_donut_exit_pipe: [0x12, 0x11, 0x03],
    LocationName.donut_plains_exit_pipe: [0x14, 0x08, 0x05],
    LocationName.vanilla_dome_top_exit_pipe: [0x1D, 0x0D, 0x04],
    LocationName.twin_bridges_exit_pipe: [0x1C, 0x14, 0x01],
    LocationName.valley_chocolate_exit_pipe: [0x47, 0x1D, 0x01],
    LocationName.vanilla_dome_star_road: [0x52, 0x2C, 0x01],
    LocationName.twin_bridges_star_road: [0x55, 0x2D, 0x01],
    LocationName.forest_star_road: [0x58, 0x2E, 0x01],
    LocationName.donut_plains_star_road: [0x5D, 0x2F, 0x01],
    LocationName.star_road_special: [0x5E, 0x30, 0x01],
    LocationName.special_complete: [0x6C, 0x31, 0x01],
    LocationName.valley_star_road: [0x5B, 0x32, 0x04],

    LocationName.dp_from_yi: [0x06, 0x00, 0x08],
    LocationName.ysp_from_yi: [0x01, 0x20, 0x01],
    LocationName.vd_from_dp: [0x0F, 0x24, 0x03],
    LocationName.foi_from_tw: [0x24, 0x21, 0x02],
    LocationName.ci_from_foi: [0x2F, 0x15, 0x05],
    LocationName.sr_from_foi: [0x34, 0x1A, 0x03],
    LocationName.vob_from_ci: [0x4E, 0x1E, 0x02],

}

smw_teleport_data = {
    LocationName.donut_plains_star_road: [0x1A, 0x78, 0x00, 0x28, 0x01],
    LocationName.star_road_donut: [0x0C, 0x28, 0x0D, 0xD8, 0x01],
    LocationName.vanilla_dome_star_road: [0x1E, 0x08, 0x04, 0xE8, 0x00],
    LocationName.star_road_vanilla: [0x1C, 0x28, 0x0D, 0x88, 0x01],
    LocationName.twin_bridges_star_road: [0x22, 0x08, 0x01, 0xF8, 0x00],
    LocationName.star_road_twin_bridges: [0x20, 0x78, 0x0D, 0x68, 0x01],
    LocationName.forest_star_road: [0x26, 0x48, 0x01, 0x08, 0x01],
    LocationName.star_road_forest: [0x24, 0xC8, 0x0D, 0x88, 0x01],
    LocationName.valley_star_road: [0x2A, 0x48, 0x09, 0x38, 0x00],
    LocationName.star_road_valley: [0x32, 0xC8, 0x0D, 0xD8, 0x01],
    LocationName.star_road_special: [0x2E, 0x78, 0x0D, 0x88, 0x01],
    LocationName.special_star_road: [0x2C, 0x18, 0x0B, 0x38, 0x01],
    LocationName.special_complete: [0x34, 0x18, 0x0B, 0x18, 0x01],
    LocationName.yoshis_house_tile: [0x30, 0x68, 0x02, 0x78, 0x00],
    LocationName.donut_plains_entrance_pipe: [0x12, 0x98, 0x00, 0x08, 0x01],
    LocationName.valley_donut_exit_pipe: [0x04, 0x08, 0x09, 0x38, 0x00],
    LocationName.valley_donut_entrance_pipe: [0x06, 0x28, 0x09, 0x18, 0x00],
    LocationName.donut_plains_exit_pipe: [0x14, 0xB8, 0x00, 0xE8, 0x00],
    LocationName.vanilla_dome_top_entrance_pipe: [0x02, 0x38, 0x04, 0xB8, 0x00],
    LocationName.vanilla_dome_top_exit_pipe: [0x10, 0xA8, 0x00, 0x38, 0x00],
    LocationName.vanilla_dome_bottom_entrance_pipe: [0x00, 0xA8, 0x04, 0x48, 0x01],
    LocationName.twin_bridges_exit_pipe: [0x0E, 0x18, 0x01, 0x78, 0x00],
    LocationName.chocolate_island_entrance_pipe: [0x16, 0x28 ,0x01, 0x78, 0x01],
    LocationName.valley_chocolate_exit_pipe: [0x08, 0xC8, 0x09, 0x98, 0x00],
    LocationName.valley_chocolate_entrance_pipe: [0x0A, 0x48, 0x09, 0x98, 0x00],
    LocationName.chocolate_island_exit_pipe: [0x18, 0xA8, 0x00, 0x88, 0x01],
}

teleport_pairs = {**smw_star_pairs, **smw_pipe_pairs}
tp_keys = list(teleport_pairs.keys())
tp_values = list(teleport_pairs.values())

smw_transition_pairs = {
    LocationName.yi_to_ysp: LocationName.ysp_from_yi,
    LocationName.yi_to_dp: LocationName.dp_from_yi,
    LocationName.dp_to_vd: LocationName.vd_from_dp,
    LocationName.tw_to_foi: LocationName.foi_from_tw,
    LocationName.foi_to_ci: LocationName.ci_from_foi,
    LocationName.foi_to_sr: LocationName.sr_from_foi,
    LocationName.ci_to_vob: LocationName.vob_from_ci,
}

# Data order:
# 0: Offset/Index to ROM
# 1-3: Y Coords for tile
# 4-5: X Coords for tile
# 6: Submap ID
# 7-8: YX Coords >> 4 + Adjustment
# 9: Walk direction when used as destination
#   0: Up
#   1: Left
#   2: Down
#   3: Right

smw_transition_data = {
    LocationName.yi_to_ysp: [0x00, 0x00, 0x00, 0x48, 0x00, 0x01, 0x00, 0x04, 0x02], 
    LocationName.ysp_from_yi: [0x02, 0x50, 0x01, 0x28, 0x00, 0x00, 0x14, 0x02, 0x00], 

    LocationName.yi_to_dp: [0x01, 0x00, 0x00, 0x98, 0x00, 0x01, 0x00, 0x09, 0x02], 
    LocationName.dp_from_yi: [0x03, 0x60, 0x01, 0x58, 0x00, 0x00, 0x15, 0x05, 0x00], 

    LocationName.dp_to_vd: [0x05, 0x90, 0x00, 0xD8, 0x00, 0x00, 0x09, 0x0D, 0x02],  
    LocationName.vd_from_dp: [0x04, 0x50, 0x01, 0x58, 0x00, 0x02, 0x14, 0x05, 0x00], 

    LocationName.tw_to_foi: [0x09, 0xB0, 0x00, 0xC8, 0x01, 0x00, 0x0A, 0x1C, 0x00], 
    LocationName.foi_from_tw: [0x08, 0x50, 0x01, 0x88, 0x00, 0x03, 0x15, 0x08, 0x02], 
    
    LocationName.foi_to_ci: [0x0C, 0x00, 0x02, 0x88, 0x00, 0x03, 0x1F, 0x08, 0x00], 
    LocationName.ci_from_foi: [0x0D, 0x00, 0x01, 0xC8, 0x01, 0x00, 0x10, 0x1C, 0x02], 
    
    LocationName.foi_to_sr: [0x0A, 0xE8, 0x01, 0x00, 0x00, 0x03, 0x1E, 0x00, 0x06], 
    LocationName.sr_from_foi: [0x0B, 0x08, 0x01, 0xA0 ,0x01, 0x00, 0x10, 0x19, 0x04], 

    LocationName.ci_to_vob: [0x06, 0x50, 0x01, 0xE8, 0x00, 0x00, 0x15, 0x0E, 0x02], 
    LocationName.vob_from_ci: [0x07, 0xA0, 0x00, 0xE8, 0x01, 0x04, 0x09, 0x1E, 0x00], 
}

tr_keys = list(smw_transition_pairs.keys())
tr_values = list(smw_transition_pairs.values())

region_mapping: Dict[str, List[str]]  = {
    # Let regions with excluded locations go first
    # Fill everything else, with YI as a priority
    LocationName.yoshis_house_tile: [
        LocationName.yi_to_ysp,
        LocationName.yi_to_dp,
    ],
    LocationName.ysp_from_yi: [
        # dead end lol
    ],
    LocationName.dp_from_yi: [
        LocationName.dp_to_vd,
        LocationName.donut_plains_entrance_pipe,
        LocationName.donut_plains_star_road,
    ],
    LocationName.valley_donut_exit_pipe: [
        LocationName.valley_donut_entrance_pipe,
    ],
    LocationName.donut_plains_exit_pipe: [
        LocationName.dp_to_vd,
    ],
    LocationName.vd_from_dp: [
        LocationName.vanilla_dome_top_entrance_pipe,
        LocationName.vanilla_dome_bottom_entrance_pipe,
        LocationName.vanilla_dome_star_road,
    ],
    LocationName.twin_bridges_exit_pipe: [
        LocationName.twin_bridges_star_road,
        LocationName.tw_to_foi,
    ],
    LocationName.vanilla_dome_top_exit_pipe: [
        LocationName.tw_to_foi,
    ],
    LocationName.foi_from_tw: [
        LocationName.foi_to_ci,
        LocationName.foi_to_sr,
    ],
    LocationName.sr_from_foi: [
        LocationName.forest_star_road,
    ],
    LocationName.ci_from_foi: [
        LocationName.chocolate_island_entrance_pipe,
        LocationName.ci_to_vob,
    ],
    LocationName.chocolate_island_exit_pipe: [
        LocationName.ci_to_vob,
    ],
    LocationName.valley_chocolate_exit_pipe: [
        LocationName.valley_chocolate_entrance_pipe,
    ],
    LocationName.vob_from_ci: [
        LocationName.valley_star_road,
    ],
    LocationName.star_road_donut: [
        LocationName.star_road_special,
    ],
    LocationName.star_road_vanilla: [
        LocationName.star_road_special,
    ],
    LocationName.star_road_twin_bridges: [
        LocationName.star_road_special,
    ],
    LocationName.star_road_forest: [
        LocationName.star_road_special,
    ],
    LocationName.star_road_valley: [
        LocationName.star_road_special,
    ],
    LocationName.special_star_road: [
        LocationName.special_complete,
    ],

}

region_excluded_destinations: Dict[str, List[str]] = {
    LocationName.yi_to_ysp: [
    ],
    LocationName.yi_to_dp: [
    ],
    LocationName.dp_to_vd: [
        ],
    LocationName.tw_to_foi: [
        ],
    LocationName.foi_to_ci: [],
    LocationName.foi_to_sr: [],
    LocationName.ci_to_vob: [],
    LocationName.donut_plains_entrance_pipe: [
        LocationName.donut_plains_exit_pipe,
    ],
    LocationName.valley_donut_entrance_pipe: [
        LocationName.valley_donut_exit_pipe,
    ],
    LocationName.vanilla_dome_top_entrance_pipe: [
    ],
    LocationName.vanilla_dome_bottom_entrance_pipe: [
    ],
    LocationName.chocolate_island_entrance_pipe: [
        LocationName.chocolate_island_exit_pipe,
    ],
    LocationName.valley_chocolate_entrance_pipe: [],
    LocationName.donut_plains_star_road: [],
    LocationName.vanilla_dome_star_road: [],
    LocationName.twin_bridges_star_road: [],
    LocationName.forest_star_road: [],
    LocationName.valley_star_road: [],
    LocationName.star_road_special: [],
    LocationName.special_complete: [
        LocationName.special_star_road,
    ],
}

region_excluded_destinations_per_starting_location: Dict[int, Dict[str, List[str]]] = {
    0: {
        LocationName.yi_to_ysp: [
            LocationName.sr_from_foi,
            LocationName.vob_from_ci,
        ],
        LocationName.yi_to_dp: [
            LocationName.sr_from_foi,
            LocationName.vob_from_ci,
        ],
        LocationName.vanilla_dome_top_entrance_pipe: [
            LocationName.yoshis_house_tile,
        ],
        LocationName.vanilla_dome_bottom_entrance_pipe: [
            LocationName.yoshis_house_tile,
        ],
    },
    1: {
        LocationName.dp_to_vd: [
            LocationName.dp_from_yi,
            LocationName.sr_from_foi,
            LocationName.vob_from_ci,
        ],
        LocationName.donut_plains_star_road: [
            LocationName.donut_plains_exit_pipe,
        ],
    },
    2: {
        LocationName.vanilla_dome_top_entrance_pipe: [
            LocationName.star_road_donut,
            LocationName.star_road_vanilla,
            LocationName.star_road_twin_bridges,
            LocationName.star_road_forest,
            LocationName.star_road_valley,
        ],
        LocationName.vanilla_dome_bottom_entrance_pipe: [
            LocationName.star_road_donut,
            LocationName.star_road_vanilla,
            LocationName.star_road_twin_bridges,
            LocationName.star_road_forest,
            LocationName.star_road_valley,
        ],
        LocationName.vanilla_dome_star_road: [
            LocationName.star_road_donut,
            LocationName.star_road_vanilla,
            LocationName.star_road_twin_bridges,
            LocationName.star_road_forest,
            LocationName.star_road_valley,
        ],
    },
    3: {
        LocationName.foi_to_ci: [
            LocationName.foi_from_tw,
            LocationName.vob_from_ci,
        ],
        LocationName.foi_to_sr: [
            LocationName.foi_from_tw,
            LocationName.vob_from_ci,
        ],
    },
    4: {
        LocationName.special_complete: [
            LocationName.special_star_road,
            LocationName.star_road_donut,
            LocationName.star_road_vanilla,
            LocationName.star_road_twin_bridges,
            LocationName.star_road_forest,
            LocationName.star_road_valley,
        ],
    },
}

region_boss_token_additions = {
    LocationName.yi_to_ysp: 0,
    LocationName.yi_to_dp: 1,
    LocationName.dp_to_vd: 1,
    LocationName.tw_to_foi: 1,
    LocationName.foi_to_ci: 0,
    LocationName.foi_to_sr: 0,
    LocationName.ci_to_vob: 1,
    LocationName.donut_plains_star_road: 0,
    LocationName.vanilla_dome_star_road: 0,
    LocationName.twin_bridges_star_road: 0,
    LocationName.forest_star_road: 1,
    LocationName.valley_star_road: 0,
    LocationName.star_road_special: 0,
    LocationName.special_complete: 0,
    LocationName.donut_plains_entrance_pipe: 0,
    LocationName.valley_donut_entrance_pipe: 0,
    LocationName.vanilla_dome_top_entrance_pipe: 0,
    LocationName.vanilla_dome_bottom_entrance_pipe: 1,
    LocationName.chocolate_island_entrance_pipe: 1,
    LocationName.valley_chocolate_entrance_pipe: 0,
}


def generate_entrance_rando(world: "WaffleWorld"):
    # This shuffle method walks through every valid exit (starting from YI house) to assign new exits to unconnected entrances
    # It attempts to swap around exits without any consideration until everything is connected
    world.transition_pairs = {**smw_transition_pairs}
    world.transition_data = {**smw_transition_data}
    world.teleport_pairs = {**smw_star_pairs, **smw_pipe_pairs}
    world.teleport_data = {**smw_teleport_data}
    
    local_mapping: Dict[str, str] = {}
    starting_location = possible_starting_entrances[world.options.starting_location.value]
    next_exits = [starting_location]
    processed_exits = []
    used_exits = []
    local_region_mapping = {**region_mapping}

    # Exclude destinations
    local_excluded_destinations = {**region_excluded_destinations}
    exclusions = region_excluded_destinations_per_starting_location[world.options.starting_location.value]
    local_excluded_destinations.update(exclusions)

    prefilled_exits: Dict[str, str] = {}
    boss_token_requirements = {
        LocationName.yi_to_ysp: 11,
        LocationName.yi_to_dp: 11,
        LocationName.dp_to_vd: 11,
        LocationName.tw_to_foi: 11,
        LocationName.foi_to_ci: 11,
        LocationName.foi_to_sr: 11,
        LocationName.ci_to_vob: 11,
        LocationName.donut_plains_star_road: 11,
        LocationName.vanilla_dome_star_road: 11,
        LocationName.twin_bridges_star_road: 11,
        LocationName.forest_star_road: 11,
        LocationName.valley_star_road: 11,
        LocationName.star_road_special: 11,
        LocationName.special_complete: 11,
        LocationName.donut_plains_entrance_pipe: 11,
        LocationName.valley_donut_entrance_pipe: 11,
        LocationName.vanilla_dome_top_entrance_pipe: 11,
        LocationName.vanilla_dome_bottom_entrance_pipe: 11,
        LocationName.chocolate_island_entrance_pipe: 11,
        LocationName.valley_chocolate_entrance_pipe: 11,
    }

    #if world.options.exclude_special_zone:
    #    prefilled_exits[LocationName.star_road_special] = LocationName.special_star_road
    #    prefilled_exits[LocationName.special_complete] = LocationName.yoshis_house_tile
    #    #local_region_mapping.pop(LocationName.special_star_road)

    if world.options.map_teleport_shuffle == "off":
        prefilled_exits[LocationName.donut_plains_star_road] = LocationName.star_road_donut
        prefilled_exits[LocationName.vanilla_dome_star_road] = LocationName.star_road_vanilla
        prefilled_exits[LocationName.twin_bridges_star_road] = LocationName.star_road_twin_bridges
        prefilled_exits[LocationName.forest_star_road] = LocationName.star_road_forest
        prefilled_exits[LocationName.valley_star_road] = LocationName.star_road_valley
        prefilled_exits[LocationName.star_road_special] = LocationName.special_star_road
        prefilled_exits[LocationName.special_complete] = LocationName.yoshis_house_tile
    
        prefilled_exits[LocationName.donut_plains_entrance_pipe] = LocationName.valley_donut_exit_pipe
        prefilled_exits[LocationName.valley_donut_entrance_pipe] = LocationName.donut_plains_exit_pipe
        prefilled_exits[LocationName.vanilla_dome_top_entrance_pipe] = LocationName.vanilla_dome_top_exit_pipe
        prefilled_exits[LocationName.vanilla_dome_bottom_entrance_pipe] = LocationName.twin_bridges_exit_pipe
        prefilled_exits[LocationName.chocolate_island_entrance_pipe] = LocationName.valley_chocolate_exit_pipe
        prefilled_exits[LocationName.valley_chocolate_entrance_pipe] = LocationName.chocolate_island_exit_pipe
    
    elif world.options.map_teleport_shuffle == "on_only_stars":
        prefilled_exits[LocationName.donut_plains_entrance_pipe] = LocationName.valley_donut_exit_pipe
        prefilled_exits[LocationName.valley_donut_entrance_pipe] = LocationName.donut_plains_exit_pipe
        prefilled_exits[LocationName.vanilla_dome_top_entrance_pipe] = LocationName.vanilla_dome_top_exit_pipe
        prefilled_exits[LocationName.vanilla_dome_bottom_entrance_pipe] = LocationName.twin_bridges_exit_pipe
        prefilled_exits[LocationName.chocolate_island_entrance_pipe] = LocationName.valley_chocolate_exit_pipe
        prefilled_exits[LocationName.valley_chocolate_entrance_pipe] = LocationName.chocolate_island_exit_pipe

    elif world.options.map_teleport_shuffle == "on_only_pipes":
        prefilled_exits[LocationName.donut_plains_star_road] = LocationName.star_road_donut
        prefilled_exits[LocationName.vanilla_dome_star_road] = LocationName.star_road_vanilla
        prefilled_exits[LocationName.twin_bridges_star_road] = LocationName.star_road_twin_bridges
        prefilled_exits[LocationName.forest_star_road] = LocationName.star_road_forest
        prefilled_exits[LocationName.valley_star_road] = LocationName.star_road_valley
        prefilled_exits[LocationName.star_road_special] = LocationName.special_star_road
        prefilled_exits[LocationName.special_complete] = LocationName.yoshis_house_tile

    if not world.options.map_transition_shuffle:
        prefilled_exits[LocationName.yi_to_ysp] = LocationName.ysp_from_yi
        prefilled_exits[LocationName.yi_to_dp] = LocationName.dp_from_yi
        prefilled_exits[LocationName.dp_to_vd] = LocationName.vd_from_dp
        prefilled_exits[LocationName.tw_to_foi] = LocationName.foi_from_tw
        prefilled_exits[LocationName.foi_to_ci] = LocationName.ci_from_foi
        prefilled_exits[LocationName.foi_to_sr] = LocationName.sr_from_foi
        prefilled_exits[LocationName.ci_to_vob] = LocationName.vob_from_ci

    for entrance, exit in prefilled_exits.items():
        local_mapping[entrance] = exit

    used_exits = list(prefilled_exits.values())

    swap_count = 0

    while len(processed_exits) != len(local_region_mapping.keys()):
        if len(next_exits) == 0:
            # Swap exits if we haven't met the processed exits goal
            unreached_transitions = [x for x in smw_transition_pairs.values() if x not in local_mapping.values()]
            unreached_teleports = [x for x in teleport_pairs.values() if x not in local_mapping.values()]
            unreached_exits = unreached_transitions + unreached_teleports
            if len(unreached_exits) == 0 or swap_count >= 10:
                local_mapping = {}
                for entrance, exit in prefilled_exits.items():
                    local_mapping[entrance] = exit
                next_exits = [starting_location]
                processed_exits = []
                used_exits = list(prefilled_exits.values())
                swap_count = 0
                continue
            unreached_candidate = world.random.choice(unreached_exits)
            if "Transition - " in unreached_candidate:
                candidates = [x for x in processed_exits if "Transition - " in x and x not in prefilled_exits.values()]
            else:
                if world.options.map_teleport_shuffle != "on_both_mix":
                    if "Pipe" in unreached_candidate:
                        candidates = [x for x in processed_exits if "Transition - " not in x and "Pipe" in x]
                    else:
                        candidates = [x for x in processed_exits if "Transition - " not in x and "Star World" in x or x != LocationName.yoshis_house_tile]
                else:
                    candidates = [x for x in processed_exits if "Transition - " not in x and x not in prefilled_exits.values()]
            if len(candidates) == 0:
                swap_count = 10
                continue
            swap_candidate = world.random.choice(candidates)
            next_exits.append(swap_candidate)
            processed_exits.remove(swap_candidate)
            
            if len(processed_exits) >= 18:
                swap_count += 1

            # Removes the previous processed entrances from the cache
            for entrance in local_region_mapping[swap_candidate]:
                if entrance in local_mapping:
                    value = local_mapping.pop(entrance)
                    next_exits.append(value)
                    if value in processed_exits:
                        processed_exits.remove(value)
                    if value in used_exits:
                        used_exits.remove(value)
        
        # Processes the current exits
        for exit in next_exits:
            next_exits.remove(exit)
            if exit in processed_exits:
                continue
            entrances = local_region_mapping[exit]
            for entrance in entrances:
                if entrance in local_mapping.keys():
                    selected_exit = local_mapping[entrance]
                else:
                    banned_exits = used_exits.copy()
                    banned_exits.append(exit)
                    banned_exits.extend(local_excluded_destinations[entrance])
                    if "Transition - " in entrance:
                        possible_exits = [x for x in smw_transition_pairs.values() if x not in banned_exits]
                    else:
                        if world.options.map_teleport_shuffle == "on_both_same_type":
                            if "Pipe" in entrance:
                                possible_exits = [x for x in smw_pipe_pairs.values() if x not in banned_exits]
                            else:
                                possible_exits = [x for x in smw_star_pairs.values() if x not in banned_exits]
                        else:
                            possible_exits = [x for x in teleport_pairs.values() if x not in banned_exits]
                    if len(possible_exits) == 0:
                        continue
                    selected_exit = world.random.choice(possible_exits)
                used_exits.append(selected_exit)
                local_mapping[entrance] = selected_exit
                next_exits.append(selected_exit)

            processed_exits.append(exit)

        # Reachabilty check
        if len(processed_exits) == len(local_region_mapping.keys()):
            remaining_exits = list(local_region_mapping.keys())
            check_next_exits = [(starting_location, 0)]
            processed_entrances = []
            boss_tokens = 0

            while len(remaining_exits) != 0:
                cache_exits = remaining_exits.copy()
                for exit_data in check_next_exits:
                    exit = exit_data[0]
                    boss_tokens = exit_data[1]
                    if exit not in remaining_exits:
                        continue
                    remaining_exits.remove(exit)
                    check_next_exits.remove(exit_data)
                    for entrance in local_region_mapping[exit]:
                        if entrance not in local_mapping.keys():
                            continue
                        if entrance not in processed_entrances:
                            boss_tokens += region_boss_token_additions[entrance]
                            boss_token_requirements[entrance] = min(boss_tokens, boss_token_requirements[entrance])
                        processed_entrances.append(entrance)
                        check_next_exits.append((local_mapping[entrance], boss_tokens))
                    
                if len(cache_exits) == len(remaining_exits) and len(cache_exits) != 0:
                    # EMERGENCY SWAP
                    # Marks isolated exits as unreachable
                    processed_exits = [x for x in processed_exits if x not in remaining_exits]
                    used_exits = [x for x in used_exits if x not in remaining_exits]
                    emergency_list = [x for x in processed_exits if x not in prefilled_exits.values()]
                    if len(emergency_list) == 0:
                        local_mapping = {}
                        for entrance, exit in prefilled_exits.items():
                            local_mapping[entrance] = exit
                        next_exits = [starting_location]
                        processed_exits = []
                        used_exits = list(prefilled_exits.values())
                        break

                    #if world.options.exclude_special_zone:
                    #    emergency_list.remove(LocationName.special_star_road)
                    #    emergency_list.remove(LocationName.yoshis_house_tile)
                    emergency_swap = world.random.choice(emergency_list)
                    processed_exits.remove(emergency_swap)
                    if emergency_swap in used_exits:
                        used_exits.remove(emergency_swap)
                    for exit, entrances in local_region_mapping.items():
                        if exit not in processed_exits:
                            for entrance in entrances:
                                if entrance not in local_mapping.keys():
                                    continue
                                value = local_mapping.pop(entrance)
                                next_exits.append(value)
                    break

    for entrance, exit in local_mapping.items():
        world.local_mapping[entrance] = exit
        if "Transition - " in entrance:
            world.transition_pairs[entrance] = exit
        else:
            world.teleport_pairs[entrance] = exit


    for exit, entrance in local_region_mapping.items():
        world.local_region_mapping[exit] = entrance

    world.boss_token_requirements = {**boss_token_requirements}


SILENT_EVENT_ADDR = 0x88933
TRANSITION_DIRECTIONS_ADDR = 0x88A77

def handle_silent_events(patch: "WaffleProcedurePatch", world: "WaffleWorld"):
    for connection, event_id in world.cached_connections.items():
        if connection not in smw_offscreen_event_indexes.keys():
            continue
        offset = SILENT_EVENT_ADDR + smw_offscreen_event_indexes[connection][1]
        size = smw_offscreen_event_indexes[connection][2]
        patch.write_bytes(offset, bytearray([event_id for _ in range(size)]))


def handle_teleport_shuffle(patch: "WaffleProcedurePatch", world: "WaffleWorld"):
    tokens = bytearray([0x00 for _ in range(0x6C)])
    
    for new_entrance, new_exit in world.teleport_pairs.items():
        old_entrance = tp_keys[tp_values.index(new_exit)]
        old_exit = teleport_pairs[new_entrance]
        
        offset = smw_teleport_data[old_entrance][0]
        tokens[offset:offset+2] = bytearray(smw_teleport_data[new_entrance][1:3])
        offset = 0x36 + smw_teleport_data[old_entrance][0]
        tokens[offset:offset+2] = bytearray(smw_teleport_data[new_entrance][3:5])
        offset = smw_teleport_data[old_exit][0]
        tokens[offset:offset+2] = bytearray(smw_teleport_data[new_exit][1:3])
        offset = 0x36 + smw_teleport_data[old_exit][0]
        tokens[offset:offset+2] = bytearray(smw_teleport_data[new_exit][3:5])

        if new_exit in smw_offscreen_event_indexes.keys():
            offset = SILENT_EVENT_ADDR + smw_offscreen_event_indexes[new_exit][1]
            size = smw_offscreen_event_indexes[new_exit][2]
            patch.write_bytes(offset, bytearray([world.cached_connections[new_entrance] for _ in range(size)]))
        
    if world.options.map_teleport_shuffle == "on_both_mix" or world.options.map_teleport_shuffle == "on_only_stars":
        patch.write_bytes(SILENT_EVENT_ADDR + 0x27, bytearray([0xFF for _ in range(0x05)]))

    patch.write_bytes(0x2049D, tokens)

def handle_transition_shuffle(patch: "WaffleProcedurePatch", world: "WaffleWorld"):
    tokens = bytearray([0x00 for _ in range(0x46)])
    extra_tokens = bytearray([0x00 for _ in range(0x1C)])

    for new_entrance, new_exit in world.transition_pairs.items():
        old_entrance = tr_keys[tr_values.index(new_exit)]
        old_exit = smw_transition_pairs[new_entrance]

        offset = smw_transition_data[old_entrance][0] * 0x05
        tokens[offset:offset+5] = bytearray(smw_transition_data[new_entrance][1:6])
        offset = smw_transition_data[old_entrance][0] * 0x02
        extra_tokens[offset:offset+2] = bytearray(smw_transition_data[new_entrance][6:8])
        offset = smw_transition_data[old_entrance][0]
        patch.write_byte(TRANSITION_DIRECTIONS_ADDR + offset, smw_transition_data[new_entrance][8])

        offset = smw_transition_data[old_exit][0] * 0x05
        tokens[offset:offset+5] = bytearray(smw_transition_data[new_exit][1:6])
        offset = smw_transition_data[old_exit][0] * 0x02
        extra_tokens[offset:offset+2] = bytearray(smw_transition_data[new_exit][6:8])
        offset = smw_transition_data[old_exit][0]
        patch.write_byte(TRANSITION_DIRECTIONS_ADDR + offset, smw_transition_data[new_exit][8])

        if new_exit in smw_offscreen_event_indexes.keys():
            offset = SILENT_EVENT_ADDR + smw_offscreen_event_indexes[new_exit][1]
            size = smw_offscreen_event_indexes[new_exit][2]
            patch.write_bytes(offset, bytearray([world.cached_connections[new_entrance] for _ in range(size)]))

    patch.write_bytes(0x219AA, tokens)
    patch.write_bytes(0x219F0, extra_tokens)
