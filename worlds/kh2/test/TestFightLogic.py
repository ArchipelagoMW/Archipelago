from . import KH2TestBase
from ..Names import ItemName


class TestEasy(KH2TestBase):
    options = {
        "FightLogic": 0
    }

    KH2TestBase()


class TestNormal(KH2TestBase):
    options = {
        "FightLogic": 1
    }

    KH2TestBase()


class TestHard(KH2TestBase):
    options = {
        "FightLogic": 2
    }

    KH2TestBase()





