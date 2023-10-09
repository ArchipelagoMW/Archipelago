from . import RoR2TestBase


class MithrixGoalTest(RoR2TestBase):
    options = {
        "victory": "mithrix"
    }

    def testMithrix(self) -> None:
        self.collect_all_but(["Commencement", "Victory"])
        self.assertFalse(self.can_reach_entrance("Commencement"))
        self.assertBeatable(False)
        self.collect_by_name("Commencement")
        self.assertTrue(self.can_reach_entrance("Commencement"))
        self.assertBeatable(True)

    def testStage5(self) -> None:
        self.collect_all_but(["Stage 4", "Sky Meadow", "Victory"])
        self.assertFalse(self.can_reach_entrance("Sky Meadow"))
        self.assertBeatable(False)
        self.collect_by_name("Sky Meadow")
        self.assertFalse(self.can_reach_entrance("Sky Meadow"))
        self.collect_by_name("Stage 4")
        self.assertTrue(self.can_reach_entrance("Sky Meadow"))
        self.assertBeatable(True)
