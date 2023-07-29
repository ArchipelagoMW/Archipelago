import unittest

from ..items import load_item_csv
from ..locations import load_location_csv


class TestCsvIntegrity(unittest.TestCase):
    def test_items_integrity(self):
        items = load_item_csv()

        for item in items:
            self.assertIsNotNone(item.code_without_offset, "Some item do not have an id."
                                                           " Run the script `update_data.py` to generate them.")

    def test_locations_integrity(self):
        locations = load_location_csv()

        for location in locations:
            self.assertIsNotNone(location.code_without_offset, "Some location do not have an id."
                                                               " Run the script `update_data.py` to generate them.")
