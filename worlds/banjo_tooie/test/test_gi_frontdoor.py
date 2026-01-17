from ..Options import GIFrontDoor
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestGIFrontDoorOpen(BanjoTooieTestBase):
    options = {
        "open_gi_frontdoor": GIFrontDoor.option_true,
    }


class TestGIFrontDoorClosed(BanjoTooieTestBase):
    options = {
        "open_gi_frontdoor": GIFrontDoor.option_false,
    }


class TestGIFrontDoorOpenIntended(TestGIFrontDoorOpen, IntendedLogic):
    options = {
        **TestGIFrontDoorOpen.options,
        **IntendedLogic.options,
    }


class TestGIFrontDoorOpenEasyTricks(TestGIFrontDoorOpen, EasyTricksLogic):
    options = {
        **TestGIFrontDoorOpen.options,
        **EasyTricksLogic.options,
    }


class TestGIFrontDoorOpenHardTricks(TestGIFrontDoorOpen, HardTricksLogic):
    options = {
        **TestGIFrontDoorOpen.options,
        **HardTricksLogic.options,
    }


class TestGIFrontDoorOpenGlitches(TestGIFrontDoorOpen, GlitchesLogic):
    options = {
        **TestGIFrontDoorOpen.options,
        **GlitchesLogic.options,
    }


class TestGIFrontDoorClosedIntended(TestGIFrontDoorClosed, IntendedLogic):
    options = {
        **TestGIFrontDoorClosed.options,
        **IntendedLogic.options,
    }


class TestGIFrontDoorClosedEasyTricks(TestGIFrontDoorClosed, EasyTricksLogic):
    options = {
        **TestGIFrontDoorClosed.options,
        **EasyTricksLogic.options,
    }


class TestGIFrontDoorClosedHardTricks(TestGIFrontDoorClosed, HardTricksLogic):
    options = {
        **TestGIFrontDoorClosed.options,
        **HardTricksLogic.options,
    }


class TestGIFrontDoorClosedGlitches(TestGIFrontDoorClosed, GlitchesLogic):
    options = {
        **TestGIFrontDoorClosed.options,
        **GlitchesLogic.options,
    }
