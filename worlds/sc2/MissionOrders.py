from .MissionTables import FillMission, MissionPools, MissionConnection, SC2Campaign
from typing import Dict, List
import math

from worlds.AutoWorld import World


def vanilla_shuffle_order() -> Dict[SC2Campaign, List[FillMission]]:
    return {
        SC2Campaign.WOL: [
            FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.WOL)], "Mar Sara", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.WOL)], "Mar Sara", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(1, SC2Campaign.WOL)], "Mar Sara", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(2, SC2Campaign.WOL)], "Colonist"),
            FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.WOL)], "Colonist"),
            FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.WOL)], "Colonist", number=7),
            FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.WOL)], "Colonist", number=7, removal_priority=1),
            FillMission(MissionPools.EASY, [MissionConnection(2, SC2Campaign.WOL)], "Artifact", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(7, SC2Campaign.WOL)], "Artifact", number=8, completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(8, SC2Campaign.WOL)], "Artifact", number=11, completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(9, SC2Campaign.WOL)], "Artifact", number=14, completion_critical=True, removal_priority=7),
            FillMission(MissionPools.HARD, [MissionConnection(10, SC2Campaign.WOL)], "Artifact", completion_critical=True, removal_priority=6),
            FillMission(MissionPools.MEDIUM, [MissionConnection(2, SC2Campaign.WOL)], "Covert", number=4),
            FillMission(MissionPools.MEDIUM, [MissionConnection(12, SC2Campaign.WOL)], "Covert"),
            FillMission(MissionPools.HARD, [MissionConnection(13, SC2Campaign.WOL)], "Covert", number=8, removal_priority=3),
            FillMission(MissionPools.HARD, [MissionConnection(13, SC2Campaign.WOL)], "Covert", number=8, removal_priority=2),
            FillMission(MissionPools.MEDIUM, [MissionConnection(2, SC2Campaign.WOL)], "Rebellion", number=6),
            FillMission(MissionPools.HARD, [MissionConnection(16, SC2Campaign.WOL)], "Rebellion"),
            FillMission(MissionPools.HARD, [MissionConnection(17, SC2Campaign.WOL)], "Rebellion"),
            FillMission(MissionPools.HARD, [MissionConnection(18, SC2Campaign.WOL)], "Rebellion", removal_priority=8),
            FillMission(MissionPools.HARD, [MissionConnection(19, SC2Campaign.WOL)], "Rebellion", removal_priority=5),
            FillMission(MissionPools.HARD, [MissionConnection(11, SC2Campaign.WOL)], "Char", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(21, SC2Campaign.WOL)], "Char", completion_critical=True, removal_priority=4),
            FillMission(MissionPools.HARD, [MissionConnection(21, SC2Campaign.WOL)], "Char", completion_critical=True),
            FillMission(MissionPools.FINAL, [MissionConnection(22, SC2Campaign.WOL), MissionConnection(23, SC2Campaign.WOL)], "Char", completion_critical=True, or_requirements=True)
        ],
        SC2Campaign.PROPHECY: [
            FillMission(MissionPools.MEDIUM, [MissionConnection(8, SC2Campaign.WOL)], "_1"),
            FillMission(MissionPools.HARD, [MissionConnection(0, SC2Campaign.PROPHECY)], "_2", removal_priority=2),
            FillMission(MissionPools.HARD, [MissionConnection(1, SC2Campaign.PROPHECY)], "_3", removal_priority=1),
            FillMission(MissionPools.FINAL, [MissionConnection(2, SC2Campaign.PROPHECY)], "_4"),
        ],
        SC2Campaign.HOTS: [
            FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.HOTS)], "Umoja", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.HOTS)], "Umoja", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(1, SC2Campaign.HOTS)], "Umoja", completion_critical=True, removal_priority=1),
            FillMission(MissionPools.EASY, [MissionConnection(2, SC2Campaign.HOTS)], "Kaldir", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.HOTS)], "Kaldir", completion_critical=True, removal_priority=2),
            FillMission(MissionPools.MEDIUM, [MissionConnection(4, SC2Campaign.HOTS)], "Kaldir", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(2, SC2Campaign.HOTS)], "Char", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(6, SC2Campaign.HOTS)], "Char", completion_critical=True, removal_priority=3),
            FillMission(MissionPools.MEDIUM, [MissionConnection(7, SC2Campaign.HOTS)], "Char", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(5, SC2Campaign.HOTS), MissionConnection(8, SC2Campaign.HOTS)], "Zerus", completion_critical=True, or_requirements=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(9, SC2Campaign.HOTS)], "Zerus", completion_critical=True, removal_priority=4),
            FillMission(MissionPools.MEDIUM, [MissionConnection(10, SC2Campaign.HOTS)], "Zerus", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(5, SC2Campaign.HOTS), MissionConnection(8, SC2Campaign.HOTS), MissionConnection(11, SC2Campaign.HOTS)], "Skygeirr Station", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(12, SC2Campaign.HOTS)], "Skygeirr Station", completion_critical=True, removal_priority=5),
            FillMission(MissionPools.HARD, [MissionConnection(13, SC2Campaign.HOTS)], "Skygeirr Station", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(5, SC2Campaign.HOTS), MissionConnection(8, SC2Campaign.HOTS), MissionConnection(11, SC2Campaign.HOTS)], "Dominion Space", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(15, SC2Campaign.HOTS)], "Dominion Space", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(14, SC2Campaign.HOTS), MissionConnection(16, SC2Campaign.HOTS)], "Korhal", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(17, SC2Campaign.HOTS)], "Korhal", completion_critical=True),
            FillMission(MissionPools.FINAL, [MissionConnection(18, SC2Campaign.HOTS)], "Korhal", completion_critical=True),
        ],
        SC2Campaign.PROLOGUE: [
            FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.PROLOGUE)], "_1"),
            FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.PROLOGUE)], "_2", removal_priority=1),
            FillMission(MissionPools.FINAL, [MissionConnection(1, SC2Campaign.PROLOGUE)], "_3")
        ],
        SC2Campaign.LOTV: [
            FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.LOTV)], "Aiur", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.LOTV)], "Aiur", completion_critical=True, removal_priority=3),
            FillMission(MissionPools.EASY, [MissionConnection(1, SC2Campaign.LOTV)], "Aiur", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(2, SC2Campaign.LOTV)], "Korhal", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.LOTV)], "Korhal", completion_critical=True, removal_priority=7),
            FillMission(MissionPools.MEDIUM, [MissionConnection(2, SC2Campaign.LOTV)], "Shakuras", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(5, SC2Campaign.LOTV)], "Shakuras", completion_critical=True, removal_priority=6),
            FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.LOTV), MissionConnection(6, SC2Campaign.LOTV)], "Purifier", completion_critical=True, or_requirements=True),
            FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.LOTV), MissionConnection(6, SC2Campaign.LOTV), MissionConnection(7, SC2Campaign.LOTV)], "Ulnar", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(8, SC2Campaign.LOTV)], "Ulnar", completion_critical=True, removal_priority=1),
            FillMission(MissionPools.HARD, [MissionConnection(9, SC2Campaign.LOTV)], "Ulnar", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(10, SC2Campaign.LOTV)], "Purifier", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(11, SC2Campaign.LOTV)], "Purifier", completion_critical=True, removal_priority=5),
            FillMission(MissionPools.HARD, [MissionConnection(10, SC2Campaign.LOTV)], "Tal'darim", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(13, SC2Campaign.LOTV)], "Tal'darim", completion_critical=True, removal_priority=4),
            FillMission(MissionPools.HARD, [MissionConnection(12, SC2Campaign.LOTV), MissionConnection(14, SC2Campaign.LOTV)], "Moebius", completion_critical=True, or_requirements=True),
            FillMission(MissionPools.HARD, [MissionConnection(12, SC2Campaign.LOTV), MissionConnection(14, SC2Campaign.LOTV), MissionConnection(15, SC2Campaign.LOTV)], "Return to Aiur", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(16, SC2Campaign.LOTV)], "Return to Aiur", completion_critical=True, removal_priority=2),
            FillMission(MissionPools.FINAL, [MissionConnection(17, SC2Campaign.LOTV)], "Return to Aiur", completion_critical=True),
        ],
        SC2Campaign.EPILOGUE: [
            FillMission(MissionPools.VERY_HARD, [MissionConnection(24, SC2Campaign.WOL), MissionConnection(19, SC2Campaign.HOTS), MissionConnection(18, SC2Campaign.LOTV)], "_1", completion_critical=True),
            FillMission(MissionPools.VERY_HARD, [MissionConnection(0, SC2Campaign.EPILOGUE)], "_2", completion_critical=True, removal_priority=1),
            FillMission(MissionPools.FINAL, [MissionConnection(1, SC2Campaign.EPILOGUE)], "_3", completion_critical=True),
        ],
        SC2Campaign.NCO: [
            FillMission(MissionPools.EASY, [MissionConnection(-1, SC2Campaign.NCO)], "_1", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.NCO)], "_1", completion_critical=True, removal_priority=6),
            FillMission(MissionPools.MEDIUM, [MissionConnection(1, SC2Campaign.NCO)], "_1", completion_critical=True, removal_priority=5),
            FillMission(MissionPools.HARD, [MissionConnection(2, SC2Campaign.NCO)], "_2", completion_critical=True, removal_priority=7),
            FillMission(MissionPools.HARD, [MissionConnection(3, SC2Campaign.NCO)], "_2", completion_critical=True, removal_priority=4),
            FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.NCO)], "_2", completion_critical=True, removal_priority=3),
            FillMission(MissionPools.HARD, [MissionConnection(5, SC2Campaign.NCO)], "_3", completion_critical=True, removal_priority=2),
            FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.NCO)], "_3", completion_critical=True, removal_priority=1),
            FillMission(MissionPools.FINAL, [MissionConnection(7, SC2Campaign.NCO)], "_3", completion_critical=True),
        ]
    }


def mini_campaign_order() -> Dict[SC2Campaign, List[FillMission]]:
    return {
        SC2Campaign.WOL: [
            FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.WOL)], "Mar Sara", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.WOL)], "Colonist"),
            FillMission(MissionPools.MEDIUM, [MissionConnection(1, SC2Campaign.WOL)], "Colonist"),
            FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.WOL)], "Artifact", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.WOL)], "Artifact", number=4, completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.WOL)], "Artifact", number=8, completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.WOL)], "Covert", number=2),
            FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.WOL)], "Covert"),
            FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.WOL)], "Rebellion", number=3),
            FillMission(MissionPools.HARD, [MissionConnection(8, SC2Campaign.WOL)], "Rebellion"),
            FillMission(MissionPools.HARD, [MissionConnection(5, SC2Campaign.WOL)], "Char", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(5, SC2Campaign.WOL)], "Char", completion_critical=True),
            FillMission(MissionPools.FINAL, [MissionConnection(10, SC2Campaign.WOL), MissionConnection(11, SC2Campaign.WOL)], "Char", completion_critical=True, or_requirements=True)
        ],
        SC2Campaign.PROPHECY: [
            FillMission(MissionPools.MEDIUM, [MissionConnection(4, SC2Campaign.WOL)], "_1"),
            FillMission(MissionPools.FINAL, [MissionConnection(0, SC2Campaign.PROPHECY)], "_2"),
        ],
        SC2Campaign.HOTS: [
            FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.HOTS)], "Umoja", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.HOTS)], "Kaldir"),
            FillMission(MissionPools.MEDIUM, [MissionConnection(1, SC2Campaign.HOTS)], "Kaldir"),
            FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.HOTS)], "Char"),
            FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.HOTS)], "Char"),
            FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.HOTS)], "Zerus", number=3),
            FillMission(MissionPools.MEDIUM, [MissionConnection(5, SC2Campaign.HOTS)], "Zerus"),
            FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.HOTS)], "Skygeirr Station", number=5),
            FillMission(MissionPools.HARD, [MissionConnection(7, SC2Campaign.HOTS)], "Skygeirr Station"),
            FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.HOTS)], "Dominion Space", number=5),
            FillMission(MissionPools.HARD, [MissionConnection(9, SC2Campaign.HOTS)], "Dominion Space"),
            FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.HOTS)], "Korhal", completion_critical=True, number=8),
            FillMission(MissionPools.FINAL, [MissionConnection(11, SC2Campaign.HOTS)], "Korhal", completion_critical=True),
        ],
        SC2Campaign.PROLOGUE: [
            FillMission(MissionPools.EASY, [MissionConnection(-1, SC2Campaign.PROLOGUE)], "_1"),
            FillMission(MissionPools.FINAL, [MissionConnection(0, SC2Campaign.PROLOGUE)], "_2")
        ],
        SC2Campaign.LOTV: [
            FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.LOTV)], "Aiur",completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.LOTV)], "Aiur", completion_critical=True),
            FillMission(MissionPools.EASY, [MissionConnection(1, SC2Campaign.LOTV)], "Korhal", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(1, SC2Campaign.LOTV)], "Shakuras", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(2, SC2Campaign.LOTV), MissionConnection(3, SC2Campaign.LOTV)], "Purifier", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.LOTV)], "Purifier", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.LOTV)], "Ulnar", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.LOTV)], "Tal'darim", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(5, SC2Campaign.LOTV), MissionConnection(7, SC2Campaign.LOTV)], "Return to Aiur", completion_critical=True),
            FillMission(MissionPools.FINAL, [MissionConnection(8, SC2Campaign.LOTV)], "Return to Aiur", completion_critical=True),
        ],
        SC2Campaign.EPILOGUE: [
            FillMission(MissionPools.VERY_HARD, [MissionConnection(12, SC2Campaign.WOL), MissionConnection(12, SC2Campaign.HOTS), MissionConnection(9, SC2Campaign.LOTV)], "_1", completion_critical=True),
            FillMission(MissionPools.FINAL, [MissionConnection(0, SC2Campaign.EPILOGUE)], "_2", completion_critical=True),
        ],
        SC2Campaign.NCO: [
            FillMission(MissionPools.EASY, [MissionConnection(-1, SC2Campaign.NCO)], "_1", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.NCO)], "_1", completion_critical=True),
            FillMission(MissionPools.MEDIUM, [MissionConnection(1, SC2Campaign.NCO)], "_2", completion_critical=True),
            FillMission(MissionPools.HARD, [MissionConnection(2, SC2Campaign.NCO)], "_3", completion_critical=True),
            FillMission(MissionPools.FINAL, [MissionConnection(3, SC2Campaign.NCO)], "_3", completion_critical=True),
        ]
    }


smooth_difficulty = [MissionPools.EASY,
                     MissionPools.MEDIUM, MissionPools.MEDIUM,
                     MissionPools.HARD, MissionPools.HARD,
                     MissionPools.VERY_HARD]
max_difficulty = len(smooth_difficulty) - 1


def make_golden_path(world: World, num_missions: int) -> list[FillMission]:
    chain_name_options = ['Mar Sara', 'Char', 'Kaldir', 'Zerus', 'Skygeirr Station',
                   'Dominion Space', 'Korhal', 'Aiur', 'Shakuras', 'Ulnar']
    world.random.shuffle(chain_name_options)

    first_chain = chain_name_options.pop()
    first_mission = FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.GLOBAL)], first_chain,
                                     completion_critical=True)

    class Campaign:
        def __init__(self, first_mission: FillMission, missions_remaining: int):
            self.mission_order = [first_mission]
            self.counter = 0
            self.last_mission_in_chain = [0]
            self.chain_names = [first_mission.category]
            self.missions_remaining = missions_remaining
            self.padding = 0

        def add_mission(self, chain: int, difficulty: int, required_missions: int = 0):
            if self.missions_remaining == 0 and difficulty is not MissionPools.FINAL:
                return
            self.counter += 1
            if self.mission_order[self.last_mission_in_chain[chain]].number == required_missions or required_missions <= 1:
                required_missions = 0
            mission_connections = [MissionConnection(self.last_mission_in_chain[chain], SC2Campaign.GLOBAL)]
            padding = 0
            if self.last_mission_in_chain[chain] == self.last_mission_in_chain[0]:
                # Adding padding to the start of new chains
                if chain != 0:
                    padding = self.padding
            else:
                # Requiring main chain progress for optional chains
                mission_connections.append(MissionConnection(self.last_mission_in_chain[0], SC2Campaign.GLOBAL))
            self.mission_order.append(FillMission(
                difficulty,
                mission_connections,
                self.chain_names[chain],
                number=required_missions,
                completion_critical=chain == 0,
                ui_vertical_padding=padding
            ))
            self.last_mission_in_chain[chain] = self.counter
            if chain == 0:
                self.padding += 1
            self.missions_remaining -= 1

    campaign = Campaign(first_mission, num_missions - 2)
    current_required_missions = 0
    main_chain = 0
    while campaign.missions_remaining > 0:
        mission_difficulty = smooth_difficulty[min(main_chain, max_difficulty)]
        main_chain += 1
        if main_chain % 2 == 1:  # Adding branches
            chains_to_make = 0 if len(campaign.chain_names) > 5 else 2 if main_chain == 1 else 1
            for new_chain in range(chains_to_make):
                campaign.chain_names.append(chain_name_options.pop())
                campaign.last_mission_in_chain.append(campaign.last_mission_in_chain[0])
        # Updating branches
        for side_chain in range(len(campaign.chain_names) - 1, 0, -1):
            campaign.add_mission(side_chain, mission_difficulty)
        # Adding main path mission
        current_required_missions = (len(campaign.mission_order) * 3) // 4
        campaign.add_mission(0, mission_difficulty, current_required_missions)
    campaign.add_mission(0, MissionPools.FINAL, current_required_missions)
    return {SC2Campaign.GLOBAL: campaign.mission_order}


def make_gauntlet(num_missions: int) -> list[FillMission]:
    mission_order: list[FillMission] = []
    row_length = 7
    rows = math.ceil(num_missions / row_length)
    difficulty_rate = (max_difficulty + 1) / num_missions if num_missions < 21 else 1/3
    if rows == 1:
        column_names = ["I", "II", "III", "IV", "V", "VI", "VII"][:num_missions - 1]
        column_names.append("Final")
    else:
        column_names = [f'_{col + 1}' for col in range(row_length)]
    first_mission = FillMission(MissionPools.STARTER, [MissionConnection(-1)], column_names[0],
                                completion_critical=True)
    mission_order.append(first_mission)
    mission_number = 1
    space_rows = 0
    while mission_number < num_missions:
        if mission_number == num_missions - 1:
            difficulty = MissionPools.FINAL
        else:
            difficulty_progress = mission_number * difficulty_rate
            difficulty = smooth_difficulty[min(math.floor(difficulty_progress), max_difficulty)]
        connection = MissionConnection(mission_number - 1)
        mission_order.append(FillMission(
            difficulty,
            [connection],
            column_names[mission_number % row_length],
            completion_critical=True,
            ui_vertical_padding=space_rows
        ))
        mission_number += 1
        # Next row
        if mission_number == row_length:
            space_rows += 1
    return {SC2Campaign.GLOBAL: mission_order}


def make_blitz(num_missions: int) -> list[FillMission]:
    min_width, max_width = 2, 5
    mission_divisor = 5
    dynamic_width = num_missions / mission_divisor
    width = math.floor(max(min(dynamic_width, max_width), min_width))
    middle_column = math.floor(width / 2)
    connections = [MissionConnection(-1)]
    mission_number = 0
    mission_order: List[FillMission] = []
    if num_missions % width > middle_column:
        final_row = math.floor(num_missions / width) * width
        final_mission_number = final_row + middle_column
    else:
        final_mission_number = num_missions - 1
    while mission_number < num_missions:
        column = mission_number % width
        row = math.floor(mission_number / width)
        if mission_number == middle_column:
            difficulty = MissionPools.STARTER
        elif mission_number == final_mission_number:
            difficulty = MissionPools.FINAL
        else:
            difficulty = smooth_difficulty[(min(row, max_difficulty))]
        mission_order.append(FillMission(
            difficulty,
            connections,
            f'_{column}',
            or_requirements=True
        ))
        mission_number += 1
        # Next row, requires previous row
        if mission_number % width == 0:
            connections = [MissionConnection(mission_number - 1 - i) for i in range(width)]
            connections.reverse()
    return {SC2Campaign.GLOBAL: mission_order}


def make_diagonal(two_start_positions: bool, num_missions: int):
    mission_order: List[FillMission] = []
    menu_connection = [MissionConnection(-1)]
    max_width = 7
    difficulty_progress = 0
    difficulty_rate = max(0.5, min(1, 3 * max_difficulty / num_missions))
    x = 0
    y = 0
    difficulty = MissionPools.EASY
    first_diagonal = True
    creation_cycle = 0  # Root -> Bottom Branch -> Right Branch
    # Creating the starter missions
    if two_start_positions:
        mission_order += [
            FillMission(MissionPools.STARTER, menu_connection, '_1', ui_vertical_padding=1),
            FillMission(MissionPools.EASY, menu_connection, '_2')
        ]
        mission_number = 2
    else:
        mission_order.append(FillMission(MissionPools.STARTER, menu_connection, '_1', completion_critical=True))
        creation_cycle = 1
        mission_number = 1
    while mission_number < num_missions:
        if mission_number == num_missions - 1:
            difficulty = MissionPools.FINAL
        elif creation_cycle == 0 and difficulty_progress < max_difficulty:
            difficulty_progress += difficulty_rate
            difficulty = smooth_difficulty[math.floor(difficulty_progress)]
        if creation_cycle == 0:
            # Root
            if y != -1:
                x += 1
            y += 1
            mission_order.append(FillMission(
                difficulty,
                [MissionConnection(mission_number - 1), MissionConnection(mission_number - 2)],
                f'_{x + 1}',
                or_requirements=True,
                completion_critical=True
            ))
        elif creation_cycle == 1:
            # Bottom branch
            mission_order.append(FillMission(
                difficulty,
                [MissionConnection(mission_number - 1)],
                f'_{x + 1}'
            ))
        else:
            # Right branch
            column = f'_{x + 2}'
            if x >= max_width - 1:
                # Wrapping around
                x = 0
                y = -1
                column = '_1'
                first_diagonal = False
            mission_order.append(FillMission(
                difficulty,
                [MissionConnection(mission_number - 2)],
                column,
                ui_vertical_padding=y if first_diagonal else 1
            ))
        mission_number += 1
        creation_cycle += 1
        if creation_cycle == 3:
            creation_cycle = 0
    return {SC2Campaign.GLOBAL: mission_order}
