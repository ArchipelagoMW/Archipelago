from typing import List, Dict


region_exit_table: Dict[int, List[str]] = {
    0: ["New Game"],

    1: ["To Waynehouse",
        "To New Muldul",
        "To Viewax",
        "To TV Island",
        "To Shield Facility",
        "To Worm Pod",
        "To Foglast",
        "To Sage Labyrinth",
        "To Hylemxylem"],

    2: ["To World",
        "To Afterlife",],

    3: ["To Airship",
        "To Waynehouse",
        "To New Muldul",
        "To Drill Castle",
        "To Viewax",
        "To Arcade Island",
        "To TV Island",
        "To Juice Ranch",
        "To Shield Facility",
        "To Worm Pod",
        "To Foglast",
        "To Sage Airship",
        "To Hylemxylem"],

    4: ["To World",
        "To Afterlife",
        "To New Muldul Vault"],
    
    5: ["To New Muldul"],
    
    6: ["To World",
        "To Afterlife"],
    
    7: ["To World"],
    
    8: ["To World"],
    
    9: ["To World",
        "To Afterlife"],
    
    10: ["To World"],
    
    11: ["To World",
            "To Afterlife",
            "To Worm Pod"],
    
    12: ["To Shield Facility",
            "To Afterlife"],
    
    13: ["To World",
            "To Afterlife"],
    
    14: ["To World",
            "To Sage Labyrinth"],
    
    15: ["To Drill Castle",
            "To Afterlife"],
    
    16: ["To World"],
    
    17: ["To World",
        "To Afterlife"]
}


exit_lookup_table: Dict[str, int] = {
    "New Game": 2,
    "To Waynehouse": 2,
    "To Afterlife": 1,
    "To World": 3,
    "To New Muldul": 4,
    "To New Muldul Vault": 5,
    "To Viewax": 6,
    "To Airship": 7,
    "To Arcade Island": 8,
    "To TV Island": 9,
    "To Juice Ranch": 10,
    "To Shield Facility": 11,
    "To Worm Pod": 12,
    "To Foglast": 13,
    "To Drill Castle": 14,
    "To Sage Labyrinth": 15,
    "To Sage Airship": 16,
    "To Hylemxylem": 17
}