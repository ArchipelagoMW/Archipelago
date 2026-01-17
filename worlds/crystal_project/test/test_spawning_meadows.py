from ..constants.ap_regions import *
from ..constants.mounts import *
from .bases import CrystalProjectTestBase

class TestSpawningMeadows(CrystalProjectTestBase):
    def test_region_accessibility(self):
        self.assertTrue(self.can_reach_region(SPAWNING_MEADOWS_AP_REGION))

    def test_region_connections_no_items(self):
        self.assert_region_entrances(SPAWNING_MEADOWS_AP_REGION, reachable_regions=(), unreachable_regions=(DELENDE_PLAINS_AP_REGION, MERCURY_SHRINE_AP_REGION, POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION, CONTINENTAL_TRAM_AP_REGION, VALKYRIE_WATCHTOWER_AP_REGION, YAMAGAWA_MA_AP_REGION))

class TestSpawningMeadowsObscureRoutes(CrystalProjectTestBase):
    options = {
        "level_gating": 0,
        "progressive_mount_mode": 0,
        "obscure_routes": 1
    }

    def test_obscure_routes(self):
        unreachable_regions = (MERCURY_SHRINE_AP_REGION, CONTINENTAL_TRAM_AP_REGION, VALKYRIE_WATCHTOWER_AP_REGION, YAMAGAWA_MA_AP_REGION)
        reachable_regions = (DELENDE_PLAINS_AP_REGION, POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION,)
        self.assert_region_entrances(SPAWNING_MEADOWS_AP_REGION, reachable_regions, unreachable_regions)

        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        unreachable_regions = (MERCURY_SHRINE_AP_REGION, VALKYRIE_WATCHTOWER_AP_REGION)
        reachable_regions = (DELENDE_PLAINS_AP_REGION, POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION, CONTINENTAL_TRAM_AP_REGION, YAMAGAWA_MA_AP_REGION)
        self.assert_region_entrances(SPAWNING_MEADOWS_AP_REGION, reachable_regions, unreachable_regions)

class TestSpawningMeadowsNoObscureRoutes(CrystalProjectTestBase):
    options = {
        "level_gating": 0,
        "progressive_mount_mode": 0,
        "obscure_routes": 0
    }

    def test_obscure_routes(self):
        unreachable_regions = (MERCURY_SHRINE_AP_REGION, POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION, CONTINENTAL_TRAM_AP_REGION, VALKYRIE_WATCHTOWER_AP_REGION, YAMAGAWA_MA_AP_REGION)
        reachable_regions = (DELENDE_PLAINS_AP_REGION,)
        self.assert_region_entrances(SPAWNING_MEADOWS_AP_REGION, reachable_regions, unreachable_regions)

        self.collect(self.get_item_by_name(IBEK_BELL))
        unreachable_regions = (CONTINENTAL_TRAM_AP_REGION,)
        reachable_regions = (DELENDE_PLAINS_AP_REGION, MERCURY_SHRINE_AP_REGION, POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION, VALKYRIE_WATCHTOWER_AP_REGION, YAMAGAWA_MA_AP_REGION)
        self.assert_region_entrances(SPAWNING_MEADOWS_AP_REGION, reachable_regions, unreachable_regions)

        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        unreachable_regions = (CONTINENTAL_TRAM_AP_REGION,)
        reachable_regions = (DELENDE_PLAINS_AP_REGION, MERCURY_SHRINE_AP_REGION, POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION, VALKYRIE_WATCHTOWER_AP_REGION, YAMAGAWA_MA_AP_REGION)
        self.assert_region_entrances(SPAWNING_MEADOWS_AP_REGION, reachable_regions, unreachable_regions)

        self.collect_mounts()
        unreachable_regions = (CONTINENTAL_TRAM_AP_REGION,)
        reachable_regions = (DELENDE_PLAINS_AP_REGION, MERCURY_SHRINE_AP_REGION, POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION, VALKYRIE_WATCHTOWER_AP_REGION, YAMAGAWA_MA_AP_REGION)
        self.assert_region_entrances(SPAWNING_MEADOWS_AP_REGION, reachable_regions, unreachable_regions)

class TestSpawningMeadowsConnectionRulesNoLevelGating(CrystalProjectTestBase):
    options = {
        "level_gating": 0,
        "progressive_mount_mode": 0,
        "obscure_routes": 0
    }

    def test_mercury_shrine_connection(self):
        self.collect_by_name(IBEK_BELL)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + MERCURY_SHRINE_AP_REGION))

    def test_poko_poko_connection(self):
        self.collect_by_name(IBEK_BELL)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION))

    def test_tram_connection(self):
        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + CONTINENTAL_TRAM_AP_REGION))

    def test_volcano_connection(self):
        self.collect_by_name(IBEK_BELL)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + VALKYRIE_WATCHTOWER_AP_REGION))

    def test_yamagawa_connection_vertical_movement(self):
        self.collect_by_name(IBEK_BELL)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))

    def test_yamagawa_connection_swimming_salmon(self):
        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))

    def test_yamagawa_connection_swimming_quintar(self):
        self.collect_by_name([PROGRESSIVE_QUINTAR_WOODWIND])
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))

class TestSpawningMeadowsConnectionRulesWithLevelGating(CrystalProjectTestBase):
    options = {
        "level_gating": 1,
        "progressive_mount_mode": 0,
        "obscure_routes": 0
    }
    # Starting Level: 3, Default Progressive Level Size: 6
    # Poko Poko Desert: 30
    def test_poko_poko_connection_fails_with_ibek_no_progressive_levels(self):
        self.collect_by_name(IBEK_BELL)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION))

    def test_poko_poko_connection_fails_with_enough_levels_no_ibek(self):
        self.collect_progressive_levels(5)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION))

    def test_poko_poko_connection_succeeds_with_ibek_and_enough_levels(self):
        self.collect_by_name(IBEK_BELL)
        self.collect_progressive_levels(4)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + POKO_POKO_SPAWNING_MEADOWS_PASS_AP_REGION))

    # Continental Tram
    def test_tram_connection_fails_with_obscure_routes_off(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + CONTINENTAL_TRAM_AP_REGION))

    # Beaurior Volcano: 37
    def test_beaurior_volcano_fails_with_ibek_no_progressive_levels(self):
        self.collect_by_name([IBEK_BELL])
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + VALKYRIE_WATCHTOWER_AP_REGION))

    def test_beaurior_volcano_connection_fails_with_enough_levels_no_ibek(self):
        self.collect_progressive_levels(6)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + VALKYRIE_WATCHTOWER_AP_REGION))

    def test_beaurior_connection_succeeds_with_ibek_and_enough_levels(self):
        self.collect_by_name(IBEK_BELL)
        self.collect_progressive_levels(5)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + VALKYRIE_WATCHTOWER_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + VALKYRIE_WATCHTOWER_AP_REGION))

    # Yamagawa M.A.: 15
    def test_yamagawa_connection_fails_with_mounts_no_progressive_levels(self):
        self.collect_mounts()
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))

    def test_yamagawa_connection_fails_with_enough_levels_no_mounts(self):
        self.collect_all_progressive_levels()
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))

    def test_yamagawa_connection_succeeds_with_enough_levels_and_ibek(self):
        self.collect_by_name([IBEK_BELL])
        self.collect_progressive_levels(1)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))

    def test_yamagawa_connection_succeeds_with_enough_levels_and_salmon(self):
        self.collect_by_name([PROGRESSIVE_SALMON_VIOLA])
        self.collect_progressive_levels(1)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))

    def test_yamagawa_connection_succeeds_with_enough_levels_and_quintar(self):
        self.collect_by_name([PROGRESSIVE_QUINTAR_WOODWIND])
        self.collect_progressive_levels(1)
        self.assertFalse(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_entrance(SPAWNING_MEADOWS_AP_REGION + " -> " + YAMAGAWA_MA_AP_REGION))