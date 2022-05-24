from typing import NamedTuple, Dict, List

no_build_regions_list = ["Liberation Day", "Breakout", "Ghost of a Chance", "Piercing the Shroud", "Whispers of Doom",
                         "Belly of the Beast"]
easy_regions_list = ["The Outlaws", "Zero Hour", "Evacuation", "Outbreak", "Smash and Grab", "Devil's Playground"]
medium_regions_list = ["Safe Haven", "Haven's Fall", "The Dig", "The Moebius Factor", "Supernova",
                       "Welcome to the Jungle", "The Great Train Robbery", "Cutthroat", "Media Blitz",
                       "A Sinister Turn", "Echoes of the Future"]
hard_regions_list = ["Maw of the Void", "Engine of Destruction", "In Utter Darkness", "Gates of Hell",
                     "Shatter the Sky"]


class MissionInfo(NamedTuple):
    id: int
    extra_locations: int
    required_world: List[int]
    number: int = 0  # number of worlds need beaten
    completion_critical: bool = False  # missions needed to beat game
    or_requirements: bool = False  # true if the requirements should be or-ed instead of and-ed


class FillMission(NamedTuple):
    type: str
    connect_to: List[int]  # -1 connects to Menu
    number: int = 0 # number of worlds need beaten
    completion_critical: bool = False  # missions needed to beat game
    or_requirements: bool = False  # true if the requirements should be or-ed instead of and-ed


vanilla_shuffle_order = [
    FillMission("no_build", [-1], completion_critical=True),
    FillMission("easy", [0], completion_critical=True),
    FillMission("easy", [1], completion_critical=True),
    FillMission("easy", [2]),
    FillMission("medium", [3]),
    FillMission("hard", [4], number=7),
    FillMission("hard", [4], number=7),
    FillMission("easy", [2], completion_critical=True),
    FillMission("medium", [7], number=8, completion_critical=True),
    FillMission("hard", [8], number=11, completion_critical=True),
    FillMission("hard", [9], number=14, completion_critical=True),
    FillMission("hard", [10], completion_critical=True),
    FillMission("medium", [2], number=4),
    FillMission("medium", [12]),
    FillMission("hard", [13], number=8),
    FillMission("hard", [13], number=8),
    FillMission("medium", [2], number=6),
    FillMission("hard", [16]),
    FillMission("hard", [17]),
    FillMission("hard", [18]),
    FillMission("hard", [19]),
    FillMission("medium", [8]),
    FillMission("hard", [21]),
    FillMission("hard", [22]),
    FillMission("hard", [23]),
    FillMission("hard", [11], completion_critical=True),
    FillMission("hard", [25], completion_critical=True),
    FillMission("hard", [25], completion_critical=True),
    FillMission("all_in", [26, 27], completion_critical=True, or_requirements=True)
]


vanilla_mission_req_table = {
    "Liberation Day": MissionInfo(1, 7, [], completion_critical=True),
    "The Outlaws": MissionInfo(2, 2, [1], completion_critical=True),
    "Zero Hour": MissionInfo(3, 4, [2], completion_critical=True),
    "Evacuation": MissionInfo(4, 4, [3]),
    "Outbreak": MissionInfo(5, 3, [4]),
    "Safe Haven": MissionInfo(6, 1, [5], number=7),
    "Haven's Fall": MissionInfo(7, 1, [5], number=7),
    "Smash and Grab": MissionInfo(8, 5, [3], completion_critical=True),
    "The Dig": MissionInfo(9, 4, [8], number=8, completion_critical=True),
    "The Moebius Factor": MissionInfo(10, 9, [9], number=11, completion_critical=True),
    "Supernova": MissionInfo(11, 5, [10], number=14, completion_critical=True),
    "Maw of the Void": MissionInfo(12, 6, [11], completion_critical=True),
    "Devil's Playground": MissionInfo(13, 3, [3], number=4),
    "Welcome to the Jungle": MissionInfo(14, 4, [13]),
    "Breakout": MissionInfo(15, 3, [14], number=8),
    "Ghost of a Chance": MissionInfo(16, 6, [14], number=8),
    "The Great Train Robbery": MissionInfo(17, 4, [3], number=6),
    "Cutthroat": MissionInfo(18, 5, [17]),
    "Engine of Destruction": MissionInfo(19, 6, [18]),
    "Media Blitz": MissionInfo(20, 5, [19]),
    "Piercing the Shroud": MissionInfo(21, 6, [20]),
    "Whispers of Doom": MissionInfo(22, 4, [9]),
    "A Sinister Turn": MissionInfo(23, 4, [22]),
    "Echoes of the Future": MissionInfo(24, 3, [23]),
    "In Utter Darkness": MissionInfo(25, 3, [24]),
    "Gates of Hell": MissionInfo(26, 2, [12], completion_critical=True),
    "Belly of the Beast": MissionInfo(27, 4, [26], completion_critical=True),
    "Shatter the Sky": MissionInfo(28, 5, [26], completion_critical=True),
    "All-In": MissionInfo(29, -1, [27, 28], completion_critical=True, or_requirements=True)
}

lookup_id_to_mission: Dict[int, str] = {
    data.id: mission_name for mission_name, data in vanilla_mission_req_table.items() if data.id}
