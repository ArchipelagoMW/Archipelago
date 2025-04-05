import unittest

from worlds.AutoWorld import AutoWorldRegister, call_all
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    gen_steps = (
        "generate_early",
        "create_regions",
    )

    test_steps = (
        "create_items",
        "set_rules",
        "connect_entrances",
        "generate_basic",
        "pre_fill",
    )

    def test_all_state_is_available(self):
        """Ensure all_state can be created at certain steps."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type, self.gen_steps)
                for step in self.test_steps:
                    with self.subTest("Step", step=step):
                        call_all(multiworld, step)
                        self.assertTrue(multiworld.get_all_state(False, True))
