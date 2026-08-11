"""`randomize_options`: let the seed pick the gameplay options.

Rolling is the easy half. The value is in the two corrections applied after,
both of which produce a broken seed if left to a coin flip:

  * `launch` goal + vanilla odds can be unwinnable (two attempts, 75% at best)
  * the item-adding options can together exceed the location count, which used
    to lose items silently and now refuses generation outright
"""
import unittest

from test.bases import WorldTestBase

from worlds.mmx5 import names
from worlds.mmx5.options import RANDOMIZED_OPTIONS

from . import MMX5TestBase


def build(seed: int, **opts):
    class T(WorldTestBase):
        game = "Mega Man X5"
        options = opts
    T.seed = seed
    t = T()
    t.setUp()
    return t


class TestRandomizeOff(MMX5TestBase):
    options = {"randomize_options": False, "goal": "sigma",
               "boss_difficulty": "intense", "pickupsanity": False}

    def test_yaml_values_are_respected(self) -> None:
        # NB `==` against a string is the supported Choice comparison; str()
        # gives "Goal(Sigma)", which silently matches nothing.
        o = self.multiworld.worlds[self.player].options
        self.assertTrue(o.goal == "sigma")
        self.assertTrue(o.boss_difficulty == "intense")
        self.assertFalse(bool(o.pickupsanity))


class TestRandomizeOn(unittest.TestCase):
    N = 40

    def setUp(self) -> None:
        self.worlds = [build(i, randomize_options=True) for i in range(self.N)]

    def _opts(self, t):
        return t.multiworld.worlds[t.player].options

    def test_every_seed_generates(self) -> None:
        self.assertEqual(len(self.worlds), self.N)

    def test_pool_always_balances(self) -> None:
        for t in self.worlds:
            pool = len(t.multiworld.itempool)
            locs = len([l for l in t.multiworld.get_locations(t.player)
                        if l.address is not None])
            self.assertEqual(pool, locs, "randomized options left an unbalanced pool")

    def test_never_rolls_the_unwinnable_launch_combination(self) -> None:
        # `==` against the string, NOT str(): str(o.goal) is "Goal(Launch)",
        # so a str() comparison here matches nothing and passes vacuously.
        # This test did exactly that before being caught.
        launch_goals = [t for t in self.worlds if self._opts(t).goal == "launch"]
        self.assertTrue(launch_goals, "no seed rolled the launch goal - test is vacuous")
        for t in launch_goals:
            self.assertFalse(self._opts(t).launch_odds == "vanilla",
                             "rolled launch goal with vanilla odds")

    def test_endgame_checks_is_left_alone(self) -> None:
        # Not in the roll: it only ever adds checks, so there is nothing to
        # gamble on, and Ivor asked for it to stay on.
        self.assertNotIn("endgame_checks", RANDOMIZED_OPTIONS)
        for t in self.worlds:
            self.assertTrue(bool(self._opts(t).endgame_checks))

    def test_actually_varies(self) -> None:
        # A roll that silently did nothing would still pass every test above.
        for name in RANDOMIZED_OPTIONS:
            values = {getattr(self._opts(t), name).value for t in self.worlds}
            self.assertGreater(len(values), 1, f"{name} never varied across {self.N} seeds")

    def test_reaches_every_value_of_each_choice(self) -> None:
        for name in ("goal", "boss_difficulty", "boss_hp_randomization"):
            option = getattr(self._opts(self.worlds[0]), name)
            expected = set(type(option).options.values())
            got = {getattr(self._opts(t), name).value for t in self.worlds}
            self.assertEqual(got, expected, f"{name} never reached some values")

    def test_rolls_from_the_world_rng_not_the_global_one(self) -> None:
        # The property that matters is reproducibility: a seed must replay.
        # That holds only if the roll draws from self.random. Using the `random`
        # module instead would pass every other test here and silently make
        # seeds unreproducible, so this drives _roll_options directly with a
        # known RNG rather than trying to seed the whole multiworld.
        import random as _random

        def roll_with(seed: int):
            world = self.worlds[0].multiworld.worlds[self.worlds[0].player]
            world.random = _random.Random(seed)
            world._roll_options()
            return {n: getattr(world.options, n).value for n in RANDOMIZED_OPTIONS}

        self.assertEqual(roll_with(4242), roll_with(4242),
                         "same RNG seed produced different options")
        self.assertNotEqual(roll_with(1), roll_with(2),
                            "different RNG seeds produced identical options")


class TestRandomizedOptionList(unittest.TestCase):
    def test_covers_every_gameplay_option(self) -> None:
        # Anything added to MMX5Options should be a deliberate include or
        # exclude here, not forgotten. This fails when a new option appears.
        from worlds.mmx5.options import MMX5Options
        import dataclasses
        declared = {f.name for f in dataclasses.fields(MMX5Options)}
        # endgame_checks, rematch_checks and reploid_checks only ever ADD
        # locations, so there is nothing to gamble on - deliberately not
        # rolled (see options.py).
        # exit_stage_anytime and water_stage_speed are pure comfort: one
        # lets you leave a stage you have not cleared, the other shortens a
        # forced-scroll section. Gambling them would randomly TAKE AWAY
        # quality of life rather than vary the challenge, which is not what
        # this option is for.
        excluded = {"start_inventory_from_pool", "randomize_options",
                    "endgame_checks", "rematch_checks", "reploid_checks",
                    "exit_stage_anytime", "water_stage_speed",
                    "progression_balancing", "accessibility",
                    "local_items", "non_local_items", "start_inventory",
                    "start_hints", "start_location_hints", "exclude_locations",
                    "priority_locations", "item_links", "death_link",
                    "plando_items", "plando_texts", "plando_connections"}
        unaccounted = declared - set(RANDOMIZED_OPTIONS) - excluded
        self.assertEqual(unaccounted, set(),
                         f"new option(s) not classified for randomize_options: {unaccounted}")
