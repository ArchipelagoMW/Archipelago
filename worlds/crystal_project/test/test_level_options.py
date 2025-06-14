from .bases import CrystalProjectTestBase
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.mounts import *
from ..constants.regions import *


class TestLevelGatingOff(CrystalProjectTestBase):
    options = {
        "levelGating": 0,
        "progressiveMountMode": 0,
        "keyMode": 0,
        "killBossesMode": 1
    }

    def test_region_accessibility(self):
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR))
        self.collect_by_name(PROGRESSIVE_SALMON_VIOLA)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR))

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

class TestLevelGatingOn(CrystalProjectTestBase):
    options = {
        "levelGating": 1,
        "progressiveMountMode": 0,
        "keyMode": 0,
        "killBossesMode": 1
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

    def test_boss_accessibility(self):
        self.collect_mounts()
        self.collect(self.get_item_by_name(SKELETON_KEY))
        # Max level: 10
        unreachable_locations = ["Soiled Den Boss - Bone Thief",
                                 "Delende Boss - Troll",
                                 "Quintar Sanctum Boss - Fancy Quintar",
                                 "Beaurior Rock Boss - Iguanadon & Iguanadin",
                                 "Shoudu Province NPC - 1 Sky Arena Win Prize",
                                 "Shoudu Province Chest - 5 Sky Arena Wins room 4",
                                 "Shoudu Province NPC - Gold in 8 Sky Arena Wins room 1",
                                 "The Depths Boss - The Devourer"]
        reachable_locations = []
        self.assert_locations(reachable_locations, unreachable_locations)
        # Max level: 20
        self.collect(self.get_item_by_name(PROGRESSIVE_LEVEL_CAP))
        expected_passing_location = "Soiled Den Boss - Bone Thief"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)
        # Max level: 30
        self.collect(self.get_item_by_name(PROGRESSIVE_LEVEL_CAP))
        expected_passing_location = "Quintar Sanctum Boss - Fancy Quintar"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)
        # Max level: 40
        self.collect(self.get_item_by_name(PROGRESSIVE_LEVEL_CAP))
        expected_passing_location_a = "Beaurior Rock Boss - Iguanadon & Iguanadin"
        #1 sky arena win only takes level 30, but Shoudu is level 36
        expected_passing_location_b = "Shoudu Province NPC - 1 Sky Arena Win Prize"
        unreachable_locations.remove(expected_passing_location_a)
        unreachable_locations.remove(expected_passing_location_b)
        reachable_locations.extend([expected_passing_location_a, expected_passing_location_b])
        self.assert_locations(reachable_locations, unreachable_locations)
        # Max level: 50
        self.collect(self.get_item_by_name(PROGRESSIVE_LEVEL_CAP))
        expected_passing_location_a = "Delende Boss - Troll"
        expected_passing_location_b = "Shoudu Province Chest - 5 Sky Arena Wins room 4"
        unreachable_locations.remove(expected_passing_location_a)
        unreachable_locations.remove(expected_passing_location_b)
        reachable_locations.extend([expected_passing_location_a, expected_passing_location_b])
        self.assert_locations(reachable_locations, unreachable_locations)
        # Max level: 60
        self.collect(self.get_item_by_name(PROGRESSIVE_LEVEL_CAP))
        expected_passing_location_a = "Shoudu Province NPC - Gold in 8 Sky Arena Wins room 1"
        expected_passing_location_b = "The Depths Boss - The Devourer"
        unreachable_locations.remove(expected_passing_location_a)
        unreachable_locations.remove(expected_passing_location_b)
        reachable_locations.extend([expected_passing_location_a, expected_passing_location_b])
        self.assert_locations(reachable_locations, unreachable_locations)