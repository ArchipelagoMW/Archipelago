from . import KH1TestBase


class TestDefault(KH1TestBase):
    options = {}


class TestFinalRest(KH1TestBase):
    options = {
        "Goal": 0,
    }


class TestDeepJungle(KH1TestBase):
    options = {
        "Goal": 1,
    }


class TestAgrabah(KH1TestBase):
    options = {
        "Goal": 2,
    }


class TestMonstro(KH1TestBase):
    options = {
        "Goal": 3,
    }


class TestAtlantica(KH1TestBase):
    options = {
        "Goal": 4,
    }


class TestHalloweenTown(KH1TestBase):
    options = {
        "Goal": 5,
    }


class TestNeverland(KH1TestBase):
    options = {
        "Goal": 6,
    }


class TestUnknown(KH1TestBase):
    options = {
        "Goal": 7,
    }
