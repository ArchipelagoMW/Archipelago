import unittest

from worlds.AutoWorld import AutoWorldRegister, Status
from . import setup_solo_multiworld


class TestWorldMemory(unittest.TestCase):
    def test_leak(self):
        """Tests that worlds don't leak references to MultiWorld or themselves with default options."""
        import gc
        import weakref
        for world_type in AutoWorldRegister.get_testable_world_types():
            with self.subTest("Game", game_name=world_type.game):
                weak = weakref.ref(setup_solo_multiworld(world_type))
                gc.collect()
                self.assertFalse(weak(), "World leaked a reference")
