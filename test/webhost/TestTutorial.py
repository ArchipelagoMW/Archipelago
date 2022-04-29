import unittest
from worlds.AutoWorld import AutoWorldRegister


class TestBase(unittest.TestCase):
    def testCreateItem(self):
        import WebHost
        tutorials_data = WebHost.create_ordered_tutorials_file()
        games_with_tutorial = set(entry["gameTitle"] for entry in tutorials_data)
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    self.assertIn(game_name, games_with_tutorial)
