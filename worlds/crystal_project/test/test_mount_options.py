from .bases import CrystalProjectTestBase
from ..constants.teleport_stones import *
from ..constants.key_items import *
from ..constants.mounts import *
from ..constants.ap_regions import *


class TestProgressiveMountModeOn(CrystalProjectTestBase):
    options = {
        "progressive_mount_mode": 1,
        "level_gating": 0,
    }

    def test_quintar_pass(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.assertFalse(self.can_reach_region(CAPITAL_JAIL_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(CAPITAL_JAIL_AP_REGION))

    def test_quintar_flute(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(SALMON_RIVER_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(SALMON_RIVER_AP_REGION))

    def test_ibek_bell(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(SOUVENIR_SHOP_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(SOUVENIR_SHOP_AP_REGION))

    def test_owl_drum(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(JIDAMBA_FOREST_FLOOR_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(JIDAMBA_FOREST_FLOOR_AP_REGION))

    def test_salmon_violin(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertFalse(self.can_reach_region(THE_OPEN_SEA_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(THE_OPEN_SEA_AP_REGION))

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
        self.assertFalse(self.can_reach_region(THE_SEQUOIA_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.assertTrue(self.can_reach_region(THE_SEQUOIA_AP_REGION))

class TestProgressiveMountModeOff(CrystalProjectTestBase):
    options = {
        "progressive_mount_mode": 0,
        "level_gating": 0,
    }

    def test_quintar_pass(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.assertFalse(self.can_reach_region(CAPITAL_JAIL_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertTrue(self.can_reach_region(CAPITAL_JAIL_AP_REGION))

    def test_quintar_flute(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertFalse(self.can_reach_region(SALMON_RIVER_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertTrue(self.can_reach_region(SALMON_RIVER_AP_REGION))

    def test_ibek_bell(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.assertFalse(self.can_reach_region(GREENSHIRE_OVERLOOK_AP_REGION))
        self.collect(self.get_item_by_name(IBEK_BELL))
        self.assertTrue(self.can_reach_region(GREENSHIRE_OVERLOOK_AP_REGION))

    def test_owl_drum(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.assertFalse(self.can_reach_region(JIDAMBA_FOREST_FLOOR_AP_REGION))
        self.collect(self.get_item_by_name(OWL_DRUM))
        self.assertTrue(self.can_reach_region(JIDAMBA_FOREST_FLOOR_AP_REGION))

    def test_salmon_violin(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.assertFalse(self.can_reach_region(THE_OPEN_SEA_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_SALMON_VIOLA))
        self.assertTrue(self.can_reach_region(THE_OPEN_SEA_AP_REGION))

    def test_quintar_ocarina(self):
        self.set_collected_job_count(18)
        self.collect_by_name(GAEA_STONE)
        self.collect_by_name(DIONE_STONE)
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertFalse(self.can_reach_region(THE_SEQUOIA_AP_REGION))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assertTrue(self.can_reach_region(THE_SEQUOIA_AP_REGION))