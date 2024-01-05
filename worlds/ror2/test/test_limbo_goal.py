from . import RoR2TestBase


class LimboGoalTest(RoR2TestBase):
    options = {
        "victory": "limbo"
    }

    def test_limbo(self) -> None:
        self.collect_all_but(["Hidden Realm: A Moment, Whole", "Victory"])
        self.assertFalse(self.can_reach_entrance("Hidden Realm: A Moment, Whole"))
        self.assertBeatable(False)
        self.collect_by_name("Hidden Realm: A Moment, Whole")
        self.assertTrue(self.can_reach_entrance("Hidden Realm: A Moment, Whole"))
        self.assertBeatable(True)
