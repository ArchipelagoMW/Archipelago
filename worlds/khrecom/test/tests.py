from . import KHRECOMTestBase

class TestDefault(KHRECOMTestBase):
    options = {}

class TestDaysLocations(KHRECOMTestBase):
    options = {
        "DaysLocations": True,
    }

class TestLeon(KHRECOMTestBase):
    options = {
        "ChecksBehindLeon": True,
    }

class TestMinigames(KHRECOMTestBase):
    options = {
        "ChecksBehindMinigames": True,
    }