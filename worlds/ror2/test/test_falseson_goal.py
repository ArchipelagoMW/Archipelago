from . import RoR2TestBase


class FalseSonGoalTest(RoR2TestBase):
    options = {
        "dlc_sots": "true",
        "victory": "falseson",
        "stage_variants": "true"
    }

    def test_false_son(self) -> None:
        self.collect_all_but(["Prime Meridian", "Victory"])
        self.assertFalse(self.can_reach_region("Prime Meridian"))
        self.assertBeatable(False)
        self.collect_by_name("Prime Meridian")
        self.assertTrue(self.can_reach_region("Prime Meridian"))
        self.assertBeatable(True)
