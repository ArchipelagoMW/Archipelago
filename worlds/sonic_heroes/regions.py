from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from worlds.sonic_heroes.options import UnlockType

from typing import Optional

from BaseClasses import Entrance, Region, CollectionState
from .constants import *
from .locations import *


class SonicHeroesRegion(Region):
    game = SONICHEROES

def create_single_region_csv_entry(world: SonicHeroesWorld, team: str, level: str, name: str, obj_checks: int):
    reg = RegionCSVData(team, level, name, obj_checks)
    world.region_list.append(reg)
    world.region_to_location[reg.name] = []


def create_special_region_csv_data(world: SonicHeroesWorld):
    create_single_region_csv_entry(world, ANYTEAM, METALMADNESS, METALMADNESS, 0)
    for name in bonus_and_emerald_stages:
        create_single_region_csv_entry(world, ANYTEAM, name, name, 0)

    #world.logic_mapping_dict[ANYTEAM] = world.init_logic_mapping_any_team()
    world.init_full_logic_mapping_defaults()




def handle_single_emerald_connection(world: SonicHeroesWorld, team: str, name: str):
    #index = 1 if world.secret else 0
    target_region_end = EMERALDSTAGE if bonus_emerald_stage_to_level[name] in emerald_levels else BONUSSTAGE

    if bonus_emerald_stage_to_level[name] in world.allowed_levels_per_team[team]:
        emerald_conn_name = f"{team} {bonus_emerald_stage_to_level[name]} Bonus Key and Goal"
        emerald_rule = lambda state: state.has_from_list_unique(world.bonus_key_event_items_per_team[team][
            bonus_emerald_stage_to_level[name]], world.player, world.bonus_keys_needed_for_bonus_stage) and state.has(
            f"{team} {bonus_emerald_stage_to_level[name]} {COMPLETIONEVENT}", world.player)
        emerald_rule_str = f"{world.bonus_keys_needed_for_bonus_stage} Bonus Keys and Goal"

        if team == SUPERHARDMODE:
            emerald_conn_name = f"{team} {bonus_emerald_stage_to_level[name]} Goal (No Keys Needed)"
            emerald_rule = lambda state: True
            emerald_rule_str = "Reach Goal"


        connect(world, emerald_conn_name,
                f"{bonus_emerald_stage_to_level[name]} {team} Goal",
                f"{bonus_emerald_stage_to_level[name]} {target_region_end}", emerald_rule,
                rule_to_str=emerald_rule_str)
    return



def handle_emerald_connections(world: SonicHeroesWorld, team: str):
    for name in bonus_and_emerald_stages:
        handle_single_emerald_connection(world, team, name)



def create_region(world: SonicHeroesWorld, name: str, hint: str = ""):
    region = SonicHeroesRegion(name, world.player, world.multiworld)
    #print(f"Boss_Locations: {world.boss_locations_added}")
    create_locations(world, region)

    if name == METALOVERLORD:
        location = SonicHeroesLocation(world.player, VICTORYLOCATION, None, region)
        region.locations.append(location)

    if world.options.unlock_type == UnlockType.option_legacy_level_gates:

        #for boss_name in world.boss_locations_added:
            #if boss_name in name:
        if name in world.boss_locations_added:
            #print(f"Creating Event Location: {name} Event Location")
            location = SonicHeroesLocation(world.player, f"{name} Event Location", None, region)
            region.locations.append(location)


    #Seaside Hill (Team) Goal
    #Seaside Hill (Team) Bonus Key 1
    name_split = name.split(" ")

    if len(name_split) > 3:
        if name_split[-2] == "Key":
            if name_split[-3] == "Bonus":
                for team in world.enabled_teams:
                    last_word_of_team = team.split(" ")[-1]
                    if name_split[-4] == last_word_of_team:
                        level_name = name_split[0] + " " + name_split[1]
                        #this should be a bonus key region
                        #print(f"I think this is a bonus key region: {name}")
                        location = SonicHeroesLocation(world.player, f"{level_name} {team} Bonus Key {int(name_split[-1])} Event", None, region)
                        region.locations.append(location)





    if name_split[-1] == "Goal":
        for team in world.enabled_teams:
            last_word_of_team = team.split(" ")[-1]
            if name_split[-2] == last_word_of_team:
                level_name = name_split[0] + " " + name_split[1]
                if level_name in world.allowed_levels_per_team[team]:
                    #level completions globally
                    location = SonicHeroesLocation(world.player, f"{name} Event Location", None, region)
                    region.locations.append(location)


                    #level completions per team
                    location = SonicHeroesLocation(world.player, f"{name} Event Location For Team", None, region)
                    region.locations.append(location)
                    world.team_level_goal_event_locations[team].append(level_name)


    world.multiworld.regions.append(region)


def create_regions(world: SonicHeroesWorld):
    create_region(world, MENU, MENUREGIONHINT)
    create_region(world, METALOVERLORD, METALMADNESSREGIONHINT)


    if world.options.unlock_type == UnlockType.option_legacy_level_gates:
        for level_group in range(len(world.gate_level_counts)):
            create_region(world, f"Gate {level_group}", f"This is Gate {level_group}")

            if level_group < len(world.gate_level_counts) - 1:
                #dont create if on last gate
                reg_name = f"Gate {level_group} Boss: {sonic_heroes_extra_names[int(world.shuffled_bosses[level_group][1:]) - 16]}"
                #reg_name = {sonic_heroes_extra_names[int(world.shuffled_bosses[level_group][1:]) - 16]}
                create_region(world, reg_name, f"{reg_name} Hint")
                create_region(world, sonic_heroes_extra_names[int(world.shuffled_bosses[level_group][1:]) - 16], f"{sonic_heroes_extra_names[int(world.shuffled_bosses[level_group][1:]) - 16]} Hint")


    create_regions_from_region_list(world)
    pass


def create_regions_from_region_list(world: SonicHeroesWorld):
    #world.region_list = []
    for reg in world.region_list:
        create_region(world, reg.name)
    pass

def get_rule_for_gate_after_prev_gate_boss(world: SonicHeroesWorld, state: CollectionState, gate_number: int):
    if gate_number == 0:
        return True
    #print(f"Gate_Number: {gate_number} :: Boss Locations: {world.boss_locations_added}")
    return state.has(f"Gate {gate_number - 1} Boss: {world.boss_locations_added[gate_number - 1]}", world.player)


def get_rule_str_for_gate_after_prev_gate_boss(world: SonicHeroesWorld, gate_number: int):
    if gate_number == 0:
        return "Gate 0 Unlocked from Start"
    return f"Beat Gate {gate_number - 1} Boss: {world.boss_locations_added[gate_number - 1]}"

def get_rule_for_gate_boss(world: SonicHeroesWorld, state: CollectionState, gate_number: int):
    #print(f"Gate {gate_number} Boss Needs {world.gate_emblem_costs[gate_number]} Emblems")
    return state.has(EMBLEM, world.player, world.gate_emblem_costs[gate_number])

def get_rule_to_str_for_gate_boss(world: SonicHeroesWorld, gate_number: int):
    return f"{world.gate_emblem_costs[gate_number]} Emblem Cost"





def connect_level_gate_entrances(world: SonicHeroesWorld) -> str:

    print(f"Gate Emblem Costs: {world.gate_emblem_costs}")
    print(f"Gate Level Counts: {world.gate_level_counts}")

    current_gate_boss = MENU

    shuffled_levels_copy: list[str] = world.shuffled_levels.copy()

    for gate_num in range(len(world.gate_level_counts)):
        if gate_num == 0:
            # connect Menu to Gate 0
            connect(world, f"{MENU} -> Gate {gate_num}", MENU, f"Gate {gate_num}", None,
                    rule_to_str="None")

        if gate_num < len(world.gate_level_counts) - 1:

            #boss region name
            current_gate_boss = f"Gate {gate_num} Boss: {sonic_heroes_extra_names[int(world.shuffled_bosses[gate_num][1:]) - 16]}"
            current_boss_name = sonic_heroes_extra_names[int(world.shuffled_bosses[gate_num][1:]) - 16]

            #connect Gate to its boss (Gate 0 -> Gate 0 Boss)
            connect(world, f"Gate {gate_num} -> {current_gate_boss}", f"Gate {gate_num}", current_gate_boss, lambda state, gate=gate_num: get_rule_for_gate_boss(world, state, gate),
                    rule_to_str=get_rule_to_str_for_gate_boss(world, gate_num))
            #connect gate num + boss to boss (for locations)
            connect(world, f"{current_gate_boss} -> {current_boss_name}", current_gate_boss, current_boss_name, None, rule_to_str="")


            #Connect Gate Boss to next Gate (Gate 0 Boss -> Gate 1)
            #final boss is done separately
            connect(world, f"{current_gate_boss} -> Gate {gate_num + 1}", current_gate_boss, f"Gate {gate_num + 1}", lambda state, gate=gate_num: get_rule_for_gate_after_prev_gate_boss(world, state, gate + 1), rule_to_str=get_rule_str_for_gate_after_prev_gate_boss(world, gate_num + 1))


        for _ in range(world.gate_level_counts[gate_num]):
            #now do each level for gate
            #print(f"Gate: {gate_num} :: Levels: {world.gate_level_counts[gate_num]}")
            current_level_entry = shuffled_levels_copy.pop(0)
            current_team = team_code_to_team[current_level_entry[0]]
            current_level = sonic_heroes_level_names[int(current_level_entry[1:]) - 1]

            if current_team == SONIC and not world.is_this_team_enabled(SONIC):
                current_team = SUPERHARDMODE

            connect(world, f"Gate {gate_num} -> {current_level} {current_team} Start", f"Gate {gate_num}", f"{current_level} {current_team} Start",
                    lambda state: True,
                    rule_to_str="")

            if current_team == SONIC and world.is_this_team_enabled(SUPERHARDMODE):
                connect(world, f"Gate {gate_num} -> {current_level} {SUPERHARDMODE} Start", f"Gate {gate_num}",
                        f"{current_level} {SUPERHARDMODE} Start",
                        lambda state: True,
                        rule_to_str="")

    return current_gate_boss


def connect_entrances(world: SonicHeroesWorld):

    goal_rule = lambda state: get_goal_rule(world, state)

    for team in world.enabled_teams:
        handle_emerald_connections(world, team)
        if world.options.unlock_type != UnlockType.option_legacy_level_gates:
            for reg in world.allowed_levels_per_team[team]:
                connect(world,f"{MENU} -> {reg} {team} Start", MENU, f"{reg} {team} Start", None, rule_to_str="None")

    final_boss_entrance_region_name = MENU

    if world.options.unlock_type == UnlockType.option_legacy_level_gates:
        final_boss_entrance_region_name = connect_level_gate_entrances(world)


    #connect(world, f"{MENU} -> {SEASIDEHILL} {SONIC} Start", MENU, f"{SEASIDEHILL} {SONIC} Start", None, rule_to_str="None")


    connect(world, f"Goal Connection", final_boss_entrance_region_name, METALMADNESS, goal_rule, rule_to_str=f"Goal Rule")
    connect(world, f"Goal Connection 2", METALMADNESS, METALOVERLORD, goal_rule, rule_to_str=f"Goal Rule")

    connect_entrances_from_connection_list(world)
    pass


def connect_entrances_from_connection_list(world: SonicHeroesWorld):
    for connection in world.connection_list:
        connect(world, connection.name, connection.source, connection.target, world.full_logic_mapping_dict[connection.rulestr], rule_to_str=connection.rulestr)

        #world.logic_mapping_dict[connection.team][connection.level][connection.rulestr]



def connect(world: SonicHeroesWorld, name: str, source: str, target: str, rule = None, reach: Optional[bool] = False, rule_to_str: Optional[str] = None) -> Optional[Entrance]:
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)

    #world.spoiler_string += f"\nConnecting Region {source} to Region {target} with rule: {rule_to_str}\n"
    #print(f"\nConnecting Region {source} to Region {target} with rule: {rule_to_str}\n")

    return connection if reach else None


def get_goal_rule(world: SonicHeroesWorld, state: CollectionState):
    goal_rule_dict: dict[str, int] = {}
    level_completion_items_dict: dict[str, list[str]] = {}

    for team in world.enabled_teams:
        level_completion_items_dict[team] = []

        if world.options.unlock_type == UnlockType.option_ability_character_unlocks:
            for char_name in team_char_names[team]:
                goal_rule_dict[get_playable_char_item_name(char_name)] = 1

        if LEVELCOMPLETIONSPERSTORY in world.options.goal_unlock_conditions:
            for name in world.team_level_goal_event_locations[team]:
                level_completion_items_dict[team].append(f"{team} {name} {COMPLETIONEVENT}")

    if EMERALDS in world.options.goal_unlock_conditions:
        for emerald in emeralds:
            goal_rule_dict[emerald] = 1



    level_completions_all_teams = True
    if LEVELCOMPLETIONSALLTEAMS in world.options.goal_unlock_conditions:
        level_completions_all_teams = state.has(f"{LEVEL} {COMPLETIONEVENT}", world.player, world.options.goal_level_completions.value)

    goal_rule_levels = {SONIC: True, DARK: True, ROSE: True, CHAOTIX: True, SUPERHARDMODE: True}
    if LEVELCOMPLETIONSPERSTORY in world.options.goal_unlock_conditions:
        teams_list = level_completion_items_dict.keys()
        if SONIC in teams_list:
            goal_rule_levels[SONIC] = state.has_from_list_unique(level_completion_items_dict[SONIC], world.player,world.options.goal_level_completions_per_story.value)
        if DARK in teams_list:
            goal_rule_levels[DARK] = state.has_from_list_unique(level_completion_items_dict[DARK], world.player,world.options.goal_level_completions_per_story.value)
        if ROSE in teams_list:
            goal_rule_levels[ROSE] = state.has_from_list_unique(level_completion_items_dict[ROSE], world.player,world.options.goal_level_completions_per_story.value)
        if CHAOTIX in teams_list:
            goal_rule_levels[CHAOTIX] = state.has_from_list_unique(level_completion_items_dict[CHAOTIX], world.player,world.options.goal_level_completions_per_story.value)
        if SUPERHARDMODE in teams_list:
            goal_rule_levels[SUPERHARDMODE] = state.has_from_list_unique(level_completion_items_dict[SUPERHARDMODE], world.player, world.options.goal_level_completions_per_story.value)

    goal_rule_items = state.has_all_counts(goal_rule_dict, world.player)



    return goal_rule_items and level_completions_all_teams and goal_rule_levels[SONIC] and goal_rule_levels[DARK] and goal_rule_levels[ROSE] and goal_rule_levels[CHAOTIX] and goal_rule_levels[SUPERHARDMODE]