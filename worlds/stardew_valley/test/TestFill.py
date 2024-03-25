from . import SVTestBase, minimal_locations_maximal_items
from .assertion import WorldAssertMixin
from .. import options


class TestMinLocationsMaxItems(WorldAssertMixin, SVTestBase):
    options = minimal_locations_maximal_items()

    def run_default_tests(self) -> bool:
        return True

    def test_fill(self):
        self.assert_basic_checks(self.multiworld)


class TestSpecificSeedForTroubleshooting(WorldAssertMixin, SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
        options.FestivalLocations: options.FestivalLocations.option_hard,
    }
    seed = 65453499742665118161

    def run_default_tests(self) -> bool:
        return True

    def test_fill(self):
        self.assert_basic_checks(self.multiworld)
