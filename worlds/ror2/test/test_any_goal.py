from . import RoR2TestBase


class DLCTest(RoR2TestBase):
    options = {
        "dlc_sotv": "true",
        "victory": "any"
    }

    def test_commencement_victory(self) -> None:
        self.collect_all_but(["Commencement", "The Planetarium", "Hidden Realm: A Moment, Whole", "Victory"])
        self.assertBeatable(False)
        self.collect_by_name("Commencement")
        self.assertBeatable(True)

    def test_planetarium_victory(self) -> None:
        self.collect_all_but(["Commencement", "The Planetarium", "Hidden Realm: A Moment, Whole", "Victory"])
        self.assertBeatable(False)
        self.collect_by_name("The Planetarium")
        self.assertBeatable(True)

    def test_moment_whole_victory(self) -> None:
        self.collect_all_but(["Commencement", "The Planetarium", "Hidden Realm: A Moment, Whole", "Victory"])
        self.assertBeatable(False)
        self.collect_by_name("Hidden Realm: A Moment, Whole")
        self.assertBeatable(True)
