import itertools
import logging
import os
import threading
import typing
import unittest
from collections.abc import Iterable
from contextlib import contextmanager

from BaseClasses import get_seed, MultiWorld, Location, Item, Region, CollectionState, Entrance
from test.bases import WorldTestBase
from test.general import gen_steps, setup_solo_multiworld as setup_base_solo_multiworld
from worlds.AutoWorld import call_all
from .assertion import RuleAssertMixin
from .options.utils import parse_class_option_keys, fill_namespace_with_default
from .. import StardewValleyWorld, StardewItem, StardewRule
from ..logic.time_logic import MONTH_COEFFICIENT
from ..options import StardewValleyOption, options

logger = logging.getLogger(__name__)

DEFAULT_TEST_SEED = get_seed()
logger.info(f"Default Test Seed: {DEFAULT_TEST_SEED}")


def skip_default_tests() -> bool:
    return not bool(os.environ.get("base", False))


def skip_long_tests() -> bool:
    return not bool(os.environ.get("long", False))


class SVTestCase(unittest.TestCase):
    skip_default_tests: bool = skip_default_tests()
    """Set False to not skip the base fill tests"""
    skip_long_tests: bool = skip_long_tests()
    """Set False to run tests that take long"""

    @contextmanager
    def solo_world_sub_test(self, msg: str | None = None,
                            /,
                            world_options: dict[str | type[StardewValleyOption], typing.Any] | None = None,
                            *,
                            seed=DEFAULT_TEST_SEED,
                            world_caching=True,
                            **kwargs) -> Iterable[tuple[MultiWorld, StardewValleyWorld]]:
        if msg is not None:
            msg += " "
        else:
            msg = ""
        msg += f"[Seed = {seed}]"

        with self.subTest(msg, **kwargs):
            with solo_multiworld(world_options, seed=seed, world_caching=world_caching) as (multiworld, world):
                yield multiworld, world


class SVTestBase(RuleAssertMixin, WorldTestBase, SVTestCase):
    game = "Stardew Valley"
    world: StardewValleyWorld

    seed = DEFAULT_TEST_SEED

    @classmethod
    def setUpClass(cls) -> None:
        if cls is SVTestBase:
            raise unittest.SkipTest("No running tests on SVTestBase import.")

        super().setUpClass()

    def world_setup(self, *args, **kwargs):
        self.options = parse_class_option_keys(self.options)

        self.multiworld = setup_solo_multiworld(self.options, seed=self.seed)
        self.multiworld.lock.acquire()
        world = self.multiworld.worlds[self.player]

        self.original_state = self.multiworld.state.copy()
        self.original_itempool = self.multiworld.itempool.copy()
        self.unfilled_locations = self.multiworld.get_unfilled_locations(1)
        if self.constructed:
            self.world = world  # noqa

    def tearDown(self) -> None:
        self.multiworld.state = self.original_state
        self.multiworld.itempool = self.original_itempool
        for location in self.unfilled_locations:
            location.item = None

        self.multiworld.lock.release()

    @property
    def run_default_tests(self) -> bool:
        if self.skip_default_tests:
            return False
        return super().run_default_tests

    def collect_months(self, months: int) -> None:
        real_total_prog_items = self.world.total_progression_items
        percent = months * MONTH_COEFFICIENT
        self.collect("Stardrop", real_total_prog_items * 100 // percent)
        self.world.total_progression_items = real_total_prog_items

    def collect_lots_of_money(self, percent: float = 0.25):
        self.collect("Shipping Bin")
        real_total_prog_items = self.world.total_progression_items
        required_prog_items = int(round(real_total_prog_items * percent))
        self.collect("Stardrop", required_prog_items)

    def collect_all_the_money(self):
        self.collect_lots_of_money(0.95)

    def collect_everything(self):
        non_event_items = [item for item in self.multiworld.get_items() if item.code]
        for item in non_event_items:
            self.multiworld.state.collect(item)

    def collect_all_except(self, item_to_not_collect: str):
        non_event_items = [item for item in self.multiworld.get_items() if item.code]
        for item in non_event_items:
            if item.name != item_to_not_collect:
                self.multiworld.state.collect(item)

    def get_real_locations(self) -> list[Location]:
        return [location for location in self.multiworld.get_locations(self.player) if location.address is not None]

    def get_real_location_names(self) -> list[str]:
        return [location.name for location in self.get_real_locations()]

    def collect(self, item: str | Item | Iterable[Item], count: int = 1) -> Item | list[Item] | None:
        assert count > 0

        if not isinstance(item, str):
            return super().collect(item)

        if count == 1:
            item = self.create_item(item)
            self.multiworld.state.collect(item)
            return item

        items = []
        for i in range(count):
            item = self.create_item(item)
            self.multiworld.state.collect(item)
            items.append(item)

        return items

    def create_item(self, item: str) -> StardewItem:
        return self.world.create_item(item)

    def get_all_created_items(self) -> list[str]:
        return [item.name for item in itertools.chain(self.multiworld.get_items(), self.multiworld.precollected_items[self.player])]

    def remove_one_by_name(self, item: str) -> None:
        self.remove(self.create_item(item))

    def reset_collection_state(self) -> None:
        self.multiworld.state = self.original_state.copy()

    def assert_rule_true(self, rule: StardewRule, state: CollectionState | None = None) -> None:
        if state is None:
            state = self.multiworld.state
        return super().assert_rule_true(rule, state)

    def assert_rule_false(self, rule: StardewRule, state: CollectionState | None = None) -> None:
        if state is None:
            state = self.multiworld.state
        return super().assert_rule_false(rule, state)

    def assert_can_reach_location(self, location: Location | str, state: CollectionState | None = None) -> None:
        if state is None:
            state = self.multiworld.state
        return super().assert_can_reach_location(location, state)

    def assert_cannot_reach_location(self, location: Location | str, state: CollectionState | None = None) -> None:
        if state is None:
            state = self.multiworld.state
        return super().assert_cannot_reach_location(location, state)

    def assert_can_reach_region(self, region: Region | str, state: CollectionState | None = None) -> None:
        if state is None:
            state = self.multiworld.state
        return super().assert_can_reach_region(region, state)

    def assert_cannot_reach_region(self, region: Region | str, state: CollectionState | None = None) -> None:
        if state is None:
            state = self.multiworld.state
        return super().assert_cannot_reach_region(region, state)

    def assert_can_reach_entrance(self, entrance: Entrance | str, state: CollectionState | None = None) -> None:
        if state is None:
            state = self.multiworld.state
        return super().assert_can_reach_entrance(entrance, state)


pre_generated_worlds = {}


@contextmanager
def solo_multiworld(world_options: dict[str | type[StardewValleyOption], typing.Any] | None = None,
                    *,
                    seed=DEFAULT_TEST_SEED,
                    world_caching=True) -> Iterable[tuple[MultiWorld, StardewValleyWorld]]:
    if not world_caching:
        multiworld = setup_solo_multiworld(world_options, seed, _cache={})
        yield multiworld, typing.cast(StardewValleyWorld, multiworld.worlds[1])
    else:
        multiworld = setup_solo_multiworld(world_options, seed)
        try:
            multiworld.lock.acquire()
            original_state = multiworld.state.copy()
            original_itempool = multiworld.itempool.copy()
            unfilled_locations = multiworld.get_unfilled_locations(1)

            yield multiworld, typing.cast(StardewValleyWorld, multiworld.worlds[1])

            multiworld.state = original_state
            multiworld.itempool = original_itempool
            for location in unfilled_locations:
                location.item = None
        finally:
            multiworld.lock.release()


# Mostly a copy of test.general.setup_solo_multiworld, I just don't want to change the core.
def setup_solo_multiworld(test_options: dict[str | type[StardewValleyOption], str] | None = None,
                          seed=DEFAULT_TEST_SEED,
                          _cache: dict[frozenset, MultiWorld] = {},  # noqa
                          _steps=gen_steps) -> MultiWorld:
    test_options = parse_class_option_keys(test_options)

    # Yes I reuse the worlds generated between tests, its speeds the execution by a couple seconds
    # If the simple dict caching ends up taking too much memory, we could replace it with some kind of lru cache.
    should_cache = should_cache_world(test_options)
    if should_cache:
        frozen_options = make_hashable(test_options, seed)
        cached_multi_world = search_world_cache(_cache, frozen_options)
        if cached_multi_world:
            print(f"Using cached solo multi world [Seed = {cached_multi_world.seed}] [Cache size = {len(_cache)}]")
            return cached_multi_world

    multiworld = setup_base_solo_multiworld(StardewValleyWorld, (), seed=seed)
    # print(f"Seed: {multiworld.seed}") # Uncomment to print the seed for every test

    args = fill_namespace_with_default(test_options)
    multiworld.set_options(args)

    if "start_inventory" in test_options:
        for item, amount in test_options["start_inventory"].items():
            for _ in range(amount):
                multiworld.push_precollected(multiworld.create_item(item, 1))

    for step in _steps:
        call_all(multiworld, step)

    if should_cache:
        add_to_world_cache(_cache, frozen_options, multiworld)  # noqa

    # Lock is needed for multi-threading tests
    setattr(multiworld, "lock", threading.Lock())

    return multiworld


def should_cache_world(test_options):
    if "start_inventory" in test_options:
        return False

    trap_distribution_key = "trap_distribution"
    if trap_distribution_key not in test_options:
        return True

    trap_distribution = test_options[trap_distribution_key]
    for key in trap_distribution:
        if trap_distribution[key] != options.TrapDistribution.default_weight:
            return False

    return True


def make_hashable(test_options, seed):
    return frozenset(test_options.items()).union({("seed", seed)})


def search_world_cache(cache: dict[frozenset, MultiWorld], frozen_options: frozenset) -> MultiWorld | None:
    try:
        return cache[frozen_options]
    except KeyError:
        for cached_options, multi_world in cache.items():
            if frozen_options.issubset(cached_options):
                return multi_world
        return None


def add_to_world_cache(cache: dict[frozenset, MultiWorld], frozen_options: frozenset, multi_world: MultiWorld) -> None:
    # We could complete the key with all the default options, but that does not seem to improve performances.
    cache[frozen_options] = multi_world


def setup_multiworld(test_options: Iterable[dict[str, int]] | None = None, seed=None) -> MultiWorld:  # noqa
    if test_options is None:
        test_options = []

    multiworld = MultiWorld(len(test_options))
    multiworld.player_name = {}
    multiworld.set_seed(seed)
    for i in range(1, len(test_options) + 1):
        multiworld.game[i] = StardewValleyWorld.game
        multiworld.player_name.update({i: f"Tester{i}"})
    args = fill_namespace_with_default(test_options)
    multiworld.set_options(args)
    multiworld.state = CollectionState(multiworld)

    for step in gen_steps:
        call_all(multiworld, step)

    return multiworld
