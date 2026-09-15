from collections import Counter, defaultdict
from functools import cache
import logging
from typing import (
    Iterable, Dict, List, Tuple, Hashable, cast, Type, FrozenSet, NamedTuple, Optional, Union, Callable, Collection, Set
)
from contextlib import ExitStack

from BaseClasses import CollectionState, Item, Location
from Options import Option

from . import HatInTimeTestBase
from ..Rules import act_connections
from .. import HatInTimeWorld

from .logic_test_helpers import (
    block_access, Spot, SpotData, TestOptions, AnyOptions, TestConditions,
    mock_region_access, mock_no_region_access, mock_can_clear_acts, mock_can_clear_all_acts
)
from . import logic_test_data


UniqueTestOptionsKey = FrozenSet[Tuple[str, Hashable]]


class SpotTest(NamedTuple):
    """A list of spots to test reachability and the test conditions to set up."""
    spots: List[SpotData]
    conditions: TestConditions


class TestSpotLogic(HatInTimeTestBase):
    """
    Tests the logic of various AHiT Locations/Entrances/Regions.

    All kinds of spot are tested together to minimise the number of worlds that have to be set up to test all the
    different option combinations.
    """
    # Do not run default tests.
    run_default_tests = False
    # Do not set up a default world.
    auto_construct = False

    # Some commonly looked up values are cached for better test performance.
    _cached_item_from_pool_lookup: Optional[Dict[str, List[Item]]]
    cached_spot_lookup: Callable[[SpotData], Spot]
    cached_filled_advancements: List[Location]
    cached_advancements_in_pool: List[Item]

    def setUp(self) -> None:
        super().setUp()
        self.cached_filled_advancements = []
        self.cached_advancements_in_pool = []
        del self.cached_item_pool_advancement_lookup

        def dummy_cached_get_spot(spot_data: SpotData):
            raise RuntimeError("cached_spot_lookup called before world_setup")

        self.cached_spot_lookup = dummy_cached_get_spot

    def tearDown(self) -> None:
        # Must be cleared before `super().tearDown()` because `super().tearDown()` checks for not having leaked the
        # world/multiworld. `cached_spot_lookup` stores Location/Entrance/Region instances, which reference the
        # MultiWorld and `cached_item_pool_advancement_lookup` stores Item instances which can reference Location
        # instances.
        del self.cached_spot_lookup
        del self.cached_item_pool_advancement_lookup
        self.cached_advancements_in_pool = []
        self.cached_filled_advancements = []
        super().tearDown()

    @property
    def cached_item_pool_advancement_lookup(self):
        """
        Tests frequently need to collect advancement items from the item pool, so these are found from the pool in
        advance and cached into a dictionary by item name.
        """
        from_pool_lookup = self._cached_item_from_pool_lookup
        if from_pool_lookup is None:
            from_pool_lookup = defaultdict(list)
            from_pool_lookup.clear()
            for item in self.cached_advancements_in_pool:
                from_pool_lookup[item.name].append(item)
            self._cached_item_from_pool_lookup = from_pool_lookup
        return from_pool_lookup

    @cached_item_pool_advancement_lookup.deleter
    def cached_item_pool_advancement_lookup(self):
        self._cached_item_from_pool_lookup = None

    # todo: Instead of setting chapter costs to pre-determined values, use special items in the tests that represent the
    #  time pieces for a specific chapter and swap them out the special items for the correct number of time pieces
    #  during the test.
    def world_setup(self, seed: Optional[int] = None) -> None:
        """
        In addition to the standard world setup:

        Removes the usual accessibility to regions by blocking connections. This enables testing logic starting from a
        specific region being accessible.
        - Blocks all connections from the origin region.
        - Blocks all connections to the origin region.
        - Blocks all connections between telescope acts ('act connections').

        Sets chapter costs to pre-determined values. This keeps the test data simpler because the test data can include
        the pre-determined number of Time Pieces for chapter access instead of needing to set the Time Pieces in test
        data dynamically after world setup is complete.

        Sets/resets cached lookups that are specific to the newly created world.
        """
        super().world_setup(seed)

        # The item pool lookup may not be needed, so is cached automatically when accessed. To ensure there is no old
        # data in the cache, it is cleared here.
        del self.cached_item_pool_advancement_lookup

        world = cast(HatInTimeWorld, self.world)

        # Cache filled locations so that there is no need to check all locations each time filled locations are needed.
        self.cached_filled_advancements = [loc for loc in world.multiworld.get_locations(world.player)
                                           if loc.advancement]
        # Cache advancement items
        self.cached_advancements_in_pool = [item for item in self.multiworld.itempool if item.advancement]

        # Create a cached spot lookup for the current world instance. This particularly helps with looking up
        # randomized regions because looking up randomized regions is an inefficient operation.
        @cache
        def get_spot(spot_data_: SpotData):
            return spot_data_.get_spot(world)

        self.cached_spot_lookup = get_spot

        origin_region = world.get_region(world.origin_region_name)

        # Block all connections from the origin region.
        for entrance in list(origin_region.exits):
            block_access(entrance)

        # Remove all connections to the origin region.
        for entrance in list(origin_region.entrances):
            block_access(entrance)

        # Remove all act connections to avoid gaining access to an act we are not testing, from an act we are testing.
        # e.g. Chapter 1 Act 1 has a connection to Acts 2 and 3 because completing Act 1 unlocks Acts 2 and 3. If state
        # is able to reach the Chapter 1 Act 1 entrance and is able to reach the Act Completion location of the act/rift
        # placed at Chapter 1 Act 1, then the entrances to Act 2 and 3, from Act 1, are accessible.
        # Note: This does not remove connections to Time Rifts, but with act randomization disabled, Time Rifts are
        # always dead ends.
        for key, acts in act_connections.items():
            if key.startswith("The Arctic Cruise") and not world.options.EnableDLC1:
                continue
            for i, act in enumerate(acts, start=1):
                entrance_name: str = f"{key}: Connection {i}"
                entrance = world.get_entrance(entrance_name)
                block_access(entrance)

        # Overwrite chapter costs to fixed values so that TestData can contain pre-determined numbers of required Time
        # Pieces when testing logic that requires entering a chapter door.
        costs = world.chapter_timepiece_costs
        for chapter_index, cost in logic_test_data.TEST_CHAPTER_TIMEPIECE_COSTS.items():
            costs[chapter_index] = cost

    def get_items_by_name_counts(self, item_names: Union[str, Iterable[str]]) -> List[Item]:
        """
        Returns actual items from the itempool that match the provided name(s), but only as many of each as are present
        in `item_names`
        """
        if isinstance(item_names, str):
            item_names = (item_names,)
        names_counter = Counter(item_names)
        items = []
        from_pool_lookup = self.cached_item_pool_advancement_lookup
        for name, count in names_counter.items():
            items.extend(from_pool_lookup[name][:count])
        return items

    def assertAccessDependencyPoolOnlyExtended(self,
                                               spot: Spot,
                                               possible_items: Collection[Iterable[str]]) -> None:
        """
        Asserts that the provided location can only be reached with any one of the provided combinations of items.

        Extended from WorldTestBase.assertAccessDependency to also check that any one item missing from a provided
        combination should result in the location being unreachable.

        Modified to only collect items from the item pool and then sweep, rather than collecting all items from both the
        item pool and filled locations that are not in `possible_items`. Collecting all items from filled locations
        would also pick up unreachable event items that AHiT uses to signify access to a specific region. Collecting
        these event items when their locations are unreachable would make it impossible to test some conditions that
        should be able to reach a provided location.
        """
        # Collect everything from the pool except the items being tested, and then sweep.
        all_items = [item_name for item_names in possible_items for item_name in item_names]
        all_items_set = set(all_items)
        state = CollectionState(self.multiworld)
        self.collect_all_from_pool_but_and_sweep(all_items_set, state)

        # Assert that the location is unreachable without any of the sets of items that should be required to reach it.
        self.assertFalse(spot.can_reach(state), f"{spot.name} should not be reachable without some of {all_items}")

        for item_names in possible_items:
            items = self.get_items_by_name_counts(item_names)
            expected_item_counts = Counter(item_names)
            actual_item_counts = Counter(item.name for item in items)
            self.assertEqual(actual_item_counts, expected_item_counts,
                             "Fewer items existed in the item pool than expected.")

            # Collect all of these possible items into a state.
            state_with_all = state.copy()
            for item in items:
                state_with_all.collect(item, prevent_sweep=True)

            # Assert that the location is reachable with all of these items from the item pool.
            test_state = state_with_all.copy()
            # For better test performance, only sweep if needed.
            if not spot.can_reach(test_state):
                test_state.sweep_for_advancements(self.cached_filled_advancements)
                self.assertTrue(spot.can_reach(test_state), f"{spot.name} should be reachable with {item_names}")

            # Assert that the location is unreachable if any one of the items is missing.
            for i in range(len(items)):
                state_missing_one = state_with_all.copy()
                skipped_item = items[i]
                state_missing_one.remove(skipped_item)
                state_missing_one.sweep_for_advancements(self.cached_filled_advancements)
                self.assertFalse(spot.can_reach(state_missing_one), f"{spot.name} should not be reachable without"
                                                                    f" {skipped_item.name}")

    def collect_all_from_pool_but_and_sweep(self, item_names: Union[str, Iterable[str]],
                                            state: CollectionState) -> None:
        """
        Collect all items from the item pool whose names are not in `item_names` and then sweep to pick up placed items.

        The main purpose of this function is as a replacement for WorldTestBase.collect_all_but() that does not collect
        unreachable event items for cases where logic checks for state having collected an event item placed in a region
        rather than checking for access to that region.
        """
        if isinstance(item_names, str):
            item_name: str = item_names
            for item in self.cached_advancements_in_pool:
                if item.name != item_name and item.advancement:
                    state.collect(item, prevent_sweep=True)
        else:
            item_names = set(item_names)
            if item_names:
                for item in self.cached_advancements_in_pool:
                    if item.name not in item_names and item.advancement:
                        state.collect(item, prevent_sweep=True)
            else:
                # Collect every advancement item.
                for item in self.cached_advancements_in_pool:
                    if item.advancement:
                        state.collect(item, prevent_sweep=True)
        # Only sweep once at the end for performance.
        state.sweep_for_advancements(self.cached_filled_advancements)

    def inaccessible_spot_test(self, spot: Spot, possible_items: Collection[Iterable[str]],
                               access_regions: Iterable[str], required_clearable_acts: Iterable[str] = ()) -> None:
        """
        Test that with access to the given regions, and any of the sets of possible items, the location is inaccessible.
        """
        # There are multiple contexts to enter and undo upon leaving the context, so use an ExitStack.
        with ExitStack() as exit_stack:
            # Grant access to all the specified regions. Other regions that these regions connect to may indirectly
            # become accessible.
            for region in access_regions:
                exit_stack.enter_context(mock_region_access(self.world, region))

            # Mark all the specified acts as clearable.
            exit_stack.enter_context(mock_can_clear_acts(required_clearable_acts))

            if possible_items:
                # For each set of items collected into a state, test that the location is unreachable.
                for item_names in possible_items:
                    state = CollectionState(self.multiworld)
                    self.collect_all_from_pool_but_and_sweep(item_names, state)
                    self.assertFalse(spot.can_reach(state), f"{spot.name} should not be reachable with everything but"
                                                            f" {item_names}")
            else:
                # There are no sets of items, so test that the location in unreachable even with all items.
                state = CollectionState(self.multiworld)
                self.collect_all_from_pool_but_and_sweep((), state)
                self.assertFalse(spot.can_reach(state), f"{spot.name} should not be reachable with no items")

    def spot_test(self, spot: Spot, possible_items: Collection[Iterable[str]],
                  required_regions: Iterable[str], required_clearable_acts: Iterable[str] = ()) -> None:
        # Check that even with all items and all acts clearable, if any required region is inaccessible, the location is
        # unreachable.
        with mock_can_clear_all_acts():
            required_regions = list(required_regions)
            for i in range(len(required_regions)):
                skipped_region = required_regions[i]
                # There are multiple contexts to enter and undo upon leaving the context, so use an ExitStack.
                with ExitStack() as exit_stack:
                    # Ensure the skipped region is inaccessible by temporarily blocking all entrances that connect to it.
                    exit_stack.enter_context(mock_no_region_access(self.world, skipped_region))
                    for j, region in enumerate(required_regions):
                        if j != i:
                            exit_stack.enter_context(mock_region_access(self.world, region))
                    state = CollectionState(self.multiworld)
                    self.collect_all_from_pool_but_and_sweep((), state)
                    self.assertFalse(spot.can_reach(state), f"{spot.name} should not be reachable without access to"
                                                            f" region {skipped_region}")

        # There are multiple contexts to enter and undo upon leaving the context, so use an ExitStack.
        with ExitStack() as exit_stack:
            for region in required_regions:
                exit_stack.enter_context(mock_region_access(self.world, region))

            # Check that with all required regions, that each of the required clearable acts are required
            required_clearable_acts = list(required_clearable_acts)
            if required_clearable_acts:
                for i in range(len(required_clearable_acts)):
                    skipped = required_clearable_acts[i]
                    acts = required_clearable_acts.copy()
                    del acts[i]
                    with mock_can_clear_acts(acts):
                        state = CollectionState(self.multiworld)
                        self.collect_all_from_pool_but_and_sweep((), state)
                        self.assertFalse(spot.can_reach(state), f"{spot.name} should not be reachable without being"
                                                                f" able to complete act {skipped}")

                # Now that it is confirmed that each required clearable act is indeed required, temporarily consider
                # them all clearable while checking the items.
                exit_stack.enter_context(mock_can_clear_acts(required_clearable_acts))

            # Finally, now that it is confirmed that each of the required regions and required clearable acts are
            # required, check that each sequence of possible items is required.
            if possible_items:
                self.assertAccessDependencyPoolOnlyExtended(spot, possible_items)
            else:
                # The location should be reachable with just access to the regions. No items from the item pool are
                # required.
                state = CollectionState(self.multiworld)
                # For better test performance, only sweep if needed.
                if not spot.can_reach(state):
                    state.sweep_for_advancements(self.cached_filled_advancements)
                    self.assertTrue(spot.can_reach(state), f"{spot.name} should be reachable without any items")

        # The location should be inaccessible with all items, but no region access.
        state = CollectionState(self.multiworld)
        self.collect_all_from_pool_but_and_sweep((), state)
        self.assertFalse(spot.can_reach(state))

    def validate_options(self, options_tests_pairs: Iterable[Tuple[TestOptions, List[SpotTest]]]):
        # Validate that each option exists and has a valid value.
        # This prevents typing an incorrect option name or value in one of the tests.
        ahit_options_type_hints: Dict[str, Type[Option]] = HatInTimeWorld.options_dataclass.type_hints
        all_ahit_option_keys = ahit_options_type_hints.keys()
        already_checked_options: Set[Tuple[str, Hashable]] = set()
        for options, tests in options_tests_pairs:
            option_keys = set(options.keys())
            invalid_options = option_keys.difference(all_ahit_option_keys)
            if invalid_options:
                self.fail(f"No such options {sorted(invalid_options)} for tests {tests}")
            failed_options = []
            for option_key, option_value in options.items():
                if isinstance(option_value, dict):
                    hashable_value = frozenset(cast(dict[str, str], option_value).items())
                    hashable_option_pair = (option_key, hashable_value)
                else:
                    # Everything else should be hashable. `frozenset` can be used in place of `set`, and `tuple` can be
                    # used in place of `list`.
                    hashable_option_pair = (option_key, option_value)

                if hashable_option_pair in already_checked_options:
                    continue

                option_type = ahit_options_type_hints[option_key]
                try:
                    option_type.from_any(option_value)
                except KeyError:
                    failed_options.append(dict(option_key=option_key, option_value=option_value))
                already_checked_options.add(hashable_option_pair)
            if failed_options:
                self.fail(f"Could not parse option values for {failed_options} for tests {tests}")

    @staticmethod
    def get_grouped_test_data() -> Iterable[Tuple[AnyOptions, List[SpotTest]]]:
        """
        Group test data by unique sets of options.

        Grouping by options reduces the number of worlds that must be set up to run the tests because each unique set of
        options can share a single world.
        """
        options_key_to_options_tests_pairs: Dict[UniqueTestOptionsKey, Tuple[AnyOptions, List[SpotTest]]] = {}
        base_options = logic_test_data.BASE_WORLD_OPTIONS
        test_spots: List[SpotData]
        for spot_type, test_data in logic_test_data.ALL_TESTS:
            for locations_raw, conditions_list in test_data.items():
                if isinstance(locations_raw, str):
                    test_spots = [SpotData(spot_type, locations_raw)]
                else:
                    test_spots = [SpotData(spot_type, loc) for loc in locations_raw]
                for conditions in conditions_list:
                    # Ignore all options matching the base options.
                    options = {k: v for k, v in conditions.options.items() if base_options.get(k) != v}
                    if spot_type == "RandomizedRegion":
                        # Insanity act randomization can create alternate routes to reach the target region if the
                        # access region(s) contain Time Rift entrances. These need to be blocked off to prevent false
                        # positives/negatives. We do this by plando-ing dead-end acts/time rifts onto these entrances,
                        # so that they cannot form connections that can reach the region being tested through
                        # alternative means.
                        hashable_insanity_act_plando = cast(frozenset[tuple[str, str]] | None,
                                                            options.get("_InsanityActPlando"))
                        if hashable_insanity_act_plando is not None:
                            del options["_InsanityActPlando"]

                        # Add a test for each act randomization option.
                        for act_rando in ("false", "light", "insanity"):
                            if (base_options.get("ActRandomizer") != act_rando
                                    or (act_rando == "insanity" and hashable_insanity_act_plando is not None)):
                                hashable_act_rando_options = options.copy()
                                hashable_act_rando_options.update(dict(ActRandomizer=act_rando))
                            else:
                                # Not going to modify, so no need to copy.
                                hashable_act_rando_options = options
                            # dict is not hashable, but a frozenset of the dict's items is when all the dict's values
                            # are hashable.
                            options_key = frozenset(hashable_act_rando_options.items())

                            # Use a new variable for the new type now that it is guaranteed that only hashable values
                            # went into creating `options_key`.
                            act_rando_options = cast(AnyOptions, hashable_act_rando_options)
                            if act_rando == "insanity" and hashable_insanity_act_plando is not None:
                                # Add ActPlando to the options.
                                insanity_act_plando = dict(hashable_insanity_act_plando)
                                options_key |= hashable_insanity_act_plando
                                assert "ActPlando" not in act_rando_options
                                act_rando_options["ActPlando"] = insanity_act_plando

                            if options_key in options_key_to_options_tests_pairs:
                                _act_rando_options, spot_tests = options_key_to_options_tests_pairs[options_key]
                            else:
                                spot_tests = []
                                options_key_to_options_tests_pairs[options_key] = (act_rando_options, spot_tests)
                            spot_tests.append(SpotTest(test_spots, conditions))
                    else:
                        options_key = frozenset(options.items())
                        spot_tests = options_key_to_options_tests_pairs.setdefault(options_key, (options, []))[1]
                        spot_tests.append(SpotTest(test_spots, conditions))
        return options_key_to_options_tests_pairs.values()

    def test_spot_logic(self) -> None:
        tests_by_options = self.get_grouped_test_data()

        # Validate that all the supplied options exist and have valid values.
        self.validate_options(tests_by_options)

        for options, tests in tests_by_options:
            combined_options = logic_test_data.BASE_WORLD_OPTIONS.copy()
            combined_options.update(options)

            # Update the options that will be used when setting up the world.
            # super().world_setup() creates the world using self.options.
            self.options = combined_options
            self.world_setup()
            world = cast(HatInTimeWorld, self.world)

            with self.subTest(seed=self.multiworld.seed, test_options=options):
                for spot_test in tests:
                    conditions = spot_test.conditions
                    access_regions = conditions.access_regions
                    required_clearable_acts = conditions.required_clearable_acts
                    for spot_data in spot_test.spots:
                        spot = self.cached_spot_lookup(spot_data)
                        spot_type = spot_data.type
                        spot_identifier: Union[str, Dict[str, str]]
                        if spot_type == "RandomizedRegion":
                            spot_identifier = dict(original=spot_data.name, randomized=spot.name)
                        else:
                            spot_identifier = spot_data.name
                        spot_info = {spot_type: spot_identifier}
                        with self.subTest(clearable_acts=required_clearable_acts, **spot_info):
                            for access_region_list in access_regions:
                                if (spot_type == "RandomizedRegion"
                                        and world.options.ActRandomizer
                                        and spot.name in access_region_list):
                                    # Act rando placed a region, that we're intending to start with access to, at the
                                    # randomized region, giving immediate or partial access.
                                    # For example, when we want to test being able to go from "Welcome to Mafia Town" to
                                    # what has been randomized at the "Time Rift - Bazaar" entrance, but when
                                    # "Welcome to Mafia Town" is the act that has been randomized to that entrance.
                                    #
                                    # skipTest() within the subTest() skips the entire test with pytest, so just log
                                    # this and continue.
                                    logging.warning("Act randomization placed the entry point region '%s' at the"
                                                    " randomized act/rift '%s' being tested, so the subtest has been"
                                                    " skipped.", spot.name, spot_data.name)
                                    continue
                                with self.subTest(access_regions=access_region_list):
                                    if conditions.negative:
                                        collect_all_but_items = conditions.possible_items
                                        self.inaccessible_spot_test(spot, collect_all_but_items, access_region_list,
                                                                    required_clearable_acts)
                                    else:
                                        required_items = conditions.possible_items
                                        self.spot_test(spot, required_items, access_region_list,
                                                       required_clearable_acts)
