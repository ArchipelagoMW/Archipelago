from .bases import CrystalProjectTestBase
from ..constants.region_passes import *

class TestCanEarnMoney(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "shopsanity" : 1,
        "regionsanity" : 1,
        "start_inventory_from_pool": {PROVING_MEADOWS_PASS : 1}
    }

    def test_can_earn_money(self):
        self.collect_all_progressive_levels()
        self.assertTrue(self.can_reach_location("Proving Meadows Chest - Tarzan"))
        self.assertFalse(self.can_reach_location("Proving Meadows Shop - Item Merchant 1"))
        self.collect_by_name(THE_PALE_GROTTO_PASS)
        self.assertTrue(self.can_reach_location("Proving Meadows Shop - Item Merchant 1"))