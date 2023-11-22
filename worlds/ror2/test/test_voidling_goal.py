from . import RoR2TestBase


class VoidlingGoalTest(RoR2TestBase):
    options = {
        "dlc_sotv": "true",
        "victory": "voidling"
    }

    def test_planetarium(self) -> None:
        self.collect_all_but(["The Planetarium", "Victory"])
        self.assertFalse(self.can_reach_entrance("The Planetarium"))
        self.assertBeatable(False)
        self.collect_by_name("The Planetarium")
        self.assertTrue(self.can_reach_entrance("The Planetarium"))
        self.assertBeatable(True)

    def test_void_locus_to_victory(self) -> None:
        self.collect_all_but(["Void Locus", "Commencement"])
        self.assertFalse(self.can_reach_location("Victory"))
        self.collect_by_name("Void Locus")
        self.assertTrue(self.can_reach_entrance("Victory"))

    def test_commencement_to_victory(self) -> None:
        self.collect_all_but(["Void Locus", "Commencement"])
        self.assertFalse(self.can_reach_location("Victory"))
        self.collect_by_name("Commencement")
        self.assertTrue(self.can_reach_location("Victory"))
