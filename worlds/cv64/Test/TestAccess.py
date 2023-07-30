from . import CV64TestBase


class WarpTest(CV64TestBase):
    options = {
        "special1s_per_warp": 3,
        "total_special1s": 21
    }

    def testWarps(self):
        self.assertFalse(self.can_reach_entrance("Warp 3"))
        self.collect([self.get_item_by_name("Special1")] * 9)
        current_s1s = self.count("Special1")
        self.assertTrue(self.can_reach_entrance("Warp 3"))


class ShopTest(CV64TestBase):
    options = {
        "stage_shuffle": True,
        "shopsanity": True
    }

    def testShop(self):
        self.assertFalse(self.can_reach_location("Renon's shop: Roast Chicken purchase"))
        self.collect(self.get_item_by_name("Clocktower Key1"))
        self.assertTrue(self.can_reach_location("Renon's shop: Roast Chicken purchase"))
