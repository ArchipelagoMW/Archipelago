from . import BombRushCyberfunkTestBase


class TestRegularGraffitiGlitchless(BombRushCyberfunkTestBase):
    options = {
        "logic": "glitchless",
        "limited_graffiti": False
    }


class TestLimitedGraffitiGlitchless(BombRushCyberfunkTestBase):
    options = {
        "logic": "glitchless",
        "limited_graffiti": True
    }


class TestRegularGraffitiGlitched(BombRushCyberfunkTestBase):
    options = {
        "logic": "glitched",
        "limited_graffiti": False
    }


class TestLimitedGraffitiGlitched(BombRushCyberfunkTestBase):
    options = {
        "logic": "glitched",
        "limited_graffiti": True
    }