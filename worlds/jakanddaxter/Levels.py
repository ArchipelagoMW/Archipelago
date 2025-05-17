# This contains the list of levels in Jak and Daxter.
# Not to be confused with Regions - there can be multiple Regions in every Level.
level_table = {
    "Geyser Rock": {
        "level_index": 0,
        "orbs": 50
    },
    "Sandover Village": {
        "level_index": 1,
        "orbs": 50
    },
    "Sentinel Beach": {
        "level_index": 2,
        "orbs": 150
    },
    "Forbidden Jungle": {
        "level_index": 3,
        "orbs": 150
    },
    "Misty Island": {
        "level_index": 4,
        "orbs": 150
    },
    "Fire Canyon": {
        "level_index": 5,
        "orbs": 50
    },
    "Rock Village": {
        "level_index": 6,
        "orbs": 50
    },
    "Lost Precursor City": {
        "level_index": 7,
        "orbs": 200
    },
    "Boggy Swamp": {
        "level_index": 8,
        "orbs": 200
    },
    "Precursor Basin": {
        "level_index": 9,
        "orbs": 200
    },
    "Mountain Pass": {
        "level_index": 10,
        "orbs": 50
    },
    "Volcanic Crater": {
        "level_index": 11,
        "orbs": 50
    },
    "Snowy Mountain": {
        "level_index": 12,
        "orbs": 200
    },
    "Spider Cave": {
        "level_index": 13,
        "orbs": 200
    },
    "Lava Tube": {
        "level_index": 14,
        "orbs": 50
    },
    "Gol and Maia's Citadel": {
        "level_index": 15,
        "orbs": 200
    }
}

level_table_with_global = {
    **level_table,
    "": {
        "level_index": 16,  # Global
        "orbs": 2000
    }
}
