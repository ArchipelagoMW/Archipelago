from BaseClasses import LocationProgressType
from test.bases import WorldTestBase



class TestGeneration(WorldTestBase):
    game = "The Legend of Zelda - Phantom Hourglass"
    options = {
        "keysanity": "in_own_dungeon",
        "phantom_combat_difficulty": "require_traps",
        "logic": "hard",
        "accessibility": "items",
        "randomize_frogs": "start_with",
        "dungeons_required": 5,
        "goal": "metal_hunt",
        "ghost_ship_in_dungeon_pool": "rescue_tetra",
        "totok_in_dungeon_pool": False,
        "randomize_harrow": "randomize_with_hints",
        "exclude_non_required_dungeons": True,
        "randomize_masked_beedle": True,
        "randomize minigames": "randomize_with_hints",
        "randomize_salvage": "randomize_with_hints",
        "additional_metal_names": "vanilla_only",
        "zauz_required_metals": 16,
        "metal_hunt_required": 2,
        "metal_hunt_total": 7,
        "ph_time_logic": "no_logic",
        "ph_starting_time": 50,
        "ph_time_increment": 10,
        "randomize_beedle_membership": "randomize",
               }
