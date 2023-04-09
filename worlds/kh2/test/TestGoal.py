from . import KH2TestBase
from ..Names import ItemName,LocationName,RegionName

class TestDefault(KH2TestBase):
    options = {}

    def testEverything(self):
        self.collect_all_but([ItemName.Victory])
        self.assertBeatable(True)


class TestLuckyEmblem(KH2TestBase):
    options = {
        "Goal": 1,
    }

    def testEverything(self):
        self.collect_all_but([ItemName.LuckyEmblem])
        self.assertBeatable(True)

class TestHitList(KH2TestBase):
    options = {
        "Goal": 2,
    }
    def testEverything(self):
        self.collect_all_but([ItemName.Bounty])
        self.assertBeatable(True)
