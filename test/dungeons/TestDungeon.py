import unittest

from BaseClasses import World, CollectionState
from Dungeons import create_dungeons, get_dungeon_item_pool
from EntranceShuffle import mandatory_connections, connect_simple
from ItemPool import difficulties, generate_itempool
from Items import ItemFactory
from Regions import create_regions
from Shops import create_shops
from Rules import set_rules


class TestDungeon(unittest.TestCase):
    def setUp(self):
        self.world = World(1, {1:'vanilla'}, {1:'noglitches'}, {1:'open'}, {1:'random'}, {1:'normal'}, {1:'normal'}, {1:False}, {1:'on'}, {1:'ganon'}, 'balanced',  {1:'items'},
                           True,  {1:False}, False, None,  {1:False})
        self.starting_regions = []  # Where to start exploring
        self.remove_exits = []      # Block dungeon exits
        self.world.difficulty_requirements[1] = difficulties['normal']
        create_regions(self.world, 1)
        create_dungeons(self.world, 1)
        create_shops(self.world, 1)
        for exitname, regionname in mandatory_connections:
            connect_simple(self.world, exitname, regionname, 1)
        connect_simple(self.world, 'Big Bomb Shop', 'Big Bomb Shop', 1)
        self.world.get_region('Menu', 1).exits = []
        self.world.swamp_patch_required[1] = True
        set_rules(self.world, 1)
        generate_itempool(self.world, 1)
        self.world.itempool.extend(get_dungeon_item_pool(self.world))
        self.world.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))

    def run_tests(self, access_pool):
        for exit in self.remove_exits:
            self.world.get_entrance(exit, 1).connected_region = self.world.get_region('Menu', 1)

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
                state.reachable_regions[1].add(self.world.get_region('Menu', 1))
                for region_name in self.starting_regions:
                    region = self.world.get_region(region_name, 1)
                    state.reachable_regions[1].add(region)
                    for exit in region.exits:
                        if exit.connected_region is not None:
                            state.blocked_connections[1].add(exit)

                for item in items:
                    item.advancement = True
                    state.collect(item)

                self.assertEqual(self.world.get_location(location, 1).can_reach(state), access)