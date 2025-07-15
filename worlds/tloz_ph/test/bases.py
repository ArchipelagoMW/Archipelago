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
        "dungeons_required": 0,
        "goal": "triforce_door",
        "ghost_ship_in_dungeon_pool": "rescue_tetra",
        "totok_in_dungeon_pool": False,
        "randomize_harrow": False,
        "exclude_non_required_dungeons": True,
        "randomize_masked_beedle": True,
               }
