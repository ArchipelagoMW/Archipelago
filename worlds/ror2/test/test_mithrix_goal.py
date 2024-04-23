from . import RoR2TestBase


class MithrixGoalTest(RoR2TestBase):
    options = {
        "victory": "mithrix",
        "require_stages": "true",
        "progressive_stages": "false"
    }

    def test_mithrix(self) -> None:
        self.collect_all_but(["Commencement", "Victory"])
        self.assertFalse(self.can_reach_region("Commencement"))
        self.assertBeatable(False)
        self.collect_by_name("Commencement")
        self.assertTrue(self.can_reach_region("Commencement"))
        self.assertBeatable(True)

    def test_stage5(self) -> None:
        self.collect_all_but(["Stage 4", "Sky Meadow", "Victory"])
        self.assertFalse(self.can_reach_region("Sky Meadow"))
        self.assertBeatable(False)
        self.collect_by_name("Sky Meadow")
        self.assertFalse(self.can_reach_region("Sky Meadow"))
        self.collect_by_name("Stage 4")
        self.assertTrue(self.can_reach_region("Sky Meadow"))
        self.assertBeatable(True)
