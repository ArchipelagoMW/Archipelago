from . import MessengerTestBase
from ..Shop import SHOP_ITEMS


class ShopCostTest(MessengerTestBase):
    options = {
        "shop_shuffle": "true"
    }

    def testShopRules(self) -> None:
        for loc in SHOP_ITEMS:
            with self.subTest("has cost", loc=loc):
                self.assertFalse(self.can_reach_location(loc))

        prices = self.multiworld.worlds[self.player].shop_prices
        for loc, price in prices.items():
            with self.subTest("prices", loc=loc):
                self.assertEqual(price, self.multiworld.get_location(loc, self.player).cost())
                self.assertTrue(loc in SHOP_ITEMS)
        self.assertEqual(len(prices), len(SHOP_ITEMS))


class PlandoTest(MessengerTestBase):
    options = {
        "shop_shuffle": "true",
        "shop_price_plan": {
            "Karuta Plates": 50,
            "Serendipitous Bodies": {100: 1, 200: 1, 300: 1}
        }
    }

    def testCosts(self) -> None:
        for loc in SHOP_ITEMS:
            with self.subTest("has cost", loc=loc):
                self.assertFalse(self.can_reach_location(loc))

        prices = self.multiworld.worlds[self.player].shop_prices
        for loc, price in prices.items():
            with self.subTest("prices", loc=loc):
                if loc == "Karuta Plates":
                    self.assertEqual(self.options["shop_price_plan"]["Karuta Plates"],
                                     self.multiworld.get_location(loc, self.player).cost())
                elif loc == "Serendipitous Bodies":
                    self.assertTrue(self.multiworld.get_location(loc, self.player).cost()
                                    in self.options["shop_price_plan"]["Serendipitous Bodies"])

                self.assertEqual(price, self.multiworld.get_location(loc, self.player).cost())
                self.assertTrue(loc in SHOP_ITEMS)
        self.assertEqual(len(prices), len(SHOP_ITEMS))
