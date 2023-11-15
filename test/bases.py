import sys
import typing
import unittest
from argparse import Namespace

from test.general import gen_steps
from worlds import AutoWorld
from worlds.AutoWorld import call_all

from BaseClasses import Location, MultiWorld, CollectionState, ItemClassification, Item
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
            state.collect(item, event=True)
        state.sweep_for_events()
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
    memory_leak_tested: typing.ClassVar[bool] = False
    """ remember if memory leak test was already done for this class """

    def setUp(self) -> None:
        if self.auto_construct:
            self.world_setup()

    def tearDown(self) -> None:
        if self.__class__.memory_leak_tested or not self.options or not self.constructed or \
                sys.version_info < (3, 11, 0):  # the leak check in tearDown fails in py<3.11 for an unknown reason
            # only run memory leak test once per class, only for constructed with non-default options
            # default options will be tested in test/general
            super().tearDown()
            return

        import gc
        import weakref
        weak = weakref.ref(self.multiworld)
        for attr_name in dir(self):  # delete all direct references to MultiWorld and World
            attr: object = typing.cast(object, getattr(self, attr_name))
            if type(attr) is MultiWorld or isinstance(attr, AutoWorld.World):
                delattr(self, attr_name)
        state_cache: typing.Optional[typing.Dict[typing.Any, typing.Any]] = getattr(self, "_state_cache", None)
        if state_cache is not None:  # in case of multiple inheritance with TestBase, we need to clear its cache
            state_cache.clear()
        gc.collect()
        self.__class__.memory_leak_tested = True
        self.assertFalse(weak(), f"World {getattr(self, 'game', '')} leaked MultiWorld object")
        super().tearDown()

    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        if type(self) is WorldTestBase or \
                (hasattr(WorldTestBase, self._testMethodName)
                 and not self.run_default_tests and
                 getattr(self, self._testMethodName).__code__ is
                 getattr(WorldTestBase, self._testMethodName, None).__code__):
            return  # setUp gets called for tests defined in the base class. We skip world_setup here.
        if not hasattr(self, "game"):
            raise NotImplementedError("didn't define game name")
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = self.game
        self.multiworld.player_name = {1: "Tester"}
        self.multiworld.set_seed(seed)
        self.multiworld.state = CollectionState(self.multiworld)
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].options_dataclass.type_hints.items():
            setattr(args, name, {
                1: option.from_any(self.options.get(name, getattr(option, "default")))
            })
        self.multiworld.set_options(args)
        for step in gen_steps:
            call_all(self.multiworld, step)

    # methods that can be called within tests
    def collect_all_but(self, item_names: typing.Union[str, typing.Iterable[str]],
                        state: typing.Optional[CollectionState] = None) -> None:
        """Collects all pre-placed items and items in the multiworld itempool except those provided"""
        if isinstance(item_names, str):
            item_names = (item_names,)
        if not state:
            state = self.multiworld.state
        for item in self.multiworld.get_items():
            if item.name not in item_names:
                state.collect(item)

    def get_item_by_name(self, item_name: str) -> Item:
        """Returns the first item found in placed items, or in the itempool with the matching name"""
        for item in self.multiworld.get_items():
            if item.name == item_name:
                return item
        raise ValueError("No such item")

    def get_items_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        """Returns actual items from the itempool that match the provided name(s)"""
        if isinstance(item_names, str):
            item_names = (item_names,)
        return [item for item in self.multiworld.itempool if item.name in item_names]

    def collect_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        """ collect all of the items in the item pool that have the given names """
        items = self.get_items_by_name(item_names)
        self.collect(items)
        return items

    def collect(self, items: typing.Union[Item, typing.Iterable[Item]]) -> None:
        """Collects the provided item(s) into state"""
        if isinstance(items, Item):
            items = (items,)
        for item in items:
            self.multiworld.state.collect(item)
    
    def remove_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        """Remove all of the items in the item pool with the given names from state"""
        items = self.get_items_by_name(item_names)
        self.remove(items)
        return items

    def remove(self, items: typing.Union[Item, typing.Iterable[Item]]) -> None:
        """Removes the provided item(s) from state"""
        if isinstance(items, Item):
            items = (items,)
        for item in items:
            if item.location and item.location.event and item.location in self.multiworld.state.events:
                self.multiworld.state.events.remove(item.location)
            self.multiworld.state.remove(item)

    def can_reach_location(self, location: str) -> bool:
        """Determines if the current state can reach the provided location name"""
        return self.multiworld.state.can_reach(location, "Location", 1)

    def can_reach_entrance(self, entrance: str) -> bool:
        """Determines if the current state can reach the provided entrance name"""
        return self.multiworld.state.can_reach(entrance, "Entrance", 1)
    
    def can_reach_region(self, region: str) -> bool:
        """Determines if the current state can reach the provided region name"""
        return self.multiworld.state.can_reach(region, "Region", 1)

    def count(self, item_name: str) -> int:
        """Returns the amount of an item currently in state"""
        return self.multiworld.state.count(item_name, 1)

    def assertAccessDependency(self,
                               locations: typing.List[str],
                               possible_items: typing.Iterable[typing.Iterable[str]],
                               only_check_listed: bool = False) -> None:
        """Asserts that the provided locations can't be reached without the listed items but can be reached with any
         one of the provided combinations"""
        all_items = [item_name for item_names in possible_items for item_name in item_names]

        state = CollectionState(self.multiworld)
        self.collect_all_but(all_items, state)
        if only_check_listed:
            for location in locations:
                self.assertFalse(state.can_reach(location, "Location", 1), f"{location} is reachable without {all_items}")
        else:
            for location in self.multiworld.get_locations():
                loc_reachable = state.can_reach(location, "Location", 1)
                self.assertEqual(loc_reachable, location.name not in locations,
                                 f"{location.name} is reachable without {all_items}" if loc_reachable
                                 else f"{location.name} is not reachable without {all_items}")
        for item_names in possible_items:
            items = self.get_items_by_name(item_names)
            for item in items:
                state.collect(item)
            for location in locations:
                self.assertTrue(state.can_reach(location, "Location", 1),
                                f"{location} not reachable with {item_names}")
            for item in items:
                state.remove(item)

    def assertBeatable(self, beatable: bool):
        """Asserts that the game can be beaten with the current state"""
        self.assertEqual(self.multiworld.can_beat_game(self.multiworld.state), beatable)

    # following tests are automatically run
    @property
    def run_default_tests(self) -> bool:
        """Not possible or identical to the base test that's always being run already"""
        return (self.options
                or self.setUp.__code__ is not WorldTestBase.setUp.__code__
                or self.world_setup.__code__ is not WorldTestBase.world_setup.__code__)

    @property
    def constructed(self) -> bool:
        """A multiworld has been constructed by this point"""
        return hasattr(self, "game") and hasattr(self, "multiworld")

    def test_all_state_can_reach_everything(self):
        """Ensure all state can reach everything and complete the game with the defined options"""
        if not (self.run_default_tests and self.constructed):
            return
        with self.subTest("Game", game=self.game):
            excluded = self.multiworld.exclude_locations[1].value
            state = self.multiworld.get_all_state(False)
            for location in self.multiworld.get_locations():
                if location.name not in excluded:
                    with self.subTest("Location should be reached", location=location):
                        reachable = location.can_reach(state)
                        self.assertTrue(reachable, f"{location.name} unreachable")
            with self.subTest("Beatable"):
                self.multiworld.state = state
                self.assertBeatable(True)

    def test_empty_state_can_reach_something(self):
        """Ensure empty state can reach at least one location with the defined options"""
        if not (self.run_default_tests and self.constructed):
            return
        with self.subTest("Game", game=self.game):
            state = CollectionState(self.multiworld)
            locations = self.multiworld.get_reachable_locations(state, 1)
            self.assertGreater(len(locations), 0,
                               "Need to be able to reach at least one location to get started.")

    def test_fill(self):
        """Generates a multiworld and validates placements with the defined options"""
        if not (self.run_default_tests and self.constructed):
            return
        from Fill import distribute_items_restrictive

        # basically a shortened reimplementation of this method from core, in order to force the check is done
        def fulfills_accessibility() -> bool:
            locations = list(self.multiworld.get_locations(1))
            state = CollectionState(self.multiworld)
            while locations:
                sphere: typing.List[Location] = []
                for n in range(len(locations) - 1, -1, -1):
                    if locations[n].can_reach(state):
                        sphere.append(locations.pop(n))
                self.assertTrue(sphere or self.multiworld.accessibility[1] == "minimal",
                                f"Unreachable locations: {locations}")
                if not sphere:
                    break
                for location in sphere:
                    if location.item:
                        state.collect(location.item, True, location)
            return self.multiworld.has_beaten_game(state, 1)

        with self.subTest("Game", game=self.game, seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
            self.assertTrue(fulfills_accessibility(), "Collected all locations, but can't beat the game.")
            placed_items = [loc.item for loc in self.multiworld.get_locations() if loc.item and loc.item.code]
            self.assertLessEqual(len(self.multiworld.itempool), len(placed_items),
                                 "Unplaced Items remaining in itempool")
