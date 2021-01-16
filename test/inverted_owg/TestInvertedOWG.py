from BaseClasses import World
from Dungeons import create_dungeons, get_dungeon_item_pool
from EntranceShuffle import link_inverted_entrances
from InvertedRegions import create_inverted_regions
from ItemPool import generate_itempool, difficulties
from Items import ItemFactory
from Regions import mark_light_world_regions
from Shops import create_shops
from Rules import set_rules
from test.TestBase import TestBase


class TestInvertedOWG(TestBase):
    def setUp(self):
        self.world = World(1, {1:'vanilla'}, {1:'owglitches'}, {1:'inverted'}, {1:'random'}, {1:'normal'}, {1:'normal'}, {1:False}, {1:'on'}, {1:'ganon'}, 'balanced',  {1:'items'},
                           True,  {1:False}, False, None,  {1:False})
        self.world.difficulty_requirements[1] = difficulties['normal']
        create_inverted_regions(self.world, 1)
        create_dungeons(self.world, 1)
        create_shops(self.world, 1)
        link_inverted_entrances(self.world, 1)
        generate_itempool(self.world, 1)
        self.world.required_medallions[1] = ['Ether', 'Quake']
        self.world.itempool.extend(get_dungeon_item_pool(self.world))
        self.world.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))
        self.world.get_location('Agahnim 1', 1).item = None
        self.world.get_location('Agahnim 2', 1).item = None
        self.world.precollected_items.clear()
        self.world.itempool.append(ItemFactory('Pegasus Boots', 1))
        mark_light_world_regions(self.world, 1)
        set_rules(self.world, 1)
