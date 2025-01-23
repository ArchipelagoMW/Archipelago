from operator import itemgetter
import random
from typing import TypedDict, ClassVar, Callable, Any
from unittest import TestCase

# Imported before importing from Fill to prevent circular imports in spawned processes, when run as part of the full
# test suite.
import worlds

from BaseClasses import Location, MultiWorld, Item, Entrance, Region, ItemClassification, LocationProgressType
from Fill import distribute_items_restrictive
from Options import Removed
from worlds.AutoWorld import AutoWorldRegister, call_all

from ..general import setup_multiworld, gen_steps


# TypedDicts for passing generated multiworld data between processes and for comparing generation output.
# At runtime, TypedDict is equivalent to a plain dict, so it is efficient to transfer between processes.
class SerializableItemData(TypedDict):
    name: str
    player: int
    code: int | None
    # classification could be stored as an int instead, but for the simplicity of providing better test output, it is
    # left as an ItemClassification.
    classification: ItemClassification


class SerializableLocationData(TypedDict):
    address: int | None
    # progress_type could be stored as an int instead, but for the simplicity of providing better test output, it is
    # left as a LocationProgressType.
    progress_type: LocationProgressType
    item: SerializableItemData | None


class SerializableEntranceData(TypedDict):
    parent_region: str | None
    connected_region: str | None


class SerializableRegionData(TypedDict):
    # While often the same, locations can be added to regions in an order independent of the order the locations were
    # created.
    locations: list[str]


class SerializableMultiWorldData(TypedDict):
    itempool: list[SerializableItemData]
    regions: dict[int, dict[str, SerializableRegionData]]
    entrances: dict[int, dict[str, SerializableEntranceData]]
    locations: dict[int, dict[str, SerializableLocationData]]
    start_inventory: dict[int, list[SerializableItemData]]
    options: dict[int, dict[str, str]]


def item_to_serializable(item: Item, item_memo: dict[int, SerializableItemData]) -> SerializableItemData:
    object_id = id(item)
    if object_id in item_memo:
        return item_memo[object_id]
    else:
        to_return: SerializableItemData = {
            "name": item.name,
            "player": item.player,
            "code": item.code,
            "classification": item.classification
        }
        item_memo[object_id] = to_return
        return to_return


def location_to_serializable(loc: Location, item_memo: dict[int, SerializableItemData]) -> SerializableLocationData:
    # ALttP does not play by the rules and sets some location addresses to `list[int]` instead of `int | None`.
    address = loc.address
    if address is not None and type(address) is not int:
        address = None

    if loc.item is None:
        item = None
    else:
        item = item_to_serializable(loc.item, item_memo)
    return {"address": address, "progress_type": loc.progress_type, "item": item}


def entrance_to_serializable(ent: Entrance) -> SerializableEntranceData:
    parent_region = ent.parent_region
    parent_region_name = parent_region.name if parent_region is not None else None
    connected_region = ent.connected_region
    connected_region_name = connected_region.name if connected_region is not None else None
    return {"parent_region": parent_region_name, "connected_region": connected_region_name}


def region_to_serializable(reg: Region) -> SerializableRegionData:
    return {"locations": [loc.name for loc in reg.locations]}


def options_to_serializable(multiworld: MultiWorld) -> dict[int, dict[str, str]]:
    # Based on Options.dump_player_options.
    all_options = {}
    for player in multiworld.player_ids:
        world = multiworld.worlds[player]
        player_output = {
            "Game": multiworld.game[player],
            "Name": multiworld.get_player_name(player),
        }
        for option_key, option in world.options_dataclass.type_hints.items():
            if issubclass(Removed, option):
                continue
            display_name = getattr(option, "display_name", option_key)
            player_output[display_name] = getattr(world.options, option_key).current_option_name
        all_options[player] = player_output
    return all_options


def multiworld_to_serializable(itempool_before_fill: list[Item], multiworld: MultiWorld) -> SerializableMultiWorldData:
    # Items that were in the item pool are expected to be placed at locations. The ItemData for these items is
    # deduplicated by tracking the created ItemData for each Item instance, by the Item instance's unique object
    # identifier. This is similar to using copy.deepcopy(obj, item_memo).
    item_memo: dict[int, SerializableItemData] = {}

    itempool = [item_to_serializable(item, item_memo) for item in itempool_before_fill]

    # The order that regions and entrances are added to the multiworld is not considered important, so are returned as
    # dictionaries.
    regions = {player: {region.name: region_to_serializable(region) for region in regions.values()}
               for player, regions in multiworld.regions.region_cache.items()}
    entrances = {player: {entrance.name: entrance_to_serializable(entrance) for entrance in entrances.values()}
                 for player, entrances in multiworld.regions.entrance_cache.items()}

    # Locations and the placed items at those locations are tested and serialized separately.
    locations = {player: {loc.name: location_to_serializable(loc, item_memo) for loc in locations.values()}
                 for player, locations in multiworld.regions.location_cache.items()}

    # Items that were in the item pool typically won't end up precollected_items, but it is possible, so `item_memo`
    # is still passed as an argument.
    precollected_items = {player: [item_to_serializable(item, item_memo) for item in items]
                          for player, items in multiworld.precollected_items.items()}

    return {
        "itempool": itempool,
        "regions": regions,
        "entrances": entrances,
        "locations": locations,
        "start_inventory": precollected_items,
        "options": options_to_serializable(multiworld),
    }


class TestDeterministicGeneration(TestCase):
    """
    Test that, for each world type, generating a multiworld is deterministic, so generating with the same seed multiple
    times produces the same result each time.

    Common sources of nondeterministic behaviour that these tests may be able to identify:
    - Iteration of sets
    - Accidental modification of shared data
    - Use of `random` module, instead of per-world or per-multiworld `.random` attributes or other deterministically
    seeded Random instances

    The tests check the following:
    - Rolled options
    - Item code and classification, and the order of the items in the item pool and start inventory (precollected items)
    - Location address and progress_type, and the order of the locations in the multiworld
    - Locations within each Region and the order of those locations
    - The parent and connected region of each Entrance
    - The placement of items after post_fill
    """

    initial_multiworld_data_cache: ClassVar[dict[str, tuple[int, SerializableMultiWorldData]]] = {}
    """
    To reduce test duration, the initial multiworld for each test is generated only once and then shared between the
    tests.
    """

    @classmethod
    def tearDownClass(cls):
        # Allow the data to be garbage collected by clearing the dict.
        cls.initial_multiworld_data_cache.clear()
        super().tearDownClass()

    def get_initial_multiworld(self, game: str) -> tuple[int, SerializableMultiWorldData] | tuple[int, None]:
        """
        Get the initial multiworld seed and multiworld as serializable data for this game, or generate it and cache it
        if it does not exist.

        Each test method within this test class shares the same initial multiworld data for better test performance, by
        reducing the number of multiworlds that need to be generated.

        If world setup fails, the returned SerializableMultiWorldData will be None and a subtest will be recorded as
        having failed along with the reason.
        """
        if game in self.initial_multiworld_data_cache:
            # The initial multiworld for this game has already been generated.
            return self.initial_multiworld_data_cache[game]

        world_type = AutoWorldRegister.world_types[game]
        # Generate without calling any generation steps to start with so that the seed can be retrieved first.
        multiworld = setup_multiworld(world_type, ())
        seed = multiworld.seed
        self.assertIsNotNone(seed)
        with self.subTest("initial multiworld setup", game=game, seed=seed):
            for step in gen_steps:
                call_all(multiworld, step)
            itempool_copy = multiworld.itempool.copy()
            distribute_items_restrictive(multiworld)
            call_all(multiworld, "post_fill")
            serializable_data = multiworld_to_serializable(itempool_copy, multiworld)
            to_return = (seed, serializable_data)
            self.initial_multiworld_data_cache[game] = to_return
            return to_return
        # If the code in the self.subTest() context fails, execution continues after the end of the context, so this
        # return statement is reachable, despite PyCharm thinking it is unreachable.
        # noinspection PyUnreachableCode
        return multiworld.seed, None

    @staticmethod
    def _new_multiworld_to_serializable_data(game: str, seed: int):
        """
        Generate a multiworld for the given game and seed and return the multiworld as serializable data.

        May be called on a separate Python process.
        """
        if game not in worlds.AutoWorldRegister.world_types:
            raise RuntimeError(f"No world loaded for game '{game}'. Failed world loads: {worlds.failed_world_loads}")
        world_type = worlds.AutoWorldRegister.world_types[game]
        multiworld = setup_multiworld(world_type, gen_steps, seed=seed)
        itempool_copy = multiworld.itempool.copy()
        distribute_items_restrictive(multiworld)
        call_all(multiworld, "post_fill")
        return multiworld_to_serializable(itempool_copy, multiworld)

    @staticmethod
    def _hash_check():
        """Called by both the main Python process and a separate Python process to check that the hash seeds differ."""
        # Note: hashing an integer returns that integer if it's not too large, so a string literal is hashed instead
        # because str objects are "salted" with an unpredictable random value that remains constant within an individual
        # Python process.
        return hash("This string is hashed to check that one process' hash seed differs from another")

    def assertDictEqualDiffMismatchedOnly(self, d1, d2, msg=None):
        """
        assertDictEqual's output on failure is not very readable for large dictionaries because it makes a diff of the
        entire dictionaries, rather than only the differences.

        If the dictionaries are not equal, this method fails like assertDictEqual, or assertEqual with dict arguments,
        but outputs only a diff of the mismatching items.
        """
        self.assertIsInstance(d1, dict, msg)
        self.assertIsInstance(d2, dict, msg)
        if d1 == d2:
            return
        # Produce copies of the dictionaries with equal items removed.
        d1_mismatched = d1.copy()
        d2_mismatched = d2.copy()
        for k, v1 in d1.items():
            if k in d2:
                v2 = d2[k]
                if v1 == v2:
                    del d1_mismatched[k]
                    del d2_mismatched[k]
        # This should always fail. assertEquals is used for better output by getting a diff over only the keys that have
        # mismatched values rather than the entire dictionaries.
        self.assertEqual(d1_mismatched, d2_mismatched, msg)
        self.fail("Dictionaries were not equal, but they somehow had all the same keys and values."
                  + "" if msg is None else f" : {msg}")

    def assertDictKeysEqual(self, d1: dict, d2: dict, msg=None):
        # Provides better failure output than comparing dict keys directly.
        self.assertEqual(set(d1.keys()), set(d2.keys()), msg)

    def assertRegionsEqual(self, r1: dict[str, SerializableRegionData], r2: dict[str, SerializableRegionData]):
        self.assertDictKeysEqual(r1, r2, "The were different regions in each multiworld")
        regions_with_locations_out_of_order = []
        for name, r1_data in r1.items():
            r1_locations = r1_data["locations"]
            r2_locations = r2[name]["locations"]
            self.assertEqual(set(r1_locations), set(r2_locations),
                             f"The locations in region '{name}' were not the same")
            if r1_locations != r2_locations:
                regions_with_locations_out_of_order.append(name)

        # Getting to here means all regions have the same content, but possibly in a different order.

        if regions_with_locations_out_of_order:
            # We still want to know if the regions themselves are in the same order after this, so run within a subTest.
            with self.subTest("region .locations order"):
                self.assertEqual([], regions_with_locations_out_of_order,
                                 "The locations in all regions were the same, but in different orders for some"
                                 " regions.")
            order_fail_message = ("Regions were the same, but in different orders and with locations in different"
                                  " orders")
        else:
            order_fail_message = "Regions were the same, but in different orders"
        self.assertEqual(tuple(r1.keys()), tuple(r2.keys()), order_fail_message)

    def assertLocationsEqual(self, l1: dict[str, SerializableLocationData], l2: dict[str, SerializableLocationData]):
        self.assertDictKeysEqual(l1, l2, "The were different locations in each multiworld")

        # Compare only "address" and "progress_type" to start with because they are much less likely to differ.
        fields = ("address", "progress_type")
        getter = itemgetter(*fields)
        l1_filtered = {k: dict(zip(fields, getter(v))) for k, v in l1.items()}
        l2_filtered = {k: dict(zip(fields, getter(v))) for k, v in l2.items()}
        self.assertDictEqualDiffMismatchedOnly(l1_filtered, l2_filtered, "The locations in the multiworld")

        # Even if the locations are in different orders, it is common for the placements to end up the same anyway.
        sorted_placements1 = []
        sorted_placements2 = []
        for name in sorted(l1.keys()):
            sorted_placements1.append({name: l1[name]["item"]})
            sorted_placements2.append({name: l2[name]["item"]})
        self.assertEqual(sorted_placements1, sorted_placements2, "Placed items did not match")

        self.assertEqual(tuple(l1.keys()), tuple(l2.keys()),
                         "Locations and the items placed at them were the same, but in different orders")

    def assertEntrancesEqual(self, e1: dict[str, SerializableEntranceData], e2: dict[str, SerializableEntranceData]):
        self.assertDictKeysEqual(e1, e2, "There were different entrances in each multiworld")
        # Entrances are unlikely to have a different parent_region or connected_region, so check each entrance one
        # at a time.
        self.assertDictEqualDiffMismatchedOnly(e1, e2, "Entrances were not the same")
        self.assertEqual(tuple(e1.keys()), tuple(e2.keys()), "Entrances were the same, but in different orders")

    def assertItemsEqual(self, i1: list[SerializableItemData], i2: list[SerializableItemData]):
        self.assertCountEqual(i1, i2, "Item counts did not match")
        self.assertEqual(i1, i2, "Items were the same, but in different orders")

    def assertOptionsEqual(self, o1: dict[str, str], o2: dict[str, str]):
        self.assertDictEqualDiffMismatchedOnly(o1, o2, "Options did not match")

    def assertMultiWorldsEqual(self, m1: SerializableMultiWorldData, m2: SerializableMultiWorldData):
        # Options are checked first because differences in rolled options are likely to affect the rest of generation.
        # Locations are checked last because the items placed at them are likely to be affected by all previously
        # checked parts.
        key_to_assert_func: dict[str, Callable[[Any, Any], None] | None] = {
            "options": self.assertOptionsEqual,
            "itempool": None,
            "start_inventory": self.assertItemsEqual,
            "regions": self.assertRegionsEqual,
            "entrances": self.assertEntrancesEqual,
            "locations": self.assertLocationsEqual,
        }
        for key, assert_func in key_to_assert_func.items():
            # Type checkers see `key` as str, rather than one of the valid string literals, so disable the inspection.
            data1 = m1[key]  # type: ignore
            data2 = m2[key]  # type: ignore
            # Iterate dictionaries with list values because comparing lists for equality produces better output than
            # comparing dictionaries for equality when the test fails.
            if key == "itempool":
                with self.subTest(key):
                    self.assertItemsEqual(data1, data2)
            else:
                # All other serializable data should be dicts keyed by player ID.
                self.assertIsInstance(data1, dict)
                self.assertIsInstance(data2, dict)
                self.assertEqual(data1.keys(), data2.keys(), "The multiworlds have a different number of players")
                if assert_func is not None:
                    with self.subTest(key):
                        for player, v1 in data1.items():
                            with self.subTest(key, player=player):
                                v2 = data2[player]
                                assert_func(v1, v2)
                else:
                    self.fail(f"No assertion function found to handle key: '{key}'")

    def test_hash_determinism(self) -> None:
        """
        Test that generation is deterministic across multiple Python processes.

        For security purposes, Python randomizes its hash seed when starting a Python process. This notably changes the
        order of elements in a set due to changing the hashes of the elements.

        For Archipelago, this means that iterating sets can be a common source of nondeterministic generation.

        To effectively test for nondeterministic generation caused by iterating sets, multiworlds with the same seed
        need to be generated with different Python hash seeds, which requires separate Python processes.

        Because the separate Python process loads all the modules anew, this test can also identify issues where
        previously run test generations from across the entire test suite have accidentally modified shared state that
        should remain constant. The separate Python process won't have any of these accidental modifications, which can
        produce different results with the same seed and fail the test.
        """
        # These imports are not required for the spawned process and might not be needed by worlds, so are imported
        # inside this method.
        from concurrent.futures import ProcessPoolExecutor, Future
        import multiprocessing

        current_hash_result = TestDeterministicGeneration._hash_check()

        # ProcessPoolExecutor is used so that we don't have to mess around with setting up communication between the new
        # process as well as exception handling and more.
        # The new process must be spawned so that the new process gets a different hash seed, resulting in different
        # ordering within `set` objects.
        with ProcessPoolExecutor(max_workers=1, mp_context=multiprocessing.get_context("spawn")) as executor:
            # Starting up the process can take a while (6 or more seconds), so give it a generous timeout.
            # This opportunity is also used to check that the new process (most likely) has a different hash seed set.
            other_process_hash_result = executor.submit(TestDeterministicGeneration._hash_check).result(timeout=20.0)
            if other_process_hash_result == current_hash_result:
                self.skipTest("Different hashes should be produced by the current process and the spawned process, but"
                              " they were the same. It is technically possible for both processes to produce the same"
                              " hash, but this should not realistically occur.")

            # The secondary process is running and has a different hash seed, so proceed with the test.
            for game, world_type in AutoWorldRegister.world_types.items():
                seed, initial_multiworld_data = self.get_initial_multiworld(game)
                if initial_multiworld_data is None:
                    continue
                with self.subTest(game=world_type.game, seed=seed):
                    future: Future[SerializableMultiWorldData]
                    # Tell the other process to generate the same seed as the initial multiworld.
                    future = executor.submit(TestDeterministicGeneration._new_multiworld_to_serializable_data, game,
                                             seed)
                    # Most solo multiworlds will generate in less than a second, though larger and more complex worlds
                    # can often take 2-3 seconds. Getting a seed that has to perform lots of swaps during progression
                    # fill can take even longer, so 10 seconds should be an ample timeout for even the worst solo
                    # generations.
                    data_from_other_process = future.result(timeout=10.0)
                    self.assertMultiWorldsEqual(initial_multiworld_data, data_from_other_process)

    def test_shared_state_determinism(self) -> None:
        """
        Test that generation is deterministic across multiple generations on the same process.

        Many worlds have constant, shared data used to create locations/regions/etc. and to set up logic that should not
        be modified across multiple generations.

        This test generates a different seed in-between two generations of the same seed and ensures that the two
        generations of the same seed produced identical results.
        """
        for game, world_type in AutoWorldRegister.world_types.items():
            seed, initial_multiworld_data = self.get_initial_multiworld(game)
            if initial_multiworld_data is None:
                continue
            with self.subTest(game=game, seed=seed):
                # If there is an issue related to mistakenly modifying constant data, and if that constant data uses
                # sets or dictionaries, then generating the same seed twice has an increased likelihood of no changes
                # being made by the second generation because any modifications should be the same as the first
                # generation.
                # To increase the likelihood of constant data being changed in a way that alters the second generation,
                # an extra multiworld is generated with a random seed before the second generation of the original seed.
                # For better performance, only the generation steps prior to `distribute_items_restrictive` are used.
                setup_multiworld(world_type, gen_steps)

                secondary_multiworld_data = TestDeterministicGeneration._new_multiworld_to_serializable_data(game, seed)
                self.assertMultiWorldsEqual(initial_multiworld_data, secondary_multiworld_data)

    def test_random_module_usage_determinism(self) -> None:
        """
        Test that generation is likely to produce the same output on webhost, specifically that it does not use the
        `random` module directly.

        Usage of the `random` module directly within worlds is unsafe because its Random instance can be used by
        libraries and more in nondeterministic ways. Worlds should use their own Random instance, either `.random` or
        `.multiworld.random`, instead. Alternatively, to work with libraries that perform randomization, worlds should
        pass a deterministic seed to the libraries or pass a new Random instance using a deterministic seed.

        It may be possible for worlds to call `random.seed(deterministic_seed)` before running library functions, but
        this should be considered a last resort.

        Failing this test means that a world will generate differently on webhost (archipelago.gg and other hosts of the
        website generator) compared to local generation.
        """
        for game, world_type in AutoWorldRegister.world_types.items():
            seed, initial_multiworld_data = self.get_initial_multiworld(game)
            if initial_multiworld_data is None:
                continue
            with self.subTest(game=game, seed=seed):
                # Set up the second world with the same seed, but without calling any of the generation steps.
                multiworld = setup_multiworld(world_type, (), seed=seed)

                # Set the `random` module to a different seed.
                # This should have no effect on generation because worlds should not be using the `random` module
                # directly, or at the very least should be setting its seed themselves before using it.
                random.seed(random.random())

                # Call the same generation steps as normal.
                for step in gen_steps:
                    call_all(multiworld, step)

                itempool_copy = multiworld.itempool.copy()
                distribute_items_restrictive(multiworld)
                call_all(multiworld, "post_fill")

                secondary_multiworld_data = multiworld_to_serializable(itempool_copy, multiworld)
                self.assertMultiWorldsEqual(initial_multiworld_data, secondary_multiworld_data)
