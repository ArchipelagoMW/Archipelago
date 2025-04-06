import unittest

from ..items import load_item_csv
from ..locations import load_location_csv
from ..options import Mods


class TestCsvIntegrity(unittest.TestCase):
    def test_items_integrity(self):
        items = load_item_csv()

        with self.subTest("Test all items have an id"):
            for item in items:
                self.assertIsNotNone(item.code_without_offset, "Some item do not have an id."
                                                               " Run the script `update_data.py` to generate them.")
        with self.subTest("Test all ids are unique"):
            all_ids = [item.code_without_offset for item in items]
            unique_ids = set(all_ids)
            self.assertEqual(len(all_ids), len(unique_ids))

        with self.subTest("Test all names are unique"):
            all_names = [item.name for item in items]
            unique_names = set(all_names)
            self.assertEqual(len(all_names), len(unique_names))

        with self.subTest("Test all mod names are valid"):
            mod_names = {item.mod_name for item in items}
            for mod_name in mod_names:
                if mod_name:
                    self.assertIn(mod_name, Mods.valid_keys)

    def test_locations_integrity(self):
        locations = load_location_csv()

        with self.subTest("Test all locations have an id"):
            for location in locations:
                self.assertIsNotNone(location.code_without_offset, "Some location do not have an id."
                                                                   " Run the script `update_data.py` to generate them.")
        with self.subTest("Test all ids are unique"):
            all_ids = [location.code_without_offset for location in locations]
            unique_ids = set(all_ids)
            self.assertEqual(len(all_ids), len(unique_ids))

        with self.subTest("Test all names are unique"):
            all_names = [location.name for location in locations]
            unique_names = set(all_names)
            self.assertEqual(len(all_names), len(unique_names))

        with self.subTest("Test all mod names are valid"):
            mod_names = {location.mod_name for location in locations}
            for mod_name in mod_names:
                if mod_name:
                    self.assertIn(mod_name, Mods.valid_keys)
