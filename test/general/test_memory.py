import unittest

from BaseClasses import MultiWorld
from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld


class TestWorldMemory(unittest.TestCase):
    def test_leak(self) -> None:
        """Tests that worlds don't leak references to MultiWorld or themselves with default options."""
        import gc
        import weakref
        refs: dict[tuple[str, str], weakref.ReferenceType[MultiWorld]] = {}
        for game_name, testable_world in AutoWorldRegister.testable_worlds.items():
            world_type = testable_world.world_type
            for options_name, options in testable_world.testable_options_by_name.items():
                with self.subTest("Game creation", game_name=game_name, options=options_name):
                    weak = weakref.ref(setup_solo_multiworld(world_type, options=options))
                    refs[(game_name, options_name)] = weak
        gc.collect()
        for (game_name, options_name), weak in refs.items():
            with self.subTest("Game cleanup", game_name=game_name, options=options_name):
                self.assertFalse(weak(), "World leaked a reference")
