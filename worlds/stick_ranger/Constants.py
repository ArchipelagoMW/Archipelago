from typing import Dict, List, Tuple

STAGE_SETTINGS: List[Tuple[str, str, str, str]] = [
    (
        "castle",
        "min_stages_req_for_castle",
        "max_stages_req_for_castle",
        "stages_req_for_castle"
    ),
    (
        "submarine_shrine",
        "min_stages_req_for_submarine_shrine",
        "max_stages_req_for_submarine_shrine",
        "stages_req_for_submarine_shrine"
    ),
    (
        "pyramid",
        "min_stages_req_for_pyramid",
        "max_stages_req_for_pyramid",
        "stages_req_for_pyramid"
    ),
    (
        "ice_castle",
        "min_stages_req_for_ice_castle",
        "max_stages_req_for_ice_castle",
        "stages_req_for_ice_castle"
    ),
    (
        "hell_castle",
        "min_stages_req_for_hell_castle",
        "max_stages_req_for_hell_castle",
        "stages_req_for_hell_castle"
    )
]

ENEMIES_OPTION_NON_BOSS: int = 1
ENEMIES_OPTION_BOSS: int = 2
ENEMIES_OPTION_ALL: int = 3

TRAP_STEP_PERCENT: int = 25

STARTER_UNLOCK_CHOICES: List[str] = [
    "Unlock Grassland 1",
    "Unlock Grassland 2",
    "Unlock Grassland 3",
    "Unlock Grassland 4",
    "Unlock Hill Country 1"
]

OPENING_STREET_EXIT: str = "Opening Street: Exit"
OPENING_STREET_BOOK: str = "Opening Street: Book"
OPENING_STREET_ENEMIES: List[str] = [
    "Opening Street: Green Smiley Walker",
    "Opening Street: Cyan Smiley Walker",
    "Opening Street: Red Smiley Walker",
    "Opening Street: Blue X Walker"
]
OPENING_STREET_BOSS: str = "Opening Street: Grey Boss Smiley Walker"

RANGER_CLASSES: List[str] = [
    "Boxer",
    "Gladiator",
    "Sniper",
    "Magician",
    "Priest",
    "Gunner",
    "Whipper",
    "Angel"
]

GOAL_LOCATIONS: Dict[str, List[str]] = {
    "Volcano": [
        "Volcano: Exit",
        "Volcano: Book",
        "Volcano: Yellow Boss Box Eel"
    ],
    "Mountaintop": [
        "Mountaintop: Exit",
        "Mountaintop: Book",
        "Mountaintop: Red Boss Smiley Eel",
        "Mountaintop: Blue Boss Fairy Eel",
        "Mountaintop: Olive Boss Star Eel",
        "Mountaintop: Green Boss Cap Eel"
    ],
    "Hell Castle": [
        "Hell Castle: Exit",
        "Hell Castle: Book",
        "Hell Castle: Hell Castle Boss"
    ]
}

GOAL_OPTIONS_MAP: Dict[int, List[str]] = {
    0: ["Hell Castle"],
    1: ["Volcano"],
    2: ["Mountaintop"],
    3: ["Hell Castle", "Volcano"],
    4: ["Hell Castle", "Mountaintop"],
    5: ["Volcano", "Mountaintop"],
    6: ["Hell Castle", "Volcano", "Mountaintop"]
}

GOAL_EXIT_LOCATIONS: Dict[int, List[str]] = {
    0: ["Hell Castle: Exit"],
    1: ["Volcano: Exit"],
    2: ["Mountaintop: Exit"],
    3: ["Hell Castle: Exit", "Volcano: Exit"],
    4: ["Hell Castle: Exit", "Mountaintop: Exit"],
    5: ["Volcano: Exit", "Mountaintop: Exit"],
    6: ["Hell Castle: Exit", "Volcano: Exit", "Mountaintop: Exit"]
}
