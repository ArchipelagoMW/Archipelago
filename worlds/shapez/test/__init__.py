from test.bases import WorldTestBase
from .. import options_presets, options_presets_lite


class ShapezTestBase(WorldTestBase):
    game = "shapez"


class ShapezLiteTestBase(WorldTestBase):
    game = "shapez lite"


class TestDefault(ShapezTestBase):
    options = {}


class TestMostVanilla(ShapezTestBase):
    options = options_presets["Most vanilla"]


class TestMinimum(ShapezTestBase):
    options = options_presets["Minimum checks"]


class TestMaximum(ShapezTestBase):
    options = options_presets["Maximum checks"]


class TestRestrictive(ShapezTestBase):
    options = options_presets["Restrictive start"]


class TestQuick(ShapezTestBase):
    options = options_presets["Quick game"]


class TestDefaultLite(ShapezLiteTestBase):
    options = {}


class TestMostVanillaLite(ShapezLiteTestBase):
    options = options_presets_lite["Most vanilla"]


class TestMaximumLite(ShapezLiteTestBase):
    options = options_presets_lite["Maximum checks"]


class TestRestrictiveLite(ShapezLiteTestBase):
    options = options_presets_lite["Restrictive start"]


class TestQuickLite(ShapezLiteTestBase):
    options = options_presets_lite["Quick game"]
