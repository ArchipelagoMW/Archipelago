from worlds.witness.options import ElevatorsComeToYou

TEST_PRESETS = {
    "Test preset 1": {
        "disable_non_randomized": True,
        "puzzle_randomization": "sigma_expert",
        "shuffle_EPs": "individual",
        "ep_difficulty": "eclipse",
        "victory_condition": "challenge",
        "shuffle_discarded_panels": False,
        "shuffle_boat": False,
        "shuffle_dog": "off",
    },
    "Test preset 2": {
        "puzzle_randomization": "none",
        "elevators_come_to_you": ElevatorsComeToYou.valid_keys - ElevatorsComeToYou.default,  # Opposite of default
        "shuffle_doors": "panels",
        "victory_condition": "mountain_box_short",
        "early_caves": True,
        "shuffle_vault_boxes": True,
        "mountain_lasers": 11,
        "shuffle_dog": "puzzle_skip",
    },
    "Test preset 3": {
        "death_link": True,
        "death_link_amnesty": 3,
        "laser_hints": True,
        "hint_amount": 40,
        "area_hint_percentage": 100,
        "vague_hints": "experimental",
    },
    "Test preset 4": {
        "shuffle_symbols": False,
        "shuffle_doors": "mixed",
        "shuffle_EPs": "individual",
        "obelisk_keys": True,
        "shuffle_lasers": "anywhere",
        "victory_condition": "mountain_box_long",
        "shuffle_dog": "random_item",
    },
    "Test preset 5": {
        "puzzle_randomization": "umbra_variety",
        "shuffle_postgame": True,
        "shuffle_discarded_panels": True,
        "shuffle_doors": "doors",
        "door_groupings": "regional",
        "victory_condition": "elevator",
        "easter_egg_hunt": "extreme",
    },
    "Test preset 6": {
        "victory_condition": "mountain_box_long",
        "shuffle_postgame": True
    }
}
