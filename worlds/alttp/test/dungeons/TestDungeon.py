from BaseClasses import CollectionState, ItemClassification
from worlds.alttp.Dungeons import get_dungeon_item_pool
from worlds.alttp.EntranceShuffle import mandatory_connections, connect_simple
from worlds.alttp.ItemPool import difficulties
from worlds.alttp.Items import item_factory
from worlds.alttp.Regions import create_regions
from worlds.alttp.Shops import create_shops
from worlds.alttp.test import LTTPTestBase


class TestDungeon(LTTPTestBase):
    def setUp(self):
        self.world_setup()
        self.starting_regions = []  # Where to start exploring
        self.remove_exits = []      # Block dungeon exits
        self.multiworld.worlds[1].difficulty_requirements = difficulties['normal']
        self.multiworld.worlds[1].options.bombless_start.value = True
        self.multiworld.worlds[1].options.shuffle_capacity_upgrades.value = 2
        create_regions(self.multiworld, 1)
        self.multiworld.worlds[1].create_dungeons()
        create_shops(self.multiworld, 1)
        for exitname, regionname in mandatory_connections:
            connect_simple(self.multiworld, exitname, regionname, 1)
        connect_simple(self.multiworld, 'Big Bomb Shop', 'Big Bomb Shop', 1)
        self.multiworld.get_region('Menu', 1).exits = []
        self.multiworld.worlds[1].swamp_patch_required = True
        self.world.set_rules()
        self.world.create_items()
        self.multiworld.itempool.extend(get_dungeon_item_pool(self.multiworld))
        self.multiworld.itempool.extend(item_factory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], self.world))

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
                    items.extend(item_factory(item_pool[0], self.world))
                else:
                    items = item_factory(items, self.world)
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
                    state.collect(item, prevent_sweep=True)  # prevent_sweep=True prevents running sweep_for_advancements() and picking up
                state.sweep_for_advancements()             # key drop keys repeatedly

                self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), access, f"failed {self.multiworld.get_location(location, 1)} with: {item_pool}")
