from . import KH2TestBase
from ..Names import ItemName


class TestDefault(KH2TestBase):
    options = {}

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)


class TestThreeProofs(KH2TestBase):
    options = {
        "Goal": 0,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)


class TestLuckyEmblem(KH2TestBase):
    options = {
        "Goal": 1,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)


class TestHitList(KH2TestBase):
    options = {
        "Goal": 2,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)


class TestLuckyEmblemHitlist(KH2TestBase):
    options = {
        "Goal": 3,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)


class TestThreeProofsNoXemnas(KH2TestBase):
    options = {
        "Goal":        0,
        "FinalXemnas": False,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.ProofofNonexistence])
        self.testAllStateCanReachEverything()
        self.assertBeatable(True)


class TestLuckyEmblemNoXemnas(KH2TestBase):
    options = {
        "Goal": 1,
        "FinalXemnas": False,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.LuckyEmblem])
        self.testAllStateCanReachEverything()
        self.assertBeatable(True)


class TestHitListNoXemnas(KH2TestBase):
    options = {
        "Goal": 2,
        "FinalXemnas": False,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.Bounty])
        self.testAllStateCanReachEverything()
        self.assertBeatable(True)


class TestLuckyEmblemHitlistNoXemnas(KH2TestBase):
    options = {
        "Goal": 3,
        "FinalXemnas": False,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.LuckyEmblem, ItemName.Bounty])
        self.testAllStateCanReachEverything()
        self.assertBeatable(True)
