from test.bases import WorldTestBase

from worlds.eldenring.items import item_table
from worlds.eldenring.locations import location_tables

class EldenRingTest(WorldTestBase):
    game = "EldenRing"

    def testLocationDefaultItems(self):
        for locations in location_tables.values():
            for location in locations:
                if location.default_item_name:
                    self.assertIn(location.default_item_name, item_table)

    def testLocationsUnique(self):
        names = set()
        for locations in location_tables.values():
            for location in locations:
                self.assertNotIn(location.name, names)
                names.add(location.name)


#pytest worlds/eldenring/tests   