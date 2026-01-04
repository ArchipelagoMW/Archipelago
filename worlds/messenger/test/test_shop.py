from typing import Dict

from BaseClasses import CollectionState
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
        prices: Dict[str, int] = self.world.shop_prices
        for loc, price in prices.items():
            with self.subTest("prices", loc=loc):
                self.assertLessEqual(price, self.multiworld.get_location(f"The Shop - {loc}", self.player).cost)
                self.assertTrue(loc in SHOP_ITEMS)
        self.assertEqual(len(prices), len(SHOP_ITEMS))


class ShopCostMinTest(ShopCostTest):
    options = {
        "shop_price": "random",
        "shuffle_seals": "false",
    }

    def test_shop_rules(self) -> None:
        if self.world.total_shards:
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

        prices = self.world.shop_prices
        for loc, price in prices.items():
            with self.subTest("prices", loc=loc):
                if loc == "Karuta Plates":
                    self.assertEqual(self.options["shop_price_plan"]["Karuta Plates"], price)
                elif loc == "Serendipitous Bodies":
                    self.assertIn(price, self.options["shop_price_plan"]["Serendipitous Bodies"])

                loc = f"The Shop - {loc}"
                self.assertLessEqual(price, self.multiworld.get_location(loc, self.player).cost)
                self.assertTrue(loc.removeprefix("The Shop - ") in SHOP_ITEMS)
        self.assertEqual(len(prices), len(SHOP_ITEMS))

        figures = self.world.figurine_prices
        for loc, price in figures.items():
            with self.subTest("figure prices", loc=loc):
                if loc == "Barmath'azel Figurine":
                    self.assertEqual(self.options["shop_price_plan"]["Barmath'azel Figurine"], price)
                elif loc == "Demon Hive Figurine":
                    self.assertIn(price, self.options["shop_price_plan"]["Demon Hive Figurine"])

                self.assertTrue(loc in FIGURINES)
        self.assertEqual(len(figures), len(FIGURINES))

        max_cost_state = CollectionState(self.multiworld)
        self.assertFalse(self.world.get_location("Money Wrench").can_reach(max_cost_state))
        prog_shards = []
        for item in self.multiworld.itempool:
            if "Time Shard " in item.name:
                value = int(item.name.strip("Time Shard ()"))
                if value >= 100:
                    prog_shards.append(item)
        for shard in prog_shards:
            max_cost_state.collect(shard, True)
        self.assertTrue(self.world.get_location("Money Wrench").can_reach(max_cost_state))
