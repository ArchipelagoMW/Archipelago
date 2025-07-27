from BaseClasses import LocationProgressType
from test.bases import *



class TestGeneration(WorldTestBase):
    game = "The Legend of Zelda - Phantom Hourglass"
    options = {
        "keysanity": "in_own_dungeon",
        "phantom_combat_difficulty": "require_traps",
        "logic": "hard",
        "accessibility": "items",
        "randomize_frogs": "start_with",
        "dungeons_required": 0,
        "goal": "metal_hunt",
        "ghost_ship_in_dungeon_pool": "rescue_tetra",
        "totok_in_dungeon_pool": False,
        "randomize_harrow": "no_harrow",
        "exclude_non_required_dungeons": True,
        "randomize_masked_beedle": False,
        "randomize minigames": "no_minigames",
        "randomize_salvage": "no_salvage",
        "additional_metal_names": "additional_rare_metal",
        "zauz_required_metals": 16,
        "metal_hunt_required": 30,
        "metal_hunt_total": 30,
        "ph_time_logic": "easy",
        "ph_starting_time": 0,
        "ph_time_increment": 6,
        "randomize_beedle_membership": "no_beedle_points",
               }

