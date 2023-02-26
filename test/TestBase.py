import typing
import unittest
import pathlib
from argparse import Namespace

import Utils
from test.general import gen_steps
from worlds import AutoWorld
from worlds.AutoWorld import call_all

file_path = pathlib.Path(__file__).parent.parent
Utils.local_path.cached_path = file_path

from BaseClasses import MultiWorld, CollectionState, ItemClassification, Item
from worlds.alttp.Items import ItemFactory


class TestBase(unittest.TestCase):
    multiworld: MultiWorld
    _state_cache = {}

    def get_state(self, items):
        if (self.multiworld, tuple(items)) in self._state_cache:
            return self._state_cache[self.multiworld, tuple(items)]
        state = CollectionState(self.multiworld)
        for item in items:
            item.classification = ItemClassification.progression
            state.collect(item)
        state.sweep_for_events()
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

                self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), access)

            # check for partial solution
            if not all_except and access:  # we are not supposed to be able to reach location with partial inventory
                for missing_item in item_pool[0]:
                    with self.subTest(msg="Location reachable without required item", location=location,
                                      items=item_pool[0], missing_item=missing_item, entry=i):
                        state = self._get_items_partial(item_pool, missing_item)
                        self.assertEqual(self.multiworld.get_location(location, 1).can_reach(state), False)

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
                        self.assertEqual(self.multiworld.get_entrance(entrance, 1).can_reach(state), False)

    def _get_items(self, item_pool, all_except):
        if all_except and len(all_except) > 0:
            items = self.multiworld.itempool[:]
            items = [item for item in items if
                     item.name not in all_except and not ("Bottle" in item.name and "AnyBottle" in all_except)]
            items.extend(ItemFactory(item_pool[0], 1))
        else:
            items = ItemFactory(item_pool[0], 1)
        return self.get_state(items)

    def _get_items_partial(self, item_pool, missing_item):
        new_items = item_pool[0].copy()
        new_items.remove(missing_item)
        items = ItemFactory(new_items, 1)
        return self.get_state(items)


class WorldTestBase(unittest.TestCase):
    options: typing.Dict[str, typing.Any] = {}
    multiworld: MultiWorld

    game: typing.ClassVar[str]  # define game name in subclass, example "Secret of Evermore"
    auto_construct: typing.ClassVar[bool] = True
    """ automatically set up a world for each test in this class """

    def setUp(self) -> None:
        if self.auto_construct:
            self.world_setup()

    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        if not hasattr(self, "game"):
            raise NotImplementedError("didn't define game name")
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = self.game
        self.multiworld.player_name = {1: "Tester"}
        self.multiworld.set_seed(seed)
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].option_definitions.items():
            setattr(args, name, {
                1: option.from_any(self.options.get(name, getattr(option, "default")))
            })
        self.multiworld.set_options(args)
        self.multiworld.set_default_common_options()
        for step in gen_steps:
            call_all(self.multiworld, step)

    def collect_all_but(self, item_names: typing.Union[str, typing.Iterable[str]]) -> None:
        if isinstance(item_names, str):
            item_names = (item_names,)
        for item in self.multiworld.get_items():
            if item.name not in item_names:
                self.multiworld.state.collect(item)

    def get_item_by_name(self, item_name: str) -> Item:
        for item in self.multiworld.get_items():
            if item.name == item_name:
                return item
        raise ValueError("No such item")

    def get_items_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        if isinstance(item_names, str):
            item_names = (item_names,)
        return [item for item in self.multiworld.itempool if item.name in item_names]

    def collect_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        """ collect all of the items in the item pool that have the given names """
        items = self.get_items_by_name(item_names)
        self.collect(items)
        return items

    def collect(self, items: typing.Union[Item, typing.Iterable[Item]]) -> None:
        if isinstance(items, Item):
            items = (items,)
        for item in items:
            self.multiworld.state.collect(item)

    def remove(self, items: typing.Union[Item, typing.Iterable[Item]]) -> None:
        if isinstance(items, Item):
            items = (items,)
        for item in items:
            if item.location and item.location.event and item.location in self.multiworld.state.events:
                self.multiworld.state.events.remove(item.location)
            self.multiworld.state.remove(item)

    def can_reach_location(self, location: str) -> bool:
        return self.multiworld.state.can_reach(location, "Location", 1)

    def can_reach_entrance(self, entrance: str) -> bool:
        return self.multiworld.state.can_reach(entrance, "Entrance", 1)

    def count(self, item_name: str) -> int:
        return self.multiworld.state.count(item_name, 1)

    def assertAccessDependency(self,
                               locations: typing.List[str],
                               possible_items: typing.Iterable[typing.Iterable[str]]) -> None:
        all_items = [item_name for item_names in possible_items for item_name in item_names]

        self.collect_all_but(all_items)
        for location in self.multiworld.get_locations():
            self.assertEqual(self.multiworld.state.can_reach(location), location.name not in locations)
        for item_names in possible_items:
            items = self.collect_by_name(item_names)
            for location in locations:
                self.assertTrue(self.can_reach_location(location))
            self.remove(items)

    def assertBeatable(self, beatable: bool):
        self.assertEqual(self.multiworld.can_beat_game(self.multiworld.state), beatable)
