import unittest

from Fill import distribute_items_restrictive
from worlds import network_data_package
from worlds.AutoWorld import AutoWorldRegister, call_all
from . import setup_solo_multiworld


class TestIDs(unittest.TestCase):
    def test_range_items(self):
        """There are Javascript clients, which are limited to Number.MAX_SAFE_INTEGER due to 64bit float precision."""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                for item_id in world_type.item_id_to_name:
                    self.assertLess(item_id, 2**53)

    def test_range_locations(self):
        """There are Javascript clients, which are limited to Number.MAX_SAFE_INTEGER due to 64bit float precision."""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                for location_id in world_type.location_id_to_name:
                    self.assertLess(location_id, 2**53)

    def test_reserved_items(self):
        """negative item IDs are reserved to the special "Archipelago" world."""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                if gamename == "Archipelago":
                    for item_id in world_type.item_id_to_name:
                        self.assertLess(item_id, 0)
                else:
                    for item_id in world_type.item_id_to_name:
                        self.assertGreater(item_id, 0)

    def test_reserved_locations(self):
        """negative location IDs are reserved to the special "Archipelago" world."""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                if gamename == "Archipelago":
                    for location_id in world_type.location_id_to_name:
                        self.assertLess(location_id, 0)
                else:
                    for location_id in world_type.location_id_to_name:
                        self.assertGreater(location_id, 0)

    def test_duplicate_item_ids(self):
        """Test that a game doesn't have item id overlap within its own datapackage"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                len_item_id_to_name = len(world_type.item_id_to_name)
                len_item_name_to_id = len(world_type.item_name_to_id)

                if len_item_id_to_name != len_item_name_to_id:
                    self.assertCountEqual(
                        world_type.item_id_to_name.values(), 
                        world_type.item_name_to_id.keys(),
                        "\nThese items have overlapping ids with other items in its own world")
                    self.assertCountEqual(
                        world_type.item_id_to_name.keys(), 
                        world_type.item_name_to_id.values(),
                        "\nThese items have overlapping names with other items in its own world")
                    
                self.assertEqual(len_item_id_to_name, len_item_name_to_id)

    def test_duplicate_location_ids(self):
        """Test that a game doesn't have location id overlap within its own datapackage"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                len_location_id_to_name = len(world_type.location_id_to_name)
                len_location_name_to_id = len(world_type.location_name_to_id)

                if len_location_id_to_name != len_location_name_to_id:
                    self.assertCountEqual(
                        world_type.location_id_to_name.values(), 
                        world_type.location_name_to_id.keys(),
                        "\nThese locations have overlapping ids with other locations in its own world")
                    self.assertCountEqual(
                        world_type.location_id_to_name.keys(), 
                        world_type.location_name_to_id.values(),
                        "\nThese locations have overlapping names with other locations in its own world")

                self.assertEqual(len_location_id_to_name, len_location_name_to_id)

    def test_postgen_datapackage(self):
        """Generates a solo multiworld and checks that the datapackage is still valid"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                multiworld = setup_solo_multiworld(world_type)
                distribute_items_restrictive(multiworld)
                call_all(multiworld, "post_fill")
                datapackage = world_type.get_data_package_data()
                for item_group, item_names in datapackage["item_name_groups"].items():
                    self.assertIsInstance(item_group, str,
                                          f"item_name_group names should be strings: {item_group}")
                    for item_name in item_names:
                        self.assertIsInstance(item_name, str,
                                              f"{item_name}, in group {item_group} is not a string")
                for loc_group, loc_names in datapackage["location_name_groups"].items():
                    self.assertIsInstance(loc_group, str,
                                          f"location_name_group names should be strings: {loc_group}")
                    for loc_name in loc_names:
                        self.assertIsInstance(loc_name, str,
                                              f"{loc_name}, in group {loc_group} is not a string")
                for item_name, item_id in datapackage["item_name_to_id"].items():
                    self.assertIsInstance(item_name, str,
                                          f"{item_name} is not a valid item name for item_name_to_id")
                    self.assertIsInstance(item_id, int,
                                          f"{item_id} for {item_name} should be an int")
                for loc_name, loc_id in datapackage["location_name_to_id"].items():
                    self.assertIsInstance(loc_name, str,
                                          f"{loc_name} is not a valid item name for location_name_to_id")
                    self.assertIsInstance(loc_id, int,
                                          f"{loc_id} for {loc_name} should be an int")
                self.assertEqual(datapackage["checksum"], network_data_package["games"][gamename]["checksum"])
