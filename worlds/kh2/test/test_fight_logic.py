from . import KH2TestBase


class TestEasy(KH2TestBase):
    options = {
        "FightLogic": 0
    }


class TestNormal(KH2TestBase):
    options = {
        "FightLogic": 1
    }


class TestHard(KH2TestBase):
    options = {
        "FightLogic": 2
    }
