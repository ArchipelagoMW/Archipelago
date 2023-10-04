from . import BumpStikTestBase


class TestRuleLogic(BumpStikTestBase):
    def testTreasures(self):
        locations = ["Treasure Bumper 4"]
        items = [["Treasure Bumper" for _ in range(4)]]
        self.assertAccessDependency(locations, items)

    def testTreasuresLv2(self):
        locations = ["Treasure Bumper 12"]
        items = [["Treasure Bumper" for _ in range(12)] + 
            ["Bonus Booster" for _ in range(2)]]
        self.assertAccessDependency(locations, items)

    def testLevels(self):
        landmarks = [f"Level {x} - Combo 5" for _ in range(2, 5)] + \
            ["Level 5 - Cleared all Hazards"]
        for x, landmark in enumerate(landmarks):
            locations = [landmark]
            items = [["Treasure Bumper" for _ in range(x * 8)] + 
                ["Bonus Booster" for _ in range(x + 1)]]
            self.assertAccessDependency(locations, items)
