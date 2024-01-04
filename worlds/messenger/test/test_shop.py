from typing import Dict

from . import MessengerTestBase
from ..shop import SHOP_ITEMS, FIGURINES


class ShopCostTest(MessengerTestBase):
    options = {
        "shop_price": "random",
        "shuffle_shards": "true",
    }

    def test_shop_rules(self) -> None:
        for loc in SHOP_ITEMS:
            loc = f"The Shop - {loc}"
            with self.subTest("has cost", loc=loc):
                self.assertFalse(self.can_reach_location(loc))

    def test_shop_prices(self) -> None:
        prices: Dict[str, int] = self.multiworld.worlds[self.player].shop_prices
        for loc, price in prices.items():
            with self.subTest("prices", loc=loc):
                self.assertLessEqual(price, self.multiworld.get_location(f"The Shop - {loc}", self.player).cost)
                self.assertTrue(loc in SHOP_ITEMS)
        self.assertEqual(len(prices), len(SHOP_ITEMS))

    def test_dboost(self) -> None:
        locations = [
            "Riviere Turquoise Seal - Bounces and Balls",
            "Forlorn Temple - Demon King", "Forlorn Temple Seal - Rocket Maze", "Forlorn Temple Seal - Rocket Sunset",
            "Sunny Day Mega Shard", "Down Under Mega Shard",
        ]
        items = [["Path of Resilience", "Meditation", "Second Wind"]]
        self.assertAccessDependency(locations, items)

    def test_currents(self) -> None:
        self.assertAccessDependency(["Elemental Skylands Seal - Water"], [["Currents Master"]])

    def test_strike(self) -> None:
        locations = [
            "Glacial Peak Seal - Projectile Spike Pit", "Elemental Skylands Seal - Fire",
        ]
        items = [["Strike of the Ninja"]]
        self.assertAccessDependency(locations, items)


class ShopCostMinTest(ShopCostTest):
    options = {
        "shop_price": "random",
        "shuffle_seals": "false",
    }

    def test_shop_rules(self) -> None:
        if self.multiworld.worlds[self.player].total_shards:
            super().test_shop_rules()
        else:
            for loc in SHOP_ITEMS:
                loc = f"The Shop - {loc}"
                with self.subTest("has cost", loc=loc):
                    self.assertTrue(self.can_reach_location(loc))

    def test_dboost(self) -> None:
        pass

    def test_currents(self) -> None:
        pass

    def test_strike(self) -> None:
        pass


class PlandoTest(MessengerTestBase):
    options = {
        "shop_price_plan": {
            "Karuta Plates": 50,
            "Serendipitous Bodies": {100: 1, 200: 1, 300: 1},
            "Barmath'azel Figurine": 500,
            "Demon Hive Figurine": {100: 1, 200: 2, 300: 1},
        },
    }

    def test_costs(self) -> None:
        for loc in SHOP_ITEMS:
            loc = f"The Shop - {loc}"
            with self.subTest("has cost", loc=loc):
                self.assertFalse(self.can_reach_location(loc))

        prices = self.multiworld.worlds[self.player].shop_prices
        for loc, price in prices.items():
            with self.subTest("prices", loc=loc):
                if loc == "Karuta Plates":
                    self.assertEqual(self.options["shop_price_plan"]["Karuta Plates"], price)
                elif loc == "Serendipitous Bodies":
                    self.assertIn(price, self.options["shop_price_plan"]["Serendipitous Bodies"])

                loc = f"The Shop - {loc}"
                self.assertLessEqual(price, self.multiworld.get_location(loc, self.player).cost)
                self.assertTrue(loc.replace("The Shop - ", "") in SHOP_ITEMS)
        self.assertEqual(len(prices), len(SHOP_ITEMS))

        figures = self.multiworld.worlds[self.player].figurine_prices
        for loc, price in figures.items():
            with self.subTest("figure prices", loc=loc):
                if loc == "Barmath'azel Figurine":
                    self.assertEqual(self.options["shop_price_plan"]["Barmath'azel Figurine"], price)
                elif loc == "Demon Hive Figurine":
                    self.assertIn(price, self.options["shop_price_plan"]["Demon Hive Figurine"])

                self.assertTrue(loc in FIGURINES)
        self.assertEqual(len(figures), len(FIGURINES))
