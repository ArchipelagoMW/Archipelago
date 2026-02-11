from typing import Dict, Any

all_bosses = {
    "goal": "bowser",
    "yoshi_egg_count": 0,
    "percentage_of_yoshi_eggs": 100,
    "yoshi_egg_placement": {"Castles"},
}

worldwide = {
    "goal": "bowser",
    "yoshi_egg_count": 0,
    "percentage_of_yoshi_eggs": 100,
    "yoshi_egg_placement": {"Every Level"},
}

easter_season = {
    "goal": "yoshi_house",
    "yoshi_egg_count": 255,
    "percentage_of_yoshi_eggs": 100,
    "yoshi_egg_placement": {"Every Level"},
    "dragon_coin_checks": True,
    "moon_checks": True,
    "hidden_1up_checks": True,
    "star_block_checks": True,
    "midway_point_checks": True,
    "room_checks": True,
    "block_checks": {
        "Coin Blocks",
        "Item Blocks",
        "Yellow Switch Palace Blocks",
        "Green Switch Palace Blocks",
        "Invisible Blocks",
        "P-Switch Blocks",
        "Flying Blocks",
    }
}

beginner = {
    "goal": "bowser",
    "yoshi_egg_count": 5,
    "percentage_of_yoshi_eggs": 75,
    "yoshi_egg_placement": {"Castles"},
    "midway_point_checks": True,
    "block_checks": {},
    "game_logic_difficulty": "easy",
    "level_shuffle": True,
    "bowser_castle_doors": "fast",
    "early_climb": True,
    "ability_shuffle": {
        "Run",
        "Carry",
        "Swim",
        "Spin Jump",
        "Climb",
        "P-Balloon",
        "Yoshi",
        "Powerups",
        "Super Star",
        "P-Switch",
        "Yellow Switch Palace",
        "Green Switch Palace",
        "Red Switch Palace",
        "Blue Switch Palace",
        "Special World",
    },
    "start_inventory": {
        "Progressive Timer": 1,
        "Inventory Heart": 20,
    },
}

dev_choice = {
    "goal": "bowser",
    "yoshi_egg_count": 10,
    "percentage_of_yoshi_eggs": 85,
    "dragon_coin_checks": True,
    "moon_checks": True,
    "hidden_1up_checks": True,
    "star_block_checks": True,
    "midway_point_checks": True,
    "room_checks": True,
    "block_checks": {
        "Coin Blocks",
        "Item Blocks",
        "Yellow Switch Palace Blocks",
        "Green Switch Palace Blocks",
        "Invisible Blocks",
        #"P-Switch Blocks",
        "Flying Blocks",
    },
    "game_logic_difficulty": "medium",
    "level_shuffle": True,
    "level_effects": 30,
    "swap_level_exits": True,
    "swap_exit_count": 12,
    "map_teleport_shuffle": "on_both_mix",
    "map_transition_shuffle": True,
    "enemy_shuffle": True,
    "boss_shuffle": "full",
    "bowser_castle_doors": "fast",
    "junk_fill_percentage": 0,
    "trap_fill_percentage": 10,
}

waffle_options_presets: Dict[str, Dict[str, Any]] = {
    "Beginner": beginner,
    "All Bosses": all_bosses,
    "Easter Season": easter_season,
    "Mr. Worldwide": worldwide,
    "Developer's Choice": dev_choice,
}
