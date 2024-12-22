import unittest
from typing import List, Tuple, TypedDict
from unittest import TestCase

import worlds
from BaseClasses import (
    CollectionState, Location, MultiWorld, Item, Entrance, Region, ItemClassification, LocationProgressType,
)
from Fill import distribute_items_restrictive
from Options import Accessibility
from worlds.AutoWorld import AutoWorldRegister, call_all, call_single
from ..general import gen_steps, setup_multiworld


class MultiworldTestBase(TestCase):
    multiworld: MultiWorld

    # similar to the implementation in WorldTestBase.test_fill
    # but for multiple players and doesn't allow minimal accessibility
    def fulfills_accessibility(self) -> bool:
        """
        Checks that the multiworld satisfies locations accessibility requirements, failing if all locations are cleared
        but not beatable, or some locations are unreachable.
        """
        locations = [loc for loc in self.multiworld.get_locations()]
        state = CollectionState(self.multiworld)
        while locations:
            sphere: List[Location] = []
            for n in range(len(locations) - 1, -1, -1):
                if locations[n].can_reach(state):
                    sphere.append(locations.pop(n))
            self.assertTrue(sphere, f"Unreachable locations: {locations}")
            if not sphere:
                return False
            for location in sphere:
                if location.item:
                    state.collect(location.item, True, location)
        return self.multiworld.has_beaten_game(state, 1)

    def assertSteps(self, steps: Tuple[str, ...]) -> None:
        """Calls each step individually, continuing if a step for a specific world step fails."""
        world_types = {world.__class__ for world in self.multiworld.worlds.values()}
        for step in steps:
            for player, world in self.multiworld.worlds.items():
                with self.subTest(game=world.game, step=step):
                    call_single(self.multiworld, step, player)
            for world_type in sorted(world_types, key=lambda world: world.__name__):
                with self.subTest(game=world_type.game, step=f"stage_{step}"):
                    stage_callable = getattr(world_type, f"stage_{step}", None)
                    if stage_callable:
                        stage_callable(self.multiworld)


@unittest.skip("too slow for main")
class TestAllGamesMultiworld(MultiworldTestBase):
    def test_fills(self) -> None:
        """Tests that a multiworld with one of every registered game world can generate."""
        all_worlds = list(AutoWorldRegister.world_types.values())
        self.multiworld = setup_multiworld(all_worlds, ())
        for world in self.multiworld.worlds.values():
            world.options.accessibility.value = Accessibility.option_full
        self.assertSteps(gen_steps)
        with self.subTest("filling multiworld", seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
            self.assertTrue(self.fulfills_accessibility(), "Collected all locations, but can't beat the game")


class TestTwoPlayerMulti(MultiworldTestBase):
    def test_two_player_single_game_fills(self) -> None:
        """Tests that a multiworld of two players for each registered game world can generate."""
        for world_type in AutoWorldRegister.world_types.values():
            self.multiworld = setup_multiworld([world_type, world_type], ())
            for world in self.multiworld.worlds.values():
                world.options.accessibility.value = Accessibility.option_full
            self.assertSteps(gen_steps)
            with self.subTest("filling multiworld", games=world_type.game, seed=self.multiworld.seed):
                distribute_items_restrictive(self.multiworld)
                call_all(self.multiworld, "post_fill")
                self.assertTrue(self.fulfills_accessibility(), "Collected all locations, but can't beat the game")


# TypedDicts for passing generated multiworld data between processes
class ItemData(TypedDict):
    name: str
    player: int
    code: int | None
    classification: ItemClassification


class LocationData(TypedDict):
    name: str
    address: int | None
    progress_type: LocationProgressType
    item: ItemData | None


class EntranceData(TypedDict):
    name: str
    parent_region: str | None
    connected_region: str | None


class RegionData(TypedDict):
    name: str
    locations: list[str]


class TestDeterministicGeneration(MultiworldTestBase):
    @staticmethod
    def _test_determinism_multiworld_to_basic_data(multiworld: MultiWorld) -> tuple[
        dict[int, list[RegionData]], dict[int, list[EntranceData]], dict[int, list[LocationData]], dict[int, list[ItemData]]
    ]:
        def item_to_basic_data(item: Item) -> ItemData:
            return {"name": item.name, "player": item.player, "code": item.code, "classification": item.classification}

        def location_to_basic_data(loc: Location) -> LocationData:
            item = loc.item
            if item is not None:
                item_data = item_to_basic_data(item)
            else:
                item_data = None

            # ALttP does not play by the rules and sets some location addresses to `list[int]` instead of `int | None`.
            address = loc.address
            if address is not None and type(address) is not int:
                address = None
            return {"name": loc.name, "address": address, "progress_type": loc.progress_type, "item": item_data}

        def entrance_to_basic_data(ent: Entrance) -> EntranceData:
            parent_region = ent.parent_region
            parent_region_name = parent_region.name if parent_region is not None else None
            connected_region = ent.connected_region
            connected_region_name = connected_region.name if connected_region is not None else None
            return {"name": ent.name, "parent_region": parent_region_name, "connected_region": connected_region_name}

        def region_to_basic_data(reg: Region) -> RegionData:
            return {"name": reg.name, "locations": [loc.name for loc in reg.locations]}

        regions = {player: list(map(region_to_basic_data, regions.values()))
                   for player, regions in multiworld.regions.region_cache.items()}
        entrances = {player: list(map(entrance_to_basic_data, entrances.values()))
                     for player, entrances in multiworld.regions.entrance_cache.items()}
        locations = {player: list(map(location_to_basic_data, locations.values()))
                     for player, locations in multiworld.regions.location_cache.items()}
        precollected_items = {player: list(map(item_to_basic_data, items))
                              for player, items in multiworld.precollected_items.items()}

        return regions, entrances, locations, precollected_items

    @staticmethod
    def _test_determinism_world_setup(world_type_name: str, seed: int):
        world_type = worlds.AutoWorldRegister.world_types[world_type_name]
        multiworld = setup_multiworld(world_type, seed=seed)
        distribute_items_restrictive(multiworld)
        call_all(multiworld, "post_fill")
        return TestDeterministicGeneration._test_determinism_multiworld_to_basic_data(multiworld)

    @staticmethod
    def _hash_check():
        return hash("hash check")

    def test_determinism(self) -> None:
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
            # if other_hash == hash_check:
            #     self.skipTest("spawned process produced the same hash as the current process")
            self.assertNotEqual(other_hash, hash_check, "Different hashes should be produced by the current"
                                                        " process and the spawned process, but they were the same")
            for world_type_name, world_type in AutoWorldRegister.world_types.items():
                self.multiworld = setup_multiworld(world_type)
                with self.subTest(game=world_type.game, seed=self.multiworld.seed):
                    future: Future = ppe.submit(TestDeterministicGeneration._test_determinism_world_setup, world_type_name, self.multiworld.seed)
                    distribute_items_restrictive(self.multiworld)
                    call_all(self.multiworld, "post_fill")
                    # Get our data first in-case we break something, so we get better exception tracebacks.
                    data_from_current_process = TestDeterministicGeneration._test_determinism_multiworld_to_basic_data(self.multiworld)
                    data_from_other_process = future.result(timeout=10.0)
                    for data_current, data_other, name in zip(data_from_current_process, data_from_other_process, ["regions", "entrances", "locations", "start_inventory"], strict=True):
                        with self.subTest(name):
                            self.assertEqual(data_current, data_other)
                    with self.subTest("locations2"):
                        current_locations = data_from_current_process[2]
                        other_locations = data_from_other_process[2]
                        for player, current_locations_data in current_locations.items():
                            other_locations_data = other_locations.get(player, [])
                            current_locations_dict = {(loc["name"], loc["address"]): (loc["progress_type"], loc["item"]) for loc in current_locations_data}
                            self.assertEqual(len(current_locations_dict), len(current_locations_data), "Duplicate locations were found (current process)")
                            other_locations_dict = {(loc["name"], loc["address"]): (loc["progress_type"], loc["item"]) for loc in other_locations_data}
                            self.assertEqual(len(other_locations_dict), len(other_locations_data), "Duplicate locations were found (other process)")
                            self.assertEqual(current_locations_dict.keys(), other_locations_dict.keys(), "the names and IDs of the locations existing in the multiworld did not match")
                            for loc_key, loc_value in current_locations_dict.items():
                                other_loc_value = other_locations_dict[loc_key]
                                self.assertEqual(other_loc_value, loc_value, f"location data for {loc_key} did not match")
