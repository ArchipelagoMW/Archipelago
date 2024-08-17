from test.bases import WorldTestBase
from .. import options_presets


class ShapezTestBase(WorldTestBase):
    game = "shapez"


class TestDefault(ShapezTestBase):
    options = {}


class TestMinimum(ShapezTestBase):
    options = options_presets["Minimum checks"]


class TestMaximum(ShapezTestBase):
    options = options_presets["Maximum checks"]
