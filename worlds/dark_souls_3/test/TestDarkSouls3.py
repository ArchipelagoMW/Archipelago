from test.TestBase import WorldTestBase

from worlds.dark_souls_3.Items import item_dictionary
from worlds.dark_souls_3.Locations import location_tables
from worlds.dark_souls_3.Bosses import all_bosses

class DarkSouls3Test(WorldTestBase):
    game = "Dark Souls III"

    def testLocationDefaultItems(self):
        for locations in location_tables.values():
            for location in locations:
                self.assertIn(location.default_item_name, item_dictionary)

    def testBossRegions(self):
        all_regions = set(location_tables)
        for boss in all_bosses:
            if boss.region:
                self.assertIn(boss.region, all_regions)

    def testBossLocations(self):
        all_locations = {location.name for locations in location_tables.values() for location in locations}
        for boss in all_bosses:
            for location in boss.locations:
                self.assertIn(location, all_locations)

    def testForceUnique(self):
        tongues = self.get_items_by_name("Pale Tongue")
        self.assertEqual(len(tongues), 1, "There should only be one Pale Tongue in the item pool.")
