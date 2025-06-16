from BaseClasses import LocationProgressType
from test.bases import WorldTestBase


class TestGeneration(WorldTestBase):
    game = "The Legend of Zelda - Phantom Hourglass"
    options = {
        "keysanity": "vanilla",
        "phantom_combat_difficulty": "require_weapon",
        "logic": "normal",
        "accessibility": "full",
        "randomize_frogs": "start_with"
               }
