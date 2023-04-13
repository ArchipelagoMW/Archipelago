import unittest

from ..items import load_item_csv
from ..locations import load_location_csv


class TestCsvIntegrity(unittest.TestCase):
    def test_items_integrity(self):
        items = load_item_csv()

        for item in items:
            assert item.code_without_offset is not None, \
                "Some item do not have an id. Run the script `update_data.py` to generate them."

    def test_locations_integrity(self):
        locations = load_location_csv()

        for location in locations:
            assert location.code_without_offset is not None, \
                "Some location do not have an id. Run the script `update_data.py` to generate them."
