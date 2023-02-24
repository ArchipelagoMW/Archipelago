from BaseClasses import ItemClassification
from test.TestBase import WorldTestBase
from worlds.pokemon_emerald.Items import PokemonEmeraldItem

class TestOverworld(WorldTestBase):
    game = "Pokemon Emerald"

    # Broken because of events
    # def testOverworld(self):
    #     self.assertTrue(self.can_reach_location("ITEM_ROUTE_102_POTION"))
    #     self.assertTrue(self.can_reach_location("ITEM_ROUTE_123_PP_UP"))
    #     self.assertTrue(self.can_reach_location("HIDDEN_ITEM_ROUTE_128_HEART_SCALE_1"))
    #     self.assertTrue(self.can_reach_location("ITEM_ROUTE_114_RARE_CANDY"))

    #     # Should use assertAccessDependency once world is fully connected
    #     self.assertFalse(self.can_reach_location("ITEM_PETALBURG_CITY_ETHER"))
    #     surf_items = self.collect_by_name(["HM03 Surf", "Balance Badge"])
    #     self.assertTrue(self.can_reach_location("ITEM_PETALBURG_CITY_ETHER"))
    #     self.remove(surf_items)
