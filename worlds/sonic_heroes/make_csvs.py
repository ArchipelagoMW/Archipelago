import csv
from importlib.resources import files

from worlds.sonic_heroes.constants import *
from worlds.sonic_heroes.csvdata import Locations





#with files(Locations).joinpath(f"{LOCATIONS}.csv").open() as csv_file:


region_headers = \
[
    TEAM,
    LEVEL,
    NAME,
    OBJCHECKS,
]

connnection_headers = \
[
    TEAM,
    LEVEL,
    SOURCE,
    TARGET,
    RULE,
    NOTES,
]


def write_region_data(reg_team: str, reg_level: str, keys: int, checkpoints: int):
    with open(f"{reg_level}{reg_team}Regions.csv".replace(" ", ""), "w", newline="") as region_csv_file:
        writer = csv.DictWriter(region_csv_file, region_headers)
        writer.writeheader()
        data = \
        [
            {
                TEAM: reg_team,
                LEVEL: reg_level,
                NAME: "Start",
                OBJCHECKS: 0,
            },
            {
                TEAM: reg_team,
                LEVEL: reg_level,
                NAME: "ObjSanity",
                OBJCHECKS: 0,
            },
        ]
        for key in range(keys):
            data.append(
                {
                    TEAM: reg_team,
                    LEVEL: reg_level,
                    NAME: f"Bonus Key {key + 1}",
                    OBJCHECKS: 0,
                }
            )
        for checkpoint in range(checkpoints):
            data.append(
                {
                    TEAM: reg_team,
                    LEVEL: reg_level,
                    NAME: f"Checkpoint {checkpoint + 1}",
                    OBJCHECKS: 0,
                }
            )
        data.append(
            {
                TEAM: reg_team,
                LEVEL: reg_level,
                NAME: "Goal",
                OBJCHECKS: 0,
            }
        )

        for y in data:
            writer.writerow(y)





def write_connection_data(con_team: str, con_level: str, keys: int, checkpoints: int):
    with open(f"{con_level}{con_team}Connections.csv".replace(" ", ""), "w", newline="") as connection_csv_file:
        writer = csv.DictWriter(connection_csv_file, connnection_headers)
        writer.writeheader()
        data = \
        [
            {
                TEAM: con_team,
                LEVEL: con_level,
                SOURCE: "Start",
                TARGET: f"ObjSanity",
                RULE: "",
                NOTES: "",
            },
            {
                TEAM: con_team,
                LEVEL: con_level,
                SOURCE: "ObjSanity",
                TARGET: f"Start",
                RULE: "",
                NOTES: "",
            },
        ]

        for key in range(keys):
            data.append(
                {
                    TEAM: con_team,
                    LEVEL: con_level,
                    SOURCE: "Start",
                    TARGET: f"Bonus Key {key + 1}",
                    RULE: "",
                    NOTES: "",
                }
            )
            data.append(
                {
                    TEAM: con_team,
                    LEVEL: con_level,
                    SOURCE: f"Bonus Key {key + 1}",
                    TARGET: f"Start",
                    RULE: "",
                    NOTES: "",
                }
            )
        for checkpoint in range(checkpoints):
            data.append(
                {
                    TEAM: con_team,
                    LEVEL: con_level,
                    SOURCE: "Start",
                    TARGET: f"Checkpoint {checkpoint + 1}",
                    RULE: "",
                    NOTES: "",
                }
            )
            data.append(
                {
                    TEAM: con_team,
                    LEVEL: con_level,
                    SOURCE: f"Checkpoint {checkpoint + 1}",
                    TARGET: f"Start",
                    RULE: "",
                    NOTES: "",
                }
            )
        data.append(
            {
                TEAM: con_team,
                LEVEL: con_level,
                SOURCE: f"Start",
                TARGET: f"Goal",
                RULE: "",
                NOTES: "",
            }
        )
        for y in data:
            writer.writerow(y)



for team in item_teams:
    if team != SONIC and team != ANYTEAM and team != SUPERHARDMODE:
        for level in level_to_game_region.keys():
            num_keys = 0
            num_checkpoints = 0

            with files(Locations).joinpath(f"{LOCATIONS}.csv").open() as csv_file:
                reader = csv.DictReader(csv_file)
                for x in reader:
                    if x[TEAM] == team:
                        if x[LEVEL] == level:
                            if x[LOCATIONTYPE] == KEYSANITY and int(x[ACT]) == 2:
                                num_keys += 1
                            if x[LOCATIONTYPE] == CHECKPOINTSANITY and int(x[ACT]) == 2:
                                num_checkpoints += 1

            #Super Secret Hidden Key
            if team == ROSE and level == CASINOPARK:
                num_keys -= 1


            #region
            write_region_data(team, level, num_keys, num_checkpoints)

            #connection
            write_connection_data(team, level, num_keys, num_checkpoints)
""""""
