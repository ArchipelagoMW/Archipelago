from .bases import CrystalProjectTestBase
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.mounts import *
from ..constants.regions import *
from ..constants.teleport_stones import *

class TestVanillaKeys(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "keyMode": 2,
    }

    def test_has_key(self):
        self.collect_mounts_and_level_caps()
        self.assertFalse(self.can_reach_location("Capital Sequoia Chest - Gardeners Shed 1"))
        self.collect(self.get_item_by_name(GARDENERS_KEY))
        self.assertTrue(self.can_reach_location("Capital Sequoia Chest - Gardeners Shed 1"))

    def test_has_prison_keys(self):
        self.collect_mounts_and_level_caps()
        self.assertFalse(self.can_reach_location("Capital Jail Chest - South Wing jail cell across from busted wall"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - West Wing jail cell among the glowy plants"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked among the foliage in West Wing"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked beyond overgrown West Wing hallway"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - East Wing bedroom closet twinsies the 1st"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked in broken East Wing jail cell"))
        self.assertFalse(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect(self.get_item_by_name(SOUTH_WING_KEY))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - South Wing jail cell across from busted wall"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - West Wing jail cell among the glowy plants"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked among the foliage in West Wing"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked beyond overgrown West Wing hallway"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - East Wing bedroom closet twinsies the 1st"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked in broken East Wing jail cell"))
        self.assertFalse(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect(self.get_item_by_name(CELL_KEY))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - South Wing jail cell across from busted wall"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - West Wing jail cell among the glowy plants"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked among the foliage in West Wing"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked beyond overgrown West Wing hallway"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - East Wing bedroom closet twinsies the 1st"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked in broken East Wing jail cell"))
        self.assertFalse(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect(self.get_item_by_name(WEST_WING_KEY))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - South Wing jail cell across from busted wall"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - West Wing jail cell among the glowy plants"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked among the foliage in West Wing"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked beyond overgrown West Wing hallway"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - East Wing bedroom closet twinsies the 1st"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked in broken East Wing jail cell"))
        self.assertFalse(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect(self.get_item_by_name(EAST_WING_KEY))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - South Wing jail cell across from busted wall"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - West Wing jail cell among the glowy plants"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked among the foliage in West Wing"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked beyond overgrown West Wing hallway"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - East Wing bedroom closet twinsies the 1st"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked in broken East Wing jail cell"))
        self.assertFalse(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect(self.get_item_by_name(DARK_WING_KEY))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - South Wing jail cell across from busted wall"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - West Wing jail cell among the glowy plants"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked among the foliage in West Wing"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked beyond overgrown West Wing hallway"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - East Wing bedroom closet twinsies the 1st"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked in broken East Wing jail cell"))
        self.assertTrue(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect(self.get_item_by_name(CELL_KEY))
        self.collect(self.get_item_by_name(CELL_KEY))
        self.collect(self.get_item_by_name(CELL_KEY))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - South Wing jail cell across from busted wall"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - West Wing jail cell among the glowy plants"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - Locked among the foliage in West Wing"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked beyond overgrown West Wing hallway"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - East Wing bedroom closet twinsies the 1st"))
        self.assertFalse(self.can_reach_location("Capital Jail Chest - Locked in broken East Wing jail cell"))
        self.assertTrue(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect_by_name(CELL_KEY)
        self.assertTrue(self.can_reach_location("Capital Jail Chest - South Wing jail cell across from busted wall"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - West Wing jail cell among the glowy plants"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - Locked among the foliage in West Wing"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - Locked beyond overgrown West Wing hallway"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - East Wing bedroom closet twinsies the 1st"))
        self.assertTrue(self.can_reach_location("Capital Jail Chest - Locked in broken East Wing jail cell"))
        self.assertTrue(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))

class TestKeyRings(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "keyMode": 1
    }

    def test_has_key(self):
        self.collect_mounts_and_level_caps()
        self.assertFalse(self.can_reach_location("Capital Sequoia Chest - Gardeners Shed 1"))
        self.collect(self.get_item_by_name(GARDENERS_KEY))
        self.assertTrue(self.can_reach_location("Capital Sequoia Chest - Gardeners Shed 1"))

    def test_has_prison_keyring(self):
        self.collect_mounts_and_level_caps()
        self.assertFalse(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect(self.get_item_by_name(PRISON_KEY_RING))
        self.assertTrue(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))

    def test_has_beaurior_keyring(self):
        self.collect_mounts_and_level_caps()
        self.assertFalse(self.can_reach_location("Beaurior Volcano Crystal - Valkyrie"))
        self.collect(self.get_item_by_name(BEAURIOR_KEY_RING))
        self.assertTrue(self.can_reach_location("Beaurior Volcano Crystal - Valkyrie"))

    def test_has_slip_glide_ride_keyring(self):
        self.collect_mounts_and_level_caps()
        self.assertFalse(self.can_reach_location("Slip Glide Ride Crystal - Summoner"))
        self.collect(self.get_item_by_name(SLIP_GLIDE_RIDE_KEY_RING))
        self.assertTrue(self.can_reach_location("Slip Glide Ride Crystal - Summoner"))

    def test_has_ice_puzzle_keyring(self):
        self.collect_mounts_and_level_caps()
        self.collect([self.get_item_by_name(VERMILLION_BOOK), self.get_item_by_name(VIRIDIAN_BOOK), self.get_item_by_name(CERULEAN_BOOK)])
        self.assertFalse(self.can_reach_location("Sequoia Athenaeum Chest - You expected another Chips Challenge, but it was me, Dio!"))
        self.collect(self.get_item_by_name(ICE_PUZZLE_KEY_RING))
        self.assertTrue(self.can_reach_location("Sequoia Athenaeum Chest - You expected another Chips Challenge, but it was me, Dio!"))

    def test_has_jidamba_keyring(self):
        self.collect_mounts_and_level_caps()
        self.assertFalse(self.can_reach_region(JIDAMBA_EACLANEYA))
        self.collect(self.get_item_by_name(JIDAMBA_KEY_RING))
        self.assertTrue(self.can_reach_region(JIDAMBA_EACLANEYA))