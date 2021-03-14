from BaseClasses import MultiWorld
from worlds.hk.Regions import create_regions
from worlds.hk import gen_hollow

from test.TestBase import TestBase


class TestVanilla(TestBase):
    def setUp(self):
        self.world = MultiWorld(1)
        self.world.game[1] = "Hollow Knight"
        create_regions(self.world, 1)
        gen_hollow(self.world, 1)