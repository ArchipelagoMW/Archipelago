import unittest

from worlds.dark_souls_3.Items import DarkSouls3Item
from worlds.dark_souls_3.Locations import location_tables

class DarkSouls3Test(unittest.TestCase):
    def testLocationDefaultItems(self):
        item_name_to_id = DarkSouls3Item.get_name_to_id()
        for locations in location_tables.values():
            for location in locations:
                self.assertIn(location.default_item_name, item_name_to_id)
