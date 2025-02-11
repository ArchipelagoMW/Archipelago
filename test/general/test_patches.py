import unittest
from worlds.AutoWorld import AutoWorldRegister
from worlds.Files import AutoPatchRegister

class TestPatches(unittest.TestCase):
    def test_patch_name_matches_game(self) -> None:
        for gamename in AutoPatchRegister.patch_types.keys():
            with self.subTest(game=gamename):
                self.assertTrue(gamename in AutoWorldRegister.world_types, 
                                f"Patch \"{gamename}\" does not match the name of any world.")