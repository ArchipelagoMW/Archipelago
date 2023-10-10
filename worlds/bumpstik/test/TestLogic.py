from . import BumpStikTestBase


class TestRuleLogic(BumpStikTestBase):
    def testLogic(self):
        for x in range(1, 33):
            if x == 32:
                self.assertFalse(self.can_reach_location("Level 5 - Cleared all Hazards"))

            self.collect(self.get_item_by_name("Treasure Bumper"))
            if x % 8 == 0:
                self.assertFalse(self.can_reach_location(f"Treasure Bumper {x + 1}"))
                for y in range(self.count("Bonus Booster"), round(x / 8) + 1):
                    self.collect(self.get_item_by_name("Bonus Booster"))
                    self.assertTrue(self.can_reach_location(f"Booster Bumper {y + 1}"))
                    if y < 4:
                        self.assertFalse(self.can_reach_location(f"Booster Bumper {y + 2}"))

            if x == 32:
                self.assertTrue(self.can_reach_location("Level 5 - Cleared all Hazards"))
            self.assertTrue(self.can_reach_location(f"Treasure Bumper {x + 1}"))
            if x < 31:
                self.assertFalse(self.can_reach_location(f"Treasure Bumper {x + 2}"))

