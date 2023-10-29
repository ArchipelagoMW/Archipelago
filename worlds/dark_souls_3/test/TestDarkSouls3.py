from test.TestBase import WorldTestBase

from worlds.dark_souls_3.Items import item_dictionary
from worlds.dark_souls_3.Locations import location_tables

class DarkSouls3Test(WorldTestBase):
    game = "Dark Souls III"

    def testLocationDefaultItems(self):
        for locations in location_tables.values():
            for location in locations:
                self.assertIn(location.default_item_name, item_dictionary)
