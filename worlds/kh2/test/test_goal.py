from . import KH2TestBase
from ..Names import ItemName


class TestDefault(KH2TestBase):
    options = {}


class TestThreeProofs(KH2TestBase):
    options = {
        "Goal": 0,
    }


class TestLuckyEmblem(KH2TestBase):
    options = {
        "Goal": 1,
    }


class TestHitList(KH2TestBase):
    options = {
        "Goal": 2,
    }


class TestLuckyEmblemHitlist(KH2TestBase):
    options = {
        "Goal": 3,
    }


class TestThreeProofsNoXemnas(KH2TestBase):
    options = {
        "Goal":        0,
        "FinalXemnas": False,
    }


class TestLuckyEmblemNoXemnas(KH2TestBase):
    options = {
        "Goal":        1,
        "FinalXemnas": False,
    }


class TestHitListNoXemnas(KH2TestBase):
    options = {
        "Goal":        2,
        "FinalXemnas": False,
    }


class TestLuckyEmblemHitlistNoXemnas(KH2TestBase):
    options = {
        "Goal":        3,
        "FinalXemnas": False,
    }

