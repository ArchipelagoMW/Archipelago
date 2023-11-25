from . import BumpStikTestBase


class TestRuleLogic(BumpStikTestBase):
    def testLogic(self):
        for x in range(1, 33):
            if x == 32:
                self.assertFalse(self.can_reach_location("Level 5 - Cleared all Hazards"))

            self.collect(self.get_item_by_name("Treasure Bumper"))
            if x % 8 == 0:
                bb_count = round(x / 8)

                if bb_count < 4:
                    self.assertFalse(self.can_reach_location(f"Treasure Bumper {x + 1}"))
                elif bb_count == 4:
                    bb_count += 1

                for y in range(self.count("Booster Bumper"), bb_count):
                    self.assertTrue(self.can_reach_location(f"Bonus Booster {y + 1}"),
                                    f"BB {y + 1} check not reachable with {self.count('Booster Bumper')} BBs")
                    if y < 4:
                        self.assertFalse(self.can_reach_location(f"Bonus Booster {y + 2}"),
                                         f"BB {y + 2} check reachable with {self.count('Treasure Bumper')} TBs")
                    self.collect(self.get_item_by_name("Booster Bumper"))

            if x < 31:
                self.assertFalse(self.can_reach_location(f"Treasure Bumper {x + 2}"))
            elif x == 31:
                self.assertFalse(self.can_reach_location("Level 5 - 50,000+ Total Points"))

            if x < 32:
                self.assertTrue(self.can_reach_location(f"Treasure Bumper {x + 1}"),
                                f"TB {x + 1} check not reachable with {self.count('Treasure Bumper')} TBs")
            elif x == 32:
                self.assertTrue(self.can_reach_location("Level 5 - 50,000+ Total Points"))
                self.assertFalse(self.can_reach_location("Level 5 - Cleared all Hazards"))
                self.collect(self.get_items_by_name("Hazard Bumper"))
                self.assertTrue(self.can_reach_location("Level 5 - Cleared all Hazards"))
