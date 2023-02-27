from . import LTTPOptionsTestBase
from ...Items import ItemFactory


class OpenPyramidTest(LTTPOptionsTestBase):
    options = {
        "open_pyramid": "open"
    }

    def testAccess(self):
        self.assertFalse(self.can_reach_entrance("Pyramid Hole"))
        self.collect_by_name(["Hammer", "Progressive Glove", "Moon Pearl"])
        self.assertTrue(self.can_reach_entrance("Pyramid Hole"))


class GoalPyramidTest(LTTPOptionsTestBase):
    options = {
        "open_pyramid": "goal"
    }

    def testCrystalsGoalAccess(self):
        self.multiworld.goal[1] = "crystals"
        self.assertFalse(self.can_reach_entrance("Pyramid Hole"))
        self.collect_by_name(["Hammer", "Progressive Glove", "Moon Pearl"])
        self.assertTrue(self.can_reach_entrance("Pyramid Hole"))

    def testGanonGoalAccess(self):
        self.assertFalse(self.can_reach_entrance("Pyramid Hole"))
        self.collect_by_name(["Hammer", "Progressive Glove", "Moon Pearl"])
        self.assertFalse(self.can_reach_entrance("Pyramid Hole"))
        self.multiworld.state.collect(ItemFactory("Beat Agahnim 2", 1))
        self.assertTrue(self.can_reach_entrance("Pyramid Hole"))

