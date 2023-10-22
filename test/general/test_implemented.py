import unittest
from worlds.AutoWorld import AutoWorldRegister

from . import setup_solo_multiworld


class TestImplemented(unittest.TestCase):
    def test_completion_condition(self):
        """Ensure a completion condition is set that has requirements."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden and game_name not in {"Sudoku"}:
                with self.subTest(game_name):
                    multiworld = setup_solo_multiworld(world_type)
                    self.assertFalse(multiworld.completion_condition[1](multiworld.state))

    def test_entrance_parents(self):
        """Tests that the parents of created Entrances match the exiting Region."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    multiworld = setup_solo_multiworld(world_type)
                    for region in multiworld.regions:
                        for exit in region.exits:
                            self.assertEqual(exit.parent_region, region)

    def test_stage_methods(self):
        """Tests that worlds don't try to implement certain steps that are only ever called as stage."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    for method in ("assert_generate",):
                        self.assertFalse(hasattr(world_type, method),
                                         f"{method} must be implemented as a @classmethod named stage_{method}.")
