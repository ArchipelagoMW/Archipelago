import unittest

from BaseClasses import MultiWorld
from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld


class TestWorldMemory(unittest.TestCase):
    def test_leak(self) -> None:
        """Tests that worlds don't leak references to MultiWorld or themselves with default options."""
        import gc
        import weakref
        refs: dict[str, weakref.ReferenceType[MultiWorld]] = {}
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game creation", game_name=game_name):
                weak = weakref.ref(setup_solo_multiworld(world_type))
                refs[game_name] = weak
        gc.collect()
        for game_name, weak in refs.items():
            with self.subTest("Game cleanup", game_name=game_name):
                self.assertFalse(weak(), "World leaked a reference")
