from typing import TypedDict
from unittest import TestCase

import worlds
from BaseClasses import (
    Location, MultiWorld, Item, Entrance, Region, ItemClassification, LocationProgressType,
)
from Fill import distribute_items_restrictive
from Options import Removed
from worlds.AutoWorld import AutoWorldRegister, call_all
from ..general import setup_multiworld


# TypedDicts for passing generated multiworld data between processes. At runtime, TypedDict is equivalent to a plain
# dict, so is efficient to transfer between processes.
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


def serialize_item(item: Item, item_memodict: dict[int, ItemData]) -> ItemData:
    object_id = id(item)
    if object_id in item_memodict:
        return item_memodict[object_id]
    else:
        to_return = {"name": item.name, "player": item.player, "code": item.code, "classification": item.classification}
        item_memodict[object_id] = to_return
        return to_return


def serialize_location(loc: Location, item_memodict: dict[int, ItemData], include_item: bool = False) -> LocationData:
    item = loc.item
    if include_item and item is not None:
        item_data = serialize_item(item, item_memodict)
    else:
        item_data = None

    # ALttP does not play by the rules and sets some location addresses to `list[int]` instead of `int | None`.
    address = loc.address
    if address is not None and type(address) is not int:
        address = None
    return {"name": loc.name, "address": address, "progress_type": loc.progress_type, "item": item_data}


def serialize_entrance(ent: Entrance) -> EntranceData:
    parent_region = ent.parent_region
    parent_region_name = parent_region.name if parent_region is not None else None
    connected_region = ent.connected_region
    connected_region_name = connected_region.name if connected_region is not None else None
    return {"name": ent.name, "parent_region": parent_region_name, "connected_region": connected_region_name}


def serialize_region(reg: Region) -> RegionData:
    return {"name": reg.name, "locations": [loc.name for loc in reg.locations]}


def serialize_options(multiworld: MultiWorld) -> dict[int, list[dict[str, str]]]:
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


def serialize_multiworld(item_pool_copy: list[Item], multiworld: MultiWorld) -> tuple[
    list[ItemData],
    dict[int, list[RegionData]],
    dict[int, list[EntranceData]],
    dict[int, list[LocationData]],
    dict[int, list[tuple[str, ItemData | None]]],
    dict[int, list[ItemData]],
    dict[int, list[dict[str, str]]]
]:
    # Items that were in the item pool are expected to be placed at locations. The ItemData for these items is
    # deduplicated by tracking the created ItemData for each Item instance, by the Item instance's unique object
    # identifier. This is similar to using copy.deepcopy(obj, item_memo).
    item_memo: dict[int, ItemData] = {}

    item_pool_before_main_fill = [serialize_item(item, item_memo) for item in item_pool_copy]
    # The order that regions and entrances are added to the multiworld is not considered important, so sort them by
    # name.
    regions = {player: sorted(map(serialize_region, regions.values()), key=lambda reg: reg["name"])
               for player, regions in multiworld.regions.region_cache.items()}
    entrances = {player: sorted(map(serialize_entrance, entrances.values()), key=lambda ent: ent["name"])
                 for player, entrances in multiworld.regions.entrance_cache.items()}
    locations = {player: [serialize_location(loc, item_memo) for loc in locations.values()]
                 for player, locations in multiworld.regions.location_cache.items()}
    # Locations with the items placed at them, to compare the results of filling the multiworld.
    placements = {player: [(loc.name, None if loc.item is None else serialize_item(loc.item, item_memo)) for loc in locations.values()]
                  for player, locations in multiworld.regions.location_cache.items()}
    # Items that were in the item pool typically won't end up precollected_items, but it is possible, so `item_memo`
    # is passed as an argument.
    precollected_items = {player: [serialize_item(item, item_memo) for item in items]
                          for player, items in multiworld.precollected_items.items()}

    return item_pool_before_main_fill, regions, entrances, locations, placements, precollected_items, serialize_options(multiworld)


class TestDeterministicGeneration(TestCase):
    @staticmethod
    def _test_determinism_world_setup(world_type_name: str, seed: int):
        world_type = worlds.AutoWorldRegister.world_types[world_type_name]
        multiworld = setup_multiworld(world_type, seed=seed)
        item_pool_copy = multiworld.itempool.copy()
        distribute_items_restrictive(multiworld)
        call_all(multiworld, "post_fill")
        return serialize_multiworld(item_pool_copy, multiworld)

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
                    item_pool_copy = self.multiworld.itempool.copy()
                    distribute_items_restrictive(self.multiworld)
                    call_all(self.multiworld, "post_fill")
                    # Serialize self.multiworld first in-case something in the test breaks, so full exception tracebacks
                    # are produced instead of receiving an Exception from the other process.
                    data_from_current_process = serialize_multiworld(item_pool_copy, self.multiworld)
                    data_from_other_process = future.result(timeout=10.0)
                    for data_current, data_other, name in zip(data_from_current_process, data_from_other_process, ["item_pool", "regions", "entrances", "locations", "locations_with_items", "start_inventory", "options"], strict=True):
                        with self.subTest(name):
                            self.assertEqual(data_current, data_other)

