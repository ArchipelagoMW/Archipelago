from BaseClasses import LocationProgressType
from test.bases import WorldTestBase


class TestGeneration(WorldTestBase):
    game = "The Legend of Zelda - Phantom Hourglass"
    options = {
        "keysanity": "in_own_dungeon",
        "phantom_combat_difficulty": "require_weapon",
        "logic": "medium",
        "accessibility": "full",
        "randomize_frogs": "start_with",
        "dungeons_required": 8,
        "goal": "beat_bellumbeck",
        "ghost_ship_in_dungeon_pool": "false",
        "totok_in_dungeon_pool": False,
        "randomize_harrow": False,
        "exclude_non_required_dungeons": True,
               }
