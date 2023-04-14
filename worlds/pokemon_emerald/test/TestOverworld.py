from test.TestBase import WorldTestBase
from worlds.pokemon_emerald.util import location_name_to_label

class TestOverworld(WorldTestBase):
    game = "Pokemon Emerald"

    def testOverworld(self):
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_ROUTE_102_POTION")))


    def testSurfMinimal(self):
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_PETALBURG_CITY_ETHER")))
        self.assertFalse(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))
        self.assertFalse(self.can_reach_entrance("REGION_ROUTE118/WATER -> REGION_ROUTE118/EAST"))
        self.assertFalse(self.can_reach_entrance("REGION_ROUTE119/UPPER -> REGION_FORTREE_CITY/MAIN"))
        self.assertFalse(self.can_reach_entrance("MAP_FORTREE_CITY:3/MAP_FORTREE_CITY_MART:0"))

        self.collect_by_name(["HM03 Surf", "Balance Badge", "HM06 Rock Smash", "Dynamo Badge"])
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_PETALBURG_CITY_ETHER")))
        self.assertTrue(self.can_reach_location(location_name_to_label("ITEM_LILYCOVE_CITY_MAX_REPEL")))
        self.assertTrue(self.can_reach_entrance("REGION_ROUTE118/WATER -> REGION_ROUTE118/EAST"))
        self.assertTrue(self.can_reach_entrance("REGION_ROUTE119/UPPER -> REGION_FORTREE_CITY/MAIN"))
        self.assertTrue(self.can_reach_entrance("MAP_FORTREE_CITY:3/MAP_FORTREE_CITY_MART:0"))
