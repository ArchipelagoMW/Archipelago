from .bases import CrystalProjectTestBase
from ..constants.ap_regions import *


class TestDefault(CrystalProjectTestBase):
    run_default_tests = True

    def test_region_accessibility(self):
        self.assertBeatable(False)
        self.collect_all_but("")
        self.assertBeatable(True)

    def test_base_functions(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.assert_region_entrances(JIDAMBA_WATERWAYS_AP_REGION, (THE_OPEN_SEA_AP_REGION,))
        self.assert_region_entrances(TANGLE_EACLANEYA_CONNECTOR_AP_REGION, (), (EACLANEYA_ENTRANCE_AP_REGION,))
        self.assert_locations(["Spawning Meadows Chest - Jump on Nan"], ["Spawning Meadows NPC - Butterfly Goo"])