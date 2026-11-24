from . import GameDevTycoonTestBase


class TestDefaultOptions(GameDevTycoonTestBase):
    """The default options generate and every location is reachable."""


class TestSuccessLevelJustRetire(GameDevTycoonTestBase):
    options = {"success_level": "just_retire"}


class TestSuccessLevelMillionaire(GameDevTycoonTestBase):
    options = {"success_level": "millionaire"}


class TestSuccessLevelTycoon(GameDevTycoonTestBase):
    options = {"success_level": "tycoon"}
