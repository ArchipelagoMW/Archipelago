from __future__ import annotations
from typing import Sequence
from BaseClasses import CollectionState, ItemClassification

from test.bases import TestBase, WorldTestBase

class WL4TestBase(WorldTestBase, TestBase):
    game = 'Wario Land 4'
    player = 1

    starting_regions: Sequence[str] = []

    def get_state(self, items):
        if (self.multiworld, tuple(items)) in self._state_cache:
            return self._state_cache[self.multiworld, tuple(items)]
        state = CollectionState(self.multiworld)
        for region_name in self.starting_regions:
            region = self.multiworld.get_region(region_name, 1)
            state.reachable_regions[1].add(region)
            for exit in region.exits:
                if exit.connected_region is not None:
                    state.blocked_connections[1].add(exit)
        for item in items:
            item.classification = ItemClassification.progression
            state.collect(item)
        state.sweep_for_events()
        self._state_cache[self.multiworld, tuple(items)] = state
        return state

    def _create_items(self, items, player):
        singleton = False
        if isinstance(items, str):
            items = [items]
            singleton = True
        ret = [self.multiworld.worlds[player].create_item(item) for item in items]
        if singleton:
            return ret[0]
        return ret

    def _get_items(self, item_pool, all_except):
        if all_except and len(all_except) > 0:
            items = self.multiworld.itempool[:]
            items = [item for item in items if item.name not in all_except]
            items.extend(self._create_items(item_pool[0], 1))
        else:
            items = self._create_items(item_pool[0], 1)
        return self.get_state(items)

    def _get_items_partial(self, item_pool, missing_item):
        new_items = item_pool[0].copy()
        new_items.remove(missing_item)
        items = self._create_items(new_items, 1)
        return self.get_state(items)
