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
    category: str
    number: int = 0  # number of worlds need beaten
    completion_critical: bool = False  # missions needed to beat game
    or_requirements: bool = False  # true if the requirements should be or-ed instead of and-ed


class FillMission(NamedTuple):
    type: str
    connect_to: List[int]  # -1 connects to Menu
    category: str
    number: int = 0  # number of worlds need beaten
    completion_critical: bool = False  # missions needed to beat game
    or_requirements: bool = False  # true if the requirements should be or-ed instead of and-ed
    relegate: bool = False  # true if this is a slot no build missions should be relegated to.


vanilla_shuffle_order = [
    FillMission("no_build", [-1], "Mar Sara", completion_critical=True),
    FillMission("easy", [0], "Mar Sara", completion_critical=True),
    FillMission("easy", [1], "Mar Sara", completion_critical=True),
    FillMission("easy", [2], "Colonist"),
    FillMission("medium", [3], "Colonist"),
    FillMission("hard", [4], "Colonist", number=7),
    FillMission("hard", [4], "Colonist", number=7, relegate=True),
    FillMission("easy", [2], "Artifact", completion_critical=True),
    FillMission("medium", [7], "Artifact", number=8, completion_critical=True),
    FillMission("hard", [8], "Artifact", number=11, completion_critical=True),
    FillMission("hard", [9], "Artifact", number=14, completion_critical=True),
    FillMission("hard", [10], "Artifact", completion_critical=True),
    FillMission("medium", [2], "Covert", number=4),
    FillMission("medium", [12], "Covert"),
    FillMission("hard", [13], "Covert", number=8, relegate=True),
    FillMission("hard", [13], "Covert", number=8, relegate=True),
    FillMission("medium", [2], "Rebellion", number=6),
    FillMission("hard", [16], "Rebellion"),
    FillMission("hard", [17], "Rebellion"),
    FillMission("hard", [18], "Rebellion"),
    FillMission("hard", [19], "Rebellion", relegate=True),
    FillMission("medium", [8], "Prophecy"),
    FillMission("hard", [21], "Prophecy"),
    FillMission("hard", [22], "Prophecy"),
    FillMission("hard", [23], "Prophecy", relegate=True),
    FillMission("hard", [11], "Char", completion_critical=True),
    FillMission("hard", [25], "Char", completion_critical=True),
    FillMission("hard", [25], "Char", completion_critical=True),
    FillMission("all_in", [26, 27], "Char", completion_critical=True, or_requirements=True)
]


vanilla_mission_req_table = {
    "Liberation Day": MissionInfo(1, 7, [], "Mar Sara", completion_critical=True),
    "The Outlaws": MissionInfo(2, 2, [1], "Mar Sara", completion_critical=True),
    "Zero Hour": MissionInfo(3, 4, [2], "Mar Sara", completion_critical=True),
    "Evacuation": MissionInfo(4, 4, [3], "Colonist"),
    "Outbreak": MissionInfo(5, 3, [4], "Colonist"),
    "Safe Haven": MissionInfo(6, 1, [5], "Colonist", number=7),
    "Haven's Fall": MissionInfo(7, 1, [5], "Colonist", number=7),
    "Smash and Grab": MissionInfo(8, 5, [3], "Artifact", completion_critical=True),
    "The Dig": MissionInfo(9, 4, [8], "Artifact", number=8, completion_critical=True),
    "The Moebius Factor": MissionInfo(10, 9, [9], "Artifact", number=11, completion_critical=True),
    "Supernova": MissionInfo(11, 5, [10], "Artifact", number=14, completion_critical=True),
    "Maw of the Void": MissionInfo(12, 6, [11], "Artifact", completion_critical=True),
    "Devil's Playground": MissionInfo(13, 3, [3], "Covert", number=4),
    "Welcome to the Jungle": MissionInfo(14, 4, [13], "Covert"),
    "Breakout": MissionInfo(15, 3, [14], "Covert", number=8),
    "Ghost of a Chance": MissionInfo(16, 6, [14], "Covert", number=8),
    "The Great Train Robbery": MissionInfo(17, 4, [3], "Rebellion", number=6),
    "Cutthroat": MissionInfo(18, 5, [17], "Rebellion"),
    "Engine of Destruction": MissionInfo(19, 6, [18], "Rebellion"),
    "Media Blitz": MissionInfo(20, 5, [19], "Rebellion"),
    "Piercing the Shroud": MissionInfo(21, 6, [20], "Rebellion"),
    "Whispers of Doom": MissionInfo(22, 4, [9], "Prophecy"),
    "A Sinister Turn": MissionInfo(23, 4, [22], "Prophecy"),
    "Echoes of the Future": MissionInfo(24, 3, [23], "Prophecy"),
    "In Utter Darkness": MissionInfo(25, 3, [24], "Prophecy"),
    "Gates of Hell": MissionInfo(26, 2, [12], "Char", completion_critical=True),
    "Belly of the Beast": MissionInfo(27, 4, [26], "Char", completion_critical=True),
    "Shatter the Sky": MissionInfo(28, 5, [26], "Char", completion_critical=True),
    "All-In": MissionInfo(29, -1, [27, 28], "Char", completion_critical=True, or_requirements=True)
}

lookup_id_to_mission: Dict[int, str] = {
    data.id: mission_name for mission_name, data in vanilla_mission_req_table.items() if data.id}
