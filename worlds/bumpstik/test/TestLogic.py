from . import BumpStikTestBase


class TestRuleLogic(BumpStikTestBase):
    def testLogic(self):
        for treasure_bumpers_held in range(1, 33):
            if treasure_bumpers_held == 32:
                self.assertFalse(self.can_reach_location("Level 5 - Cleared all Hazards"))

            self.collect(self.get_item_by_name("Treasure Bumper"))
            if treasure_bumpers_held % 8 == 0:
                bb_count = round(treasure_bumpers_held / 8)

                if bb_count < 4:
                    self.assertFalse(self.can_reach_location(f"Treasure Bumper {treasure_bumpers_held + 1}"))
                    # Can't reach Treasure Bumper 9 check until level 2 is unlocked, etc.
                    # But we don't have enough Treasure Bumpers to reach this check anyway??
                elif bb_count == 4:
                    bb_count += 1
                    # Level 4 has two new Bonus Booster checks; need to check both

                for booster_bumpers_held in range(self.count("Booster Bumper"), bb_count + 1):
                    if booster_bumpers_held > 0:
                        self.assertTrue(self.can_reach_location(f"Bonus Booster {booster_bumpers_held}"),
                                    f"Bonus Booster {booster_bumpers_held} check not reachable with {self.count('Booster Bumper')} Booster Bumpers")
                    if booster_bumpers_held < 5:
                        self.assertFalse(self.can_reach_location(f"Bonus Booster {booster_bumpers_held + 1}"),
                                         f"Bonus Booster {booster_bumpers_held + 1} check reachable with {self.count('Treasure Bumper')} Treasure Bumpers and {self.count('Booster Bumper')} Booster Bumpers")
                    if booster_bumpers_held < bb_count:
                        self.collect(self.get_item_by_name("Booster Bumper"))

            self.assertTrue(self.can_reach_location(f"Treasure Bumper {treasure_bumpers_held}"),
                            f"Treasure Bumper {treasure_bumpers_held} check not reachable with {self.count('Treasure Bumper')} Treasure Bumpers")

            if treasure_bumpers_held < 32:
                self.assertFalse(self.can_reach_location(f"Treasure Bumper {treasure_bumpers_held + 1}"))
            elif treasure_bumpers_held == 32:
                self.assertTrue(self.can_reach_location("Level 5 - 50,000+ Total Points"))
                self.assertFalse(self.can_reach_location("Level 5 - Cleared all Hazards"))
                self.collect(self.get_items_by_name("Hazard Bumper"))
                self.assertTrue(self.can_reach_location("Level 5 - Cleared all Hazards"))
