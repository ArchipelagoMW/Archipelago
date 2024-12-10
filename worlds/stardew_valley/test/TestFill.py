from . import SVTestBase
from .assertion import WorldAssertMixin
from .options.presets import minimal_locations_maximal_items
from .. import options
from ..mods.mod_data import ModNames


class TestMinLocationsMaxItems(WorldAssertMixin, SVTestBase):
    options = minimal_locations_maximal_items()

    def run_default_tests(self) -> bool:
        return True

    def test_fill(self):
        self.assert_basic_checks(self.multiworld)


class TestSpecificSeedForTroubleshooting(WorldAssertMixin, SVTestBase):
    options = {
        options.Fishsanity: options.Fishsanity.option_all,
        options.Goal: options.Goal.option_master_angler,
        options.QuestLocations: -1,
        options.Mods: (ModNames.sve,),
    }
    seed = 65453499742665118161

    def run_default_tests(self) -> bool:
        return True

    def test_fill(self):
        self.assert_basic_checks(self.multiworld)
