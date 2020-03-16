import unittest

from BaseClasses import World, CollectionState
from Dungeons import create_dungeons, get_dungeon_item_pool
from EntranceShuffle import link_entrances
from InvertedRegions import mark_dark_world_regions
from ItemList import difficulties
from Items import ItemFactory
from Regions import create_regions
from Rules import set_rules


class TestVanilla(unittest.TestCase):
    def setUp(self):
        self.world = World(1, 'vanilla', 'noglitches', 'open', 'random', 'normal', 'normal', 'none', 'on', 'ganon', 'balanced',
                           True, False, False, False, False, False, False, False, False, None,
                           'none', False)
        self.world.difficulty_requirements = difficulties['normal']
        create_regions(self.world, 1)
        create_dungeons(self.world, 1)
        link_entrances(self.world, 1)
        mark_dark_world_regions(self.world)
        set_rules(self.world, 1)

    def run_tests(self, access_pool):
        for location, access, *item_pool in access_pool:
            items = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None
            with self.subTest(location=location, access=access, items=items, all_except=all_except):
                if all_except and len(all_except) > 0:
                    items = self.world.itempool[:]
                    items = [item for item in items if item.name not in all_except and not ("Bottle" in item.name and "AnyBottle" in all_except)]
                    items.extend(ItemFactory(item_pool[0], 1))
                else:
                    items = ItemFactory(items, 1)
                state = CollectionState(self.world)
                for item in items:
                    item.advancement = True
                    state.collect(item)

                self.assertEqual(self.world.get_location(location, 1).can_reach(state), access)