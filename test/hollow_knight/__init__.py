from worlds.hk import HKWorld
from BaseClasses import MultiWorld
from worlds import AutoWorld
from worlds.hk.Options import hollow_knight_randomize_options, hollow_knight_skip_options

from test.TestBase import TestBase


class TestVanilla(TestBase):
    def setUp(self):
        self.world = MultiWorld(1)
        self.world.game[1] = "Hollow Knight"
        self.world.worlds[1] = HKWorld(self.world, 1)
        for hk_option in hollow_knight_randomize_options:
            setattr(self.world, hk_option, {1: True})
        for hk_option, option in hollow_knight_skip_options.items():
            setattr(self.world, hk_option, {1: option.default})
        AutoWorld.call_single(self.world, "create_regions", 1)
        AutoWorld.call_single(self.world, "generate_basic", 1)
        AutoWorld.call_single(self.world, "set_rules", 1)