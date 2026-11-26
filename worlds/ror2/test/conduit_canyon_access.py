from . import RoR2TestBase


class SolusHeartGoalTest(RoR2TestBase):
    options = {
        "dlc_alloyed": "true",
        "dlc_sots": "true",
        "dlc_sotv": "true",
        "victory": "solus_heart",
        "stage_variants": "true"
    }

    def test_conduit_canyon_access_treeborn_colony_blocked(self) -> None:
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Reformed Altar")
        self.collect_by_name("Treeborn Colony")
        self.collect_by_name("Conduit Canyon")
        self.assertFalse(self.can_reach_region("Conduit Canyon"))
        self.collect_by_name("Rallypoint Delta")
        self.assertTrue(self.can_reach_region("Conduit Canyon"))

    def test_conduit_canyon_access_golden_dieback_blocked(self) -> None:
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Reformed Altar")
        self.collect_by_name("Golden Dieback")
        self.collect_by_name("Conduit Canyon")
        self.assertFalse(self.can_reach_region("Conduit Canyon"))
        self.collect_by_name("Rallypoint Delta")
        self.assertTrue(self.can_reach_region("Conduit Canyon"))

    def test_conduit_canyon_access_rallypoint_delta(self) -> None:
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Reformed Altar")
        self.collect_by_name("Rallypoint Delta")
        self.collect_by_name("Conduit Canyon")
        self.assertTrue(self.can_reach_region("Conduit Canyon"))

    def test_conduit_canyon_access_scorched_acres(self) -> None:
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Reformed Altar")
        self.collect_by_name("Scorched Acres")
        self.collect_by_name("Conduit Canyon")
        self.assertTrue(self.can_reach_region("Conduit Canyon"))

    def test_conduit_canyon_access_sulfur_pools(self) -> None:
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Reformed Altar")
        self.collect_by_name("Scorched Acres")
        self.collect_by_name("Conduit Canyon")
        self.assertTrue(self.can_reach_region("Conduit Canyon"))

    def test_conduit_canyon_access_iron_alluvium(self) -> None:
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Reformed Altar")
        self.collect_by_name("Iron Alluvium")
        self.collect_by_name("Conduit Canyon")
        self.assertTrue(self.can_reach_region("Conduit Canyon"))

    def test_conduit_canyon_access_iron_auroras_variant(self) -> None:
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Progressive Stage")
        self.collect_by_name("Reformed Altar")
        self.collect_by_name("Iron Auroras")
        self.collect_by_name("Conduit Canyon")
        self.assertTrue(self.can_reach_region("Conduit Canyon"))
