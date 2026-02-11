import csv
from typing import Any
from worlds.sonic_heroes.constants import *

rule_list: list[str] = ["BreakKeyCage"]
team_list: list[str] = ["Sonic"]
level_strs: list[str] = ["SH", "OP", "GM", "PP", "CP", "BH", "RC", "BS", "Frog", "LJ", "HC", "MM", "EF", "Final"]
team_level_strs: list[str] = [f"{SONIC}{x}" for x in level_strs]
levels: list[str] = [x for x in sonic_heroes_level_names.values()]
completed_rule_list: list[str] = [f"BreakKeyCageSonic{x}" for x in level_strs]

def handle_sonic_connection_csv_file(level: str):
    file_name = get_csv_file_name(SONIC, level, CONNECTIONS)
    with open(f"{file_name}.csv", mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for x in reader:
            rule = x[RULE]
            handle_rule_str(rule, level)


def handle_rule_str(rule: str, level: str):
    if rule == "" or rule == "NOTPOSSIBLE":
        return

    print(rule)
    found_team_level: bool = False
    team_level: str = ""

    for team_lvl in team_level_strs:
        if team_lvl in rule:
            found_team_level = True
            team_level = team_lvl
            break
    short_rule = rule.replace(team_level, "")

    index: int = 0
    list_size: int = len(rule_list)
    while index < list_size:
        if short_rule in rule_list[index] and short_rule != rule_list[index]:
            print(f"Collision between {short_rule} and {rule_list[index]}")
        index += 1

    if short_rule not in rule_list:
        rule_list.append(short_rule)


handle_sonic_connection_csv_file(SEASIDEHILL)

#for level in levels:
    #handle_sonic_connection_csv_file(level)