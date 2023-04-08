from typing import Dict

from . import MessengerTestBase
from ..Shop import SHOP_ITEMS, FIGURINES


class ShopCostTest(MessengerTestBase):
    options = {
        "shop_shuffle": "true",
        "shop_price": "random",
        "shuffle_shards": "true",
    }

    def testShopRules(self) -> None:
        for loc in SHOP_ITEMS:
            loc = f"The Shop - {loc}"
            with self.subTest("has cost", loc=loc):
                self.assertFalse(self.can_reach_location(loc))

        prices: Dict[str, int] = self.multiworld.worlds[self.player].shop_prices
        for loc, price in prices.items():
            with self.subTest("prices", loc=loc):
                self.assertEqual(price, self.multiworld.get_location(f"The Shop - {loc}", self.player).cost())
                self.assertTrue(loc in SHOP_ITEMS)
        self.assertEqual(len(prices), len(SHOP_ITEMS))

    def testDBoost(self) -> None:
        locations = [
            "Riviere Turquoise Seal - Bounces and Balls", "Riviere Turquoise Seal - Launch of Faith",
        ]
        items = [["Path of Resilience", "Meditation", "Second Wind"]]
        self.assertAccessDependency(locations, items)

    def testCurrents(self) -> None:
        self.assertAccessDependency(["Elemental Skylands Seal - Water"], [["Currents Master"]])

    def testStrike(self) -> None:
        locations = [
            "Searing Crags - Power Thistle", "Searing Crags - Key of Strength", "Searing Crags - Astral Tea Leaves",
            "Searing Crags Seal - Triple Ball Spinner", "Searing Crags Seal - Raining Rocks",
            "Searing Crags Seal - Rhythm Rocks", "Searing Crags Mega Shard", "Cloud Ruins - Acro",
            "Cloud Ruins Seal - Ghost Pit", "Cloud Ruins Seal - Toothbrush Alley", "Cloud Ruins Seal - Saw Pit",
            "Cloud Ruins Seal - Money Farm Room", "Cloud Entrance Mega Shard", "Time Warp Mega Shard",
            "Money Farm Room Mega Shard 1", "Money Farm Room Mega Shard 2",
            "Glacial Peak Seal - Ice Climbers", "Glacial Peak Seal - Projectile Spike Pit",
            "Glacial Peak Seal - Glacial Air Swag", "Glacial Peak Mega Shard", "Riviere Turquoise - Butterfly Matriarch",
            "Riviere Turquoise Seal - Flower Power", "Quick Restock Mega Shard 1", "Quick Restock Mega Shard 2",
            "Elemental Skylands - Key of Symbiosis", "Elemental Skylands Seal - Air", "Elemental Skylands Seal - Water",
            "Elemental Skylands Seal - Fire", "Earth Mega Shard", "Water Mega Shard", "Rescue Phantom",
        ]
        items = [["Strike of the Ninja"]]
        self.assertAccessDependency(locations, items)


class ShopMinLocTest(MessengerTestBase):
    options = {
        "shuffle_seals": "false",
        "shop_shuffle": "true",
    }


class PlandoTest(MessengerTestBase):
    options = {
        "shop_shuffle": "true",
        "shop_price_plan": {
            "Karuta Plates": 50,
            "Serendipitous Bodies": {100: 1, 200: 1, 300: 1},
            "Barmath'azel Figurine": 500,
            "Demon Hive Figurine": {100: 1, 200: 2, 300: 1},
        },
    }

    def testCosts(self) -> None:
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
                self.assertEqual(price, self.multiworld.get_location(loc, self.player).cost())
                self.assertTrue(loc.replace("The Shop - ", "") in SHOP_ITEMS)
        self.assertEqual(len(prices), len(SHOP_ITEMS))

        figures = self.multiworld.worlds[self.player].figurine_prices
        for loc, price in figures.items():
            with self.subTest("figure prices", loc=loc):
                if loc == "Barmath'azel Figurine":
                    self.assertEqual(self.options["shop_price_plan"]["Barmath'azel Figurine"], price)
                elif loc == "Demon Hive Figurine":
                    self.assertIn(price, self.options["shop_price_plan"]["Demon Hive Figurine"])

                self.assertEqual(price, self.multiworld.get_location(loc, self.player).cost())
                self.assertTrue(loc in FIGURINES)
        self.assertEqual(len(figures), len(FIGURINES))
