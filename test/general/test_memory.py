import unittest

from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld


class TestWorldMemory(unittest.TestCase):
    def test_leak(self):
        """Tests that worlds don't leak references to MultiWorld or themselves with default options."""
        import gc
        import weakref
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game_name=game_name):
                weak = weakref.ref(setup_solo_multiworld(world_type))
                gc.collect()
                self.assertFalse(weak(), "World leaked a reference")
