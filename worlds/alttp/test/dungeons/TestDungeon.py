import unittest
from argparse import Namespace

from BaseClasses import MultiWorld, CollectionState, ItemClassification
from worlds.alttp.Dungeons import create_dungeons, get_dungeon_item_pool
from worlds.alttp.EntranceShuffle import mandatory_connections, connect_simple
from worlds.alttp.ItemPool import difficulties, generate_itempool
from worlds.alttp.Items import ItemFactory
from worlds.alttp.Regions import create_regions
from worlds.alttp.Shops import create_shops
from worlds.alttp.Rules import set_rules
from worlds import AutoWorld


class TestDungeon(unittest.TestCase):
    def setUp(self):
        self.multiworld = MultiWorld(1)
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types["A Link to the Past"].option_definitions.items():
            setattr(args, name, {1: option.from_any(option.default)})
        self.multiworld.set_options(args)
        self.multiworld.set_default_common_options()
        self.starting_regions = []  # Where to start exploring
        self.remove_exits = []      # Block dungeon exits
        self.multiworld.difficulty_requirements[1] = difficulties['normal']
        create_regions(self.multiworld, 1)
        create_dungeons(self.multiworld, 1)
        create_shops(self.multiworld, 1)
        for exitname, regionname in mandatory_connections:
            connect_simple(self.multiworld, exitname, regionname, 1)
        connect_simple(self.multiworld, 'Big Bomb Shop', 'Big Bomb Shop', 1)
        self.multiworld.get_region('Menu', 1).exits = []
        self.multiworld.swamp_patch_required[1] = True
        self.multiworld.worlds[1].set_rules()
        self.multiworld.worlds[1].create_items()
        self.multiworld.itempool.extend(get_dungeon_item_pool(self.multiworld))
        self.multiworld.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))

    def run_tests(self, access_pool):
        for exit in self.remove_exits:
            self.multiworld.get_entrance(exit, 1).connected_region = self.multiworld.get_region('Menu', 1)

        for location, access, *item_pool in access_pool:
            items = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None
            with self.subTest(location=location, access=access, items=items, all_except=all_except):
                if all_except and len(all_except) > 0:
                    items = self.multiworld.itempool[:]
                    items = [item for item in items if item.name not in all_except and not ("Bottle" in item.name and "AnyBottle" in all_except)]
                    items.extend(ItemFactory(item_pool[0], 1))
                else:
                    items = ItemFactory(items, 1)
                state = CollectionState(self.multiworld)
                state.reachable_regions[1].add(self.multiworld.get_region('Menu', 1))
                for region_name in self.starting_regions:
                    region = self.multiworld.get_region(region_name, 1)
                    state.reachable_regions[1].add(region)
                    for exit in region.exits:
                        if exit.connected_region is not None:
                            state.blocked_connections[1].add(exit)

                for item in items:
                    item.classification = ItemClassification.progression
                    state.collect(item)

                self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), access)