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

    KH2TestBase()


class TestLuckyEmblem(KH2TestBase):
    options = {
        "Goal": 1,
    }

    KH2TestBase()


class TestHitList(KH2TestBase):
    options = {
        "Goal": 2,
    }

    KH2TestBase()


class TestLuckyEmblemHitlist(KH2TestBase):
    options = {
        "Goal": 3,
    }

    KH2TestBase()


class TestThreeProofsNoXemnas(KH2TestBase):
    options = {
        "Goal":        0,
        "FinalXemnas": False,
    }

    KH2TestBase()


class TestLuckyEmblemNoXemnas(KH2TestBase):
    options = {
        "Goal": 1,
        "FinalXemnas": False,
    }

    KH2TestBase()


class TestHitListNoXemnas(KH2TestBase):
    options = {
        "Goal": 2,
        "FinalXemnas": False,
    }

    KH2TestBase()


class TestLuckyEmblemHitlistNoXemnas(KH2TestBase):
    options = {
        "Goal": 3,
        "FinalXemnas": False,
    }

    KH2TestBase()
