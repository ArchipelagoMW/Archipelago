from BaseClasses import MultiWorld
from worlds.hk.Regions import create_regions
from worlds.hk import gen_hollow

from test.TestBase import TestBase


class TestVanilla(TestBase):
    def setUp(self):
        self.world = MultiWorld(1)
        self.world.game[1] = "Hollow Knight"
        import Options
        for hk_option in Options.hollow_knight_randomize_options:
            getattr(self.world, hk_option)[1] = True
        create_regions(self.world, 1)
        gen_hollow(self.world, 1)