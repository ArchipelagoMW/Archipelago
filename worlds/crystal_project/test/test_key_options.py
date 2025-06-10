from .bases import CrystalProjectTestBase
from .. import GAEA_STONE
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.mounts import *
from ..constants.regions import *


class TestVanillaKeys(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "keyMode": 2,
    }

    def test_has_key(self):
        self.collect_by_name([GAEA_STONE, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertFalse(self.can_reach_location("Capital Sequoia Chest - Gardeners Shed 1"))
        self.collect_by_name(GARDENERS_KEY)
        self.assertTrue(self.can_reach_location("Capital Sequoia Chest - Gardeners Shed 1"))

class TestKeyRings(CrystalProjectTestBase):
    run_default_tests = False

    options = {
        "keyMode": 1
    }

    def test_has_prison_keyring(self):
        self.collect_by_name([PROGRESSIVE_SALMON_VIOLA, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertFalse(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))
        self.collect_by_name(PRISON_KEY_RING)
        self.assertTrue(self.can_reach_location("Capital Jail Crystal - Reaper, above hell pool"))

    def test_has_beaurior_keyring(self):
        self.collect_by_name([IBEK_BELL, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertFalse(self.can_reach_location("Beaurior Volcano Crystal - Valkyrie"))
        self.collect_by_name(BEAURIOR_KEY_RING)
        self.assertTrue(self.can_reach_location("Beaurior Volcano Crystal - Valkyrie"))

    def test_has_slip_glide_ride_keyring(self):
        self.collect_by_name([OWL_DRUM, IBEK_BELL, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP, PROGRESSIVE_LEVEL_CAP])
        self.assertFalse(self.can_reach_location("Slip Glide Ride Crystal - Summoner"))
        self.collect_by_name(SLIP_GLIDE_RIDE_KEY_RING)
        self.assertTrue(self.can_reach_location("Slip Glide Ride Crystal - Summoner"))
