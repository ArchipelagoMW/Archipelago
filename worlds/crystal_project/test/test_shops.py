from .bases import CrystalProjectTestBase
from ..constants.region_passes import *
from ..constants.display_regions import *
from ..constants.mounts import *

class TestCanEarnMoneyBasic(CrystalProjectTestBase):
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
        self.collect_by_name(DELENDE_PASS)
        self.collect_by_name(THE_PALE_GROTTO_PASS)
        self.assertTrue(self.can_reach_location("Proving Meadows Shop - Item Merchant 1"))

class TestCanEarnMoneySaraSara(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "shopsanity" : 1,
        "regionsanity" : 1,
        "start_inventory_from_pool": {SARA_SARA_BEACH_PASS : 1}
    }

    def test_can_earn_money(self):
        self.collect_all_progressive_levels()
        #the default unit test setup does not process start inventory so i need to have the pass here too (and i have to add it bc it's not in the pool since it's in the starting inventory)
        self.multiworld.state.add_item(SARA_SARA_BEACH_PASS, self.player)
        self.collect(self.get_item_by_name(SARA_SARA_BAZAAR_PASS))
        self.assertFalse(self.can_reach_location(SARA_SARA_BEACH_DISPLAY_NAME + " Chest - Silver-crossed palm chest"))
        self.assertFalse(self.can_reach_location(SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Old Nan's Stew Subsidiary"))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_location(SARA_SARA_BEACH_DISPLAY_NAME + " Chest - Silver-crossed palm chest"))
        self.assertTrue(self.can_reach_location(SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Old Nan's Stew Subsidiary"))