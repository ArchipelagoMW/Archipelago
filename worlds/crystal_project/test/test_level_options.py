from ..constants.key_items import *
from ..constants.keys import *
from ..constants.regions import *
from .bases import CrystalProjectTestBase


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