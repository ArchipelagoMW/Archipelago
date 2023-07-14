from . import KH2TestBase
from ..Names import ItemName


class TestEasy(KH2TestBase):
    options = {
        "FightLogic": 0
    }

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)
        self.testAllStateCanReachEverything()


class TestNormal(KH2TestBase):
    options = {
        "FightLogic": 1
    }

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)
        self.testAllStateCanReachEverything()


class TestHard(KH2TestBase):
    options = {
        "FightLogic": 2
    }

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)
        self.testAllStateCanReachEverything()





