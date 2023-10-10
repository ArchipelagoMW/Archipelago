from worlds.alttp.Dungeons import get_dungeon_item_pool
from worlds.alttp.InvertedRegions import mark_dark_world_regions
from worlds.alttp.ItemPool import difficulties
from worlds.alttp.Items import ItemFactory
from test.TestBase import TestBase

from worlds.alttp.test import LTTPTestBase


class TestMinor(TestBase, LTTPTestBase):
    def setUp(self):
        self.world_setup()
        self.multiworld.logic[1] = "minorglitches"
        self.multiworld.difficulty_requirements[1] = difficulties['normal']
        self.multiworld.worlds[1].er_seed = 0
        self.multiworld.worlds[1].create_regions()
        self.multiworld.worlds[1].create_items()
        self.multiworld.required_medallions[1] = ['Ether', 'Quake']
        self.multiworld.itempool.extend(get_dungeon_item_pool(self.multiworld))
        self.multiworld.itempool.extend(ItemFactory(
            ['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1',
             'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))
        self.multiworld.get_location('Agahnim 1', 1).item = None
        self.multiworld.get_location('Agahnim 2', 1).item = None
        mark_dark_world_regions(self.multiworld, 1)
        self.multiworld.worlds[1].set_rules()
