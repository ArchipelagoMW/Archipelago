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
from Options import alttp_options

class TestVanilla(TestBase):
    def setUp(self):
        self.world = MultiWorld(1)
        for option_name, option in alttp_options.items():
            setattr(self.world, option_name, {1: option.default})
        self.world.logic[1] = "noglitches"
        self.world.difficulty_requirements[1] = difficulties['normal']
        create_regions(self.world, 1)
        create_dungeons(self.world, 1)
        create_shops(self.world, 1)
        link_entrances(self.world, 1)
        generate_itempool(self.world, 1)
        self.world.required_medallions[1] = ['Ether', 'Quake']
        self.world.itempool.extend(get_dungeon_item_pool(self.world))
        self.world.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))
        self.world.get_location('Agahnim 1', 1).item = None
        self.world.get_location('Agahnim 2', 1).item = None
        mark_dark_world_regions(self.world, 1)
        set_rules(self.world, 1)