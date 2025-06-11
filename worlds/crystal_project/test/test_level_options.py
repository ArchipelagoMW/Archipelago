from .bases import CrystalProjectTestBase
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.mounts import *
from ..constants.regions import *


class TestLevelGatingOff(CrystalProjectTestBase):
    options = {
        "levelGating": 0,
    }

    def test_region_accessibility(self):
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR))
        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR))

class TestLevelGatingOn(CrystalProjectTestBase):
    options = {
        "levelGating": 1,
    }

    def test_region_accessibility(self):
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR))
        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR))
        self.collect(self.get_item_by_name(PROGRESSIVE_LEVEL_CAP))
        self.collect(self.get_item_by_name(PROGRESSIVE_LEVEL_CAP))
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR))
        self.collect(self.get_item_by_name(PROGRESSIVE_LEVEL_CAP))
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR))
