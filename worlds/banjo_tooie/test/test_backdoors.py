from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from ..Options import Backdoors
from . import BanjoTooieTestBase


class TestOpenBackdoors(BanjoTooieTestBase):
    options = {
        "backdoors": Backdoors.option_true,
    }


class TestClosedBackdoors(BanjoTooieTestBase):
    options = {
        "backdoors": Backdoors.option_false,
    }


class TestOpenBackdoorsIntended(TestOpenBackdoors, IntendedLogic):
    options = {
        **TestOpenBackdoors.options,
        **IntendedLogic.options,
    }


class TestOpenBackdoorsEasyTricks(TestOpenBackdoors, EasyTricksLogic):
    options = {
        **TestOpenBackdoors.options,
        **EasyTricksLogic.options,
    }


class TestOpenBackdoorsHardTricks(TestOpenBackdoors, HardTricksLogic):
    options = {
        **TestOpenBackdoors.options,
        **HardTricksLogic.options,
    }


class TestOpenBackdoorsGlitches(TestOpenBackdoors, GlitchesLogic):
    options = {
        **TestOpenBackdoors.options,
        **GlitchesLogic.options,
    }


class TestClosedBackdoorsIntended(TestClosedBackdoors, IntendedLogic):
    options = {
        **TestClosedBackdoors.options,
        **IntendedLogic.options,
    }


class TestClosedBackdoorsEasyTricks(TestClosedBackdoors, EasyTricksLogic):
    options = {
        **TestClosedBackdoors.options,
        **EasyTricksLogic.options,
    }


class TestClosedBackdoorsHardTricks(TestClosedBackdoors, HardTricksLogic):
    options = {
        **TestClosedBackdoors.options,
        **HardTricksLogic.options,
    }


class TestClosedBackdoorsGlitches(TestClosedBackdoors, GlitchesLogic):
    options = {
        **TestClosedBackdoors.options,
        **GlitchesLogic.options,
    }
