from . import KH1TestBase

class TestDefault(KH1TestBase):
    options = {}

class TestSephiroth(KH1TestBase):
    options = {
        "Goal": 0,
    }

class TestUnknown(KH1TestBase):
    options = {
        "Goal": 1,
    }

class TestPostcards(KH1TestBase):
    options = {
        "Goal": 2,
    }

class TestFinalAnsem(KH1TestBase):
    options = {
        "Goal": 3,
    }

class TestPuppies(KH1TestBase):
    options = {
        "Goal": 4,
    }
class TestFinalRest(KH1TestBase):
    options = {
        "Goal": 5,
    }
