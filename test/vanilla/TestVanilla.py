from argparse import Namespace

from BaseClasses import MultiWorld
from worlds.alttp.Dungeons import create_dungeons, get_dungeon_item_pool
from worlds.alttp.EntranceShuffle import link_entrances
from worlds.alttp.InvertedRegions import mark_dark_world_regions
from worlds.alttp.ItemPool import difficulties, generate_itempool
from worlds.alttp.Items import ItemFactory
from worlds.alttp.Regions import create_regions
from worlds.alttp.Shops import create_shops
from worlds.alttp.Rules import set_rules
from test.TestBase import TestBase
from worlds import AutoWorld

class TestVanilla(TestBase):
    def setUp(self):
        self.world = MultiWorld(1)
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types["A Link to the Past"].option_definitions.items():
            setattr(args, name, {1: option.from_any(option.default)})
        self.world.set_options(args)
        self.world.set_default_common_options()
        self.world.logic[1] = "noglitches"
        self.world.difficulty_requirements[1] = difficulties['normal']
        create_regions(self.world, 1)
        create_dungeons(self.world, 1)
        create_shops(self.world, 1)
        link_entrances(self.world, 1)
        self.world.worlds[1].create_items()
        self.world.required_medallions[1] = ['Ether', 'Quake']
        self.world.itempool.extend(get_dungeon_item_pool(self.world))
        self.world.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))
        self.world.get_location('Agahnim 1', 1).item = None
        self.world.get_location('Agahnim 2', 1).item = None
        mark_dark_world_regions(self.world, 1)
        self.world.worlds[1].set_rules()