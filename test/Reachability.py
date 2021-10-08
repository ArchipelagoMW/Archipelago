import unittest
from argparse import Namespace
from BaseClasses import MultiWorld
from worlds.AutoWorld import AutoWorldRegister, call_all


class TestBase(unittest.TestCase):
    _state_cache = {}
    gen_steps = ["generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill"]

    def testAllStateCanReachEverything(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if game_name != "Ori and the Blind Forest":  # TODO: fix Ori Logic
                with self.subTest("Game", game=game_name):

                    world = MultiWorld(1)
                    world.game[1] = game_name
                    world.player_name = {1: "Tester"}
                    world.set_seed()
                    args = Namespace()
                    for name, option in world_type.options.items():
                        setattr(args, name, {1: option.from_any(option.default)})
                    world.set_options(args)
                    world.set_default_common_options()
                    for step in self.gen_steps:
                        call_all(world, step)
                    state = world.get_all_state(False)
                    for location in world.get_locations():
                        with self.subTest("Location should be reached", location=location):
                            self.assertTrue(location.can_reach(state))
