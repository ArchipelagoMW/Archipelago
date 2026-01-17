from .bases import CrystalProjectTestBase
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.ap_regions import *
from ..items import key_rings, dungeon_keys

class MultiuseKeyMethods(CrystalProjectTestBase):
    def has_no_skeleton_key(self):
        self.assertTrue(self.count(SKELETON_KEY) == 0)

    def has_no_dungeon_keys(self):
        self.assertTrue(len(self.get_items_by_name(dungeon_keys)) == 0)

    def has_no_keyring(self):
        self.assertTrue(len(self.get_items_by_name(key_rings)) == 0)

    def has_skeleton_key(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        #Player can reach South Wing Rubble location without any prison keys if they go through the Tram
        unreachable_locations = ["Capital Sequoia Chest - Gardener's Shed 1",
                     "Capital Jail Chest - South Wing jail cell across from busted wall",
                     "Capital Jail Chest - West Wing jail cell among the glowy plants",
                     "Capital Jail Chest - Locked among the foliage in West Wing",
                     "Capital Jail Chest - Locked beyond overgrown West Wing hallway",
                     "Capital Jail Chest - East Wing bedroom closet twinsies the 1st",
                     "Capital Jail Chest - Locked in broken East Wing jail cell",
                     "Capital Jail Crystal - Reaper, above hell pool"]
        reachable_locations = ["Capital Jail Chest - Fiercely guarded and locked in South Wing rubble 1"]
        self.assert_locations(reachable_locations, unreachable_locations)

        self.collect(self.get_item_by_name(SKELETON_KEY))
        reachable_locations.extend(unreachable_locations)
        unreachable_locations = []
        self.assert_locations(reachable_locations, unreachable_locations)

    def has_singleton_key(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.assertFalse(self.can_reach_location("Capital Sequoia Chest - Gardener's Shed 1"))
        self.collect(self.get_item_by_name(GARDENERS_KEY))
        self.assertTrue(self.can_reach_location("Capital Sequoia Chest - Gardener's Shed 1"))

class TestSkeletonKeyMode(MultiuseKeyMethods):
    options = {
        "key_mode": 0
    }

    def test_has_skeleton_key(self):
        self.has_skeleton_key()

class TestKeyRings(MultiuseKeyMethods):
    run_default_tests = False

    options = {
        "key_mode": 1
    }

    def test_has_no_dungeon_keys(self):
        self.has_no_dungeon_keys()

    def test_has_skeleton_key(self, skeleton_key_bool = True):
        if skeleton_key_bool:
            self.has_skeleton_key()
        else:
            self.has_no_skeleton_key()

    def test_has_singleton_key(self):
        self.has_singleton_key()

    def test_has_prison_keyring(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.assertFalse(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect(self.get_item_by_name(PRISON_KEY_RING))
        self.assertTrue(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))

    def test_has_beaurior_keyring(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.assertFalse(self.can_reach_location("Beaurior Rock Chest - What's behind Door Number 3? Ominous lamp room!"))
        self.collect(self.get_item_by_name(BEAURIOR_KEY_RING))
        self.assertTrue(self.can_reach_location("Beaurior Rock Chest - What's behind Door Number 3? Ominous lamp room!"))

    def test_has_slip_glide_ride_keyring(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.assertFalse(self.can_reach_location("Slip Glide Ride Crystal - Summoner"))
        self.collect(self.get_item_by_name(SLIP_GLIDE_RIDE_KEY_RING))
        self.assertTrue(self.can_reach_location("Slip Glide Ride Crystal - Summoner"))

    def test_has_ice_puzzle_keyring(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.collect([self.get_item_by_name(VERMILLION_BOOK), self.get_item_by_name(VIRIDIAN_BOOK), self.get_item_by_name(CERULEAN_BOOK)])
        self.assertFalse(self.can_reach_location("Sequoia Athenaeum Chest - You expected another Chip's Challenge, but it was me, Dio!"))
        self.collect(self.get_item_by_name(ICE_PUZZLE_KEY_RING))
        self.assertTrue(self.can_reach_location("Sequoia Athenaeum Chest - You expected another Chip's Challenge, but it was me, Dio!"))

    def test_has_jidamba_keyring(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        self.assertFalse(self.can_reach_region(EACLANEYA_TRICKY_BLOCK_BRANCHES_AP_REGION))
        self.collect(self.get_item_by_name(JIDAMBA_KEY_RING))
        self.assertTrue(self.can_reach_region(EACLANEYA_TRICKY_BLOCK_BRANCHES_AP_REGION))

class TestVanillaKeys(MultiuseKeyMethods):
    run_default_tests = False

    options = {
        "key_mode": 2
    }

    def test_has_no_keyring(self):
        self.has_no_keyring()

    def test_has_skeleton_key(self, skeleton_key_bool = True):
        if skeleton_key_bool:
            self.has_skeleton_key()
        else:
            self.has_no_skeleton_key()

    def test_has_singleton_key(self):
        self.has_singleton_key()

    def test_has_prison_keys(self):
        self.collect_mounts_and_progressive_levels_and_passes()
        #Player can reach South Wing Rubble location without any prison keys if they go through the Tram
        unreachable_locations = ["Capital Jail Chest - South Wing jail cell across from busted wall",
                                 "Capital Jail Chest - West Wing jail cell among the glowy plants",
                                 "Capital Jail Chest - Locked among the foliage in West Wing",
                                 "Capital Jail Chest - Locked beyond overgrown West Wing hallway",
                                 "Capital Jail Chest - East Wing bedroom closet twinsies the 1st",
                                 "Capital Jail Chest - Locked in broken East Wing jail cell",
                                 "Capital Jail Crystal - Reaper, above hell pool"]
        reachable_locations = ["Capital Jail Chest - Fiercely guarded and locked in South Wing rubble 1"]
        self.assert_locations(reachable_locations, unreachable_locations)

        self.collect(self.get_item_by_name(SOUTH_WING_KEY))
        expected_passing_location = "Capital Jail Chest - South Wing jail cell across from busted wall"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)

        self.collect(self.get_item_by_name(CELL_KEY))
        self.assert_locations(reachable_locations, unreachable_locations)

        self.collect(self.get_item_by_name(WEST_WING_KEY))
        expected_passing_location = "Capital Jail Chest - West Wing jail cell among the glowy plants"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)

        self.collect(self.get_item_by_name(EAST_WING_KEY))
        expected_passing_location = "Capital Jail Chest - East Wing bedroom closet twinsies the 1st"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)

        self.collect(self.get_item_by_name(DARK_WING_KEY))
        expected_passing_location = "Capital Jail Crystal - Reaper, above hell pool"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)

        self.collect(self.get_item_by_name(CELL_KEY))
        self.collect(self.get_item_by_name(CELL_KEY))
        self.collect(self.get_item_by_name(CELL_KEY))
        expected_passing_location = "Capital Jail Chest - Locked among the foliage in West Wing"
        unreachable_locations.remove(expected_passing_location)
        reachable_locations.extend([expected_passing_location])
        self.assert_locations(reachable_locations, unreachable_locations)

        self.collect_by_name(CELL_KEY)
        expected_passing_location_a = "Capital Jail Chest - Locked beyond overgrown West Wing hallway"
        expected_passing_location_b = "Capital Jail Chest - Locked in broken East Wing jail cell"
        unreachable_locations.remove(expected_passing_location_a)
        unreachable_locations.remove(expected_passing_location_b)
        reachable_locations.extend([expected_passing_location_a, expected_passing_location_b])
        self.assert_locations(reachable_locations, unreachable_locations)

class TestKeyRingsSkeleFree(TestKeyRings):
    run_default_tests = False

    options = {
        "key_mode": 3
    }

    def test_has_no_dungeon_keys(self):
        self.has_no_dungeon_keys()

    def test_has_skeleton_key(self, skeleton_key_bool = False):
        TestKeyRings.test_has_skeleton_key(self, skeleton_key_bool)

    def test_has_singleton_key(self):
        self.has_singleton_key()

    def test_has_prison_keyring(self):
        TestKeyRings.test_has_prison_keyring(self)

    def test_has_beaurior_keyring(self):
        TestKeyRings.test_has_beaurior_keyring(self)

    def test_has_slip_glide_ride_keyring(self):
        TestKeyRings.test_has_slip_glide_ride_keyring(self)

    def test_has_ice_puzzle_keyring(self):
        TestKeyRings.test_has_ice_puzzle_keyring(self)

    def test_has_jidamba_keyring(self):
        TestKeyRings.test_has_jidamba_keyring(self)

class TestVanillaKeysSkeleFree(TestVanillaKeys):
    run_default_tests = False

    options = {
        "key_mode": 4
    }

    def test_has_no_skeleton_key(self):
        self.has_no_skeleton_key()

    def test_has_no_keyring(self):
        self.has_no_keyring()

    def test_has_skeleton_key(self, skeleton_key_bool = False):
        TestVanillaKeys.test_has_skeleton_key(self, skeleton_key_bool)

    def test_has_singleton_key(self):
        self.has_singleton_key()

    def test_has_prison_keys(self):
        TestVanillaKeys.test_has_prison_keys(self)