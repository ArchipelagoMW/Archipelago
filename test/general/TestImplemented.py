import os
import unittest
from worlds.AutoWorld import AutoWorldRegister

from . import setup_solo_multiworld


class TestImplemented(unittest.TestCase):
    def testCompletionCondition(self):
        """Ensure a completion condition is set that has requirements."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden and game_name not in {"ArchipIDLE", "Sudoku"}:
                with self.subTest(game_name):
                    multiworld = setup_solo_multiworld(world_type)
                    self.assertFalse(multiworld.completion_condition[1](multiworld.state))

    def testEntranceParents(self):
        """Tests that the parents of created Entrances match the exiting Region."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    multiworld = setup_solo_multiworld(world_type)
                    for region in multiworld.regions:
                        for exit in region.exits:
                            self.assertEqual(exit.parent_region, region)

    def testStageMethods(self):
        """Tests that worlds don't try to implement certain steps that are only ever called as stage."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    for method in ("assert_generate",):
                        self.assertFalse(hasattr(world_type, method),
                                         f"{method} must be implemented as a @classmethod named stage_{method}.")

    def testHasTests(self):
        """Tests that worlds have implemented their own tests."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if game_name in {"Sudoku", "ChecksFinder", "Dark Souls III", "Donkey Kong Country 3", "Factorio",
                             "Final Fantasy", "Hollow Knight", "Hylics 2", "Meritous", "Ocarina of Time",
                             "Pokemon Red and Blue", "Raft", "Risk of Rain 2", "Sonic Adventure 2 Battle",
                             "Starcraft 2 Wings of Liberty", "Super Metroid", "Super Mario 64", "Super Mario World",
                             "SMZ3", "Slay the Spire", "Subnautica", "Timespinner", "VVVVVV", "The Witness"}\
                    or world_type.hidden:
                continue
            with self.subTest(game_name):
                path = f"{os.path.dirname(world_type.__file__)}/test/__init__.py"
                self.assertTrue(os.path.exists(path))
