import unittest

from BaseClasses import CollectionState
from Items import ItemFactory


class TestBase(unittest.TestCase):

    _state_cache = {}

    def get_state(self, items):
        if (self.world, tuple(items)) in self._state_cache:
            return self._state_cache[self.world, tuple(items)]
        state = CollectionState(self.world)
        for item in items:
            item.advancement = True
            state.collect(item)
        state.sweep_for_events()
        self._state_cache[self.world, tuple(items)] = state
        return state

    def run_location_tests(self, access_pool):
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
                state = self.get_state(items)

                self.assertEqual(self.world.get_location(location, 1).can_reach(state), access)

    def run_entrance_tests(self, access_pool):
        for entrance, access, *item_pool in access_pool:
            items = item_pool[0]
            all_except = item_pool[1] if len(item_pool) > 1 else None
            with self.subTest(entrance=entrance, access=access, items=items, all_except=all_except):
                if all_except and len(all_except) > 0:
                    items = self.world.itempool[:]
                    items = [item for item in items if item.name not in all_except and not ("Bottle" in item.name and "AnyBottle" in all_except)]
                    items.extend(ItemFactory(item_pool[0], 1))
                else:
                    items = ItemFactory(items, 1)
                state = self.get_state(items)

                self.assertEqual(self.world.get_entrance(entrance, 1).can_reach(state), access)