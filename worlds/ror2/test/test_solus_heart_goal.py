from . import RoR2TestBase


class SolusHeartGoalTest(RoR2TestBase):
    options = {
        "dlc_alloyed": "true",
        "victory": "solus_heart",
        "stage_variants": "true"
    }

    def test_false_son(self) -> None:
        self.collect_all_but(["Neural Sanctum", "Victory"])
        self.assertFalse(self.can_reach_region("Neural Sanctum"))
        self.assertBeatable(False)
        self.collect_by_name("Neural Sanctum")
        self.assertTrue(self.can_reach_region("Neural Sanctum"))
        self.assertBeatable(True)
