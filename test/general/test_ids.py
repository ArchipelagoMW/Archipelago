import unittest
from worlds.AutoWorld import AutoWorldRegister


class TestIDs(unittest.TestCase):
    def test_unique_items(self):
        """Tests that every game has a unique ID per item in the datapackage"""
        known_item_ids = set()
        for gamename, world_type in AutoWorldRegister.world_types.items():
            current = len(known_item_ids)
            known_item_ids |= set(world_type.item_id_to_name)
            self.assertEqual(len(known_item_ids) - len(world_type.item_id_to_name), current)

    def test_unique_locations(self):
        """Tests that every game has a unique ID per location in the datapackage"""
        known_location_ids = set()
        for gamename, world_type in AutoWorldRegister.world_types.items():
            current = len(known_location_ids)
            known_location_ids |= set(world_type.location_id_to_name)
            self.assertEqual(len(known_location_ids) - len(world_type.location_id_to_name), current)

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
                self.assertEqual(len(world_type.item_id_to_name), len(world_type.item_name_to_id))

    def test_duplicate_location_ids(self):
        """Test that a game doesn't have location id overlap within its own datapackage"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                self.assertEqual(len(world_type.location_id_to_name), len(world_type.location_name_to_id))
