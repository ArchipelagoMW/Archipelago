from .bases import CrystalProjectTestBase
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.regions import *


class TestLevelGatingOff(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "levelGating": 0,
    }

    def test_region_accessibility(self):
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR))
        self.collect_by_name("Item - Progressive Salmon Violin")
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR))

class TestLevelGatingOn(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "levelGating": 1,
    }

    def test_region_accessibility(self):
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR))
        self.collect_by_name("Item - Progressive Salmon Violin")
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR))
        self.collect_by_name([PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR))

    # leaving this on temporarily so you can see an example with things like how to make a tuple with only one element etc, delete once we have more tests using assert_region_entrances
    def test_new_function_test(self):
        self.assert_region_entrances(IBEK_CAVE, unreachable_regions=(SARA_SARA_BEACH,))
        self.collect_by_name("Item - Ibek Bell")
        self.collect_by_name([PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assert_region_entrances(IBEK_CAVE, reachable_regions=(SARA_SARA_BEACH,))
