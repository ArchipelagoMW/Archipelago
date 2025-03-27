import typing
import copy

from BaseClasses import MultiWorld
from worlds.AutoWorld import World


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

### 0: Sonic
### 1: Tails
### 2: Knuckles
### 3: Shadow
### 4: Eggman
### 5: Rouge
### 6: Kart
### 7: Cannon's Core
level_styles: typing.List[int] = [
    0,
    2,
    1,
    0,
    0,
    2,
    1,
    2,
    6,
    1,
    0,
    2,
    1,
    2,
    0,
    0,

    4,
    5,
    4,
    3,
    5,
    4,
    4,
    5,
    3,
    6,
    3,
    5,
    4,
    3,

    7,
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
    "Cannon's Core - ",
]

def get_mission_count_table(multiworld: MultiWorld, world: World, player: int):
    mission_count_table: typing.Dict[int, int] = {}

    if world.options.goal == 3:
        for level in range(31):
            mission_count_table[level] = 0
    else:
        sonic_active_missions = 1
        tails_active_missions = 1
        knuckles_active_missions = 1
        shadow_active_missions = 1
        eggman_active_missions = 1
        rouge_active_missions = 1
        kart_active_missions = 1
        cannons_core_active_missions = 1

        for i in range(2,6):
            if getattr(world.options, "sonic_mission_" + str(i), None):
                sonic_active_missions += 1

            if getattr(world.options, "tails_mission_" + str(i), None):
                tails_active_missions += 1

            if getattr(world.options, "knuckles_mission_" + str(i), None):
                knuckles_active_missions += 1

            if getattr(world.options, "shadow_mission_" + str(i), None):
                shadow_active_missions += 1

            if getattr(world.options, "eggman_mission_" + str(i), None):
                eggman_active_missions += 1

            if getattr(world.options, "rouge_mission_" + str(i), None):
                rouge_active_missions += 1

            if getattr(world.options, "kart_mission_" + str(i), None):
                kart_active_missions += 1

            if getattr(world.options, "cannons_core_mission_" + str(i), None):
                cannons_core_active_missions += 1

        sonic_active_missions        = min(sonic_active_missions, world.options.sonic_mission_count.value)
        tails_active_missions        = min(tails_active_missions, world.options.tails_mission_count.value)
        knuckles_active_missions     = min(knuckles_active_missions, world.options.knuckles_mission_count.value)
        shadow_active_missions       = min(shadow_active_missions, world.options.sonic_mission_count.value)
        eggman_active_missions       = min(eggman_active_missions, world.options.eggman_mission_count.value)
        rouge_active_missions        = min(rouge_active_missions, world.options.rouge_mission_count.value)
        kart_active_missions         = min(kart_active_missions, world.options.kart_mission_count.value)
        cannons_core_active_missions = min(cannons_core_active_missions, world.options.cannons_core_mission_count.value)

        active_missions: typing.List[typing.List[int]] = [
            sonic_active_missions,
            tails_active_missions,
            knuckles_active_missions,
            shadow_active_missions,
            eggman_active_missions,
            rouge_active_missions,
            kart_active_missions,
            cannons_core_active_missions
        ]

        for level in range(31):
            level_style = level_styles[level]
            level_mission_count = active_missions[level_style]
            mission_count_table[level] = level_mission_count

    return mission_count_table


def get_mission_table(multiworld: MultiWorld, world: World, player: int):
    mission_table: typing.Dict[int, int] = {}

    if world.options.goal == 3:
        for level in range(31):
            mission_table[level] = 0
    else:
        sonic_active_missions: typing.List[int] = [1]
        tails_active_missions: typing.List[int] = [1]
        knuckles_active_missions: typing.List[int] = [1]
        shadow_active_missions: typing.List[int] = [1]
        eggman_active_missions: typing.List[int] = [1]
        rouge_active_missions: typing.List[int] = [1]
        kart_active_missions: typing.List[int] = [1]
        cannons_core_active_missions: typing.List[int] = [1]

        # Add included missions
        for i in range(2,6):
            if getattr(world.options, "sonic_mission_" + str(i), None):
                sonic_active_missions.append(i)

            if getattr(world.options, "tails_mission_" + str(i), None):
                tails_active_missions.append(i)

            if getattr(world.options, "knuckles_mission_" + str(i), None):
                knuckles_active_missions.append(i)

            if getattr(world.options, "shadow_mission_" + str(i), None):
                shadow_active_missions.append(i)

            if getattr(world.options, "eggman_mission_" + str(i), None):
                eggman_active_missions.append(i)

            if getattr(world.options, "rouge_mission_" + str(i), None):
                rouge_active_missions.append(i)

            if getattr(world.options, "kart_mission_" + str(i), None):
                kart_active_missions.append(i)

            if getattr(world.options, "cannons_core_mission_" + str(i), None):
                cannons_core_active_missions.append(i)

        active_missions: typing.List[typing.List[int]] = [
            sonic_active_missions,
            tails_active_missions,
            knuckles_active_missions,
            shadow_active_missions,
            eggman_active_missions,
            rouge_active_missions,
            kart_active_missions,
            cannons_core_active_missions
        ]

        for level in range(31):
            level_style = level_styles[level]

            level_active_missions: typing.List[int] = copy.deepcopy(active_missions[level_style])
            level_chosen_missions: typing.List[int] = []

            # The first mission must be M1, M2, M3, or M4
            first_mission = 1
            first_mission_options = [1, 2, 3]

            if not world.options.animalsanity:
                first_mission_options.append(4)

            if world.options.mission_shuffle:
                first_mission = multiworld.random.choice([mission for mission in level_active_missions if mission in first_mission_options])

            level_active_missions.remove(first_mission)

            # Place Active Missions in the chosen mission list
            for mission in level_active_missions:
                if mission not in level_chosen_missions:
                    level_chosen_missions.append(mission)

            if world.options.mission_shuffle:
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


def print_mission_orders_to_spoiler(mission_map: typing.Dict[int, int],
                                    mission_count_map: typing.Dict[int, int],
                                    shuffled_region_list: typing.Dict[int, int],
                                    levels_per_gate: typing.Dict[int, int],
                                    player_name: str,
                                    spoiler_handle: typing.TextIO):
    spoiler_handle.write("\n")
    header_text = "SA2 Mission Orders for {}:\n"
    header_text = header_text.format(player_name)
    spoiler_handle.write(header_text)

    level_index = 0
    for gate_idx in range(len(levels_per_gate)):
        gate_len = levels_per_gate[gate_idx]
        gate_levels = shuffled_region_list[int(level_index):int(level_index+gate_len)]
        gate_levels.sort()

        gate_text = "Gate {}:\n"
        gate_text = gate_text.format(gate_idx)
        spoiler_handle.write(gate_text)

        for i in range(len(gate_levels)):
            stage = gate_levels[i]
            mission_count = mission_count_map[stage]
            mission_order: typing.List[int] = mission_orders[mission_map[stage]]
            stage_prefix: str = stage_name_prefixes[stage]

            for mission in range(mission_count):
                stage_prefix += str(mission_order[mission]) + " "

            spoiler_handle.write(stage_prefix)
            spoiler_handle.write("\n")

        level_index += gate_len
        spoiler_handle.write("\n")

    mission_count = mission_count_map[30]
    mission_order: typing.List[int] = mission_orders[mission_map[30]]
    stage_prefix: str = stage_name_prefixes[30]

    for mission in range(mission_count):
        stage_prefix += str(mission_order[mission]) + " "

    spoiler_handle.write(stage_prefix)
    spoiler_handle.write("\n\n")
