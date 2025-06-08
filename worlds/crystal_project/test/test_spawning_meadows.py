from ..constants.regions import *
from ..constants.key_items import *
from .bases import CrystalProjectTestBase

class TestSpawningMeadows(CrystalProjectTestBase):
    run_default_tests = False

    def test_region_accessibility(self):
        self.assertTrue(self.can_reach_region(SPAWNING_MEADOWS))

    def test_region_connections_no_items(self):
        self.assert_region_entrances(SPAWNING_MEADOWS, reachable_regions=(DELENDE,), unreachable_regions=(MERCURY_SHRINE,POKO_POKO_DESERT,CONTINENTAL_TRAM,BEAURIOR_VOLCANO,YAMAGAWA_MA))

class TestSpawningMeadowsConnectionRulesNoLevelGating(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "levelGating": 0,
    }

    def test_mercury_shrine_connection(self):
        self.collect_by_name("Item - Ibek Bell")
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + MERCURY_SHRINE))

    def test_poko_poko_connection(self):
        self.collect_by_name("Item - Ibek Bell")
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + POKO_POKO_DESERT))

    def test_tram_connection(self):
        self.collect_by_name("Item - Progressive Salmon Violin")
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + CONTINENTAL_TRAM))

    def test_volcano_connection(self):
        self.collect_by_name("Item - Ibek Bell")
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + BEAURIOR_VOLCANO))

    def test_yamagawa_connection_vertical_movement(self):
        self.collect_by_name("Item - Ibek Bell")
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + YAMAGAWA_MA))

    def test_yamagawa_connection_swimming_salmon(self):
        self.collect_by_name("Item - Progressive Salmon Violin")
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + YAMAGAWA_MA))

    def test_yamagawa_connection_swimming_quintar(self):
        self.collect_by_name(["Item - Progressive Quintar Flute","Item - Progressive Quintar Flute","Item - Progressive Quintar Flute"])
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + YAMAGAWA_MA))

class TestSpawningMeadowsConnectionRulesWithLevelGating(CrystalProjectTestBase):
    run_default_tests = False
    
    options = {
        "levelGating": 1,
    }

    def test_poko_poko_connection_fails_with_ibek_no_level_cap(self):
        self.collect_by_name("Item - Ibek Bell")
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + POKO_POKO_DESERT))

    def test_poko_poko_connection_fails_with_level_cap_no_ibek(self):
        self.collect_by_name([PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + POKO_POKO_DESERT))

    def test_poko_poko_connection_succeeds_with_ibek_and_level_cap(self):
        self.collect_by_name("Item - Ibek Bell")
        self.collect_by_name([PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + POKO_POKO_DESERT))

    def test_tram_connection_fails_with_salmon_no_level_cap(self):
        self.collect_by_name("Item - Progressive Salmon Violin")
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + CONTINENTAL_TRAM))

    def test_tram_connection_fails_with_quintar_no_level_cap(self):
        self.collect_by_name(["Item - Progressive Quintar Flute", "Item - Progressive Quintar Flute","Item - Progressive Quintar Flute"])
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + CONTINENTAL_TRAM))

    def test_tram_connection_fails_with_level_cap_no_swimming(self):
        self.collect_by_name([PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + CONTINENTAL_TRAM))

    def test_tram_connection_succeeds_with_salmon_and_level_cap(self):
        self.collect_by_name("Item - Progressive Salmon Violin")
        self.collect_by_name([PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + CONTINENTAL_TRAM))

    def test_tram_connection_succeeds_with_quintar_and_level_cap(self):
        self.collect_by_name(["Item - Progressive Quintar Flute", "Item - Progressive Quintar Flute","Item - Progressive Quintar Flute"])
        self.collect_by_name([PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS + " -> " + CONTINENTAL_TRAM))