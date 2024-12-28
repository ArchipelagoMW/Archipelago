import random
from typing import TypedDict, ClassVar
from unittest import TestCase

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
    classification: ItemClassification


class SerializableLocationData(TypedDict):
    name: str
    address: int | None
    progress_type: LocationProgressType
    item: SerializableItemData | None


class SerializableEntranceData(TypedDict):
    name: str
    parent_region: str | None
    connected_region: str | None


class SerializableRegionData(TypedDict):
    name: str
    locations: list[str]


class SerializableMultiWorldData(TypedDict):
    item_pool: list[SerializableItemData]
    regions: dict[int, list[SerializableRegionData]]
    entrances: dict[int, list[SerializableEntranceData]]
    locations: dict[int, list[SerializableLocationData]]
    placements: dict[int, list[tuple[str, SerializableItemData | None]]]
    start_inventory: dict[int, list[SerializableItemData]]
    options: dict[int, list[dict[str, str]]]


DICTS_OF_LISTS = frozenset(("regions", "entrances", "locations", "placements", "start_inventory", "options"))
"""
Keys in SerializableMultiworldData which have values that are dicts containing list values.

These are compared one list at a time for better test output when a test fails.
"""


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


def location_to_serializable(loc: Location, item_memo: dict[int, SerializableItemData], include_item: bool = False
                             ) -> SerializableLocationData:
    item = loc.item
    if include_item and item is not None:
        item_data = item_to_serializable(item, item_memo)
    else:
        item_data = None

    # ALttP does not play by the rules and sets some location addresses to `list[int]` instead of `int | None`.
    address = loc.address
    if address is not None and type(address) is not int:
        address = None
    return {"name": loc.name, "address": address, "progress_type": loc.progress_type, "item": item_data}


def entrance_to_serializable(ent: Entrance) -> SerializableEntranceData:
    parent_region = ent.parent_region
    parent_region_name = parent_region.name if parent_region is not None else None
    connected_region = ent.connected_region
    connected_region_name = connected_region.name if connected_region is not None else None
    return {"name": ent.name, "parent_region": parent_region_name, "connected_region": connected_region_name}


def region_to_serializable(reg: Region) -> SerializableRegionData:
    return {"name": reg.name, "locations": [loc.name for loc in reg.locations]}


def options_to_serializable(multiworld: MultiWorld) -> dict[int, list[dict[str, str]]]:
    # Based on Options.dump_player_options.
    all_options = {}
    for player in multiworld.player_ids:
        output = []
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
        output.append(player_output)
        all_options[player] = output
    return all_options


def multiworld_to_serializable(item_pool_before_fill: list[Item], multiworld: MultiWorld) -> SerializableMultiWorldData:
    # Items that were in the item pool are expected to be placed at locations. The ItemData for these items is
    # deduplicated by tracking the created ItemData for each Item instance, by the Item instance's unique object
    # identifier. This is similar to using copy.deepcopy(obj, item_memo).
    item_memo: dict[int, SerializableItemData] = {}

    item_pool_before_main_fill = [item_to_serializable(item, item_memo) for item in item_pool_before_fill]

    # The order that regions and entrances are added to the multiworld is not considered important, so sort them by
    # name.
    regions = {player: sorted(map(region_to_serializable, regions.values()), key=lambda reg: reg["name"])
               for player, regions in multiworld.regions.region_cache.items()}
    entrances = {player: sorted(map(entrance_to_serializable, entrances.values()), key=lambda ent: ent["name"])
                 for player, entrances in multiworld.regions.entrance_cache.items()}

    # Locations and the placed items at those locations are tested and serialized separately.
    locations: dict[int, list[SerializableLocationData]] = {}
    placements: dict[int, list[tuple[str, SerializableItemData | None]]] = {}
    for player, player_locations in multiworld.regions.location_cache.items():
        locations_list = locations[player] = []

        placements_list = placements[player] = []

        for loc_name, loc in player_locations.items():
            locations_list.append(location_to_serializable(loc, item_memo))
            item = loc.item
            if item is not None:
                serializable_item = item_to_serializable(item, item_memo)
            else:
                serializable_item = None
            placements_list.append((loc_name, serializable_item))

    # Items that were in the item pool typically won't end up precollected_items, but it is possible, so `item_memo`
    # is still passed as an argument.
    precollected_items = {player: [item_to_serializable(item, item_memo) for item in items]
                          for player, items in multiworld.precollected_items.items()}

    return {
        "options": options_to_serializable(multiworld),
        "item_pool": item_pool_before_main_fill,
        "start_inventory": precollected_items,
        "regions": regions,
        "entrances": entrances,
        "locations": locations,
        "placements": placements,
    }


class TestDeterministicGeneration(TestCase):
    """
    Test that, for each world type, generating a multiworld with the same seed produces deterministic results.

    Common sources of nondeterministic behaviour that this test may be able to identify:
    - Iteration of sets
    - Accidental modification of shared data
    - Use of `random` module instead of per-world or per-multiworld `.random` attributes, or use of other
    nondeterministically seeded Random instances
    """

    initial_multiworld_data: ClassVar[dict[str, tuple[int, SerializableMultiWorldData]]] = {}

    @classmethod
    def tearDownClass(cls):
        # Allow the data to be garbage collected by clearing the dict.
        cls.initial_multiworld_data.clear()

    def get_initial_multiworld(self, game: str) -> tuple[int, SerializableMultiWorldData | None]:
        """
        Get the initial multiworld seed and serializable data for this game, or generate it if it does not exist.

        Each test method within this test class shares the same initial multiworld data for better test performance, by
        reducing the number of multiworlds that need to be generated.
        """
        if game in self.initial_multiworld_data:
            return self.initial_multiworld_data[game]

        world_type = AutoWorldRegister.world_types[game]
        multiworld = setup_multiworld(world_type, ())
        seed = multiworld.seed
        self.assertIsNotNone(seed)
        with self.subTest("initial multiworld setup", game=game, seed=seed):
            for step in gen_steps:
                call_all(multiworld, step)
            item_pool_copy = multiworld.itempool.copy()
            distribute_items_restrictive(multiworld)
            call_all(multiworld, "post_fill")
            serializable_data = multiworld_to_serializable(item_pool_copy, multiworld)
            to_return = (seed, serializable_data)
            self.initial_multiworld_data[game] = to_return
            return to_return
        # If the code in the self.subTest() context fails, execution continues after the end of the context, so this
        # return statement is reachable, despite PyCharm thinking it is unreachable.
        # noinspection PyUnreachableCode
        return multiworld.seed, None

    @staticmethod
    def _test_hash_determinism_world_setup(game: str, seed: int):
        """
        Called on a separate Python process to generate a multiworld and return the multiworld as serializable data.
        """
        world_type = worlds.AutoWorldRegister.world_types[game]
        multiworld = setup_multiworld(world_type, seed=seed)
        item_pool_copy = multiworld.itempool.copy()
        distribute_items_restrictive(multiworld)
        call_all(multiworld, "post_fill")
        return multiworld_to_serializable(item_pool_copy, multiworld)

    @staticmethod
    def _hash_check():
        """Called by both the main Python process and a separate Python process to check that the hashseeds differ."""
        # Note: hashing an integer returns that integer if it's not too large, so a string literal is hashed instead
        # because str objects are "salted" with an unpredictable random value that remains constant within an individual
        # Python process.
        return hash("This string is hashed to check that one process' hashseed differs from another")

    def assertMultiWorldsEquivalent(self, m1: SerializableMultiWorldData, m2: SerializableMultiWorldData):
        for key, data_current in m1.items():
            # PyCharm sees `key` as str, rather than one of the valid string literals, so disable the inspection.
            # noinspection PyTypedDict
            data_other = m2[key]
            with self.subTest(key):
                # Iterate dictionaries with list values because comparing lists for equality produces better output than
                # comparing dictionaries for equality when the test fails and was run using unittest.
                if key in DICTS_OF_LISTS:
                    self.assertEqual(data_current.keys(), data_other.keys())
                    for k_current, v_current in data_current.items():
                        v_other = data_other[k_current]
                        self.assertEqual(v_current, v_other)
                else:
                    self.assertEqual(data_current, data_other)

    def test_hash_determinism(self) -> None:
        """
        For security purposes, Python randomizes its hash seed when starting a Python process. This notably changes the
        order of elements in a set due to changing the hashes of the elements.

        For Archipelago, this means that iterating sets can be a common source of nondeterministic generation.

        To effectively test for nondeterministic generation caused by iterating sets, multiworlds with the same seed
        need to be generated with different Python hash seeds, which requires separate Python processes.
        """
        from concurrent.futures import ProcessPoolExecutor, Future
        import multiprocessing

        hash_check = TestDeterministicGeneration._hash_check()

        # ProcessPoolExecutor is used so that we don't have to mess around with setting up communication between the new
        # process as well as exception handling and more.
        # The new process must be spawned so that the new process gets a different hashseed, resulting in different
        # ordering within `set` objects.
        with ProcessPoolExecutor(max_workers=1, mp_context=multiprocessing.get_context("spawn")) as ppe:
            # Starting up the process takes a while (6 or more seconds), so give it a generous timeout.
            # This opportunity is also used to check that the new process (most likely) has a different hashseed set.
            other_hash = ppe.submit(TestDeterministicGeneration._hash_check).result(timeout=20.0)
            if other_hash == hash_check:
                self.skipTest("Different hashes should be produced by the current  process and the spawned process, but"
                              " they were the same. It is technically possible for both processes to produce the same"
                              " hash, but this should not realistically occur.")

            # The secondary process is running and has a different hashseed, so proceed with the test.
            for game, world_type in AutoWorldRegister.world_types.items():
                seed, initial_multiworld_data = self.get_initial_multiworld(game)
                if initial_multiworld_data is None:
                    continue
                with self.subTest(game=world_type.game, seed=seed):
                    future: Future = ppe.submit(TestDeterministicGeneration._test_hash_determinism_world_setup,
                                                game, seed)
                    data_from_other_process = future.result(timeout=10.0)
                    self.assertMultiWorldsEquivalent(initial_multiworld_data, data_from_other_process)

    def test_shared_state_determinism(self) -> None:
        """
        Many worlds have constant, shared data used to create locations/regions/etc. and to set up logic that should not
        be modified across multiple generations.
        """
        for game, world_type in AutoWorldRegister.world_types.items():
            seed, initial_multiworld_data = self.get_initial_multiworld(game)
            if initial_multiworld_data is None:
                continue
            with self.subTest(game=game, seed=seed):
                # Generate an extra multiworld with a random seed to increase the likelihood that if constant, shared
                # data is being modified, that the data is modified in a way that alters subsequent generation. For
                # better performance, only the generation steps prior to `distribute_items_restrictive` are used.
                _extra_multiworld = setup_multiworld(world_type)

                multiworld2 = setup_multiworld(world_type, seed=seed)
                item_pool_copy2 = multiworld2.itempool.copy()
                distribute_items_restrictive(multiworld2)
                call_all(multiworld2, "post_fill")

                data2 = multiworld_to_serializable(item_pool_copy2, multiworld2)
                self.assertMultiWorldsEquivalent(initial_multiworld_data, data2)

    def test_random_module_usage_determinism(self) -> None:
        """
        Usage of the `random` module directly within worlds is unsafe because its Random instance can be used by
        libraries and more in nondeterministic ways. Worlds should use their own Random instance, either `.random` or
        `.multiworld.random`, instead. Alternatively, to work with libraries that perform randomization, worlds should
        pass a deterministic seed to the libraries or pass a new Random instance using a deterministic seed.

        It may be possible for worlds to call `random.seed(deterministic_seed)` before running library functions, but
        this should be considered a last resort.
        """
        generation_steps = gen_steps
        for game, world_type in AutoWorldRegister.world_types.items():
            seed, initial_multiworld_data = self.get_initial_multiworld(game)
            if initial_multiworld_data is None:
                continue
            with self.subTest(game=game, seed=seed):
                # Set up the second world with the same seed, but increment the `random` module's RNG before calling any
                # of the generation steps.
                multiworld2 = setup_multiworld(world_type, (), seed=seed)
                # Set the `random` module to a different seed.
                # This should have no effect on generation because worlds should not be using the `random` module
                # directly, or at the very least should be setting its seed themselves before using it.
                random.seed(random.random())
                # Call the same generation steps as normal.
                for step in generation_steps:
                    call_all(multiworld2, step)

                item_pool_copy2 = multiworld2.itempool.copy()
                distribute_items_restrictive(multiworld2)
                call_all(multiworld2, "post_fill")

                data2 = multiworld_to_serializable(item_pool_copy2, multiworld2)
                self.assertMultiWorldsEquivalent(initial_multiworld_data, data2)
