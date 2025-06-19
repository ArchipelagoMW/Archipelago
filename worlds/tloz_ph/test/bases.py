from BaseClasses import LocationProgressType
from test.bases import WorldTestBase


class TestGeneration(WorldTestBase):
    game = "The Legend of Zelda - Phantom Hourglass"
    options = {
        "keysanity": "anywhere",
        "phantom_combat_difficulty": "require_weapon",
        "logic": "normal",
        "accessibility": "full",
        "randomize_frogs": "start_with",
        "dungeons_required": 1,
        "goal": "beat_bellumbeck"
               }
