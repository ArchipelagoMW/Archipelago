import unittest
from worlds.AutoWorld import AutoWorldRegister

from . import setup_default_world


class TestImplemented(unittest.TestCase):
    def testCompletionCondition(self):
        """Ensure a completion condition is set that has requirements."""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden and gamename not in {"ArchipIDLE", "Final Fantasy", "Sudoku"}:
                with self.subTest(gamename):
                    world = setup_default_world(world_type)
                    self.assertFalse(world.completion_condition[1](world.state))
