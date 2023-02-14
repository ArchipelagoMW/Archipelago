import unittest
from worlds.AutoWorld import AutoWorldRegister

from . import setup_default_world


class TestImplemented(unittest.TestCase):
    def testCompletionCondition(self):
        """Ensure a completion condition is set that has requirements."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden and game_name not in {"ArchipIDLE", "Final Fantasy", "Sudoku"}:
                with self.subTest(game_name):
                    multiworld = setup_default_world(world_type)
                    self.assertFalse(multiworld.completion_condition[1](multiworld.state))

    def testEntranceParents(self):
        """Tests that the parents of created Entrances match the exiting Region."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden and game_name not in {"Final Fantasy"}:
                with self.subTest(game_name):
                    multiworld = setup_default_world(world_type)
                    for region in multiworld.regions:
                        for exit in region.exits:
                            self.assertEqual(exit.parent_region, region)
