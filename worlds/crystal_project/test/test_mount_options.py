from .bases import CrystalProjectTestBase
from ..constants.teleport_stones import *
from ..constants.key_items import *
from ..constants.mounts import *
from ..constants.regions import *


class TestProgressiveMountModeOn(CrystalProjectTestBase):
    options = {
        "progressiveMountMode": 1,
        "levelGating": 0,
    }

    def test_quintar_pass(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.assertFalse(self.can_reach_region(CAPITAL_JAIL))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(CAPITAL_JAIL))

    def test_quintar_flute(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(SALMON_RIVER))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(SALMON_RIVER))

    def test_ibek_bell(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(TALL_TALL_HEIGHTS))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(TALL_TALL_HEIGHTS))

    def test_owl_drum(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(JIDAMBA_TANGLE))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(JIDAMBA_TANGLE))

    def test_salmon_violin(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(THE_OPEN_SEA))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(THE_OPEN_SEA))

    def test_quintar_ocarina(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(THE_SEQUOIA))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(THE_SEQUOIA))

class TestProgressiveMountModeOff(CrystalProjectTestBase):
    options = {
        "progressiveMountMode": 0,
        "levelGating": 0,
    }

    def test_quintar_pass(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.assertFalse(self.can_reach_region(CAPITAL_JAIL))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertTrue(self.can_reach_region(CAPITAL_JAIL))

    def test_quintar_flute(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertFalse(self.can_reach_region(SALMON_RIVER))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertTrue(self.can_reach_region(SALMON_RIVER))

    def test_ibek_bell(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.assertFalse(self.can_reach_region(TALL_TALL_HEIGHTS))
        self.collect(self.get_item_by_name(IBEK_BELL))
        self.assertTrue(self.can_reach_region(TALL_TALL_HEIGHTS))

    def test_owl_drum(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.assertFalse(self.can_reach_region(JIDAMBA_TANGLE))
        self.collect(self.get_item_by_name(OWL_DRUM))
        self.assertTrue(self.can_reach_region(JIDAMBA_TANGLE))

    def test_salmon_violin(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.assertFalse(self.can_reach_region(THE_OPEN_SEA))
        self.collect(self.get_item_by_name(PROGRESSIVE_SALMON_VIOLA))
        self.assertTrue(self.can_reach_region(THE_OPEN_SEA))

    def test_quintar_ocarina(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertFalse(self.can_reach_region(THE_SEQUOIA))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertTrue(self.can_reach_region(THE_SEQUOIA))