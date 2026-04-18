import unittest
from argparse import Namespace

from BaseClasses import MultiWorld, CollectionState, ItemClassification
from worlds import AutoWorldRegister
from ..Items import item_factory


class TestBase(unittest.TestCase):
    multiworld: MultiWorld
    _state_cache = {}

    def get_state(self, items):
        if (self.multiworld, tuple(items)) in self._state_cache:
            return self._state_cache[self.multiworld, tuple(items)]
        state = CollectionState(self.multiworld)
        for item in items:
            item.classification = ItemClassification.progression
            state.collect(item, prevent_sweep=True)
        state.sweep_for_advancements()
        state.update_reachable_regions(1)
        self._state_cache[self.multiworld, tuple(items)] = state
        return state

    def get_path(self, state, region):
        def flist_to_iter(node):
            while node:
                value, node = node
                yield value

        from itertools import zip_longest
        reversed_path_as_flist = state.path.get(region, (region, None))
        string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
        # Now we combine the flat string list into (region, exit) pairs
        pathsiter = iter(string_path_flat)
        pathpairs = zip_longest(pathsiter, pathsiter)
        return list(pathpairs)

    def run_location_tests(self, access_pool):
        for i, (location, access, *item_pool) in enumerate(access_pool):
            items = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None
            state = self._get_items(item_pool, all_except)
            path = self.get_path(state, self.multiworld.get_location(location, 1).parent_region)
            with self.subTest(msg="Reach Location", location=location, access=access, items=items,
                              all_except=all_except, path=path, entry=i):

                self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), access,
                                 f"failed {self.multiworld.get_location(location, 1)} with: {item_pool}")

            # check for partial solution
            if not all_except and access:  # we are not supposed to be able to reach location with partial inventory
                for missing_item in item_pool[0]:
                    with self.subTest(msg="Location reachable without required item", location=location,
                                      items=item_pool[0], missing_item=missing_item, entry=i):
                        state = self._get_items_partial(item_pool, missing_item)

                        self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), False,
                                         f"failed {self.multiworld.get_location(location, 1)}: succeeded with "
                                         f"{missing_item} removed from: {item_pool}")

    def run_entrance_tests(self, access_pool):
        for i, (entrance, access, *item_pool) in enumerate(access_pool):
            items = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None
            state = self._get_items(item_pool, all_except)
            path = self.get_path(state, self.multiworld.get_entrance(entrance, 1).parent_region)
            with self.subTest(msg="Reach Entrance", entrance=entrance, access=access, items=items,
                              all_except=all_except, path=path, entry=i):

                self.assertEqual(self.multiworld.get_entrance(entrance, 1).can_reach(state), access)

            # check for partial solution
            if not all_except and access:  # we are not supposed to be able to reach location with partial inventory
                for missing_item in item_pool[0]:
                    with self.subTest(msg="Entrance reachable without required item", entrance=entrance,
                                      items=item_pool[0], missing_item=missing_item, entry=i):
                        state = self._get_items_partial(item_pool, missing_item)
                        self.assertEqual(self.multiworld.get_entrance(entrance, 1).can_reach(state), False,
                                         f"failed {self.multiworld.get_entrance(entrance, 1)} with: {item_pool}")

    def _get_items(self, item_pool, all_except):
        if all_except and len(all_except) > 0:
            items = self.multiworld.itempool[:]
            items = [item for item in items if
                     item.name not in all_except and not ("Bottle" in item.name and "AnyBottle" in all_except)]
            items.extend(item_factory(item_pool[0], self.multiworld.worlds[1]))
        else:
            items = item_factory(item_pool[0], self.multiworld.worlds[1])
        return self.get_state(items)

    def _get_items_partial(self, item_pool, missing_item):
        new_items = item_pool[0].copy()
        new_items.remove(missing_item)
        items = item_factory(new_items, self.multiworld.worlds[1])
        return self.get_state(items)


class LTTPTestBase(unittest.TestCase):
    def world_setup(self):
        from worlds.alttp.Options import Medallion
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = "A Link to the Past"
        self.multiworld.set_seed(None)
        args = Namespace()
        for name, option in AutoWorldRegister.world_types["A Link to the Past"].options_dataclass.type_hints.items():
            setattr(args, name, {1: option.from_any(getattr(option, "default"))})
        self.multiworld.set_options(args)
        self.multiworld.state = CollectionState(self.multiworld)
        self.world = self.multiworld.worlds[1]
        # by default medallion access is randomized, for unittests we set it to vanilla
        self.world.options.misery_mire_medallion.value = Medallion.option_ether
        self.world.options.turtle_rock_medallion.value = Medallion.option_quake
