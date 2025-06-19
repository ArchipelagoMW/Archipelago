from random import random
from unittest import TestCase

from BaseClasses import MultiWorld
from . import setup_solo_multiworld, gen_steps
from worlds.AutoWorld import AutoWorldRegister, call_single


class TestDeterminism(TestCase):
    def test_multiworld_random(self) -> None:
        """Tests that Worlds don't use `multiworld.random` outside class methods."""
        def rand(multiworld: MultiWorld) -> None:
            raise ValueError("multiworld random should not be called from World instance methods.")

        for game_name, world_type in AutoWorldRegister.world_types.items():
            multiworld = setup_solo_multiworld(world_type, ())
            setattr(multiworld, "random", property(rand))

            for step in gen_steps:

                with self.subTest(game_name, step=step):
                    call_single(multiworld, step, 1)
