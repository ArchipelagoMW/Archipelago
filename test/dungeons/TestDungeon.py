import unittest

from BaseClasses import World, CollectionState
from Dungeons import create_dungeons, get_dungeon_item_pool
from EntranceShuffle import mandatory_connections, connect_simple
from ItemList import difficulties, generate_itempool
from Items import ItemFactory
from Regions import create_regions
from Rules import set_rules


class TestDungeon(unittest.TestCase):
    def setUp(self):
        self.world = World(1, 'vanilla', 'noglitches', 'open', 'random', 'normal', 'normal', 'none', 'on', 'ganon', 'balanced',
                           True, False, False, False, False, False, False, False, False, None,
                           'none', False)
        self.starting_regions = []
        self.world.difficulty_requirements = difficulties['normal']
        create_regions(self.world, 1)
        create_dungeons(self.world, 1)
        for exitname, regionname in mandatory_connections:
            connect_simple(self.world, exitname, regionname, 1)
        connect_simple(self.world, self.world.get_entrance('Big Bomb Shop', 1), self.world.get_region('Big Bomb Shop', 1), 1)
        self.world.swamp_patch_required[1] = True
        set_rules(self.world, 1)
        generate_itempool(self.world, 1)
        self.world.itempool.extend(get_dungeon_item_pool(self.world))
        self.world.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))

    def run_tests(self, access_pool):
        for region in self.starting_regions:
            self.world.get_region(region, 1).can_reach_private = lambda _: True

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