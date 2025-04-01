import logging
import os
import threading
import unittest
from contextlib import contextmanager
from typing import Dict, ClassVar, Iterable, Tuple, Optional, List, Union, Any

from BaseClasses import MultiWorld, CollectionState, get_seed, Location, Item
from test.bases import WorldTestBase
from test.general import gen_steps, setup_solo_multiworld as setup_base_solo_multiworld
from worlds.AutoWorld import call_all
from .assertion import RuleAssertMixin
from .options.utils import fill_namespace_with_default, parse_class_option_keys, fill_dataclass_with_default
from .. import StardewValleyWorld, StardewItem
from ..options import StardewValleyOption

logger = logging.getLogger(__name__)

DEFAULT_TEST_SEED = get_seed()
logger.info(f"Default Test Seed: {DEFAULT_TEST_SEED}")


class SVTestCase(unittest.TestCase):
    # Set False to not skip some 'extra' tests
    skip_base_tests: bool = True
    # Set False to run tests that take long
    skip_long_tests: bool = True

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        base_tests_key = "base"
        if base_tests_key in os.environ:
            cls.skip_base_tests = not bool(os.environ[base_tests_key])
        long_tests_key = "long"
        if long_tests_key in os.environ:
            cls.skip_long_tests = not bool(os.environ[long_tests_key])

    @contextmanager
    def solo_world_sub_test(self, msg: Optional[str] = None,
                            /,
                            world_options: Optional[Dict[Union[str, StardewValleyOption], Any]] = None,
                            *,
                            seed=DEFAULT_TEST_SEED,
                            world_caching=True,
                            **kwargs) -> Tuple[MultiWorld, StardewValleyWorld]:
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
    player: ClassVar[int] = 1

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
        if self.skip_base_tests:
            return False
        return super().run_default_tests

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

    def get_real_locations(self) -> List[Location]:
        return [location for location in self.multiworld.get_locations(self.player) if location.address is not None]

    def get_real_location_names(self) -> List[str]:
        return [location.name for location in self.get_real_locations()]

    def collect(self, item: Union[str, Item, Iterable[Item]], count: int = 1) -> Union[None, Item, List[Item]]:
        assert count > 0

        if not isinstance(item, str):
            super().collect(item)
            return

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

    def remove_one_by_name(self, item: str) -> None:
        self.remove(self.create_item(item))

    def reset_collection_state(self):
        self.multiworld.state = self.original_state.copy()


pre_generated_worlds = {}


@contextmanager
def solo_multiworld(world_options: Optional[Dict[Union[str, StardewValleyOption], Any]] = None,
                    *,
                    seed=DEFAULT_TEST_SEED,
                    world_caching=True) -> Tuple[MultiWorld, StardewValleyWorld]:
    if not world_caching:
        multiworld = setup_solo_multiworld(world_options, seed, _cache={})
        yield multiworld, multiworld.worlds[1]
    else:
        multiworld = setup_solo_multiworld(world_options, seed)
        multiworld.lock.acquire()
        world = multiworld.worlds[1]

        original_state = multiworld.state.copy()
        original_itempool = multiworld.itempool.copy()
        unfilled_locations = multiworld.get_unfilled_locations(1)

        yield multiworld, world

        multiworld.state = original_state
        multiworld.itempool = original_itempool
        for location in unfilled_locations:
            location.item = None

        multiworld.lock.release()


# Mostly a copy of test.general.setup_solo_multiworld, I just don't want to change the core.
def setup_solo_multiworld(test_options: Optional[Dict[Union[str, StardewValleyOption], str]] = None,
                          seed=DEFAULT_TEST_SEED,
                          _cache: Dict[frozenset, MultiWorld] = {},  # noqa
                          _steps=gen_steps) -> MultiWorld:
    test_options = parse_class_option_keys(test_options)

    # Yes I reuse the worlds generated between tests, its speeds the execution by a couple seconds
    # If the simple dict caching ends up taking too much memory, we could replace it with some kind of lru cache. 
    should_cache = "start_inventory" not in test_options
    if should_cache:
        frozen_options = frozenset(test_options.items()).union({("seed", seed)})
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


def search_world_cache(cache: Dict[frozenset, MultiWorld], frozen_options: frozenset) -> Optional[MultiWorld]:
    try:
        return cache[frozen_options]
    except KeyError:
        for cached_options, multi_world in cache.items():
            if frozen_options.issubset(cached_options):
                return multi_world
        return None


def add_to_world_cache(cache: Dict[frozenset, MultiWorld], frozen_options: frozenset, multi_world: MultiWorld) -> None:
    # We could complete the key with all the default options, but that does not seem to improve performances.
    cache[frozen_options] = multi_world


def setup_multiworld(test_options: Iterable[Dict[str, int]] = None, seed=None) -> MultiWorld:  # noqa
    if test_options is None:
        test_options = []

    multiworld = MultiWorld(len(test_options))
    multiworld.player_name = {}
    multiworld.set_seed(seed)
    multiworld.state = CollectionState(multiworld)
    for i in range(1, len(test_options) + 1):
        multiworld.game[i] = StardewValleyWorld.game
        multiworld.player_name.update({i: f"Tester{i}"})
    args = fill_namespace_with_default(test_options)
    multiworld.set_options(args)

    for step in gen_steps:
        call_all(multiworld, step)

    return multiworld
