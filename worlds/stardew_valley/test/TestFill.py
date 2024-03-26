from . import SVTestBase, minimal_locations_maximal_items
from .assertion import WorldAssertMixin


class TestMinLocationsMaxItems(WorldAssertMixin, SVTestBase):
    options = minimal_locations_maximal_items()

    def run_default_tests(self) -> bool:
        return True

    def test_fill(self):
        self.assert_basic_checks(self.multiworld)
