from test.bases import WorldTestBase

from worlds.dark_souls_3.Items import item_dictionary
from worlds.dark_souls_3.Locations import location_tables
from worlds.dark_souls_3.Bosses import all_bosses

class DarkSouls3Test(WorldTestBase):
    game = "Dark Souls III"

    def testLocationDefaultItems(self):
        for locations in location_tables.values():
            for location in locations:
                if location.default_item_name:
                    self.assertIn(location.default_item_name, item_dictionary)

    def testLocationsUnique(self):
        names = set()
        for locations in location_tables.values():
            for location in locations:
                self.assertNotIn(location.name, names)
                names.add(location.name)

    def testBossLocations(self):
        all_locations = {location.name for locations in location_tables.values() for location in locations}
        for boss in all_bosses:
            for location in boss.locations:
                self.assertIn(location, all_locations)
