from typing import Dict, Any

all_random = {
    "progression_balancing": "random",
    "accessibility": "random",
    "death_link": "random",
    "game_language": "random",
    "goal": "random",
    "goal_speed": "random",
    "total_heart_stars": "random",
    "heart_stars_required": "random",
    "filler_percentage": "random",
    "trap_percentage": "random",
    "gooey_trap_weight": "random",
    "slow_trap_weight": "random",
    "ability_trap_weight": "random",
    "jumping_target": "random",
    "stage_shuffle": "random",
    "boss_shuffle": "random",
    "allow_bb": "random",
    "animal_randomization": "random",
    "copy_ability_randomization": "random",
    "strict_bosses": "random",
    "open_world": "random",
    "ow_boss_requirement": "random",
    "boss_requirement_random": "random",
    "consumables": "random",
    "starsanity": "random",
    "kirby_flavor_preset": "random",
    "gooey_flavor_preset": "random",
    "music_shuffle": "random",
}

beginner = {
    "goal": "zero",
    "goal_speed": "normal",
    "total_heart_stars": 50,
    "heart_stars_required": 30,
    "filler_percentage": 25,
    "trap_percentage": 0,
    "gooey_trap_weight": "random",
    "slow_trap_weight": "random",
    "ability_trap_weight": "random",
    "jumping_target": 5,
    "stage_shuffle": "pattern",
    "boss_shuffle": "shuffled",
    "allow_bb": "random",
    "strict_bosses": True,
    "open_world": True,
    "ow_boss_requirement": 3,
}


kdl3_options_presets: Dict[str, Dict[str, Any]] = {
    "All Random": all_random,
    "Beginner": beginner,
}
