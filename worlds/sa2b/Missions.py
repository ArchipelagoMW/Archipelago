import typing
import copy

from BaseClasses import MultiWorld


mission_orders: typing.List[typing.List[int]] = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 5, 4],
    [1, 2, 4, 3, 5],
    [1, 2, 4, 5, 3],
    [1, 2, 5, 3, 4],
    [1, 2, 5, 4, 3],

    [1, 3, 2, 4, 5],
    [1, 3, 2, 5, 4],
    [1, 3, 4, 2, 5],
    [1, 3, 4, 5, 2],
    [1, 3, 5, 2, 4],
    [1, 3, 5, 4, 2],

    [1, 4, 2, 3, 5],
    [1, 4, 2, 5, 3],
    [1, 4, 3, 2, 5],
    [1, 4, 3, 5, 2],
    [1, 4, 5, 2, 3],
    [1, 4, 5, 3, 2],

    [1, 5, 2, 3, 4],
    [1, 5, 2, 4, 3],
    [1, 5, 3, 2, 4],
    [1, 5, 3, 4, 2],
    [1, 5, 4, 2, 3],
    [1, 5, 4, 3, 2],

    [2, 1, 3, 4, 5],
    [2, 1, 3, 5, 4],
    [2, 1, 4, 3, 5],
    [2, 1, 4, 5, 3],
    [2, 1, 5, 3, 4],
    [2, 1, 5, 4, 3],

    [2, 3, 1, 4, 5],
    [2, 3, 1, 5, 4],
    [2, 3, 4, 1, 5],
    [2, 3, 4, 5, 1],
    [2, 3, 5, 1, 4],
    [2, 3, 5, 4, 1],

    [2, 4, 1, 3, 5],
    [2, 4, 1, 5, 3],
    [2, 4, 3, 1, 5],
    [2, 4, 3, 5, 1],
    [2, 4, 5, 1, 3],
    [2, 4, 5, 3, 1],

    [2, 5, 1, 3, 4],
    [2, 5, 1, 4, 3],
    [2, 5, 3, 1, 4],
    [2, 5, 3, 4, 1],
    [2, 5, 4, 1, 3],
    [2, 5, 4, 3, 1],

    [3, 1, 2, 4, 5],
    [3, 1, 2, 5, 4],
    [3, 1, 4, 2, 5],
    [3, 1, 4, 5, 2],
    [3, 1, 5, 4, 2],
    [3, 1, 5, 2, 4],

    [3, 2, 1, 4, 5],
    [3, 2, 1, 5, 4],
    [3, 2, 4, 1, 5],
    [3, 2, 4, 5, 1],
    [3, 2, 5, 1, 4],
    [3, 2, 5, 4, 1],

    [3, 4, 1, 2, 5],
    [3, 4, 1, 5, 2],
    [3, 4, 2, 1, 5],
    [3, 4, 2, 5, 1],
    [3, 4, 5, 1, 2],
    [3, 4, 5, 2, 1],

    [3, 5, 1, 4, 2],
    [3, 5, 1, 2, 4],
    [3, 5, 2, 1, 4],
    [3, 5, 2, 4, 1],
    [3, 5, 4, 1, 2],
    [3, 5, 4, 2, 1],

    [4, 1, 2, 3, 5],
    [4, 1, 2, 5, 3],
    [4, 1, 3, 2, 5],
    [4, 1, 3, 5, 2],
    [4, 1, 5, 3, 2],
    [4, 1, 5, 2, 3],

    [4, 2, 1, 3, 5],
    [4, 2, 1, 5, 3],
    [4, 2, 3, 1, 5],
    [4, 2, 3, 5, 1],
    [4, 2, 5, 1, 3],
    [4, 2, 5, 3, 1],

    [4, 3, 1, 2, 5],
    [4, 3, 1, 5, 2],
    [4, 3, 2, 1, 5],
    [4, 3, 2, 5, 1],
    [4, 3, 5, 1, 2],
    [4, 3, 5, 2, 1],

    [4, 5, 1, 3, 2],
    [4, 5, 1, 2, 3],
    [4, 5, 2, 1, 3],
    [4, 5, 2, 3, 1],
    [4, 5, 3, 1, 2],
    [4, 5, 3, 2, 1],
]

### 0: Speed
### 1: Mech
### 2: Hunt
### 3: Kart
### 4: Cannon's Core
level_styles: typing.List[int] = [
    0,
    2,
    1,
    0,
    0,
    2,
    1,
    2,
    3,
    1,
    0,
    2,
    1,
    2,
    0,
    0,

    1,
    2,
    1,
    0,
    2,
    1,
    1,
    2,
    0,
    3,
    0,
    2,
    1,
    0,

    4,
]

stage_name_prefixes: typing.List[str] = [
    "City Escape - ",
    "Wild Canyon - ",
    "Prison Lane - ",
    "Metal Harbor - ",
    "Green Forest - ",
    "Pumpkin Hill - ",
    "Mission Street - ",
    "Aquatic Mine - ",
    "Route 101 - ",
    "Hidden Base - ",
    "Pyramid Cave - ",
    "Death Chamber - ",
    "Eternal Engine - ",
    "Meteor Herd - ",
    "Crazy Gadget - ",
    "Final Rush - ",
    "Iron Gate - ",
    "Dry Lagoon - ",
    "Sand Ocean - ",
    "Radical Highway - ",
    "Egg Quarters - ",
    "Lost Colony - ",
    "Weapons Bed - ",
    "Security Hall - ",
    "White Jungle - ",
    "Route 280 - ",
    "Sky Rail - ",
    "Mad Space - ",
    "Cosmic Wall - ",
    "Final Chase - ",
    "Cannon Core - ",
]

def get_mission_count_table(multiworld: MultiWorld, player: int):
    speed_active_missions = 1
    mech_active_missions = 1
    hunt_active_missions = 1
    kart_active_missions = 1
    cannons_core_active_missions = 1

    for i in range(2,6):
        if getattr(multiworld, "speed_mission_" + str(i), None)[player]:
            speed_active_missions += 1

        if getattr(multiworld, "mech_mission_" + str(i), None)[player]:
            mech_active_missions += 1

        if getattr(multiworld, "hunt_mission_" + str(i), None)[player]:
            hunt_active_missions += 1

        if getattr(multiworld, "kart_mission_" + str(i), None)[player]:
            kart_active_missions += 1

        if getattr(multiworld, "cannons_core_mission_" + str(i), None)[player]:
            cannons_core_active_missions += 1

    speed_active_missions        = min(speed_active_missions, multiworld.speed_mission_count[player].value)
    mech_active_missions         = min(mech_active_missions, multiworld.mech_mission_count[player].value)
    hunt_active_missions         = min(hunt_active_missions, multiworld.hunt_mission_count[player].value)
    kart_active_missions         = min(kart_active_missions, multiworld.kart_mission_count[player].value)
    cannons_core_active_missions = min(cannons_core_active_missions, multiworld.cannons_core_mission_count[player].value)

    active_missions: typing.List[typing.List[int]] = [
        speed_active_missions,
        mech_active_missions,
        hunt_active_missions,
        kart_active_missions,
        cannons_core_active_missions
    ]

    mission_count_table: typing.Dict[int, int] = {}

    for level in range(31):
        level_style = level_styles[level]
        level_mission_count = active_missions[level_style]
        mission_count_table[level] = level_mission_count

    return mission_count_table


def get_mission_table(multiworld: MultiWorld, player: int):
    mission_table: typing.Dict[int, int] = {}

    speed_active_missions: typing.List[int] = [1]
    mech_active_missions: typing.List[int] = [1]
    hunt_active_missions: typing.List[int] = [1]
    kart_active_missions: typing.List[int] = [1]
    cannons_core_active_missions: typing.List[int] = [1]

    # Add included missions
    for i in range(2,6):
        if getattr(multiworld, "speed_mission_" + str(i), None)[player]:
            speed_active_missions.append(i)

        if getattr(multiworld, "mech_mission_" + str(i), None)[player]:
            mech_active_missions.append(i)

        if getattr(multiworld, "hunt_mission_" + str(i), None)[player]:
            hunt_active_missions.append(i)

        if getattr(multiworld, "kart_mission_" + str(i), None)[player]:
            kart_active_missions.append(i)

        if getattr(multiworld, "cannons_core_mission_" + str(i), None)[player]:
            cannons_core_active_missions.append(i)

    active_missions: typing.List[typing.List[int]] = [
        speed_active_missions,
        mech_active_missions,
        hunt_active_missions,
        kart_active_missions,
        cannons_core_active_missions
    ]

    for level in range(31):
        level_style = level_styles[level]

        level_active_missions: typing.List[int] = copy.deepcopy(active_missions[level_style])
        level_chosen_missions: typing.List[int] = []

        # The first mission must be M1, M2, or M4
        first_mission = 1

        if multiworld.mission_shuffle[player]:
            first_mission = multiworld.random.choice([mission for mission in level_active_missions if mission in [1, 2, 3, 4]])

        level_active_missions.remove(first_mission)

        # Place Active Missions in the chosen mission list
        for mission in level_active_missions:
            if mission not in level_chosen_missions:
                level_chosen_missions.append(mission)

        if multiworld.mission_shuffle[player]:
            multiworld.random.shuffle(level_chosen_missions)

        level_chosen_missions.insert(0, first_mission)

        # Fill in the non-included missions
        for i in range(2,6):
            if i not in level_chosen_missions:
                level_chosen_missions.append(i)

        # Determine which mission order index we have, for conveying to the mod
        for i in range(len(mission_orders)):
            if mission_orders[i] == level_chosen_missions:
                level_mission_index = i
                break

        mission_table[level] = level_mission_index

    return mission_table


def get_first_and_last_cannons_core_missions(mission_map: typing.Dict[int, int], mission_count_map: typing.Dict[int, int]):
        mission_count = mission_count_map[30]
        mission_order: typing.List[int] = mission_orders[mission_map[30]]
        stage_prefix: str = stage_name_prefixes[30]

        first_mission_number = mission_order[0]
        last_mission_number = mission_order[mission_count - 1]
        first_location_name: str = stage_prefix + str(first_mission_number)
        last_location_name: str = stage_prefix + str(last_mission_number)

        return first_location_name, last_location_name
