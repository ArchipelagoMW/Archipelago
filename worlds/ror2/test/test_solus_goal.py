from . import RoR2TestBase


class SolusGoalTest(RoR2TestBase):
    options = {
        "dlc_alloyed": "true",
        "victory": "solus"
    }

    def test_neural_sanctum_to_victory(self) -> None:
        self.collect_all_but(["Neural Sanctum", "Victory"])
        self.assertFalse(self.can_reach_location("Victory"))
        self.collect_by_name("Neural Sanctum")
        self.assertTrue(self.can_reach_location("Victory"))

    def test_decompile_ending_chain(self) -> None:
        self.collect_all_but(["Conduit Canyon", "Victory"])
        self.assertFalse(self.can_reach_region("Conduit Canyon"))
        self.assertFalse(self.can_reach_region("Solutional Haunt"))
        self.collect_by_name("Conduit Canyon")
        self.assertTrue(self.can_reach_region("Conduit Canyon"))
        self.assertTrue(self.can_reach_region("Solutional Haunt"))
        self.assertTrue(self.can_reach_region("Computational Exchange"))
        self.assertTrue(self.can_reach_region("Neural Sanctum"))
        self.assertBeatable(True)
