from collections.abc import Callable
from random import Random
from unittest import TestCase

from . import setup_solo_multiworld, gen_steps
from worlds.AutoWorld import AutoWorldRegister, call_single, call_stage


class TestDeterminism(TestCase):
    def test_multiworld_random(self) -> None:
        """Tests that Worlds don't use `multiworld.random` outside class methods."""

        class RejectCallsRandom(Random):
            def __getattribute__(self, item):
                attribute = super().__getattribute__(item)

                if not allow_multiworld_random_calls and isinstance(attribute, Callable):
                    assert False

                return attribute

        for game_name, world_type in AutoWorldRegister.world_types.items():
            allow_multiworld_random_calls = True
            multiworld = setup_solo_multiworld(world_type, ())
            multiworld.random = RejectCallsRandom()

            for step in gen_steps:
                with self.subTest(game_name, step=step):
                    allow_multiworld_random_calls = False
                    call_single(multiworld, step, 1)
                    allow_multiworld_random_calls = True
                    call_stage(multiworld, step)
