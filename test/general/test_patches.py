import unittest
from worlds.AutoWorld import AutoWorldRegister
from worlds.Files import AutoPatchRegister


class TestPatches(unittest.TestCase):
    def test_patch_name_matches_game(self) -> None:
        for game_name in AutoPatchRegister.patch_types:
            with self.subTest(game=game_name):
                self.assertIn(game_name, AutoWorldRegister.world_types.keys(),
                              f"Patch '{game_name}' does not match the name of any world.")
