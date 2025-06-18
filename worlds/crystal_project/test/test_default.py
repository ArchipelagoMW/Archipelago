from .bases import CrystalProjectTestBase
from ..constants.regions import *


class TestDefault(CrystalProjectTestBase):
    run_default_tests = True

    def test_region_accessibility(self):
        self.assertBeatable(False)
        self.collect_all_but("")
        self.assertBeatable(True)

    def test_base_functions(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.assert_region_entrances(JIDAMBA_TANGLE, (THE_OPEN_SEA,), (JIDAMBA_EACLANEYA,))
        self.assert_locations(["Spawning Meadows Chest - Jump on Nan"], ["Spawning Meadows NPC - Butterfly Goo"])