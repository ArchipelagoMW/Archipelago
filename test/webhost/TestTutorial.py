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
                    try:
                        self.assertIn(game_name, games_with_tutorial)
                    except AssertionError:
                        # look for partial name in the tutorial name
                        for game in games_with_tutorial:
                            if game_name in game:
                                break
                        else:
                            self.fail(f"{game_name} has no setup tutorial. "
                                      f"Games with Tutorial: {games_with_tutorial}")
