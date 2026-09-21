from . import KH1TestBase

class TestDefault(KH1TestBase):
    options = {}

class TestSephiroth(KH1TestBase):
    options = {
        "Final Rest Door Key": 0,
    }

class TestUnknown(KH1TestBase):
    options = {
        "Final Rest Door Key": 1,
    }

class TestPostcards(KH1TestBase):
    options = {
        "Final Rest Door Key": 2,
    }

class TestLuckyEmblems(KH1TestBase):
    options = {
        "Final Rest Door Key": 3,
    }

class TestPuppies(KH1TestBase):
    options = {
        "Final Rest Door Key": 4,
    }
class TestFinalRest(KH1TestBase):
    options = {
        "Final Rest Door Key": 5,
    }
