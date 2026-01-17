from .bases import CrystalProjectTestBase
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.mounts import *
from ..constants.ap_regions import *
from BaseClasses import CollectionState


class TestLevelGatingOff(CrystalProjectTestBase):
    options = {
        "level_gating": 0,
        "progressive_mount_mode": 0,
        "key_mode": 0,
        "kill_bosses_mode": 1
    }

    def test_region_accessibility(self):
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))

    def test_boss_accessibility(self):
        self.collect_mounts()
        self.collect(self.get_item_by_name(SKELETON_KEY))

        unreachable_locations = []
        reachable_locations = ["Soiled Den Boss - Bone Thief",
                                 "Delende Boss - Troll",
                                 "Quintar Sanctum Boss - Fancy Quintar",
                                 "Beaurior Rock Boss - Iguanadon & Iguanadin",
                                 "Shoudu Province NPC - 1 Sky Arena Win Prize",
                                 "Shoudu Province Chest - 5 Sky Arena Wins room 4",
                                 "Shoudu Province NPC - Gold in 8 Sky Arena Wins room 1",
                                 "The Depths Boss - The Devourer"]
        self.assert_locations(reachable_locations, unreachable_locations)

class TestLevelGatingLevelPasses(CrystalProjectTestBase):
    options = {
        "progressive_mount_mode": 0,
        "key_mode": 0,
        "kill_bosses_mode": 1
    }
    # Level gating defaults: Progressive Level Passes, Starting Level = 3, Progressive Level Size = 6
    def test_region_accessibility(self):
        # Ancient Reservoir Min Level = 33
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_progressive_levels(4)
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))

    def test_boss_accessibility(self):
        self.collect_mounts()
        self.collect(self.get_item_by_name(SKELETON_KEY))
        # Starting Level: 3, Progressive Level Size: 6
        # Bone Thief 12, Fancy Quintar 26, 1 Sky Arena 30 (but Shoudu is 36), Iganabros 40, 5 Sky Arena 44, Troll 50, 8 Sky Arena 54, The Devourer 65
        unreachable_locations = ["Soiled Den Boss - Bone Thief",
                                 "Quintar Sanctum Boss - Fancy Quintar",
                                 "Shoudu Province NPC - 1 Sky Arena Win Prize",
                                 "Beaurior Rock Boss - Iguanadon & Iguanadin",
                                 "Shoudu Province Chest - 5 Sky Arena Wins room 4",
                                 "Delende Boss - Troll",
                                 "Shoudu Province NPC - Gold in 8 Sky Arena Wins room 1",
                                 "The Depths Boss - The Devourer"]
        reachable_locations = []
        self.assert_locations(reachable_locations, unreachable_locations)
        # +2 Progressive Levels: 15
        self.collect_progressive_levels(2)
        expected_passing_location = "Soiled Den Boss - Bone Thief"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)
        # +2 Progressive Levels: 27
        self.collect_progressive_levels(2)
        expected_passing_location = "Quintar Sanctum Boss - Fancy Quintar"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)
        # +1 Progressive Level: 33
        # 1 sky arena win itself only requires level 30, but Shoudu is level 36
        self.collect_progressive_levels(1)
        self.assert_locations(reachable_locations, unreachable_locations)
        # +1 Progressive Level: 39
        self.collect_progressive_levels(1)
        expected_passing_location = "Shoudu Province NPC - 1 Sky Arena Win Prize"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)
        # +1 Progressive Level: 45
        self.collect_progressive_levels(1)
        expected_passing_location_a = "Beaurior Rock Boss - Iguanadon & Iguanadin"
        expected_passing_location_b = "Shoudu Province Chest - 5 Sky Arena Wins room 4"
        unreachable_locations.remove(expected_passing_location_a)
        unreachable_locations.remove(expected_passing_location_b)
        reachable_locations.extend([expected_passing_location_a, expected_passing_location_b])
        self.assert_locations(reachable_locations, unreachable_locations)
        # +1 Progressive Level: 51
        self.collect_progressive_levels(1)
        expected_passing_location = "Delende Boss - Troll"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)
        # +1 Progressive Level: 57
        self.collect_progressive_levels(1)
        expected_passing_location = "Shoudu Province NPC - Gold in 8 Sky Arena Wins room 1"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)
        # +1 Progressive Level: 60
        # The Devourer is above level 60, but by default that's the highest level a player can reach
        self.collect_progressive_levels(1)
        expected_passing_location = "The Depths Boss - The Devourer"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)

class TestLevelGatingLevelCapped(TestLevelGatingLevelPasses):
    options = {
        "level_gating": 2,
        "progressive_mount_mode": 0,
        "key_mode": 0,
        "kill_bosses_mode": 1
    }

class TestLevelGatingLevelCatchUp(TestLevelGatingLevelPasses):
    options = {
        "level_gating": 3,
        "progressive_mount_mode": 0,
        "key_mode": 0,
        "kill_bosses_mode": 1
    }

class TestMaxLevelIncrease(CrystalProjectTestBase):
    options = {
        "level_gating": 1,
        "max_level": 62,
        "progressive_mount_mode": 0,
        "key_mode": 0,
        "kill_bosses_mode": 1
    }

    def test_boss_above_level_60(self):
        self.collect_mounts()
        self.collect(self.get_item_by_name(SKELETON_KEY))
        # Starting Level: 3, Progressive Level Size: 6

        # The Devourer: 65
        unreachable_locations = ["The Depths Boss - The Devourer"]
        reachable_locations = []
        self.collect_progressive_levels(9)
        self.assert_locations(reachable_locations, unreachable_locations)
        self.collect_progressive_levels(1)
        expected_passing_location = "The Depths Boss - The Devourer"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)

    def test_region_above_level_60(self):
        self.collect_mounts()
        self.collect(self.get_item_by_name(SKELETON_KEY))
        # Starting Level: 3, Progressive Level Size: 6

        # The Depths: 63
        self.collect_progressive_levels(9)
        self.assertFalse(self.can_reach_region(THE_DEPTHS_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_region(THE_DEPTHS_AP_REGION))

class TestMaxLevelDecrease(CrystalProjectTestBase):
    options = {
        "level_gating": 1,
        "max_level": 3,
        "progressive_mount_mode": 0,
        "key_mode": 0,
        "kill_bosses_mode": 1
    }

    # you can do everything at level 3 B)
    def test_region_above_level_60(self):
        self.collect_mounts()
        self.collect(self.get_item_by_name(SKELETON_KEY))
        # The Depths: 63
        self.assertTrue(self.can_reach_region(THE_DEPTHS_AP_REGION))

    def test_number_of_progressive_levels_in_pool(self):
        # 0 Progressive Levels in the pool
        self.assertTrue(len(self.get_items_by_name(PROGRESSIVE_LEVEL)) == 0)
        starting_state: CollectionState = CollectionState(self.multiworld)
        # 0 pre-collected Progressive Levels
        self.assertTrue(starting_state.has(PROGRESSIVE_LEVEL, self.player, 0))
        self.assertFalse(starting_state.has(PROGRESSIVE_LEVEL, self.player, 1))

class TestProgressiveLevelSize(CrystalProjectTestBase):
    options = {
        "progressive_level_size": 10,
        "progressive_mount_mode": 0,
        "key_mode": 0,
    }

    def test_region_accessibility(self):
        self.collect_mounts()
        # Ancient Reservoir Min Level = 33; Starting Level: 3
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_progressive_levels(2)
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))

class TestLevelComparedToEnemiesIncrease(CrystalProjectTestBase):
    options = {
        "level_gating": 1,
        "level_compared_to_enemies": 5,
        "max_level": 62,
        "progressive_mount_mode": 0,
        "key_mode": 0,
        "kill_bosses_mode": 1
    }

    def test_region_accessibility(self):
        self.collect_mounts()
        # Ancient Reservoir Min Level = 33; +5 Level Compared to Enemies; Starting Level: 3 but player will start as 3+5 bc our starting level takes the max(starting level, region level + L.C.T.E.)
        # Progressive Level Size: 6
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_progressive_levels(4)
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))

    def test_region_above_level_60(self):
        self.collect_mounts()
        self.collect(self.get_item_by_name(SKELETON_KEY))
        # +5 Level Compared to Enemies; Starting Level: 3 but player will start as 3+5 bc our starting level takes the max(starting level, region level + L.C.T.E.); Progressive Level Size: 6

        # The Depths: 63
        self.collect_progressive_levels(8)
        self.assertFalse(self.can_reach_region(THE_DEPTHS_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_region(THE_DEPTHS_AP_REGION))

class TestLevelComparedToEnemiesDecrease(CrystalProjectTestBase):
    options = {
        "level_gating": 1,
        "level_compared_to_enemies": -5,
        "max_level": 62,
        "progressive_mount_mode": 0,
        "key_mode": 0,
        "kill_bosses_mode": 1
    }

    def test_region_accessibility(self):
        self.collect_mounts()
        # Ancient Reservoir Min Level = 33; -5 Level Compared to Enemies; Starting Level: 3 (our starting level takes the max(starting level, region level + L.C.T.E.), and the L.C.T.E. is negative this time)
        # Progressive Level Size: 6
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_progressive_levels(4)
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))

    def test_region_above_level_60(self):
        self.collect_mounts()
        self.collect(self.get_item_by_name(SKELETON_KEY))
        # -5 Level Compared to Enemies; Starting Level: 3 (our starting level takes the max(starting level, region level + L.C.T.E.), and the L.C.T.E. is negative this time); Progressive Level Size: 6

        # The Depths: 63
        # 62 - 5 = 58 capped at max level and adjusted for level compared to enemies
        # (58 - 3) / 6 = 10 progressive levels to reach the depths
        self.collect_progressive_levels(9)
        self.assertFalse(self.can_reach_region(THE_DEPTHS_AP_REGION))
        self.collect_progressive_levels(1)
        self.assertTrue(self.can_reach_region(THE_DEPTHS_AP_REGION))