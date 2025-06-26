from BaseClasses import LocationProgressType
from test.bases import WorldTestBase


class TestGeneration(WorldTestBase):
    game = "The Legend of Zelda - Phantom Hourglass"
    options = {
        "keysanity": "in_own_dungeon",
        "phantom_combat_difficulty": "require_weapon",
        "logic": "normal",
        "accessibility": "full",
        "randomize_frogs": "randomize",
        "dungeons_required": 6,
        "goal": "beat_bellumbeck",
        "ghost_ship_in_dungeon_pool": "cubus_sisters",
        "totok_in_dungeon_pool": True,
        "randomize_harrow": False,
               }
