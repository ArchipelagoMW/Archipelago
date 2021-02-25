from BaseClasses import MultiWorld
from worlds.hk.Regions import create_regions
from worlds.hk import gen_hollow

from test.TestBase import TestBase


class TestVanilla(TestBase):
    def setUp(self):
        self.world = MultiWorld(1, {1: 'vanilla'}, {1: 'noglitches'}, {1: 'open'}, {1: 'random'}, {1: 'normal'}, {1: 'normal'}, {1:False}, {1: 'on'}, {1: 'ganon'}, 'balanced', {1: 'items'},
                                True, {1:False}, False, None, {1:False})
        self.world.game[1] = "Hollow Knight"
        create_regions(self.world, 1)
        gen_hollow(self.world, 1)