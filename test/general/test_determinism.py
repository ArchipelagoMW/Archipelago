from unittest import TestCase
from . import setup_solo_multiworld, gen_steps
from worlds.AutoWorld import AutoWorldRegister, call_single


class TestDeterminism(TestCase):
    def test_multiworld_random(self) -> None:
        """Tests that Worlds don't use `multiworld.random` outside class methods."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game_name):
                multiworld = setup_solo_multiworld(world_type, ())
                multiworld.random.seed(0)
                test_result = multiworld.random.random()
                multiworld.random.seed(0)
                for step in gen_steps:
                    call_single(multiworld, step, 1)
                    self.assertEqual(test_result, multiworld.random.random())
                    multiworld.random.seed(0)
