import unittest

from Fill import distribute_items_restrictive
from NetUtils import encode
from worlds.AutoWorld import AutoWorldRegister, call_all, Status
from worlds import failed_world_loads
from . import setup_solo_multiworld


class TestImplemented(unittest.TestCase):
    def test_completion_condition(self):
        """Ensure a completion condition is set that has requirements."""
        for world_type in AutoWorldRegister.get_testable_world_types():
            if world_type.status != Status.hidden_enabled and world_type.game not in {"Sudoku"}:
                with self.subTest(world_type.game):
                    multiworld = setup_solo_multiworld(world_type)
                    self.assertFalse(multiworld.completion_condition[1](multiworld.state))

    def test_entrance_parents(self):
        """Tests that the parents of created Entrances match the exiting Region."""
        for world_type in AutoWorldRegister.get_testable_world_types():
            if world_type.status != Status.hidden_enabled:
                with self.subTest(world_type.game):
                    multiworld = setup_solo_multiworld(world_type)
                    for region in multiworld.regions:
                        for exit in region.exits:
                            self.assertEqual(exit.parent_region, region)

    def test_stage_methods(self):
        """Tests that worlds don't try to implement certain steps that are only ever called as stage."""
        for world_type in AutoWorldRegister.get_testable_world_types():
            if world_type.status != Status.hidden_enabled:
                with self.subTest(world_type.game):
                    for method in ("assert_generate",):
                        self.assertFalse(hasattr(world_type, method),
                                         f"{method} must be implemented as a @classmethod named stage_{method}.")

    def test_slot_data(self):
        """Tests that if a world creates slot data, it's json serializable."""
        for world_type in AutoWorldRegister.get_testable_world_types():
            # has an await for generate_output which isn't being called
            if world_type.game in {"Ocarina of Time", "Zillion"}:
                continue
            multiworld = setup_solo_multiworld(world_type)
            with self.subTest(game=world_type.game, seed=multiworld.seed):
                distribute_items_restrictive(multiworld)
                call_all(multiworld, "post_fill")
                for key, data in multiworld.worlds[1].fill_slot_data().items():
                    self.assertIsInstance(key, str, "keys in slot data must be a string")
                    self.assertIsInstance(encode(data), str, f"object {type(data).__name__} not serializable.")

    def test_no_failed_world_loads(self):
        if failed_world_loads:
            self.fail(f"The following worlds failed to load: {failed_world_loads}")
