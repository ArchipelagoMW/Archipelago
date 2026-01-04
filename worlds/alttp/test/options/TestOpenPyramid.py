from test.bases import WorldTestBase
from ...Items import item_factory


class PyramidTestBase(WorldTestBase):
    game = "A Link to the Past"


class OpenPyramidTest(PyramidTestBase):
    options = {
        "open_pyramid": "open"
    }

    def testAccess(self):
        self.assertFalse(self.can_reach_entrance("Pyramid Hole"))
        self.collect_by_name(["Hammer", "Progressive Glove", "Moon Pearl"])
        self.assertTrue(self.can_reach_entrance("Pyramid Hole"))


class GoalPyramidTest(PyramidTestBase):
    options = {
        "open_pyramid": "goal"
    }

    def testCrystalsGoalAccess(self):
        self.multiworld.worlds[1].options.goal.value = 1  # crystals
        self.assertFalse(self.can_reach_entrance("Pyramid Hole"))
        self.collect_by_name(["Hammer", "Progressive Glove", "Moon Pearl"])
        self.assertTrue(self.can_reach_entrance("Pyramid Hole"))

    def testGanonGoalAccess(self):
        self.assertFalse(self.can_reach_entrance("Pyramid Hole"))
        self.collect_by_name(["Hammer", "Progressive Glove", "Moon Pearl"])
        self.assertFalse(self.can_reach_entrance("Pyramid Hole"))
        self.collect(item_factory("Beat Agahnim 2", self.multiworld.worlds[1]))
        self.assertTrue(self.can_reach_entrance("Pyramid Hole"))

